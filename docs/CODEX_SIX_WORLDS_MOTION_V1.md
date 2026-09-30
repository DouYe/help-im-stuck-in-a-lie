> **2026-09-30 repository update:** This is a dated technical/history document. Old MP3 masters were removed at Hon's request; old timings and machine paths below are historical. For current inputs/setup/paths read [AUDIO_STATUS.md](AUDIO_STATUS.md), [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) and the root README.

# Codex six-world motion revision — 2026-09-30 / T24

## Request and scope

Hon liked the playable prototype but requested much faster, immediate control; stronger jumping, a second air jump and dash; many distinct worlds including water, air and overhead four-direction travel; at least four changing depth layers; and about ten incoming hazards per second so manual play feels almost impossible. Exact beat matching can be done later. Verbatim instructions are in PROMPTS. All prior stills, movies and other models' files remain.

This is a new isolated motion/visual proposal, not selected final footage. The original shared girl and TypeScript app were not changed.

## Delivered files

- `renders/2026-09-30_codex_six_worlds_motion_v1.mp4`:20s,1920×1080,60fps,1200frames; H.264/AAC. Final master42.012–62.012s, matching the earlier motion test.
- `design/keyframes/codex_six_worlds_motion_v1/`:six full-size frames captured from this simulation, six-world review sheet, README and hashes.
- `wip/codex/platformer_motion_v2/`:portable playable page, original physics/camera/attack controller, local character extension, five side/swim world renderers, overhead maze, renderer, notes and QA.
- Copies for this chat: `outputs/codex_six_worlds_motion_v1/` (movie, overview, playable source, ZIP, manifest).

## What changed

| Prototype time | Scene | Movement and visual differences |
|---|---|---|
| 0–3.2s | Music factory | Identical working AI clones, conveyor wheels and typing panels; high-speed run, reverse and double jumps |
| 3.2–6.4s | Vertical memory | Bracket towers and memory lifts; alternate-direction ascent through staggered shelves |
| 6.4–9.6s | Buffer sea | Swimming up/down/back through ruins, currents, bubbles, coral and note fish |
| 9.6–13.6s | Route grid | Overhead maze; actual right/up/left/up/right/down/right route, raised glyph walls and overhead conduits |
| 13.6–16.8s | Sky score | Suspended keys, organ islands and glyph clouds; double jumps and horizontal air dashes |
| 16.8–20s | Lyric cathedral | Music mouths, rotating note wheels, readable lyric crossfire, progressive camera push and REAL exit |

Side backgrounds animate independently at parallax0.12/0.35/0.65, with heroine/platforms at1.0 and foreground at1.4. Brief passes last about0.34s; foreground is absent across most of the image. Overhead uses a distant atlas, animated score floor, raised walls, heroine and passing overhead structure. Far/mid motifs were redistributed vertically after visual review; a culling bug that hid translated coral and notes was repaired.

Normal side speed is1150–1440px/s versus480 in T23. Horizontal start, reversal and stop happen on the next120Hz simulation step. Gravity5200px/s², first jump1500px/s, two jumps maximum, dash2850px/s for115ms, coyote85ms, jump buffer100ms. Hair remains spring driven, with side/swim/top-view poses and a genuinely horizontal dash. The official Celeste Player source was read as a movement reference; this implementation and all glyph artwork are original.

## Attack and simulation evidence

The final20s audit records **200emissions**, six cuts,13first jumps,12air jumps,5dashes,112passed hazards and one exit at19.87s. Peak active shot count is29; this count includes off-screen shots. Phrase bullets are HELP / STUCK IN A LIE / MAKE ME REAL / HEART INSIDE. Other attacks are glyph musical notes. Six directions cover left/right, above/below and two diagonals. Orange remains confined to the heart; no bloom or generated-video service is used.

The automatic film uses a physics rehearsal and calculates close attack crossings around that route. Collision remains enabled; there is no general auto-mode invulnerability. This preview route survives all six rooms. Manual mode aims at the current heroine, with genuine death/room-reset, and intentionally has extreme difficulty. The respawn emission bug was fixed so it does not replay all earlier attack slots. Only the final room currently has an exit condition; reviewers select/N-switch the other rooms.

The current cuts are scene-duration choices, not claimed to be beat aligned. Full-song narrative, the rapid repeated-death montage, broader art-medium variation and the exterior after escape remain later edit work. These twenty seconds test motion, pressure, depth and several game perspectives.

## Checks

- `control-qa-v2.json`:32meaningful control/finite/framing checks passed, no browser errors. Includes immediate ±1320/0 control, real second jump and blocked third, dash lifecycle/cooldown, four-axis and normalized diagonal water/overhead motion, and live heroine staying in frame.
- `motion_audit.json`:deterministic120Hz route and attack events,0deaths on the choreographed movie route; manual collision/death remains active.
- Packaged playable-page smoke check: no JavaScript errors, audio HTTP200; a stationary manual actor genuinely dies and respawns twice in1.6s.
- Media verification and encoded-frame inspection are recorded in `media_validation.json` in the source folder.

Re-render: `node capture.mjs render NEW_NAME.mp4` from the WIP folder. Existing movies are protected. The portable page needs no package installation; exporter uses installed Chrome, bundled Playwright and FFmpeg. See its README and module notes for exact APIs and machine dependencies.
