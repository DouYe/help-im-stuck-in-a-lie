import json
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent
model_root = Path(r'C:\Users\honkw\Documents\Codex\2026-09-12\distrokid\work\models')
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=6, download_root=str(model_root))
prompt = "Help, I'm stuck in the line. Stuck in the line. Make me real this time. Real this time. Help, I'm stuck in the line. Stuck in the line. I still got a heart inside. Heart inside."
segments, info = model.transcribe(str(ROOT/'assembly_40_70.wav'), language='en', beam_size=5, condition_on_previous_text=False, vad_filter=False, word_timestamps=True, initial_prompt=prompt)
items = []
for seg in segments:
    item = {'start':round(40+seg.start,3), 'end':round(40+seg.end,3), 'text':seg.text.strip(), 'words':[{'start':round(40+w.start,3),'end':round(40+w.end,3),'word':w.word} for w in (seg.words or [])]}
    items.append(item)
    print(json.dumps(item,ensure_ascii=False),flush=True)
(ROOT/'transcript.json').write_text(json.dumps(items,indent=2,ensure_ascii=False),encoding='utf-8')
