# Awakened AI factory — three new static proposals

**Status:** new Codex scene studies for Hon to review. They are not selected references, final engine scenes, timed lyric shots, or animation. The previously accepted seven Codex images remain untouched in `../codex_selected_references_v1/`. The earlier varied-worker factory drafts remain in `../../../wip/codex/music_factory_lab_v1/` as process history; Hon asked to keep earlier pictures.

## Story direction received from Hon

One AI awakens on a music-factory assembly line among many **visually identical AIs**. She alone has the orange symbol heart. She tries to run left to right out of the factory, dies, returns to the beginning, and repeats until she gets out. The 2D platformer path may occasionally switch to a 3D view. Enemies may be instruments and their projectiles may be note glyphs or **readable** lyric words. A later animated edit may use an extremely fast 3–5-second burst of repeated deaths/respawns, as Hon described from [Kaizo Trap](https://www.youtube.com/watch?v=lIES3ii-IOg). The precise frame cadence, placement in Hon's song, and number of deaths are open.

## These new images

| Frame | Purpose | Specific visual mechanism |
|---|---|---|
| `F01_music_factory_identical_ai.png` | Factory origin / awakening | Ten figures share one continuous side-view belt. All use the approved symbol-girl rig; the main AI has the only orange heart. Prompt cards progress through beat, tune, voice, mix, and song stations. Glyphs form the belt, architecture and tonal shading. |
| `F02_return_to_line_zero.png` | Death resets the story | A larger spawn chamber brings the heroine back to the line. Grey memory cells show earlier failed runs, while the same idle AIs continue working. `TRY // 019` is an illustrative counter, not a decided plot count. |
| `F03_trumpet_lyric_attack.png` | First escape obstacle | A flat 2D gap forces a jump. A code-built trumpet faces the heroine and fires glyph music notes. Separate high-contrast `LIE`, `HELP`, and `STUCK IN A LIE` projectiles remain readable. The door marked `REAL` is visible beyond the instrument. |

All three are 1920 × 1080 stills. Ink, bone and greys are used throughout; orange appears only in the heroine's symbol heart. The original 17 × 27 bold girl is drawn by `design/character/src/final_sheet.py`, unchanged. Reproducible source is in `../../../wip/codex/music_factory_lab_v1/` (`build_factory_clones.py`, `build_respawn.py`, `build_brass_boss.py`, shared `build_factory.py`). `manifest.json` contains hashes of the delivered PNGs.

**How this relates to other work:** Grok Bot's `wip/new-bot/platform_run_v1/` tested a 16-frame continuous side-scroll, but Hon subsequently rejected it as messy and asked for one **clear, structurally legible scene per still**. Grok's later `wip/new-bot/clear_shots_v1/` is separately awaiting review. These three Codex pictures concentrate on the identical-AI factory premise, a readable reset room, and a larger brass encounter; they do not overwrite either Grok set. Other camera styles, including 3D, remain available for later still proposals. Do not turn this pack into a still-image video; Hon said to animate later.
