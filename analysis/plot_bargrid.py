"""Bar-grid view: one row per bar, x = position in the bar (16ths), brightness = vocal energy.
Repeated lyric lines show up as repeated rhythm/melody patterns."""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path('/home/claude/lie-video')
v = np.load(ROOT/'analysis/vocals.npz'); a = json.load(open(ROOT/'data/audio.real.json'))
voc = v['voc'].astype(np.float32)
down = np.array(a['downbeats']); bar = np.diff(down).mean()
freqs = np.fft.rfftfreq(2048, 1/44100)[:voc.shape[1]]
# pitch-ish image: vocal spectrum 150-1200 Hz (fundamentals + 2nd harmonics) per bar
sel = (freqs > 150) & (freqs < 1200)
Lg = np.log1p(100*voc[:, sel]/np.percentile(voc[:, sel], 99.5))
en = np.sqrt((voc[:, (freqs>200)&(freqs<4000)]**2).sum(1)); en = en/np.percentile(en, 99)
starts = np.r_[down[0]-bar*np.arange(1, int(down[0]/bar)+1)[::-1], down]
starts = starts[starts > -bar]
nb = len(starts); cols = 256
img = np.zeros((nb, cols)); spec = np.zeros((nb, cols, sel.sum()))
for i, s in enumerate(starts):
    ts = s + np.arange(cols)/cols*bar
    idx = np.clip((ts*100).astype(int), 0, len(en)-1)
    img[i] = en[idx] * (ts >= 0)
    spec[i] = Lg[idx]
fig, ax = plt.subplots(1, 2, figsize=(26, 0.34*nb+1), gridspec_kw={'width_ratios':[1, 1.6]})
ax[0].imshow(np.clip(img, 0, 1.2), aspect='auto', cmap='magma', extent=[0, 16, nb-0.5, -0.5])
for x in range(17): ax[0].axvline(x, color='w', lw=0.3 if x%4 else 1.0, alpha=0.4)
ax[0].set_yticks(range(nb)); ax[0].set_yticklabels([f'{i-(len(starts)-len(down))} @{s:6.2f}s' for i, s in enumerate(starts)], fontsize=8)
ax[0].set_xticks(range(0, 17, 4))
# spectral view: per bar, the 16ths x frequency (concat bins vertically compressed): show max-freq trace
S = spec.max(axis=2)
pk = spec.argmax(axis=2)
ax[1].imshow(np.where(np.clip(img,0,1)>0.25, pk, np.nan), aspect='auto', cmap='viridis', extent=[0,16,nb-0.5,-0.5])
for x in range(17): ax[1].axvline(x, color='k', lw=0.3 if x%4 else 1.0, alpha=0.4)
ax[1].set_yticks(range(nb)); ax[1].set_yticklabels([f'{i-(len(starts)-len(down))}' for i in range(nb)], fontsize=8)
ax[1].set_title('dominant vocal bin (pitch proxy) where vocal energy > 0.25')
plt.tight_layout(); plt.savefig(ROOT/'out/wip/bargrid.png', dpi=50); print('ok', nb)
