"""Per-bar centre-vocal spectrogram with syllable-onset candidates and optional word marks.
Usage: plot_centre.py firstbar nbars out.png [words-json [[t, 'word'], ...]]"""
import sys, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import signal
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
V = np.load(ROOT/'analysis/centre.npz')['V'].astype(np.float32)
a = json.load(open(ROOT/'data/audio.json'))
beats = np.array(a['beats']); down = np.array(a['downbeats']); bp = beats[1]-beats[0]
freqs = np.fft.rfftfreq(2048, 1/44100)[:V.shape[1]]
L = np.log1p(300*V/np.percentile(V, 99.9))
sel = (freqs > 250) & (freqs < 4000)
Lb = np.log1p(300*V[:, sel]/np.percentile(V, 99.9))
fl = np.maximum(np.diff(Lb, axis=0, prepend=Lb[:1]), 0).sum(1)
fl = np.convolve(fl, np.hanning(7)/np.hanning(7).sum(), mode='same')
fl /= np.percentile(fl, 99.5)
en = np.sqrt((V[:, sel]**2).sum(1)); en /= np.percentile(en, 99.5)
pk, pr = signal.find_peaks(fl, height=0.25, distance=8, prominence=0.15)
b0, nb, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
words = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
fig, axes = plt.subplots(nb, 1, figsize=(24, 3.3*nb), squeeze=False)
for r in range(nb):
    bi = b0 + r
    a0 = down[bi] if bi < len(down) else down[-1] + (bi-len(down)+1)*4*bp
    a1 = a0 + 4*bp; i0, i1 = int(a0*100), int(a1*100)
    ax = axes[r, 0]
    ax.imshow(L[i0:i1, :186].T, aspect='auto', origin='lower', extent=[a0, a1, 0, 4000], cmap='magma', vmin=0.15, vmax=np.percentile(L, 99.8))
    tt = np.arange(i0, i1)/100
    ax.plot(tt, 60 + 1300*np.clip(en[i0:i1], 0, 1.4), color='cyan', lw=1.3)
    ax.plot(tt, 60 + 900*np.clip(fl[i0:i1], 0, 1.5), color='lime', lw=0.8)
    for p in pk[(pk >= i0) & (pk < i1)]:
        ax.plot([p/100], [3850], 'v', color='lime', ms=7)
    for k in range(17):
        x = a0 + k*bp/4
        ax.axvline(x, color='w', lw=1.2 if k % 4 == 0 else 0.35, alpha=0.8 if k % 4 == 0 else 0.3)
        if k < 16: ax.text(x+0.005, 150, f'{k//4+1}.{k%4+1}', color='w', fontsize=7, alpha=0.7)
    for t, w in words:
        if a0 <= t < a1:
            ax.axvline(t, color='deepskyblue', lw=1.6)
            ax.text(t+0.01, 3350, w, color='deepskyblue', fontsize=14, weight='bold')
    ax.text(a0+0.01, 3650, f'bar {bi} @ {a0:.2f}s', color='w', fontsize=11)
    ax.set_xlim(a0, a1); ax.set_yticks([])
plt.tight_layout(); plt.savefig(out, dpi=52); print(out)
np.save(ROOT/'analysis/syl_onsets.npy', pk/100)
