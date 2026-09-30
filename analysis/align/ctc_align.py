"""Forced alignment of known lyrics to the separated vocal with a CTC model (sherpa-onnx zipformer2
CTC, LibriSpeech BPE-500, onnxruntime). Kaldi-style 80-bin fbank (numpy), Viterbi over the CTC
lattice with the exact transcript, word times from the token spans.
usage: python3 ctc_align.py <t0> <t1> "<line 1>|<line 2>|..."  -> prints JSON word times
"""
import sys, os, json, math
import numpy as np
from scipy.io import wavfile
import onnxruntime as ort

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = os.environ.get('CTC', '/tmp/claude-0/models/sherpa-onnx-zipformer-ctc-en-2023-10-02')

def kaldi_fbank(x, sr=16000, nmel=80, low=20.0, high=-400.0):
    fl, fs, nfft = 400, 160, 512
    n = (len(x) + fs // 2) // fs                      # snip_edges = false
    xp = np.pad(x, (fl, fl), mode='reflect')
    frames = np.empty((n, fl), np.float64)
    for i in range(n):
        s = i * fs + fs // 2 - fl // 2 + fl
        frames[i] = xp[s:s + fl]
    frames -= frames.mean(1, keepdims=True)           # remove DC
    pre = frames.copy(); pre[:, 1:] -= 0.97 * frames[:, :-1]; pre[:, 0] -= 0.97 * frames[:, 0]
    win = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(fl) / (fl - 1))) ** 0.85
    spec = np.abs(np.fft.rfft(pre * win, n=nfft)) ** 2
    hi = sr / 2 + high if high <= 0 else high
    mel = lambda f: 1127.0 * np.log(1.0 + f / 700.0)
    mlo, mhi = mel(low), mel(hi)
    centers = mlo + (mhi - mlo) * np.arange(nmel + 2) / (nmel + 1)
    fbin = mel(np.arange(nfft // 2 + 1) * sr / nfft)
    W = np.zeros((nmel, nfft // 2 + 1))
    for m in range(nmel):
        l, c, r = centers[m], centers[m + 1], centers[m + 2]
        up = (fbin - l) / (c - l); dn = (r - fbin) / (r - c)
        W[m] = np.maximum(0, np.minimum(up, dn))
    e = spec @ W.T
    return np.log(np.maximum(e, np.finfo(np.float32).eps)).astype(np.float32)

def load_tokens():
    toks = {}
    for line in open(os.path.join(MD, 'tokens.txt'), encoding='utf-8'):
        p, i = line.rstrip('\n').rsplit(' ', 1); toks[p] = int(i)
    return toks

def tokenize_word(w, toks):
    """Fewest-pieces segmentation of '▁WORD' into vocabulary pieces (DP)."""
    s = '▁' + w
    n = len(s); best = [None] * (n + 1); best[0] = []
    for i in range(n):
        if best[i] is None: continue
        for j in range(i + 1, n + 1):
            p = s[i:j]
            if p in toks and (best[j] is None or len(best[i]) + 1 < len(best[j])): best[j] = best[i] + [p]
    if best[n] is None:  # fall back: '▁' then letters
        return [p for p in ['▁'] + list(w) if p in toks]
    return best[n]

def viterbi(lp, ids):
    """CTC forced alignment. lp [T, V] log-probs, ids token ids. Returns per-token (first, last) frame."""
    T = lp.shape[0]; S = 2 * len(ids) + 1
    lab = [0] * S
    for k, t in enumerate(ids): lab[2 * k + 1] = t
    NEG = -1e30
    dp = np.full((T, S), NEG); bp = np.zeros((T, S), np.int32)
    dp[0, 0] = lp[0, 0]; dp[0, 1] = lp[0, lab[1]]
    for t in range(1, T):
        for s in range(S):
            cands = [(dp[t - 1, s], s)]
            if s >= 1: cands.append((dp[t - 1, s - 1], s - 1))
            if s >= 2 and lab[s] != 0 and lab[s] != lab[s - 2]: cands.append((dp[t - 1, s - 2], s - 2))
            v, a = max(cands)
            dp[t, s] = v + lp[t, lab[s]]; bp[t, s] = a
    s = S - 1 if dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    path = [0] * T
    for t in range(T - 1, -1, -1):
        path[t] = s; s = bp[t, s]
    spans = [[None, None] for _ in ids]
    for t, s in enumerate(path):
        if s % 2 == 1:
            k = s // 2
            if spans[k][0] is None: spans[k][0] = t
            spans[k][1] = t
    return spans, path

def main():
    t0, t1 = float(sys.argv[1]), float(sys.argv[2])
    lines = [l.strip() for l in sys.argv[3].split('|') if l.strip()]
    sr, v = wavfile.read(os.path.join(ROOT, 'audio', os.environ.get('SONG', 'edit'), 'vocals_16k.wav'))
    x = v.astype(np.float32) / 32768.0
    seg = x[int(t0 * sr):int(t1 * sr)]
    feats = kaldi_fbank(seg)
    sess = ort.InferenceSession(os.path.join(MD, 'model.onnx'), providers=['CPUExecutionProvider'])
    lp, ln = sess.run(None, {'x': feats[None], 'x_lens': np.array([feats.shape[0]], np.int64)})
    lp = lp[0][:ln[0]]
    fshift = (t1 - t0) / lp.shape[0]
    toks = load_tokens()
    words, ids, owner = [], [], []
    for li, l in enumerate(lines):
        for w in l.split():
            clean = ''.join(ch for ch in w.upper() if ch.isalpha() or ch == "'")
            pieces = tokenize_word(clean, toks)
            for p in pieces: ids.append(toks[p]); owner.append(len(words))
            words.append({'w': w, 'line': li, 'pieces': pieces})
    spans, path = viterbi(lp, ids)
    # greedy decode for reference
    g = lp.argmax(1); inv = {v: k for k, v in toks.items()}
    hyp = []; prev = -1
    for k in g:
        if k != prev and k != 0: hyp.append(inv[int(k)])
        prev = k
    for wi, wd in enumerate(words):
        ks = [k for k, o in enumerate(owner) if o == wi]
        f0 = min(spans[k][0] for k in ks); f1 = max(spans[k][1] for k in ks)
        wd['start'] = round(t0 + f0 * fshift, 3); wd['end'] = round(t0 + (f1 + 1) * fshift, 3)
        wd['conf'] = round(float(np.mean([lp[spans[k][0]:spans[k][1] + 1, ids[k]].max() for k in ks])), 2)
    print(json.dumps({'fshift': fshift, 'greedy': ''.join(hyp).replace('▁', ' ').strip(), 'words': words}, indent=0))

if __name__ == '__main__':
    main()
