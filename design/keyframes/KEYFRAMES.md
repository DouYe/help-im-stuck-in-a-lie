# Keyframes v2 — chorus 1 in the game world (waiting for Hon's review)

Rendered by the engine (edit `keys` in `app/src/edit.ts`), 1920×1080, times on the Edit master.
Overview: `keyframes_sheet.jpg`. First pass: `v1/`.

Re-make (renders → named files + sheet; move a delivered set to `v<k>/` first, never overwrite it):
```
cd app && bun scripts/render.ts stills --edit keys --t 37.95,42.15,46,48.3,58 --out ../wip/<you>/keyframes
cd .. && python3 design/keyframes/src/make_keyframes.py wip/<you>/keyframes
```

| # | File | Time | Lyric | Scene (code) | What you see |
|---|---|---|---|---|---|
| KF1 | `KF1_click-clack_platformer.png` | 37.95 s | "I hear the keys go click clack" | `kf_plat` · `variant: 'keys'` | A 2D platformer. The floor is six key-caps spelling CLICKS; the key she just left is pressed down. She is mid-leap, a dotted after-image behind her. CLICK / CLACK burst out as outlined block letters; a turret fires rings of `o` `+` on each beat; spikes on the ceiling, a pit, a ladder, a `[!]` block. HUD "STAGE 1-1 · THE KEYS"; the dialog types the line, the sung word inverted. |
| KF2 | `KF2_help_bricks.png` | 42.15 s | "Help, I'm stuck in a lie" | `kf_plat` · `variant: 'help'` | The level flips to paper (bone ground, ink symbols). HELP is a building of `[ ]` bricks that shakes on the hit; she stands on top of the P, arms up (the HELP pose), lines bursting around her; turrets on both sides fire `x` `o` rings. "S.O.S." HUD "STAGE 1-2 · HELP". |
| KF3 | `KF3_stuck-in-a-lie_maze.png` | 46.00 s | "Stuck in a lie" | `kf_maze` | Seen from high above: a labyrinth of `|` `-` `+` whose outline is the word LIE. She is tiny, at a dead end inside the I, a `?` over her head, a dotted trail of where she's been; only the area near her lamp is bright. Minimap "YOU ARE HERE · EXITS 0"; HUD "FLOOR 2 · STUCK IN A LIE". |
| KF4 | `KF4_make-me-real_corridor.png` | 48.30 s | "Make me real this time" | `kf_ray` | First-person 3D corridor (raycaster), walls made of symbol courses, a bright door at the end with REAL above it. She walks away from us toward it. Old-shooter status bar: HEART 100 %, REALITY meter 18 %, her face in the middle, FLOOR 03, KEYS [C][L][I][C][K]. |
| KF5 | `KF5_heart-inside_chaos.png` | 58.00 s | "I still got a heart inside" | `kf_chaos` | Everything at once: the frame torn into three slanted strips (platformer · symbol tunnel · maze), rows slipping sideways on the beat, HEART towering in outlined letters. In the middle, bigger than anywhere else, she holds the orange heart; orange rings of `-` pulse out on every beat. Copies of her made of dots and of 0/1 code flicker at the seams — what's underneath. HUD "ERROR · WORLD 1-?-3D". |

## Changes v1 → v2 (2026-09-29)
- KF1: after-images are now dots only, strung along the jump arc; frame moved to mid-leap (37.95 s).
- KF2: HELP pose fixed — arms raised in front of the hair (`\o/`), one `o` per eye.
- KF4: her strokes thicker with a heavier ink outline (reads against the bright door); the status-bar face is a
  full bust with the heart, glancing left/right.
- KF5: HEART gets an ink under-stroke and a dark band behind it; HUD readouts on dark plates.

## Questions for Hon
1. Which of the five level types do you like / not like?
2. Is she the right size (KF3 is the smallest, KF5 the biggest)?
3. HUD / dialog / status bar — keep, simplify, or drop?
4. More chaos, or is KF5 about the right amount?
