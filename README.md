# Help! I'm stuck in a LIE — music video

Shared source, visual references, rendered previews and working records for Hon's music video. The aim is for another AI to clone this repository, understand the work, continue it and return updates through GitHub.

**Updated: 2026-09-30.** The six-world motion prototype fits Hon's current expectations. It is a direction to build on; final shots, full-song editing and the rapid death montage are still open. **Replacement song and lyrics are pending.** Earlier MP3 masters are retired; see [audio status](docs/AUDIO_STATUS.md) before using any timing data. Hon requested publishing the existing work now and will supply the new song in a later prompt.

## Start here

1. Read [AGENTS.md](AGENTS.md), [current status](coordination/STATUS.md), [decisions](docs/DECISIONS.md), the newest three [worklog entries](coordination/WORKLOG.md), and [tasks](coordination/TASKS.md).
2. Read [repository setup and collaboration](docs/REPOSITORY_GUIDE.md), then claim a task before editing.
3. Hon's actual instructions are recorded in [PROMPTS](docs/PROMPTS.md). Distinguish those instructions from another model's proposals.

For Hon: [中文使用说明](使用说明.md). For the detailed motion implementation: [Codex Chinese handoff](docs/CODEX_AGENT_HANDOFF_V1.md) and [six-world technical record](docs/CODEX_SIX_WORLDS_MOTION_V1.md). Those dated records mention former audio files and local preview ports; the current setup and audio status above take precedence.

## The story and visual direction

An AI girl awakens in a music factory among identical AI workers. Only she has an orange symbol heart. She attempts to escape, repeatedly dies and returns to the start, then eventually gets out. The world is constructed from characters and code: platforms, architecture, music-instrument enemies, note projectiles and readable lyric attacks.

Platformer movement is the main motion language, with water, sky, overhead travel, close-ups, occasional depth/3D and computed artwork for variety. Keep each composition readable while allowing intense cuts. Black, white and grey dominate; orange belongs to the symbol heart. The locked screen rules and character details are in [DECISIONS](docs/DECISIONS.md) and [GIRL_SPEC](design/character/GIRL_SPEC.md).

## Watch, play and review

| Work | Location | State |
|---|---|---|
| Latest 20-second, 1080p60 six-world motion movie | [MP4](renders/2026-09-30_codex_six_worlds_motion_v1.mp4) | Hon: this version fits expectations; motion direction accepted, final film unfinished |
| Latest playable Canvas source | [platformer_motion_v2](wip/codex/platformer_motion_v2/) | Immediate movement, double jump/dash, six worlds, animated depth and 10 attacks/sec |
| Six frames captured from that simulation | [frame pack](design/keyframes/codex_six_worlds_motion_v1/) | Review materials; individual final shots not selected |
| Seven selected Codex code-world still references | [selected references](design/keyframes/codex_selected_references_v1/) | Hon kept 02–06, 07B and 08 as references |
| Claude's eight visual media | [styles_v1](design/keyframes/styles_v1/) | Hon said all good; exact usage and orange field colours remain open |
| Claude's 10-frame close/game/computed-plate story | [story_v1](design/keyframes/story_v1/) | Proposal awaiting selection; death lines becoming platforms are not implemented |
| Codex four-frame AI factory/escape proposals | [music_factory_lab_v2](design/keyframes/codex_music_factory_lab_v2/) | Proposal awaiting selection |
| Claude's 13 bold-girl keyframes | [v3](design/keyframes/v3/) | Awaiting review |
| Other models' explorations | [wip](wip/), indexed in [FILE_MAP](docs/FILE_MAP.md) | Mixed review and rejected sets; preserve their labels and history |

The current automatic movie uses real physics with choreographed attack crossings and survives its six rooms. Manual mode has collision, death and room reset, with deliberately extreme difficulty. A rapid repeated-death montage, whole-song beat/lyric alignment, close-up/computed-plate integration and the outside world are still to do.

## Clone the complete project

```sh
git lfs install
git clone https://github.com/DouYe/help-im-stuck-in-a-lie.git
cd help-im-stuck-in-a-lie
git lfs pull
```

Install Git LFS before cloning so images, movies and future song audio arrive as real media. A download containing only small text pointers is incomplete. Setup and run commands: [REPOSITORY_GUIDE](docs/REPOSITORY_GUIDE.md).

To play the latest prototype with Node 20+, run `node tools/serve-motion.mjs --port 5190` from this root and open its printed URL. No npm install is needed for preview. It is silent while the replacement master is pending. Audit/capture commands are in [tools/README.md](tools/README.md).

## Folder map

```text
coordination/        STATUS, TASKS, WORKLOG — shared current state
docs/                brief, instructions, decisions, pipeline, lyrics and handoffs
design/              character, world rules, style index, keyframes and references
wip/<model>/         preserved model-specific sources, trials and audits
renders/             dated movies; earlier root movies now in renders/archive/
app/                 original TypeScript/three.js video engine
analysis/            historical beat and lyric analysis sources/results
data/                retired-master timing data; pending regeneration for new song
audio/current/       replacement master destination: song.mp3 (not supplied yet)
archive/             earlier Claude deliveries, audio-free snapshot, relocation map
tools/               portable project entry commands
```

[FILE_MAP](docs/FILE_MAP.md) explains the packs and their state. [Relocation manifest](archive/relocation-manifest.json) maps moved historical paths to their new locations. The local project and GitHub use the same relative paths; `.git`, installed dependencies and regenerated caches are local infrastructure.

## Attribution and rights

The earlier TypeScript engine adapts [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video); its MIT licence is preserved as [LICENSE.pdoom-engine](LICENSE.pdoom-engine). That licence covers the upstream engine's applicable code. Making this repository public does not grant a new licence for Hon's song, lyrics, original characters or artwork. Asset origins and review history remain in the project records.
