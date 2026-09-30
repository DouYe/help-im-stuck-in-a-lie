# Animated symbol-built environments

This is the isolated scene-rendering module for the fast platformer music-video motion proposal. It leaves the shared approved character rig and earlier outputs untouched.

## API

`MusicWorlds.draw(ctx, sceneId, state)` draws a full frame's background and traversable geometry. `state` accepts `{time, localTime, p, cam, platforms, width, height}`. `cam` is `{x,y,zoom}`, world coordinates centered at `(960,570)` on a 1920×1080 frame. A platform is `{x,end,y,name}`. Draw heroine and real hazards afterward, under `translate(960,570); scale(cam.zoom); translate(-cam.x,-cam.y)`. Then call `MusicWorlds.drawForeground(ctx, sceneId, state)`.

Five scene IDs: `factory`, `shaft` (also `vertical`), `water` (also `underwater`), `sky`, `final` (also `cathedral`). The module only uses ink, bone and gray. It never draws an orange heart itself. Factory clone bays optionally call the original `PlatformerCharacter.draw` API, always with `noHeart:true`; the girl's hero motion belongs to root's physics/character modules.

## Five compositions

- Factory: large distant parallel production lines, animated gears and cables, identical AI bays with gentle working motions, and a shared moving conveyor.
- Shaft: tall bracket rails, moving lifts and braces, background vertical stacks; camera movement in both axes is visible in the depth layers.
- Underwater: long current glyphs and subtle horizontal refraction, receding ruined arches, syntax coral, buoyant bubble glyphs, note-fish schools.
- Sky: island silhouettes with glyph shading, clouds made of code density, distant organ-palace architecture and suspended piano keys.
- Final: nested cathedral arches, a rotating note wheel, receding lyric columns and brass mouths, plus an exit gate anchored to the last traversable platform.

Every environment has three distinct animated background depths at 0.12, 0.35 and 0.65, then the primary platform world at 1.0. Sparse foreground glyph scenery travels at 1.4 and is drawn after the player. A narrow foreground pass is visible for only 0.34 seconds every 4.7 seconds; bottom-edge strips remain away from the central action. Type-on rows, gears, waves, fish, notes, lifts, conveyor marks and clone gestures are deterministic functions of time, so seeking a frame gives reproducible art.

The renderer intentionally supplies geometry rather than physics, collision, true projectiles or scene timing. Those are controlled by game.js. The apparent enemies in the final architecture are decorative emitters; game.js owns the hazards.

Verification: Node's parser accepted the module, and all five background/foreground APIs completed smoke draws with representative camera/platform inputs. Visible-glyph bounds pruning limits draw calls to approximately 2,000–5,800 for the tested 1920×1080 view, before the optional clone rig. Final composition and interaction are to be checked in root's integrated render.

Integrated still review at 1.5 / 4.8 / 8.0 / 11.5 / 15.2 / 18.5 seconds confirmed a centered readable heroine, clear platform edges and legible attack phrases across six distinct scene silhouettes. A composition problem clustered factory/water/sky far and middle art in the bottom half. Root authorized a revision: far/middle Y offsets are now factory -400/-220, water -400/-220, sky -430/-210; far motifs received a small visibility lift, while nearer heroine/platform contrast remains dominant. Shaft and cathedral were unchanged. Local-coordinate note/coral helpers now suspend world-coordinate glyph culling after a correct world bounding check, restoring visible coral and idle musical notes. Final capture should use this revised module.
