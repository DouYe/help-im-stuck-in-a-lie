"""Refine CTC word times with the separated vocal: snap each word start to the nearest vocal onset
(spectral flux peak) around the CTC spike; end = where the vocal energy falls away before the next word.
Also plots the vocal spectrogram with the words for checking.  usage: refine.py align.json out.json out.png"""
import sys, json, os
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(sys.argv[1]))
sr, v = wavfile.read(os.path.join(ROOT, 'audio', os.environ.get('SONG', 'edit'), 'vocals.wav'))
x = v.astype(np.float32).mean(1) / 32768.0
HOP = 220  # 5 ms
N = 2048
win = np.hanning(N)
nfr = (len(x) - N) // HOP
idx = np.arange(N)[None, :] + HOP * np.arange(nfr)[:, None]
# restrict to the analysed window
t0 = min(w['start'] for w in d['words']) - 3; t1 = max(w['end'] for w in d['words']) + 3
f0, f1 = int(t0 * sr / HOP), int(t1 * sr / HOP)
idx = idx[f0:f1]
S = np.abs(np.fft.rfft(x[idx] * win, axis=1))
freqs = np.fft.rfftfreq(N, 1 / sr)
# log-mel-ish bands 80..8000
edges = np.geomspace(80, 8000, 65)
B = np.stack([S[:, (freqs >= a) & (freqs < b)].sum(1) for a, b in zip(edges[:-1], edges[1:])], 1)
L = np.log1p(B * 50)
flux = np.maximum(0, np.diff(L, axis=0, prepend=L[:1])).sum(1)
flux = np.convolve(flux, np.hanning(7) / np.hanning(7).sum(), 'same')
rms = np.sqrt((x[idx] ** 2).mean(1))
rms_s = np.convolve(rms, np.hanning(9) / np.hanning(9).sum(), 'same')
tt = (np.arange(f0, f1) * HOP + N / 2) / sr
pk, _ = find_peaks(flux, height=np.percentile(flux, 60), distance=int(0.06 * sr / HOP))
ptimes = tt[pk]; pvals = flux[pk]
words = d['words']
for i, w in enumerate(words):
    c = w['start']
    cand = [(abs(pt - c) + (0.04 if pt > c else 0), pt, pv) for pt, pv in zip(ptimes, pvals) if c - 0.28 <= pt <= c + 0.1]
    if cand:
        # prefer strong peaks close to the CTC spike
        best = min(cand, key=lambda z: z[0] - 0.08 * z[2] / (pvals.max() + 1e-9))
        w['onset'] = round(float(best[1]), 3)
    else:
        w['onset'] = round(c - 0.03, 3)
for i, w in enumerate(words):
    nxt = words[i + 1]['onset'] if i + 1 < len(words) else w['onset'] + 1.5
    a = np.searchsorted(tt, w['onset']); b = np.searchsorted(tt, nxt)
    seg = rms_s[a:b]
    if len(seg) < 3: w['off'] = round(float(nxt), 3); continue
    pkv = seg[: max(3, len(seg) // 2)].max()
    # last frame above 25% of the word's peak (the note's release), capped at the next onset
    above = np.where(seg > 0.25 * pkv)[0]
    e = tt[a + above[-1]] if len(above) else tt[b - 1]
    w['off'] = round(float(min(e + 0.02, nxt - 0.01)), 3)
json.dump(d, open(sys.argv[2], 'w'), indent=0)
# ---- plot
try:
    from PIL import Image, ImageDraw
    img = L.T[::-1]
    img = (255 * (img - img.min()) / (img.max() - img.min() + 1e-9)).astype(np.uint8)
    Wd = 3200; H = 64 * 5
    im = Image.fromarray(img).resize((Wd, H)).convert('RGB')
    canvas = Image.new('RGB', (Wd, H + 260), (12, 12, 12)); canvas.paste(im, (0, 0))
    dr = ImageDraw.Draw(canvas)
    X = lambda t: int((t - tt[0]) / (tt[-1] - tt[0]) * Wd)
    # rms curve
    r = rms_s / rms_s.max()
    for k in range(1, len(tt)):
        dr.line([(X(tt[k - 1]), H + 120 - r[k - 1] * 100), (X(tt[k]), H + 120 - r[k] * 100)], fill=(200, 200, 200))
    for pt in ptimes: dr.line([(X(pt), H + 125), (X(pt), H + 135)], fill=(120, 120, 255))
    for w in words:
        dr.line([(X(w['onset']), 0), (X(w['onset']), H + 140)], fill=(255, 90, 20), width=2)
        dr.line([(X(w['off']), H + 20), (X(w['off']), H + 140)], fill=(120, 60, 20))
        dr.text((X(w['onset']) + 3, H + 145 + 18 * (words.index(w) % 3)), w['w'], fill=(255, 255, 255))
    # seconds ticks
    s = int(tt[0]) + 1
    while s < tt[-1]:
        dr.line([(X(s), H + 200), (X(s), H + 215)], fill=(160, 160, 160)); dr.text((X(s) + 2, H + 218), str(s), fill=(160, 160, 160)); s += 1
    canvas.save(sys.argv[3])
except Exception as e:
    print('plot failed', e)
for w in words: print(f"{w['line']} {w['onset']:7.3f} {w['off']:7.3f}  ctc {w['start']:7.3f}  {w['w']}")
