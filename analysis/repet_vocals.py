"""Non-ML vocal isolation: REPET-SIM on the centre channel.

The accompaniment repeats (every bar / every chorus), the lead vocal mostly does not. For every frame we
find the k most similar frames elsewhere in the song (cosine similarity of the log spectrum, at least
1 s away), take their per-bin median as the "repeating background", and keep what exceeds it as vocal.
Combined with centre extraction (|mid| - |side|), this gives a usable vocal spectrogram for alignment.
Saves analysis/vocals.npz (vocal magnitude up to 8 kHz at 100 fps, and a vocal energy envelope) and
writes audio/real/vocals_est.wav (resynthesised with the mixture phase) to sanity-check.
"""
from pathlib import Path
import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
SR, HOP, NFFT = 44100, 441, 2048
sr, x = wavfile.read(ROOT / 'audio' / 'real' / 'song_stereo.wav')
x = x.astype(np.float32) / 32768.0
mid, side = (x[:, 0] + x[:, 1]) * 0.5, (x[:, 0] - x[:, 1]) * 0.5
win = np.hanning(NFFT).astype(np.float32)
def stft(y):
    pad = np.concatenate([np.zeros(NFFT // 2, np.float32), y, np.zeros(NFFT, np.float32)])
    nfr = 1 + len(y) // HOP
    out = np.empty((nfr, NFFT // 2 + 1), np.complex64)
    for s in range(0, nfr, 2000):
        e = min(nfr, s + 2000)
        idx = np.arange(s, e)[:, None] * HOP + np.arange(NFFT)[None, :]
        out[s:e] = np.fft.rfft(pad[idx] * win, axis=1)
    return out
Xm = stft(mid); Xs = stft(side)
T = Xm.shape[0]
KB = 372  # bins up to ~8 kHz
Vm = np.abs(Xm[:, :KB]); Vs = np.abs(Xs[:, :KB])
V = np.maximum(Vm - Vs, 0)            # centre-panned magnitude
F = np.log1p(50 * V)
F = F - F.mean(1, keepdims=True)
F /= np.linalg.norm(F, axis=1, keepdims=True) + 1e-9
K, MIN_D = 24, 100                    # 24 neighbours, >= 1 s apart
W = np.empty_like(V)
for s in range(0, T, 400):
    e = min(T, s + 400)
    sim = F[s:e] @ F.T                 # (chunk, T)
    for i in range(s, e):              # forbid near-diagonal
        sim[i - s, max(0, i - MIN_D):min(T, i + MIN_D)] = -9
    idx = np.argpartition(-sim, K, axis=1)[:, :K]
    W[s:e] = np.minimum(np.median(V[idx], axis=1), V[s:e])
    print(f'\r{e}/{T}', end='')
print()
mask = np.clip((V - W) / (V + 1e-9), 0, 1) ** 1.5
voc = Vm * mask                        # vocal magnitude estimate (applied to the mid spectrum)
freqs = np.fft.rfftfreq(NFFT, 1 / SR)[:KB]
band = (freqs > 200) & (freqs < 5000)
venv = np.sqrt((voc[:, band] ** 2).sum(1))
np.savez_compressed(ROOT / 'analysis' / 'vocals.npz', voc=voc.astype(np.float16), venv=venv.astype(np.float32))
# resynthesis for a listen (ISTFT with mid phase)
full = np.zeros_like(Xm)
full[:, :KB] = Xm[:, :KB] * mask
y = np.zeros(T * HOP + NFFT, np.float32); wsum = np.zeros_like(y)
fr = np.fft.irfft(full, n=NFFT, axis=1).astype(np.float32) * win
for i in range(T):
    y[i * HOP:i * HOP + NFFT] += fr[i]; wsum[i * HOP:i * HOP + NFFT] += win ** 2
y = y[NFFT // 2:NFFT // 2 + len(mid)] / np.maximum(wsum[NFFT // 2:NFFT // 2 + len(mid)], 1e-3)
y = y / (np.abs(y).max() + 1e-9) * 0.9
wavfile.write(ROOT / 'audio' / 'real' / 'vocals_est.wav', SR, (y * 32767).astype(np.int16))
print('saved vocals.npz and vocals_est.wav')
