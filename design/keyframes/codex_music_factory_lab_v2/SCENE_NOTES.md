# Awakened AI factory — four static scene proposals (v2)

**Status:** for Hon's review. These are still-image scene studies, not selected keyframes, timed lyric shots, engine scenes, or an animation. `codex_music_factory_lab_v1/`, the earlier factory drafts in `wip/codex/music_factory_lab_v1/`, the seven selected Codex references in `codex_selected_references_v1/`, and other models' images remain in place. F01–F03 here are byte-identical copies of the v1 PNGs; F04 is the added perspective study.

## Story and visual direction

Hon's heroine is an awakened AI among visually identical AIs on a music-factory line. Only she has the orange symbol heart. She tries to escape, dies and returns to the beginning repeatedly, then eventually gets out. The primary camera language is a left-to-right 2D platformer; occasional depth views bring variety. Instrument enemies, music-note projectiles and readable lyric words connect combat to the song. Each still should be a clear, structured shot in a world visibly built from characters and code.

| Frame | Scene and camera | Readable action / later edit use |
|---|---|
| `F01_music_factory_identical_ai.png` | Orthographic 2D music lab, one continuous assembly line | Ten identical AI workers share prompt, beat, tune, voice, mix and export stations. The heroine alone has an orange heart. This can establish the factory and her awakening. |
| `F02_return_to_line_zero.png` | Front-on spawn room with memory cells | Death sends her to `SPAWN / 00`; faint cells preserve the trace of earlier attempts. `TRY // 019` is an illustrative graphic, not a decided plot count. |
| `F03_trumpet_lyric_attack.png` | Side-view platformer encounter | The girl must cross a legible gap. A trumpet made from code fires note glyphs; `LIE`, `HELP` and `STUCK IN A LIE` remain readable as hazards. `REAL` appears beyond it. |
| `F04_perspective_escape_corridor.png` | 2.5D code corridor, converging toward an exit | Five increasingly small, heartless AI bays repeat along the depth axis. The orange-heart heroine moves toward a clear `REAL` door. This offers a camera change while preserving the character-built world. `ATTEMPT 018` is illustrative. |

All four PNGs are 1920 × 1080. The only saturated orange is in the heroine's heart; ink, bone and greys carry the rest. The same original bold symbol-girl rig (`design/character/src/final_sheet.py`) is reused. A SHA-256 manifest accompanies the images.

The rapid death/respawn burst Hon described from [Kaizo Trap](https://www.youtube.com/watch?v=lIES3ii-IOg) is a **future animation/edit idea**. The 3–5-second duration, 10–20 deaths and one/two-frame changeover are his exploratory description, not fixed timing. No video was made. Exact placement on the song and which images to use await review.

Sources: `wip/codex/music_factory_lab_v1/` contains the v1 generator scripts and `package_factory_v2.py`; its `perspective_variant/build_perspective.py` generates F04. Grok's separately authored T19 runner was rejected; T20 clear shots were considered too plain; T21 denser mosaic stills are separately in review. This pack does not replace or alter any of them.
