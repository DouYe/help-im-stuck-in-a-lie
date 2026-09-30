# Styles Trial (Grok Bot New Bot) - four NEW media stills

Hon (2026-09-30) to Grok Bot: *"请看看这个project。然后我可能需要你生成一些关键帧，就是各种不同风格的，你先试一试。"* — look at the project; try generating keyframes in various different styles first.

This folder is a **WIP trial** under `wip/new-bot/styles_trial/`. It does **not** overwrite locked `design/keyframes/styles_v1/` (S1-S8) or `design/keyframes/v3/`.

Same locked girl: bold style-1 rig (`design/character/src/final_sheet.py` / `vgirl.py`), knockout, orange symbol heart only. Palette: ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314`. English only. Everything built from symbols/strokes. No bloom / glow / gradients / other colours.

Overview: `styles_trial_sheet.jpg`. Full frames (1920x1080):

| # | File | Medium | Lyric moment | Notes |
|---|---|---|---|---|
| N1 | `N1_blueprint_make-me-real.png` | **blueprint** - bone construction lines on ink (cyanotype feel without cyan) | "Make me real this time" | Grid + dimension callouts (17 COLS / 27 ROWS), title block, orange **APPROVED** stamp. |
| N2 | `N2_chalk-blackboard_help.png` | **chalk on blackboard** - bone chalk dust + strokes | "Help, I'm stuck in a lie" | HELP pose, chalk notes, eraser dust as `.` glyphs, orange heart only. |
| N3 | `N3_woodcut_heart-inside.png` | **linoleum / woodcut** - heavy carved strokes on bone paper | "Heart inside" | Carved border of `/ \ x #`, registration marks, thicker stroke (`lw=0.42`), stuck pose. |
| N4 | `N4_led-matrix_real-this-time.png` | **LED / matrix panel** - glyph LED modules | "Real this time" | Module grid, status strip (PWR/SYNC/HEART OK, TRUTH ERR), REAL in `#` blocks. |

Generator: `src/make_styles_trial.py` (Python + Pillow, imports the girl from `design/character/src/`):

```
python wip/new-bot/styles_trial/src/make_styles_trial.py
```

Distinct from styles_v1 S1-S8 (amber terminal, receipt, orange screenprint, spec sheet, ASCII shading, comic, cross-stitch, engraving). Waiting for Hon's review — keep / drop / iterate.

Questions for Hon:
1. Which of N1-N4 (if any) to promote alongside or instead of S1-S8?
2. Want more media next (topographic contour maze, rubber-stamp collage, …)?