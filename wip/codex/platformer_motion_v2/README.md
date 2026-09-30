# Heart // six worlds — motion revision 1

An original Canvas2D music-video prototype for Hon. The full project and older art are preserved separately.

Open `index.html` in Chrome or Edge, or serve this directory. It starts a silent automatic preview. **Replay film + music** starts the 20-second song excerpt; **Play this world** switches to manual input.

## Controls

- A/D or left/right: immediate movement, reverse or stop.
- Space (or W/up in a side view): jump, then one air jump.
- X/Shift: dash; direction includes up/down in water and the overhead world.
- S/down: duck in side views; move down in free-moving worlds.
- R: restart. N: next world. Scene selector chooses any of six worlds.

## Film

| Time | World | Movement / visual structure |
|---|---|---|
| 0–3.2 s | Music factory | Same AI workers, conveyors, gears; fast side run and reversal |
| 3.2–6.4 s | Vertical memory | Zigzag upward jumps among bracket towers and moving code |
| 6.4–9.6 s | Buffer sea | Swimming up/down/back across code ruins, fish notes and currents |
| 9.6–13.6 s | Route grid | Actual overhead route right/up/left/up/right/down/right |
| 13.6–16.8 s | Sky score | Double jumps and air dashes over floating piano islands |
| 16.8–20 s | Lyric cathedral | Lyric/instrument crossfire, camera push and REAL gate |

Side worlds have three independently animated background depths (.12/.35/.65), gameplay at1.0 and brief foreground passes at1.4. Overhead uses an atlas, animated score floor, raised glyph walls, heroine and overhead conduits. Marks, architecture, enemies and hair are calculated; no video-generation model was used.

Physics:120Hz; video:60fps. Side speed1150–1440px/s (old prototype480), dash2850, gravity5200, jump1500, coyote85ms, input buffer100ms, maximum2jumps. Directional input snaps deliberately as Hon requested. Hair remains damped and reacts to actual velocity/acceleration. The local rig extension leaves the locked shared girl and app source untouched.

## Dense attacks and movie choreography

200attacks are emitted over20seconds:10per second, with six incoming directions, readable lyric phrases and glyph notes. A shot remains alive for2.8seconds; peak active count is recorded by `motion_audit.json`. Collision is active in both modes. Dash has115ms collision grace.

The automatic film is choreographed. It first rehearses its original physics route, then selects narrow attack crossings around that future route. It does not grant general invulnerability. Manual mode aims at the live heroine; it is intentionally very difficult, and is not a balanced commercial game. Death resets the current room. Only the final world currently has an exit condition; N/selector lets reviewers explore all worlds.

The song is the project's current Final master,42.012–62.012seconds, matching the earlier movement test. This revision tests speed, visual variety, layers and pressure. Beat-by-beat cut alignment, a longer death montage and whole-song story remain future edit work, as Hon allowed for this stage. These scenes are proposals, not locked final art.

## Reproduce

`node capture.mjs audit` writes the route/event audit and PNG samples. `node capture.mjs render NEW_NAME.mp4` exports1080p60 H.264/AAC and refuses an existing movie destination. Installed Chrome, bundled Playwright and FFmpeg paths are machine-specific in the script; the playable page has no package dependencies.

`control-qa-v2.mjs` verifies snap control, second/blocked third jump, dash lifecycle, water/overhead cardinal and diagonal inputs, and on-screen film framing. It writes `control-qa-v2.json`.

Movement reference read: the developer's [official Celeste Player source](https://github.com/NoelFB/Celeste/blob/master/Source/Player/Player.cs) and [Player README](https://github.com/NoelFB/Celeste/blob/master/Source/Player/Readme.md). All engine and visual code here is original; no Celeste characters or artwork are included.

Files: `game.js` controller/physics/attacks/camera; `character.js` articulated glyph rig; `worlds.js` five side/swim worlds; `topdown.js` overhead architecture/collision; `capture.mjs` offline renderer; module notes and QA in this folder.
