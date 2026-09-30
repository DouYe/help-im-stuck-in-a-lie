> **2026-09-30 repository update:** This is a dated technical/history document. Old MP3 masters were removed at Hon's request; old timings and machine paths below are historical. For current inputs/setup/paths read [AUDIO_STATUS.md](AUDIO_STATUS.md), [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) and the root README.

# PIPELINE — how the video is built, run and rendered

Engine: adapted from the "I'm Upping My P(doom)" video (github.com/mexicat/pdoom-video, MIT — see
`LICENSE.pdoom-engine`). **Every frame is a pure function of song time**: the page draws time *t* with three.js
+ Canvas2D, a headless Chrome steps through the times, ffmpeg encodes. Everything specific to this song is new.

## 1. Set up a machine
| Need | For | Notes |
|---|---|---|
| **Bun** (bun.sh) | dev server, bundler, render script | `cd app && bun install` (three 0.186, opentype.js, playwright-core) |
| **Google Chrome** | rendering | found via Playwright `channel: 'chrome'`, or set `CHROME_PATH` |
| **ffmpeg** | video encode, audio conversion | on PATH |
| **Python 3** + numpy, scipy, matplotlib, Pillow | analysis, sheets | `pip install numpy scipy matplotlib pillow` |
| onnxruntime | lyric alignment only | `pip install onnxruntime` |
| Models (lyric alignment only) | vocal separation, CTC | `UVR-MDX-NET-Voc_FT.onnx` — github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR-MDX-NET-Voc_FT.onnx · `sherpa-onnx-zipformer-ctc-en-2023-10-02` — github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-zipformer-ctc-en-2023-10-02.tar.bz2 · point env `MDX` and `CTC` at them |

Large generated audio (`audio/*/song_stereo.wav`, `vocals*.wav`, `instrumental.wav`) and the analysis caches
(`analysis/*.npz`) are **not** in the shared folder — regenerate them (below).

## 2. Preview and render
```
cd app
bun scripts/serve.ts 5173
#   browser: http://localhost:5173/?edit=keys&t=46   (space = play; &edit= picks the edit)
bun scripts/render.ts stills --edit keys --t 37.95,42.15,46,48.3,58 --out ../wip/<you>/stills
bun scripts/render.ts sheet  --edit keys --from 35.5 --to 62 --n 12 --cols 4 --out ../wip/<you>/sheet.png
bun scripts/render.ts video  --edit keys --from 35.5 --to 62 --samples 12 --shutter 0.3 --fade-audio --out ../renders/<date>_chorus1_<you>.mp4
```
- `--samples N --shutter S` = motion blur (N sub-frames). 4 is fine for checks; 12 for finals (GPU machine).
- `--audio audio/final/song.mp3` muxes the Final master instead of the Edit (identical before 114.66 s).
- `--scale 2` renders 4K. Without `--url` the script starts its own server.
- Output is 1920×1080, 60 fps by default (`--fps`).

## 3. Where things are in the engine (`app/src/`)
| Path | What |
|---|---|
| `edit.ts` | **The edits.** Each edit = a list of cuts `{ when, mode, params, transition }` + a range. Edits: `keys` (keyframes v2/v3 chorus scenes, **the default**), `more` (keyframes v3 new moments, 0 s → bar 26), `game` (old platformer WIP), `seven`, `heroine`, `chaos`. `when` can be `{ line: 'Stuck in a lie', nth }`, `{ bar: N }` (0-based downbeat index; the HUD shows N+1; chorus 1 = bar 17 = 42.01 s) or `{ t: seconds }`; cuts snap to the beat at/before a line's first word. Same mode twice in a row = one continuous shot with cues. |
| `timeline.ts` | turns an edit into engine entries (merges same-mode cuts, overlaps neighbours for transitions) |
| `scenes/kf_plat.ts` | 2D platformer — `variant: 'keys'` (KF1, CLICKS key-caps) and `'help'` (KF2, paper level, HELP bricks) |
| `scenes/kf_maze.ts` | KF3 — top-down maze whose cells spell LIE, lamp light, trail, minimap |
| `scenes/kf_ray.ts` | KF4 — GLSL raycaster corridor of symbol walls, REAL door, Doom-style status bar |
| `scenes/kf_chaos.ts` | KF5 — three torn strips (platformer / tunnel / maze), row-slip glitch, HEART, her with the heart |
| `scenes/kf_more.ts` | keyframes v3 moments, `variant:` `boot` · `labels` · `prompt` · `iso` · `cage` · `run` · `fall` · `close` (edit `more`); helpers `symSeg` / `symPoly` (lines and polygons drawn as symbols) and `tag` |
| `game/girl.ts` | **the girl's rig** (port of `design/character/src/vgirl.py`): `pose(name, t)`, `turn(f)`, `above()`, `raster()`, `drawGirl(pen, pose, t, x, y, w, opts)` — bold by default (`GIRL_LW` 0.32, `GIRL_MIN_PX` 2.4) with a knockout (`opts.knock`: background colour, or `false` for ghosts) |
| `game/glyph.ts` | the symbol alphabet + `GlyphPen` (batched Canvas2D strokes); mirrors `glyphs.py` |
| `game/world.ts` | colours `C`, symbol heart, far field, big maze, `symBox`, `hud()`, `dialog()`, `brickWord()`, `outlineWord()` |
| `game/pixfont.ts` | 5×7 and 3×5 pixel fonts for words-as-geometry |
| `game/sprite.ts`, `girl.txt`, `girl_frames.ts`, `gen_frames.py` | **legacy** first hand-typed ASCII sprite (only the old `plat` scene uses it) — don't use |
| `danmaku/mode.ts`, `transition.ts` | base class of every scene (`draw(f, out)` returns post overrides; `wordsIn`, `linesIn`, `cue`, `param`); universal transitions `wave`, `sweep`, `dive`, `fade`, `cut`, `through` |
| `engine/` | renderer, post, GL helpers (`FSPass`, `Layer2D`), audio data access (`audio.hit('kick', t)`, beats), lyrics |
| `scenes/*.ts` (others) | earlier cuts: poster, engrave, sketch, flap, tape, xray, stitch (seven); maze, portrait, heart, help, tunnel, slam, storm, bars, swarm, polygraph, cage (heroine / chaos); plat (old) |
| `scripts/serve.ts` | Bun dev server (+ `import.meta.glob` shim); serves `/audio` and `/data` from the project root |
| `scripts/render.ts` | stills / sheet / plates / perf / video |

Add a scene: create `app/src/scenes/<name>.ts` extending `Mode` (see `kf_maze.ts` for a compact example); it is
picked up automatically by file name; use it in an edit as `mode: '<name>'`.
⚠ **Return `{ bloom: 0, halation: 0, ca: 0, grain: ~0.03, vignette: ~0.2 }` from `draw()`.** The engine's post
defaults (`engine/post.ts`) have bloom 0.55, halation 0.25 and chromatic aberration 1.2, which break the locked
no-glow look.

## 4. Music analysis (`analysis/`)
```
ffmpeg -i audio/edit/song.mp3 -ac 2 -ar 44100 audio/edit/song_stereo.wav
SONG=edit python3 analysis/analyze_song.py       # beats, downbeats, sections, envelopes, onsets -> data/audio.edit.json
SONG=edit python3 analysis/finalize_real.py      # beat grid nudged to the drums -> data/audio.json
```
⚠ `finalize_real.py` **also rewrites `data/lyrics.json` with the OLD template** (one bar early). Back up
`data/lyrics.json` first, or re-run `analysis/align/write_lyrics.py` afterwards (step 5).
`data/audio.json` is what the app reads (99.0 BPM; beats, downbeats, 100-fps envelopes rms/low/mid/high/vocal/
drums/bass/other, onsets). Note: its `sections` field is the old estimate — chorus 1 really starts at the
42.01 s downbeat (see `LYRICS.md`). `analysis/compare_masters.py A.mp3 B.mp3` shows where two masters are
identical and how times map across (Edit vs Final: `LYRICS.md`); `analysis/map_edit.py` is the older, hard-coded
Real → Edit version.

## 5. Lyric forced alignment (`analysis/align/`)
```
SONG=edit MDX=<path>/UVR-MDX-NET-Voc_FT.onnx python3 analysis/align/separate.py
#   -> audio/edit/vocals.wav, vocals_16k.wav, instrumental.wav
CTC=<path>/sherpa-onnx-zipformer-ctc-en-2023-10-02 python3 analysis/align/ctc_align.py 33.5 63.5 \
  "I hear the keys go click clack click clack|They want another hook|They want it bad|Help, I'm stuck in a lie|..." > align.json
SONG=edit python3 analysis/align/refine.py align.json refined.json check.png   # snap to vocal onsets, plot to check
python3 analysis/align/write_lyrics.py refined.json                           # -> data/lyrics.json
```
- `separate.py`: UVR-MDX-NET-Voc_FT in onnxruntime (n_fft 7680, hop 1024, dim_f 3072, dim_t 256, compensate
  1.021, averaged with the inverted pass).
- `ctc_align.py <t0> <t1> "line|line|…"`: kaldi-style 80-bin fbank in numpy → zipformer2 CTC log-probs → words
  split into the model's BPE pieces → Viterbi forced alignment.
- `refine.py`: each word start snapped to the nearest vocal spectral-flux onset in [ctc − 0.28, ctc + 0.10] s;
  end = last frame above 25 % of the word's peak. Accuracy ≈ ±0.05–0.1 s.
- Needs the **exact lyric text**. For the rest of the song, get the official lyrics from Hon first (task T4).

## 6. Switching to the Final master (task T3)
```
ffmpeg -i audio/final/song.mp3 -ac 2 -ar 44100 audio/final/song_stereo.wav
SONG=final python3 analysis/analyze_song.py   # -> data/audio.final.json
```
Before 114.66 s the two masters are sample-identical, so beats and chorus-1 lyrics carry over unchanged. After
it the Final has a new ≈10 s passage, then the Edit's music 7.273 s later — re-check the grid there.
`finalize_real.py` hard-codes the Edit's section bars and the old lyric template (and overwrites
`data/lyrics.json`): adapt it for Final rather than running it as is. Align the rest of the lyrics directly on
the Final (T4). Finally point the app at `audio/final/song.mp3` (`app/src/main.ts` loads `audio/edit/song.mp3`;
`render.ts --audio` sets the muxed track).

## 7. Design sheets (Python)
```
python3 design/character/src/final_sheet.py     # -> design/character/GIRL_style1_final.png
python3 design/world/src/world_sheets.py         # -> design/world/palette.png, symbols.png, ui_kit_proposed.png
python3 design/keyframes/src/make_keyframes.py wip/<you>/keyframes   # rendered stills -> KF1…KF5 + sheet
```
The girl exists twice — `design/character/src/vgirl.py` and `app/src/game/girl.ts`. Keep them identical.

## 8. Working from a cloud sandbox
Copy the folder in (or the parts you need), work, then copy every changed file back to the PC folder and log
it. Never leave the only copy of anything in a sandbox.
