"""Map the updated song (audio/edit) onto the analysed original (audio/real): for every 2 s window of the
new file, find the best-matching position in the old file (normalised cross-correlation of log-mel
frames). Prints the offset map so beat/lyric data can be carried over where the audio is the same."""
import numpy as np
from scipy.io import wavfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SR, HOP, NFFT = 44100, 441, 2048
def logmel(path):
    sr, x = wavfile.read(path); x = x.astype(np.float32).mean(1) / 32768
    win = np.hanning(NFFT).astype(np.float32)
    pad = np.concatenate([np.zeros(NFFT // 2, np.float32), x, np.zeros(NFFT, np.float32)])
    T = 1 + len(x) // HOP
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    mel = lambda f: 2595 * np.log10(1 + f / 700); imel = lambda m: 700 * (10 ** (m / 2595) - 1)
    pts = imel(np.linspace(mel(40), mel(12000), 42))
    fb = np.array([np.clip(np.minimum((freqs - pts[i]) / (pts[i + 1] - pts[i]), (pts[i + 2] - freqs) / (pts[i + 2] - pts[i + 1])), 0, None) for i in range(40)], np.float32)
    out = np.empty((T, 40), np.float32)
    for s in range(0, T, 2000):
        e = min(T, s + 2000); idx = np.arange(s, e)[:, None] * HOP + np.arange(NFFT)[None, :]
        out[s:e] = np.log1p(100 * (np.abs(np.fft.rfft(pad[idx] * win, axis=1)) @ fb.T))
    return out
A = logmel(ROOT / 'audio/real/song_stereo.wav'); B = logmel(ROOT / 'audio/edit/song_stereo.wav')
print('old', len(A) / 100, 's  new', len(B) / 100, 's')
def z(X): X = X - X.mean(0); return X / (np.linalg.norm(X) + 1e-9)
L = 200  # 2 s windows
res = []
for s in range(0, len(B) - L, 100):
    w = z(B[s:s + L])
    best = (-1, 0)
    # coarse search every 5 frames, then refine
    for o in range(0, len(A) - L, 5):
        c = float((w * z(A[o:o + L])).sum())
        if c > best[0]: best = (c, o)
    c0, o0 = best
    for o in range(max(0, o0 - 6), min(len(A) - L, o0 + 7)):
        c = float((w * z(A[o:o + L])).sum())
        if c > best[0]: best = (c, o)
    res.append((s / 100, best[1] / 100, best[0]))
prev = None
for tn, to, c in res:
    off = to - tn
    mark = '' if prev is None or abs(off - prev) < 0.03 else '   <-- jump'
    print(f'new {tn:6.1f}s -> old {to:7.2f}s  offset {off:+7.2f}  corr {c:.3f}{mark}')
    prev = off
