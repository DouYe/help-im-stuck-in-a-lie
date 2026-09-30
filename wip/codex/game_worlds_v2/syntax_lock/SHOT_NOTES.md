# KF10 · Conditional Lock — 50.6 s

Original, code-built game-world option for the Edit master at **50.533 s**, the onset of “Real” in the second “Real this time.” This is a proposed keyframe, not an approved scene.

## Picture

- A floating conditional lock fills the frame. Its six structural planes are shaded by literal `.` `:` `+` `=` `%` `#` `@` `x` characters at different scales. Their placement forms the architecture rather than sitting on a painted texture.
- The large `REAL` is also built from ASCII characters. Two animated `{{{` and `}}}` jaws bracket the variable core. The `if (heart == true) {` lintel expresses the double meaning: a code test and a girl's plea.
- `==>` and `<==` are playable floor rails. The true branch reaches `return REAL;`; the false branch ends at `LOCK();`. The camera sees both routes at once, like a boss puzzle. This is a floating branching machine, not a conventional corridor.
- The near-plane girl uses the project's `final_sheet.py` bold 17×27 Q1 glyph rig with an opaque knockout. Her small symbol heart is the only orange.

## Cut and motion proposal

- **50.533 (“Real”)**: beat cut to this exact composition. The word `REAL` arrives through a one-frame collision of the two code jaws; the character remains still for a few frames, then steps toward the true rail.
- **51.12 (“this”)**: the false branch folds upward and the camera takes a short lateral parallax step. Only now reveal `THIS` if lyric typography continues.
- **51.56 (“time”)**: the true rail advances into the hexagonal core, the whole lock clamps one character width, and the camera punches through on the next beat. Only now reveal `TIME`.
- Keep hard cuts on beats and all post effects at zero bloom, halation, and chromatic aberration.

## Rebuild

```powershell
& 'C:\Users\honkw\AppData\Local\Programs\Python\Python310\python.exe' -X utf8 'D:\Videos\Help! I''m stuck in a LIE\wip\codex\game_worlds_v2\syntax_lock\make_syntax_lock.py'
```

Output: `KF10_real_this_time_syntax_lock.png`, 1920×1080 PNG. The script reads the project's current character rig and fonts, and Pillow from `wip/codex/visual_audit/lib` if available. It changes no shared project asset.
