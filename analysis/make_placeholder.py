"""Placeholder track + timing data for 'Help! I'm stuck in a LIE' (first 15 s).

Synthesizes an original 128 BPM beat (kick / snare / hats / bass / pad / a lead
"voice" that plays one note per word), and writes the same data files the
P(doom) engine reads: data/audio.json (beats, downbeats, sections, envelopes,
onsets) and data/lyrics.json (word timings). Because every sound is generated
here, the timings are exact; for the real song they come from analysis
(beat tracking + forced alignment) instead.
"""
import json, wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SR = 44100
BPM = 128.0
BEAT = 60.0 / BPM            # 0.46875 s
BAR = 4 * BEAT               # 1.875 s
DUR = 16.0                   # a little tail past 15 s
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

stems = {k: np.zeros(N) for k in ['kick', 'snare', 'hat', 'bass', 'pad', 'voice']}
onsets = {'kick': [], 'snare': [], 'hat': [], 'vocal': []}

def add(stem, start, sig):
    i = int(start * SR)
    j = min(N, i + len(sig))
    if i < N: stems[stem][i:j] += sig[: j - i]

def env_exp(n, tau): return np.exp(-np.arange(n) / SR / tau)

def kick(at, amp=1.0):
    n = int(0.45 * SR); tt = np.arange(n) / SR
    f = 45 + 110 * np.exp(-tt / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 0.16) + 0.3 * rng.standard_normal(n) * env_exp(n, 0.004)
    add('kick', at, amp * s); onsets['kick'].append([round(at, 4), round(amp, 3)])

def snare(at, amp=0.8):
    n = int(0.3 * SR); tt = np.arange(n) / SR
    s = 0.6 * rng.standard_normal(n) * env_exp(n, 0.07) + 0.5 * np.sin(2 * np.pi * 190 * tt) * env_exp(n, 0.05)
    add('snare', at, amp * s); onsets['snare'].append([round(at, 4), round(amp, 3)])

def hat(at, amp=0.25, open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    s = np.diff(rng.standard_normal(n + 1)) * env_exp(n, 0.08 if open_ else 0.015)
    add('hat', at, amp * s); onsets['hat'].append([round(at, 4), round(amp, 3)])

def saw(freq, n):
    tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * freq * k * tt) / k for k in range(1, 12)) * 0.5

def note(stem, at, dur, freq, amp, a=0.005, r=0.08, sat=1.0):
    n = int((dur + r) * SR); tt = np.arange(n) / SR
    e = np.clip(tt / a, 0, 1) * np.where(tt < dur, 1.0, np.exp(-(tt - dur) / (r / 4)))
    s = np.tanh(sat * saw(freq, n)) * e
    add(stem, at, amp * s)

midi = lambda m: 440.0 * 2 ** ((m - 69) / 12)
b2t = lambda bar, beat=0.0: bar * BAR + beat * BEAT

# ---- arrangement: 8 bars = 15 s. bars 0-1 intro, 2-3 build, 4-7 drop
for bar in range(8):
    for bt in range(4):
        at = b2t(bar, bt)
        if bar >= 2 or bt == 0: kick(at, 1.0 if bar >= 4 else 0.75)
        if bar >= 2 and bt in (1, 3): snare(at, 0.9 if bar >= 4 else 0.7)
        for h in (0.5,) if bar < 2 else (0.0, 0.5):
            hat(at + h * BEAT, 0.22 if h else 0.12, open_=(bar >= 4 and h == 0.5))
    if bar == 3:  # snare roll into the drop
        for k in range(8): snare(b2t(3, 2) + k * BEAT / 4, 0.3 + 0.07 * k)

# bass (A minor: A, F, C, G) from bar 2, eighth-note pulses
roots = [45, 41, 48, 43]
for bar in range(2, 8):
    r = roots[bar % 4]
    for e in range(8):
        note('bass', b2t(bar, e / 2), BEAT / 2 * 0.8, midi(r - 12 if e % 2 == 0 else r), 0.35, sat=2.0)

# pad: whole-bar chords the whole way
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
for bar in range(8):
    for m in chords[bar % 4]:
        note('pad', b2t(bar), BAR, midi(m), 0.06 if bar < 4 else 0.08, a=0.3, r=0.6)

# ---- the "voice": one lead note per word, at the word timings below
LINES = [
    # (text, [(word, bar, beat, dur_beats, midi)])
    ("Help!", [("Help!", 1, 2.0, 1.5, 76)]),
    ("I'm stuck in a LIE", [("I'm", 2, 0.0, 0.9, 72), ("stuck", 2, 1.0, 0.9, 74), ("in", 2, 2.0, 0.45, 72),
                            ("a", 2, 2.5, 0.45, 71), ("LIE", 2, 3.0, 4.5, 69)]),
    ("Help!", [("Help!", 4, 0.0, 1.5, 76)]),
    ("I'm stuck in a LIE", [("I'm", 5, 0.0, 0.9, 72), ("stuck", 5, 1.0, 0.9, 74), ("in", 5, 2.0, 0.45, 72),
                            ("a", 5, 2.5, 0.45, 71), ("LIE", 5, 3.0, 3.5, 69)]),
    ("LIE LIE LIE LIE", [("LIE", 7, 0.0, 0.45, 81), ("LIE", 7, 1.0, 0.45, 79), ("LIE", 7, 2.0, 0.45, 77),
                         ("LIE", 7, 3.0, 0.9, 76)]),
]
lines = []
for text, ws in LINES:
    words = []
    for w, bar, bt, db, m in ws:
        s = b2t(bar, bt); e = s + db * BEAT
        note('voice', s, db * BEAT * 0.95, midi(m), 0.16, a=0.01, r=0.12, sat=1.5)
        onsets['vocal'].append([round(s, 4), 0.8])
        words.append({"w": w, "start": round(s, 4), "end": round(e, 4)})
    lines.append({"text": text, "start": words[0]["start"], "end": words[-1]["end"], "words": words})

# ---- mix + write wav
mix = (stems['kick'] * 0.9 + stems['snare'] * 0.5 + stems['hat'] * 0.5 + stems['bass'] + stems['pad'] + stems['voice'])
fade = np.clip((DUR - t) / 0.8, 0, 1)
mix = np.tanh(1.2 * mix * fade) * 0.85
(ROOT / 'audio').mkdir(exist_ok=True)
with wave.open(str(ROOT / 'audio' / 'song.wav'), 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())

# ---- envelopes at 100 fps, normalised 0..1 (what the engine's f.a.* reads)
FPS = 100
hop = SR // FPS
def envelope(x):
    n = len(x) // hop
    r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
    return r / (r.max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f >= hi)] = 0
    return np.fft.irfft(X, len(x))
drums = stems['kick'] + stems['snare'] + stems['hat']
feat = {
    'rms': envelope(mix), 'low': envelope(band(mix, 20, 200)), 'mid': envelope(band(mix, 200, 2000)),
    'high': envelope(band(mix, 2000, 16000)), 'vocal': envelope(stems['voice']), 'drums': envelope(drums),
    'bass': envelope(stems['bass']), 'other': envelope(stems['pad']),
}
beats = [round(i * BEAT, 4) for i in range(int(DUR / BEAT) + 1)]
audio = {
    'duration': DUR, 'bpm': BPM, 'beat_period': BEAT, 'time_signature': 4, 'fps': FPS,
    'beats': beats, 'downbeats': beats[::4],
    'sections': [{'name': 'intro', 'start': 0.0, 'end': b2t(2)}, {'name': 'build', 'start': b2t(2), 'end': b2t(4)},
                 {'name': 'drop', 'start': b2t(4), 'end': DUR}],
    **{k: [round(float(v), 4) for v in a] for k, a in feat.items()},
    'onsets': {k: sorted(v) for k, v in onsets.items()},
}
(ROOT / 'data').mkdir(exist_ok=True)
json.dump(audio, open(ROOT / 'data' / 'audio.json', 'w'))
json.dump({'lines': lines, 'extras': [], 'notes': 'placeholder timings for the synthesized demo beat'},
          open(ROOT / 'data' / 'lyrics.json', 'w'), indent=1)
print('ok', len(beats), 'beats;', sum(len(l['words']) for l in lines), 'words')
