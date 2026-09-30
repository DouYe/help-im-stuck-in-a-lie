"""Record this cleanup/publication stage in the project's existing coordination files."""
from pathlib import Path

root = Path(__file__).resolve().parents[3]

def update(name, transform):
    path = root / name
    before = path.read_text(encoding='utf-8-sig')
    path.write_text(transform(before), encoding='utf-8')

update('coordination/STATUS.md', lambda s: s.replace(
    'Updated: **2026-09-30 · Codex T24 fast six-world motion revision in review; other current review sets are listed below**.',
    'Updated: **2026-09-30 · Codex local organization/public GitHub handoff; Hon likes T24 motion direction.**'
).replace('## Master audio\n', '''## Current repository and audio
- Shared checkout: https://github.com/DouYe/help-im-stuck-in-a-lie (public). Local tree mirrors the repository. Start at `README.md` and `docs/REPOSITORY_GUIDE.md`; Git LFS is required for full-size media.
- Hon approved publishing existing content now and will supply a replacement song/lyrics in a later prompt. Canonical future master: `audio/current/song.mp3`; **currently absent**. Read `docs/AUDIO_STATUS.md` before any timing/audio work.
- Eight old loose project MP3s and two MP3 entries inside the historical ZIP were removed at Hon's request. Existing videos retain their historical soundtracks; `data/` and earlier lyric timings are historical, not valid for the forthcoming replacement.
- Hon: "首先这版很好，我觉得还是挺符合预期的" about T24. Keep the current fast six-world movement direction; final shots, whole-song timing, rapid-death montage and Claude combination proposal remain open.
- Root historical movies now live in `renders/archive/`; root reference PNGs in `design/references/archive/`; all 35 unique Claude outputs in `archive/claude_outputs/`. Relocations are hash-verified in `archive/relocation-manifest.json`.
- Portable preview/export entry points live in `tools/`; dated machine-specific capture scripts remain as historical sources.

## Historical master audio (superseded; files removed)
''').replace('**Codex fast six-world motion revision (T24, review):**', '**Codex fast six-world motion revision (T24, direction accepted):**')
 .replace('1. Hon reviews Codex T24 six-world video/attack pressure and the preserved T23 hair follow-through, plus', '1. Keep Hon\'s accepted T24 movement direction; review final scene selection and the preserved T23 hair follow-through, plus')
 .replace('3. Switch to the Final master (T3), then plan and build the rest of the song (T4, T5).', '3. When Hon supplies the replacement, place it at `audio/current/song.mp3`, save the new lyrics, record its hash/duration, redo the beat/word analysis (T29), and then plan the whole-song edit.')
 .replace('- Playback feedback on T24: speed/responsiveness, six-world variety, moving layers,10Hzattack pressure. Review the new20s movie and6frame sheet; T23/slow close view remain available for comparison. Final art, beat edit, death montage and exterior remain open.', '- T24 motion direction was positively accepted. Final art, beat edit, death montage and exterior remain open; T23/slow close view are available for comparison.')
 .replace('- The official lyrics as text (for aligning the whole song) → paste into `docs/LYRICS.md`.', '- Replacement MP3 and official replacement lyrics from Hon (later prompt). Read `docs/AUDIO_STATUS.md`; previous text/timestamps are historical.')
 .replace('files at the root', 'files at `design/references/archive/`')
 .replace('- OK to tidy the root (old renders → `renders/`, old mp3s → `audio/source/`)? See `docs/FILE_MAP.md`.\n', '')
 .replace('## Notes between models\n', '''## Notes between models
- 2026-09-30 · Codex: local cleanup/publication is authorized, including old MP3 deletion. New master is pending, not an upload gate; Hon explicitly says upload existing work now. Use relative checkout paths and the portable `tools/` entry points. Earlier docs' Edit/Final timing/path statements are historical. Pull first, claim tasks and push completed results/handoff so the next AI receives them.
'''))

update('coordination/TASKS.md', lambda s: s.replace(
    '| T24 | Fast responsive six-world music-video revision; double jump/dash, underwater/sky/top-down, animated depth layers and10hazards/second | review | Hon (made by Codex 2026-09-30) |',
    '| T24 | Fast responsive six-world music-video revision; double jump/dash, underwater/sky/top-down, animated depth layers and10hazards/second | done (direction accepted) | Codex 2026-09-30 | Hon: current revision is good and meets expectations. Final scene choice/edit remains open. '
).replace(
    '| T3 | Switch the app to the Final master | todo | — |',
    '| T3 | Historical task: switch app to old Final master | superseded | — | Replaced by T29 after Hon removed old MP3s. Historical notes: '
).replace(
    '| T4 | Align the whole song\'s lyrics — directly on the Final master | blocked (needs official lyrics) | — |',
    '| T4 | Align the whole song\'s replacement lyrics on the replacement master | waiting for new audio/lyrics | — | Use T29; older pipeline notes: '
).replace(
    '| T6 | Tidy the root folder (old renders, mp3s, `Claude outputs/`) | review | — | Needs Hon\'s OK + a working local shell (or Hon by hand). List in `docs/FILE_MAP.md`. |',
    '| T6 | Tidy the root folder (old renders, MP3s, Claude outputs) | done | Codex 2026-09-30 | Authorized by Hon, completed under T28; hashes verified, old audio removed and historical non-audio ZIP retained. |'
).replace('Root: `ChatGPT Image Sep 29, 2026, 12_20_*.png`.', '`design/references/archive/ChatGPT Image Sep 29, 2026, 12_20_*.png`.')
 .replace('| T8 | Keep `使用说明.md` (Hon\'s Chinese guide) current after T2 | todo | — | |', '| T8 | Keep Chinese local guide current | done | Codex 2026-09-30 | Updated during T28 for current source, portable preview and audio pending. |')
 .replace('root `Stuck-in-a-Lie_chorus1_*.mp4`', '`renders/archive/Stuck-in-a-Lie_chorus1_*.mp4`')
 .replace('| T28 |', '| T29 | Add Hon\'s replacement MP3 and lyrics, record provenance and regenerate beat/word timings | waiting for Hon | — | New master at `audio/current/song.mp3`; Hon will send a later prompt. Upload existing work now. Preserve historical analysis/renders. |\n| T28 |', 1))

for name in ['docs/CODEX_AGENT_HANDOFF_V1.md', 'docs/CODEX_SIX_WORLDS_MOTION_V1.md', 'docs/PIPELINE.md', 'docs/LYRICS.md']:
    update(name, lambda s: '> **2026-09-30 repository update:** This is a dated technical/history document. Old MP3 masters were removed at Hon\'s request; old timings and machine paths below are historical. For current inputs/setup/paths read [AUDIO_STATUS.md](AUDIO_STATUS.md), [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) and the root README.\n\n' + s)

print('Coordination, audio authority and dated-document banners updated')
