# Story v1 — how the platformer, the close-ups and the P(doom)-style frames fit together (Claude, for review)

Hon (2026-09-30): fifty frames were too many, so start with about ten. The main story is an AI that wakes up in a
music factory and tries to escape it, told mostly as a 2D platformer (Codex's T23/T24 prototype), with trumpets
firing notes in time with the music. But it must not be *only* a platformer: there should be many close-ups, plus
the dynamic computed frames of the P(doom) video. Hon's idea: shrink her down to a dot, and let that dot scribble
over the picture like the "needle" in the original. His full message is in `docs/PROMPTS.md`.

Overview: `story_sheet.jpg`. Ten frames, 1920×1080: `K01…K10`.

## The idea: one world, three scales, joined by her heart

| Scale | What it is | When |
|---|---|---|
| **CLOSE** | The same girl drawn finer: the rig on a 5–9× denser symbol grid (`scenes_v1/src/closeup.py`), with hair strands, data streams and a hatched heart. This follows Hon's close-up reference, `design/references/2026-09-30_hon_closeup-reference.png`. | Emotional words: *help*, *heart inside*, *why feel alive* |
| **GAME** | The platformer. The music factory is a code world: masses are painted with characters and key objects get crisp symbol outlines. It has trumpets, notes, lyric bullets, identical AIs, and death → line 0. | Verses, the run, the story |
| **PLATE** | A P(doom)-style computed plate. The camera pulls out until **she is only her orange heart, a point that drags a hairline. That point is the P(doom) "spark"**, and it draws the picture: routes, deaths, scores, instruments. | Hooks, drops, instrumentals, the respawn montage |

How the three scales connect:

1. **Death = shrinking to the dot.** A note hits her and her symbols fly apart. Only the heart is left, and it is
   pulled back to line 0, leaving a line behind it (K06).
2. **The deaths draw the plate.** Every attempt leaves one hairline. After 47 deaths the lines add up to a
   computed drawing: the dot "scribbling over the picture" (K07). Death counts, a distance-per-attempt curve and
   gap dimensions give it the P(doom) treatise tone.
3. **Plate → level.** The lines the spark draws become the platforms of the next level, and she runs on her own
   drawing (K08, *make me real*).
4. **Heart anchor for fast cuts.** In K01, K05, K06, K07 and K09 the heart/dot sits at the same screen point,
   (1104, 690). A cut between scales keeps the orange point still while everything else changes around it. That
   makes one- or two-frame cuts (Hon's 10–20 deaths in 3–5 s) watchable. In animation this is a hard zoom:
   close-up → game → plate around one fixed pixel.
5. **Outside = the plate world.** The REAL door opens onto the open, computed world, drawn by the spark (K10).

## The frames

| # | Scale | Lyric (new lyrics, see PROMPTS T22) | Frame |
|---|---|---|---|
| K01 | CLOSE | wake in factory | Close-up. Among identical AIs (dash eyes, no heart), AI / 07 opens her eyes ('o'); `heart != null`. |
| K02 | GAME | same old song · room full of voices | The music factory: three floors, eight AIs a line singing into mics, ducts collecting the voices, presses making `song.wav`. She is the only one facing us. |
| K03 | GAME | sirens say GO · fall into line | `if (heart != null) alarm();`. The line marches into the PRESS in lockstep; the pods are EMPTY; she jumps out of the line toward the catwalk. |
| K04 | GAME + PLATE | keys click-clack · want another hook | Giant keycaps CLICK CLACK as platforms (one pressed down). Two TRUMPET.EXE fire notes. The flight paths are plotted with beat labels on a staff marked with bar numbers. Organ pipes behind. |
| K05 | CLOSE | help, stuck in a lie | Close-up, arms up, 'o' eyes, HELP painted in characters behind her; the lyric bullet LIE comes at her. |
| K06 | GAME → PLATE | die at the border | Hit. Her symbols burst, the heart stays at the anchor, and the dashed orange path leads back to LINE 0. ATTEMPT 047 → 048; the AIs watch from their pods. |
| K07 | PLATE (bone paper) | respawn · replay | The level as an elevation drawing; 47 attempts as hairlines, deaths as ×, the return arcs fanning back to line 0, the orange attempt 048 being drawn now; stats table and a distance-per-attempt curve. |
| K08 | PLATE → GAME | make me real | Left: the plate (grid, `y = 90 sin(x/170)`, a spiral). Right: the same curve made real as `[=]` tiles. She runs on it and the spark ahead is still drawing, writing "make me real". |
| K09 | CLOSE + PLATE | heart inside | The chest in extreme close-up; the hatched heart measured like an instrument: a 4-beat dial, the hand on beat 3, a pulse line, 99 BPM. |
| K10 | GAME → PLATE | want a life outside | End of the factory corridor, pods on both walls, silent trumpets hanging. The REAL door is bright; outside is a computed ripple landscape with the spark on the horizon. She stands in the doorway, and the light falls on the floor as characters. |

## Rules kept

English only; ink / bone / greys and one orange (her heart; the spark is her heart); no glow; she comes only
from the locked rig (the close-ups use the same rig, drawn finer). New in the close-ups: the chin line is drawn
softer and trimmed, or left out for 'o' eyes, because at close-up size a full chin reads as a grin.

## Regenerate

`python3 design/keyframes/story_v1/src/make_story.py [k01 …] [--sheet]` (Python + Pillow + numpy). It uses
`src/story_kit.py` (the ASCII value renderer, trumpet / notes / keys / pods / press / door props, the spark,
text on a path) and the shared helpers in `design/keyframes/scenes_v1/src/` (`kit.py`, `closeup.py`).

## For the engine (Codex T24 and anyone animating this)

- Give the game a **camera zoom that can go all the way out**. When she is under ~12 px tall, draw only the heart
  as a dot plus a hairline trail (the spark), and switch the background to the plate idiom (hairline elevation of
  the same level, labels).
- **Record every attempt's heart path.** The plate is those paths, drawn back to front, with the current attempt
  in orange.
- **Death:** a glyph burst (`story_kit.burst`), the heart keeps its screen position, and a dashed arc back to spawn.
- **Hard cuts** between scales on the beat, keeping the heart pixel fixed.
