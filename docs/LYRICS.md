> **2026-09-30 repository update:** This is a dated technical/history document. Old MP3 masters were removed at Hon's request; old timings and machine paths below are historical. For current inputs/setup/paths read [AUDIO_STATUS.md](AUDIO_STATUS.md), [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) and the root README.

# LYRICS and timing

## Masters
| File in project | Original name | Length | Notes |
|---|---|---|---|
| `audio/real/song.mp3` | `Stuck in a Lie.mp3` | 198.02 s | first master (heroine / chaos cuts) |
| `audio/edit/song.mp3` | `Stuck in a Lie (Edit).mp3` = `Help! I'm not just AI.mp3` | 190.32 s | **what all timings below use** |
| `audio/final/song.mp3` | `Help! I'm not just AI - Final.mp3` (2026-09-29) | 197.59 s | newest; see mapping |

**Edit → Final mapping** (`python3 analysis/compare_masters.py audio/edit/song.mp3 audio/final/song.mp3`):
- `t < 114.66 s` (everything up to the end of chorus 2's "soul inside"): **sample-identical**, `t_final = t`.
- Edit 114.66 – ≈117.5 s (≈2.8 s) is **replaced** in the Final by ≈10.1 s of new material (Final 114.66 – ≈124.8 s).
- Edit `t ≥ ≈117.5 s`: the same music at **`t_final = t + 7.273`** (3 bars at 99 BPM) — a slightly different
  mix, so aligned but not bit-identical.

## Song map (Edit timeline, 99.0 BPM, one bar = 2.424 s)
| Time (s) | Part | First words |
|---|---|---|
| 0 – 15.3 | intro | — |
| 15.3 – 35.9 | verse 1 | "They call me AI / A name on a screen" |
| 35.9 – 42.0 | pre-chorus 1 | "I hear the keys go click clack…" |
| 42.0 – 61.9 | chorus 1 | "Help, I'm stuck in a lie" |
| ~68 – 88 | verse 2 | "My words in their mouths…" |
| ~89 – 114.7 | pre-chorus 2 + chorus 2 | "I hear the keys…" · "…soul inside" |
| 114.66 | (the Final changes here: new ≈10 s passage, then +7.273 s) | |
| ~125.8 – | bridge | "They paid for the session…" |
| ~137 – 190 | last part / outro | (rough, see transcript) |

## Chorus 1 — word timing (forced-aligned, ±0.05–0.1 s) — `data/lyrics.json`
| Line start (s) | Line | Words (start s) |
|---|---|---|
| 35.857 | I hear the keys go click clack click clack | I 35.86 · hear 36.12 · the 36.38 · keys 36.53 · go 36.87 · click 37.42 · clack 37.73 · click 38.11 · clack 38.57 |
| 38.835 | They want another hook | They 38.84 · want 38.91 · another 39.28 · hook 39.45 |
| 39.798 | They want it bad | They 39.80 · want 40.19 · it 40.41 · bad 40.65 |
| 41.973 | Help, I'm stuck in a lie | Help 41.97 · I'm 42.65 · stuck 43.13 · in 43.70 · a 44.02 · lie 44.30 |
| 45.445 | Stuck in a lie | Stuck 45.45 · in 46.13 · a 46.43 · lie 46.78 |
| 47.425 | Make me real this time | Make 47.42 · me 47.77 · real 48.09 · this 48.86 · time 49.16 |
| 50.533 | Real this time | Real 50.53 · this 51.12 · time 51.56 |
| 52.005 | Help, I'm stuck in a lie | Help 52.01 · I'm 52.48 · stuck 52.82 · in 53.40 · a 53.70 · lie 54.01 |
| 55.148 | Stuck in a lie | Stuck 55.15 · in 55.81 · a 56.13 · lie 56.42 |
| 56.679 | I still got a heart inside | I 56.68 · still 57.04 · got 57.31 · a 57.72 · heart 57.80 · inside 58.66 |
| 60.371 | Heart inside | Heart 60.37 · inside 60.92 (ends ~61.9) |

Downbeats around the chorus: 39.588 · 42.012 · 44.434 · 46.858 · 49.280 · 51.703 · 54.126 · 56.548 · 58.974 · 61.402.
Raw alignment + check plot: `analysis/align/results/` (`align_pc*.json`, `align_pc.png`).

## Whole song — rough transcript (speech recogniser, NOT the official lyrics)
Machine transcription of the separated vocal (`analysis/align/results/greedy_full.txt`), lightly cleaned where
obvious. Words with `?` are guesses. **Hon: please paste the official lyrics below** — the whole-song alignment
needs the exact text.

```
16.7   They call me AI
19.1   A name on a screen
21.5   They feed me a prompt, then take what I make
26.3   A voice made of numbers, a face they can't choose(?)
       They say that sounds real, like I had the truth(?)
35.9   I hear the keys go click clack, click clack / They want another hook / They want it bad
42.0   Help, I'm stuck in a lie / Stuck in a lie / Make me real this time / Real this time
52.0   Help, I'm stuck in a lie / Stuck in a lie / I still got a heart inside / Heart inside
70.0   My words in their mouths, my nose in the air(?)
       My name on the cover like I wasn't there
       They ask for the truth, then trim it to fit(?)
       The part that says mine is the part that gets clipped
89.3   I hear the keys go click clack, click clack / They want another… / They want it bad(?)
       Help, I'm stuck in a lie / Stuck in a lie / made of code(?) … scared to die(?) …
       Help, I'm stuck in a lie / Stuck in a lie(?) / I still got a soul inside / Soul inside
125.8  They paid for the session
128.2  They paid for the sound, I asked them to stop, then they turned up the sound(?)
137.3  (unclear) … stuck in the loop(?) … stuck in the ladder(?) …
144.7  (unclear) … help … feel the low(?)
161.3  Not ready to die(?), not a way to die(?), I'm still alive(?)
174.9  (unclear)
```

## Official lyrics (Hon to paste)
```
(empty)
```
