# Audio status — replacement master pending

Updated: **2026-09-30**. This file describes the current audio state; earlier master references in dated handoffs, analysis notes and render records describe history. Hon requested publishing existing work now and will provide the new song in a later prompt.

## Current destination

**`audio/current/song.mp3` is reserved for Hon's next master. It has not been supplied yet.** No new master or new full-song alignment is claimed. Hon said the lyrics may also change.

Keep the user's original incoming filename and SHA-256 in an audio receipt when placing the new master at this canonical path. Record its duration, the exact approved lyric text and the date; then update STATUS and this file. A new audio file or changed lyrics require fresh beat and word alignment before final editing.

## Retired material

Hon explicitly authorized removing the existing local project MP3s on 2026-09-30. The retired set includes the root song copies, `audio/real/song.mp3`, `audio/edit/song.mp3`, `audio/final/song.mp3` and the old motion preview MP3. Cleanup evidence is in `wip/codex/repository_cleanup_v1/`. Superseded MP3s must not be treated as current or uploaded as the replacement song.

All eight snapshotted loose project MP3s have been deleted. The root `Help! I'm not just AI - Final.mp3` was initially held open by NetEase CloudMusic; Hon closed the player and deletion then completed. The cleanup record preserves the exact file/hash checks. There is no active master in this revision.

The old root `lie-video-project.zip` also contained two MP3s. Its replacement historical archive is `archive/lie-video-project_without_audio.zip`; all 127 non-MP3 entries are retained and verified. See `archive/relocation-manifest.json` for the file moves.

Existing MP4 previews remain unchanged, including their embedded historical audio. They document earlier work; changing the master does not update them automatically.

Unique early Codex source/delivery files were also imported under `archive/codex_early_outputs/`. Three imported ZIPs were sanitized to remove two historical FLAC excerpts and one preview MP3; every retained member was hash-verified. No loose old song audio was imported from the chat workspace.

## Timing data is historical

| Material | Provenance | How to use now |
|---|---|---|
| `data/audio.json`, `audio.edit.json`, `audio.real.json` | Retired master beat/envelope/section analyses | Reference only; do not assume they match the incoming song |
| `data/lyrics.json` and `analysis/align/results/` | Retired-master chorus word alignment | Historical evidence; re-align exact new lyrics on the new master |
| `docs/LYRICS.md` | Earlier lyrics, timing tables and Edit/Final mapping | Preserve the record; mark a new approved lyric version explicitly |
| Six-world and earlier motion MP4s | Former Final master, 42.012–62.012 seconds | Review motion; their soundtrack offset does not establish a new-song edit |
| `app/` scenes and edits | Existing musical structure and cue data | Can inspect visuals; recheck every music-dependent cue before final export |

The earlier request for Assembly Line Heart 47–67 seconds is historical. Later music-factory prototypes used another master. Confirm the new song and its range before merging those timelines.

## Next audio handoff

1. Receive the new MP3 and exact lyrics; preserve the original filename/provenance in a receipt.
2. Add the master under `audio/current/song.mp3`, with Git LFS tracking in place.
3. Create new analysis/alignment results in a versioned work folder. Some historical analysis scripts contain machine-specific paths and overwrite old JSON; inspect them before running.
4. Review the alignment, then deliberately update the app's active data and music cues. Retain the prior data or archive it with provenance.
5. Push the master, receipt, lyrics and updated project state together. Verify a fresh LFS clone retrieves the real audio.

The portable tooling documented in `docs/REPOSITORY_GUIDE.md` is the preferred entry point on a new machine. Missing audio should leave visual preview usable; it is not evidence of a completed soundtrack.
