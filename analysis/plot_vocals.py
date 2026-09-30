"""Plot the REPET vocal estimate (log spectrogram <= 4 kHz) with the beat grid and marks.
Usage: plot_vocals.py t0 t1 rowlen out.png [marks-json]"""
import sys, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
v = np.load(ROOT/'analysis/vocals.npz'); a = json.load(open(ROOT/'data/audio.real.json'))
voc = v['voc'].astype(np.float32)[:, :186]   # <= 4 kHz
venv = v['venv']
L = np.log1p(200 * voc / np.percentile(voc, 99.9))
beats = np.array(a['beats']); down = np.array(a['downbeats']); bp = beats[1]-beats[0]
t0, t1, row, out = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
marks = json.loads(sys.argv[5]) if len(sys.argv) > 5 else []
nrow = int(np.ceil((t1-t0)/row))
fig, axes = plt.subplots(nrow, 1, figsize=(24, 3.4*nrow), squeeze=False)
en = venv / np.percentile(venv, 99.5)
for r in range(nrow):
    ax = axes[r, 0]; a0 = t0 + r*row; a1 = min(t1, a0+row)
    i0, i1 = int(a0*100), int(a1*100)
    ax.imshow(L[i0:i1].T, aspect='auto', origin='lower', extent=[a0, a1, 0, 4000], cmap='magma', vmin=0.2, vmax=np.percentile(L, 99.8))
    tt = np.arange(i0, i1)/100
    ax.plot(tt, 50 + 1200*np.clip(en[i0:i1], 0, 1.3), color='cyan', lw=1.2)
    for b in beats[(beats >= a0) & (beats < a1)]:
        ax.axvline(b, color='w', lw=0.5, alpha=0.5)
        for q in (0.25, 0.5, 0.75): ax.axvline(b+q*bp, color='w', lw=0.3, alpha=0.18)
    for b in down[(down >= a0) & (down < a1)]:
        bar = int(np.argmin(np.abs(down-b)))
        ax.axvline(b, color='w', lw=1.6, alpha=0.9); ax.text(b+0.02, 3700, f'bar {bar}', color='w', fontsize=10)
    for t, lab in marks:
        if a0 <= t < a1:
            ax.axvline(t, color='lime', lw=1.2); ax.text(t+0.01, 3300, lab, color='lime', fontsize=11)
    ax.set_xlim(a0, a0+row); ax.set_xticks(np.arange(np.ceil(a0), a1+0.01, 1.0)); ax.tick_params(labelsize=8)
plt.tight_layout(); plt.savefig(out, dpi=55); print(out)
