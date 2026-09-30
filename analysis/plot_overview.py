"""Diagnostic overview: centre-harmonic (vocal-ish) spectrogram with beat grid, vocal envelope and
section novelty, in rows. Usage: python3 plot_overview.py [t0 t1 rowlen out.png]"""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
c = np.load(ROOT / 'analysis' / 'cache.npz')
a = json.load(open(ROOT / 'data' / 'audio.real.json'))
HcLM = c['HcLM'].astype(np.float32)
vocal = c['vocal']; oenv = c['oenv']; vflux = c['vflux']
beats = np.array(a['beats']); down = np.array(a['downbeats'])
t0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0
t1 = float(sys.argv[2]) if len(sys.argv) > 2 else a['duration']
row = float(sys.argv[3]) if len(sys.argv) > 3 else 20
out = sys.argv[4] if len(sys.argv) > 4 else str(ROOT / 'out' / 'wip' / 'overview.png')
marks = json.loads(sys.argv[5]) if len(sys.argv) > 5 else []   # [[t, label], ...]
nrow = int(np.ceil((t1 - t0) / row))
fig, axes = plt.subplots(nrow, 1, figsize=(22, 3.1 * nrow), squeeze=False)
for r in range(nrow):
    ax = axes[r, 0]
    a0, a1 = t0 + r * row, min(t1, t0 + (r + 1) * row)
    i0, i1 = int(a0 * 100), int(a1 * 100)
    img = HcLM[i0:i1, 4:64].T
    ax.imshow(img, aspect='auto', origin='lower', extent=[a0, a1, 0, 1], cmap='magma', vmin=np.percentile(HcLM, 30), vmax=np.percentile(HcLM, 99.7))
    tt = np.arange(i0, i1) / 100
    ax.plot(tt, 0.02 + 0.3 * vocal[i0:i1], color='cyan', lw=1)
    vf = vflux[i0:i1] / (np.percentile(vflux, 99.5) + 1e-9)
    ax.plot(tt, 0.02 + 0.2 * np.clip(vf, 0, 1.5), color='lime', lw=0.6)
    for b in beats[(beats >= a0) & (beats < a1)]:
        ax.axvline(b, color='white', lw=0.5, alpha=0.35)
    for b in down[(down >= a0) & (down < a1)]:
        ax.axvline(b, color='white', lw=1.4, alpha=0.8)
    for t, lab in marks:
        if a0 <= t < a1:
            ax.axvline(t, color='orange', lw=1.2)
            ax.text(t, 0.93, lab, color='orange', fontsize=9, rotation=0, va='top')
    ax.set_xlim(a0, a0 + row)
    ax.set_xticks(np.arange(np.ceil(a0), a1 + 0.01, 1.0))
    ax.tick_params(labelsize=7)
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(out, dpi=60)
print(out)
