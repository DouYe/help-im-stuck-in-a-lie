# Repository setup and AI collaboration

Updated: **2026-09-30**. Repository destination: [DouYe/help-im-stuck-in-a-lie](https://github.com/DouYe/help-im-stuck-in-a-lie). The local canonical project is `D:\Videos\Help! I'm stuck in a LIE` on Hon's PC. Elsewhere, use the root of your clone; all paths below are relative to it.

## Get every asset

```sh
git lfs install
git clone https://github.com/DouYe/help-im-stuck-in-a-lie.git
cd help-im-stuck-in-a-lie
git lfs pull
git lfs ls-files
git status --short
```

Install Git LFS and fetch its content before reviewing media. If an image, movie or song file contains text beginning `version https://git-lfs.github.com/spec/v1`, you have a pointer rather than the media. Run `git lfs pull` in the clone. Preserve `.gitattributes` so subsequent binary additions use the same storage rules.

The publication's tracked paths and original media hashes are in `coordination/REPOSITORY_MANIFEST.json`. Run `python wip/codex/repository_cleanup_v1/repository_manifest.py verify` after a fresh clone to check them. The dated publication check is recorded in `coordination/REPOSITORY_VERIFICATION.json`; regenerate the manifest deliberately when a later task adds or changes tracked files.

The repository contains authored sources, documentation, media, selected references and preserved exploration packs. `.git`, `node_modules`, Python environments, bytecode and regenerated tool caches are local infrastructure rather than deliverables. Both local and GitHub project files use the same relative paths; there is no separate flattened upload layout.

## Understand before changing

Read `AGENTS.md`, `README.md`, `coordination/STATUS.md`, `docs/DECISIONS.md`, the newest three `coordination/WORKLOG.md` entries and `coordination/TASKS.md`. Then read the specific pack's README/spec and claim a task.

- Hon's directions and approvals are in `docs/PROMPTS.md` and `docs/DECISIONS.md`. Another model's proposal is not an approval.
- `docs/AUDIO_STATUS.md` is the current master state. The new song and lyrics are pending; old cue data and old-master references in historical documents are not current.
- `docs/FILE_MAP.md` maps the packs. `archive/relocation-manifest.json` resolves older root/Claude-output paths that remain in history and manifests.
- Start current motion work from `wip/codex/platformer_motion_v2/`. The older movie named `codex_platformer_motion_v2.mp4` belongs to **source v1**; the newest film name includes **six_worlds**.
- Claude's `design/keyframes/story_v1/` proposes close/game/computed-plate continuity. Zoom-to-heart, accumulating death lines and lines becoming platforms are not implemented in the six-world engine.

The previous Chinese handoff and technical records remain useful for module interfaces and verified motion results. They mention local ports 5188/5189 and removed audio masters; use the current setup and audio document for those parts.

## Preview without a build

With Node 20+ installed, run the portable preview from the repository root. It needs no package installation:

```sh
node tools/serve-motion.mjs --port 5190
```

Open the URL printed by the server, normally `http://127.0.0.1:5190/`. It maps the page's preview audio request to `audio/current/song.mp3`, and stays silent while that file is missing. Use **Play this world** for manual input. A/D or left/right move, Space jumps twice, X/Shift dashes, W/S or arrows navigate water/overhead, R resets, N changes worlds. Use Ctrl+C to stop the server.

For a silent fallback, open `wip/codex/platformer_motion_v2/index.html` in Chrome/Edge, or serve the repository with `python -m http.server 5190 --bind 127.0.0.1` and visit `/wip/codex/platformer_motion_v2/`. The fallback does not map the new master to the page's old preview-audio filename.

## Portable audit and movie capture

```sh
npm ci
npm run audit:motion -- --out wip/YOUR_MODEL/motion_audit_v1
npm run render:motion -- --out renders/NEW_NAME_v1.mp4 --audio audio/current/song.mp3 --audio-start 0
```

The root package lock pins `playwright-core`; use an installed Chrome/Edge/Chromium browser and FFmpeg on PATH. Overrides include `--chrome /absolute/path/to/browser` or `CHROME_PATH`, and `--ffmpeg /path/to/ffmpeg`. The helpers refuse existing render/audit destinations. While new audio is pending, an explicit silent technical capture is available:

```sh
node tools/capture-motion.mjs render --out wip/YOUR_MODEL/silent_smoke_v1.mp4 --silent --duration 1
```

See [tools/README.md](../tools/README.md) for audio offsets, browser setup, dependencies and the recorded verification. Windows has local verification; macOS/Linux discovery is implemented but has not been executed on those systems. The prototype's typography requests Consolas, so a different font/browser can change rasterization. The historical WIP `capture.mjs` and some QA scripts contain Hon's installed Chrome/Playwright paths; they are preserved records rather than the portable entry point. Capture does not perform new-song beat or lyric alignment.

## Other pipelines

| Pipeline | Entry | Dependencies and scope |
|---|---|---|
| Six-world Canvas prototype | `wip/codex/platformer_motion_v2/` | Browser for playing; portable capture tooling for deterministic MP4 export |
| Earlier TypeScript/three.js scene engine | `app/` and `docs/PIPELINE.md` | Bun, Chrome and FFmpeg; `bun install` inside app. Existing cue/audio settings need the new-master migration |
| Character/world/static sheets | `design/**/src/` and pack specs | Python/Pillow; original authored fonts are retained under `app/public/fonts/` |
| Beat and lyric analysis | `analysis/`, `analysis/align/`, `docs/PIPELINE.md` | Python scientific libraries; separation/alignment models fetched separately. Inspect old hardcoded paths and overwrite behaviour |

The repository preserves past scripts as well as current tools. Some historical Python files refer to `D:\Videos\...` or `/home/claude/lie-video`; older capture scripts refer to a Codex dependency cache. Inspect or adapt these paths in a new version before running them. The project does not promise every historical generator is portable unchanged.

## Continue and return an update

Start with a clean working tree. Fetch updates before claiming work. Use a branch for a parallel change, and keep each model's new work in its own `wip/<model>/` version. Do not edit another active task's owned files.

```sh
git pull --ff-only
git switch -c <model>/<task-name>
# Create the change, review it and complete the project handoff records.
git status --short
git diff --stat
git diff
git add <changed-project-paths>
git commit -m "Describe the completed change"
git push -u origin <model>/<task-name>
```

Use your own GitHub identity with write access; an existing public clone grants read access, not push permission. Return a pull request or branch for merging if working concurrently. If Hon chooses serial direct updates, pull before the next change and push without rewriting shared history.

At the end, update `coordination/WORKLOG.md`, `STATUS.md` and `TASKS.md`; log any new user instruction in `docs/PROMPTS.md`, and update decisions/file/style indexes as applicable. Include files, validation, open issues and the next useful step. Commit documentation with the actual artifacts so the next AI can understand one revision from the repository alone.

Retain previous images, videos and delivery versions. Make a new version for art/code changes. The 2026-09-30 cleanup is a specific exception authorized by Hon for superseded MP3s; it does not authorize deleting other retained media.

## Rights and source attribution

`LICENSE.pdoom-engine` preserves the MIT licence for the adapted upstream engine. Original song, lyrics, character and artwork have no new licence grant merely because this repository is public. Keep source references and prior authors' records when adapting their work.
