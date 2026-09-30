# Heart // Factory Escape — playable motion test

Open `index.html` in Chrome or Edge. The film replays automatically. Click **Play yourself** to control the same simulated character: A/D or left/right to move; Space/W/up to jump; S/down to duck; R to restart.

The world is calculated at 120 physics steps per second and filmed at 60 fps. This is a small actual 2D platformer engine: movement acceleration, gravity, platform collision, flying-projectile collision, death, respawn and an exit. The automatic controller uses the same movement and collision rules as manual play. It jumps at gaps and ducks or jumps when projectiles approach. Its first attempt deliberately fails to duck; the second changes that action.

The character is an isolated motion extension of the approved 17×27 symbol girl. Running feet and knees articulate; jump/fall legs prepare for the landing; landing compresses the body briefly. Hair roots stay at the scalp, while tips follow a damped spring driven by velocity and acceleration. The orange symbol heart follows the torso. Existing locked rig files are unchanged.

Files:

- `index.html`, `game.js`, `character.js`: self-contained playable scene, no libraries or internet required.
- `character-notes.md`: local rig and spring API.
- `motion_audit.json`: deterministic event log for the automatic film.
- `capture.mjs`: this Windows machine's renderer using installed Chrome, bundled Playwright and FFmpeg. Run `node capture.mjs audit`, or `node capture.mjs render NEW_VERSION.mp4`. The renderer refuses an existing destination. Runtime paths in this script are machine-specific; the playable HTML is portable.

The video is a 20-second **movement prototype**, using the current project's Final song at 42.012–62.012 s. It tests gameplay and follow-through rather than deciding the complete music-video edit or the final escape environment. The last gate is a level endpoint; the full story's outside world remains to be designed. The v1 rendered movie is retained as a process draft; v2 improves visible head clearance under high lyric attacks.

All earlier image sets remain in their original locations. No AI video generation or Blender scene was used for this calculated test.
