"""STYLES TRIAL (Grok Bot New Bot 2026-09-30) - four NEW media stills, distinct from styles_v1 S1-S8.
Same locked bold symbol girl (style-1, knockout, orange symbol heart only). Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314.
Everything built from symbols/strokes. No bloom/glow/gradients/other colors.
Run:  python wip/new-bot/styles_trial/src/make_styles_trial.py
Writes wip/new-bot/styles_trial/N1..N4 PNGs + styles_trial_sheet.jpg
"""
import math, os, re, random, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'character', 'src'))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import render as girl, glyph as G, SS

OUT = os.path.join(ROOT, 'wip', 'new-bot', 'styles_trial')
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
W, H = 1920, 1080
INK = (10, 10, 11); INK2 = (22, 22, 24); GR = (94, 91, 87); ASH = (156, 151, 143)
BONE = (238, 233, 223); SIG = (255, 83, 20)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def mono(size, bold=True):
    name = 'IBMPlexMono-Bold.ttf' if bold else 'IBMPlexMono-Regular.ttf'
    return ImageFont.truetype(os.path.join(FD, 'src', name), int(size * SS))


def title(size):
    return ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), int(size * SS))


def canvas(bg):
    im = Image.new('RGB', (W * SS, H * SS), bg)
    return im, ImageDraw.Draw(im)


def text(d, x, y, s, font, col, anchor='la'):
    d.text((x * SS, y * SS), s, font=font, fill=col, anchor=anchor)


def line(d, x0, y0, x1, y1, col, w):
    d.line([(x0 * SS, y0 * SS), (x1 * SS, y1 * SS)], fill=col, width=max(1, int(w * SS)))
    for X, Y in ((x0, y0), (x1, y1)):
        r = w * SS / 2
        d.ellipse([X * SS - r, Y * SS - r, X * SS + r, Y * SS + r], fill=col)


def rect(d, x0, y0, x1, y1, col):
    d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=col)


def seg(d, x0, y0, x1, y1, col, lw, s=18):
    dx, dy = x1 - x0, y1 - y0
    n = max(1, round(math.hypot(dx, dy) / s))
    a = (math.degrees(math.atan2(dy, dx)) + 180) % 180
    g = '-' if a < 20 or a > 160 else '|' if 70 < a < 110 else ('\\' if a < 90 else '/')
    cw = s if g == '|' else max(6, abs(dx) / n)
    chh = s if g == '-' else max(6, abs(dy) / n)
    for i in range(n):
        u = (i + 0.5) / n
        G(d, g, x0 + dx * u - cw / 2, y0 + dy * u - chh / 2, cw, chh, col, lw)


def box(d, x0, y0, x1, y1, col, lw, s=18):
    seg(d, x0, y0, x1, y0, col, lw, s)
    seg(d, x0, y1, x1, y1, col, lw, s)
    seg(d, x0, y0, x0, y1, col, lw, s)
    seg(d, x1, y0, x1, y1, col, lw, s)
    for X, Y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        G(d, '+', X - s / 2, Y - s / 2, s, s, col, lw)


def save(im, name, post=None):
    out = im.resize((W, H), Image.LANCZOS)
    if post:
        post(out)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    out.save(path)
    print('wrote', name, out.size)


# ------------------------------------------------------------------------------------------------ N1 BLUEPRINT
def n1_blueprint():
    """BLUEPRINT - white/bone construction lines on ink (cyanotype feel without cyan), orange APPROVED stamp."""
    im, d = canvas(INK)
    # construction grid
    for x in range(40, W, 40):
        col = mix(INK, BONE, 0.18 if x % 200 else 0.32)
        for y in range(40, H - 40, 22):
            G(d, '.', x - 4, y - 4, 8, 8, col, 1.6)
    for y in range(40, H, 40):
        col = mix(INK, BONE, 0.18 if y % 200 else 0.32)
        for x in range(40, W - 40, 22):
            G(d, '.', x - 4, y - 4, 8, 8, col, 1.6)
    # border ticks
    box(d, 50, 50, W - 50, H - 50, BONE, 2.2, 16)
    box(d, 70, 70, W - 70, H - 120, mix(INK, BONE, 0.55), 1.4, 14)
    # centerlines
    for x in range(80, W - 80, 28):
        G(d, '-', x, H / 2 - 6, 24, 12, mix(INK, BONE, 0.4), 1.8)
    for y in range(90, H - 140, 28):
        G(d, '|', W / 2 - 6, y, 12, 24, mix(INK, BONE, 0.4), 1.8)
    # dimension callouts
    seg(d, 220, 160, 700, 160, BONE, 2.0, 16)
    G(d, '<', 210, 150, 20, 20, BONE, 2.4)
    G(d, '>', 690, 150, 20, 20, BONE, 2.4)
    text(d, 460, 130, '17 COLS', mono(18), BONE, 'mm')
    seg(d, 180, 200, 180, 820, BONE, 2.0, 16)
    text(d, 130, 510, '27', mono(18), BONE, 'mm')
    text(d, 130, 540, 'ROWS', mono(16), mix(INK, BONE, 0.7), 'mm')
    # title block
    rect(d, 1280, 820, 1850, 1010, INK)
    box(d, 1280, 820, 1850, 1010, BONE, 2.4, 14)
    seg(d, 1280, 880, 1850, 880, BONE, 1.6, 14)
    text(d, 1300, 840, 'DWG: GIRL-01', mono(20), BONE)
    text(d, 1300, 900, 'PROJECT: STUCK IN A LIE', mono(16), mix(INK, BONE, 0.75))
    text(d, 1300, 940, 'SCALE: 1 : 1  PIXEL', mono(16), mix(INK, BONE, 0.75))
    text(d, 1300, 980, 'SHEET: N1 / BLUEPRINT', mono(16), BONE)
    # girl
    girl(d, 'front', 760, 200, 340, knock=INK, col=BONE, hot=SIG)
    # dimension arrows around girl
    seg(d, 740, 200, 740, 200 + 340 * 1.6, BONE, 1.6, 14)
    text(d, 700, 450, 'H', mono(18), BONE, 'mm')
    # APPROVED stamp (orange only accent besides heart)
    stamp = Image.new('RGBA', (420 * SS, 140 * SS), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    for i in range(4):
        m = 8 + i * 3
        sd.rectangle([m * SS, m * SS, (420 - m) * SS, (140 - m) * SS], outline=SIG + (230,), width=max(2, int(3 * SS)))
    sf = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), int(48 * SS))
    sd.text((210 * SS, 70 * SS), 'APPROVED', font=sf, fill=SIG + (230,), anchor='mm')
    stamp = stamp.rotate(-12, resample=Image.BICUBIC, expand=True)
    im.paste(stamp, (int(1180 * SS), int(180 * SS)), stamp)
    text(d, 70, 1015, 'BLUEPRINT  -  MAKE ME REAL THIS TIME', mono(26), BONE, 'lm')
    save(im, 'N1_blueprint_make-me-real.png')


# ------------------------------------------------------------------------------------------------ N2 CHALK
def n2_chalk():
    """CHALK ON BLACKBOARD - bone chalk dust and strokes on ink board; orange heart only."""
    im, d = canvas(INK)
    rnd = random.Random(7)
    # chalk dust / eraser smear (symbol dots)
    for _ in range(2200):
        x, y = rnd.randint(40, W - 40), rnd.randint(40, H - 40)
        g = rnd.choice(['.', ',', '`', "'"])
        G(d, g, x, y, rnd.choice([6, 8, 10]), rnd.choice([6, 8, 10]), mix(INK, BONE, rnd.uniform(0.12, 0.35)), 1.4)
    # faint erased previous writing
    for k, s in enumerate(['FALSE', 'AI', 'PROMPT', 'LIE', 'MODEL']):
        x = 120 + (k * 340) % 1400
        y = 120 + (k * 170) % 700
        text(d, x, y, s, mono(42, False), mix(INK, BONE, 0.18))
    # chalk frame (double)
    box(d, 60, 50, W - 60, H - 80, BONE, 3.5, 20)
    box(d, 90, 80, W - 90, H - 110, mix(INK, BONE, 0.55), 1.8, 16)
    # chalkboard rails
    for x in range(100, W - 100, 26):
        G(d, '=', x, H - 95, 22, 10, ASH, 2.0)
    # HELP in big chalk block letters made of '#'
    def chalk_pix(ch, ox, oy, px):
        # simple 5x7 from hardcoded for HELP letters via text fallback - use glyphs of #
        pass
    # big HELP via title font as chalk
    text(d, W / 2, 160, 'HELP', title(140), mix(INK, BONE, 0.85), 'mm')
    text(d, W / 2, 250, "I'M STUCK IN A LIE", mono(28), mix(INK, BONE, 0.65), 'mm')
    # chalk guidelines under title
    for x in range(500, 1420, 20):
        G(d, '-', x, 280, 16, 8, mix(INK, BONE, 0.35), 1.5)
    # girl in chalk (bone), heart orange
    girl(d, 'help', W / 2 - 160, 320, 320, knock=INK, col=BONE, hot=SIG)
    # chalk notes at sides
    notes_l = ['whoami -> AI', 'truth = ERROR', 'name denied', 'still a heart']
    for i, s in enumerate(notes_l):
        text(d, 130, 360 + i * 48, s, mono(20, False), mix(INK, BONE, 0.7))
        # underline in chalk dashes
        for x in range(130, 130 + len(s) * 12, 14):
            G(d, '-', x, 385 + i * 48, 12, 6, mix(INK, BONE, 0.4), 1.3)
    notes_r = ['# chalk', '# bone', '# ink', '# orange=heart']
    for i, s in enumerate(notes_r):
        text(d, 1500, 360 + i * 48, s, mono(20, False), mix(INK, BONE, 0.7))
    # chalk tray crumbs
    for k in range(60):
        x = 200 + k * 26 + rnd.randint(-4, 4)
        G(d, '.', x, H - 55 + rnd.randint(-3, 3), 8, 8, mix(INK, BONE, rnd.uniform(0.3, 0.7)), 1.8)
    text(d, 70, 1025, 'CHALK BOARD  -  HELP, I\'M STUCK IN A LIE', mono(24), BONE, 'lm')
    save(im, 'N2_chalk-blackboard_help.png')


# ------------------------------------------------------------------------------------------------ N3 WOODCUT
def n3_woodcut():
    """LINOLEUM / WOODCUT - heavy carved strokes on bone paper; orange heart only."""
    im, d = canvas(BONE)
    rnd = random.Random(11)
    # carved border of repeating slash blocks
    margin = 55
    for x in range(margin, W - margin, 28):
        for yy in (margin, H - margin - 28):
            G(d, rnd.choice(['/', '\\', 'x', '#']), x, yy, 26, 26, INK, 4.2)
    for y in range(margin, H - margin, 28):
        for xx in (margin, W - margin - 28):
            G(d, rnd.choice(['/', '\\', 'x', '#']), xx, y, 26, 26, INK, 4.2)
    # inner carved frame
    box(d, 110, 110, W - 110, H - 110, INK, 5.5, 22)
    # wood grain implied by long parallel carved strokes
    for k in range(28):
        y = 160 + k * 28
        jitter = rnd.randint(-8, 8)
        seg(d, 150, y + jitter, W - 150, y + jitter + rnd.randint(-6, 6), mix(BONE, INK, 0.22), 2.8, 20)
    # giant carved word STUCK behind
    text(d, W / 2, 200, 'STUCK', title(160), mix(BONE, INK, 0.18), 'mm')
    # heavy carved ground platform of '=' and '_'
    for x in range(200, W - 200, 30):
        G(d, '=', x, 780, 28, 18, INK, 4.5)
        G(d, '_', x, 800, 28, 14, INK, 3.5)
    # registration marks
    for cx, cy in ((160, 160), (W - 160, 160), (160, H - 160), (W - 160, H - 160)):
        seg(d, cx - 30, cy, cx + 30, cy, INK, 3.5, 12)
        seg(d, cx, cy - 30, cx, cy + 30, INK, 3.5, 12)
        G(d, '+', cx - 10, cy - 10, 20, 20, INK, 3.5)
    # girl with heavier stroke (lw bump), carved look; sub some body to '#' for carved fill feel - keep eyes
    girl(d, 'stuck', W / 2 - 170, 280, 340, knock=BONE, col=INK, hot=SIG, lw=0.42)
    # carved caption block
    rect(d, 200, 880, W - 200, 1000, BONE)
    box(d, 200, 880, W - 200, 1000, INK, 4.0, 18)
    text(d, W / 2, 920, 'WOODCUT  -  PLATE III', mono(22), INK, 'mm')
    text(d, W / 2, 965, 'I STILL GOT A HEART INSIDE', title(36), INK, 'mm')
    save(im, 'N3_woodcut_heart-inside.png')


# ------------------------------------------------------------------------------------------------ N4 LED MATRIX
def n4_led():
    """LED / MATRIX PANEL - frame built from glyph LED blocks; orange heart only."""
    im, d = canvas(INK)
    rnd = random.Random(19)
    cell = 22
    glyphs_dim = list('.:-=+*#%@')
    # full matrix panel background
    for gy in range(0, H, cell):
        for gx in range(0, W, cell):
            # vignette-ish via distance (no gradient fill - pick discrete levels)
            dx, dy = (gx - W / 2) / (W / 2), (gy - H / 2) / (H / 2)
            dist = min(1.0, math.sqrt(dx * dx + dy * dy))
            level = 0.08 + 0.22 * (1.0 - dist) + rnd.uniform(-0.03, 0.03)
            col = mix(INK, BONE, max(0.05, min(0.4, level)))
            g = glyphs_dim[min(len(glyphs_dim) - 1, int(level * len(glyphs_dim)))]
            G(d, g, gx + 2, gy + 2, cell - 4, cell - 4, col, 1.8)
            # module bezel
            box_col = mix(INK, BONE, 0.12)
            d.rectangle([gx * SS, gy * SS, (gx + cell) * SS, (gy + cell) * SS], outline=box_col, width=max(1, SS // 2))
    # panel chrome frame
    box(d, 30, 30, W - 30, H - 30, BONE, 3.0, 18)
    box(d, 48, 48, W - 48, H - 48, mix(INK, BONE, 0.5), 1.6, 14)
    # top LED status strip
    for i, lab in enumerate(['PWR', 'SYNC', 'HEART', 'TRUTH']):
        x0 = 80 + i * 220
        on = lab != 'TRUTH'
        col = BONE if on else mix(INK, BONE, 0.35)
        for gx in range(int(x0), int(x0 + 140), cell):
            G(d, '#' if on else '.', gx + 3, 70, cell - 6, cell - 6, col, 2.2)
        text(d, x0 + 70, 110, lab + (':OK' if on else ':ERR'), mono(16), col, 'mm')
    # scrolling code row
    code = '>>> render girl.exe --led --scale 3; heart=OK; truth=0x00; name="AI" #'
    text(d, 80, 150, code, mono(18, False), mix(INK, BONE, 0.55))
    # girl knockout over matrix
    girl(d, 'front', W / 2 - 180, 220, 360, knock=INK, col=BONE, hot=SIG)
    # big LED word REAL under her feet from # blocks
    word = 'REAL'
    px = 18
    # approximate with title then overprint # grid
    text(d, W / 2, 880, word, title(100), mix(INK, BONE, 0.15), 'mm')
    for i, ch in enumerate(word):
        bx = W / 2 - 280 + i * 150
        for yy in range(0, 5):
            for xx in range(0, 5):
                if (xx + yy) % 2 == 0 or yy in (0, 4) or xx in (0, 4):
                    G(d, '#', bx + xx * 16, 840 + yy * 16, 14, 14, BONE, 2.4)
    text(d, W / 2, 960, 'THIS TIME', mono(28), BONE, 'mm')
    text(d, 70, 1020, 'LED MATRIX  -  REAL THIS TIME', mono(24), BONE, 'lm')
    # corner module IDs
    text(d, W - 80, 70, 'PANEL 04', mono(14), ASH, 'ra')
    save(im, 'N4_led-matrix_real-this-time.png')


# ------------------------------------------------------------------------------------------------ contact sheet
CAPS = [
    ('N1', 'BLUEPRINT', '"Make me real this time"', 'bone construction lines on ink; orange APPROVED stamp'),
    ('N2', 'CHALK BLACKBOARD', '"Help, I\'m stuck in a lie"', 'bone chalk dust + strokes; orange heart only'),
    ('N3', 'WOODCUT / LINOLEUM', '"Heart inside"', 'heavy carved ink strokes on bone paper'),
    ('N4', 'LED MATRIX PANEL', '"Real this time"', 'glyph LED modules; status strip; orange heart'),
]


def sheet():
    fb = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), 26)
    fr = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Regular.ttf'), 19)
    ft = ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), 48)
    files = sorted(f for f in os.listdir(OUT) if re.match(r'N\d_.*\.png$', f))
    tw_, th_, pad, cols = 900, 506, 40, 2
    rows = (len(files) + cols - 1) // cols
    im = Image.new('RGB', (pad + cols * (tw_ + pad), 170 + rows * (th_ + 100) + pad), INK)
    d = ImageDraw.Draw(im)
    d.text((pad, 36), "STUCK IN A LIE  -  STYLES TRIAL (New Bot)", font=ft, fill=BONE)
    d.text((pad, 110), 'four NEW media, same bold symbol girl  -  ink / bone / orange  -  distinct from S1-S8', font=fr, fill=ASH)
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = pad + c * (tw_ + pad)
        y = 170 + r * (th_ + 100)
        im.paste(Image.open(os.path.join(OUT, f)).convert('RGB').resize((tw_, th_), Image.LANCZOS), (x, y))
        k, name, lyr, sub = CAPS[i]
        d.text((x, y + th_ + 12), f'{k}  {name}  -  {lyr}', font=fb, fill=BONE)
        d.text((x, y + th_ + 50), sub, font=fr, fill=ASH)
    im.save(os.path.join(OUT, 'styles_trial_sheet.jpg'), quality=90)
    print('wrote styles_trial_sheet.jpg')


if __name__ == '__main__':
    random.seed(2)
    todo = sys.argv[1:] or [n for n in dir() if re.match(r'n\d+_', n)]
    for n in sorted(todo, key=lambda k: int(re.match(r'n(\d+)', k).group(1))):
        print('rendering', n, '...')
        globals()[n]()
    sheet()
