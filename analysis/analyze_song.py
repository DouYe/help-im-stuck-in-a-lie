"""Music analysis for the real song, numpy/scipy only (no ML models available here).

Writes data/audio.json in the format the engine reads:
  beats, downbeats, bpm, sections, 100 fps envelopes (rms/low/mid/high/vocal/drums/bass/other)
  and onset lists (kick/snare/hat/vocal) with strengths.
Also writes analysis/cache.npz (features for the alignment step) and diagnostic PNGs.

Techniques
- STFT (2048 / hop 441 = 100 fps) of mid (L+R) and side (L-R).
- Vocal estimate = centre-panned harmonic energy: |mid| - |side| (vocals sit in the centre, most
  pads/reverbs are wide), then harmonic/percussive median filtering, 250-4000 Hz.
- Onset strength = log-mel spectral flux; tempo = autocorrelation with a 120 BPM prior;
  beats = dynamic programming (Ellis 2007), then refined to a constant-tempo grid.
- Downbeat phase = the beat phase where chords change (chroma flux) and kicks are strongest.
- Sections = checkerboard novelty on a beat-synchronous self-similarity matrix.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import ndimage, signal

ROOT = Path(__file__).resolve().parents[1]
import os
SONG = os.environ.get('SONG', 'edit')   # audio/<SONG>/song_stereo.wav (edit = the updated mix)
SRC = ROOT / 'audio' / SONG / 'song_stereo.wav'
SR = 44100
HOP = 441
NFFT = 2048
FPS = SR / HOP  # 100

sr, x = wavfile.read(SRC)
assert sr == SR, sr
x = x.astype(np.float32) / 32768.0
L, R = x[:, 0], x[:, 1]
mid, side = (L + R) * 0.5, (L - R) * 0.5
N = len(mid)
dur = N / SR
print(f'duration {dur:.2f}s')

def stft_mag(y):
    win = np.hanning(NFFT).astype(np.float32)
    pad = np.concatenate([np.zeros(NFFT // 2, np.float32), y, np.zeros(NFFT, np.float32)])
    nfr = 1 + (len(y)) // HOP
    out = np.empty((nfr, NFFT // 2 + 1), np.float32)
    B = 2000
    for s in range(0, nfr, B):
        e = min(nfr, s + B)
        idx = np.arange(s, e)[:, None] * HOP + np.arange(NFFT)[None, :]
        out[s:e] = np.abs(np.fft.rfft(pad[idx] * win, axis=1))
    return out

M = stft_mag(mid)
S = stft_mag(side)
T = M.shape[0]
freqs = np.fft.rfftfreq(NFFT, 1 / SR)
times = np.arange(T) / FPS
print('stft', M.shape)

# ---------------------------------------------------------------- mel filterbank
def mel(f): return 2595 * np.log10(1 + f / 700)
def imel(m): return 700 * (10 ** (m / 2595) - 1)
def melbank(n=80, fmin=30, fmax=16000):
    pts = imel(np.linspace(mel(fmin), mel(fmax), n + 2))
    fb = np.zeros((n, len(freqs)), np.float32)
    for i in range(n):
        a, b, c = pts[i], pts[i + 1], pts[i + 2]
        fb[i] = np.clip(np.minimum((freqs - a) / (b - a), (c - freqs) / (c - b)), 0, None)
    return fb, pts[1:-1]
FB, melc = melbank()
LM = np.log1p(100 * (M @ FB.T))            # log-mel of the full mix (mid)

# ---------------------------------------------------------------- HPSS on mid, and centre extraction
Mc = np.maximum(M - 1.0 * S, 0)             # centre-panned magnitude
def hpss(X, kt=31, kf=31):
    H = ndimage.median_filter(X, size=(kt, 1))
    P = ndimage.median_filter(X, size=(1, kf))
    mh = H ** 2 / (H ** 2 + P ** 2 + 1e-9)
    return X * mh, X * (1 - mh)
# downsample frequency for speed in HPSS (keep up to 8 kHz at full res)
Hm, Pm = hpss(M)
Hc, _ = hpss(Mc)
print('hpss done')

def band(X, lo, hi):
    m = (freqs >= lo) & (freqs < hi)
    return np.sqrt((X[:, m] ** 2).sum(1))

def norm01(v, pct=99.5):
    v = v - np.percentile(v, 1)
    v = v / (np.percentile(v, pct) + 1e-9)
    return np.clip(v, 0, 1)

def smooth(v, w=5):
    k = np.hanning(w * 2 + 1); k /= k.sum()
    return np.convolve(v, k, mode='same')

env = {
    'rms': norm01(smooth(np.sqrt((M ** 2).mean(1)), 3)),
    'low': norm01(smooth(band(M, 20, 150), 3)),
    'mid': norm01(smooth(band(M, 150, 2000), 3)),
    'high': norm01(smooth(band(M, 2000, 16000), 3)),
    'vocal': norm01(smooth(band(Hc, 250, 4000), 4)),
    'drums': norm01(smooth(band(Pm, 30, 16000), 2)),
    'bass': norm01(smooth(band(Hm, 30, 200), 4)),
    'other': norm01(smooth(band(np.maximum(Hm - Hc, 0), 200, 8000), 4)),
}

# ---------------------------------------------------------------- onset strength, tempo, beats
flux = np.maximum(np.diff(LM, axis=0, prepend=LM[:1]), 0).sum(1)
flux = flux - ndimage.uniform_filter1d(flux, 31)
oenv = np.maximum(flux, 0)
oenv /= oenv.std() + 1e-9

def tempo_est(o, lo=70, hi=190):
    ac = np.correlate(o - o.mean(), o - o.mean(), mode='full')[len(o) - 1:]
    lags = np.arange(len(ac))
    bpm = 60 * FPS / np.maximum(lags, 1)
    prior = np.exp(-0.5 * (np.log2(bpm / 120) / 0.9) ** 2)
    sc = ac * prior
    sc[(bpm < lo) | (bpm > hi)] = 0
    lag = int(np.argmax(sc))
    # parabolic refinement
    if 1 <= lag < len(sc) - 1:
        a, b, c = sc[lag - 1], sc[lag], sc[lag + 1]
        lag = lag + 0.5 * (a - c) / (a - 2 * b + c + 1e-9)
    return 60 * FPS / lag

bpm0 = tempo_est(oenv)
print(f'tempo estimate {bpm0:.2f} BPM')

def beat_dp(o, bpm, tight=100):
    period = 60 * FPS / bpm
    score = o.copy()
    back = -np.ones(len(o), int)
    lo, hi = int(round(period / 2)), int(round(period * 2))
    for i in range(len(o)):
        if i < lo: continue
        prev = np.arange(max(0, i - hi), i - lo + 1)
        if len(prev) == 0: continue
        pen = -tight * (np.log((i - prev) / period)) ** 2
        cand = score[prev] + pen
        j = int(np.argmax(cand))
        score[i] = o[i] + cand[j]
        back[i] = prev[j]
    # backtrack from best in last period
    i = int(np.argmax(score[-int(period):])) + len(o) - int(period)
    beats = []
    while i >= 0:
        beats.append(i)
        i = back[i]
    return np.array(beats[::-1])

bdp = beat_dp(oenv, bpm0)
# constant-tempo grid fit (most AI-generated / DAW songs have a fixed tempo)
k = np.arange(len(bdp))
A = np.vstack([k, np.ones_like(k)]).T
per, off = np.linalg.lstsq(A, bdp.astype(float), rcond=None)[0]
res = bdp - (k * per + off)
print(f'DP beats {len(bdp)}; grid period {per:.3f} frames = {60 * FPS / per:.3f} BPM; residual std {res.std():.2f} frames, max {np.abs(res).max():.1f}')

# refine grid by maximizing onset energy at the grid (fine search of period and offset)
def grid_score(per, off):
    ts = off + per * np.arange(int((T - off) / per))
    ts = ts[(ts >= 0) & (ts < T - 1)]
    i0 = np.floor(ts).astype(int); f = ts - i0
    return (oenv[i0] * (1 - f) + oenv[i0 + 1] * f).mean()
best = (grid_score(per, off % per), per, off % per)
for p in np.linspace(per * 0.997, per * 1.003, 61):
    for o in np.linspace(0, p, 200, endpoint=False):
        s = grid_score(p, o)
        if s > best[0]: best = (s, p, o)
_, per, off = best
bpm = 60 * FPS / per
print(f'refined grid: {bpm:.3f} BPM, first beat at {off / FPS:.3f}s')
beats_t = (off + per * np.arange(int((T - off) / per))) / FPS
# extend backwards to t >= 0
while beats_t[0] - per / FPS >= 0: beats_t = np.insert(beats_t, 0, beats_t[0] - per / FPS)

# ---------------------------------------------------------------- chroma, downbeats
pc = np.full(len(freqs), -1)
valid = (freqs > 60) & (freqs < 5000)
pc[valid] = (np.round(12 * np.log2(freqs[valid] / 440.0)) % 12).astype(int)
C = np.zeros((T, 12), np.float32)
for p in range(12): C[:, p] = Hm[:, pc == p].sum(1)
C = C / (C.sum(1, keepdims=True) + 1e-9)
bi = np.clip(np.round(beats_t * FPS).astype(int), 0, T - 1)
# beat-synchronous chroma (mean over each beat)
Cb = np.array([C[bi[i]:bi[i + 1]].mean(0) if i + 1 < len(bi) else C[bi[i]:].mean(0) for i in range(len(bi))])
cflux = np.r_[0, np.abs(np.diff(Cb, axis=0)).sum(1)]
kick_env = norm01(band(Pm, 30, 120))
kb = np.array([kick_env[max(0, b - 3):b + 4].max() for b in bi])
ph_score = [cflux[p::4].mean() * 2 + kb[p::4].mean() for p in range(4)]
ph = int(np.argmax(ph_score))
print('downbeat phase scores', np.round(ph_score, 3), '-> phase', ph)
downbeats_t = beats_t[ph::4]

# ---------------------------------------------------------------- onsets per drum / vocal
def peaks(v, thr, dist_s=0.08):
    v = norm01(v)
    p, pr = signal.find_peaks(v, height=thr, distance=int(dist_s * FPS), prominence=thr * 0.6)
    return [[round(float(i / FPS), 3), round(float(pr['peak_heights'][j]), 3)] for j, i in enumerate(p)]
def pflux(X, lo, hi):
    b = band(X, lo, hi)
    d = np.maximum(np.diff(np.log1p(50 * b), prepend=0), 0)
    return d
onsets = {
    'kick': peaks(pflux(Pm, 30, 120), 0.25, 0.18),
    'snare': peaks(pflux(Pm, 180, 4000) * (band(Pm, 1000, 8000) / (band(Pm, 30, 150) + 1e-3)) ** 0.3, 0.3, 0.18),
    'hat': peaks(pflux(Pm, 7000, 16000), 0.3, 0.08),
    'vocal': peaks(pflux(Hc, 250, 4000), 0.2, 0.1),
}
print({k: len(v) for k, v in onsets.items()})

# ---------------------------------------------------------------- sections (novelty on beat-sync features)
LMb = np.array([LM[bi[i]:bi[i + 1]].mean(0) if i + 1 < len(bi) else LM[bi[i]:].mean(0) for i in range(len(bi))])
Fz = np.hstack([(LMb - LMb.mean(0)) / (LMb.std(0) + 1e-6), 3 * (Cb - Cb.mean(0)) / (Cb.std(0) + 1e-6)])
Fz /= np.linalg.norm(Fz, axis=1, keepdims=True) + 1e-9
SSM = Fz @ Fz.T
K = 16
g = np.exp(-0.5 * (np.linspace(-2, 2, 2 * K) ** 2))
ck = np.outer(g, g) * np.sign(np.outer(np.r_[-np.ones(K), np.ones(K)], np.r_[-np.ones(K), np.ones(K)]))
nov = np.zeros(len(bi))
for i in range(K, len(bi) - K):
    nov[i] = (SSM[i - K:i + K, i - K:i + K] * ck).sum()
nov = np.maximum(nov, 0); nov /= nov.max() + 1e-9
bpk, _ = signal.find_peaks(nov, height=0.15, distance=8)
bounds = sorted(set([0] + [int(b) for b in bpk]))
print('section boundaries (beat idx, s):', [(b, round(float(beats_t[b]), 2)) for b in bounds])

np.savez_compressed(ROOT / 'analysis' / f'cache.{SONG}.npz', LM=LM.astype(np.float16), Hc_band=band(Hc, 250, 4000).astype(np.float32),
                    vflux=pflux(Hc, 250, 4000).astype(np.float32), beats=beats_t, downbeats=downbeats_t, nov=nov, oenv=oenv.astype(np.float32),
                    vocal=env['vocal'], melc=melc, HcLM=np.log1p(100 * (Hc @ FB.T)).astype(np.float16))

audio = {
    'duration': round(dur, 3), 'bpm': round(bpm, 3), 'beat_period': round(60 / bpm, 5), 'time_signature': 4, 'fps': 100,
    'beats': [round(float(b), 4) for b in beats_t], 'downbeats': [round(float(b), 4) for b in downbeats_t],
    'sections': [],  # labelled in align step
    **{k: [round(float(v), 3) for v in a] for k, a in env.items()},
    'onsets': onsets,
    'notes': 'numpy/scipy analysis: centre-channel harmonic vocal estimate, DP beats on a constant grid',
}
json.dump(audio, open(ROOT / 'data' / f'audio.{SONG}.json', 'w'))
print(f'wrote data/audio.{SONG}.json')
