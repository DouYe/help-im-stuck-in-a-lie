# girl.txt -> girl_frames.ts  (run after editing the sprite text)
import json, os
here = os.path.dirname(os.path.abspath(__file__))
fr = {}; name = None
for line in open(os.path.join(here, 'girl.txt'), encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('== '): name = line[3:].strip(); fr[name] = []; continue
    if name is not None: fr[name].append(line)
for k in fr:
    while fr[k] and not fr[k][-1].strip(): fr[k].pop()
    w = max(len(r) for r in fr[k]); fr[k] = [r.ljust(w) for r in fr[k]]
open(os.path.join(here, 'girl_frames.ts'), 'w', encoding='utf-8').write(
    '// generated from girl.txt by gen_frames.py — edit the .txt, not this file\n'
    'export const GIRL: Record<string, string[]> = ' + json.dumps(fr, indent=1, ensure_ascii=False) + ';\n')
print(len(fr), 'frames')
