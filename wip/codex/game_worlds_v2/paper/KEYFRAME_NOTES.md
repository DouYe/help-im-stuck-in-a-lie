# Paper gravity / code world — proposal

**Review frame:** `KF_55p15_stuck_paper_gravity_ASCII.png` · 1920×1080 · Edit/Final 55.15 s, start of the second “Stuck in a lie.” This is a new candidate, not an approved look or an app scene.

The world is a 2D cut-paper gravity puzzle. One code branch fails, the entire stage turns clockwise, and gravity pulls the girl horizontally through the uncompiled void. `L`, `I`, `E` are physically separate load-bearing pieces; the letters are cut from dense `@ % # x + = .` shading rather than printed across a flat backdrop. Indented `if / return / else / gravity / fall` statements are playable paper ledges. The approved bold 17×27 glyph girl is the only consistently clean figure. Her heart uses the project's orange symbol-heart construction.

The distant architectural plate was generated as an original monochrome paper structure with the built-in image-generation tool, then used **only as a luminance/depth map**. The visible frame is drawn as exact monospaced ASCII characters from that map; the source image pixels are absent from the final. The structural letters, paper slabs, code strips, and character are deterministic Python/Pillow overlays.

**Motion proposal:** enter on the 54.126 s downbeat; for one beat, the top `if (real)` ledge splits from `else`. On “Stuck” at 55.148 s, rotate the scene's level planes 90° with a hard 2–3 frame impact and switch gravity right. Keep the girl visible against the central black code void as the ASCII shadows move at different speeds. `fall("LIE")` slams shut on “lie” at 56.42 s. Cut at the 56.548 s downbeat into the heart reveal.

**Build:** `python -X utf8 compose_paper_ascii.py`. The script reads `paper_architecture_plate.png` and the current approved `design/character/src/final_sheet.py` rig. `compose_paper_frame.py` and its non-ASCII render were an intermediate study; the `_ASCII.png` file is the review candidate.

**Image-generation prompt used for the depth plate:** Original 16:9 cut-paper gravity-puzzle architecture at a 90-degree level rotation, nested black/bone/grey folded rooms and hard paper shadows, no character, no readable words, no orange or other hue, no glow/bloom/lens flare/neon, original environment without recognizable existing-game assets. The plate was converted into literal glyph luminance before delivery.
