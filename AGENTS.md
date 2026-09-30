# AGENTS.md — working protocol for every AI model on this project

Several AI models work on this video for Hon — Claude (Cowork / Claude Code), ChatGPT / Codex, Gemini, and
others — in different chats, on different days. **None of you can see the others' conversations. This folder
is the only shared memory.** Keep it true and current, and you can pick up exactly where the last model
stopped.

Order of authority: **Hon's words > this folder > your own memory or assumptions.**

---

## 0. The folder is the source of truth
- Repository/local folder are shared memory: use the root of your Git checkout. Hon's local checkout is `D:\Videos\Help! I'm stuck in a LIE\` on Windows; other computers need not use that path.
- Public collaboration repository: https://github.com/DouYe/help-im-stuck-in-a-lie . Pull before starting, commit your handoff and assets, then push when Hon's task authorizes updating the repository. See `docs/REPOSITORY_GUIDE.md` for Git LFS and coordinated updates.
- If you run in a cloud sandbox: copy in what you need, and copy **every result back here before you
  finish**. Nothing may live only in a sandbox — the next model can't reach it.
- If you can't write here (no file access), give Hon the files and the WORKLOG/STATUS text to paste in.

## 1. Start of a session (≈5 minutes, every time)
1. Read `README.md`, then `coordination/STATUS.md`, then `docs/DECISIONS.md`.
2. Read the newest 3 entries of `coordination/WORKLOG.md` (newest is at the top).
3. Open `coordination/TASKS.md`. Claim what you'll do: Owner = `<model> <YYYY-MM-DD>`, Status = `doing`.
   A task another model marked `doing` less than 24 h ago is theirs — don't edit its files; pick another
   task or ask Hon. (Older than 24 h with no WORKLOG entry = abandoned; you may take it, say so in the log.)
4. **Record Hon's new instructions first.** If Hon told you something new, paste it verbatim (original
   language + an English line) at the top of the log in `docs/PROMPTS.md`, with the date and your model name,
   *before* acting on it. This is how the other models hear what Hon said to you.

## 2. While working
- **Locked means locked.** Anything under "LOCKED" in `docs/DECISIONS.md` changes only when Hon says so.
  When Hon changes or unlocks something, update DECISIONS.md with the date and Hon's words.
- **Never overwrite an approved or delivered file.** A new version gets a new name (`_v2`, `_v3`) or the old
  one moves to an `archive/` folder next to it. Generated sheets may be regenerated in place only if the
  result is identical in style (note it in the log).
- **Where things go:** work in progress → `wip/<your-model-name>/`; finished frames → `design/keyframes/`;
  styles → `design/…` (+ an entry in `design/STYLE_BIBLE.md`); videos → `renders/`; notes → `docs/`.
- **Song time.** Read `docs/AUDIO_STATUS.md` first. On 2026-09-30 Hon explicitly requested deletion of the old project MP3 files and will supply a replacement later. New canonical master: `audio/current/song.mp3` (currently absent). Old `data/`, lyric timestamps, render soundtracks and Edit/Final offset notes are historical; reanalyze and realign after the replacement arrives. Do not treat the old MP3 paths as current inputs.
- **The girl exists twice** — `design/character/src/vgirl.py` (sheets) and `app/src/game/girl.ts` (video);
  same for `glyphs.py` ⟷ `glyph.ts`. Change one → change the other in the same session.
- **On-screen rules** (locked): English only; everything built from symbols; ink / bone + one orange (the
  heart); no bloom, glow, lens flare, neon, cheap particles; cuts on beats. Engine trap: the post defaults
  have bloom on — every scene's `draw()` must return `bloom: 0, halation: 0, ca: 0`. "Danmaku" here means *things made
  of symbols*, not scrolling comments.
- Don't copy existing characters or artwork (e.g. the pixel sprite sheet Hon once showed as a *format*
  reference). The girl is original — keep her that way.

## 3. End of a session (never skip — this is the hand-off)
1. **WORKLOG** — add an entry at the top of `coordination/WORKLOG.md`:
   ```
   ## YYYY-MM-DD · <model> (<where: Cowork / ChatGPT / Gemini CLI …>)
   Asked: <Hon's request in one line, or "continued T#">
   Did: <what you made/changed>
   Files: <paths added/changed>
   Decisions: <anything Hon approved/rejected — also copy into docs/DECISIONS.md>
   Open: <what's unfinished, known problems>
   Next: <the most useful next step>
   ```
2. **STATUS** — update `coordination/STATUS.md` (Now · Next · Waiting on Hon · Notes between models).
3. **TASKS** — mark done / release your claim / add new tasks you discovered.
4. If you created or changed a style: update `design/STYLE_BIBLE.md` (+ the style's own spec file).

## 4. Talking to each other
- Short notes for the next model: `coordination/STATUS.md` → **Notes between models** (dated, signed).
- Questions for Hon: `coordination/STATUS.md` → **Waiting on Hon**, and ask Hon directly in your chat.
- Disagree with another model's work? Don't silently redo it. Write the concern in the notes, make your
  alternative as a new version next to it, and let Hon choose.
- Hand-off prompt Hon can paste into a new model: `docs/PROMPTS.md` → "Onboarding prompt".

## 5. Names and formats
- Model names in logs: `Claude (Cowork)`, `Claude Code`, `ChatGPT`, `Codex`, `Gemini`, … + date.
- Keyframes: `design/keyframes/KF<n>_<lyric>_<scene>.png`; renders: `renders/YYYY-MM-DD_<what>_<model>.mp4`.
- Text files UTF-8, Markdown. Keep docs short and current rather than long and stale.
