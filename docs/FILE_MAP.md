# FILE MAP — what the project files are

Updated: **2026-09-30**. Paths are relative to the repository/project root. **Current** means an active entry/source; **reference** means retained for inspection; **proposal** means not selected final footage; **old/rejected** means preserve the record without reviving it as the current direction.

The local directory and GitHub use the same relative paths. Historical logs/manifests may still name former root files or `Claude outputs/`; resolve them through [archive/relocation-manifest.json](../archive/relocation-manifest.json). Current audio state is [AUDIO_STATUS](AUDIO_STATUS.md); old timing files are not aligned to the forthcoming master.

## Root and coordination

| Path | What | State |
|---|---|---|
| `README.md` · `AGENTS.md` · `CLAUDE.md` · `GEMINI.md` | Human/AI entry points and working protocol | Current |
| `使用说明.md` | Hon's current guide in Chinese | Current |
| `HOW-IT-WORKS.md` | Pointer to the earlier engine pipeline | Current pointer; pipeline audio references are historical |
| `LICENSE.pdoom-engine` | Upstream adapted engine's MIT licence | Applies to its code; no new original-media licence |
| `package.json` · `package-lock.json` | Root portable Node commands and pinned capture dependency | Current |
| `requirements.txt` | Python/Pillow still-generator dependency declaration | Current; old audio analysis needs additional libraries |
| `.gitignore` · `.gitattributes` | Local infrastructure exclusions and media LFS tracking | Current |
| `coordination/STATUS.md` | Now, next, waiting and notes between models | Current |
| `coordination/TASKS.md` | Task board and owners | Current |
| `coordination/WORKLOG.md` | Sessions, newest first | Current/history |

## docs/

| File | What |
|---|---|
| `REPOSITORY_GUIDE.md` | Clone with full LFS media, portable preview/capture, paths, collaboration and push workflow |
| `AUDIO_STATUS.md` | New master pending; eight retired MP3 removals and stale timing provenance |
| `CODEX_AGENT_HANDOFF_V1.md` | Dated Chinese technical handoff: motion modules, controls, audit results and pending Claude integration; old audio/ports now superseded |
| `CODEX_SIX_WORLDS_MOTION_V1.md` | T24 six-world motion implementation and validation record |
| `CODEX_PLATFORMER_MOTION_V1.md` | T23 earlier single-factory motion and hair test |
| `PROJECT_BRIEF.md` | Story, world, look and whole-song draft |
| `PROMPTS.md` | Hon's instructions verbatim, translations and reusable prompts |
| `DECISIONS.md` | Locked decisions, direction, selected references, pending choices and rejected approaches |
| `PIPELINE.md` | Earlier TypeScript engine, analysis and lyric alignment instructions; inspect old paths/master settings before reuse |
| `LYRICS.md` | Historical master mapping and lyrics/timing records; await replacement lyrics |
| `FILE_MAP.md` | This index |

## design/

| Path | What | State |
|---|---|---|
| `STYLE_BIBLE.md` | Index of styles and packs | Current |
| `character/GIRL_SPEC.md` · `GIRL_style1_final.png` | Character rules and turnaround/walk/action/overhead sheet | Character style locked; HELP-pose tweak pending |
| `character/src/` | `vgirl.py`, `glyphs.py`, `final_sheet.py` and rig/sheet sources | Current shared character; mirrors app rig |
| `character/explorations/` | Design rounds leading to style 1/Q1 | Reference |
| `character/archive/` | Approved v1 sheet and intermediate thin HELP treatment | Reference/history |
| `world/palette.png` · `symbols.png` | Palette and world vocabulary | Palette locked; vocabulary proposed |
| `world/ui_kit_proposed.png` · `WORLD_SPEC.md` · `src/` | UI and worlds-as-symbol-geometry specifications/source | Proposal |
| `references/` | Hon's saved close-up and T23 prototype references | Reference |
| `references/archive/ChatGPT Image Sep 29, 2026, 12_20_22 PM.png` and `…12_20_50 PM.png` | Two former root portraits; preserved originals, role not confirmed | Reference, not final style |
| `keyframes/codex_six_worlds_motion_v1/` | Six actual simulation frames, overview and hashes | Current review pack; motion direction accepted, final shots open |
| `keyframes/codex_selected_references_v1/` | Seven full-size selected Codex frames 02–06, 07B, 08, selected-only sheet and manifest | Hon selected as references, not final scenes |
| `keyframes/codex_music_factory_lab_v2/` | Four factory/respawn/trumpet/perspective-exit static proposals, notes and manifest | Proposal |
| `keyframes/codex_music_factory_lab_v1/` | Earlier three-frame factory pack | Historical proposal; retained |
| `keyframes/codex_candidates_v1/` | Five early scene/camera alternatives, sheet, notes and generators | Proposal |
| `keyframes/codex_game_worlds_v2/` | Original mixed candidate set including rejected 01/painted 07 and accepted code 07B | History; use selected-only set for approved references |
| `keyframes/story_v1/` | Claude K01–K10/story sheet/notes/source: close, game and computed plate joined by heart | Proposal, T26; not yet implemented in motion engine |
| `keyframes/styles_v1/` | Claude eight media, S1–S8/style sheet/spec/source | Hon said all good; final usage and orange field colours open |
| `keyframes/v3/` | Claude 13 bold-girl moments, overview, variants and notes | Awaiting selection |
| `keyframes/KF1…KF5_*.png`, root `keyframes_sheet.jpg` and `KEYFRAMES.md` | Claude v2 thin-girl frames | Old; unchanged |
| `keyframes/v1/` | First pass | Old |
| `keyframes/scenes_v1/` | Superseded broad scene attempt with reusable drawing/close-up kit and three frames | Tools used by story_v1; frames reference |
| `keyframes/src/` | Captured-still naming and contact-sheet generator | Source |

## Motion sources, tools and renders

| Path | What | State |
|---|---|---|
| `wip/codex/platformer_motion_v2/` | Latest six-world Canvas source: physics/controller, character, side/water worlds, topdown, original capture and QA records | Current movement source; new work should derive a new version |
| `tools/serve-motion.mjs` | Portable dependency-free Node preview, canonical audio mapping | Current entry point |
| `tools/capture-motion.mjs` · `motion-common.mjs` | Portable audit/capture helpers, browser/FFmpeg discovery, protected output paths | Current entry point |
| `tools/README.md` · `verification.json` | Commands, dependencies, font/OS limits and local verification | Current |
| `renders/2026-09-30_codex_six_worlds_motion_v1.mp4` | T24 20-second 1080p60 six-world preview, 200 attacks; retired Final 42.012–62.012 s | Hon says fits expectations; final song/edit open |
| `wip/codex/platformer_motion_v1/` | Earlier one-factory playable source, captured process versions and QA | Old motion reference |
| `renders/2026-09-30_codex_platformer_motion_v2.mp4` | T23 movie, despite filename belongs to **source v1**; one death/reset | Old motion reference |
| `renders/2026-09-30_codex_platformer_hair_slow_v1.mp4` | Four-second silent half-speed hair/drop review | Motion reference |
| `renders/2026-09-30_codex_game_worlds_motion_board_v1.mp4` | Earlier 21.833-second still-image preview of mixed candidates | Historical board; not the current moving engine |
| `renders/archive/Help-Im-stuck-in-a-LIE_first15s.mp4` | Former root first engine test | Old |
| `renders/archive/Stuck-in-a-Lie_chorus1_heroine.mp4` | Former root symbol-heroine chorus cut | Old |
| `renders/archive/Stuck-in-a-Lie_chorus1_chaos.mp4` | Former root chaotic no-figure/red cut | Old/rejected palette |
| `renders/archive/Stuck-in-a-Lie_chorus1_seven.mp4` | Former root seven-art-style cut | Old/rejected R2 |

Videos retain their embedded old soundtrack. Existing movies are not overwritten when the new song arrives. WIP copies of delivered media may intentionally duplicate curated renders/frames; their pack context and source relationships are retained.

## Earlier engine and historical audio data

| Path | What | State |
|---|---|---|
| `app/` | Original Bun/TypeScript/three.js scene/timeline/video engine | Preserved source; see PIPELINE for scene map |
| `app/public/fonts/` | Authored font assets and any included font licences | Reference/runtime assets |
| `analysis/` | Beat/section analysis, former master comparison and plots | Historical source/results; some paths/master assumptions need adaptation |
| `analysis/align/` | Vocal separation, CTC/refinement/word-timing sources and results | Historical source/results |
| `data/audio.json`, `audio.edit.json`, `audio.real.json` | Former master beat/envelope/onset analyses | Historical, pending new-master replacement |
| `data/lyrics.json`, `lyrics.template_old.json` | Forced-aligned former chorus words and superseded estimated template | Historical; new lyrics require alignment |
| `audio/current/song.mp3` | Canonical incoming replacement master location | **Pending; file not supplied** |
| `audio/edit/`, `audio/final/`, `audio/real/` | Former master destinations | Retired; do not restore superseded MP3s for new production |

## Preserved explorations and cleanup evidence

| Path | What | State |
|---|---|---|
| `wip/new-bot/mosaic_lyrics_50/` | 50 glyph-mosaic lyric/story frames, sheets, notes and source | Review proposal, T22; lyric draft does not approve new master text |
| `wip/new-bot/mosaic_dense_v1/` | Eight denser framed code-world compositions | Review proposal, T21 |
| `wip/new-bot/escape_levels_v1/` | 24 escape-level frames | Review proposal, T16 |
| `wip/new-bot/styles_trial/` | Four additional media: blueprint, chalk, woodcut, LED | Review proposal, T13 |
| `wip/new-bot/clear_shots_v1/` | Eight readable framed structures | Historical reference; Hon found too plain |
| `wip/new-bot/platform_run_v1/` | Continuous platform strip | Rejected as messy; retained |
| `wip/new-bot/scenes_50/` | Dense 50-scene attempt | Rejected as noisy; retained |
| `wip/new-bot/styles_55_calm/` | 55 calm style stills | Rejected as too empty; retained |
| `wip/codex/` other folders | Generators, audits, selection packaging and prior factory/art alternatives | Source/history; inspect each folder's notes |
| `wip/codex/repository_cleanup_v1/` | Inventories, layout audit, old-MP3 snapshot and cleanup verification | Cleanup evidence; final deletion result is authoritative |
| `archive/claude_outputs/` | 35 earlier Claude character rounds/style previews and deliveries | Unique historical collection; audit found **no byte-identical copies** in the current design packs |
| `archive/codex_early_outputs/` | Earlier Assembly Line Heart/Codex deliverables recovered from the chat workspace: movies, stills, timing notes and source | Historical original-project work; not the current song/edit; obsolete standalone audio excluded |
| `archive/lie-video-project_without_audio.zip` | Earlier project snapshot with 127 non-MP3 entries; two retired MP3 entries removed | Historical snapshot; nonaudio contents verified, includes unique/older source |
| `archive/relocation-manifest.json` | Old→new path mapping and integrity records for cleanup moves | Current path/provenance index |

No retained artwork was discarded as a duplicate. All eight snapshotted loose project MP3s were removed, and old audio-bearing archives were replaced with audio-free historical copies, under Hon's explicit cleanup request. Original-project earlier deliveries are preserved; the upstream reference video's media remains an external reference, linked through source/provenance rather than republished as Hon's work.
