import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path('/home/claude/lie-video')
c = np.load(ROOT/'analysis/cache.npz'); a = json.load(open(ROOT/'data/audio.real.json'))
LM = c['LM'].astype(np.float32); HcLM = c['HcLM'].astype(np.float32)
beats = np.array(a['beats']); bi = np.clip((beats*100).astype(int), 0, len(LM)-1)
# bar-synchronous features (downbeats)
down = np.array(a['downbeats']); di = np.clip((down*100).astype(int), 0, len(LM)-1)
def sync(X, idx):
    return np.array([X[idx[i]:idx[i+1]].mean(0) if i+1 < len(idx) else X[idx[i]:].mean(0) for i in range(len(idx))])
F = np.hstack([sync(LM, bi), sync(HcLM, bi)])
F = (F - F.mean(0)) / (F.std(0)+1e-6); F /= np.linalg.norm(F, axis=1, keepdims=True)
S = F @ F.T
# smooth along diagonals (8 beats) to show repeated sequences
from scipy import ndimage
k = np.eye(8)/8
Sd = ndimage.convolve(S, k, mode='nearest')
fig, ax = plt.subplots(1, 2, figsize=(22, 11))
ax[0].imshow(Sd, cmap='magma', origin='upper', extent=[beats[0], beats[-1], beats[-1], beats[0]], vmin=0, vmax=np.percentile(Sd, 99.5))
ax[0].set_xticks(np.arange(0, 200, 10)); ax[0].set_yticks(np.arange(0, 200, 10)); ax[0].grid(alpha=0.3)
# vocal activity per bar
voc = c['vocal']; vb = np.array([voc[di[i]:di[i+1]].mean() if i+1<len(di) else voc[di[i]:].mean() for i in range(len(di))])
en = np.array([np.exp(LM[di[i]:di[i+1]]).mean() if i+1<len(di) else 0 for i in range(len(di))])
ax[1].bar(down, vb, width=2.2, color='cyan', alpha=0.7, align='edge', label='vocal (centre harmonic)')
ax[1].plot(down, en/en.max(), color='orange', label='loudness')
ax[1].set_xticks(np.arange(0, 200, 5)); ax[1].grid(alpha=0.3); ax[1].legend()
plt.tight_layout(); plt.savefig(ROOT/'out/wip/ssm.png', dpi=55)
print('bars', len(down), 'bar len', np.diff(down).mean())
