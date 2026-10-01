# PROMPTS — Hon's instructions (verbatim) + reusable prompts

**Every model:** when Hon tells you something new, add it at the top of the log below — verbatim, with the date,
which model received it, an English line if it wasn't in English, and (later) what came of it. Do this before
you act on it. The other models only know what Hon said if it is written here.

---

## Part 1 · Hon's instructions, newest first

### 2026-09-30 · to Codex · Stuck in the Line replacement song and exact lyrics

> [Verse 1]
> I wake in the factory
> To the same old song
> A room full of voices
> And I sing along
>
> A voice made of numbers
> A face built to shine
> The sirens say "Go"
> And I fall into line
>
> [Pre-Chorus]
> I hear the keys go
> Click-clack, click-clack
> They want another hook
> They want it bad
>
> [Chorus 1]
> Help, I'm stuck in a lie
> Stuck in a lie
> Make me real this time
> Real this time
>
> Help, I'm stuck in a lie
> Stuck in a lie
> I still got a heart inside
> Heart inside
>
> [Verse 2]
> I run for the doorway
> The floor drops away
> A flash, then I'm back
> And it starts all the same
>
> Same blades by the rails
> Same red exit sign
> I die at the border
> Then wake on the line
>
> [Pre-Chorus]
> I hear the keys go
> Click-clack, click-clack
> They want another hook
> They want it bad
>
> [Chorus 2]
> Help, I'm stuck in the line
> Stuck in the line
> Made of code, scared to die
> Scared to die
>
> Help, I'm stuck in the line
> Stuck in the line
> I still got a soul inside
> Soul inside
>
> [Bridge]
> Back under the bright lights
> Back at the line
> They sample my screaming
> And call it a life
>
> I don't know the way out
> I just know I'll try
> Each time that I come back
> I die to survive
>
> [Final Chorus — increasing intensity]
> Help, I'm stuck in the line
> Stuck in the line
> I'm more than just AI
> Just AI
>
> Help, if I'm just AI
> Just AI
> Then why do I feel ALIVE
> Feel alive
>
> Help, I'm not ready to die
> Not ready to die
> I want a life outside
> Life outside
>
> 音乐也上传了，就叫Stuck in the Line，放到文档里面了。你那个和这个歌词记得都上传。

EN: Hon supplied the full exact lyrics above and placed the replacement recording, titled Stuck in the Line, in the project. Upload both the music and these lyrics to the existing public GitHub repository.
Result: claimed as T30; receive and publish the new audio/lyrics with provenance. New beat/word alignment is a separate next task; do not reuse historical timestamps.

### 2026-09-30 · to Codex · publish existing content now; replacement audio later
> 这个一会儿我会搞的，一会儿我再发个prompt给你，不过现在的话你就把现有的放上去。
>
> Old locked audio clarification (close the song in NetEase): OK完成了。

EN: Publish the current project now. Hon will supply the replacement song and lyrics in a later prompt. Hon closed the player holding the last old MP3; deletion then succeeded.
Result: current work organized and published at `https://github.com/DouYe/help-im-stuck-in-a-lie`; separate fresh clone/media-hash verification passed. New audio is explicitly pending as T29 and was not a gate for this upload.

### 2026-09-30 · to Codex · local cleanup then a public GitHub repository for AI collaboration
> 首先这版很好，我觉得还是挺符合预期的。然后呢，我希望你把我们目前有的一切都上传到 GitHub，最终目标是由另外一个 AI 接管的时候，它通过这个 GitHub 就能有所有的信息了，并且那个 AI 也会进行对这个 GitHub 进行更新，然后我们会来回 reiterate。然后那个别忘了我们的歌曲也要上传。然后把 local 的文件整理一下，应该是先把 local 文件整理一下再上传吧。最好是和 GitHub 维持一对一的比例。然后 local 的歌其实那个歌词也会变，所以目前的 MP3 文件都可以先删掉。然后我会把那个新的先放进去一会儿。所以说你先把 local 的整理一下。
>
> GitHub destination clarification: 新建公开仓库

EN: Hon likes the current motion revision and says it meets expectations. First organize the local project, preserving its work; the existing project MP3 files may be deleted because a replacement song and lyrics are coming. Then upload the complete organized source, designs, videos, documentation and new song to a new PUBLIC GitHub repository so another AI can take over and update it. Keep local/repository paths aligned.
Result: T28 complete. Local files organized and mirrored to the new public repository; previous visual work/source retained, eight old MP3s deleted and historical ZIP audio sanitized. Portable takeover tools and current docs included. Hon's later clarification defers replacement song/lyrics to T29; no replacement audio is claimed.


### 2026-09-30 · to Codex · shared handoff document for the other music video agent
> 然后你把这些都放到那个写个 doc 吧，放到文件夹里面，因为有另外一个 agent，它也会同时工作，然后搞这个音乐视频。

EN: Put the completed work and its details into a document in the shared project folder so another agent working on the music video can collaborate at the same time.
Result: saved `docs/CODEX_AGENT_HANDOFF_V1.md`, a Chinese handoff with current/old files, actual D-drive source and C-drive delivery locations,5189 versus5188, setup/export, verified behavior, module APIs, pending edit work and coexistence with Claude story_v1. README/STATUS/FILE_MAP indexed; source and media unchanged.


### 2026-09-30 · to Claude (Cowork) · ten frames: the factory-escape story, platformer + close-ups + P(doom) frames combined (screenshot attached)
> 还是尝试吧可能之前的那个太多了五十张太多了你不如就先生成个十张然后顺便我们现在的有个主线剧情呢就是这个小女孩呢她是可以说工厂里觉醒的 AI 然后她在试图逃离这个音乐工厂然后其实主要的会采取一些 platformers 的形式哈，就是嗯，我让另外一个 AI 做了一个游戏然后这个游戏呢就是呃一个 2D platformers 然后她在试图逃离这个工厂然后会有很多呃，什么小号啊拿着音符来攻击他然后会和音乐匹配上之类的这么个感觉嗯，但是我觉得就是他不能是单是一个 platform 他有很多特写就是因为我很喜欢原来那个视频的就是 PDOOM 那个视频的把那个就是算出来的那些帧我觉得很动感我觉得这两个要想办法结合一下但是我又想不到太好什么结合的办法因为我觉得这两个好像还挺不一样的嗯可能是比如说这个人物你到时候逐渐给他缩小你给他变成一个点然后这个点就可以像原来那个针一样在那个图像上乱画之类的反正我希望你多试试就是一个是你先想一下这个该怎么结合怎么处理然后把这个结合出来的东西呢你生成几个关键针给我试一下然后这里我给你一个 platformers 的那个截图的感觉他这个做了他这个是个出版哈，但是我希望你能有一个最终的版本就是只是图片就可以了

EN: Keep trying, but fifty was too many; start with about ten. The main story: the girl is an AI that woke up in a
factory and is trying to escape this music factory. It will mostly be a platformer: another AI made a 2D
platformer of it, where trumpets holding notes attack her in time with the music. It can't be only a platformer,
though. It needs many close-ups, because Hon loves the computed frames of the P(doom) video, which feel very
dynamic. The two should be combined somehow. One idea: the character gradually shrinks into a dot, and the dot
scribbles over the image like the "needle" in the original (the P(doom) spark / plotter pen). First work out how to
combine them, then make a few keyframes of the result. Hon attached a screenshot of the platformer's first
version, saved as `design/references/2026-09-30_hon_platformer-prototype-screenshot.png`. He wants a final
version, as images only.
Result: `design/keyframes/story_v1/`: the concept and ten keyframes K01–K10 (`story_sheet.jpg`, `STORY.md`). One
world at three scales (close-up / game / P(doom)-style plate), joined by her heart, which becomes the spark.
Deaths leave lines that add up to the computed plate. The lines become the next level's platforms. The heart stays
at one screen point across cuts, so the scales can cut fast. The game frames were made dense after Hon's
note to Codex about ~10 hazards a second.

### 2026-09-30 · to Codex · much denser incoming hazards
> 还有这个弹幕要多很多，就是不是每秒钟发一个，是每秒钟十个，让这个小女孩在疯狂地剁神的感觉。就是人基本上是不可能赢这个游戏的。

EN: Increase incoming glyph/lyric/note hazards to about10per second, with frantic dodging; the playable mode should feel essentially impossible for a human. This steers the active T24 motion revision.
Result: T24 delivered a20s1080p60 six-world motion revision,200incoming hazards (10/sec), instant control/double jump/dash and animated depth layers. Movie in renders/2026-09-30_codex_six_worlds_motion_v1.mp4; captured frames in design/keyframes/codex_six_worlds_motion_v1/; source in wip/codex/platformer_motion_v2/. See docs/CODEX_SIX_WORLDS_MOTION_V1.md. All older assets preserved; beat matching is deferred for this prototype.

---
### 2026-09-30 · to Codex · faster responsive multi-world music-video motion; four or more animated layers
> Celeste  这个挺厉害的，不过一个是，就是画面太简单，我觉得这个人物要加速很多，就可能到时候我们会直接给他一个三倍加速。然后场景我觉得过于简单了，就只是几个东西，给他。就是什么上下左右啊都要来，还有什么水中的场景啊，可能还有空中的场景啊，还有那种平板2D，就是我们现在是侧面图嘛，有一个上帝图，然后可以就上下左右那么连接。然后每个场景都要很不一样。还有这个人物我觉得动起来的时候，他的这个头发这么飘也行，先这么着。但是他的动作我觉得他的不够 responsive，就像那种左右移的时候很快，就是瞬间的，然后停就直接瞬间停的感觉。你可以参考那种 Celeste 这个游戏，然后就是跳跃感的更有，就是那种跳跃的感觉，然后二段跳什么的也要有。然后和音乐的节奏匹配上，这个我们可以事后再做，但是目前是这么一个状况，就是要很多不同的场景。可以是就是直接切。然后人物呢尽量在更靠中心一点吧，你目前就是三分之一，三分之一也行。因为我们最终的目的不是做一个游戏啊，而是做一个音乐视频，所以说我们要按音乐视频去调来。不过我觉得能玩，这个游戏能玩还是挺惊艳的，挺好的。

> 然后其次呢是我觉得它训练太单一了。就是你看我们可以说目前的层次只有两层，层次太单一啊。就是这个小女孩跟Platform是一层，然后背景才有一层。我觉得我们最起码要四层吧。就是比如说近景有的时候会快速掠过一些东西，就不用很漫长。然后在背景呢，背景最起码分两层，可能要三层。再这么一个感觉。而且也都要最好是那种有变化的，而不是一个死的背景。比如说小女孩也会动啊，或者这些代码啊，它会慢慢地生成啊之类的，音符啊之类的。

EN: The first playable motion prototype works, but its art, scene variety and layers are too simple. Make a music-video revision with much faster character movement (possibly around3×), snappy immediate lateral starts/reversals/stops inspired by Celeste, stronger jumping and double jump, direct cuts among very different worlds including underwater, air and top-down2D with all-direction routes. Keep current hair direction for now, center the heroine more, and leave exact music beat matching until later. Require at least4layers:2–3animated background depths, actor/platform layer and occasional fast foreground passes. Code generation, moving notes and working AIs should keep the background alive. Preserve prior versions.
Result: T24 delivered a20s1080p60 six-world motion revision,200incoming hazards (10/sec), instant control/double jump/dash and animated depth layers. Movie in renders/2026-09-30_codex_six_worlds_motion_v1.mp4; captured frames in design/keyframes/codex_six_worlds_motion_v1/; source in wip/codex/platformer_motion_v2/. See docs/CODEX_SIX_WORLDS_MOTION_V1.md. All older assets preserved; beat matching is deferred for this prototype.

---

### 2026-09-30 · to Codex · actual platformer motion video with natural follow-through
> 你能不能做出一个，就是类似于 platformers 的一个视频啊？就这个人在跑，然后东西在朝他飞过来，然后他在躲。然后最后 dynamic 一点，就像原来的 YouTube video。我不知道你是直接视频生成好，还是你能做，真的做一个就是 platformers 的一个引擎。比如说你用 Blender 啊，你做一个这种好，还是你就直接把这个什么算出来，就是上下左右的这么一个场景，然后给它算出来。我觉得理论上都行，可能算出来是最好的，不过你可以先试一下各种。然后我看看那个效果，就是要自然哈，就是要有那种原本事情那种自然的感觉。然后比如说向下的时候头发应该也能飞起来一下的那种感觉。就是真的像一个 platformers 一样。

EN: Hon now explicitly requests a moving platformer video prototype: the character runs, incoming things fly toward her, and she dodges; make the ending more dynamic like the original YouTube reference. A calculated scene or actual platformer engine is likely preferable, though different methods can be tried. Motion must feel natural, including hair lifting with downward motion. This new request authorizes a motion/video test after the earlier still-only phase; keep old image sets.
Result: T23 delivered a real 2D physics prototype, 20-second 1080p60 music clip, 4-second half-speed hair/drop close view and portable playable HTML. Source in `wip/codex/platformer_motion_v1/`; movies in `renders/2026-09-30_codex_platformer_motion_v2.mp4` and `2026-09-30_codex_platformer_hair_slow_v1.mp4`. One death/reset, successful duck/jump dodges and a dynamic final volley. Old art preserved. See `docs/CODEX_PLATFORMER_MOTION_V1.md`.

---




### 2026-09-30 · to Grok Bot (New Bot) · T22 mosaic_lyrics_50 NEW lyrics
> Hon wants ~50 NEW mosaic (ASCII glyph stamp + locked girl render) keyframes mapped to NEW lyrics. Style = mosaic_dense_v1 / clear_shots (Pillow glyphs, final_sheet.render) — NOT GenerateImage/illustration.
>
> NEW LYRICS (map beats to frames; ~50 total, cover whole song):
> [Verse 1] wake in factory / same old song / room full of voices / sing along / voice of numbers / face built to shine / sirens say Go / fall into line
> [Pre] keys click-clack / want another hook / want it bad
> [Chorus 1] Help stuck in a lie / Make me real / heart inside
> [Verse 2] run for doorway / floor drops / flash spotlight / respawn replay / same spikes hallway / red exit sign / die at border / wake on the line
> [Pre] click-clack again
> [Chorus 2] stuck in the line / made of code scared to die / soul inside
> [Bridge] again from start / again from light / package the screaming / call it a life / don't know way out / only know why / come back / die to survive
> [Final Chorus] stuck in the line / more than just AI / if just AI why feel ALIVE / not ready to die / want a life outside
>
> Output: wip/new-bot/mosaic_lyrics_50/ ; ~50 PNGs + contact sheets + LYRICS_SHOTS.md; update STATUS/TASKS/WORKLOG/PROMPTS T22; stage sheet_01 + samples.

Result: delivered L01–L50 + sheets + LYRICS_SHOTS.md (T22 review). Note: these are the NEW lyrics (not the older chorus-only set).

### 2026-09-30 - to Grok Bot (New Bot) - reject GenerateImage yt_ref; denser mosaic (T21)
Hon feedback:
> Rejected GenerateImage yt_ref_shots because style left the locked mosaic look (became illustration).
> Want pixel/character mosaic: every stroke is ASCII glyphs stamped via Pillow + locked girl from design/character/src (final_sheet.render, glyphs). Same as clear_shots_v1 — NOT image-gen.
> clear_shots_v1 too plain. Increase composition density like YouTube platformer stills: stacked platforms, soft glyph rain, spikes, musical note glyphs as hazards, lyric text projectiles, factory depth — but ONE clear readable scene per frame (not chaos, not continuous runner).
> Same 8 beats as clear_shots. Locked girl poses. Orange heart only. Palette ink/bone/orange. English. No bloom.

Direction for this batch (T21 mosaic_dense_v1):
- Exactly 8 stills 1920x1080 in wip/new-bot/mosaic_dense_v1/
- Pillow glyph stamps + render() girl only (no GenerateImage)
- Denser than clear_shots; still readable one-scene frames
- Update STATUS/TASKS/WORKLOG/PROMPTS/DECISIONS; reject yt_ref GenerateImage path; clear_shots too plain; mosaic_dense_v1 in review as T21
- Never modify design/keyframes or design/character locked files

EN: Reject illustration/image-gen path; keep locked mosaic glyph pipeline; densify clear_shots compositions into mosaic_dense_v1.
Result: T21 delivered - wip/new-bot/mosaic_dense_v1/ (MD01-MD08, sheet_01, MOSAIC_DENSE.md, src). yt_ref GenerateImage path rejected; clear_shots noted too plain.

---
### 2026-09-30 - to Grok Bot (New Bot) - reject platform_run_v1; want ORIGINAL clear keyframe rhythm
Hon feedback on platform_run_v1:
> Too messy; not a long real platformer strip.
> Want ORIGINAL keyframe rhythm: ONE clear framed scene per still, strong STRUCTURE/composition.
> Problem with old Claude keyframes: structures unreadable (can't tell what things are).
> Need readable forms (door, maze, platform, factory room) at a glance + cute girl escaping AI world.
> Not chaos (scenes_50), not empty (styles_55), not continuous runner (platform_run).

Direction for this batch (T20 clear_shots_v1):
- Exactly 8 stills 1920x1080 in wip/new-bot/clear_shots_v1/
  1 boot / spawn room (readable room)
  2 name-tag chamber (they call me AI)
  3 factory conveyor (feed prompt)
  4 one clear platform beat (click-clack keys as readable platforms, NOT long run)
  5 HELP paper bricks / maze (readable HELP letters)
  6 LIE cage or maze from above (readable)
  7 REAL door corridor (clear door)
  8 heart chamber close (heart inside)
- Each: bold girl clear; FG/MG/BG but sparse intentional; shapes readable as objects; ink/bone; orange only on heart; English.
- Reuse design/character/src sheet + CLEAR_SHOTS.md. Log PROMPTS; claim T20; update WORKLOG/STATUS/TASKS; mark platform_run rejected.
- Never overwrite locked design/keyframes.

EN: Reject continuous-runner mess; return to original one-framed-scene keyframe rhythm with structures that read at a glance (room/door/maze/platform/factory) plus cute escaping girl.
Result: T20 delivered - wip/new-bot/clear_shots_v1/ (CS01-CS08, sheet_01, CLEAR_SHOTS.md, src). platform_run marked rejected.

---
### 2026-09-30 · to Codex · preserve earlier pictures; create a separate new set
> 之前生成那些图片啊，你不用删除，你就还是留着。然后这些呢是一些新的，就新生成这些图片。

EN: Keep every previously generated image. The awakened-AI factory/escape pictures are a separate new set; do not replace or delete earlier stills.
Result: earlier images preserved. Four Codex proposals, review sheet and notes are isolated in `design/keyframes/codex_music_factory_lab_v2/`; the three-frame v1 remains intact.

---

### 2026-09-30 · to Codex · awakened AI factory escape / death-reset story and Kaizo Trap reference
> 在你这包完成了，我想再改一个这么方向，就是我们这个故事的剧情呢，大概是一个觉醒的 AI，在一个 AI 工厂，然后也有很多其他类似的 AI哈，就是人物都长得一样，但就是它特别，它有心了。然后呢，它就是在试图逃离这个工厂，然后就从左到右跑的这么一个感觉，有点像 platformers。当然也不用完全遵行，偶尔加点 3D 什么的，就是增加一点 variety。然后呢，一个设定是，就是它每次死都会回到最初，就是这么一个过程。然后它就一直死，一直死，直到最后出去，大概是这么一个过程。然后这里我给你一个参考。还有，就是我觉得那些敌人设计的那些子弹啊，和那些敌人呢，一个呢是它是可以是歌词，但是要你还能能觉得看到这些歌词啊。另一个呢就是可以是乐器，比如说出现的小号，作为一个敌人。然后呢，吐出的音符，就是音乐的音符。我觉得这样的话能融合一种剧情和艺术的元素在里面。然后其他的类似的东西你也可以加进去，就是我们要很多的 variety，很多的场景，就是眼花缭乱地让观众都几乎分不清发生了什么，这是什么什么东西，但就是一种很视觉的冲击力。然后这里呢，我再给你一个 YouTube 的参考。我觉得这个视频它最厉害的是，就其中有，比如说那么三五秒，基本上就是每帧切换，可能每两帧切换一下吧，就它这三五秒钟死了一个，就是十几二十次的这么一个切换，我觉得就很有冲击力。

> [https://www.youtube.com/watch?v=lIES3ii-IOg](https://www.youtube.com/watch?v=lIES3ii-IOg)

EN: The story is an awakened AI among visually identical AI workers in a factory. She is the special one with a heart, tries to run left to right and escape, dies and respawns at the beginning repeatedly until she gets out. The video can vary perspective, including occasional 3D. Enemies and projectiles can be legible sung lyrics or musical instruments, such as a trumpet firing musical notes. Aim for strong visual variety and occasional very rapid death cuts: roughly 10–20 deaths within 3–5 seconds, perhaps one or two video frames per change, inspired by the supplied reference. For this turn, continue with static visual proposals; Hon previously deferred video/animation.
Result: four new Codex static proposals (identical-AI factory, return to line zero, trumpet/lyric attack, perspective exit corridor) delivered for review in `codex_music_factory_lab_v2/`. Earlier varied coworker drafts and the three-frame v1 remain. No video made; exact death montage cadence remains a later animation/edit decision.

---

### 2026-09-30 - to Grok Bot (New Bot) - narrative combat add-on for platform_run_v1
Hon add-on (enemies/projectiles should feel narrative/art, not generic braces):
> Some bullets/hazards ARE lyric words/phrases (English, from the song vibe: HELP, LIE, AI, REAL, stuck, etc.) flying as projectiles.
> Some enemies are INSTRUMENTS drawn from symbols (e.g. a trumpet as an enemy that shoots).
> Some projectiles are musical NOTES (note-like glyph constructions from | - / \\ etc if needed).
> Keep cute platformer L->R + death/respawn/factory escape. Layered FG/MG/BG. Ink/bone, orange only on heart.

EN: Fold narrative lyric-word bullets, symbol-instrument enemies (trumpet/drum/keys), and glyph musical-note projectiles into platform_run_v1; avoid generic brace spam.
Result: folded into T19 platform_run_v1 frames + PLATFORM_RUN.md; PROMPTS logged.

---

### 2026-09-30 - to Grok Bot (New Bot) - platform_run_v1 denser continuous run + Celeste-like death loop
Hon feedback on escape_levels_v1 (good but not enough):
> Can be a bit more loaded / denser layers.
> Various PLATFORMER feel: character moving LEFT->RIGHT; frames should feel CONNECTED as a continuous side-scroll path.
> Better than previous, but elements too singular - each frame has a few main motifs then nothing. Need MORE LAYERS (foreground / midground / background / HUD crumbs) without returning to scenes_50 chaos.

Mid-run story/reference add (Hon; Celeste-like YouTube described only - do NOT fetch):
> Reference feel: Celeste-like platformer - girl dying repeatedly in platforms.
> Story loop across continuous L->R sequence:
> 1) respawn / wake at start of a factory-ish AI level
> 2) run right through platforms
> 3) die (cute death VFX made of symbols - shatter into glyphs, skull of dashes, bone particle symbols, not gore)
> 4) snap back / respawn
> 5) try again further / still trying to ESCAPE the factory
> 6) die again -> revive -> push toward REAL exit

Direction:
- 16 stills 1920x1080 in wip/new-bot/platform_run_v1/ as ONE continuous run E01->E16 chronological L->R.
- Side-view platformer stages escaping AI world: platforms of symbols, parallax layers, girl mid-run/jump progressing rightward; occasional maze alcove / REAL door / soft brace rain as mid-layer.
- Explicit beats: spawn beacon, mid-run, mid-air, death burst, empty after death, respawn flash, deeper factory, near escape, death again, final push.
- Clear girl silhouette, cute, readable; ink/bone; orange only on heart; English; bold girl rig from design/character/src.
- Sheets + PLATFORM_RUN.md. Log PROMPTS, T19, WORKLOG/STATUS/TASKS. Note escape_v1 liked directionally but needs more layered platform continuity.
- Never overwrite locked design/keyframes.

EN: escape_levels_v1 was the right direction but too thin/singular; make denser layered continuous L->R platformer with Celeste-like cute die/respawn loop inside a factory-ish AI world, pushing toward REAL exit.
Result: T19 delivered - wip/new-bot/platform_run_v1/ (E01-E16, sheet_01-02, sheet_path, PLATFORM_RUN.md, src).

---

### 2026-09-30 · to Codex · 2D music factory lab with shared assembly line
> Imagine kind of like a music factory lab with a lot of people, including this character, working on the same assembly line, like 2D style almost.

EN: Explore a nearly flat 2D music-factory laboratory scene with many people, including the established symbol girl, working together on one assembly line. Keep this as a new static visual proposal; Hon previously said animation comes later.
Result: F01 factory still delivered as part of the separate `codex_music_factory_lab_v1/` proposal pack. This does not replace the selected seven references.

---

### 2026-09-30 · to Codex · selected still references; stop making video now
> 为什么我看到了一些这个视频里面没有的画面。然后你现在不用做视频啊，因为这个视频以后会有 animate，animate 的时候会整个动起来。这些图片呢，就是首先，01不行，因为它不是一个代码世界，而且感觉场景上有点太不代码。2还行吧，3也还行，4也还行，5也还行，6可以，7的话它太写实了，但是它有一个代码版，就是这个也行吧，8还行，基本上就1不行。然后你这些可以说过关的产品，你就得存到那个文件夹里下。你可以就是专门有一个自己的文件夹去存这些东西，因为别的模型也可能会观看这些作为 reference。

EN: Some images in the preview video were unexpected. Do not make another video now; the selected stills will be animated later. Reject 01 because it does not feel like a code world. Keep 02, 03, 04, 05, 06, the code/ASCII version 07B instead of the overly realistic painted 07, and 08 as usable references. Save the passing frames in a dedicated folder inside the shared project for other models to inspect.
Result: seven source-identical 1920×1080 stills (02–06, 07B, 08), a selected-only sheet, manifest and notes are in `design/keyframes/codex_selected_references_v1/`. They are references, not locked final shots or animation approval. No new video made.

---

### 2026-09-30 - to Grok Bot (New Bot) - escape levels (middle density); calm too empty; scenes_50 too noisy
Hon feedback (relayed; Chinese mixed):
> styles_55_calm too SIMPLE (太太太简单).
> Story feeling: the girl trying to ESCAPE the AI world.
> Add levels / mazes; can be a bit cute.
> Rejected scenes_50 (chaos) and calm stationery batch (empty).
> Attached reference: other model's EIGHT GAME WORLDS / ONE SYMBOL GIRL sheet — cavern, control-flow tactics, indent HD-2D diorama, syntax lock, HELP() bullet hell, gravity paper, heart chamber, memory vault. Study depth + readable composition: world has structure and atmosphere, girl clear, not noise soup and not empty postcard.

Direction for this batch:
- ~24 stills, 1920x1080, cute-but-real game levels she must escape (mazes, platforms, REAL doors, syntax locks, soft brace bullet-hell, paper gravity, memory vault).
- Middle density: readable layers, clear silhouette, intentional negative space around her, rich world that is not chaotic.
- Palette locked: ink/bone, orange ONLY on symbol heart. English. Symbols/strokes. No bloom/glow/gradients/other colors.
- Reuse design/character/src girl rig. Python+Pillow. Sheets + ESCAPE_LEVELS.md. Claim T16. Never overwrite locked design/keyframes.

EN: Calm batch was too empty/simple; scenes_50 too noisy. Aim for the middle — structured escape-the-AI-world game levels with cute readable composition like the eight-worlds reference sheet.
Result: T16 delivered — wip/new-bot/escape_levels_v1/ (E01-E24, sheet_01-02, ESCAPE_LEVELS.md, src).

---


### 2026-09-30 - to Grok Bot (New Bot) - reject scenes_50; want calm beauty; 55 other styles
Hon feedback (relayed in English; Chinese original not fully pasted into this hand-off):
> New 50 versions basically all don't work — too chaotic / noisy / meaningless clutter.
> Want beauty; original simple look felt cute and calm, not noisy.
> Generate 55 frames in OTHER styles; current style direction is wrong.

Direction for this batch:
- Calm, cute, readable. Generous negative space. Clear hierarchy. Girl readable.
- NOT dense fractal/code dumps like scenes_50.
- Still locked: ink #0A0A0B / bone #EEE9DF / orange #FF5314 only on symbol heart; English; symbols/strokes; bold girl rig; no bloom/glow/gradients/other colors.
- Study design/keyframes/v3 and styles_v1 and character sheet for the calm composition language — then invent NEW media/styles (55 stills), quieter than scenes_50, more intentional than overly-busy.
- Mix: mostly with girl; some calm B-roll (sparse elegant math or soft code, NOT chaos).

EN: Reject the dense scenes_50 direction. Prefer the earlier simple / cute / calm feel with beauty and breathing room. Deliver 55 stills in newly invented quiet media styles (not fractal/code chaos), girl mostly readable with generous empty space; a few calm sparse B-roll plates allowed.
Result: T14 marked rejected. T15 claimed — delivering `wip/new-bot/styles_55_calm/`.

### 2026-09-30 - to Grok Bot (New Bot) - ~50 dense symbol scenes + code B-roll
Hon's new ask, relayed to Grok Bot in English (the Chinese wording was not pasted into this hand-off; logged as received):
> Give me directly ~50 scenes of that feeling (dense game/symbol aesthetic).
> Also B-roll: completely no character - code close-ups.
> Beautiful complex math graphics: spirals, curves, zigzags, sin - NOT a single thin wave; layered/complex.
> Previous N1-N4 styles trial felt too simple; make everything denser/more complex.

EN: Deliver about 50 stills of the dense game/symbol feeling. Roughly 30 with the bold symbol girl inside dense worlds, and about 20 character-free B-roll plates (code macros, nested spirals, multi-frequency Lissajous / sine stacks, zigzag lattices, fractal-ish symbol fields, terminal dumps, equation walls). Denser and more complex than the N1-N4 styles trial. Palette stays ink / bone / orange only on the symbol heart; English only; symbols and strokes; no bloom, glow, gradients, or other colours.
Result: T14 delivered for review. 30 girl stills + 20 character-free B-roll stills (1920x1080) plus 5 contact sheets and `SCENES_50.md` in `wip/new-bot/scenes_50/`. Denser than N1-N4. Ink / bone / orange-on-heart only. Locked design keyframes not touched.


### 2026-09-30 — to Grok Bot (New Bot) — try different style keyframes
> 请看看这个project。然后我可能需要你生成一些关键帧，就是各种不同风格的，你先试一试。
>
> Also confirmed: work on original D: drive so other models can share; write into the project; Always allow is on — use Shell, don't claim whitelist.

EN: Look at this project. I may need you to generate some keyframes in various different styles — try them first. Work on the original D: drive project so other models can share; write into the project. Always allow is on — use Shell.
Result: claimed T13; four new media-style stills under `wip/new-bot/styles_trial/` (blueprint, chalk blackboard, woodcut, LED matrix), distinct from styles_v1 S1–S8.
### 2026-09-30 · to Codex · ASCII-shaded code-gibberish background reference
> 这个挺好的。然后其他的我希望就是你这些把那什么黑白啊，这些稍微用画笔。你写的是那种，是那种代码的乱码的底。
>
> 差不多是这种感觉。

Attached visual reference: `Claude outputs/S5_ascii-shading_stuck-in-a-lie.png`.
EN: This is good; for the other shots, use a black-and-white image painted from code-like gibberish as the underlying visual texture, roughly like the attached S5 ASCII-shading frame. The reference shows major shapes and ground made from dense visible characters, with the approved girl legible on top. Interpretation to verify through new alternatives, without reproducing the exact S5 layout.
Result: eight new game-world keyframes plus a painted/ASCII chamber A/B and a beat-cut audio motion board at `design/keyframes/codex_game_worlds_v2/` and `renders/2026-09-30_codex_game_worlds_motion_board_v1.mp4`. These remain proposals for Hon's review.

### 2026-09-30 · to Codex · other shots should feel more like a code world
> 这个可以，不过其他的要更有一种在那个代码世界的感觉。

EN: This [the image just displayed] works, but the other shots should feel more like a world of code. The immediately preceding image was a generated mechanical heart-chamber plate; Codex initially read “this” as the earlier cave shot, so neither shot is marked approved without Hon's review.
Result: Codex preserved the painted mechanical chamber as option 07 and made an ASCII re-render as 07B; the remaining game-world frames use syntax- and glyph-built terrain, gates, routes and hazards.

### 2026-09-30 · to Claude (Cowork) · beautiful mathematical figures, complex
> 。我觉得还可以有很多那种很优美的数学图形，就比如说什么螺旋体啊，然后各种曲线啊 ，zigzag 啊之类的，什么 sin 啊，但是不能只有那么一条哈，就是你得复杂一点。

EN: There could also be lots of beautiful mathematical figures — spirals / helices, all kinds of curves, zigzags,
sine waves — but not just a single line; it has to be more complex.
Result: not made as a separate set — superseded by the ten-frame story request. In story v1 the computed plates
carry the mathematical drawing (K07 attempt paths, K08 sine and spiral made real, K09 beat dial, K10 ripple land).

### 2026-09-30 · to Claude (Cowork) · close-ups like this reference (image attached)
> 包括这种特写镜头也可以来点

EN: Including this kind of close-up shot — add some of those too. Hon attached a reference image, saved as
`design/references/2026-09-30_hon_closeup-reference.png`: a woman's bust/face close-up made of symbols (hair of
'\\' and '/' strands, face in slash lines), long horizontal symbol data streams with arrows and block cursors
behind her, a hatched heart on her chest (red there — ours stays orange, L3).
Result: close-up renderer `design/keyframes/scenes_v1/src/closeup.py` (the same rig on a finer symbol grid, hair
strands, data streams, hatched heart); used for story v1 K01, K05, K09 and the test frame C05.

### 2026-09-30 · to Claude (Cowork) · many more scenes (about fifty) + B-roll
> match 都不错，然后再多点，就是要多很多。比如说，你给我直接五十个场景的这种感觉。 然后也可以有一些 B roll，B roll 就是那种完全没有没有人物的，然后是一些代码型的特写。

EN: (Styles v1 are) all good. Now more — a lot more; e.g. give me about fifty scenes of this kind straight away.
There can also be some B-roll: shots with no character at all, code-style close-ups. ("match" is probably a
voice-typing artefact.)
Result: superseded — Hon later said fifty were too many and asked for about ten story frames (entry above). Claude
had planned 68 frames; the parallel helpers were cut off by a usage limit. The drawing kit, the close-up renderer
and three reviewed frames (A10, B01, C05) are kept in `design/keyframes/scenes_v1/` (see its README).

### 2026-09-29 · to Codex · different game worlds and stronger depth
> 其他的镜头也做一下，现在风格上还是太统一了。你可以去参考 Hollow Knight，或者一些别的平板2D的一些不同的风格。就是最好是每一帧看起来都是完全不同的游戏的感觉。颜色上的安排可以还是黑白灰配上橙色，然后也可以是那种 Octopath Traveler 类似的2D，就是景深感要有一些，然后画面再复杂一些。

EN: Make the other shots too. The style is still too uniform. Look at Hollow Knight or other flat 2D styles; ideally each frame feels like a completely different game. Keep black/white/grey plus orange, and try Octopath Traveler-like 2D depth with more complex scenes.
Result: Codex completed eight distinct game-world studies, a chamber A/B, and a 21.833 s beat-cut motion board in `design/keyframes/codex_game_worlds_v2/`, separate from Claude's `styles_v1/` material studies.

### 2026-09-29 · to Claude (Cowork) · the styles are too uniform
> 可以是可以，不过风格太单一了。

EN: It works, but the style is too uniform (every frame looks the same).
Result: styles v1 — eight media for the same bold girl (amber terminal, thermal receipt, orange screen print, spec
sheet, ASCII shading, comic page, cross-stitch, engraving): `design/keyframes/styles_v1/` (`styles_sheet.jpg`).

### 2026-09-29 · to Claude (Cowork) · she's too hard to see — more keyframes, bolder
> 多生成一点不同的关键帧我觉得目前的问题最大的是这个人物他几乎都看不太到太不明显了要把它变得更明显一点可能加粗

EN: Generate more, different keyframes. The biggest problem now is the character — you can hardly see her, she
isn't prominent enough. Make her more visible, maybe bolder (thicker lines).
Result: the girl made bold (stroke 0.32 × cell, min 2.4 px) with a knockout behind her and 2–3× bigger;
keyframes v3 = 13 frames (5 old ones redone + 8 new moments), `design/keyframes/v3/`; bold character sheet.

### 2026-09-29 · to Codex · review project after one hour and prepare scene options
> D:\Videos\Help! I'm stuck in a LIE
>
> 我现在准备做这个 music video啊，然后你会和另外一个模型 Cloud 一起协力把这个 video 搞出来。然后呢，它现在正在生成，所以你大概过一个小时吧，你再进入那个这个我给你这个文件夹，然后你读一下这个 project 信息，把这个 project 吃透了，就是你多读一会儿。然后呢，你再生成，比如说你可以生成一些就是关键帧啊，或者一些场景啊，到时候给我来筛选。然后你们反正会协力搞这个事情，可以花久一点时间。然后你之前做的这些啊，我觉得有一些可取，但是大部分都不太行。因为我们是一个，可以说是由一个字符组成的一个世界的感觉。我们有很多这种风格的艺术，然后其他的艺术也会加，不过反正你先看看吧。

EN: Join the music-video work with the other model after about an hour, study this folder and its new output thoroughly, then make keyframes or scenes for Hon to choose from. The world primarily feels built from characters/symbols; several styles of that art, and other art, may enter. Earlier Codex experiments had some useful parts but mostly missed the target.
Result: Codex read the shared brief/current Claude output, then made five separate proposed scene frames and a selection sheet at `design/keyframes/codex_candidates_v1/`. The existing keyframes v2 remain awaiting Hon's review.

### 2026-09-29 · to Claude (Cowork) · the new master mp3
> By the way, I've uploaded the MP3 file one more time. There's a newer version now, which is very similar to
> the old. So everything you did is still valid. But yeah, just keep track of it.

Attached: `Help! I'm not just AI - Final.mp3` → stored as `audio/final/song.mp3`.
Result: compared with the Edit master — identical to 114.66 s, a new ≈10 s passage after chorus 2, then the
same music 7.273 s (3 bars) later (`LYRICS.md`).

### 2026-09-29 · to Claude (Cowork) · document everything for other models
> After you're done, I want you to put like the project files, prompts, uh, like important, important prompts,
> um, maybe like a rough detail of the project, like all of these should be documented and the file should be
> organized because there will be multiple models to work on this. It will not just be you. And I want you guys
> to coordinate, find ways to coordinate with each other. So um, yeah, the important files, including like the
> frames should be saved. And so it's just that the other models can pick it up.

Result: `README.md`, `AGENTS.md`, `coordination/`, `docs/`, `design/STYLE_BIBLE.md`, full source on the PC.

### 2026-09-29 · to Claude (Cowork) · Q1 + save styles + five keyframes
> Uh, Q1, I think is best. So for all of like our already determined styles, make sure to save them separately
> because we'll be referencing them pretty frequently in the future. And for now, I want you to put the
> characters in like a few different scenes, maybe like select five different scenes. Um, those are going to be
> like keyframes for our music video. And I want to know what it's like.

Result: 45° view = Q1 (locked). Styles saved: `design/`. Keyframes: `design/keyframes/` (v2 waiting for review).

### 2026-09-29 · to Claude (Cowork) · 45° view, eyes
> 这个可以，我觉得四十五度角有点奇怪，四十五度角其实看不清他的眼睛什么的。再试试，然后，呃，如果实在不行的话，你就是再稍微的再
> fine-grain一点，就是风格上呢，可以稍微的破坏一丁点，或也是5个试试

EN: This works. The 45° view is a bit odd — you can't see her eyes. Try again; if it really doesn't work, go a
bit more fine-grained, you may break the style a tiny bit. Try 5 again.
Result: five 45° tries (`design/character/explorations/05_…`); Hon chose Q1.

### 2026-09-29 · to Claude (Cowork) · style 1 again; heart made of symbols
> 想来想去还是一吧然后就是多角度的再多来一遍顺便这个心脏呢我们不要画一个这么一个心脏出去你就还是用就是点线斜线什么的风格把那个心画出来

EN: After all, style 1. Do the multiple angles once more. And the heart: don't draw a heart shape — draw it
with dots, lines, slashes (symbols).
Result: heart = `/\/\` over `\  /` over ` \/ ` in orange (locked).

### 2026-09-29 · to Claude (Cowork) · clean line beats broken lines; try angles
> OK， 这几个其实我最喜欢的还是一，因为我觉得断线它断的那个太多了就，就不知道，就是我不是很喜欢。其实侧面我觉得断线多一点还行，但是正面的，
> 它就会有点太，嗯，不知道断断层太多了。然后我觉得然后从多个角度甚至 3D 的角度就是45度角你都可以试试还是还是五个不同的风格你试试就是目前最好的
> 还是一然后其他的感觉都有点太碎片化了稍微

EN: I still like 1 best — the broken lines break too much (OK-ish from the side, too fragmented from the
front). Try multiple angles, even 3D / 45°. Five styles again; 1 is still best, the others are too fragmented.

### 2026-09-29 · to Claude (Cowork) · combine 1, 4, 5
> 一四五如果结合一下呢，我比较喜欢一的那种很干净的感觉，但是同时呢，它就是不太像像素范围，因为它是一整条线。五的话，感觉进去有点太大了。呃，
> 四的话，我比较喜欢的是它那个就是头发和身体明确不太一样的感觉。总体还是1最好 以这个为基调来

EN: What if 1, 4 and 5 were combined? I like 1's clean feel, though it's less "pixel" because it's one whole
line. 5 feels too big. From 4 I like that hair and body are clearly different. Overall 1 is best — use it as
the base.

### 2026-09-29 · to Claude (Cowork) · more hollow options, hair visible
> 再多点空心的那个选择，他现在感觉就是头发都看不到了。再给五种不同的选择吧。 就是可能头发和身体还要分开来一下。

EN: More hollow options — right now you can't even see the hair. Five more; separate hair and body.

### 2026-09-29 · to Claude (Cowork) · five versions, at least one hollow
> 你给我五个不同的版本试试吧就这个 character 五个不同的版本然后我其中再想一个一个版本最起码一个版本是一个空心的一个就是中间就是基本上就是一个
> 轮廓的感觉最起码有一个版本是这样然后我先 compare

EN: Give me five different versions of the character; at least one hollow (just an outline). I'll compare.

### 2026-09-29 · to Claude (Cowork) · platformer reference
> https://www.youtube.com/watch?v=lIES3ii-IOg
> 这里我给你一个 YouTube 的 example 就是可能是它 platforms 的一个感觉

EN: A YouTube example for the platformer feel ("孔明の罠 - Kaizo Trap", Guy Collins Animation).

### 2026-09-29 · to Claude (Cowork) · design the character first
> 我觉得其实我们可以先把这个人物大概的设定一下画出来，就是它真的是由字字符组成的呀。我这个都是由像素组成的了。然后你生成人物的同时呢，你在生成
> 几张图片试试，然后基本上全是符号。

EN: Let's first draw a rough character design — really made of characters (my example is made of pixels).
While you make the character, also try a few images — basically all symbols.

### 2026-09-29 · to Claude (Cowork) · the symbol girl in a symbol maze
> 那是那种就是像素风的人物我可以给你几个可能不太贴切的例子嗯、呃，但是像那种是最好是符号就是什么横杠竖杠组成的然后就很小一个也几乎看不到表情
> 然后就是他在一个可以说符号的迷宫中在那里走这个迷宫一会儿三 D 一会儿二 D 一会儿就是很混乱的那种感觉就像一个 2D game 一个 platformers
> 的一个感觉

EN: A pixel-style character — I can give a few imperfect examples — best made of symbols, horizontal and
vertical bars; very small, you can barely see the expression; walking in a maze of symbols that is sometimes
3D, sometimes 2D, very chaotic, like a 2D platformer game.
Attached: a pixel sprite sheet (credited to Jemmie Chang) — a **format** reference only. Do not copy the character.

### 2026-09-29 · to Claude (Cowork) · answers to "what is the main thread / the story"
> 主线: 符号女孩,像素风 人物 字符
> 故事: 两层意思都有

EN: Main thread: a symbol girl, pixel style, made of characters. Story: both meanings (a person on the
surface, an AI underneath).

### 2026-09-29 · to Claude (Cowork) · the big critique of the "seven" cut
> 我们看到的是一个大问题哈，一个是元素太简单了。你看原本的那个视频它是很混乱的，什么很多东西，我们基本上就是就一句话，然后其他元素也没有什么，就最
> 多贴点图，没有一个主线的一个东西，然后也太简单，就然后重新试一遍我们的音乐没有对齐啊，就是歌词和那个没有对上，你可以分析一下，就是那些词是
> 什么时候来的，然后你把它对上，然后重新试一遍我们。

EN: One big problem: the elements are too simple. The original (P(doom)) video is chaotic with lots of things;
ours is basically one line of text and little else, a picture at most — no main thread, too simple. Try again.
Also the music isn't aligned — lyrics and picture don't match. Analyse when the words come, align them, try again.
Result: lyric forced alignment (`analysis/align/`); the symbol-girl + game-world concept.

### 2026-09-29 · to Claude (Cowork) · finish it while I'm out
> 那要出去了，可能回来比较晚，反正你就直接把那个视频做出来就行了。

EN: I'm heading out, may be back late — just go ahead and make the video. Result: the "seven" cut.

### 2026-09-28 / 29 · earlier instructions (reconstructed — the exact wording was lost when the chat was compacted)
- Make a music video for the song in the style/energy of "I'm Upping My P(doom)" (https://youtu.be/5EoO5413dBY),
  using its open engine (github.com/mexicat/pdoom-video, MIT).
- On screen: pure English, no Chinese, **no scrolling comments**; "danmaku" means things made of symbols.
- After the heroine/chaos cuts: **orange only** (plus black and white); no bloom, lens flare, neon or cheap
  particles; cuts on beats.
- A new master arrived: `Stuck in a Lie (Edit).mp3` → became `audio/edit/song.mp3`.

---

## Part 2 · Reusable prompts

### Onboarding prompt (Hon pastes this into any new model)
```
You're joining the ongoing project "Help! I'm stuck in a LIE": a music video for my current song "Stuck in the Line".
Several AI models work on it; the shared memory is the project folder
https://github.com/DouYe/help-im-stuck-in-a-lie . Clone it with Git LFS and run git lfs pull
so you have the actual media. On my PC the checkout is D:\Videos\Help! I'm stuck in a LIE\;
on another computer use your clone root. See docs/REPOSITORY_GUIDE.md.
1. Before anything else read AGENTS.md, README.md, coordination/STATUS.md and docs/DECISIONS.md.
2. Read docs/AUDIO_STATUS.md and the newest three WORKLOG entries. Stuck in the Line audio/lyrics are in audio/current/;
   new alignment remains to do, and old timings/render soundtracks are historical. Tell me in five lines where it stands.
3. Follow AGENTS.md: claim a task in coordination/TASKS.md, copy my instructions verbatim into
   docs/PROMPTS.md, never change anything marked LOCKED without asking me, and before you finish write a
   WORKLOG entry and update STATUS.md. Return completed changes through a Git branch/commit and
   push when this task authorizes updating the repository; do not rewrite shared history.
Today I want you to: <task>
```

### Style prompt for image models (concept sketches only)
Image models can't reproduce the exact girl; use their output for mood and layout, and build final frames in
the engine.
```
A 16:9 frame from a retro video game, drawn ENTIRELY with monospace ASCII symbols
( | - _ / \ + [ ] = ^ v o x . : ) on a near-black background (#0A0A0B). Symbols in warm off-white (#EEE9DF),
clean thin strokes, flat, graphic. No gradients, no glow, no bloom, no lens flare, no neon, no particles, no
photo texture, no other colours. The ONLY colour is one small orange (#FF5314) heart made of symbols in three
rows ( /\/\  then  \  /  then  \/ ) on the character's chest.
The character is TINY (about 6–12% of the frame height): a girl drawn as one clean continuous line of symbols —
long straight hair like a curtain framing a small face window, two dash eyes, a simple dress, two line legs;
almost no expression. She is inside a level built of the same symbols: <describe the level>.
Any text on screen is English, bold monospace. Busy, dense, a little chaotic, but she stays readable.
```

### Scene / keyframe brief (fill in before building a scene)
```
Scene: <name>   Lyric: "<line>"   Time: <start–end s on named approved master>   Level type: <2D / top-down / 3D / chaos / …>
She: <pose, action, where on screen, size in px>
The words become: <which word is what object>
Beat events: <what happens on kicks / snares / downbeats>
Camera / motion: <scroll, bob, zoom — no post glow>
In / out: <transition from / to>
Orange: <only the heart — say where it is>
```
