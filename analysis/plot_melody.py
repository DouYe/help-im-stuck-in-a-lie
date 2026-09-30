"""Plot the extracted sung melody (pitch contour) with the beat grid, for lyric alignment.
Usage: python3 plot_melody.py t0 t1 rowlen out.png [marks-json]"""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
m = np.load(ROOT / 'analysis' / 'melody.npz')
a = json.load(open(ROOT / 'data' / 'audio.real.json'))
f0, conf, energy, SALS, cents = m['f0'], m['conf'], m['energy'], m['SALS'].astype(np.float32), m['cents']
beats = np.array(a['beats']); down = np.array(a['downbeats'])
t0, t1, row = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
out = sys.argv[4]
marks = json.loads(sys.argv[5]) if len(sys.argv) > 5 else []
en = np.log1p(energy / np.percentile(energy, 50))
en = en / np.percentile(en, 99.5)
nrow = int(np.ceil((t1 - t0) / row))
fig, axes = plt.subplots(nrow, 1, figsize=(24, 3.6 * nrow), squeeze=False)
S = SALS / (np.percentile(SALS, 99, axis=1, keepdims=True) + 1e-6)
for r in range(nrow):
    ax = axes[r, 0]
    a0, a1 = t0 + r * row, min(t1, t0 + (r + 1) * row)
    i0, i1 = int(a0 * 100), int(a1 * 100)
    ax.imshow(S[i0:i1].T, aspect='auto', origin='lower', extent=[a0, a1, cents[0], cents[-1]], cmap='gray_r', vmin=0.3, vmax=1.2, alpha=0.8)
    tt = np.arange(i0, i1) / 100
    c = np.clip((conf[i0:i1] - 1.5) / 2.5, 0, 1) * np.clip(en[i0:i1] * 1.5, 0, 1)
    cc = 1200 * np.log2(f0[i0:i1] / 100)
    ax.scatter(tt, cc, s=5, c=c, cmap='plasma', vmin=0, vmax=1)
    ax.plot(tt, cents[0] + en[i0:i1] * 900, color='teal', lw=1)
    for b in beats[(beats >= a0) & (beats < a1)]:
        bi = int(np.argmin(np.abs(beats - b)))
        ax.axvline(b, color='k', lw=0.4, alpha=0.4)
        for q in (0.25, 0.5, 0.75):
            ax.axvline(b + q * (beats[1] - beats[0]), color='k', lw=0.2, alpha=0.15)
    for b in down[(down >= a0) & (down < a1)]:
        bar = int(np.argmin(np.abs(down - b)))
        ax.axvline(b, color='k', lw=1.3, alpha=0.8)
        ax.text(b + 0.02, cents[-1] - 120, f'bar {bar}', fontsize=9)
    for t, lab in marks:
        if a0 <= t < a1:
            ax.axvline(t, color='red', lw=1)
            ax.text(t + 0.01, cents[-1] - 400, lab, color='red', fontsize=10)
    ax.set_xlim(a0, a0 + row)
    ax.set_xticks(np.arange(np.ceil(a0 * 4) / 4, a1 + 0.01, 0.25), minor=True)
    ax.set_xticks(np.arange(np.ceil(a0), a1 + 0.01, 1.0))
    ax.tick_params(labelsize=8)
    ax.set_ylim(cents[0], cents[-1])
plt.tight_layout()
plt.savefig(out, dpi=55)
print(out)
