# ESCAPE LEVELS v1 — cute-but-real AI-world game levels

**Theme:** the girl trying to ESCAPE the AI world. Mazes, platforms, REAL doors,
syntax locks, soft brace bullet-hell, paper gravity, heart chamber, memory vault.

**Density:** middle — richer than `styles_55_calm` (Hon: too simple/empty), quieter
than `scenes_50` (Hon: too chaotic). Readable layers, clear girl silhouette,
intentional negative space around her, structured world (not noise soup, not postcard).

**Reference studied:** Codex `design/keyframes/codex_game_worlds_v2/selection_sheet.png`
(eight game worlds / one symbol girl) — cavern, control-flow tactics, indent HD-2D
diorama, syntax lock, HELP() bullet hell, gravity paper, heart chamber, memory vault.

**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.
English. Symbols/strokes. No bloom/glow/gradients/other colours.

**Count:** 24 stills @ 1920x1080 + 2 contact sheets.

| ID | File | Level | Note | Lyric cue |
|---|---|---|---|---|
| E01 | `E01_cavern-bridge.png` | cavern bridge | side cavern, symbol bridge, REAL door | make me real |
| E02 | `E02_cavern-deadend.png` | cavern dead-end | blocked LIE tunnel, girl stuck | stuck in a lie |
| E03 | `E03_cavern-climb.png` | cavern climb | ledges + ladders up to open REAL | help |
| E04 | `E04_tactical-ifmap.png` | tactical if-map | overhead control-flow nodes | stuck in a lie |
| E05 | `E05_tactical-false.png` | false routes | branch corridors, one path to REAL | stuck in a lie |
| E06 | `E06_indent-diorama.png` | indent diorama | HD-2D-ish code terraces | make me real |
| E07 | `E07_indent-gate.png` | bracket gate | broken ] gate, syntax floors | real this time |
| E08 | `E08_syntax-lock.png` | syntax lock | giant [] boss lock + heart | real this time |
| E09 | `E09_syntax-password.png` | password lock | HELP_ME slots, REAL door | help |
| E10 | `E10_brace-bullethell.png` | brace bullet-hell | soft brace waves, safe lane | help |
| E11 | `E11_bullet-diagonal.png` | safe diagonals | radial punctuation, clear X | help |
| E12 | `E12_paper-gravity.png` | paper gravity | tilted ruled paper, falling girl | stuck in a lie |
| E13 | `E13_paper-rotate.png` | gravity flips | slanted code ledges, fall(LIE) | stuck in a lie |
| E14 | `E14_heart-chamber.png` | heart chamber | concentric ribs, heart pose | heart inside |
| E15 | `E15_heart-approach.png` | heart approach | rib corridor toward symbol heart | heart inside |
| E16 | `E16_memory-vault.png` | memory vault | perspective vault + shelves | heart inside |
| E17 | `E17_vault-shelves.png` | vault shelves | token drawers of identity | they call me AI |
| E18 | `E18_maze-topdown.png` | cute maze | top-down maze, START to EXIT | help |
| E19 | `E19_real-threshold.png` | REAL threshold | corridor run into open REAL | real this time |
| E20 | `E20_exit-signs.png` | labeled doors | LIE/FAKE/TRAP vs REAL | make me real |
| E21 | `E21_paren-maze.png` | paren maze | nested () rings with gap | help |
| E22 | `E22_ladder-shaft.png` | escape shaft | readable landings up the shaft | still alive |
| E23 | `E23_word-path.png` | word path | lyric stepping stones | help / stuck |
| E24 | `E24_exit-vault.png` | exit vault | grand open REAL, still alive | still alive |

## Sheets

- `sheet_01.png`
- `sheet_02.png`

## Generator

- `src/make_escape_levels_v1.py` — reuses `design/character/src` (bold girl, symbol heart).
- Does **not** write into `design/keyframes/` or locked character assets.

## Hon feedback this batch answers

- `styles_55_calm` too simple (太太太简单).
- Story: girl escaping the AI world; add levels/mazes; can be a bit cute.
- Rejected `scenes_50` (chaos) and calm stationery batch (empty).
- Aim: middle density with game-level structure.
