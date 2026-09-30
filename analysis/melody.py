"""Predominant-melody (sung line) extraction without ML: harmonic-sum salience on the centre channel.

For every 10 ms frame: hi-res STFT (8192) of mid and side, centre = max(|mid| - |side|, 0), then for
f0 candidates 100-1000 Hz (10-cent steps) salience = sum_h 0.8^(h-1) * |centre|(h*f0)^0.5.
Keeps the best candidate, its salience, and a confidence (peak / median over candidates) with a
light continuity bonus (Viterbi over candidates). Saves analysis/melody.npz.
"""
from pathlib import Path
import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
SR, HOP, NFFT = 44100, 441, 8192
sr, x = wavfile.read(ROOT / 'audio' / 'real' / 'song_stereo.wav')
x = x.astype(np.float32) / 32768.0
mid, side = (x[:, 0] + x[:, 1]) * 0.5, (x[:, 0] - x[:, 1]) * 0.5
T = 1 + len(mid) // HOP
win = np.hanning(NFFT).astype(np.float32)
pad = lambda y: np.concatenate([np.zeros(NFFT // 2, np.float32), y, np.zeros(NFFT, np.float32)])
pm, ps = pad(mid), pad(side)
freqs = np.fft.rfftfreq(NFFT, 1 / SR)
cents = np.arange(0, 3300, 10)                      # 100 Hz .. ~670 Hz * 1.5
f0s = 100 * 2 ** (cents / 1200)
H = 8
hw = 0.8 ** np.arange(H)
binpos = (f0s[:, None] * np.arange(1, H + 1)[None, :]) / (SR / NFFT)   # fractional bin index
b0 = np.floor(binpos).astype(int); bf = (binpos - b0).astype(np.float32)
valid = (b0 + 1) < len(freqs)
b0 = np.where(valid, b0, 0); bf = np.where(valid, bf, 0)
f0_best = np.zeros(T, np.float32); sal_best = np.zeros(T, np.float32); conf = np.zeros(T, np.float32)
energy = np.zeros(T, np.float32)
SALS = np.zeros((T, len(f0s)), np.float16)
B = 400
for s in range(0, T, B):
    e = min(T, s + B)
    idx = np.arange(s, e)[:, None] * HOP + np.arange(NFFT)[None, :]
    Mx = np.abs(np.fft.rfft(pm[idx] * win, axis=1))
    Sx = np.abs(np.fft.rfft(ps[idx] * win, axis=1))
    C = np.maximum(Mx - Sx, 0) ** 0.5
    # band energy 150-4000 Hz of the centre
    energy[s:e] = (C[:, (freqs > 150) & (freqs < 4000)] ** 2).sum(1)
    v = C[:, b0] * (1 - bf) + C[:, b0 + 1] * bf        # (frames, f0, H)
    v = v * valid
    sal = (v * hw).sum(2)
    SALS[s:e] = sal.astype(np.float16)
    print(f'\r{e}/{T}', end='')
print()
# Viterbi with continuity: transition cost grows with pitch jump (in 10-cent steps)
S = SALS.astype(np.float32)
S = S / (np.percentile(S, 99, axis=1, keepdims=True) + 1e-6)
nC = S.shape[1]
jump = np.abs(np.arange(nC)[:, None] - np.arange(nC)[None, :])
# only allow jumps up to 1.5 octaves; cost per 100 cents
trans = -0.02 * (jump / 10.0)
trans[jump > 180] = -1e9
score = S[0].copy(); back = np.zeros((T, nC), np.int16)
for t in range(1, T):
    cand = score[None, :] + trans            # (to, from)
    j = np.argmax(cand, axis=1)
    back[t] = j
    score = cand[np.arange(nC), j] + S[t]
    if t % 2000 == 0: print(f'\rviterbi {t}/{T}', end='')
print()
path = np.zeros(T, int); path[-1] = int(np.argmax(score))
for t in range(T - 1, 0, -1): path[t - 1] = back[t, path[t]]
f0_best = f0s[path]
sal_best = S[np.arange(T), path]
conf = sal_best / (np.median(S, axis=1) + 1e-6)
np.savez_compressed(ROOT / 'analysis' / 'melody.npz', f0=f0_best.astype(np.float32), sal=sal_best.astype(np.float32),
                    conf=conf.astype(np.float32), energy=energy, cents=cents, SALS=SALS)
print('saved melody.npz')
