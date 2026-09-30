# Symbol girl motion module v2

This file is an isolated motion study derived from v1 `character.js`. The locked `vgirl.py`, `girl.ts`, and glyph modules are unchanged. It retains the original 17×27 raster, continuous symbol outlines, separate long hair/dress, closed eye dash, and the orange symbol heart. Only the heart uses orange.

## API

`PlatformerCharacter.draw(ctx, state, timeSeconds)` uses the existing foot anchor: `state.x`, `state.y`, and `width` (116 default). Existing fields continue to work: `vx`, `vy`, `facing` ±1, `grounded`, `duck`, `landing`, `runPhase`, `hair`, `opacity`, `bone`, `knock`, `noHeart`, `heartColor`.

New side-view fields:

- `dashing`: 0..1, or `true` for full pose. Turns the intact glyph girl horizontal, reaches hands ahead, and tucks the feet. A small hair component is attenuated while turning so the curtain trails behind rather than flying vertically from the world-axis lag.
- `swim`: boolean. Alternating arm strokes, gentle leg kicks, small torso tilt; water reduces hair spring force and damping.
- `moveY`: optional normalized up/down input used only if `vy` is absent; ±1 maps to ±300 px/s in water or ±700 px/s in air for pose / hair direction.
- `angle`: optional radians of extra screen-space rotation about the foot anchor after the facing flip. Horizontal right dash uses 0; right-facing up dash uses `-Math.PI / 2`. Do not supply an absolute movement heading here unless you account for facing.
- `maxSpeed`: optional velocity normalization for hair, default 1320 px/s; clamped 640..2200. This avoids permanently flattened hair at the faster prototype speeds. Call `updateHair` once per simulation step.
- `topDown`: boolean for hair stepping; disables side-view falling lift. Overhead rendering itself uses `drawTop`.

`PlatformerCharacter.drawTop(ctx, state, timeSeconds)` uses a body-centre anchor at `state.x`, `state.y`; default width 96 px. It is a new proposed overhead view, a foreshortened crown / curtain / face / dress / feet built through the same symbol raster. Movement rotates the body. Eyes and symbol heart stay upright for readability.

- Direction follows `vx`, `vy`, falling back to `moveX`, `moveY` if velocity is absent.
- Optional top-view `angle` is an absolute body heading: 0 up, π/2 right, π down, -π/2 left. At rest, retain `angle` from the previous movement if desired; otherwise facing ±1 gives right/left.
- `runPhase`, `dashing`, `hair`, `width`, opacity/palette/heart options are supported. Cardinal footprints are roughly 96×96 at the default width; diagonal rotation can span more.

`createHair(state)` and `updateHair(hair, state, dt)` keep their existing API. `pose(state,time)` includes `dashing` and `swim` in its returned metadata. If root supplies `runPhase`, root controls cadence; fallback cadence caps at 3.6 cycles/s so a 3× sprint does not become a frantic tiny walk.

## Verification

2026-09-30: `node --check` passed. A real Chromium canvas rendered idle, 1320 px/s sprint, rising jump, falling hair lift, full dash, water, and all four overhead directions; see `character-qa-v2.png`. Stable sprint hair was about -0.235 figure widths, leaving room for reversal/landing motion within the ±0.48 safety range. Draw and pose contain no random state, external font, or asset dependency.

The overhead camera and movement poses are proposals for the music-video prototype. This module does not define physics, collision sizes, scene timing, dash ghosts, camera cuts, or audio synchronization.
