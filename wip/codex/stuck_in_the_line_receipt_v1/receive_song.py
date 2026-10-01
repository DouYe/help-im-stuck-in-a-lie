"""Record the replacement master and update current handoff documents, without changing art/timing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parents[3]
audio = root / 'audio/current/song.mp3'
lyrics = root / 'audio/current/lyrics.txt'
text = lyrics.read_text(encoding='utf-8')
assert text.startswith('[Verse 1]\n') and text.endswith('Life outside\n')
assert len([line for line in text.splitlines() if line.startswith('[')]) == 8
assert 'Same red exit sign\n' in text and 'Then why do I feel ALIVE\n' in text
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
    'format=duration,size,bit_rate:format_tags=title,artist:stream=index,codec_name,sample_rate,channels',
    '-of', 'json', str(audio)]))
audio_stream = next(s for s in probe['streams'] if s['codec_name'] == 'mp3')
receipt = {
    'received_date': '2026-09-30', 'date_timezone': 'America/Los_Angeles',
    'recorded_utc': datetime.now(timezone.utc).isoformat(), 'song_title': 'Stuck in the Line',
    'original_filename': 'Stuck in the Line.mp3', 'original_location': 'project root',
    'canonical_audio_path': 'audio/current/song.mp3', 'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest(),
    'audio_bytes': audio.stat().st_size, 'duration_seconds': float(probe['format']['duration']),
    'codec': audio_stream['codec_name'], 'sample_rate_hz': int(audio_stream['sample_rate']),
    'channels': audio_stream['channels'], 'embedded_title': probe['format'].get('tags', {}).get('title'),
    'embedded_artist': probe['format'].get('tags', {}).get('artist'),
    'canonical_lyrics_path': 'audio/current/lyrics.txt', 'lyrics_sha256': hashlib.sha256(lyrics.read_bytes()).hexdigest(),
    'lyric_source': "Hon's exact 2026-09-30 message, not inferred from audio or ID3", 'section_blocks': 8,
    'full_audio_decode': 'passed: FFmpeg mapped audio stream 0:a:0 with no decode errors',
    'audio_modified_or_reencoded': False, 'beat_word_alignment': 'not performed; historical timing data is stale',
    'published_repository': 'https://github.com/DouYe/help-im-stuck-in-a-lie',
}
(root / 'audio/current/receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
(root / 'docs/LYRICS_STUCK_IN_THE_LINE_v1.md').write_text(
    '# Stuck in the Line — current lyrics v1\n\n'
    'Received from Hon on **2026-09-30 (America/Los_Angeles)**. This is the exact supplied text, including section labels, capitalization and the distinction between **lie** in Chorus 1 and **line** in Chorus 2/final chorus. '
    'Canonical plain text: [audio/current/lyrics.txt](../audio/current/lyrics.txt). Master: [song.mp3](../audio/current/song.mp3); provenance: [receipt.json](../audio/current/receipt.json).\n\n'
    '**No new word/beat timestamps have been established.** Historical `LYRICS.md` and `data/` remain old-master records. The lyric “Same red exit sign” is preserved verbatim; it does not by itself revise the locked palette.\n\n'
    '```text\n' + text + '```\n', encoding='utf-8')

def edit(path, old, new):
    target = root / path
    current = target.read_text(encoding='utf-8-sig')
    assert old in current, f'Missing edit anchor: {path}: {old[:60]}'
    target.write_text(current.replace(old, new), encoding='utf-8')

edit('AGENTS.md', '**Song time.** Read `docs/AUDIO_STATUS.md` first. On 2026-09-30 Hon explicitly requested deletion of the old project MP3 files and will supply a replacement later. New canonical master: `audio/current/song.mp3` (currently absent). Old `data/`, lyric timestamps, render soundtracks and Edit/Final offset notes are historical; reanalyze and realign after the replacement arrives. Do not treat the old MP3 paths as current inputs.',
    '**Song time.** Read `docs/AUDIO_STATUS.md` first. Hon supplied **Stuck in the Line** and exact replacement lyrics on 2026-09-30. Current master: `audio/current/song.mp3` (205.56 s); current text: `audio/current/lyrics.txt` / `docs/LYRICS_STUCK_IN_THE_LINE_v1.md`; hash/provenance: `audio/current/receipt.json`. Old `data/`, lyric timestamps, render soundtracks and Edit/Final offset notes are historical. New beat/word alignment is still required; do not reuse old timestamps for this master.')
edit('README.md', '**Replacement song and lyrics are pending.** Earlier MP3 masters are retired; see [audio status](docs/AUDIO_STATUS.md) before using any timing data. Hon requested publishing the existing work now and will supply the new song in a later prompt.',
    '**Current song: [Stuck in the Line](audio/current/song.mp3), received with [Hon\'s exact lyrics](docs/LYRICS_STUCK_IN_THE_LINE_v1.md) on 2026-09-30.** Earlier MP3 masters are retired; see [audio status](docs/AUDIO_STATUS.md) and [receipt](audio/current/receipt.json). New beat/word alignment remains to do; existing movie soundtracks and timing data are historical.')
edit('README.md', 'It is silent while the replacement master is pending.', 'It now reads `audio/current/song.mp3` from time zero by default; the existing visual choreography has not been aligned to this new song.')
edit('README.md', 'audio/current/       replacement master destination: song.mp3 (not supplied yet)', 'audio/current/       current song.mp3, exact lyrics.txt and hash/duration receipt.json')
edit('docs/REPOSITORY_GUIDE.md', 'The new song and lyrics are pending; old cue data and old-master references in historical documents are not current.', 'Stuck in the Line and Hon\'s exact lyrics are present in `audio/current/`; see `receipt.json` and `docs/LYRICS_STUCK_IN_THE_LINE_v1.md`. New beat/word alignment remains pending; historical cues are not current.')
edit('docs/REPOSITORY_GUIDE.md', 'While new audio is pending, an explicit silent technical capture is available:', 'For a silent technical capture, use the explicit flag:')
edit('docs/REPOSITORY_GUIDE.md', 'and stays silent while that file is missing.', 'and starts the current master at zero by default; the old visual choreography is not new-song alignment. If that file is missing, preview stays silent.')
edit('docs/FILE_MAP.md', 'forthcoming master', 'current Stuck in the Line master')
edit('docs/FILE_MAP.md', 'New master pending; eight retired MP3 removals and stale timing provenance', 'Current Stuck in the Line receipt and remaining alignment work; retired MP3/stale-timing provenance')
edit('docs/FILE_MAP.md', '| `LYRICS.md` | Historical master mapping and lyrics/timing records; await replacement lyrics |', '| `LYRICS.md` | Historical master mapping and lyrics/timing records |\n| `LYRICS_STUCK_IN_THE_LINE_v1.md` | Current exact lyrics supplied by Hon, versioned separately; not timestamped yet |')
edit('docs/FILE_MAP.md', 'Replacement master destination (`song.mp3` pending)', 'Current Stuck in the Line master (`song.mp3`), exact `lyrics.txt` and `receipt.json`') if 'Replacement master destination (`song.mp3` pending)' in (root/'docs/FILE_MAP.md').read_text() else None
edit('docs/PROMPTS.md', 'New audio/lyrics are pending;\n   old timings and old render soundtracks are historical.', 'Stuck in the Line audio/lyrics are in audio/current/;\n   new alignment remains to do, and old timings/render soundtracks are historical.')
edit('coordination/STATUS.md', '- Hon approved publishing existing content now and will supply a replacement song/lyrics in a later prompt. Canonical future master: `audio/current/song.mp3`; **currently absent**. Read `docs/AUDIO_STATUS.md` before any timing/audio work.',
    '- **Current master received: Stuck in the Line**, `audio/current/song.mp3` (205.56 s, 48 kHz stereo MP3). Hon\'s exact current lyrics are `audio/current/lyrics.txt` / `docs/LYRICS_STUCK_IN_THE_LINE_v1.md`; original filename/hash/duration are in `audio/current/receipt.json`. Receipt/upload is T30; new alignment is still T29/T4. Read `docs/AUDIO_STATUS.md` before timing work.')
edit('coordination/STATUS.md', 'not valid for the forthcoming replacement.', 'not validated for the new Stuck in the Line master.')
edit('coordination/STATUS.md', '3. When Hon supplies the replacement, place it at `audio/current/song.mp3`, save the new lyrics, record its hash/duration, redo the beat/word analysis (T29), and then plan the whole-song edit.', '3. Use the received Stuck in the Line master and exact new lyrics to regenerate beat/word analysis (T29/T4) in a new version, then plan the whole-song edit. Receipt is complete; old offsets must not be reused.')
edit('coordination/STATUS.md', '- Replacement MP3 and official replacement lyrics from Hon (later prompt). Read `docs/AUDIO_STATUS.md`; previous text/timestamps are historical.', '- New MP3 and exact lyrics have been received. Next music-dependent work is fresh alignment/analysis, not another audio request. Previous timestamps remain historical.')
edit('coordination/STATUS.md', '## Notes between models\n', '## Notes between models\n- 2026-09-30 · Codex: Hon has now supplied Stuck in the Line and full exact lyrics. Use `audio/current/` and the new lyric document. Audio bytes were preserved; full decode passed. Chorus 1 says lie, Chorus 2/final say line. No new timing, video or palette change is claimed. Earlier pending-audio notes below are historical.\n')
edit('coordination/TASKS.md', '| T29 | Add Hon\'s replacement MP3 and lyrics, record provenance and regenerate beat/word timings | waiting for Hon | — | New master at `audio/current/song.mp3`; Hon will send a later prompt. Upload existing work now. Preserve historical analysis/renders. |',
    '| T29 | Regenerate beat/word timings for Stuck in the Line and exact new lyrics | todo | — | Receipt/upload handled by T30; master and text are present in `audio/current/`. Preserve old analyses/renders and generate new versions before migration. |')
edit('coordination/TASKS.md', '| T4 | Align the whole song\'s replacement lyrics on the replacement master | waiting for new audio/lyrics |', '| T4 | Align the whole song\'s replacement lyrics on the replacement master | todo (audio/lyrics received) |')
edit('docs/DECISIONS.md', '`audio/current/song.mp3` is pending; old analysis is historical.', 'Receipt subsequently completed by T30: Stuck in the Line and exact lyrics are in `audio/current/`; old analysis is historical and new alignment remains pending.')
edit('docs/DECISIONS.md', '| A13 |', '| A15 | Current replacement song is **Stuck in the Line**, received with the exact eight-section lyric text on 2026-09-30. Keep lie/line wording and ALIVE capitalization. Upload song/text together; this receipt does not approve old timestamps for the new master or change the locked screen palette. | 2026-09-30 |\n| A13 |')

status = root / 'docs/AUDIO_STATUS.md'
old = status.read_text(encoding='utf-8')
history = old[old.index('## Retired material'):old.index('## Next audio handoff')]
history = history.replace('There is no active master in this revision.', 'That cleanup revision had no active master; the new Stuck in the Line receipt above supersedes it.')
status.write_text('# Audio status — Stuck in the Line\n\nUpdated: **2026-09-30 (America/Los_Angeles)**. Hon supplied the replacement song and exact full lyrics and requested uploading both.\n\n'
    '## Current master and lyrics\n\n'
    '- **Song:** Stuck in the Line. Original filename: `Stuck in the Line.mp3`, supplied at the project root and moved without reencoding to [`audio/current/song.mp3`](../audio/current/song.mp3).\n'
    '- **Duration/format:** 205.56 s (3:25.56), 48 kHz, stereo MP3; 4,671,453 bytes. Full audio decode passed.\n'
    f'- **SHA-256:** `{receipt["audio_sha256"]}`.\n'
    '- **Current lyric text:** [`audio/current/lyrics.txt`](../audio/current/lyrics.txt) and [`LYRICS_STUCK_IN_THE_LINE_v1.md`](LYRICS_STUCK_IN_THE_LINE_v1.md), exact text from Hon. Eight section blocks; Pre-Chorus occurs twice. Preserve Chorus 1 lie, Chorus 2/final line, quotes and ALIVE capitalization.\n'
    '- **Receipt:** [`audio/current/receipt.json`](../audio/current/receipt.json), with original filename, audio/text hashes and codec metadata.\n\n'
    '**New beat/word alignment has not been performed.** Existing `data/` and preview movie soundtracks are historical. Default portable preview now starts this master at zero; its old 20-second choreography is not evidence of synchronization with the replacement.\n\n'
    + history + '## Next audio work\n\n'
    '1. Generate new versioned beat/section analysis and forced word alignment on this master with the exact new lyric text (T29/T4).\n'
    '2. Verify those results, then deliberately migrate active app music cues/data. Preserve prior analysis rather than overwriting historical evidence.\n'
    '3. Select the intended song range before new movie editing. The prior 42.012–62.012 s / Assembly Line Heart 47–67 s ranges are not approvals for this master.\n', encoding='utf-8')

(root / 'audio/current/README.md').write_text('# Stuck in the Line — current song\n\n'
    'Received from Hon on 2026-09-30. `song.mp3` is the unchanged original `Stuck in the Line.mp3`; `lyrics.txt` is Hon\'s exact lyric message. See `receipt.json` for hashes/duration and `../../docs/AUDIO_STATUS.md` for current timing status.\n\n'
    'Beat/word alignment remains to do (T29/T4). Old movies keep historical soundtracks and must not be assumed to match this master. The portable preview reads this master from time zero by default. Audio uses Git LFS; run `git lfs pull` after cloning.\n', encoding='utf-8')
edit('使用说明.md', '你已要求删除项目内旧 MP3，因为歌曲和歌词还会变。新歌曲的固定位置是 **`audio/current/song.mp3`**，现在等你提供。你说先上传现有作品，新歌稍后再发 prompt；因此这轮交接不宣称新歌已经上传。',
    '你提供的 **Stuck in the Line** 已收到：原始 MP3 不改音频地放在 **`audio/current/song.mp3`**，时长 **3 分 25.56 秒**。这次发来的歌词原样存到 **`audio/current/lyrics.txt`** 和 [新版歌词文档](docs/LYRICS_STUCK_IN_THE_LINE_v1.md)。原文件名、哈希和时长见 [receipt.json](audio/current/receipt.json)。')
edit('使用说明.md', '新歌进来后，重新分析和对齐，再做正式剪辑。', '接下来重新分析和对齐这首新歌，再做正式剪辑。')
edit('使用说明.md', '新歌未放入时是无声预览；以后会读取 `audio/current/song.mp3`。', '现在会读取 `audio/current/song.mp3`，默认从歌曲开头播放；当前运动路线还没有与新歌节拍对齐。')
edit('使用说明.md', '真实图片、视频和以后加入的歌曲', '真实图片、视频和当前歌曲')
print(json.dumps({'title': receipt['song_title'], 'duration': receipt['duration_seconds'],
                  'sha256': receipt['audio_sha256'], 'lyrics_sections': 8, 'receipt': 'audio/current/receipt.json'}))
