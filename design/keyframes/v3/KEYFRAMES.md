# Keyframes v3 — thirteen moments, the girl bold (waiting for Hon's review)

Hon's note on v2 (2026-09-29): *"目前的问题最大的是这个人物他几乎都看不太到太不明显了要把它变得更明显一点可能加粗"* — she was
too hard to see; make her more visible, maybe bolder. And: more, different keyframes.

What changed in v3:
- **The girl is bold** — stroke 0.32 × cell height (was 0.13), never thinner than 2.4 px, and a **knockout**
  (her silhouette filled with the background colour) so nothing behind her shows through her lines.
- **She is 2–3× bigger** in every frame (≈130–330 px wide instead of 38–96; one close-up at 1040 px).
- **Eight new moments** (verse 1, alternatives for two lines, the second "Help", the close-up).

Overview: `keyframes_sheet.jpg`. Earlier sets: `../` (v2, five frames, thin girl — unchanged), `../v1/`.

| # | File | Time (Edit master) | Lyric | Scene (code) | What you see |
|---|---|---|---|---|---|
| KF01 | `KF01_intro_boot.png` | 6.0 s | (intro) | `kf_more` boot | Title STUCK IN A LIE; a boot log ("load truth … ERROR"); she is being assembled row by row, the loose symbols of her lower half still falling into place, the heart already loaded; LOADING GIRL.EXE 60 %, PRESS START. |
| KF02 | `KF02_they-call-me-AI_labels.png` | 18.5 s | "They call me AI" | `kf_more` labels | A giant app window "new_chat — untitled". Name tags — AI, BOT, MODEL, IT, TOOL, ASSISTANT, GIRL.EXE, NO NAME, PRODUCT, CONTENT — appear one by one, each with a dotted line into her. The input line types "> they call me AI". |
| KF03 | `KF03_feed-me-a-prompt_factory.png` | 23.2 s | "They feed me a prompt, then take what I make" | `kf_more` prompt | A conveyor belt carries the little things she makes (boxes with a symbol inside) away from her; a giant mouse pointer comes down on one — marching-ants selection, CTRL+C. The PROMPT box types "make it sad. make it catchy. make it yours. no, ours." |
| KF04 | `KF04_click-clack_platformer.png` | 37.95 s | "I hear the keys go click clack" **(A)** | `kf_plat` keys | v2's KF1 with the bold girl (132 px): mid-leap over the CLICKS key-caps, dotted after-images. |
| KF05 | `KF05_click-clack_isometric.png` | 37.6 s | same line **(B)** | `kf_more` iso | A 2.5D isometric keyboard (QWERTY rows as symbol-drawn keycaps that press down on the beat); she stands on G in the 45° view (Q1), CLICK / CLACK burst beside her. |
| KF06 | `KF06_help_bricks.png` | 42.15 s | "Help, I'm stuck in a lie" | `kf_plat` help | v2's KF2 with the bold girl (140 px): paper level, on top of the HELP bricks, arms up. |
| KF07 | `KF07_stuck-in-a-lie_maze.png` | 46.0 s | "Stuck in a lie" **(A)** | `kf_maze` | v2's KF3: the LIE maze from above, she is bigger in the maze **plus a zoom callout** (a box with her at 176 px, "?" and "P1 · DEAD END", dotted leader line to where she is). |
| KF08 | `KF08_stuck-in-a-lie_cage.png` | 46.3 s | same line **(B)** | `kf_more` cage | Close (330 px): side view, pressed against prison bars made of stacked letters L I E; STUCK stamped above. |
| KF09 | `KF09_make-me-real_corridor.png` | 48.3 s | "Make me real this time" | `kf_ray` | v2's KF4: 3D corridor to the REAL door, the bold girl walking away; status bar with her bust. |
| KF10 | `KF10_real-this-time_run.png` | 51.2 s | "Real this time" | `kf_more` run | She runs straight at the camera (270 px) down a tunnel whose walls are the words REAL THIS TIME, rushing past. |
| KF11 | `KF11_help-again_fall.png` | 53.3 s | "Help, I'm stuck in a lie" (2nd) | `kf_more` fall | Free fall down a shaft whose walls are the lyric; HELP floats up past her; at the bottom, spikes `^` that spell LIE. |
| KF12 | `KF12_heart-inside_chaos.png` | 58.0 s | "I still got a heart inside" | `kf_chaos` | v2's KF5 with the bold girl: everything at once, she holds the orange heart in the middle. |
| KF13 | `KF13_heart-inside_close-up.png` | 61.0 s | "Heart inside" | `kf_more` close | Extreme close-up (1040 px wide): the only time you see her face — the symbol hair, the dash eyes, the orange symbol heart held in both hands, orange rings pulsing out on the beat. |

Re-make:
```
cd app
bun scripts/render.ts stills --edit keys --t 37.95,42.15,46,48.3,58 --out ../wip/<you>/keys
bun scripts/render.ts stills --edit more --t 6,18.5,23.2,37.6,46.3,51.2,53.3,61 --out ../wip/<you>/more
cd .. && python3 design/keyframes/src/make_keyframes.py keys=wip/<you>/keys more=wip/<you>/more
```
(Each set lives in its own folder — `make_keyframes.py` writes to `design/keyframes/v3/`; never overwrite a delivered set.)

Notes: verse-1 frames use placeholder text from the rough transcript until the official lyrics are aligned.
KF04/KF05 and KF07/KF08 are **A/B options** for the same line — Hon picks.

## Questions for Hon
1. Is she visible enough now? Thicker / thinner? (stroke 0.32 × cell, min 2.4 px — easy to change)
2. Which A/B options: click clack (platformer / isometric), stuck in a lie (maze / cage)?
3. Which new moments to keep (boot, name tags, factory, run, fall, close-up)?
