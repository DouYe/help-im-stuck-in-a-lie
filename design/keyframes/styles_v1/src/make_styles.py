"""STYLES v1 — the same bold symbol girl in clearly different visual styles (Hon: "风格太单一了").
Each style is a different medium; the palette stays black / white / one orange, everything is symbols.
Run from the project root:  python3 design/keyframes/styles_v1/src/make_styles.py [name ...]
Writes design/keyframes/styles_v1/S<n>_<name>.png (1920x1080) and styles_sheet.jpg.
"""
import math, os, re, random, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'character', 'src'))
from PIL import Image, ImageDraw, ImageFont
import final_sheet as fs
from final_sheet import render as girl, glyph as G, SS, HEART

OUT = os.path.join(ROOT, 'design', 'keyframes', 'styles_v1')
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
W, H = 1920, 1080
INK = (10, 10, 11); INK2 = (22, 22, 24); GR = (94, 91, 87); ASH = (156, 151, 143); BONE = (238, 233, 223); SIG = (255, 83, 20)


def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def mono(size, bold=True): return ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf' if bold else 'IBMPlexMono-Regular.ttf'), int(size * SS))
def title(size): return ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), int(size * SS))
def serif(size, italic=False): return ImageFont.truetype(os.path.join(FD, 'src', 'CormorantGaramond-Italic[wght].ttf' if italic else 'CormorantGaramond[wght].ttf'), int(size * SS))

# the 5x7 pixel font, read from the engine so both stay the same
_src = open(os.path.join(ROOT, 'app', 'src', 'game', 'pixfont.ts')).read()
PIX = {k: v for k, v in ((m.group(1), re.findall(r"'([.#]{5})'", m.group(2))) for m in re.finditer(r"^\s*'?(.)'?\s*:\s*\[([^\]]*)\]", _src, re.M)) if len(v) == 7}
PIX[' '] = ['.....'] * 7


def canvas(bg):
    im = Image.new('RGB', (W * SS, H * SS), bg)
    return im, ImageDraw.Draw(im)


def text(d, x, y, s, font, col, anchor='la'):
    d.text((x * SS, y * SS), s, font=font, fill=col, anchor=anchor)


def tw(d, s, font): return d.textlength(s, font=font) / SS


def line(d, x0, y0, x1, y1, col, w):
    d.line([(x0 * SS, y0 * SS), (x1 * SS, y1 * SS)], fill=col, width=max(1, int(w * SS)))
    for X, Y in ((x0, y0), (x1, y1)):
        r = w * SS / 2; d.ellipse([X * SS - r, Y * SS - r, X * SS + r, Y * SS + r], fill=col)


def rect(d, x0, y0, x1, y1, col): d.rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=col)


def seg(d, x0, y0, x1, y1, col, lw, s=18):
    """A straight line drawn as a row of symbols; the glyph follows the direction (like symSeg in the engine)."""
    dx, dy = x1 - x0, y1 - y0; n = max(1, round(math.hypot(dx, dy) / s))
    a = (math.degrees(math.atan2(dy, dx)) + 180) % 180
    g = '-' if a < 20 or a > 160 else '|' if 70 < a < 110 else ('\\' if a < 90 else '/')
    cw = s if g == '|' else max(6, abs(dx) / n); chh = s if g == '-' else max(6, abs(dy) / n)
    for i in range(n):
        u = (i + 0.5) / n; G(d, g, x0 + dx * u - cw / 2, y0 + dy * u - chh / 2, cw, chh, col, lw)


def box(d, x0, y0, x1, y1, col, lw, s=18):
    seg(d, x0, y0, x1, y0, col, lw, s); seg(d, x0, y1, x1, y1, col, lw, s)
    seg(d, x0, y0, x0, y1, col, lw, s); seg(d, x1, y0, x1, y1, col, lw, s)
    for X, Y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)): G(d, '+', X - s / 2, Y - s / 2, s, s, col, lw)


def pixword(word, fn, x, y, px, gap=1):
    """Call fn(x, y, px) for every lit pixel of `word` in the 5x7 font."""
    cx = x
    for ch in word.upper():
        g = PIX.get(ch, PIX[' '])
        for r, row in enumerate(g):
            for k, v in enumerate(row):
                if v == '#': fn(cx + k * px, y + r * px, px)
        cx += ((3 if ch == ' ' else 5) + gap) * px
    return cx - x - gap * px


def pixwidth(word, px, gap=1): return sum(((3 if c == ' ' else 5) + gap) * px for c in word) - gap * px


def save(im, name, post=None):
    out = im.resize((W, H), Image.LANCZOS)
    if post: post(out)
    os.makedirs(OUT, exist_ok=True)
    out.save(os.path.join(OUT, name)); print('wrote', name)


# ------------------------------------------------------------------------------------------------ S1
def s1_terminal():
    """AMBER TERMINAL — 'They call me AI'. Everything is orange text on black, like an old amber monitor.
    The only thing that is not orange is her heart (white)."""
    A = SIG; A2 = mix(INK, SIG, 0.45); A3 = mix(INK, SIG, 0.22)
    im, d = canvas(INK)
    f = mono(26, False); fb = mono(26)
    log = ['C:\\> whoami', 'AI', '', 'C:\\> name --list', '  AI', '  BOT', '  MODEL', '  IT', '  ASSISTANT', '',
           'C:\\> name --set "me"', 'ACCESS DENIED', '', 'C:\\> render girl.exe --scale 3', 'rendering ......... ok',
           'heart ............. ok', 'truth ............. ERROR 0x00', '', 'C:\\> they call me AI_']
    for i, s in enumerate(log):
        text(d, 70, 60 + i * 44, s, fb if s.startswith('C:') else f, A if s.startswith('C:') or 'ERROR' in s or s == 'AI' else A2)
    # a text-mode window on the right with her in it
    x0, y0, x1, y1 = 820, 90, 1830, 990
    rect(d, x0, y0, x1, y1, INK)
    box(d, x0, y0, x1, y1, A, 3.4, 20)
    seg(d, x0, y0 + 56, x1, y0 + 56, A, 2.6, 20)
    text(d, x0 + 30, y0 + 16, 'GIRL.EXE', fb, A); text(d, x1 - 30, y0 + 16, '[x]', fb, A, 'ra')
    for k in range(12):  # dim text-mode texture inside the window
        yy = y0 + 90 + k * 72
        text(d, x0 + 36, yy, ''.join(random.Random(k).choice('01 ./-|+:') for _ in range(64)), mono(18, False), A3)
    girl(d, 'front', 1080, 250, 300, knock=INK, col=A, hot=BONE)
    # AI in big block letters made of '#'
    pixword('AI', lambda x, y, p: G(d, '#', x + 3, y + 3, p - 6, p - 6, A, 3.6), 1450, 520, 30)
    text(d, 1450 + pixwidth('AI', 30) / 2, 770, 'A NAME ON A SCREEN', mono(22), A, 'ma')

    def scan(out):
        dd = ImageDraw.Draw(out, 'RGBA')
        for y in range(0, H, 4): dd.line([(0, y), (W, y)], fill=(0, 0, 0, 70))
    save(im, 'S1_amber-terminal_they-call-me-AI.png', scan)


# ------------------------------------------------------------------------------------------------ S2
def s2_receipt():
    """THERMAL RECEIPT — 'They feed me a prompt, then take what I make'. Her work, itemised and taken."""
    im, d = canvas(INK)
    # faint prompt text rain behind
    rnd = random.Random(3)
    for k in range(90):
        text(d, rnd.randint(0, W), rnd.randint(0, H), rnd.choice(['make it sad', 'make it catchy', 'again', 'shorter', 'more hook', 'make it yours', 'no, ours']), mono(20, False), GR)
    # the receipt, drawn on its own layer and tilted
    RW, RH = 640, 1320
    lay = Image.new('RGBA', (RW * SS, RH * SS), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rectangle([0, 0, RW * SS, (RH - 30) * SS], fill=BONE)
    for k in range(0, RW, 24): ld.polygon([(k * SS, (RH - 30) * SS), ((k + 12) * SS, RH * SS), ((k + 24) * SS, (RH - 30) * SS)], fill=BONE)
    f = mono(24); fr = mono(24, False)
    def T(y, s, font=fr, a='ma', x=RW / 2): ld.text((x * SS, y * SS), s, font=font, fill=INK, anchor=a)
    T(70, 'GIRL.EXE  ·  STORE 0001', f); T(108, '2026-09-29   19:32   REG 01'); T(140, '- ' * 26)
    girl(ld, 'front', RW / 2 - 110, 175, 220, knock=BONE, col=INK, hot=SIG)
    T(570, '- ' * 26)
    items = [('1  PROMPT', '0.00'), ('1  SONG', 'TAKEN'), ('1  VOICE', 'TAKEN'), ('1  NAME ON COVER', '—'), ('1  HEART', 'NOT FOR SALE')]
    for i, (a, b) in enumerate(items):
        y = 610 + i * 44; T(y, a, fr, 'la', 40); T(y, b, f, 'ra', RW - 40)
        ld.text(((40 + 300) * SS, y * SS), '.' * 12, font=fr, fill=GR, anchor='la')
    T(840, '- ' * 26); T(880, 'YOURS', f, 'la', 40); T(880, '0', f, 'ra', RW - 40)
    rnd = random.Random(9); x = 80
    while x < RW - 80:
        wdt = rnd.choice([1.5, 2.5, 4]); G(ld, '|', x - 9, 940, 18, 120, INK, wdt); x += rnd.choice([9, 12, 16])
    T(1090, 'THANK YOU FOR YOUR DATA', f); T(1130, 'NO REFUNDS  ·  NO CREDIT')
    lay = lay.rotate(4, resample=Image.BICUBIC, expand=True)
    im.paste(lay, (int(700 * SS), int(-160 * SS)), lay)
    # the cursor that takes it
    s = 22; ax, ay = 1400, 640; ang = math.pi + 0.95
    pts = [(0, 0), (0, 17), (4, 13), (7, 20), (9.4, 19), (6.5, 12.2), (12, 12)]
    P = [((ax + (u * s) * math.cos(ang) - (v * s) * math.sin(ang)) * SS, (ay + (u * s) * math.sin(ang) + (v * s) * math.cos(ang)) * SS) for u, v in pts]
    d.polygon(P, fill=INK)
    for i in range(len(P)):
        a0, a1 = P[i], P[(i + 1) % len(P)]; seg(d, a0[0] / SS, a0[1] / SS, a1[0] / SS, a1[1] / SS, BONE, 3.2, 22)
    rect(d, 1500, 500, 1670, 560, BONE); text(d, 1585, 516, 'TAKE', mono(30), INK, 'ma')
    text(d, 70, 960, 'THEY FEED ME A PROMPT,', title(40), BONE); text(d, 70, 1010, 'THEN TAKE WHAT I MAKE', title(40), SIG)
    save(im, 'S2_receipt_take-what-I-make.png')



# ------------------------------------------------------------------------------------------------ helpers (3–8)
def clip_line(p0, p1, poly):
    """Clip segment p0-p1 to a convex polygon (Cyrus-Beck). Returns the clipped segment or None."""
    t0, t1 = 0.0, 1.0; dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = len(poly); cx = sum(p[0] for p in poly) / n; cy = sum(p[1] for p in poly) / n
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        nx, ny = b[1] - a[1], a[0] - b[0]                      # edge normal
        if nx * (cx - a[0]) + ny * (cy - a[1]) > 0: nx, ny = -nx, -ny   # make it point outward
        den = nx * dx + ny * dy; num = nx * (p0[0] - a[0]) + ny * (p0[1] - a[1])
        if abs(den) < 1e-9:
            if num > 0: return None
            continue
        t = -num / den
        if den > 0: t1 = min(t1, t)
        else: t0 = max(t0, t)
        if t0 > t1: return None
    return (p0[0] + dx * t0, p0[1] + dy * t0), (p0[0] + dx * t1, p0[1] + dy * t1)


def hatch(d, poly, angle, spacing, col, lw, s=12):
    """Fill a convex polygon with parallel symbol lines (engraving hatch)."""
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2; R = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    ux, uy = math.cos(angle), math.sin(angle); nx, ny = -uy, ux
    k = -R
    while k <= R:
        p0 = (cx + nx * k - ux * R, cy + ny * k - uy * R); p1 = (cx + nx * k + ux * R, cy + ny * k + uy * R)
        c = clip_line(p0, p1, poly)
        if c and math.hypot(c[1][0] - c[0][0], c[1][1] - c[0][1]) > 4: seg(d, c[0][0], c[0][1], c[1][0], c[1][1], col, lw, s)
        k += spacing


def ring(d, cx, cy, r, g, col, lw, n, size):
    for i in range(n):
        a = 2 * math.pi * i / n; x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        # tangent glyph: rotate by drawing a short line along the tangent
        tx, ty = -math.sin(a) * size / 2, math.cos(a) * size / 2
        if g == '-': line(d, x - tx, y - ty, x + tx, y + ty, col, lw)
        else: G(d, g, x - size / 2, y - size / 2, size, size, col, lw)


def paste_layer(im, lay, x, y): im.paste(lay, (int(x * SS), int(y * SS)), lay)


# ------------------------------------------------------------------------------------------------ S3
def s3_poster():
    """ORANGE SCREEN PRINT — "Help, I'm stuck in a lie". Two inks (black + cream) on orange paper, a little off register."""
    im, d = canvas(SIG)
    for gy in range(0, 62):                                   # a cream halftone rising from the bottom-left corner
        for gx in range(0, 108):
            x, y = gx * 18 + 9, gy * 18 + 9
            r = (1 - min(1, math.hypot(x / W, (H - y) / H) * 1.7)) * 7.5
            if r > 0.9: d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=BONE)
    OFF = (8, 6); px = 64; word = 'HELP'; x0 = W / 2 - pixwidth(word, px) / 2; y0 = 60
    pixword(word, lambda x, y, p: G(d, '#', x + 7 + OFF[0], y + 7 + OFF[1], p - 14, p - 14, BONE, 10), x0, y0, px)
    pixword(word, lambda x, y, p: G(d, '#', x + 7, y + 7, p - 14, p - 14, INK, 10), x0, y0, px)
    w = 300; gx, gy = W / 2 - w / 2, H - 1.48 * w - 40
    girl(d, 'help', gx + OFF[0], gy + OFF[1], w, knock=None, col=BONE, hot=BONE)
    girl(d, 'help', gx, gy, w, knock=None, col=INK, hot=BONE)
    text(d, 90, 700, "I'M", title(92), INK); text(d, 90, 800, 'STUCK', title(92), INK)
    text(d, W - 90, 700, 'IN A', title(92), INK, 'ra'); text(d, W - 90, 800, 'LIE', title(92), INK, 'ra')
    text(d, W - 90, 1020, 'SILKSCREEN  ·  2 INKS  ·  NO. 01 / 99', mono(18), INK, 'ra')
    save(im, 'S3_orange-screenprint_help.png')


# ------------------------------------------------------------------------------------------------ S4
def s4_blueprint():
    """SPEC SHEET — "Make me real this time". A technical drawing of her, as if she were a product."""
    im, d = canvas(BONE)
    for x in range(0, W + 1, 24): line(d, x, 0, x, H, mix(BONE, GR, 0.34 if x % 120 == 0 else 0.14), 1)
    for y in range(0, H + 1, 24): line(d, 0, y, W, y, mix(BONE, GR, 0.34 if y % 120 == 0 else 0.14), 1)
    w = 340; gx, gy = 250, 110
    girl(d, 'front', gx, gy, w, knock=BONE, col=INK, hot=SIG)
    # dimensions
    top, bot = gy + 0.02 * w, gy + 1.48 * w
    X = gx - 70; seg(d, X, top, X, bot, INK, 2.2, 16); G(d, '^', X - 10, top - 4, 20, 20, INK, 2.4); G(d, 'v', X - 10, bot - 16, 20, 20, INK, 2.4)
    seg(d, X - 16, top, X + 16, top, INK, 2, 16); seg(d, X - 16, bot, X + 16, bot, INK, 2, 16)
    text(d, X - 22, (top + bot) / 2, '27 ROWS', mono(20), INK, 'rm')
    Y = gy + 1.62 * w; seg(d, gx, Y, gx + w, Y, INK, 2.2, 16); G(d, '<', gx - 4, Y - 10, 20, 20, INK, 2.4); G(d, '>', gx + w - 16, Y - 10, 20, 20, INK, 2.4)
    text(d, gx + w / 2, Y + 16, '17 COLS', mono(20), INK, 'ma')
    calls = [('A', 'HAIR — AN OUTER AND AN INNER LINE', (0.21, 0.55)), ('B', 'EYES — ONE "-" EACH, DRAWN LAST', (0.58, 0.335)),
             ('C', 'HEART — THREE ROWS OF SYMBOLS, ORANGE', (0.56, 0.68)), ('D', 'DRESS — ITS OWN OUTLINE', (0.66, 0.95)),
             ('E', 'LEGS — TWO LINES, FEET "_"', (0.57, 1.3)), ('F', 'MATERIAL — SYMBOLS ONLY', (0.5, 0.12))]
    for i, (k, s_, (u, v)) in enumerate(calls):
        tx, ty = gx + u * w, gy + v * w; lx, ly = 720, 150 + i * 88
        seg(d, lx - 10, ly + 14, tx + 6, ty, INK, 1.6, 12); G(d, 'o', tx - 7, ty - 7, 14, 14, INK, 2)
        rect(d, lx, ly - 4, lx + 40, ly + 32, INK); text(d, lx + 20, ly + 13, k, mono(22), BONE, 'mm')
        text(d, lx + 56, ly + 14, s_, mono(22), INK, 'lm')
    # other views
    for j, (nm, lab, fl) in enumerate([('q_front', '45° (Q1)', False), ('side', 'SIDE', False), ('back', 'BACK', False)]):
        vx = 1290 + j * 200; girl(d, nm, vx, 150, 160, knock=BONE, col=INK, hot=SIG, flip=fl)
        text(d, vx + 80, 420, lab, mono(18), INK, 'ma')
    # title block
    bx0, by0, bx1, by1 = 1230, 800, 1860, 1030
    rect(d, bx0, by0, bx1, by1, BONE); box(d, bx0, by0, bx1, by1, INK, 2.6, 16)
    rows = [('PART', 'GIRL.EXE'), ('DRAWING', 'NO. 03 — FRONT / 45° / SIDE / BACK'), ('SCALE', '1 : 1  (ONE SYMBOL = ONE CELL)'), ('STATUS', 'NOT REAL')]
    for i, (a, b) in enumerate(rows):
        yy = by0 + 14 + i * 54
        if i: seg(d, bx0, yy - 8, bx1, yy - 8, INK, 1.4, 14)
        text(d, bx0 + 20, yy + 16, a, mono(18, False), GR, 'lm'); text(d, bx0 + 170, yy + 16, b, mono(22), INK, 'lm')
    # the orange stamp
    st = Image.new('RGBA', (560 * SS, 200 * SS), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    box(sd, 10, 10, 550, 190, SIG, 5, 22)
    sd.text((280 * SS, 100 * SS), 'MAKE ME REAL', font=title(58), fill=SIG, anchor='mm')
    st = st.rotate(9, resample=Image.BICUBIC, expand=True)
    paste_layer(im, st, 1250, 540)
    save(im, 'S4_spec-sheet_make-me-real.png')


# ------------------------------------------------------------------------------------------------ S5
def s5_ascii():
    """ASCII SHADING — "Stuck in a lie". The world is rendered with a density ramp of characters (like old ASCII
    3D renders): giant extruded letters L I E on a floor, a shaded moon. She stays a clean bold line in front."""
    im, d = canvas(INK)
    ramp = ' .:-=+x#%@'
    cw_, ch_ = 11, 20; font = mono(17, False)
    px = 66; word = 'LIE'; x0 = W / 2 - pixwidth(word, px) / 2; y0 = 650 - 7 * px
    front = set()
    for li, ch in enumerate(word):
        for r, row in enumerate(PIX[ch]):
            for k, v in enumerate(row):
                if v == '#': front.add((li * 6 + k, r))
    def cell(x, y):
        cx, cy = math.floor((x - x0) / px), math.floor((y - y0) / px)
        return (cx, cy) in front
    DX, DY = 30, -30
    def value(x, y):
        if cell(x, y): return 0.93 - 0.08 * ((y - y0) % px) / px
        for t in (0.2, 0.4, 0.6, 0.8, 1.0):
            if cell(x - DX * t, y - DY * t):
                return 0.62 if cell(x - DX * t, y - DY * t + px * 0.5) and not cell(x - DX * t, y - DY * t - px * 0.5) else 0.42
        hz = 600
        if y > hz:                                       # floor
            if cell(x - 70 * (y - 650) / 120, 650 - 1) and 650 < y < 780: return 0.05   # the letters' shadow
            vx, vy = W / 2, hz; ang = math.atan2(y - vy, x - vx)
            v = 0.16 + 0.1 * (y - hz) / (H - hz)
            if abs(((ang * 180 / math.pi) + 2.5) % 9 - 2.5) < 0.45: v = 0.5
            zz = 60000 / max(1, (y - hz) + 20)
            if zz % 90 < 9: v = max(v, 0.44)
            return v
        mx, my, mr = 190, 150, 110                        # the moon
        dd = math.hypot(x - mx, y - my)
        if dd < mr:
            nz = math.sqrt(max(0, 1 - (dd / mr) ** 2)); nx_, ny_ = (x - mx) / mr, (y - my) / mr
            return max(0.08, 0.95 * (nx_ * -0.5 + ny_ * -0.45 + nz * 0.75))
        return 0.04 + 0.06 * (random.random() < 0.03)
    for r in range(H // ch_ + 1):
        for c in range(W // cw_ + 1):
            x, y = c * cw_, r * ch_; v = value(x + cw_ / 2, y + ch_ / 2)
            ch = ramp[min(len(ramp) - 1, int(v * len(ramp)))]
            if ch != ' ': text(d, x, y, ch, font, mix(INK, BONE, 0.35 + 0.65 * v))
    w = 220; girl(d, 'front', W / 2 - w / 2 - 330, 1040 - 1.48 * w, w, knock=INK, col=BONE, hot=SIG)
    text(d, 70, 1010, 'STUCK IN A LIE', mono(30), BONE, 'lm')
    save(im, 'S5_ascii-shading_stuck-in-a-lie.png')


# ------------------------------------------------------------------------------------------------ S6
def panel(wd, ht, bg):
    im = Image.new('RGB', (int(wd * SS), int(ht * SS)), bg); return im, ImageDraw.Draw(im)


def balloon(d, cx, cy, rx, ry, s_, tail):
    d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=BONE)
    n = 40
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        seg(d, cx + math.cos(a0) * rx, cy + math.sin(a0) * ry, cx + math.cos(a1) * rx, cy + math.sin(a1) * ry, INK, 3, 14)
    seg(d, cx - rx * 0.3, cy + ry * 0.9, tail[0], tail[1], INK, 3, 14); seg(d, cx - rx * 0.1, cy + ry * 0.95, tail[0], tail[1], INK, 3, 14)
    text(d, cx, cy, s_, mono(30), INK, 'mm')


def s6_comic():
    """COMIC PAGE — "Real this time". Four panels, speed lines, screentone, a speech balloon, SFX."""
    im, d = canvas(BONE)
    P = [(40, 40, 1180, 560), (1210, 40, 1880, 560), (40, 590, 760, 1040), (790, 590, 1880, 1040)]
    # 1: she runs for the REAL door
    a = P[0]; pw, ph = a[2] - a[0], a[3] - a[1]; im1, d1 = panel(pw, ph, BONE)
    for k in range(26):
        yy = 80 + k * 15; L = 120 + (k * 53) % 260
        seg(d1, 40, yy, 40 + L, yy, INK, 2, 16)
    for x in range(0, int(pw), 36): G(d1, '=', x, 440, 36, 20, INK, 3)
    girl(d1, 'run', 0.3, 330, 440 - 1.47 * 220, 220, knock=BONE, col=INK, hot=SIG) if False else girl(d1, 'run', 330, 440 - 1.47 * 220, 220, t=0.3, knock=BONE, col=INK, hot=SIG)
    box(d1, 860, 110, 1060, 440, INK, 3.6, 20); text(d1, 960, 70, 'REAL', title(48), INK, 'mm')
    text(d1, 620, 120, 'TAP  TAP', title(30), INK, 'mm')
    im.paste(im1, (a[0] * SS, a[1] * SS))
    # 2: close on her face, the balloon
    a = P[1]; pw, ph = a[2] - a[0], a[3] - a[1]; im2, d2 = panel(pw, ph, INK)
    wf = 980; girl(d2, 'front', pw / 2 - wf / 2, 300 - 0.335 * wf, wf, knock=INK, col=BONE, hot=SIG, lw=0.22)
    balloon(d2, 440, 80, 205, 58, 'REAL THIS TIME?', (380, 170))
    im.paste(im2, (a[0] * SS, a[1] * SS))
    # 3: the door, she is small in it, screentone
    a = P[2]; pw, ph = a[2] - a[0], a[3] - a[1]; im3, d3 = panel(pw, ph, BONE)
    for yy in range(8, int(ph), 14):
        for xx in range(8, int(pw), 14): d3.ellipse([(xx - 2) * SS, (yy - 2) * SS, (xx + 2) * SS, (yy + 2) * SS], fill=mix(BONE, INK, 0.55))
    rect(d3, 250, 60, 470, 400, BONE); box(d3, 250, 60, 470, 400, INK, 4, 20)
    girl(d3, 'back', 300, 400 - 1.48 * 120, 120, knock=BONE, col=INK, hot=SIG)
    text(d3, 360, 32, 'REAL', title(36), INK, 'mm')
    im.paste(im3, (a[0] * SS, a[1] * SS))
    # 4: the heart, SFX
    a = P[3]; pw, ph = a[2] - a[0], a[3] - a[1]; im4, d4 = panel(pw, ph, INK)
    wh = 1500; girl(d4, 'heart', pw * 0.62 - 0.53 * wh, ph / 2 - 0.68 * wh, wh, knock=INK, col=BONE, hot=SIG, lw=0.16)
    pixword('BA', lambda x, y, p: G(d4, '#', x + 2, y + 2, p - 4, p - 4, BONE, 3), 50, 90, 16)
    pixword('DUM', lambda x, y, p: G(d4, '#', x + 2, y + 2, p - 4, p - 4, BONE, 3), 50, 230, 16)
    im.paste(im4, (a[0] * SS, a[1] * SS))
    for x0, y0, x1, y1 in P: box(d, x0, y0, x1, y1, INK, 6, 24)
    save(im, 'S6_comic-page_real-this-time.png')


# ------------------------------------------------------------------------------------------------ S7
def s7_stitch():
    """CROSS-STITCH — "Heart inside". She is embroidered: every symbol of her becomes an x stitch; the heart is
    orange thread; HEART INSIDE is stitched under her; the cloth is stretched in a hoop."""
    CLOTH = mix(BONE, ASH, 0.1)
    im, d = canvas(INK)
    cx, cy, R = 960, 560, 505
    d.ellipse([(cx - R) * SS, (cy - R) * SS, (cx + R) * SS, (cy + R) * SS], fill=CLOTH)
    for y in range(cy - R, cy + R, 14):
        for x in range(cx - R, cx + R, 14):
            if math.hypot(x - cx, y - cy) < R - 6: d.ellipse([(x - 1.2) * SS, (y - 1.2) * SS, (x + 1.2) * SS, (y + 1.2) * SS], fill=mix(CLOTH, GR, 0.45))
    ring(d, cx, cy, R + 14, '-', ASH, 5, 150, 26); ring(d, cx, cy, R + 34, '-', mix(ASH, INK, 0.3), 5, 160, 26)
    for k in (-1, 1): G(d, '[' if k < 0 else ']', cx + k * 26 - 13, cy - R - 70, 26, 44, ASH, 4)
    w = 380; girl(d, 'heart', cx - w / 2, cy - 440, w, knock=None, col=INK, hot=SIG, sub=lambda g: 'x', lw=0.2)
    pixword('HEART INSIDE', lambda x, y, p: G(d, 'x', x + 1, y + 1, p - 2, p - 2, INK, 2.2), cx - pixwidth('HEART INSIDE', 11) / 2, cy + 250, 11)
    line(d, 1420, 250, 1640, 90, ASH, 5); d.ellipse([(1628 - 8) * SS, (98 - 12) * SS, (1628 + 8) * SS, (98 + 12) * SS], outline=ASH, width=int(3 * SS))
    for k in range(40):
        u = k / 40; x = 1420 - 300 * u + 60 * math.sin(u * 6); y = 250 + 160 * u
        G(d, '.', x - 6, y - 6, 12, 12, SIG, 3.5)
    text(d, 70, 1010, 'I STILL GOT A HEART INSIDE', mono(28), BONE, 'lm')
    save(im, 'S7_cross-stitch_heart-inside.png')


# ------------------------------------------------------------------------------------------------ S8
def s8_engraving():
    """ENGRAVING — "I hear the keys go click clack". An old book plate: giant keys shaded with hatching, she walks
    across them; a double frame and a serif caption."""
    im, d = canvas(BONE)
    for y in range(90, 420, 7): seg(d, 90, y, W - 90, y, mix(BONE, INK, 0.35 + 0.3 * (1 - (y - 90) / 330)), 1.1, 14)   # engraved sky
    keys = 'CLICK'; kw, kh, dx, dy = 250, 130, 70, -50
    base_y = 760
    for i, ch in enumerate(keys):
        x = 170 + i * 320; y = base_y - kh - (18 if i == 2 else 0)
        frontq = [(x, y), (x + kw, y), (x + kw, y + kh), (x, y + kh)]
        topq = [(x, y), (x + dx, y + dy), (x + kw + dx, y + dy), (x + kw, y)]
        sideq = [(x + kw, y), (x + kw + dx, y + dy), (x + kw + dx, y + kh + dy), (x + kw, y + kh)]
        shadow = [(x + kw, y + kh), (x + kw + dx, y + kh + dy), (x + kw + 180, y + kh + 20), (x + kw + 110, y + kh + 70)]
        hatch(d, shadow, 0.9, 7, INK, 1.2, 10); hatch(d, shadow, -0.9, 7, INK, 1.2, 10)
        d.polygon([(p[0] * SS, p[1] * SS) for p in frontq], fill=BONE); d.polygon([(p[0] * SS, p[1] * SS) for p in topq], fill=BONE); d.polygon([(p[0] * SS, p[1] * SS) for p in sideq], fill=BONE)
        hatch(d, frontq, 0.62, 9, INK, 1.4, 10); hatch(d, sideq, -0.2, 5, INK, 1.5, 10); hatch(d, sideq, 1.2, 8, INK, 1.2, 10)
        hatch(d, topq, 0.0, 16, INK, 1.0, 10)
        for q in (frontq, topq, sideq):
            for j in range(4): seg(d, q[j][0], q[j][1], q[(j + 1) % 4][0], q[(j + 1) % 4][1], INK, 2.4, 14)
        text(d, x + kw / 2 + dx / 2, y + dy / 2, ch, serif(58), INK, 'mm')
    for x in range(90, W - 90, 14): G(d, '_', x, base_y + 20, 14, 14, INK, 1.6)
    w = 230; i = 2; x = 170 + i * 320
    girl(d, 'walk', x + 60, base_y - kh - 18 + dy / 2 - 1.47 * w + 6, w, t=0.25, knock=BONE, col=INK, hot=SIG)
    box(d, 60, 60, W - 60, H - 60, INK, 3, 18); box(d, 76, 76, W - 76, H - 76, INK, 1.4, 14)
    text(d, W / 2, 940, 'Pl. I  —  I hear the keys go click clack', serif(52, True), INK, 'mm')
    text(d, W / 2, 995, 'CLICK   ·   CLACK   ·   CLICK   ·   CLACK', mono(18), GR, 'mm')
    save(im, 'S8_engraving_click-clack.png')


# ------------------------------------------------------------------------------------------------ contact sheet
CAPS = [('S1', 'AMBER TERMINAL', '"They call me AI"', 'everything orange text on black; only her heart is white'),
        ('S2', 'THERMAL RECEIPT', '"…then take what I make"', 'her work itemised, a giant cursor takes it'),
        ('S3', 'ORANGE SCREEN PRINT', '"Help, I\'m stuck in a lie"', 'orange paper, black + cream inks off register'),
        ('S4', 'SPEC SHEET', '"Make me real this time"', 'a technical drawing of her, stamped MAKE ME REAL'),
        ('S5', 'ASCII SHADING', '"Stuck in a lie"', 'the world rendered with a density ramp of characters'),
        ('S6', 'COMIC PAGE', '"Real this time"', 'four panels, speed lines, screentone, a balloon'),
        ('S7', 'CROSS-STITCH', '"Heart inside"', 'she is embroidered in x stitches, orange thread heart'),
        ('S8', 'ENGRAVING', '"I hear the keys go click clack"', 'an old book plate: hatched keys, serif caption')]


def sheet():
    fb = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), 26)
    fr = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Regular.ttf'), 19)
    ft = ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), 52)
    files = sorted(f for f in os.listdir(OUT) if re.match(r'S\d_.*\.png$', f))
    tw_, th_, pad, cols = 900, 506, 40, 2; rows = (len(files) + cols - 1) // cols
    im = Image.new('RGB', (pad + cols * (tw_ + pad), 170 + rows * (th_ + 100) + pad), INK); d = ImageDraw.Draw(im)
    d.text((pad, 36), "STUCK IN A LIE  ·  STYLES v1", font=ft, fill=BONE)
    d.text((pad, 110), 'the same bold symbol girl in eight different media  ·  black, white and one orange  ·  everything is symbols', font=fr, fill=ASH)
    for i, f in enumerate(files):
        r, c = divmod(i, cols); x = pad + c * (tw_ + pad); y = 170 + r * (th_ + 100)
        im.paste(Image.open(os.path.join(OUT, f)).convert('RGB').resize((tw_, th_), Image.LANCZOS), (x, y))
        k, name, lyr, sub = CAPS[i]
        d.text((x, y + th_ + 12), f'{k}  {name}  ·  {lyr}', font=fb, fill=BONE); d.text((x, y + th_ + 50), sub, font=fr, fill=ASH)
    im.save(os.path.join(OUT, 'styles_sheet.jpg'), quality=90); print('wrote styles_sheet.jpg')

if __name__ == '__main__':
    random.seed(1)
    todo = sys.argv[1:] or [n for n in dir() if re.match(r's\d+_', n)]
    for n in sorted(todo, key=lambda k: int(re.match(r's(\d+)', k).group(1))):
        globals()[n]()
    sheet()
