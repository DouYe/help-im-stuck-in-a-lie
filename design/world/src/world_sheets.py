"""Reference sheets for the world style: palette.png, symbols.png, ui_kit_proposed.png.
Run from the project root:  python3 design/world/src/world_sheets.py
Uses the girl's glyph drawer (design/character/src) and the app's fonts; the UI kit is cropped from the
keyframes in design/keyframes/."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'character', 'src'))
from PIL import Image, ImageDraw, ImageFont
import final_sheet as fs

SS = fs.SS
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
OUT = os.path.join(ROOT, 'design', 'world')
INK = (10, 10, 11); INK2 = (22, 22, 24); GR = (94, 91, 87); ASH = (156, 151, 143); BONE = (238, 233, 223); SIG = (255, 83, 20)
def mono(bold, s): return ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf' if bold else 'IBMPlexMono-Regular.ttf'), s)
def title(s): return ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), s)


def palette():
    W, H = 1800, 760
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    d.text((60, 40), 'PALETTE  ·  LOCKED', font=title(48), fill=BONE)
    d.text((60, 104), 'black, white, one orange. the orange is her heart (and, sparingly, lives in the HUD). no other hues, no gradients, no glow.', font=mono(0, 20), fill=ASH)
    sw = [('ink', '#0A0A0B', INK, 'background, everything dark'), ('ink2', '#161618', INK2, 'panels (status bar, dialog bg)'),
          ('graphite', '#5E5B57', GR, 'far field, dim symbols, hatching'), ('ash', '#9C978F', ASH, 'secondary text, labels'),
          ('bone', '#EEE9DF', BONE, 'the girl, walls, text (never pure white)'), ('signal orange', '#FF5314', SIG, 'the heart ONLY (+ HUD lives)')]
    f = mono(0, 17)
    for i, (n, hx, c, use) in enumerate(sw):
        x = 60 + i * 285; y = 170
        d.rectangle([x, y, x + 250, y + 300], fill=c, outline=GR if c in (INK, INK2) else None, width=2)
        d.text((x, y + 320), n, font=mono(1, 24), fill=BONE); d.text((x, y + 356), hx, font=mono(0, 22), fill=ASH)
        line, yy = '', y + 392
        for w in use.split():
            if d.textlength(line + ' ' + w, font=f) > 250: d.text((x, yy), line.strip(), font=f, fill=ASH); yy += 24; line = ''
            line += ' ' + w
        d.text((x, yy), line.strip(), font=f, fill=ASH)
    d.text((60, H - 60), 'post: bloom 0 · halation 0 · chromatic aberration 0 · grain ~0.03 · vignette ~0.2 · (paper frames invert: bone background, ink symbols)', font=mono(0, 18), fill=GR)
    im.save(os.path.join(OUT, 'palette.png'))


def symbols():
    W, H = 1800, 1220
    im = Image.new('RGB', (W * SS, H * SS), INK); d = ImageDraw.Draw(im)
    def T(x, y, s, f, c=BONE): d.text((x * SS, y * SS), s, font=f, fill=c)
    fH, fL = mono(1, 24 * SS), mono(0, 17 * SS)
    T(60, 40, 'THE SYMBOL VOCABULARY', title(48 * SS))
    T(60, 104, 'everything on screen is drawn from these strokes (app/src/game/glyph.ts = design/character/src/glyphs.py). one symbol per grid cell.', fL, ASH)
    groups = [('HER  ·  locked (the rig picks these by stroke direction)', ['|', '-', '_', '`', '/', '\\', '+', 'o', '>'], ['vertical', 'centre', 'low', 'high', 'diag', 'diag', 'crossing', 'open eye', 'nose']),
              ('WALLS · FLOORS · BRICKS  ·  proposed', ['|', '-', '=', '+', '#', '[', ']', '_'], ['wall', 'wall', 'ground', 'corner', 'ceiling', 'brick', 'brick', 'ledge']),
              ('HAZARDS · BULLETS  ·  proposed', ['^', 'v', 'x', 'o', '<', '>'], ['spike up', 'spike down', 'bullet', 'bullet', 'arrow', 'arrow']),
              ('TRAILS · CODE · MARKS  ·  proposed', ['.', ':', '0', '1', '(', ')', "'", ','], ['trail', 'trail', 'code', 'code', 'pit', 'pit', 'tick', 'tick'])]
    y, rows_y = 170, []
    for head, gl, labs in groups:
        T(60, y, head, fH); rows_y.append(y); y += 50
        for i, (g, lab) in enumerate(zip(gl, labs)):
            x = 60 + i * 190
            d.rectangle([x * SS, y * SS, (x + 120) * SS, (y + 120) * SS], outline=GR, width=SS)
            fs.glyph(d, g, x + 10, y + 10, 100, 100, BONE, 5)
            T(x, y + 130, g, fH, ASH); T(x + 40, y + 134, lab, fL, GR)
        y += 200
    hx0, hy0 = 1330, rows_y[2]
    T(hx0, hy0, 'THE HEART  ·  locked', fH, SIG)
    for r, row in enumerate(fs.HEART):
        for c, g in enumerate(row):
            if g != ' ': fs.glyph(d, g, hx0 + 40 + c * 60, hy0 + 60 + r * 60, 60, 60, SIG, 5)
    T(hx0, hy0 + 260, 'orange, 4 x 3 cells:  /\\/\\  \\  /   \\/', fL, ASH)
    T(60, H - 60, "legacy glyph '*' draws a heart OUTLINE - do not use it: the heart is always the 3-row symbol heart.", fL, GR)
    im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, 'symbols.png'))


def ui_kit():
    K = os.path.join(ROOT, 'design', 'keyframes')
    op = lambda n: Image.open(os.path.join(K, n)).convert('RGB')
    kf1, kf2, kf3, kf4 = op('KF1_click-clack_platformer.png'), op('KF2_help_bricks.png'), op('KF3_stuck-in-a-lie_maze.png'), op('KF4_make-me-real_corridor.png')
    W, H = 1920, 1260
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    d.text((60, 36), 'UI KIT  ·  PROPOSED (keyframes v2, not yet approved)', font=title(44), fill=BONE)
    lab = mono(1, 22)
    def put(img, box, xy, t):
        im.paste(img.crop(box), xy); d.text((xy[0] + 10, xy[1] - 32), t, font=lab, fill=SIG)
    put(kf1, (0, 0, 1920, 110), (0, 150), 'TOP HUD  ·  lives as symbol hearts · stage name · song time · bar/beat   (world.ts hud)')
    put(kf1, (240, 870, 1690, 1030), (0, 330), 'DIALOG  ·  types the sung line; the word being sung is inverted   (world.ts dialog)')
    put(kf2, (240, 870, 1690, 1030), (0, 560), 'DIALOG on a paper (inverted) level')
    put(kf4, (0, 925, 1920, 1080), (0, 790), 'STATUS BAR (3D levels)  ·  HEART · REALITY meter · her face (glances) · FLOOR · KEYS   (kf_ray.ts)')
    put(kf3, (1640, 860, 1905, 1010), (0, 1020), 'MINIMAP')
    put(kf1, (420, 640, 1560, 790), (330, 1020), 'WORDS AS LEVEL GEOMETRY  ·  key-caps / bricks / outlined blocks  (world.ts)')
    d.text((10, 1200), 'Everything is symbols; UI text is IBM Plex Mono Bold, titles Archivo Expanded Black. Orange stays on the hearts.', font=mono(0, 20), fill=ASH)
    im.save(os.path.join(OUT, 'ui_kit_proposed.png'))


if __name__ == '__main__':
    palette(); symbols(); ui_kit(); print('wrote palette.png, symbols.png, ui_kit_proposed.png to', OUT)
