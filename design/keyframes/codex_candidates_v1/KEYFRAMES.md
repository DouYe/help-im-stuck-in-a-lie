# Codex candidate scenes v1 — for Hon to select

Five **new proposals**, 1920×1080 PNGs. The five Claude keyframes v2 in `design/keyframes/` are untouched and still awaiting Hon's review. This is a set of visual and camera tests, not an approved edit or a rendered video.

The project sources for this set were `docs/PROJECT_BRIEF.md`, `docs/DECISIONS.md`, `design/STYLE_BIBLE.md`, `design/character/GIRL_SPEC.md`, `docs/LYRICS.md`, and the existing `design/keyframes/keyframes_sheet.jpg`. Every frame imports the locked 17×27 symbol-girl rig, uses ink/bone/grey with a symbol-built orange heart, and uses no glow or gradients. The level types, protagonist scale, typography and small UI details below are still proposals.

Open **`selection_sheet.png`** first, then the full-size PNGs:

| Pick | File | Musical moment | What this tests |
|---|---|---|---|
| A | `A_prompt_press.png` | Verse 1, roughly 21.5 s, “They feed me a prompt…” | A coherent machine level: a character conveyor carries the girl from PROMPT/INPUT through a COPY press toward an OUTPUT/TAKE strip. The camera can track her while the press stamps on a beat. This verse timing is provisional until the official full-song lyrics are aligned. |
| B | `B_false_floor.png` | 46.78 s, final “lie” | The girl's platform cracks at a character-built chute. Instead of a subtitle over an empty frame, the sung words are level architecture. A short hold shows where she is before the camera changes dimension. |
| C | `C_viewpoint_rupture.png` | 47.50 s, “Make” | A hard cut on the **46.858 s downbeat** to an inverted, deep maze. B and C keep the orange heart on the **same pixel bounds, x=940–980 and y=544–575**; only the camera/world changes. The frame shows MAKE only; ME and REAL should arrive at 47.77 s and 48.09 s if animated. |
| D | `D_real_threshold.png` | 50.53 s, “Real” | A proposed 245 px Q1 close-up at the threshold, with glyph-built walls pressing inward. This tests whether a single more legible view of the approved girl gives the chorus an emotional anchor. The figure size is *not* approved yet. |
| E | `E_heart_cross_section.png` | 58.66 s, “inside” | The small girl faces a much larger glyph cross-section of herself; her chest connects to the same orange character heart inside. Camera push can enter the chamber on the 58.974 s downbeat, then pull back to the same girl at 61.402 s. |

## How the cut would move

- **B → C:** preserve the girl's screen position for 2–3 frames; let the surrounding symbol walls invert, pitch and unfold on the 46.858 s kick. This is a match cut, not two unrelated backgrounds.
- **C → D:** continue her route through the maze, then move close on the 50.492 s beat; REAL appears when sung at 50.533 s. D is one insert in a fuller chase, not an eight-second held still.
- **Toward E:** repeat the world closing around her during the second “Help / Stuck” lines. At “heart” (57.80 s) move toward her chest; at 58.974 s cut inside. Use the contrast of dense glyph walls against one held orange heart.
- Exact word starts and the full 42–62 s candidate shot path are in `wip/codex/project_docs/chorus1_42-62_camera_edit_plan.md`. That path is a proposal and has not been animated or audio-checked.

Generators are kept in `src/`; they import `design/character/src/vgirl.py` and `glyphs.py` read-only. The two match-cut PNGs were visually checked with identical heart bounds. The five PNGs and sheet were visually inspected at full size; no motion or final render is claimed.

**Questions for Hon:** Which of A–E should continue? Does the B→C matched camera jump feel right? Is D's larger character acceptable for one beat? Should E's heart cross-section be denser, or should that moment breathe?
