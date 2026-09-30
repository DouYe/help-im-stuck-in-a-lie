# KF13 proposal — ASCII Memory Vault

- **Time / lyric:** about 61.0 s on `audio/edit/song.mp3`, “Heart inside.”
- **Game identity:** a text-mode gothic exploration/boss chamber. Nested vaulted openings, tall collision columns and a perspective tile floor give a playable deep route; all their light and shadow are dense monospaced `. : + = x # % @` glyphs, with small snippets of syntax carved into the walls.
- **Shot / cut:** camera has moved in after the chaotic 58 s chorus frame. The 17 × 27 approved bold symbol girl fills the centre, holding a deliberately enlarged orange heart. On the sung “heart” or following beat, a short push-in could make the heart dominate while the ASCII vault recedes. The bottom left dialogue tile is a text-adventure cue and contains the lyric.
- **Palette:** ink and the project’s bone/grey ramp, with `#FF5314` only in the symbol heart. No glow, bloom, lens flare or generic particles.
- **Relation to existing work:** proposal separate from Claude’s KF13 close-up and S7 cross-stitch heart; neither source nor output is overwritten. No existing game character or environment is copied.

## Rebuild

`render_heart_vault.py` uses the project’s `design/character/src/final_sheet.py` approved rig and Pillow. On this machine, Pillow is available by setting `PYTHONPATH` to `D:/Videos/Help! I'm stuck in a LIE/wip/codex/visual_audit/lib`, then running Python 3.10. It writes `KF13_heart_inside_ascii_vault.png` here at 1920 × 1080.

This is a **still for selection**, not an integrated or approved engine scene.
