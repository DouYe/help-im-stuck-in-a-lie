# MOSAIC DENSE v1 - denser mosaic glyph stills (NOT image-gen)

**Theme:** Same locked **pixel/character mosaic** as `clear_shots_v1`: every stroke is
ASCII glyphs stamped via Pillow + locked girl from `design/character/src`
(`final_sheet.render`, `glyphs`). **NOT** GenerateImage / illustration.

**Hon feedback this batch answers:**
- Rejected **GenerateImage yt_ref_shots** — style left the locked mosaic look (became illustration).
- `clear_shots_v1` too plain — need denser YouTube-platformer still composition.
- Keep mosaic glyph pipeline. Increase density: stacked platforms, soft glyph rain,
  spikes, musical note glyphs, lyric text projectiles, factory depth.
- Still **ONE clear readable scene per frame** (not chaos / scenes_50, not continuous runner / platform_run).

**Composition:**
- Girl small-to-medium but readable (clear_shots sizes OK); world denser around her.
- Layers: soft glyph rain / distant factory silhouettes (BG); sharp platforms + hazards (MG);
  optional framing spikes/pipes (FG edges).
- Choreographed density: clear negative-space path so the eye finds the girl.
- Shot flavors across the 8: precipice leap, spike/gear gauntlet, freefall between walls,
  death stains as soft glyphs, lyric/note swarm, looming factory, REAL door crossroads,
  ascent out of dense hazards.

**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.
English. Symbols/strokes. No bloom/glow/gradients/other colours.

**Count:** exactly 8 stills @ 1920x1080 + 1 contact sheet.

| ID | File | Scene | Dense flavor | Lyric cue | Pose |
|---|---|---|---|---|---|
| MD01 | `MD01_boot-spawn-room.png` | boot / spawn room | looming factory silhouettes + server racks + edge spikes | LOADING GIRL.EXE | front |
| MD02 | `MD02_name-tag-chamber.png` | name-tag chamber | lyric/name-tag projectile swarm + note glyphs | they call me AI | front |
| MD03 | `MD03_factory-conveyor.png` | factory conveyor | gears + stacked belts + lyric scraps + pipe frame | feed me a prompt | q_front |
| MD04 | `MD04_platform-beat.png` | precipice CLICK leap | stacked platforms + floor spike gauntlet + mid-air jump | keys go click clack | jump |
| MD05 | `MD05_help-bricks.png` | HELP bricks ascent | climb platforms out of dense floor spikes onto HELP | Help, I'm stuck in a lie | help |
| MD06 | `MD06_lie-maze-above.png` | LIE maze freefall | denser L/I/E walls + freefall shaft between I walls | stuck in a lie | front above |
| MD07 | `MD07_real-door-corridor.png` | REAL door crossroads | side LIE/AI false doors + note/lyric swarm | make me real this time | back |
| MD08 | `MD08_heart-chamber-close.png` | heart chamber ascent | outer hazard ring + concentric ribs + orange heart | heart inside | heart |

## Sheets

- `sheet_01.png` (4x2 contact)

## Generator

- `src/make_mosaic_dense_v1.py` — reuses `design/character/src` (bold girl, symbol heart).
- Does **not** write into `design/keyframes/` or locked character assets.
- Same Shot/polyline/platform/put/girl pipeline as `clear_shots_v1`.

## Palette audit

All MD01-MD08 + sheet: only ink / bone / orange(heart). MD07 is back-view (rig has no heart, so no orange) — intentional.

## Rejected directions (do not iterate)

- GenerateImage / yt_ref_shots illustration path — left mosaic look
- `wip/new-bot/scenes_50/` — chaos
- `wip/new-bot/styles_55_calm/` — empty
- `wip/new-bot/platform_run_v1/` — messy continuous runner
- `wip/new-bot/clear_shots_v1/` — too plain (kept as archive reference; this pack densifies it)
