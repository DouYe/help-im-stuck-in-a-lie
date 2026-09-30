# Codex match-cut pair — proposal, 2026-09-29

These two new 1920×1080 stills are exploratory alternatives. They do not replace the five Claude keyframes awaiting Hon's review.

| Frame | File | Proposed musical moment | Visual idea |
|---|---|---|---|
| A | 01_stuck_side_chute.png | 46.78 s, final "lie" | Side-on false platform breaks under the girl. A wall of 0 1 | / \ glyphs narrows into a descending chute. "STUCK IN A LIE" is a stencil assembled from the same stroke glyphs. |
| B | 02_make_me_real_deep_maze.png | 47.50 s, "Make" | On the 46.858 s downbeat the camera pitches from side view into a steep, deep maze; ink/ivory polarity snaps. Low walls form a left/right zigzag route. Only "MAKE" is visible at this lyric time; "ME" and "REAL" should enter at their sung starts. |

**Match cut:** The girl's locked 17×27 symbol rig is imported read-only from design/character/src/vgirl.py and glyphs.py. Both frames keep her orange symbol-heart on the identical pixel bounds x=940–980, y=544–575 (center 960,560). A uses the stuck pose; B turns her to the approved Q1 45° pose. A cut to B can be hard and exactly on the 46.858 s downbeat. The girl should hold position for two or three frames as the world inverts and unfolds; wall movement can then overshoot on kick, settle before "Make" at 47.425 s. "Me" starts 47.77 s and "real" 48.09 s.

**Visual constraints:** Ink #0A0A0B, bone #EEE9DF, graphite/ash greys, orange #FF5314 only on the symbol heart. All world structures and large letters are assembled from stroke glyphs; small UI labels use the project's IBM Plex Mono. No glow, gradients, bloom, neon, or particles. The design explores a connected world and a strong camera relationship rather than five isolated illustrations.

**Technical check:** Both PNGs were rendered with make_matchcut.py using the Codex bundled Pillow 12.3. They are 1920×1080 and have identical orange-heart bounding boxes. I viewed both at full-frame size. The existing shared app/, design/, data/, and coordination files were not changed.
