"""Aligned word times (refine.py output) -> data/lyrics.json (engine format)."""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(sys.argv[1]))
lines = {}
for w in d['words']:
    lines.setdefault(w['line'], []).append(w)
out = []
for li in sorted(lines):
    ws = lines[li]
    words = [{'w': w['w'], 'start': round(w['onset'], 3), 'end': round(max(w['off'], w['onset'] + 0.08), 3)} for w in ws]
    text = ' '.join(w['w'] for w in ws)
    out.append({'text': text, 'start': words[0]['start'], 'end': words[-1]['end'], 'words': words})
json.dump({'lines': out, 'extras': [], 'notes': 'Aligned: UVR-MDX-NET vocal separation + CTC forced alignment (zipformer2 CTC, '
           'sherpa-onnx) of the known lyrics, word starts snapped to vocal onsets. analysis/align/.'},
          open(os.path.join(ROOT, 'data', 'lyrics.json'), 'w'), indent=1)
for l in out: print(f"{l['start']:7.3f}-{l['end']:7.3f}  {l['text']}")
