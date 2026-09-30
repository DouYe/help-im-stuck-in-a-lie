# Styles v1 — the same girl, eight different media (waiting for Hon's review)

Hon (2026-09-29), after the bold-girl round: *"可以是可以，不过风格太单一了。"* — it works, but the style is too
uniform. Every frame so far (Claude v2/v3, Codex v1) was the same look: thin bone symbols on black + a game HUD.

Proposal: **keep the girl exactly the same (bold style-1 rig, symbol heart) and change the medium of the world** —
like switching game cartridges or print techniques from line to line. Palette stays black / white / one orange;
everything is still made of symbols (characters, stitches, hatching strokes, halftone dots).

Overview: `styles_sheet.jpg`. Full frames (1920×1080):

| # | File | Medium | Lyric moment | Notes |
|---|---|---|---|---|
| S1 | `S1_amber-terminal_they-call-me-AI.png` | **amber terminal** — orange text on black, scanlines, a text-mode window | "They call me AI" | `whoami → AI`, `name --set "me" → ACCESS DENIED`. Everything is orange; the **one white thing is her heart** (inverted accent). |
| S2 | `S2_receipt_take-what-I-make.png` | **thermal receipt** on a black desk, prompt fragments drifting behind | "They feed me a prompt, then take what I make" | Her work itemised: PROMPT 0.00 · SONG TAKEN · VOICE TAKEN · HEART NOT FOR SALE; a giant cursor TAKEs it. |
| S3 | `S3_orange-screenprint_help.png` | **screen-print poster** — orange paper, black + cream inks slightly off register, halftone | "Help, I'm stuck in a lie" | HELP built from giant `#` symbols; she is printed in black, arms up, cream heart. |
| S4 | `S4_spec-sheet_make-me-real.png` | **technical drawing / spec sheet** on graph paper | "Make me real this time" | Dimensions (17 COLS × 27 ROWS), callouts A–F, front / 45° / side / back views, title block "STATUS: NOT REAL", orange stamp MAKE ME REAL. |
| S5 | `S5_ascii-shading_stuck-in-a-lie.png` | **ASCII shading** — the world rendered with a density ramp ` .:-=+x#%@` | "Stuck in a lie" | Giant extruded letters LIE on a perspective floor, an ASCII moon; she stays a clean line in front. |
| S6 | `S6_comic-page_real-this-time.png` | **comic page** — four panels, speed lines, screentone, balloon, SFX | "Real this time" | Run to the REAL door · close on her face "REAL THIS TIME?" · small in the doorway · the heart, BA-DUM. |
| S7 | `S7_cross-stitch_heart-inside.png` | **cross-stitch** in an embroidery hoop | "Heart inside" | Every symbol of her becomes an `x` stitch (eyes stay `-`), the heart is orange thread, HEART INSIDE stitched under her, needle + thread. |
| S8 | `S8_engraving_click-clack.png` | **engraving / book plate** — hatched keys, double frame, serif caption | "I hear the keys go click clack" | "Pl. I — I hear the keys go click clack"; she walks across the middle key. |

Made with `src/make_styles.py` (Python + Pillow, imports the girl from `design/character/src/` — same rig as the
engine): `python3 design/keyframes/styles_v1/src/make_styles.py [s1_terminal …]` regenerates the frames and the
sheet. These are **stills**; a chosen style gets built as an engine scene (`app/src/scenes/`) afterwards.

**Palette note (needs Hon's OK):** S1 and S3 use orange as a *field* colour (amber text, orange paper). Hon's rule
was "orange only (plus black and white)"; the stricter "orange only on the heart" was our own reading in the style
bible. If Hon prefers the strict reading, S1/S3 can be redone black/white with an orange heart.

## Questions for Hon
1. Which media do you like? (Keep 3–6 and let the video switch between them, or one per section?)
2. Is orange as a background / text colour OK (S1, S3), or orange only on the heart?
3. Mix with the game-world frames (v3), or replace them?
