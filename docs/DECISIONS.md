# DECISIONS

Only Hon locks or unlocks. When Hon decides something, write it here with the date and Hon's words (short
quote; the full message goes in `PROMPTS.md`).

## LOCKED
| # | Decision | Since | Hon's words / source |
|---|---|---|---|
| L1 | On screen: **English only**, no Chinese; **no scrolling comments** | 2026-09-28 | early brief (reconstructed) |
| L2 | "Danmaku" = **things made of symbols**; everything in the picture is built from symbols | 2026-09-28 | early brief |
| L3 | Palette: ink `#0A0A0B`, bone `#EEE9DF` (+ greys `#161618` `#5E5B57` `#9C978F`) and **one orange `#FF5314`** — no other hues | 2026-09-29 | "orange only" (after the chaos cut used red) |
| L4 | **No bloom, lens flare, neon, glow, cheap particles**; clean post (scenes must return `bloom: 0, halation: 0, ca: 0` — the engine defaults are not zero) | 2026-09-29 | after the heroine/chaos cuts (reconstructed) |
| L5 | **Cuts on beats**; words appear when sung | 2026-09-29 | after the heroine/chaos cuts (reconstructed) |
| L6 | Main thread = **the symbol girl** (pixel style, made of characters), tiny, barely any expression | 2026-09-29 | "符号女孩,像素风 人物 字符" |
| L7 | Story has **both meanings**: a person stuck in a lie / an AI asking to be real | 2026-09-29 | "两层意思都有" |
| L8 | Character **style 1**: one clean unbroken line of symbols (not broken/dashed, not blocky), hair and body separate shapes, 17×27 grid | 2026-09-29 | "总体还是1最好 以这个为基调来" · "想来想去还是一吧" |
| L9 | **45° view = Q1** (face window turned, both eyes visible, one `>` nose) | 2026-09-29 | "Q1, I think is best" |
| L10 | **The heart is made of symbols** ( `/\/\` over `\  /` over ` \/ ` ), orange — never a drawn heart shape | 2026-09-29 | "用就是点线斜线什么的风格把那个心画出来" |
| L11 | Lyric timing comes from **forced alignment** of the known lyrics on the separated vocal (not estimates) | 2026-09-29 | "你可以分析一下，就是那些词是什么时候来的，然后你把它对上" |
| L12 | Keep all determined styles **saved separately** for reference (`design/`) | 2026-09-29 | "make sure to save them separately" |

## DIRECTION (agreed, details still open)
| # | Direction | Since |
|---|---|---|
| A13 | Hon says the T24 fast six-world motion revision is good and meets expectations. Keep its movement/scene-variety direction; this does not select all final shots or complete the whole music video. | 2026-09-30 |
| A14 | Organize local and publish all current work to a new **public** GitHub repository; preserve images/videos/source, remove old MP3 masters, and add the replacement song/lyrics later. The local project tree and Git checkout use the same paths. `audio/current/song.mp3` is pending; old analysis is historical. | 2026-09-30 |
| A1 | The world is a **maze / game made of symbols** that switches 2D ↔ 3D, chaotic, platformer feel (ref. "Kaizo Trap") | 2026-09-29 |
| A2 | More visual impact and variety than the seven cut, with occasional very fast changes. Later feedback narrows each still to **one clear framed scene with readable structure**; avoid both empty layouts and noise soup (R10, T20). | 2026-09-29; clarified 2026-09-30 |
| A6 | The different game-style shots must clearly feel like a **world of code**: symbols and syntax construct playable terrain, routes and hazards, beyond decorative glyph texture. Hon said the image just shown was workable, but the exact shot indicated by “这个” has not been independently confirmed; treat all new frames as proposals. | 2026-09-30 |
| A7 | During the earlier Codex still-selection phase, keep selected **still images** for reference and pause video-making. Hon's newer T23 instruction explicitly resumes a scoped platformer motion/video prototype; final scene selection remains open. | 2026-09-30 |
| A8 | **Story direction:** an awakened AI works among visually identical AI figures in a music factory; only she has the orange symbol heart. She tries to escape toward the right, repeatedly dies and respawns at the beginning, and eventually gets out. Mostly 2D platformer language, with occasional other views such as 3D; exact song mapping and scenes remain open. | 2026-09-30 |
| A9 | **Combat vocabulary:** instrument enemies (e.g. a symbol-built trumpet), glyph music-note projectiles, and lyric-word/phrase projectiles that remain readable. Fast death/restart montage is a later edit idea, roughly 10–20 deaths in 3–5 s by Hon's description of Kaizo Trap; no exact frame count approved. | 2026-09-30 |
| A10 | Keep previous picture sets. New factory/escape proposals live separately and do not replace the selected seven Codex references or other models' work. | 2026-09-30 |
| A11 | **Not only a platformer:** the factory-escape platformer is combined with many close-ups and P(doom)-style computed frames (Hon: "他不能是单是一个 platform 他有很多特写 … 这两个要想办法结合一下"); start with ~10 keyframes, not 50 ("五十张太多了") | 2026-09-30 |
| A12 | **Motion revision T24:** music-video pacing comes first; much faster near-centered girl, immediate left/right start/reverse/stop, stronger/double jumps, water/sky/overhead4-axis scenes,4+animated depths and about10incoming symbol hazards/sec. Manual play may be essentially impossible. Hon explicitly defers exact beat matching at this prototype stage; final L5 remains. | 2026-09-30 |
| A4 | **She must be clearly visible**: bold strokes + knockout + 2–3× bigger (exact weight/sizes pending review, P5) | 2026-09-29 |
| A5 | **More stylistic variety** — the frames must not all share one look. Hon to Claude: "风格太单一了"; Hon to Codex: "最好是每一帧看起来都是完全不同的游戏的感觉" (each frame like a completely different game — refs Hollow Knight, Octopath Traveler-like 2D depth, more complex scenes; still black/white/grey + orange). Two answers in progress: Claude's styles v1 (different media, P6) and Codex's game worlds v2 (T12) | 2026-09-29 |
| A3 | **Historical, superseded by A14 for new work:** old Edit/Final master mapping (identical to 114.66 s; then Edit + 7.273 s). Retain old renders and analysis as provenance; old MP3 inputs were removed at Hon's request. | 2026-09-29; superseded 2026-09-30 |


## SELECTED AS VISUAL REFERENCES (not locked final scenes)
Hon's 2026-09-30 newer instruction to Codex authorizes a **platformer motion/video prototype**: real running, jumping/dodging incoming objects, natural falling and hair inertia, and a more dynamic ending. This is a scoped motion test after A7's earlier still-only phase; final whole-song scene selection is still open. See T23 and PROMPTS.

| # | Selection | Since | Hon's words / source |
|---|---|---|---|
| V1 | Codex frames **02, 03, 04, 05, 06, 07B, 08** can be shared with other models as usable still references. Keep 07B as the code version of the heart chamber. Selection does not approve an engine scene, animation, or exact timing. See `design/keyframes/codex_selected_references_v1/`. | 2026-09-30 | "2还行吧，3也还行，4也还行，5也还行，6可以，7的话它太写实了，但是它有一个代码版，就是这个也行吧，8还行" |

## PENDING (waiting for Hon)
| # | Item | Where |
|---|---|---|
| P1 | The HUD / dialog / status-bar UI and the level types (first shown in keyframes v2, now v3) | `design/keyframes/`, `design/world/ui_kit_proposed.png` |
| P2 | Refined HELP pose (arms up in front of the hair, one `o` per eye) | `design/character/GIRL_style1_final.png` |
| P3 | Role of the two ChatGPT images (root folder) | STATUS |
| P4 | Whole-song level plan | `PROJECT_BRIEF.md` → Whole song |
| P6 | Styles v1 (8 media): Hon "都不错" (all good, 2026-09-30) — all eight stay in the pool; orange as a field colour (S1, S3) not objected to, not explicitly confirmed | `design/keyframes/styles_v1/` |
| P5 | Keyframes v3 (13 frames): the bold treatment (0.32 × cell, min 2.4 px, knockout), her sizes, the A/B options, which new moments to keep | `design/keyframes/v3/` |
| P7 | Claude's combination proposal (story v1): one world at three scales (close / game / plate) joined by her heart = the P(doom) spark; deaths leave lines that build the plate; plate lines become platforms; heart-anchored fast cuts | `design/keyframes/story_v1/STORY.md`, `story_sheet.jpg` |

## REJECTED / SUPERSEDED (don't bring these back without asking)
| # | What | Why | Date |
|---|---|---|---|
| R1 | Red (the chaos cut's red HELP screens) | palette became orange only | 2026-09-29 |
| R2 | The "seven" cut — one art style per shot (poster, engrave, sketch, flap, tape, xray, stitch) | "元素太简单了 … 没有一个主线" — too simple, no main thread | 2026-09-29 |
| R3 | Old lyric template timings | one bar early; replaced by forced alignment | 2026-09-29 |
| R4 | Character styles 2–5 (broken / dashed lines, blocky mask outlines) | "断线它断的那个太多了" — too fragmented, robotic | 2026-09-29 |
| R5 | A drawn heart shape (incl. the legacy `*` glyph) | must be symbols (L10) | 2026-09-29 |
| R6 | First 45° attempts where the eyes were lost | "看不清他的眼睛" | 2026-09-29 |
| R7 | Copying the reference sprite sheet's character | format reference only | 2026-09-29 |
| R8 | Codex game-world frame 01, cavern | "不是一个代码世界" — setting is insufficiently code-like | 2026-09-30 |
| R9 | Codex game-world frame 07, painted heart chamber | "太写实了" — keep its code/ASCII variant 07B as reference instead | 2026-09-30 |
| R10 | Grok platform_run_v1 continuous L->R runner | too messy; not a long real platformer strip; want clear framed keyframe rhythm instead | 2026-09-30 |
| R11 | GenerateImage yt_ref_shots illustration path | left locked mosaic look (became illustration); must stay Pillow glyph stamps + render() girl | 2026-09-30 |


### R3 · 2026-09-30 · scenes_50 dense direction rejected
Hon: new 50 versions basically all don't work — too chaotic / noisy / meaningless clutter. Want beauty; original simple look felt cute and calm, not noisy. Generate 55 frames in OTHER styles.
Outcome: T14 / `wip/new-bot/scenes_50/` rejected (kept as archive). T15 `wip/new-bot/styles_55_calm/` delivered for review (calm / cute / readable, generous negative space).

### R4 - 2026-09-30 - platform_run_v1 continuous-runner rejected
Hon: too messy; not a long real platformer strip. Want ORIGINAL keyframe rhythm: ONE clear framed scene per still, strong STRUCTURE, readable forms (door/maze/platform/factory room) at a glance + cute girl escaping AI world. Not chaos (scenes_50), not empty (styles_55), not continuous runner.
Outcome: T19 / wip/new-bot/platform_run_v1/ rejected (kept as archive). T20 wip/new-bot/clear_shots_v1/ delivered for review (8 clear framed stills).

### R5 - 2026-09-30 - GenerateImage yt_ref rejected; clear_shots too plain; mosaic_dense_v1
Hon: GenerateImage yt_ref_shots left the locked mosaic look (became illustration). Want pixel/character mosaic via Pillow + locked girl render(), same as clear_shots_v1 — NOT image-gen. clear_shots_v1 too plain; need denser YouTube-platformer still composition while keeping one readable scene per frame.
Outcome: yt_ref GenerateImage path rejected (R11). T20 clear_shots_v1 kept as archive reference (too plain). T21 wip/new-bot/mosaic_dense_v1/ delivered for review (8 denser mosaic stills).

