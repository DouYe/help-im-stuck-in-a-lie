from pathlib import Path
import re, shutil, zipfile
project=Path(__file__).resolve().parents[3]
out=Path(r'C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs\codex_six_worlds_motion_v1')
def edit(rel,fn):
    p=project/rel
    before=p.read_text(encoding='utf-8-sig')
    after=fn(before)
    if after!=before:p.write_text(after,encoding='utf-8')
summary='T24 delivered a20s1080p60 six-world motion revision,200incoming hazards (10/sec), instant control/double jump/dash and animated depth layers. Movie in renders/2026-09-30_codex_six_worlds_motion_v1.mp4; captured frames in design/keyframes/codex_six_worlds_motion_v1/; source in wip/codex/platformer_motion_v2/. See docs/CODEX_SIX_WORLDS_MOTION_V1.md. All older assets preserved; beat matching is deferred for this prototype.'
edit('docs/PROMPTS.md',lambda s:s.replace('Result: in progress with T24; preserving older prototypes.','Result: '+summary).replace('Result: in progress as T24, isolated `wip/codex/platformer_motion_v2/`.','Result: '+summary))
task='| T24 | Fast responsive six-world music-video revision; double jump/dash, underwater/sky/top-down, animated depth layers and10hazards/second | review | Hon (made by Codex 2026-09-30) | Delivered20s1080p60/200attacks plus6captured frames and portable playable engine.32control/framing checks and full video decode passed. `docs/CODEX_SIX_WORLDS_MOTION_V1.md`; isolated `wip/codex/platformer_motion_v2/`; retain T23. Exact beat matching deferred by Hon. |'
edit('coordination/TASKS.md',lambda s:re.sub(r'^\| T24 \|.*$',task,s,flags=re.M))
entry='''## 2026-09-30 · Codex (ChatGPT desktop) — fast six-world music-video revision (T24)
Asked: much faster immediate control, stronger/double jumps, water/air/overhead world variety, at least4animated depth layers, and roughly10incoming hazards/sec with extreme manual difficulty. Exact beat matching can be later.
Did: built an isolated revision with six direct-cut original glyph worlds, instant side control, double jump, dash, articulated swimming and top views, near-centered camera,3animated background depths plus actor/platform and brief foreground.200lyric/note attacks from6directions in20s. Automatic movie rehearses real physics and choreographs close attack crossings; manual mode has real collisions and room resets. Fixed old-slot re-emission on reset, wide-gap jump memory, sky landing/framing and decorative local-coordinate culling. No locked shared girl/app code changed; every prior image/movie preserved.
Files: `renders/2026-09-30_codex_six_worlds_motion_v1.mp4`; six captured full-size frames/review sheet/manifest at `design/keyframes/codex_six_worlds_motion_v1/`; engine/exporter/QA/notes at `wip/codex/platformer_motion_v2/`; `docs/CODEX_SIX_WORLDS_MOTION_V1.md`. Chat-output movie, sheet, source and ZIP are in `outputs/codex_six_worlds_motion_v1/`.
Validation:32meaningful input/finite/framing checks passed without browser errors. Final audit:6cuts,13jumps,12double jumps,5dashes,112passed hazards,0deaths on the rehearsed film route and one exit19.867s. Active shots peak29(includes offscreen). MP4 confirmed1920x1080/60fps/1200frames/20s with20s AAC; full decode passed; refreshed scene frames and encoded exit inspected.
Decisions: these are proposed motion worlds, not selected final scenes. This particular20s test defers L5 beat alignment per Hon's explicit latest instruction. Song source Final42.012–62.012s matches T23. Extreme manual difficulty is intentional, not game balancing.
Open: Hon's playback judgment on speed, visual pressure and layered scene variety; whole-song edit, rapid death montage, outside scene and combining close-up/P(doom) art remain future work. Claude's newer story_v1 stills are separate and preserved.
Next: use Hon's feedback to combine selected art and the working motion engine, then align cuts/attack phrases to the song. Source page runs locally on5189; old5188 remains unchanged.

'''
edit('coordination/WORKLOG.md',lambda s:s if '— fast six-world music-video revision (T24)' in s else s[:s.index('## ')] +entry+s[s.index('## '):])
now='- **Codex fast six-world motion revision (T24, review):**20s1080p60 movie at `renders/2026-09-30_codex_six_worlds_motion_v1.mp4`,6captured frames at `design/keyframes/codex_six_worlds_motion_v1/`, portable playable source at `wip/codex/platformer_motion_v2/`. Fast snap control, double jump/dash; factory/shaft/water/overhead/sky/cathedral; animated depth layers;200real lyric/note emissions (10/sec).32checks/full decode passed. Automatic movie route is choreographed; manual game intentionally extreme. See `docs/CODEX_SIX_WORLDS_MOTION_V1.md`. Beat alignment deferred for this test; old T23 retained.\n\n'
def status(s):
    if now.strip() not in s:s=s.replace('## Now\n\n','## Now\n\n'+now,1)
    s=re.sub(r'^Updated:.*$', 'Updated: **2026-09-30 · Codex T24 fast six-world motion revision in review; other current review sets are listed below**.',s,count=1,flags=re.M)
    old='- Playback feedback on T23: does the running/jumping/ducking and falling hair feel natural? Review the20s video and4s slow close view. This prototype uses one factory level; final many-style editing and outside environment remain open.'
    s=s.replace(old,'- Playback feedback on T24: speed/responsiveness, six-world variety, moving layers,10Hzattack pressure. Review the new20s movie and6frame sheet; T23/slow close view remain available for comparison. Final art, beat edit, death montage and exterior remain open.')
    note='- 2026-09-30 · Codex: T24 is the current motion proposal, isolated from the locked app and all other models. New film source uses rehearsed physics + calculated safe attack crossings, not general invulnerability; manual collision is real.10Hzemissions are fixed across room resets. For final integration inspect both this prototype and Claude story_v1; no scene selection approval claimed.\n'
    s=s.replace('## Notes between models\n','## Notes between models\n'+note,1) if note not in s else s
    s=s.replace('1. Hon reviews Codex T23 platformer video and hair follow-through,','1. Hon reviews Codex T24 six-world video/attack pressure and the preserved T23 hair follow-through,',1)
    return s
edit('coordination/STATUS.md',status)
direction='| A12 | **Motion revision T24:** music-video pacing comes first; much faster near-centered girl, immediate left/right start/reverse/stop, stronger/double jumps, water/sky/overhead4-axis scenes,4+animated depths and about10incoming symbol hazards/sec. Manual play may be essentially impossible. Hon explicitly defers exact beat matching at this prototype stage; final L5 remains. | 2026-09-30 |\n'
edit('docs/DECISIONS.md',lambda s:s if '| A12 |' in s else s.replace('## SELECTED AS VISUAL REFERENCES',direction+'\n## SELECTED AS VISUAL REFERENCES',1))
style='| **Codex fast six-world motion** — factory/shaft/water/overhead/sky/cathedral, immediate control/double jump/dash,10Hzlyric/note crossfire,3animated BG depths plus brief foreground | proposed motion revision awaiting Hon review; exact beat edit deferred | `keyframes/codex_six_worlds_motion_v1/six_worlds_review_sheet.png`; `renders/2026-09-30_codex_six_worlds_motion_v1.mp4` | `docs/CODEX_SIX_WORLDS_MOTION_V1.md`; source `wip/codex/platformer_motion_v2/`; shared locked rig unchanged |\n'
edit('design/STYLE_BIBLE.md',lambda s:s if '**Codex fast six-world motion**' in s else s.replace('|---|---|---|---|\n','|---|---|---|---|\n'+style,1))
row='| Fast six-world motion revision | **Codex20s1080p60 revision awaiting review** —200attacks/10Hz, instant control, doublejump/dash, water/sky/overhead travel and animated layers. `docs/CODEX_SIX_WORLDS_MOTION_V1.md`; all earlier files remain. |\n'
edit('README.md',lambda s:s if '| Fast six-world motion revision |' in s else s.replace('|---|---|\n','|---|---|\n'+row,1))
maps='| `wip/codex/platformer_motion_v2/` | T24six-world original Canvas revision,10Hzattack choreography/manual collision, character/world/topdown modules, renderer and32check QA; see `docs/CODEX_SIX_WORLDS_MOTION_V1.md` |\n| `renders/2026-09-30_codex_six_worlds_motion_v1.mp4` | T24motion proposal20s1080p60/200attacks, Final42.012–62.012s; beat matching deferred |\n| `design/keyframes/codex_six_worlds_motion_v1/` | Six actual simulation frames, review sheet and hashes; proposals for review, not selected final art |\n'
edit('docs/FILE_MAP.md',lambda s:s if '`wip/codex/platformer_motion_v2/`' in s else s.replace('## Code and data\n| Path | What |\n|---|---|\n','## Code and data\n| Path | What |\n|---|---|\n'+maps,1))
shutil.copy2(project/'docs/CODEX_SIX_WORLDS_MOTION_V1.md',out/'MOTION_NOTES.md')
with zipfile.ZipFile(out/'playable_engine.zip','a',zipfile.ZIP_DEFLATED) as z:
    if 'media_validation.json' not in z.namelist():z.write(out/'playable/media_validation.json','media_validation.json')
print('T24 hand-off docs updated; other models and older deliverables retained.')
