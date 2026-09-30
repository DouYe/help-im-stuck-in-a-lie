# Project brief

## The song
- *"Help! I'm stuck in a LIE"* — also titled *"Help! I'm not just AI"*. By Hon. 99 BPM, 4/4, ~3:10 (Edit) /
  ~3:18 (Final).
- The singer is an AI (or someone treated like one): *"They call me AI / A name on a screen / They feed me a
  prompt then take what I make"*; the chorus: *"Help, I'm stuck in a lie / Make me real this time / I still got
  a heart inside."* Lyrics and timing: `LYRICS.md`.

## The story (Hon: "两层意思都有" — both meanings at once)
- **Surface:** a small girl is trapped in a maze made of lies and keeps trying to get out.
- **Underneath:** she *is* an AI — made of symbols, living inside a machine's world, asking to be real.
  The world she runs through is built from the same symbols she is. The heart is the one thing that isn't
  grey: orange, and made of symbols too.

**Hon's newer story direction (2026-09-30):** she awakens among many visually identical AIs on a music-factory
assembly line. She alone has the orange symbol heart. She runs right to escape, dies, snaps back to the factory
start, and tries again until she gets out. The sequence can usually read as a 2D platformer, with occasional
camera/style changes including 3D. This is a direction, not a finished whole-song scene map. Previous images
remain saved; new scene studies are separate.

## The main thread (主线)
Hon: *"符号女孩, 像素风 人物 字符"* — a symbol girl, pixel style, made of characters.
- **Small but always clearly visible** — you can barely see her expression, but you always see HER: bold
  strokes with a knockout, ≈130–230 px wide in normal shots, 270–330 px close, one extreme close-up
  (Hon 2026-09-29: "几乎都看不太到 … 要把它变得更明显一点可能加粗").
- **Made of symbols** — horizontal and vertical bars, slashes: one clean line of symbols on a 17×27 grid.
- She is on screen in (almost) every shot; the world changes around her.
- Spec: `design/character/GIRL_SPEC.md`.

## The world
Hon: *"他在一个可以说符号的迷宫中在那里走这个迷宫一会儿三 D 一会儿二 D 一会儿就是很混乱的那种感觉就像一个 2D game 一个
platformers 的一个感觉"* — she walks in a maze of symbols that is sometimes 3D, sometimes 2D, very chaotic, like a
2D platformer game.
- Reference for the feel: "孔明の罠 - Kaizo Trap" by Guy Collins Animation —
  https://www.youtube.com/watch?v=lIES3ii-IOg (a platformer character trapped in an unfair game).
- Level types so far (keyframes v2): 2D side-scroller platformer · inverted paper level · top-down maze whose
  walls spell a word · 3D raycast corridor (old-shooter look) · "error" chaos where all of them tear together.
- Game furniture made of symbols: HUD with lives as symbol hearts, an RPG dialog box that types the sung line
  (the word being sung inverted), a Doom-style status bar with her face, a minimap, turrets firing rings of
  `o` `x` `+`, spikes `^` `v`, bricks `[ ]`, ladders, `!` blocks.
- Lyrics become level geometry: the keys she jumps on spell CLICKS, the bricks she stands on spell HELP, the
  maze is the word LIE, the door says REAL, HEART towers over the chaos.
- New combat proposals: instruments made of symbols can be enemies (a trumpet firing note glyphs is one
  example); lyrics can fly as hazards, but each word/phrase must remain readable. Later animation may use a
  brief burst of very rapid death/respawn cuts. Keep individual stills as clear framed scenes with readable
  doors, platforms, rooms and machines; the continuous runner trial was rejected as messy.

## The look (locked — see `DECISIONS.md`)
- Ink `#0A0A0B` background, bone `#EEE9DF` symbols, **one orange `#FF5314`** — the heart (and HUD lives).
- No bloom, lens flare, neon, gradients or cheap particles. Clean, graphic, dense.
- English only on screen. No scrolling comments ("danmaku" in this project = things made of symbols).
- Cuts land on beats; words appear when they are sung.
- References for density and energy: the "I'm Upping My P(doom)" video (https://youtu.be/5EoO5413dBY) —
  chaotic, many things happening; our engine comes from it (github.com/mexicat/pdoom-video, MIT).

## Whole song (draft — needs Hon's OK, task T5)
| Part (Edit timeline) | Idea |
|---|---|
| Intro 0–15 s | Boot screen / title card made of symbols; she spawns ("PLAYER 1"). |
| Verse 1 15–35 s | "They call me AI…": a calm 2D level; the prompt/keyboard motifs. |
| Pre + chorus 1 35.5–62 s | Keyframes v2: CLICKS keys → HELP bricks → LIE maze → REAL corridor → HEART chaos. |
| Verse 2 ~68–88 s | "My words in their mouths… my name on the cover": levels made of other people's text. |
| Chorus 2 ~88–114 s | Chorus 1's levels, harder and glitched ("soul inside"). |
| (Final only) new ≈10 s passage at 114.66 s | A natural "level transition" / loading screen. |
| Bridge ~125 s (Edit) | "They paid for the session…": the world shows its machinery — the AI underneath. |
| Last chorus / outro | Escape or loop: the ending is Hon's call. |
