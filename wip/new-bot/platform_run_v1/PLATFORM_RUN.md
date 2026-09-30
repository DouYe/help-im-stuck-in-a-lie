# PLATFORM RUN v1 - continuous L->R side-scroll escape

**Theme:** one continuous Celeste-like platformer path escaping a factory-ish AI world.
Girl runs/jumps LEFT to RIGHT; E01-E16 are chronological camera windows
on the same scrolling stage (cam advances ~780 world units per frame).

**Story loop (Hon mid-run note; Celeste-like ref described only, no YouTube fetch):**
1. Respawn / wake at spawn beacon in factory-ish AI level
2. Run right through layered platforms
3. Die (cute symbol death VFX: glyph shatter, dash-skull, bone particles — not gore)
4. Empty platform after death → snap respawn flash
5. Try again deeper into the factory, still escaping
6. Die again → revive → push toward REAL exit

**Narrative combat (Hon add-on):** hazards are art, not generic braces.
- Lyric-word projectiles: HELP / LIE / AI / REAL / stuck / FAKE / alive ...
- Instrument enemies from symbols: TRUMPET (shoots lyrics), DRUM (shoots notes), KEYS
- Musical NOTES built from | - / \ o (no unicode dependency)

**Hon feedback answered (escape_levels_v1):**
- Liked directionally but not enough - needed denser / more loaded layers.
- Want PLATFORMER feel: character moving L->R; frames CONNECTED as continuous path.
- escape_v1 motifs too singular (few main props then empty). Need MORE LAYERS
  (foreground / midground / background / HUD crumbs) without scenes_50 chaos.

**Density:** denser than escape_levels_v1 (parallax + multi-layer platforms + HUD crumbs),
still structured and readable - not scenes_50 noise soup.

**Layers per frame:**
1. Far: faint code hills / distant pillars
2. Mid: terraces, soft brace rain (where staged), mid platforms
3. Play: ground + near ledges + stage motifs + instrument enemies + lyric/note projectiles
4. FG: sparse hanging braces / corner props
5. HUD crumbs: HP / STAGE / mini path ticks / tiny MAP
6. Girl: bold side-view run/jump/walk, clear knockout silhouette; orange only on heart

**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.
English. Symbols/strokes. No bloom/glow/gradients/other colours.

**Count:** 16 stills @ 1920x1080 + 3 sheets (sheet_01, sheet_02, sheet_path).

| ID | File | Stage | Beat | Pose | Girl X | Cam | Lyric |
|---|---|---|---|---|---|---|---|
| E01 | `E01_spawn-beacon.png` | spawn beacon | spawn | front | 320 | 0 | still alive |
| E02 | `E02_factory-run.png` | factory run | run | run | 358 | 780 | stuck in a lie |
| E03 | `E03_mid-air-jump.png` | mid-air jump | jump | jump | 436 | 1560 | help |
| E04 | `E04_hazard-brace.png` | hazard brace | run | run | 514 | 2340 | help |
| E05 | `E05_death-burst.png` | death burst | death | fall | 592 | 3120 | stuck in a lie |
| E06 | `E06_empty-after.png` | empty after | empty | front | 670 | 3900 | help |
| E07 | `E07_respawn-flash.png` | respawn flash | respawn | front | 360 | 4680 | still alive |
| E08 | `E08_deeper-factory.png` | deeper factory | factory | run | 700 | 5460 | they call me AI |
| E09 | `E09_syntax-climb.png` | syntax climb | jump | jump | 904 | 6240 | make me real |
| E10 | `E10_near-escape.png` | near escape | near | run | 900 | 7020 | real this time |
| E11 | `E11_REAL-peek.png` | REAL peek | near | walk | 1000 | 7800 | real this time |
| E12 | `E12_death-again.png` | death again | death | fall | 1138 | 8580 | stuck in a lie |
| E13 | `E13_revive-flash.png` | revive flash | respawn | front | 400 | 9360 | still alive |
| E14 | `E14_push-deeper.png` | push deeper | run | run | 1294 | 10140 | help |
| E15 | `E15_final-approach.png` | final approach | near | jump | 1400 | 10920 | real this time |
| E16 | `E16_exit-REAL.png` | exit REAL | push | run | 1320 | 11700 | still alive |

## Sheets

- `sheet_01.png`
- `sheet_02.png`
- `sheet_path.png`

## Generator

- `src/make_platform_run_v1.py` - reuses `design/character/src` (bold girl, symbol heart).
- Does **not** write into `design/keyframes/` or locked character assets.

## Palette audit

All frames: only ink / bone / orange(heart).

## Continuity notes

- Shared `ground_y(wx)` / hill functions so terrain reads as one path.
- Edge crumbs `<- E0n` / `E0n ->` reinforce chronological order.
- Girl screen-X advances ~78px per frame (280 -> ~1450) for L->R progress read.
- Occasional mid-layer motifs: maze alcove (E04), brace rain (E05/E13),
  syntax gate (E08), REAL door (E09/E16), heart pass (E12), memory shelves (E14).
