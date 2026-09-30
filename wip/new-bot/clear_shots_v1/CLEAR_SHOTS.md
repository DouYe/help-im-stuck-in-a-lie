# CLEAR SHOTS v1 - original keyframe rhythm, readable structures

**Theme:** ONE clear framed scene per still. Strong STRUCTURE / composition.
Forms readable at a glance (room, door, maze, platform, factory) + cute girl
escaping the AI world.

**Hon feedback this batch answers:**
- Rejected `platform_run_v1` - too messy; not a long real platformer strip.
- Want ORIGINAL keyframe rhythm (like Claude KF moments), not continuous runner.
- Old Claude keyframes: structures often unreadable (can't tell what things are).
- Need readable forms at a glance.
- Not chaos (`scenes_50`), not empty (`styles_55_calm`), not continuous runner.

**Density:** sparse intentional FG / MG / BG. Clear silhouette. Negative space
around the girl. Objects must read as objects.

**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.
English. Symbols/strokes. No bloom/glow/gradients/other colours.

**Count:** exactly 8 stills @ 1920x1080 + 1 contact sheet.

| ID | File | Scene | Readable form | Lyric cue | Pose |
|---|---|---|---|---|---|
| CS01 | `CS01_boot-spawn-room.png` | boot / spawn room | room + BOOT LOG panel + EXIT door + SPAWN pad | LOADING GIRL.EXE | front |
| CS02 | `CS02_name-tag-chamber.png` | name-tag chamber | windowed chamber + name tags on dotted lines | they call me AI | front |
| CS03 | `CS03_factory-conveyor.png` | factory conveyor | PROMPT hopper + conveyor + product boxes + cursor | feed me a prompt | q_front |
| CS04 | `CS04_platform-beat.png` | one platform beat | 5 keycap platforms spelling CLICK (NOT long run) | keys go click clack | jump |
| CS05 | `CS05_help-bricks.png` | HELP paper bricks | giant brick letters H-E-L-P, girl on P | Help, I'm stuck in a lie | help |
| CS06 | `CS06_lie-maze-above.png` | LIE maze from above | top-down maze walls forming L / I / E + callout | stuck in a lie | front above |
| CS07 | `CS07_real-door-corridor.png` | REAL door corridor | perspective corridor ending in clear REAL door | make me real this time | back |
| CS08 | `CS08_heart-chamber-close.png` | heart chamber close | concentric ribs + girl holding orange heart | heart inside | heart |

## Sheets

- `sheet_01.png` (4x2 contact)

## Generator

- `src/make_clear_shots_v1.py` - reuses `design/character/src` (bold girl, symbol heart).
- Does **not** write into `design/keyframes/` or locked character assets.

## Palette audit

All CS01-CS08 + sheet: only ink / bone / orange(heart). CS07 is back-view (rig has no heart, so no orange) - intentional.

## Rejected directions (do not iterate)

- `wip/new-bot/scenes_50/` - chaos
- `wip/new-bot/styles_55_calm/` - empty
- `wip/new-bot/platform_run_v1/` - messy continuous runner