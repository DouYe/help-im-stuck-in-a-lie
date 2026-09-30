# Portable six-world preview and capture

These tools read `wip/codex/platformer_motion_v2/` without changing its game, drawing, physics or choreography.
The old `capture.mjs` and QA scripts in that delivered folder remain historical machine-specific records.
Run commands from the repository root. Node 20+ is required; no dependency is needed for the playable preview.

## Preview

```sh
node tools/serve-motion.mjs --port 5188
```

Open the printed localhost URL. The existing controls and six-world automatic film work as before.
The server maps the page's `preview_audio.mp3` request to `audio/current/song.mp3`.
It starts silently if the replacement song has not arrived. It never searches old masters or extracts audio
from an earlier video. A new master starts at zero by default because its word timings are not yet confirmed.

```sh
node tools/serve-motion.mjs --port 5189 --audio audio/current/song.mp3 --audio-start 42.012
node tools/serve-motion.mjs --silent
```

A nonzero start crops a 20-second temporary MP3 with FFmpeg and removes that temporary file on shutdown.
The example `42.012` is the **previous prototype's** offset; confirm it against the replacement song.
The preview serves only the motion source folder and the selected audio, bound to `127.0.0.1`.
Use Ctrl+C to stop. An occupied port is reported, rather than stopping another running agent's service.

## Capture

Install the root's pinned capture dependency. This does not download a browser automatically.

```sh
npm ci
npm run audit:motion -- --out wip/YOUR_MODEL/motion_audit_v1
npm run render:motion -- --out renders/NEW_NAME_v1.mp4 --audio audio/current/song.mp3 --audio-start 0
```

`audit` calculates the complete 20-second route and writes its events plus 12 PNG samples into a **new** folder.
`render` writes 1920×1080, 60 fps H.264/AAC, plus `NEW_NAME_v1.mp4.audit.json`.
It requires FFmpeg on PATH, and FFprobe for checking that the selected audio contains the whole excerpt.
Use `--ffmpeg /path/to/ffmpeg` or `FFMPEG_PATH` for another installation; FFprobe is discovered beside that path,
or can be set with `--ffprobe /path/to/ffprobe` / `FFPROBE_PATH`.
It refuses an existing video, report or audit directory. Choose a new versioned destination.
Missing audio is an error when rendering; a silent test requires an explicit flag:

```sh
node tools/capture-motion.mjs render --out wip/YOUR_MODEL/silent_smoke_v1.mp4 --silent --duration 1
```

`--duration` (up to 20 seconds) and `--fps` (1–120) support short technical smoke captures.
They do not stretch the original timeline. For the delivered movie's motion use the 20s/60fps defaults.
Cuts, hazards and lyrics are still the prototype's existing choreography; this is not replacement-song analysis.

### Chrome / Edge / Chromium

The capture helper looks for installed Chrome or Edge on Windows and macOS, and Chrome/Chromium on Linux.
Override discovery with `--chrome /absolute/path/to/browser`, `CHROME_PATH`, or `--channel chrome` / `--channel msedge`.
If none is installed, the optional command `npx playwright-core install chromium` installs the dependency's
matching Chromium; capture then uses that standard Playwright cache. No Codex cache path is embedded.
On Linux, install the browser's required system libraries as appropriate for your environment.

The current drawing code requests `Consolas,monospace`. Consolas availability and browser font rasterization
can change typography across operating systems; the helper does not substitute or redesign the art.

## Python stills and older pipelines

```sh
python -m venv .venv
# Activate the environment using your operating system's normal command.
python -m pip install -r requirements.txt
```

`requirements.txt` covers Pillow-based still generators. The candidate generator's relocated project-root
calculation is repaired in `design/keyframes/codex_candidates_v1/src/make_candidates.py`.
Older analysis scripts additionally need `numpy`, `scipy`, `matplotlib` and sometimes `onnxruntime` plus external
model files. They contain historical machine paths and master-specific section maps: inspect them before use.
The TypeScript/Three.js engine in `app/` keeps its separate Bun/package setup. This helper does not certify or
silently rerun that older pipeline. New audio and lyrics require new timing analysis before final beat editing.

## Verification of this tooling

See `verification.json` for the local Node/server/browser/capture checks. Windows was tested locally.
macOS/Linux browser discovery is implemented but has not been executed on those operating systems.
