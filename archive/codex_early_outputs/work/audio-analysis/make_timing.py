import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
transcript = json.loads((ROOT/'transcript.json').read_text(encoding='utf-8'))
words = [w for seg in transcript for w in seg['words'] if w['start'] >= 46.9]
phrases = [
    ("Help, I'm stuck in the line",0,6),
    ("Stuck in the line",6,10),
    ("Make me real this time",10,15),
    ("Real this time",15,18),
    ("Help, I'm stuck in the line",18,24),
    ("Stuck in the line",24,28),
    ("I still got a heart inside",28,34),
    ("Heart inside",34,36),
]
output = {'source_file':r'C:\Users\honkw\Downloads\Assembly Line Heart.mp3',
          'clip_start':45.0,'clip_end':65.0,
          'tempo_bpm':98.7543046,'bar_zero_absolute':47.6941667,
          'bar_period_seconds':2.43027381,
          'beat_period_seconds':.60756845,
          'timing_method':'faster-whisper-small English word timestamps, checked against repeating instrumental onsets; estimated, not manual listening',
          'phrases':[]}
for text,a,b in phrases:
    ww=[]
    for w in words[a:b]:
        ww.append({'text':w['word'].strip(),
                   'start':w['start'],'end':w['end'],
                   'start_in_clip':round(w['start']-45,3),'end_in_clip':round(w['end']-45,3)})
    output['phrases'].append({'text':text,'start':ww[0]['start'],'end':ww[-1]['end'],
                              'start_in_clip':ww[0]['start_in_clip'],'end_in_clip':ww[-1]['end_in_clip'],
                              'within_requested_clip':ww[-1]['end']<=65,
                              'words':ww})
(ROOT/'timing_45_65.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps([{k:v for k,v in p.items() if k!='words'} for p in output['phrases']],indent=2))
