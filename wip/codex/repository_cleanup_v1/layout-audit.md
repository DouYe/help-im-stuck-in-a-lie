# Local layout audit · 2026-09-30

Read-only inspection of the D-drive project; no project files were moved or deleted. This note is the only write.

## Retain these paths

- `app/` is the earlier TypeScript/Bun engine. Its server serves project-root `audio/` and `data/` and app `public/` assets (`app/scripts/serve.ts:11–12,54`); font files are project assets. `app/src/main.ts:98` and `app/scripts/render.ts:113` use `audio/edit/song.mp3`.
- `wip/codex/platformer_motion_v2/` is the latest six-world Canvas prototype. Keep it alongside v1. `capture.mjs:12–13` resolves `../../../audio/final/song.mp3` with `preview_audio.mp3` fallback; the preview excerpt is also an old MP3 to remove under Hon's instruction. Browser playback references that excerpt.
- Retain all `design/`, `wip/<model>/` source, images, video proposals, notes and QA JSON. The generated stills/QA pictures communicate rejected versus accepted ideas, and historical sets were explicitly preserved.
- `analysis/` holds 24 scripts/results, not a large cache. `data/` holds beat/lyric analysis of the old masters; keep provenance but mark obsolete until new audio and lyrics are analyzed.
- Existing generators depend on folder depth (`__file__.parents[n]`); retain app/design/wip depths for this cleanup. Some generators are already machine-specific: e.g. `analysis/plot_ssm.py:4`, `analysis/plot_bargrid.py:6` use `/home/claude/lie-video`; many WIP Python scripts use D-drive paths; captures/QA load Playwright from the Codex cache and hardcode Chrome. These need portable path resolution for GitHub takeover.
- Copied `design/keyframes/codex_candidates_v1/src/make_candidates.py:12` uses `HERE.parents[2]`, which resolves to `design/`, although it expects the project root. The original `wip/codex/visual_audit/make_candidates.py` resolves correctly. Fix this copy before presenting all generators as runnable.

## Safe minimal rearrangement

1. Root's four historical MP4 files → `renders/archive/`, preserving bytes/names.
2. Root's two ChatGPT PNG references → `design/references/archive/`, preserving both originals. The 12:20:50 file is hash-identical to `design/references/2026-09-30_hon_closeup-reference.png`; 12:20:22 is unique.
3. `Claude outputs/` → `archive/claude_outputs/`, preserving all 35 files (46.4 MB). No byte-identical duplicates elsewhere were found; current FILE_MAP's “same images” text is inaccurate. Docs reference its S5 image; update those links.
4. `lie-video-project.zip` needs special handling: it contains TWO old MP3 masters. It is mostly redundant (114 byte-identical entries), but has 14 older changed files and a unique `analysis/syl_onsets.npy`. Retain an audio-free archival snapshot rather than discard its unique contents. Old audio must not survive concealed inside the ZIP.
5. Root contains four old MP3s; `audio/{real,edit,final}/song.mp3` and both prototypes' preview excerpts are also old songs. Remove them after recording the inventory; introduce the intended new master destination and mark the song as pending.

Update README, FILE_MAP, STATUS, TASKS and Chinese usage links after moves; WORKLOG/PROMPTS should retain historical wording with a relocation map. No executable code references root media names or `Claude outputs/` were found.

## Dependencies and duplication

- No nested Git repository, node_modules, symlink or junction was found. All individual files are below 50 MiB.
- `wip/codex/visual_audit/lib/` is a bundled Pillow installation, plus `__pycache__` directories scattered in source trees. These are reproducible dependencies/caches: replace the library payload with declared Pillow setup and ignore caches; do not ignore media, fonts or QA results broadly.
- Delivered MP4 duplicates: `renders/2026-09-30_codex_six_worlds_motion_v1.mp4` = WIP `six_worlds_motion_v1.mp4` (40.3 MB); platformer movie (12.8 MB), slow hair clip (2.0 MB), and game-world board (5.3 MB) also have WIP copies. Keeping them is least disruptive because delivery scripts reference their WIP copy. Consolidation would require updating those scripts and the handoff, not merely deleting the copies.
- Many selected/current stills intentionally repeat historical PNGs in versioned sets. Retain these copies to preserve selection context; git keeps identical blobs efficiently.

Suggested repository tree: current existing `app/ analysis/ audio/ coordination/ data/ design/ docs/ renders/ wip/`, plus `archive/` for historical root deliveries/snapshot. GitHub and local can then share exactly these project paths; runtime dependencies remain locally generated and ignored.
