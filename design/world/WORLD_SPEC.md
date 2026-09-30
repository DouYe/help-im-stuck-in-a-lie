# The world — spec (palette locked · the rest PROPOSED, from keyframes v2)

## Palette (locked) — `palette.png`
| Name | Hex | Use |
|---|---|---|
| ink | `#0A0A0B` | background |
| ink2 | `#161618` | panels (status bar, dialog background on dark levels) |
| graphite | `#5E5B57` | far field, dim symbols, hatching |
| ash | `#9C978F` | secondary text, labels |
| bone | `#EEE9DF` | the girl, walls, main text (never pure white) |
| orange | `#FF5314` | the heart only (+ the lives in the HUD) |
Paper levels invert: bone background, ink symbols (KF2).

## Symbols — `symbols.png`
Everything is drawn from the stroke alphabet in `app/src/game/glyph.ts` (= `design/character/src/glyphs.py`),
one symbol per grid cell, round caps, stroke ≈ 0.13 × cell height for the girl, 1.3–3.2 px for the world.
Proposed roles: walls `|` `-` with `+` corners · ground `=` · ceiling `#` · bricks `[ ]` · spikes `^` `v` ·
bullets `o` `x` `+` · trails `.` `:` · code `0` `1` · pits `( )`. The legacy `*` (a drawn heart) is not used.

## Game furniture (proposed) — `ui_kit_proposed.png`
- **Top HUD** (`hud()` in `world.ts`): lives as orange symbol hearts + `x 03`, stage name centre
  (`STAGE 1-1 · THE KEYS`), song time and bar/beat right. `plate:` option puts dark plates behind it on busy frames.
- **Dialog box** (`dialog()`): a `symBox` frame with her small portrait; types the sung line word by word;
  the word being sung is inverted (bone block, ink text). Paper version on inverted levels.
- **Status bar** (3D levels, `kf_ray.ts`): HEART hearts + 100 % · REALITY meter of `|` bars · her bust in the
  middle, glancing left/right every 1.2 s · FLOOR number + stage · KEYS `[C] [L] [I] [C] [K]`.
- **Minimap** (top-down maze): the whole word-maze in dots, her position blinking as a tiny heart,
  "YOU ARE HERE · EXITS 0".
- **Words as geometry** (`brickWord`, `outlineWord`, 5×7 `pixfont.ts`): key-caps, bricks, outlined blocks,
  maze cells — the lyric is the level.
- **Hazards on the beat:** turrets `[o]` fire rings of `o` `x` `+` on every beat; row-slip glitch on beats in
  chaos levels; spikes; pits.

## Level types (proposed) — see `../keyframes/KEYFRAMES.md`
2D side platformer · paper (inverted) level · top-down maze whose cells spell a word, lit by her lamp ·
3D raycast corridor (old-shooter look, symbol walls) · chaos: the level types torn into slanted strips at once ·
(v3) boot/loading screen · app window with name tags · factory conveyor + giant mouse pointer · isometric
keyboard (2.5D, she in the 45° view) · a cell with bars made of letters · a tunnel of words rushing at the
camera · a falling shaft with spikes that spell a word · an extreme close-up.

## Her size and visibility (updated 2026-09-29, keyframes v3 — Hon: she was too hard to see)
- Bold strokes (0.32 × cell, min 2.4 px) and a knockout are built into `drawGirl` — don't draw extra outlines.
- ≈130–230 px wide in normal shots; 50–60 px only when a whole map is on screen, then add a **zoom callout**
  (a symbol box with her big inside, dotted leader line to her position — KF07); 270–330 px close; one
  extreme close-up ≈1040 px (KF13).
- Keep the world a notch dimmer or thinner than her: world strokes 1.3–2.6 px or bone at 55–80 % alpha, her
  strokes full bone. She should be the brightest, heaviest line in the frame (the orange heart aside).
