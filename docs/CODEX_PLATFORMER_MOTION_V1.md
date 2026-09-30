# Codex platformer motion test — 2026-09-30 / T23

Hon explicitly resumed video work for this test: running, incoming objects and dodging should feel like an actual platformer, with natural hair inertia while falling. The implementation is a small deterministic 2D Canvas engine, filmed offline. No generated-video service or Blender was needed for this prototype.

## Review files

- `renders/2026-09-30_codex_platformer_motion_v2.mp4`: 20.000 s, 1920×1080, 60 fps / 1,200 frames, H.264 + AAC. Current Final song excerpt 42.012–62.012 s.
- `renders/2026-09-30_codex_platformer_hair_slow_v1.mp4`: 4.000 s, 1920×1080, 60 fps / 240 frames, silent. Close view of prototype 9.2–11.2 s at half speed, re-rendered at 120 source time samples/s; not AI interpolation.
- `wip/codex/platformer_motion_v1/index.html`: open in Chrome/Edge for automatic replay or manual play. A/D or arrows move; Space/W/up jump; S/down duck; R restarts.
- Source: `game.js`, `character.js`, `capture.mjs`, `README.md`, `character-notes.md` in the same folder. The previous rendered v1 movie remains there as a process draft.

## What is calculated

Physics runs at fixed 1/120 s. Horizontal acceleration, gravity (2,350 px/s²), a jump impulse (−990 px/s), platform contact and projectile collision produce the motion. Normal speed is 480 px/s; the last stretch reaches 550 px/s. The film controller uses the same rules as manual play. On the first attempt it deliberately does not duck; the second remembers that action. It also looks ahead to platform gaps and incoming notes.

The local articulated rig preserves the symbol girl's 17×27 vocabulary and orange heart. It adds knees, swing/contact feet, jump tuck, fall extension, landing compression and damped hair driven by velocity/acceleration. The hair roots stay at the scalp. Locked shared character files and engine files remain unchanged; this local extension is a proposed motion implementation awaiting review.

## Observed event times in the 20-second test

| Prototype time | Event |
|---|---|
| 1.92–2.75 s | First jump across the gap |
| 3.02 s | LIE collision / death |
| 3.66 s | Return to factory origin, attempt 02 |
| 6.82 s | LIE passes over the ducked heroine |
| 9.72–10.11 s | 190 px drop; hair rises and landing compresses the body |
| 11.11 / 15.50 s | Notes pass underneath while she is airborne |
| 12.32 / 17.47 s | STUCK / HELP pass over her duck |
| 18.30–18.53 s | Final jump clears a three-note volley |
| 18.48 s | REAL gate reached |

The event log records one death, one respawn, eight passed projectiles and an exit. All 17 manual-control checks passed; both movies passed full FFmpeg decoding, and ffprobe confirmed dimensions, frame rates, frame counts and audio presence. Full-size encoded frames were checked at the duck and drop. Perceived motion and art direction remain for Hon to judge in playback.

This is a gameplay/movement test. It has one factory environment and a restrained late camera push. It does not yet represent the whole-song edit, the many-style montage, or a fully designed exterior after escaping. The current gate reads as a completed level. All older picture sets, earlier motion tests and other models' assets remain available.

## Re-render on this machine

From `wip/codex/platformer_motion_v1/`: `node capture.mjs render NEW_VERSION.mp4`; for the close half-speed clip: `node capture.mjs slow NEW_SLOW_VERSION.mp4`. The exporter uses installed Chrome plus the current bundled Playwright path in `capture.mjs`, and FFmpeg on PATH. It serves only a private localhost renderer and exports top-down Canvas RGBA, so no WebGL vflip is applied. Explicit stream mapping excludes the MP3's attached cover art. The capture script refuses an existing destination; the playable HTML itself needs no dependencies.
