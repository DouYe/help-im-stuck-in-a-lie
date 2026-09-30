# The girl — character spec (style 1, final)

Reference sheet: `GIRL_style1_final.png`.
Explorations that led here: `explorations/` (01 → 05).

## Look
- **One clean, unbroken line of symbols.** Every "pixel" of her is one symbol on a grid; consecutive symbols
  touch, so it reads as a single clean line — not dashed, not broken, not filled.
- **Grid:** 17 columns × 27 rows for a full figure (1 : 1.6 box). Keep this grid for every pose, so she never
  changes resolution.
- **Symbols:** `|` vertical, `-` horizontal (centre), `_` low, `` ` `` high, `/` `\` diagonals, `+` only where
  two lines cross, `>` the nose in a turned view. **Stroke: BOLD — 0.32 × cell height, never under 2.4 px**
  (was 0.13; changed 2026-09-29 because she was too hard to see), round caps.
- **Knockout:** before her symbols are drawn, her silhouette (row by row, leftmost to rightmost symbol, a little
  larger) is filled with the background colour, so nothing behind her shows through her lines. Paper levels
  use the paper colour; ghosts / after-images have no knockout (`drawGirl(..., { knock })`).
- **Colour:** bone (#EEE9DF) on ink (#0A0A0B). The heart is the only orange (#FF5314).
- **Hair and body are separate shapes.** The hair is a long curtain with an outer line and an inner line that
  frames the face and falls outside the shoulders to the waist. The dress has its own outline (shoulders,
  waist, flared skirt). Legs are two lines, feet a short `_`.
- **Face:** the face is a window in the hair. Two closed eyes (`-` `-`), nothing else. The eyes are always drawn
  **last, on top of every other line**, one symbol each, so no other line can swallow them.
- **Heart:** also made of symbols, 4 × 3 small cells at the chest:
  ```
  /\/\
  \  /
   \/
  ```
  Orange. Holding it ("heart" pose) it is drawn 1.35× bigger.

## Angles and poses (all on the sheet)
- 8 directions: front · 45° front (Q1) · side · 45° back · back · and the mirrors.
  - **45° (Q1):** the face window shifts toward the turn, the far hair is a thin strip, both eyes stay visible
    (near eye a little wider), one `>` for the nose on the far cheek.
- Walking in 4 directions (+45°), two steps each — for the top-down maze.
- Platformer (side): walk ×4, jump, fall (hair and arms up), stuck (pressed to a wall), HELP (front view, arms
  raised like `\o/` **in front of** the hair, eyes one `o` each), holding the heart.
- From above (45° down) — for the 3D maze: the body shortens under the head, the parting shows.

## Size in the game
Updated 2026-09-29 (keyframes v3): **≈130–230 px wide in normal shots** on a 1920 × 1080 frame, 50–60 px only
when a whole map is on screen (and then with a zoom callout), 270–330 px for close shots, one extreme
close-up ≈1040 px. (Before: 40–80 px — too small, Hon: "几乎都看不太到".) Pending Hon's review.

## How she is built (for animation)
She is a vector rig (`src/vgirl.py`: polylines per part — hair_out, hair_in, strands, face, eyes, nose, neck,
body, arms, legs, over + the heart position), rasterized every frame into the symbol grid (`raster`: each cell a
stroke passes through takes the symbol matching the stroke's direction). Part `over` is rasterized separately
and drawn on top of the other lines (used for arms that pass in front of the hair). An eye given as a single
point becomes one `o`; a short horizontal eye becomes one `-`. Animate the rig (legs, hair, turn
0 → 45° via `turn(f)`) and the symbols re-choose themselves. `src/final_sheet.py` renders the sheet.
The same rig is ported to the video engine in `app/src/game/girl.ts`. Known difference (task T9): in the engine
the front-facing poses (front, frontwalk, heart, help) are built with `turn(0)`, while the sheet's front view is
the hand-written front in `vgirl.py` — a few cells of hair/feet differ. Make them identical before final renders.
Legacy, don't use: `app/src/game/sprite.ts` + `girl.txt` + `girl_frames.ts` + `gen_frames.py` (the first
hand-typed ASCII sprite, only used by the old `plat` scene).

## Changelog
- 2026-09-29 — v1: style 1 + Q1 + symbol heart approved by Hon ("Q1, I think is best").
- 2026-09-29 — v1.2: **bold** (stroke 0.32 × cell, min 2.4 px) + knockout, heart cells a little bigger
  (0.72 × 0.58 cell); sheet regenerated; the thin v1.1 sheet is `archive/GIRL_style1_final_v1.1_thin.png`.
- 2026-09-29 — v1.1: HELP pose refined — the eyes were rings covering 2×3 cells ("88" look) and the raised arms
  disappeared into the hair. Now: one `o` per eye; arms (part `over`) drawn on top of the hair. Sheet
  regenerated; nothing else changed. The v1 sheet is kept as `archive/GIRL_style1_final_v1.png`.
  (Pending Hon's OK — `docs/DECISIONS.md` P2.)
