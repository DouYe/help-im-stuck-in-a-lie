# Scenes v1 — superseded (kept for its tools)

On 2026-09-30, around 00:10, Hon asked for about fifty scenes, plus B-roll (code close-ups without the girl),
close-ups like his reference image, and complex mathematical figures. Claude planned 68 frames (`src/plan.py`) and
started them with parallel helpers, which were cut off by a usage limit. Later that day Hon said fifty was too many
and asked for about ten keyframes that follow the story instead. Those are in **`design/keyframes/story_v1/`**.

What is kept here:
- `src/kit.py` — shared drawing helpers (girl placement, glyph curves, perspective warp, depth of field, grain,
  code plates, palette check).
- `src/closeup.py` — the close-up renderer. It draws the same rig on a finer symbol grid, with hair strands, data
  streams and a hatched heart. `story_v1` uses it.
- Three reviewed frames: `A10_polygraph_sounds-real.png`, `B01_bios-boot_intro.png`,
  `C05_closeup-heart_heart-inside.png`.

The helpers' unfinished, unreviewed frames were not copied into the project folder.
