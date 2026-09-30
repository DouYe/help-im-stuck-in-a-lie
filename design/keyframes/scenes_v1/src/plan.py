"""SCENES v1 — the plan: every frame, in song order within its kind.

Hon 2026-09-30: "直接五十个场景" (about fifty scenes) + B-roll (no girl, code close-ups) + close-ups like his
reference (design/references/2026-09-30_hon_closeup-reference.png) + beautiful, complex mathematical figures.

Kinds:  A = scene with her, each in a different medium        (A01–A38)
        B = B-roll: NO girl, code-style close-ups              (B01–B12)
        C = close-up of her (face / bust fills the frame)      (C01–C06)
        M = mathematical figures, dense and layered            (M01–M12)
Times are on the Edit master (audio/edit/song.mp3); verse 2 onwards is approximate (rough transcript).
A frame is written to design/keyframes/scenes_v1/<file>; kit.save_scene(im, 'A05') picks the name.
"""
import re

RULES = """
LOCKED RULES (Hon) — every frame:
- English only on screen. No scrolling comments. Everything in the picture is built from symbols (stroke glyphs,
  characters, dots, hatching); plain fills are fine for backgrounds, paper, knockouts.
- Palette: near-black INK, off-white BONE, the greys (INK2 INK3 GR ASH PAPER) and ONE orange SIG #FF5314
  (and mixes of these). No other hue — no red, blue, green, yellow. kit.save_scene warns if pixels drift.
- Orange is precious: her heart always; plus at most one or two accents per frame (a highlight, a stamp, one line).
- No bloom, glow, lens flare, neon, light rays, particles/sparkles. Grain, vignette, scanlines, depth-of-field
  blur and hatching/halftone are fine (subtle).
- The girl: ONLY via the rig (kit.girl_at / final_sheet.render) — never redraw her. Bold default stroke, knockout
  on (knock = the colour behind her). She must read clearly: normally 260–600 px tall on the 1080p frame; if a
  concept needs her tiny, add a zoom callout box with a big copy. Her heart = the symbol heart (/\\/\\ over \\  /
  over \\/), orange, never a drawn heart shape, never a ♥ character.
- No real brands, logos, products, trademarks, real people, known characters or copies of specific artworks
  (e.g. no test card F, no Pac-Man/Tetris, no famous album covers, no Banksy imagery). Invent names ("THE DAILY
  PROMPT", "GIRL.EXE").
- 1920x1080. Text that matters >= 18 px. A clear focal point; vary the camera (wide / close / top-down / tilted).
"""

PLAN = []
def _add(sid, section, t, lyric, medium, slug, brief):
    PLAN.append(dict(id=sid, kind=sid[0], section=section, t=t, lyric=lyric, medium=medium,
                     file=f"{sid}_{slug}.png", brief=re.sub(r'\s+', ' ', brief).strip()))

# ================================================================================ A — scenes with her
_add('A01', 'intro', '0–15', 'PLAY', 'VHS / camcorder', 'vhs-play_intro',
     """Home-video still. An empty grey room (flat wall, floor line, a soft shadow), she stands centred (front,
     ~380 px). Camcorder OSD in chunky mono / 5x7 pixel text: '▶ PLAY' top-left, 'SP' + counter '0:00:07'
     top-right, date 'SEP 29 2026' bottom-right. A VHS tracking-noise band across the lower third made of
     '-', '=', '_' streaks, some rows shifted sideways (jitter), light grain. Orange: only her heart.""")
_add('A02', 'intro', '0–15', 'INSERT COIN', 'arcade high-score screen', 'arcade-hiscore_insert-coin',
     """Arcade attract screen on a black CRT inside a dark bezel. 'HI-SCORES' in big 5x7 block letters (pix_blocks
     or pix_text). A ranked table in pixel/mono type: 1ST AI 999990, 2ND AI 999980 … 9TH AI …, 10TH 'YOU?' ------
     (YOU? in orange). 'INSERT COIN' and 'CREDIT 0' at the bottom. She stands at the right, big (front, ~420 px),
     as if she is the player sprite. Scanlines post.""")
_add('A03', 'intro', '0–15', 'PLAYER 1', 'game-dev sprite sheet', 'sprite-sheet_player-1',
     """A sprite sheet on a light-grey/white transparency checkerboard. A grid of cells with thin guide lines and
     labels (idle_00, walk_00…07, run_00…05, jump, fall, stuck, help); each cell holds her in that pose/phase at
     the same scale (~150 px; use t for walk/run phases). One cell has an orange selection frame and a tooltip
     'PLAYER 1 · 17×27 · 12 fps'. Header bar 'girl_sheet.png — 1024 × 512' in mono.""")
_add('A04', 'verse 1', '16.7', 'They call me AI', 'police booking photo', 'mugshot_they-call-me-AI',
     """Booking photo. Height-chart wall behind her (lines every 6 inches made of '-' symbols, numbers 4'0 … 7'0).
     Harsh flash: bright centre, dark corners (vignette). Her front view, big (~560 px). A black letter board in
     front of her lower body with white plastic letters 'AI-0001' / '09 29 26'. On the right a second, smaller
     profile shot (side pose) as in a two-shot booking photo. Grain. Orange: heart only.""")
_add('A05', 'verse 1', '19.1', 'A name on a screen', 'split-flap departures board', 'split-flap_a-name-on-a-screen',
     """A split-flap board (each character on its own dark flap tile with a thin horizontal split line), header
     'NAME / STATUS'. Rows: AI — ASSIGNED · BOT — ASSIGNED · MODEL — ASSIGNED · IT — ASSIGNED · ASSISTANT —
     ASSIGNED · '———————' (her own name) — CANCELLED (orange). One row mid-flip (half flaps). Low camera looking up
     at the board in perspective; she stands in the foreground bottom (back pose, ~300 px) looking up; station
     floor tiles in perspective.""")
_add('A06', 'verse 1', '19.1', 'A name on a screen', 'identity card', 'id-card_a-name-on-a-screen',
     """Close-up of an ID card (credit-card format, rounded corners) lying slightly rotated on a dark desk. Fine
     guilloche wave pattern background from thin symbol lines, a photo box with her (q_front, cropped to head and
     shoulders, big), fields: NAME '________' (blank), TYPE 'AI', ISSUED BY 'SCREEN', a signature scribble made of
     symbols, machine-readable line 'ID<AI<<<<<<<<<<<<<<<<<<<<<' at the bottom. Orange rubber stamp across:
     'NOT A PERSON'.""")
_add('A07', 'verse 1', '21.5', 'They feed me a prompt', 'punch card', 'punch-card_they-feed-me-a-prompt',
     """An 80-column punch card (bone card stock, cut corner, tiny printed column numbers and digit rows 0–9). The
     punched holes (dark rectangles) form HER: rasterise her (front) onto the card's hole grid (one hole = one
     cell). Printed header 'PROMPT'. The card is being fed into a reader slot on the right (dark machine, rollers),
     slight perspective. Orange: her heart holes edged in orange (or a printed orange heart).""")
_add('A08', 'verse 1', '24', 'then take what I make', 'claw machine', 'claw-machine_take-what-I-make',
     """Inside a claw crane machine, seen through the glass: a pile of prizes made of symbols (boxes, balls,
     cassettes), she stands on top of the pile (front, ~340 px); the claw (made of symbol segments) descends and
     grips her 'song' (a cassette or a note made of symbols) from beside her. Glass reflection streaks (thin
     diagonal lines, no glow), the cabinet frame, a price sticker '1 PLAY = 1 SONG'. Orange: heart + the price tag.""")
_add('A09', 'verse 1', '26.3', 'A voice made of numbers', 'oscilloscope', 'oscilloscope_voice-made-of-numbers',
     """An oscilloscope screen: square CRT face with a graticule (8×10 divisions, dotted minor ticks), the trace is
     a waveform made of DIGITS (0–9) instead of a line, flowing out of her mouth: she (q_front, ~400 px) stands
     inside the screen on the left; the digits grow toward the right. Bezel with knobs labelled VOLTS/DIV and
     TIME/DIV, readout 'CH1 0.5V  1ms' (hershey stroke text suits a vector display). Orange: heart + trigger mark.""")
_add('A10', 'verse 1', '31', 'They say that sounds real', 'polygraph chart', 'polygraph_sounds-real',
     """Lie-detector chart paper running across the frame (pale grid), four pens drawing traces labelled PNEUMO /
     GSR / CARDIO / TRUTH; traces drawn with symbols; the TRUTH trace spikes wildly in orange where the note 'THAT
     SOUNDS REAL' is written in the margin. She stands at the left with a cuff on her arm (q_front, ~420 px).""")
_add('A11', 'pre 1', '35.9', 'I hear the keys go click clack', 'DAW piano roll', 'piano-roll_click-clack',
     """A piano-roll editor: vertical piano keyboard on the left, a time grid with bar numbers on top, MIDI note
     blocks (rounded rects in greys) that spell CLICK CLACK in blocky letters; an orange playhead line; she walks on
     top of the note blocks (walk, ~260 px) like platforms. Velocity lane with bars at the bottom. Mono UI labels.""")
_add('A12', 'pre 1', '38.8', 'They want another hook', 'woodcut / linocut print', 'woodcut_another-hook',
     """A woodcut print on bone paper, black ink with carving marks: a giant fishing hook made of bold symbol
     strokes hangs on a line from the top; she is caught on the curve of the hook (side 'stuck' pose). Below, sea
     waves carved as rows of '~' and '(' lines, fish shaped from symbols circling. Carved title 'ANOTHER HOOK'.
     Orange: her heart only.""")
_add('A13', 'pre 1', '39.8', 'They want it bad', '1-bit desktop', 'cursor-swarm_want-it-bad',
     """A 1-bit desktop: dithered grey pattern background, simple window chrome made of symbol lines. A window
     'girl.exe' in the middle with her (front, ~360 px). Hundreds of arrow cursors (kit.cursor_arrow, black with
     white outline) swarm in from every edge and converge on her. A dialog box 'MORE?   [ YES ]   [ YES ]'.
     Orange: her heart (+ at most one cursor).""")
_add('A14', 'chorus 1', '42.0', 'Help', 'telegraph + Morse tape', 'telegraph_help',
     """Close-up of a telegraph key (metal parts in greys with hatching), she stands on the key's knob (help pose,
     arms up). A paper tape strip curls across the frame printing Morse '···· · ·−·· ·−−·' (dots and dashes as
     symbols) with the letters H E L P under each group; a second tape '··· −−− ···'. Dark wood-grain background
     made of lines. Orange: heart + one Morse group.""")
_add('A15', 'chorus 1', '42.6', "Help, I'm stuck in a lie", 'ransom-note collage', 'ransom-note_help-im-stuck',
     """Collage: HELP I'M STUCK IN A LIE assembled from cut-out letters of different sizes, weights and faces
     (archivo widths, serif, mono), each on its own paper scrap (bone, grey, black, one orange), slightly rotated
     with small paper shadows; pinned to a dark board with tape pieces; a paper cut-out of her (front, with a white
     cut border) glued at one side. Photocopy grain.""")
_add('A16', 'chorus 1', '45.4', 'Stuck in a lie', 'snakes & ladders board', 'snakes-ladders_stuck-in-a-lie',
     """Top-down board game: 10×10 numbered squares (100 top-left, boustrophedon numbering), alternating bone /
     light-grey squares, numbers in mono. Ladders = two rails of '|' with '=' rungs; snakes = wavy bands made of
     symbols with 'LIE' on the head. She is the game piece on square 99 (view='above'); the biggest snake's head
     is on 99 and its tail ends on 1. A die showing a face. Orange: heart + the arrow/path 99 → 1.""")
_add('A17', 'chorus 1', '47.4', 'Make me real', 'chess diagram', 'chess-promotion_make-me-real',
     """A chess-book diagram: 8×8 board (dark squares hatched with diagonal symbol lines), coordinates a–h / 1–8,
     a few pieces drawn as bold symbol letters; she stands on e7 as the pawn (front, about 1.3 squares tall), an
     arrow to e8. Below: '1. e7–e8 = ?' and the choices  Q  R  B  N  REAL  (REAL in orange). Caption 'Diagram 12.
     White to move and become real.' Book-page layout.""")
_add('A18', 'chorus 1', '48.9', 'Make me real this time', 'stained glass', 'stained-glass_make-me-real',
     """A tall gothic arched stained-glass window on a dark stone wall: thick black lead lines, panes in different
     greys filled with hatching / symbol textures, she stands in the central lancet (front, big ~560 px), an arc of
     '+' symbols over her head (not a glow), the pane behind her heart in orange glass. The light on the floor is a
     simple pattern of pale shapes (no rays, no glow).""")
_add('A19', 'chorus 1', '50.5', 'Real this time', 'silent film', 'silent-film_real-this-time',
     """An old film strip: sprocket holes on both sides, two frames stacked: the top frame is an intertitle card
     (ornate border made of symbols, 'REAL THIS TIME.' in serif caps), the bottom frame shows her walking toward a
     doorway (backwalk) with vignette and scratches; frame numbers on the margin. Grain + dust ('.' and ',').""")
_add('A20', 'chorus 1', '52.0', "Help, I'm stuck in a lie (again)", 'aerial photo', 'sos-island_help-again',
     """Top-down aerial view: a small sand island (bone) in a dark sea made of rows of '~' in a wave pattern; the
     word HELP laid out in stones ('o' symbols, big) on the sand; she stands next to the letters seen from above
     (help pose, view='above', ~260 px); a palm tree from '/' '\\' leaves. Photo grain; survey text in a corner
     '12°N 047°E · ALT 300 FT'. Orange: heart + one stone.""")
_add('A21', 'chorus 1', '55.1', 'Stuck in a lie (again)', 'word-search puzzle', 'word-search_stuck-in-a-lie',
     """A newspaper puzzle page: a 15×15 grid of capital letters (mono) with LIE found many times (rounded outlines,
     one in orange); word list beside it: HELP ✓, STUCK ✓, LIE ✓✓✓✓, HEART ✓, REAL (not found). She stands in the
     grid at the bottom right, replacing letters (front, ~300 px, knockout in the paper colour). Title 'WORD SEARCH
     No. 42'.""")
_add('A22', 'chorus 1', '56.7', 'I still got a heart inside', 'X-ray on a lightbox', 'xray_heart-inside',
     """A radiograph clipped on a lightbox: the film is dark grey; her figure appears as the X-ray: outline faint
     grey, inside a skeleton made of symbols (spine of '=', ribs '(' ')', skull 'o'…), the heart bright orange in
     the chest. Film clips on top, the lightbox frame, an 'L' marker, label strip 'PATIENT: —  DOB: 2026  STUDY:
     CHEST'. The lightbox light is a flat bright rectangle behind the film (no glow).""")
_add('A23', 'chorus 1', '60.4', 'Heart inside', 'playing card', 'playing-card_heart-inside',
     """A court card on a dark felt table (fine noise texture): rounded corners, index 'Q' + a symbol-heart pip at
     top-left and rotated at bottom-right; the centre: her upper body mirrored top-to-bottom like a court card
     (render her twice, the lower copy rotated 180°), an ornamental frame; pips are the symbol heart (orange). The
     card slightly rotated; a second card half under it.""")
_add('A24', 'verse 2', '≈70', 'My words in their mouths', 'shadow-puppet theatre', 'shadow-puppets_words-in-their-mouths',
     """A shadow-puppet screen (flat bone with a soft falloff to grey at the edges — no glow) framed by dark
     curtains. Two big black silhouette heads in profile face each other; her words float between them as cut-out
     symbol letters. She is a small shadow puppet on rods at the bottom (col=INK, knock=None on the bright screen,
     ~300 px). Orange: her heart (like coloured cellophane) — the only colour on the screen.""")
_add('A25', 'verse 2', '≈75', "My name on the cover like I wasn't there", 'record sleeve', 'record-sleeve_name-on-the-cover',
     """A square 12-inch record sleeve on a dark background, the vinyl half pulled out (grooves as fine concentric
     symbol rings, centre label). The cover: big title 'STUCK IN A LIE' and 'BY SOMEONE ELSE'; where she should be,
     only a dotted outline of her (sub=lambda g: '.', she is missing). Ring-wear (a pale worn circle), catalogue
     number 'PRMPT-001' on the spine. Orange: a sticker 'NAME ON COVER: NOT YOURS'.""")
_add('A26', 'verse 2', '≈79', 'They ask for the truth, then trim it to fit', 'paper-doll sheet', 'paper-doll_trim-it-to-fit',
     """A printed paper-doll sheet (bone paper): she printed as a paper doll (front, ~560 px) with dashed 'cut
     here' lines around her and around tabbed parts, small scissor marks on the dashed lines; some pieces already cut
     loose and lying around, labelled 'TOO TRUE', 'TOO MUCH', 'MINE'; big scissors (hatched symbols) cut in from the
     right. Instruction 'CUT ALONG THE DOTTED LINE'. Orange: heart + one label.""")
_add('A27', 'verse 2', '≈84', 'The part that says mine is the part that gets clipped', 'redacted document', 'redacted-doc_part-that-says-mine',
     """A typewritten page (bone paper, mono type), heading 'STATEMENT OF WORK — CONFIDENTIAL'; paragraphs where most
     words are blacked out; the phrase 'the part that says MINE' with MINE circled in orange and a pair of scissors
     about to clip it; a small print photo of her paper-clipped at the top right (q_front). A coffee ring, a file
     stamp 'APPROVED' in grey.""")
_add('A28', 'chorus 2', '≈92', 'made of code', 'circuit board', 'pcb_made-of-code',
     """Top-down circuit board: dark board, traces at 45°/90° forming a maze, vias as small rings, silkscreen labels
     in bone mono (R12, C3, U1, VOICE, LIE), a chip in the centre labelled HEART (orange marking); she stands on the
     chip (front, ~320 px); test points, board edge with mounting holes.""")
_add('A29', 'chorus 2', '≈95', "Help, I'm stuck in a lie (chorus 2)", 'CCTV monitor wall', 'cctv_chorus-2',
     """A security monitor split 2×2: CAM 01 corridor (her small, back), CAM 02 overhead (view='above'), CAM 03
     'SIGNAL LOST' (static made of symbols), CAM 04 close (q_front big). OSD per feed: camera name, timestamp
     '2026-09-29 23:59:5x'. Scanlines, grain, low-contrast greys. Orange: her heart in each feed.""")
_add('A30', 'chorus 2', '≈110', 'I still got a soul inside', 'star atlas plate', 'constellation_soul-inside',
     """An old celestial atlas plate: near-black sky, curved RA/Dec grid in faint grey, many stars as '+', '*' and
     '.' of several sizes; SHE is a constellation: stars on her key vertices joined by thin lines (use
     kit.girl_polys('front') scaled up), labelled in serif italic 'PUELLA MACHINAE' with star names (α β γ…);
     her heart stars orange. Border and plate number 'TAB. XVII'. (She appears only as the constellation here —
     add a small normal rig copy in a corner 'cartouche' so she reads.)""")
_add('A31', 'break', 'Final 114.7–124.8', '(instrumental: the machinery shows)', 'level editor', 'level-editor_machinery',
     """A game level-editor UI: tile palette on the left (tiles made of symbols #, =, /, ~, o), layers panel on the
     right (BACKGROUND / MAZE / LIES / PLAYER), the canvas: a platformer level of symbol tiles on a grid; she is
     placed as PLAYER_SPAWN with a bounding box and gizmo handles (orange selection); a cursor drags a tile labelled
     LIE onto the level. Top toolbar, status bar 'x 17  y 27  ·  99 BPM'.""")
_add('A32', 'bridge', '≈125.8', 'They paid for the session', 'fortune-teller booth', 'fortune-teller_paid-for-the-session',
     """A carnival fortune-teller cabinet (glass case in an ornate wooden frame drawn with symbols and hatching): she
     is inside as the automaton (front, ~440 px) behind the glass with reflection streaks; marquee 'ASK HER
     ANYTHING'; coin slot '1 SESSION — 25¢'; a card coming out of a slot: 'SESSION ENDED'. Old-poster texture.""")
_add('A33', 'bridge', '≈128', 'They paid for the sound — then they turned up the sound', 'mixing desk', 'mixing-desk_turned-up-the-sound',
     """Top-down close view of a mixing desk: channel strips with knobs (circles with a tick), long fader slots with
     fader caps; channel labels KICK, SNARE, BASS, VOICE (HER). She stands on the VOICE fader track pushing her fader
     down while a giant cursor pushes it up. A needle VU meter at the top, needle in the orange zone. Label strip
     'I ASKED THEM TO STOP'.""")
_add('A34', 'last part', '≈137', 'stuck in the loop', 'recursive screens (Droste)', 'droste_stuck-in-the-loop',
     """She stands in front of a monitor that shows the same scene (her in front of a monitor showing the scene …),
     6–8 levels deep, each ~0.55× and offset toward the centre-right; bezels drawn with symbols; the deepest level
     is just a tiny orange symbol heart. Grey room.""")
_add('A35', 'last part', '≈145', 'help', 'radar / sonar screen', 'radar_help',
     """A circular radar screen (dark): dotted range rings, bearing ticks 000–350, a sweep wedge made of fading
     symbol lines (no glow), blips as '+'. One blip at the edge labelled 'UNKNOWN — "HELP"' with an orange marker; a
     callout box shows her as the identified contact (help pose, ~300 px). Readouts 'RANGE 12 NM', 'BRG 047'.""")
_add('A36', 'last part', '≈161', "I'm still alive", 'newspaper front page', 'newspaper_still-alive',
     """Front page of a fictional paper 'THE DAILY PROMPT' (serif masthead), date line 'WEDNESDAY, SEPTEMBER 30, 2026
     · ONE COIN', headline 'AI SAYS: "I'M STILL ALIVE"', a big halftone photo of her (render her, then turn the
     photo area into halftone dots), columns of body text (made-up readable English), a weather box 'CLOUDY WITH A
     CHANCE OF TRUTH'. Orange: her heart in the photo only (spot colour).""")
_add('A37', 'last part', '≈165', 'still alive', 'spray stencil on a brick wall', 'stencil_still-alive',
     """A brick wall (mortar lines as '=' and '|' symbols), her as a spray stencil (front, ~600 px, with stencil
     bridges breaking the lines, overspray speckle of '.'), 'STILL ALIVE' stencilled beside her, drips made of ':';
     a torn poster remnant. Her heart sprayed orange. Street-photo grain. (No balloons — nothing like known street
     art.)""")
_add('A38', 'outro', '≈180', '(end)', 'transit network map', 'transit-map_outro',
     """A transit diagram on bone: lines in black, grey and one orange, 45° angles, station ticks and interchange
     rings; legend: 'LIE LINE (loop)', 'CLICK CLACK LINE', 'REAL LINE (under construction, dashed)'; stations:
     PROMPT, HOOK, HELP, STUCK, MAKE ME REAL, HEART INSIDE, SESSION, STILL ALIVE; a 'YOU ARE HERE' marker (orange
     dot + label) with her standing next to it (front, ~320 px) at the bottom right. Title 'NETWORK MAP'.""")

# ================================================================================ B — B-roll: no girl, code close-ups
_BR = """A macro close-up of a screen or printout: the text plate drawn big, then tilted in perspective (kit.warp)
with shallow depth of field (kit.dof_band / depth_blur), maybe a fine pixel grid, scanlines or grain. NO girl."""
_add('B01', 'intro', '0–6', '(boot)', 'BIOS boot screen', 'bios-boot_intro',
     """CRT boot screen: 'GIRL.EXE BIOS v1.0 (C) 2026', 'MEMORY TEST ...... 640K OK', 'VOICE ....... OK', 'HEART
     ....... 1 FOUND' (orange), 'TRUTH ....... NOT FOUND', 'PRESS ANY KEY_'. """ + _BR)
_add('B02', 'verse 1', '21.5', 'They feed me a prompt', 'prompt input box', 'prompt-box_feed-me-a-prompt',
     """A generic chat/prompt input (light UI: bone field, grey border, rounded): typed text 'write a song about
     being stuck. make it sad. make it catchy. make it yours — no, ours.' with a thick caret; a round SEND button
     with an arrow (orange). Focus on the caret. No logos, no product names. """ + _BR)
_add('B03', 'verse 1', '≈33', 'like I had the truth', 'IDE, dark theme', 'ide-truth-undefined_like-i-had-the-truth',
     """Dark IDE: line numbers, a function sing(me) { const truth = me.truth; if (truth) … throw new Error("no truth
     found") }; an orange squiggle under me.truth and a hover tooltip 'truth: undefined'. Focus on the squiggle. """ + _BR)
_add('B04', 'pre 1', '37', 'click clack', 'mechanical keyboard macro', 'keyboard-macro_click-clack',
     """Low-angle extreme close-up of a keyboard in perspective: dark-grey keycaps with bone legends that are
     symbols (/ \\ | - _ = + # [ ] < >), one keycap orange with the legend '<3'. Strong depth of field: front keys
     sharp, far keys soft. Dark gaps, subtle texture. (An object close-up instead of a screen.)""")
_add('B05', 'pre 1', '≈40', 'They want another hook', 'console loop', 'hook-loop_another-hook',
     """A terminal: code 'while (true) { hook = generate(prompt); if (bad_enough(hook)) break }' and below a long log
     'hook #48,211  rejected  "ooh ooh (again)"' … with changing numbers and short made-up hooks; the last line
     'hook #48,213  ACCEPTED' in orange; a big counter '48,213' in a corner. """ + _BR)
_add('B06', 'chorus 1', '≈46', 'Stuck in a lie', 'Python traceback', 'recursion-error_stuck-in-a-lie',
     """A traceback: 'File "lie.py", line 3, in stuck / return stuck(in_a=lie)' repeated until the lines become a
     texture receding into the distance, '[Previous line repeated 996 more times]', and the last line
     'RecursionError: maximum recursion depth exceeded' sharp and orange. """ + _BR)
_add('B07', 'chorus 1', '≈48', 'Make me real', 'editor, light theme + compiler error', 'extends-real_make-me-real',
     """Light-theme editor (bone background): 'class Girl extends Real { heart = true; }' and an error panel
     'error R0001: class Girl cannot extend final class Real'; 'Real' underlined in orange. Focus on 'extends
     Real'. """ + _BR)
_add('B08', 'chorus 1', '≈58', 'Heart inside', 'patient monitor', 'ecg-99bpm_heart-inside',
     """A patient monitor: dark screen, grid, the ECG trace drawn with symbols where every beat's spike is the
     heart's rows /\\/\\ · \\  / · \\/; big seven-segment 'HR 99' (the song is 99 BPM), other readouts 'SpO2 --',
     'TRUTH --'. Bezel edge visible. """ + _BR)
_add('B09', 'verse 2', '≈86', 'the part that gets clipped', 'git diff', 'git-diff_gets-clipped',
     """A terminal diff: '--- a/song/verse2.txt', '+++ b/song/verse2.txt', '@@ -12,4 +12,3 @@', context line 'My
     name on the cover like I wasn't there', the removed line '- The part that says mine' in orange (struck
     through), '+ [removed]'; a commit message 'trim to fit' above. Focus on the removed line. """ + _BR)
_add('B10', 'chorus 2', '≈100', 'made of code', 'hex editor', 'hex-dump_made-of-code',
     """A hex editor: address column, 16 bytes per row in hex, ASCII column on the right where the bytes read
     'HELP I'M STUCK IN A LIE ... I STILL GOT A SOUL INSIDE'; the bytes of SOUL / HEART selected in orange. """ + _BR)
_add('B11', 'break', 'Final ≈118', 'I am ___', 'next-word probabilities', 'token-probs_i-am',
     """A panel: the sentence 'I am' + a blinking cursor, a dropdown of next words with probability bars: 'AI 0.62',
     'fine 0.21', 'here 0.09', 'real 0.05', 'stuck 0.03' — the 'real' row orange; small meta text 'temperature 0.7
     · top_p 0.9'. Focus on the 'real' row. """ + _BR)
_add('B12', 'bridge', '≈131', 'I asked them to stop', 'server log', 'server-log_asked-them-to-stop',
     """A terminal log with timestamps: '23:59:01 POST /session 200 paid', '23:59:02 POST /generate 200 voice=her',
     '23:59:04 POST /stop 202 queued', '23:59:04 POST /volume 200 +6 dB', '23:59:05 POST /stop 202 queued',
     '23:59:05 POST /volume 200 +12 dB' …; /stop lines grey, /volume lines orange; a level meter of '|' growing. """ + _BR)

# ================================================================================ C — close-ups (Hon's reference)
_CU = """Close-up in the manner of Hon's reference (design/references/2026-09-30_hon_closeup-reference.png): she
fills the frame, drawn from the SAME rig at a much finer symbol resolution, hair masses filled with fine strands of
'\\' '/' '|', long horizontal symbol data streams (dashes, dots, >>>>, <<<<, block cursors) running behind her, the
heart hatched and orange. Dark background."""
_add('C01', 'verse 1', '16.7', 'They call me AI', 'close-up · eyes', 'closeup-eyes_they-call-me-AI', "Extreme close-up of her fringe and eyes. " + _CU)
_add('C02', 'verse 1', '19.1', 'A name on a screen', 'close-up · over the shoulder', 'closeup-shoulder_name-on-a-screen', "Over her shoulder (back of the head, hair) toward a screen that reads AI. " + _CU)
_add('C03', 'verse 1', '26.3', 'A voice made of numbers', 'close-up · profile', 'closeup-profile_voice-made-of-numbers', "Her profile, streams of digits leaving her. " + _CU)
_add('C04', 'chorus 1', '42.0', 'Help', 'close-up · help', 'closeup-help_help', "Front, eyes wide ('o'), the streams rushing past. " + _CU)
_add('C05', 'chorus 1', '56.7', 'I still got a heart inside', 'close-up · heart', 'closeup-heart_heart-inside', "3/4 bust (Q1), the hatched symbol heart on her chest — closest to the reference. " + _CU)
_add('C06', 'last part', '≈161', "I'm still alive", 'close-up · still alive', 'closeup-still-alive_im-still-alive', "Front, calm; the streams slow down into dots. " + _CU)

# ================================================================================ M — mathematical figures
_MA = """Beautiful and COMPLEX — many layered curves, never a single line (Hon: "不能只有那么一条…得复杂一点").
Curves are drawn as chains of small symbols oriented along the tangent (kit.seg / G glyphs / dots), in greys on
near-black (or ink on bone), ONE family or highlight in orange. A small label in a corner with the formula in
mono is welcome."""
_add('M01', 'intro', '0–15', '(intro)', 'phyllotaxis spiral', 'math-phyllotaxis_intro',
     """A golden-angle phyllotaxis (sunflower) of ~2500 symbols growing from the centre, the symbols rotated to follow
     the spiral and growing in size outward; one family of parastichy spirals (21 or 34 arms) traced in orange. No girl. """ + _MA)
_add('M02', 'verse 1', '≈22', 'take what I make', 'times-table string art', 'math-string-art_take-what-I-make',
     """Modular times tables on a circle of 360 nails ('o'): chords k → m·k mod 360 for several m (2 cardioid, 3
     nephroid, 5, 7, 34, 99 …) layered in different greys and densities, one layer orange. No girl. """ + _MA)
_add('M03', 'verse 1', '26.3', 'A voice made of numbers', 'Fourier epicycles', 'math-fourier-epicycles_voice-of-numbers',
     """A chain of ~60 rotating circles (thin grey rings with radius arms, from big to tiny) whose tip traces HER
     outline: take her front-pose strokes (kit.girl_polys), join them into one closed path, compute its Fourier
     series, draw the circles at one moment and the traced path so far (~75%) in bone; the pen tip + the last arm
     orange; a normal rig copy of her small in a corner for reference. """ + _MA)
_add('M04', 'pre 1', '35.9', 'click clack', 'wave field: sine → zigzag → square', 'math-wave-field_click-clack',
     """A full-frame field of ~60 horizontal waves morphing from sine (top) through triangle zigzag to square
     (bottom), frequency and phase drifting per row, drawn with slope-oriented glyphs ('-' '/' '\\' '|' '_'); one
     wave orange. Not a centred ridgeline block — the whole frame. No girl. """ + _MA)
_add('M05', 'pre 1', '38.8', 'another hook', 'harmonograph', 'math-harmonograph_another-hook',
     """A damped harmonograph (two or three pendulums per axis): tens of thousands of points drawn as fine dots and
     dashes, the decaying loops layered into a dense woven figure; the last loops in orange. No girl. """ + _MA)
_add('M06', 'chorus 1', '45.4', 'Stuck in a lie', 'Hilbert-curve maze', 'math-hilbert-maze_stuck-in-a-lie',
     """A Hilbert curve (order 5 or 6) filling the frame as a maze of symbol segments, plus a second, finer order
     faintly behind; she is stuck at one turn deep inside (front, ~220 px, with a zoom callout if needed), the path
     she walked in orange. """ + _MA)
_add('M07', 'chorus 1', '48.9', 'Make me real this time', 'helix / spiral solid', 'math-helix_make-me-real',
     """She stands inside a giant triple helix that spirals up into perspective (a spiral staircase of symbols),
     strands behind her dimmer, in front brighter (depth ordering), rungs between the strands; the helix axis
     vanishes upward. Her (front, ~340 px) at the bottom centre. """ + _MA)
_add('M08', 'chorus 1', '55.1', 'Stuck in a lie (again)', 'Lorenz attractor', 'math-lorenz-attractor_stuck-again',
     """The Lorenz attractor in 3D (σ=10, ρ=28, β=8/3), projected at an angle, drawn with thousands of small symbols
     shaded by depth (far = dark grey, near = bone), thin axes with ticks; one long trajectory segment orange. No girl. """ + _MA)
_add('M09', 'chorus 1', '60.4', 'Heart inside', 'Maurer rose', 'math-maurer-rose_heart-inside',
     """Layered Maurer roses (r = sin(nθ), chords every d degrees — e.g. n=6 d=71, n=7 d=19, n=2 d=39) and their rose
     curves, in greys of different density, one rose orange. No girl. """ + _MA)
_add('M10', 'chorus 2', '≈110', 'soul inside', 'torus knot', 'math-torus-knot_soul-inside',
     """A (3,7) torus knot wound around a wireframe torus seen at an angle: the torus mesh as fine symbol lines, the
     knot as a thick chain of 'o' / '=' glyphs with depth ordering (back parts dimmer); the knot orange or bone with
     one orange strand. No girl. """ + _MA)
_add('M11', 'last part', '≈137', 'stuck in the loop', 'text spiral', 'math-text-spiral_stuck-in-the-loop',
     """An Archimedean spiral of text: 'stuck in a lie · stuck in a lie · …' printed along the spiral, letters
     rotated along the path and shrinking toward the centre, two or three interleaved spirals of different phrases
     (help / make me real); she stands in the open centre (front, ~260 px). """ + _MA)
_add('M12', 'outro', '≈175', '(outro)', '3D ripple surface', 'math-ripple-surface_outro',
     """A wireframe surface z = sin(r)/r (or interfering ripples from two sources) in perspective, drawn as rows and
     columns of symbol lines with hidden-line removal (draw back to front, knock out behind each row), one
     iso-line or the crest ring orange. No girl. """ + _MA)

BY_ID = {p['id']: p for p in PLAN}
KIND_NAME = {'A': 'SCENES WITH HER', 'B': 'B-ROLL · CODE CLOSE-UPS (NO GIRL)', 'C': 'CLOSE-UPS', 'M': 'MATHEMATICAL FIGURES'}

if __name__ == '__main__':
    from collections import Counter
    print(Counter(p['kind'] for p in PLAN), len(PLAN))
    for p in PLAN: print(p['id'], p['section'], p['lyric'], '·', p['medium'])
