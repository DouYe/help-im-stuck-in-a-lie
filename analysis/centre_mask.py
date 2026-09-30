"""Azimuth (panning) mask: keep time-frequency bins where L and R are nearly identical (dead centre,
where lead vocals sit), then remove drums with a harmonic/percussive split. Saves analysis/centre.npz."""
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import ndimage
ROOT = Path(__file__).resolve().parents[1]
SR, HOP, NFFT = 44100, 441, 2048
sr, x = wavfile.read(ROOT/'audio/real/song_stereo.wav'); x = x.astype(np.float32)/32768
win = np.hanning(NFFT).astype(np.float32)
def stft(y):
    pad = np.concatenate([np.zeros(NFFT//2, np.float32), y, np.zeros(NFFT, np.float32)])
    nfr = 1 + len(y)//HOP; out = np.empty((nfr, NFFT//2+1), np.complex64)
    for s in range(0, nfr, 2000):
        e = min(nfr, s+2000); idx = np.arange(s, e)[:, None]*HOP + np.arange(NFFT)[None, :]
        out[s:e] = np.fft.rfft(pad[idx]*win, axis=1)
    return out
XL, XR = stft(x[:, 0]), stft(x[:, 1])
KB = 372
M = (XL[:, :KB] + XR[:, :KB]) * 0.5; S = (XL[:, :KB] - XR[:, :KB]) * 0.5
r = np.abs(S) / (np.abs(M) + 1e-9)
cm = np.exp(-0.5 * (r / 0.12) ** 2)           # 1 at dead centre, ~0 when |side| > 0.3 |mid|
C = np.abs(M) * cm
H = ndimage.median_filter(C, size=(17, 1)); P = ndimage.median_filter(C, size=(1, 17))
hm = H**2 / (H**2 + P**2 + 1e-12)
V = C * hm
np.savez_compressed(ROOT/'analysis/centre.npz', V=V.astype(np.float16))
print('ok', V.shape)
