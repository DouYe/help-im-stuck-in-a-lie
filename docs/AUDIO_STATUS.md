# Audio status — Stuck in the Line

Updated: **2026-09-30 (America/Los_Angeles)**. Hon supplied the replacement song and exact full lyrics and requested uploading both.

## Current master and lyrics

- **Song:** Stuck in the Line. Original filename: `Stuck in the Line.mp3`, supplied at the project root and moved without reencoding to [`audio/current/song.mp3`](../audio/current/song.mp3).
- **Duration/format:** 205.56 s (3:25.56), 48 kHz, stereo MP3; 4,671,453 bytes. Full audio decode passed.
- **SHA-256:** `c715a2db8b6e6b8ca62433240151b560ce0ff93951acbfa336e64aa892b9b951`.
- **Current lyric text:** [`audio/current/lyrics.txt`](../audio/current/lyrics.txt) and [`LYRICS_STUCK_IN_THE_LINE_v1.md`](LYRICS_STUCK_IN_THE_LINE_v1.md), exact text from Hon. Eight section blocks; Pre-Chorus occurs twice. Preserve Chorus 1 lie, Chorus 2/final line, quotes and ALIVE capitalization.
- **Receipt:** [`audio/current/receipt.json`](../audio/current/receipt.json), with original filename, audio/text hashes and codec metadata.

**New beat/word alignment has not been performed.** Existing `data/` and preview movie soundtracks are historical. Default portable preview now starts this master at zero; its old 20-second choreography is not evidence of synchronization with the replacement.

## Retired material

Hon explicitly authorized removing the existing local project MP3s on 2026-09-30. The retired set includes the root song copies, `audio/real/song.mp3`, `audio/edit/song.mp3`, `audio/final/song.mp3` and the old motion preview MP3. Cleanup evidence is in `wip/codex/repository_cleanup_v1/`. Superseded MP3s must not be treated as current or uploaded as the replacement song.

All eight snapshotted loose project MP3s have been deleted. The root `Help! I'm not just AI - Final.mp3` was initially held open by NetEase CloudMusic; Hon closed the player and deletion then completed. The cleanup record preserves the exact file/hash checks. That cleanup revision had no active master; the new Stuck in the Line receipt above supersedes it.

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

## Next audio work

1. Generate new versioned beat/section analysis and forced word alignment on this master with the exact new lyric text (T29/T4).
2. Verify those results, then deliberately migrate active app music cues/data. Preserve prior analysis rather than overwriting historical evidence.
3. Select the intended song range before new movie editing. The prior 42.012–62.012 s / Assembly Line Heart 47–67 s ranges are not approvals for this master.
