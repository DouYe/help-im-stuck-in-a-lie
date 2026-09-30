import json
from pathlib import Path

import librosa
import numpy as np
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parent
y, sr = librosa.load(ROOT / 'assembly_40_70.wav', sr=22050, mono=True)
hop = 256
onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset, sr=sr, hop_length=hop, trim=False)
times = librosa.frames_to_time(np.arange(len(onset)), sr=sr, hop_length=hop)
beat_times = 40 + librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop)
peak_idx, peak_props = find_peaks(onset, distance=int(.14 * sr / hop), prominence=np.std(onset) * .32)
peak_times = 40 + times[peak_idx]
peak_strength = onset[peak_idx]
peak_list = [{'t': round(float(t), 3), 'strength': round(float(s), 3)} for t,s in zip(peak_times, peak_strength) if 43 <= t <= 67]

# A short-time measure suitable for spotting word attacks and accents.
rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0]
spec = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop))
centroid = librosa.feature.spectral_centroid(S=spec, sr=sr)[0]
chunks = []
for t in np.arange(43, 67, .25):
    a = np.searchsorted(times,t-40)
    b = np.searchsorted(times,t+.25-40)
    chunks.append({'t':round(float(t),2),'rms':round(float(np.mean(rms[a:b])),4),'onset':round(float(np.max(onset[a:b])),3),'centroid':round(float(np.mean(centroid[a:b])),0)})

data = {
    'source_offset':40,
    'analysis_duration': len(y)/sr,
    'beat_track_tempo':float(np.asarray(tempo).ravel()[0]),
    'beat_times':np.round(beat_times[(beat_times>=43)&(beat_times<=67)],3).tolist(),
    'onset_peaks':peak_list,
    'quarter_second_bins':chunks,
}
(ROOT/'rhythm.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps({'tempo':data['beat_track_tempo'],'beats':data['beat_times'],'onsets':sorted(peak_list,key=lambda x:x['strength'],reverse=True)[:25]},indent=2))
