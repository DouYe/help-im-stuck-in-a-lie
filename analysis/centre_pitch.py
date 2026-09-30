"""Pitch contour of the centre-masked vocal (harmonic-sum salience + Viterbi). Saves analysis/cpitch.npz"""
import numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
V = np.load(ROOT/'analysis/centre.npz')['V'].astype(np.float32)
T, KB = V.shape
binhz = 44100/2048
C = V ** 0.6
cents = np.arange(0, 3000, 10); f0s = 150*2**(cents/1200)           # 150 .. ~840 Hz
H = 10; hw = 0.85**np.arange(H)
pos = f0s[:, None]*np.arange(1, H+1)[None, :]/binhz
b0 = np.floor(pos).astype(int); bf = (pos-b0).astype(np.float32); ok = (b0+1) < KB
b0 = np.where(ok, b0, 0); bf = np.where(ok, bf, 0)
SAL = np.zeros((T, len(f0s)), np.float32)
for s in range(0, T, 1000):
    e = min(T, s+1000); X = C[s:e]
    v = (X[:, b0]*(1-bf) + X[:, b0+1]*bf)*ok
    # subtract the sub-octave to reduce octave errors
    SAL[s:e] = (v*hw).sum(2)
S = SAL/(np.percentile(SAL, 99, axis=1, keepdims=True)+1e-6)
nC = S.shape[1]; jump = np.abs(np.arange(nC)[:, None]-np.arange(nC)[None, :])
trans = -0.03*(jump/10.0); trans[jump > 120] = -1e9
score = S[0].copy(); back = np.zeros((T, nC), np.int16)
for t in range(1, T):
    cand = score[None, :]+trans; j = np.argmax(cand, 1); back[t] = j; score = cand[np.arange(nC), j]+S[t]
p = np.zeros(T, int); p[-1] = int(np.argmax(score))
for t in range(T-1, 0, -1): p[t-1] = back[t, p[t]]
en = np.sqrt((V[:, 12:186]**2).sum(1)); en /= np.percentile(en, 99.5)
np.savez_compressed(ROOT/'analysis/cpitch.npz', f0=f0s[p], sal=SAL[np.arange(T), p]/(np.percentile(SAL, 99.5)+1e-9), en=en, cents=cents, S=S.astype(np.float16))
print('ok')
