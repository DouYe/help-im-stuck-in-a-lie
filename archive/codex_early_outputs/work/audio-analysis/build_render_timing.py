import json
import re
from pathlib import Path

import librosa
import numpy as np
from scipy.ndimage import gaussian_filter1d

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'assembly-video' / 'timing.json'
OUT.parent.mkdir(parents=True, exist_ok=True)
CLIP_START = 47.0
CLIP_DURATION = 20.0
FPS = 60

transcript = json.loads((ROOT / 'transcript.json').read_text(encoding='utf-8'))
raw_words = [w for seg in transcript for w in seg['words'] if w['start'] >= 46.9]
phrase_words = [
    ['Help,', "I'm", 'stuck', 'in', 'the', 'line'],
    ['Stuck', 'in', 'the', 'line'],
    ['Make', 'me', 'real', 'this', 'time'],
    ['Real', 'this', 'time'],
    ['Help,', "I'm", 'stuck', 'in', 'the', 'line'],
    ['Stuck', 'in', 'the', 'line'],
    ['I', 'still', 'got', 'a', 'heart', 'inside'],
    ['Heart', 'inside'],
]
assert sum(map(len, phrase_words)) == len(raw_words)
lines = []
i = 0
for phrase in phrase_words:
    line_words = []
    for expected in phrase:
        found = raw_words[i]
        assert re.sub(r'[^a-z]', '', expected.lower()) == re.sub(r'[^a-z]', '', found['word'].lower()), (expected, found)
        start = max(0.0, found['start'] - CLIP_START)
        end = min(CLIP_DURATION, found['end'] - CLIP_START)
        if expected == 'I' and i == 28 and end == start:
            start = 15.08  # ASR gives a zero-length timestamp; assign a short lead-in.
            end = 15.14
        line_words.append({'text': expected, 'start': round(start, 3), 'end': round(end, 3)})
        i += 1
    lines.append({'start':line_words[0]['start'], 'end':line_words[-1]['end'], 'words':line_words})

bar_zero = 47.6941667
beat_period = 2.43027381 / 4
beats = [round(bar_zero + n * beat_period - CLIP_START, 4)
         for n in range(-1, 34) if 0 <= bar_zero + n * beat_period - CLIP_START < CLIP_DURATION]

y, sr = librosa.load(ROOT / 'assembly_40_70.wav', sr=22050, mono=True)
hop = 256
rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop, center=True)[0]
rms = gaussian_filter1d(rms, sigma=2.0)
rms_times = 40 + librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
sample_times = CLIP_START + (np.arange(CLIP_DURATION*FPS) + 0.5) / FPS
values = np.interp(sample_times,rms_times,rms)
lo, hi = np.quantile(values,[0.05,0.97])
energy = np.clip((values-lo)/(hi-lo),0,1)
energy = np.round(energy,3).tolist()

data = {'clipStart':CLIP_START, 'bpm':round(60/beat_period,4),
        'beats':beats, 'energy':energy, 'lines':lines}
OUT.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'output':str(OUT),'bpm':data['bpm'],'beat_count':len(beats),'frame_count':len(energy),
                  'energy_quantiles':np.quantile(energy,[0,.1,.5,.9,1]).round(3).tolist(),
                  'lines':[{k:v for k,v in x.items() if k!='words'} for x in lines]},indent=2))
