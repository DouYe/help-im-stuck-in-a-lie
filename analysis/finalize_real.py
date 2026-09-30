"""Finalize the real song's timing data for the engine.

1. Beat grid: the constant-tempo grid from analyze_song.py, nudged per beat toward the actual drum
   onsets (running median of local offsets, +-60 ms), so hits land on the kick/snare.
2. Sections by bar (structure read from the self-similarity / vocal plots, see analysis notes).
3. Chorus 1 word timings (+ the last pre-chorus line), in BEATS from the chorus downbeat, converted to
   seconds on the refined grid. Estimated from the centre-channel vocal (pitch/energy) plots and the
   repeat of the chorus melody after 4 bars; syllables snapped to the 16th-note grid.
Writes data/audio.json and data/lyrics.json (the demo beat's files move to data/demo/).
"""
import json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import os
SONG = os.environ.get('SONG', 'edit')
a = json.load(open(ROOT / 'data' / f'audio.{SONG}.json'))
c = np.load(ROOT / 'analysis' / f'cache.{SONG}.npz')
o = c['oenv'].astype(np.float32)
beats = np.array(a['beats'])

# ---- 1. per-beat nudge toward the onsets
offs, w = np.full(len(beats), np.nan), np.zeros(len(beats))
for i, b in enumerate(beats):
    i0, i1 = int((b - 0.07) * 100), int((b + 0.07) * 100) + 1
    if i0 < 0 or i1 >= len(o): continue
    seg = o[i0:i1]; j = int(np.argmax(seg))
    offs[i] = (i0 + j) / 100 - b; w[i] = seg[j]
good = (w > np.percentile(w[w > 0], 40)) & ~np.isnan(offs)
sm = np.zeros(len(beats))
for i in range(len(beats)):
    lo, hi = max(0, i - 8), min(len(beats), i + 9)
    g = good[lo:hi]
    sm[i] = np.median(offs[lo:hi][g]) if g.sum() >= 3 else np.nan
idx = np.arange(len(beats)); ok = ~np.isnan(sm)
sm = np.interp(idx, idx[ok], sm[ok])
sm = np.clip(sm, -0.06, 0.06)
beats2 = beats + sm
assert np.all(np.diff(beats2) > 0.4)
first_down = int(np.argmin(np.abs(beats - a['downbeats'][0])))
down2 = beats2[first_down::4]
bar = lambda n: float(down2[n])
beat_of_bar = lambda n: first_down + 4 * n
tb = lambda k: float(np.interp(k, idx, beats2))   # time of (fractional) beat index

# ---- 2. sections
secs = [('intro', 0.0, bar(6)), ('verse1', bar(6), bar(14)), ('pre1', bar(14), bar(16)), ('chorus1', bar(16), bar(24)),
        ('post1', bar(24), bar(25)), ('rest', bar(25), a['duration'])]
a['sections'] = [{'name': n, 'start': round(s, 3), 'end': round(e, 3)} for n, s, e in secs]
a['beats'] = [round(float(x), 4) for x in beats2]
a['downbeats'] = [round(float(x), 4) for x in down2]
a['notes'] = a.get('notes', '') + '; beats nudged to drum onsets (running median); sections by bar'

# ---- 3. lyrics (beats relative to the chorus downbeat = bar 16)
B0 = beat_of_bar(16)
LINES = [
    ('They want it bad', [('They', -1.2, -0.95), ('want', -0.93, -0.62), ('it', -0.6, -0.37), ('bad', -0.35, -0.02)]),
    ("Help, I'm stuck in a lie", [('Help,', 0.0, 0.45), ("I'm", 0.5, 0.95), ('stuck', 1.0, 1.45), ('in', 1.5, 1.72), ('a', 1.75, 1.97), ('lie', 2.0, 3.1)]),
    ('Stuck in a lie', [('Stuck', 5.0, 5.45), ('in', 5.5, 5.72), ('a', 5.75, 5.97), ('lie', 6.0, 7.2)]),
    ('Make me real this time', [('Make', 9.0, 9.45), ('me', 9.5, 9.95), ('real', 10.0, 10.55), ('this', 10.6, 11.05), ('time', 11.1, 12.0)]),
    ('Real this time', [('Real', 12.8, 13.5), ('this', 13.55, 14.05), ('time', 14.1, 15.45)]),
    ("Help, I'm stuck in a lie", [('Help,', 16.0, 16.45), ("I'm", 16.5, 16.95), ('stuck', 17.0, 17.45), ('in', 17.5, 17.72), ('a', 17.75, 17.97), ('lie', 18.0, 19.1)]),
    ('Stuck in a lie', [('Stuck', 21.0, 21.45), ('in', 21.5, 21.72), ('a', 21.75, 21.97), ('lie', 22.0, 23.2)]),
    ('I still got a heart inside', [('I', 24.75, 24.97), ('still', 25.0, 25.45), ('got', 25.5, 25.72), ('a', 25.75, 25.97), ('heart', 26.0, 26.55),
                                    ('inside', 26.6, 28.75, [(26.6, 27.2), (27.25, 28.75)])]),
    ('Heart inside', [('Heart', 28.9, 29.45), ('inside', 29.5, 31.1, [(29.5, 30.0), (30.05, 31.1)])]),
]
lines = []
for text, ws in LINES:
    words = []
    for wdef in ws:
        w, s, e = wdef[:3]
        d = {'w': w, 'start': round(tb(B0 + s), 4), 'end': round(tb(B0 + e), 4), 'beat': s}
        if len(wdef) > 3: d['syl'] = [[round(tb(B0 + x), 4), round(tb(B0 + y), 4)] for x, y in wdef[3]]
        words.append(d)
    lines.append({'text': text, 'start': words[0]['start'], 'end': words[-1]['end'], 'words': words})

demo = ROOT / 'data' / 'demo'
demo.mkdir(exist_ok=True)
for f in ('audio.json', 'lyrics.json'):
    p = ROOT / 'data' / f
    if p.exists() and not (demo / f).exists(): shutil.move(str(p), str(demo / f))
json.dump(a, open(ROOT / 'data' / 'audio.json', 'w'))
json.dump({'lines': lines, 'extras': [], 'notes': 'Chorus 1 (+ last pre-chorus line) only. Estimated without a separated vocal: '
           'syllables snapped to 16ths from centre-channel pitch/energy; see analysis/finalize_real.py.'},
          open(ROOT / 'data' / 'lyrics.json', 'w'), indent=1)
print('bar 15', round(bar(15), 3), 'bar 16', round(bar(16), 3), 'bar 24', round(bar(24), 3), 'bar 25', round(bar(25), 3))
for l in lines: print(f"{l['start']:7.3f}-{l['end']:7.3f}  {l['text']}")
