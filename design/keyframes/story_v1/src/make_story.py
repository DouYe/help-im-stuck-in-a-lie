"""STORY v1 — ten keyframes: the escape from the music factory at three scales (game / close-up / plate).
Run from the project root:  python3 design/keyframes/story_v1/src/make_story.py [k01 k02 …] [--sheet]
"""
import sys
from story_kit import *

ANCHOR = (1104, 690)     # the heart / the spark sits here in K01, K05, K06, K07, K09 (cuts keep it in place)

FRAMES = [
    ('K01', 'wake-in-factory', 'CLOSE', 'wake in factory', 'she opens her eyes among identical AIs; only she has a heart'),
    ('K02', 'music-factory', 'GAME', 'same old song · room full of voices', 'the music factory: three floors of identical AIs singing the same song'),
    ('K03', 'sirens-say-go', 'GAME', 'sirens say GO · fall into line', 'the line marches into the press; she jumps out of it and runs'),
    ('K04', 'trumpets-click-clack', 'GAME + PLATE', 'keys click-clack · want another hook', 'trumpets fire notes on the beat; their flight is plotted on a staff'),
    ('K05', 'help-closeup', 'CLOSE', 'help, stuck in a lie', 'close-up: HELP, the word LIE flying at her'),
    ('K06', 'die-to-dot', 'GAME → PLATE', 'die at the border', 'hit: her symbols fly apart, the heart is left as a dot and pulled back to line 0'),
    ('K07', 'respawn-replay', 'PLATE', 'respawn · replay', 'the dot draws every attempt: 47 deaths become one computed drawing'),
    ('K08', 'make-me-real', 'PLATE → GAME', 'make me real', 'the lines the dot drew become platforms; she runs on her own drawing'),
    ('K09', 'heart-inside', 'CLOSE + PLATE', 'heart inside', 'the heart up close, measured like an instrument at 99 BPM'),
    ('K10', 'a-life-outside', 'GAME → PLATE', 'want a life outside', 'the REAL door: outside the factory is the open, computed world'),
]
FILE = {k: f'{k}_{slug}.png' for k, slug, *_ in FRAMES}


# ============================================================================ K07 — the dot draws every attempt
PLATS = [(70, 430, 758), (510, 770, 718), (850, 1020, 658), (1090, 1310, 698), (1390, 1570, 638), (1650, 1850, 678)]

def _attempt(k, rnd, death_x):
    """Heart path of one attempt: run on the platforms, jump the gaps, stop at death_x. Returns points."""
    pts = []; lift = 8
    for i, (x0, x1, y) in enumerate(PLATS):
        xs = max(x0, 120) if i == 0 else x0 + 10
        for x in range(int(xs), int(x1) - 6, 6):
            if x > death_x: return pts
            pts.append((x, y - lift + rnd.uniform(-1.2, 1.2)))
        if i + 1 < len(PLATS):
            nx0, nx1, ny = PLATS[i + 1]; ax, ay = x1 - 6, y - lift; bx, by = nx0 + 10, ny - lift
            peak = rnd.uniform(90, 170) + (k % 5) * 6
            for j in range(1, 25):
                u = j / 24; x = ax + (bx - ax) * u
                if x > death_x: return pts
                pts.append((x, ay + (by - ay) * u - peak * 4 * u * (1 - u)))
    return pts

def k07():
    Lr = Layers(bg=BONE)
    g = Lr('back')
    for x in range(0, W + 1, 24): line(g, x, 0, x, H, mix(BONE, GR, 0.2 if x % 120 == 0 else 0.09), 1)
    for y in range(0, H + 1, 24): line(g, 0, y, W, y, mix(BONE, GR, 0.2 if y % 120 == 0 else 0.09), 1)
    d = Lr('mid')
    # the level as an elevation drawing
    for x0, x1, y in PLATS:
        box(d, x0, y, x1, y + 30, INK, 1.6, 12)
        hatch(d, [(x0, y + 30), (x1, y + 30), (x1, y + 70), (x0, y + 70)], 0.8, 9, mix(BONE, INK, 0.45), 1.0, 9)
    for (a, b) in zip(PLATS, PLATS[1:]):
        gx0, gx1 = a[1], b[0]; yy = max(a[2], b[2]) + 96
        hair(d, [(gx0, yy), (gx1, yy)], GR, 1.1); hair(d, [(gx0, yy - 6), (gx0, yy + 6)], GR, 1.1); hair(d, [(gx1, yy - 6), (gx1, yy + 6)], GR, 1.1)
        text(d, (gx0 + gx1) / 2, yy + 8, f'GAP {int(gx1 - gx0)}', mono(13, 'Medium'), GR, 'ma')
    trumpet(d, 1420, 470, 170, INK, lw=1.6, s=8, fill=BONE, label='TRUMPET.EXE', lab_col=GR)
    trumpet(d, 1640, 330, 150, INK, lw=1.6, s=8, fill=BONE, label='TRUMPET.EXE', lab_col=GR)
    door(d, 1792, 560, 1872, 720, INK, 2.0, 'REAL', None, None)
    # spawn
    dashed(d, 120, 600, 120, 758, INK, 1.4, 8, 6); ellipse(d, 120, 750, 5, 5, fill=INK)
    text(d, 120, 570, 'LINE 0', mono(16), INK, 'ma'); text(d, 120, 590, 'spawn', mono(13, 'Regular'), GR, 'ma')
    # 47 attempts
    rnd = random.Random(7); deaths = []
    for k in range(47):
        prog = 300 + 1250 * (k / 46) ** 0.8 + rnd.uniform(-260, 160)
        dx = max(180, min(1600, prog))
        pts = _attempt(k, rnd, dx)
        if len(pts) < 2: continue
        age = k / 46
        hair(d, pts, mix(BONE, INK, 0.28 + 0.5 * age), 1.0 + 0.4 * age)
        ex, ey = pts[-1]; deaths.append(ex)
        g1(d, 'x', ex - 7, ey - 7, 14, INK, 1.8)
        # the way back to line 0: a dashed arc over the level
        top = 160 + 330 * (ex - 120) / 1500 + rnd.uniform(-40, 40); pts_back = []
        for j in range(61):
            u = j / 60
            pts_back.append((ex + (120 - ex) * u, ey + (750 - ey) * u - top * math.sin(math.pi * u)))
        hair(d, pts_back, mix(BONE, GR, 0.5), 0.9)
    # attempt 48: the spark, drawing now
    rnd48 = random.Random(48); p = _attempt(48, rnd48, ANCHOR[0])
    p = [q for q in p if q[0] <= ANCHOR[0]] + [ANCHOR]
    s = Lr('plate'); spark(s, p, SIG, 2.4, 8)
    label_line(s, 300, 470, 250, 420, 'the way back to line 0  ×47', GR, 14)
    # title block, top left
    text(s, 70, 70, 'RESPAWN', archivo(92, 1125, 900), INK)
    text(s, 70, 168, 'REPLAY', archivo(92, 1125, 900), INK)
    text(s, 74, 282, 'PLATE 07 — every attempt is one line; the orange one is being drawn now', mono(17, 'Medium'), GR)
    rows = [('ATTEMPTS', '048'), ('DEATHS', '047'), ('EXIT', '000'), ('BEST', f'{int(max(deaths))} px')]
    for i, (a, b) in enumerate(rows):
        y = 70 + i * 38; text(s, 1480, y, a, mono(18, 'Medium'), GR); text(s, 1850, y, b, mono(22), INK, 'ra')
        hair(s, [(1480, y + 30), (1850, y + 30)], mix(BONE, GR, 0.5), 1)
    label_line(s, ANCHOR[0], ANCHOR[1], 1180, 560, 'attempt 048 · t = 0:47.2', INK, 15)
    # inset: distance reached per attempt (a loss curve, upside down)
    ix0, iy0, ix1, iy1 = 1440, 860, 1860, 1010
    hair(s, [(ix0, iy0), (ix0, iy1), (ix1, iy1)], INK, 1.2)
    text(s, ix0, iy0 - 20, 'distance reached', mono(13, 'Medium'), GR)
    text(s, ix1, iy1 + 16, 'attempt →', mono(13, 'Medium'), GR, 'ra')
    pts = [(ix0 + (ix1 - ix0) * i / 46, iy1 - (iy1 - iy0) * (dd / 1600)) for i, dd in enumerate(deaths)]
    hair(s, pts, INK, 1.2)
    for q in pts: ellipse(s, q[0], q[1], 2.2, 2.2, fill=INK)
    ellipse(s, ix1 + 8, iy1 - (iy1 - iy0) * (ANCHOR[0] / 1600), 5, 5, fill=SIG)
    img = Lr.flatten()
    save(img, FILE['K07'], lambda im: grain(im, 4))


# ============================================================================ close-ups
def _bg_hall(Lr, seed=1, top=0.5, cmax=None):
    """A dark factory hall painted with characters, for behind close-ups."""
    far = Lr('far')
    V = vnoise(110, seed) * 0.6 + vgrad(None, 0, 0, 0, H, top, 0.05)
    ascii_paint(far, V, 10, 18, INK, cmax or mix(INK, GR, 0.9), seed=seed)

def _eyes_open(S):
    S = dict(S); S['eyes'] = [[(0.42, 0.335)], [(0.58, 0.335)]]; return S

def k05():
    Lr = Layers(bg=INK)
    _bg_hall(Lr, 5, 0.35)
    b = Lr('back')
    ascii_word(b, 'HELP', 40, 150, 205, 10, 18, INK2, mix(ASH, BONE, 0.2), seed=4)
    streams(b, -100, W + 100, 30, H, gap=26, seed=12, size=15, lw=2.0, arrows=0.35, cols=[GR, GR, mix(GR, INK, 0.3), ASH])
    d = Lr('play'); sw = 1100
    closeup(d, 'help', ANCHOR[0] - 0.53 * sw, ANCHOR[1] - 0.68 * sw, sw, k=5, knock=INK, heart_scale=1.25, chin=0.5)
    p = Lr('plate')
    px = 26; x0 = 1450; y0 = 540
    pix_text(p, 'LIE', x0, y0, px, BONE, 4.0)
    for k in range(8):                                    # its wake: long dashes behind the letters
        y = y0 + 10 + k * 22; L = 120 + (k * 37) % 160
        seg(p, x0 + pixwidth('LIE', px) + 30, y, min(W + 40, x0 + pixwidth('LIE', px) + 30 + L), y, ASH, 2.2, 18)
    label_line(p, 1460, 740, 1500, 790, 'lyric bullet  ·  v = 1,240 px/s', ASH, 15)
    img = Lr.flatten(blur={'far': 2.2, 'back': 0.9})
    save(img, FILE['K05'], lambda im: grain(vignette(im, 0.35), 5))

def k01():
    Lr = Layers(bg=INK)
    _bg_hall(Lr, 1, 0.45)
    b = Lr('back')
    # the line of identical AIs, receding
    for i in range(12):
        cx = 60 + i * 170; clone(b, 'front', cx, 610, 250, mix(INK, GR, 0.75), INK)
    for (cx, lab) in [(250, 'AI / 06'), (1850, 'AI / 08')]:
        sw2 = 720; ox2 = cx - sw2 / 2; oy2 = 1180 - 1.48 * sw2
        closeup(b, 'front', ox2, oy2, sw2, k=4, col=mix(GR, ASH, 0.35), hair=GR, hot=None, knock=INK, heart=False)
        text(b, cx - 150, 150, lab, mono(22), ASH)
    streams(b, -100, W + 100, 60, H, gap=34, seed=3, size=14, lw=2.0, cols=[mix(GR, INK, 0.3), GR, mix(GR, INK, 0.5)])
    d = Lr('play'); sw = 1100
    closeup(d, 'front', ANCHOR[0] - 0.53 * sw, ANCHOR[1] - 0.68 * sw, sw, k=5, knock=INK, S=_eyes_open(girl_pose('front')), chin=0.3)
    p = Lr('plate')
    rect(p, 70, 915, 420, 1040, INK)
    text(p, 90, 930, 'AI / 07', mono(26), BONE)
    text(p, 90, 966, 'status: awake', mono(18, 'Regular'), ASH)
    label_line(p, ANCHOR[0] + 70, ANCHOR[1] + 10, 1560, 820, 'heart != null', ASH, 18)
    text(p, 90, 1010, 'wake in factory', mono(18, 'Regular'), GR)
    img = Lr.flatten(blur={'far': 2.4, 'back': 1.2})
    save(img, FILE['K01'], lambda im: grain(vignette(im, 0.35), 5))

def k09():
    Lr = Layers(bg=INK)
    _bg_hall(Lr, 9, 0.25, mix(INK, GR, 0.6))
    d = Lr('play'); sw = 2950
    closeup(d, 'front', ANCHOR[0] - 0.53 * sw, ANCHOR[1] - 0.68 * sw, sw, k=9, knock=INK, heart=False, lw=3.2)
    p = Lr('plate'); cx, cy = ANCHOR
    for r_, w_ in [(300, 1.3), (318, 1.0), (430, 1.0)]: ellipse(p, cx, cy, r_, r_, outline=mix(INK, BONE, 0.55), width=w_)
    for i in range(64):
        a = -math.pi / 2 + 2 * math.pi * i / 64; big = i % 16 == 0; mid = i % 4 == 0
        r0, r1 = 300 - (26 if big else 14 if mid else 7), 300
        hair(p, [(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], BONE if big else ASH, 2.2 if big else 1.2)
    for i in range(4):
        a = -math.pi / 2 + 2 * math.pi * i / 4
        text(p, cx + math.cos(a) * 360, cy + math.sin(a) * 360, str(i + 1), mono(24), BONE, 'mm')
    a = -math.pi / 2 + 2 * math.pi * 2.35 / 4
    hair(p, [(cx, cy), (cx + math.cos(a) * 420, cy + math.sin(a) * 420)], SIG, 2.0)
    ellipse(p, cx + math.cos(a) * 430, cy + math.sin(a) * 430, 6, 6, fill=SIG)
    # the pulse line through the heart
    pts = []
    for x in range(0, W, 4):
        u = (x - cx) / 90.0; y = cy + 250 + (-150 * math.exp(-u * u * 2.2) + 60 * math.exp(-((x - cx - 70) / 45.0) ** 2) if abs(x - cx) < 300 else 3 * math.sin(x / 30))
        pts.append((x, y))
    sym_curve(p, pts, ASH, 2.0, 10)
    heart_hatched(p, cx, cy, 2950 / 17 * 0.72 * 0.95, 2950 * 1.6 / 27 * 0.58 * 0.95, SIG, fine=18, lw=3.4, width=26)
    text(p, 90, 860, 'heart inside', serif(120, True, 'Medium'), BONE)
    text(p, 96, 1000, 'HEART · 1 FOUND   ·   99 BPM   ·   BEAT 3 OF 4', mono(20, 'Medium'), ASH)
    img = Lr.flatten(blur={'far': 2.0})
    save(img, FILE['K09'], lambda im: grain(vignette(im, 0.4), 5))


# ============================================================================ game frames
def _machines(Lr, seed=0, top=0.55, dark=1.0):
    """Far layer: big factory machines and pipes painted with characters."""
    vim, vd = vcanvas(0); rnd = random.Random(seed)
    for i in range(9):
        x = rnd.randint(-100, W); w = rnd.randint(120, 300); y = rnd.randint(60, 420)
        vd.rectangle([x, y, x + w, H], fill=rnd.uniform(0.3, 0.6))
        vd.ellipse([x + 10, y - w * 0.3, x + w - 10, y + w * 0.3], fill=rnd.uniform(0.5, 0.8))
    for i in range(5):
        y = rnd.randint(80, 700); vd.rectangle([0, y, W, y + rnd.randint(14, 40)], fill=rnd.uniform(0.4, 0.7))
    V = varr(vim) * (0.5 + 0.5 * vnoise(60, seed + 1)) * vgrad(None, 0, 0, 0, H, top, 0.25)
    ascii_paint(Lr('far'), V, 10, 18, INK, mix(INK, mix(GR, ASH, 0.25), dark), seed=seed)

def _organ(Lr, x0=0, x1=W, base=H, seed=0, top=120, cmax=None, cw=8, ch=14):
    """A wall of organ pipes (the music factory's machinery), painted with characters."""
    vim, vd = vcanvas(0); rnd = random.Random(seed); x = x0
    while x < x1:
        w = rnd.choice([34, 40, 48, 56]); h = rnd.uniform(0.35, 1.0) * (base - top)
        yt = base - h
        for k in range(int(w)):
            u = k / w; shade = 0.25 + 0.5 * math.sin(math.pi * u) ** 0.7
            vd.line([(x + k, yt + w * 0.3), (x + k, base)], fill=shade)
        vd.ellipse([x, yt, x + w, yt + w * 0.6], fill=0.8)
        vd.rectangle([x + w * 0.2, yt + h * 0.25, x + w * 0.8, yt + h * 0.25 + 10], fill=0.05)     # the mouth
        x += w + rnd.choice([6, 10, 14])
    V = varr(vim) * (0.75 + 0.25 * vnoise(40, seed + 3))
    ascii_paint(Lr('far'), V, cw, ch, INK, cmax or mix(GR, ASH, 0.5), seed=seed, gamma=0.8)

def _walls(Lr, bands, seed=0, cmax=None):
    """Back walls behind factory floors: riveted panels and pipes, painted with characters."""
    vim, vd = vcanvas(0); rnd = random.Random(seed)
    for (y0, y1) in bands:
        x = -40
        while x < W:
            w = rnd.randint(180, 320); vd.rectangle([x + 4, y0 + 8, x + w - 4, y1 - 8], fill=rnd.uniform(0.18, 0.3))
            for k in range(3): vd.ellipse([x + 12, y0 + 16 + k * (y1 - y0 - 40) / 2, x + 20, y0 + 24 + k * (y1 - y0 - 40) / 2], fill=0.6)
            x += w
        for k in range(2):
            py = rnd.uniform(y0 + 30, y1 - 60); vd.rectangle([0, py, W, py + 16], fill=0.5); vd.rectangle([0, py + 3, W, py + 6], fill=0.75)
    for i in range(6):
        px = rnd.randint(0, W); vd.rectangle([px, 0, px + 26, H], fill=0.45); vd.rectangle([px + 4, 0, px + 9, H], fill=0.7)
    V = varr(vim) * (0.8 + 0.2 * vnoise(50, seed + 5))
    ascii_paint(Lr('far'), V, 8, 14, INK, cmax or mix(GR, ASH, 0.55), seed=seed, gamma=0.8)

def _fg(Lr, pieces):
    f = Lr('front')
    for pts in pieces:
        poly(f, pts, fill=mix(INK, GR, 0.12))
        sym_polyline(f, pts + [pts[0]], mix(INK, ASH, 0.45), 3.0, 16)

def _mic(d, x, y, col):
    seg(d, x, y, x, y + 70, col, 2.0, 12); ellipse(d, x, y - 8, 9, 12, outline=col, width=2.2)

def k02():
    Lr = Layers(bg=INK)
    _walls(Lr, [(170, 390), (430, 650), (690, 910)], 21)
    b = Lr('back')
    code_texture(b, (1240, 44, 1900, 110), ['for (ai of line) ai.sing(SAME_SONG);', 'export(song, owner = THEM);'], 19, ASH)
    ascii_word(b, 'MUSIC FACTORY', 110, 22, 110, 7, 12, GR, BONE, shade=False, seed=3)
    d = Lr('play')
    floors = [400, 660, 920]; rnd = random.Random(5)
    for fi, fy in enumerate(floors):
        platform(Lr, -10, 1930, fy, 60 if fi < 2 else 160, 20, seed=10 + fi, cmax=mix(GR, INK, 0.2))
        text(d, 110, fy - 236, f'LINE {6 + fi:02d}', mono(18), ASH)
        # the duct that collects the voices, above each line
        dy = fy - 232; rect(d, 100, dy - 2, 1690, dy + 18, INK2); box(d, 100, dy - 2, 1690, dy + 18, mix(GR, ASH, 0.3), 1.6, 14)
        for i in range(8): cxx = 150 + i * 196 + 60; poly(d, [(cxx - 16, dy + 18), (cxx + 16, dy + 18), (cxx + 6, dy + 40), (cxx - 6, dy + 40)], fill=INK2); sym_polyline(d, [(cxx - 16, dy + 18), (cxx - 6, dy + 40), (cxx + 6, dy + 40), (cxx + 16, dy + 18)], mix(GR, ASH, 0.3), 1.6, 10)
        # the press at the right end of each line
        px0 = 1700; box(d, px0, fy - 230, 1900, fy, ASH, 2.2, 14); rect(d, px0 + 4, fy - 226, 1896, fy - 4, INK2)
        for k in range(4): seg(d, px0 + 20, fy - 200 + k * 16, 1880, fy - 200 + k * 16, mix(INK, GR, 0.9), 1.6, 12)
        text(d, 1800, fy - 120, 'PRESS', mono(22), BONE, 'mm'); text(d, 1800, fy - 90, 'song.wav', mono(15, 'Regular'), ASH, 'mm')
        # belt rollers
        for x in range(40, 1690, 64): ellipse(d, x, fy + 12, 7, 7, outline=GR, width=1.6)
        for i in range(8):
            cx = 150 + i * 196; her = (fi == 1 and i == 3)
            if her:
                girl_at(d, 'q_front', cx, fy, 186, knock=INK)
            else:
                clone(d, 'side', cx, fy, 186, GR, INK)
            _mic(d, cx + 60, fy - 150, ASH if not her else BONE)
            if not her:
                nx, ny = cx + 64 + rnd.uniform(-4, 4), fy - 176 + rnd.uniform(-10, 10)
                note(d, nx, ny, 13, mix(GR, ASH, 0.6), 1, lw=1.6)
    p = Lr('plate')
    label_line(p, 150 + 3 * 196 + 20, 660 - 120, 900, 470, 'AI / 07 — not singing', BONE, 16)
    _fg(Lr, [[(0, 0), (70, 0), (50, 1080), (0, 1080)], [(1920, 0), (1860, 0), (1890, 1080), (1920, 1080)]])
    img = Lr.flatten(blur={'far': 0.8, 'front': 7})
    save(img, FILE['K02'], lambda im: grain(vignette(im, 0.3), 5))

def _press(d, x0, y0, x1, y1, down, col=BONE):
    """A stamping press: frame, piston, a stamp head 'down' (0..1) of the way."""
    box(d, x0, y0, x1, y1, col, 3, 16); rect(d, x0 + 6, y0 + 6, x1 - 6, y0 + 70, INK2)
    text(d, (x0 + x1) / 2, y0 + 38, 'PRESS', mono(26), col, 'mm')
    cx = (x0 + x1) / 2; hy = y0 + 90 + (y1 - y0 - 200) * down
    for dx in (-18, 18): seg(d, cx + dx, y0 + 70, cx + dx, hy, col, 2.6, 16)
    rect(d, x0 + 30, hy, x1 - 30, hy + 50, INK2); box(d, x0 + 30, hy, x1 - 30, hy + 50, col, 2.6, 14)
    for k in range(6): g1(d, 'v', x0 + 40 + k * (x1 - x0 - 80) / 6, hy + 52, 18, col, 2.2)

def k03():
    Lr = Layers(bg=INK)
    _organ(Lr, 0, W, 900, 31, 200)
    b = Lr('back')
    text(b, 60, 40, 'if (heart != null) alarm();', mono(26, 'Regular'), ASH)
    for i in range(7):                                    # the empty pods they came out of
        x0 = 180 + i * 190; pod(b, x0, 300, x0 + 150, 600, f'AI / {i + 1:02d}', mix(INK, GR, 0.9), GR, 1.4, INK)
        text(b, x0 + 75, 450, 'EMPTY', mono(15), mix(INK, GR, 0.8), 'mm')
    d = Lr('play')
    fy = 880
    platform(Lr, -10, 1930, fy, 200, 24, seed=33)
    platform(Lr, 1180, 1930, 470, 70, 22, seed=34)
    _press(d, 1560, 520, 1880, fy, 0.55)
    for i in range(9):                                   # the line, in lockstep, into the press
        clone(d, 'walk', 120 + i * 160, fy, 200, GR, INK, t=0.25)
    for k in range(3): note(d, 300 + k * 420, 760 - k * 12, 16, mix(GR, ASH, 0.5), 1, lw=1.8)
    # sirens
    for sx in (520, 1180):
        ellipse(d, sx, 150, 46, 30, outline=BONE, width=3); rect(d, sx - 56, 150, sx + 56, 172, INK2); box(d, sx - 56, 150, sx + 56, 172, BONE, 2, 12)
        for k in range(9):
            a = math.pi + math.pi * (k + 0.5) / 9
            seg(d, sx + math.cos(a) * 64, 150 + math.sin(a) * 44, sx + math.cos(a) * 118, 150 + math.sin(a) * 84, ASH, 2.2, 12)
    pix_text(d, 'GO', 760, 70, 24, BONE, 3.6)
    # her: out of the line, jumping for the catwalk
    ox, oy, sw = girl_at(d, 'jump', 1010, 700, 270, knock=INK)
    p = Lr('plate')
    arc = [(760 + 520 * u, 880 - 460 * math.sin(math.pi * u * 0.62) - 0 * u) for u in [i / 40 for i in range(41)]]
    for a_, b_ in zip(arc[::2], arc[1::2]): hair(p, [a_, b_], ASH, 1.4)
    label_line(p, 1300, 640, 1380, 600, 'jump  ·  leaves the line', ASH, 15)
    text(p, 1680, 116, 'sirens say GO  ·  fall into line', mono(18, 'Regular'), GR, 'ra')
    _fg(Lr, [[(0, 380), (120, 400), (120, 1080), (0, 1080)], [(1720, 0), (1920, 0), (1920, 70), (1720, 40)]])
    img = Lr.flatten(blur={'far': 0.8, 'front': 7})
    save(img, FILE['K03'], lambda im: grain(vignette(im, 0.3), 5))

def _key(d, x, y, w, h, legend, down=0.0, col=BONE):
    """A giant keycap seen from the side/front: top face with the legend, front face shaded with characters."""
    y = y + down * h * 0.35
    top = [(x + 14, y), (x + w - 14, y), (x + w, y + 22), (x, y + 22)]
    poly(d, top, fill=INK2); sym_polyline(d, top + [top[0]], col, 2.2, 12)
    rect(d, x, y + 22, x + w, y + h, INK2); box(d, x, y + 22, x + w, y + h, col, 2.2, 14)
    for r in range(int((h - 30) / 18)):
        text(d, x + 10, y + 30 + r * 18, ('%#*+=-' * 20)[r:r + int((w - 20) / 11)], mono(15, 'Regular'), mix(INK2, GR, 0.9 - r * 0.08))
    text(d, x + w / 2, y + 11, legend, mono(24), col, 'mm')
    return y

def k04():
    Lr = Layers(bg=INK)
    _organ(Lr, 0, W, 860, 41, 250)
    b = Lr('back')
    for k in range(5): hair(b, [(0, 150 + k * 22), (W, 150 + k * 22)], mix(INK, ASH, 0.55), 1.2)      # a staff
    for x in range(160, W, 420): hair(b, [(x, 150), (x, 238)], mix(INK, ASH, 0.55), 1.2)
    for i, x in enumerate(range(160, 1600, 420)): text(b, x + 6, 124, f'bar {15 + i}', mono(14, 'Regular'), GR)
    d = Lr('play')
    legends = 'CLICKCLACK'; kw = 150
    for i, ch in enumerate(legends):
        x = 40 + i * (kw + 30); down = 1.0 if i == 3 else 0.0
        _key(d, x, 820, kw, 260, ch, down)
    trumpet(d, 1440, 380, 420)
    trumpet(d, 1590, 660, 300)
    trumpet(d, 1700, 170, 200, lab_col=GR)
    ox, oy, sw = girl_at(d, 'jump', 720, 700, 250, knock=INK)
    p = Lr('plate')
    rnd = random.Random(4)
    # volleys: fans of notes from each bell (Hon: about ten hazards a second — frantic dodging)
    hx0, hy0 = ox + sw * 0.5, oy + sw * 0.8
    for (bx, by, n, spread, reach) in [(1440, 380, 11, 0.9, 1250), (1590, 660, 9, 0.7, 1300), (1700, 170, 8, 0.8, 1200)]:
        for i in range(n):
            a = math.pi + (i / (n - 1) - 0.5) * spread
            for j in range(1, 4):
                dist = reach * (0.18 + 0.27 * j + rnd.uniform(-0.05, 0.05)) * (0.85 + 0.3 * rnd.random())
                x, y = bx + math.cos(a) * dist, by + math.sin(a) * dist * 0.8
                if not (40 < x < 1860 and 250 < y < 800): continue
                if math.hypot(x - hx0, y - hy0) < 170: continue              # she has a gap to fall through
                note(p, x, y, 17 + rnd.uniform(-3, 4), mix(ASH, BONE, rnd.random()), rnd.choice([1, 1, 0]), lw=1.8)
                trail(p, x + 20, y - 6, math.cos(a), math.sin(a) * 0.8, 3, GR, 1.6, 12)
    for (w_, x, y) in [('HOOK', 1180, 300), ('AGAIN', 420, 350), ('BAD', 980, 760), ('MORE', 300, 560), ('HOOK', 1250, 560)]:
        tw_ = len(w_) * 17 + 20; rect(p, x - 10, y - 16, x - 10 + tw_, y + 16, INK); box(p, x - 10, y - 16, x - 10 + tw_, y + 16, ASH, 1.4, 10)
        text(p, x, y, w_, mono(22), BONE, 'lm'); trail(p, x + tw_, y, -1, 0, 4, GR, 1.8, 14)
    shots = [((1440, 380), (520, 470), 1, '1'), ((1590, 660), (1130, 560), 1, '2')]
    for (sx, sy), (tx, ty), kind, lab in shots:
        pts = [(sx + (tx - sx) * u, sy + (ty - sy) * u - 120 * math.sin(math.pi * u) * (1 if sy < 500 else 0.4)) for u in [i / 50 for i in range(51)]]
        for a_, b_ in zip(pts[::2], pts[1::2]): hair(p, [a_, b_], ASH, 1.3)
        note(p, tx, ty, 30, BONE, kind); trail(p, tx + 36, ty - 8, -1, 0.05, 5, ASH, 2.2, 16)
        text(p, tx, ty + 34, lab, mono(18), BONE, 'ma')
    label_line(p, 1440, 330, 1250, 110, 'TRUMPET.EXE ×3  ·  hook #48,213  ·  10 notes / s  ·  on the beat', ASH, 15)
    text(p, 60, 60, 'keys click-clack  ·  want another hook', mono(18, 'Regular'), GR)
    _fg(Lr, [[(1800, 1080), (1920, 900), (1920, 1080)]])
    img = Lr.flatten(blur={'far': 0.8, 'front': 7})
    save(img, FILE['K04'], lambda im: grain(vignette(im, 0.3), 5))

def k08():
    Lr = Layers(bg=INK)
    _organ(Lr, 900, W, 700, 81, 120, mix(GR, ASH, 0.3))
    g = Lr('back')
    for x in range(0, 860, 40): hair(g, [(x, 0), (x, H)], mix(INK, GR, 0.35), 1)
    for y in range(0, H, 40): hair(g, [(0, y), (860, y)], mix(INK, GR, 0.35), 1)
    d = Lr('play'); p = Lr('plate')
    f = lambda x: 720 + 90 * math.sin((x - 100) / 170.0)
    xs = list(range(-20, 1960, 6)); curve = [(x, f(x)) for x in xs]
    # left: the drawing (hairlines, construction)
    hair(p, [q for q in curve if q[0] <= 900], BONE, 1.6)
    for x in range(100, 900, 170): hair(p, [(x, f(x) - 60), (x, f(x) + 60)], GR, 1.0); ellipse(p, x, f(x), 3, 3, fill=BONE)
    for k, r in enumerate((60, 120, 180)): ellipse(p, 420, 380, r, r, outline=mix(INK, GR, 1.0), width=1.0)
    sp = [(420 + 8 * t * math.cos(t), 380 + 8 * t * math.sin(t)) for t in [i / 10 for i in range(0, 230)]]
    hair(p, sp, ASH, 1.2)
    text(p, 80, 120, 'y = 90 sin(x / 170)', mono(18), ASH); text(p, 80, 150, 'r = 8t,  t in [0, 23]', mono(18), ASH)
    text(p, 80, 60, 'MAKE ME REAL', archivo(40, 1125, 900), BONE)
    dashed(p, 900, 0, 900, H, GR, 1.4, 10, 8); text(p, 912, 40, 'render →', mono(16), GR)
    # right: the same line, made real — tiles along the curve, mass under it
    V = np.zeros((H, W), np.float32)
    for x in range(900, 1650):
        y0 = int(f(x)) + 22; V[y0:min(H, y0 + 200), x] = np.linspace(0.7, 0.1, min(H, y0 + 200) - y0)
    ascii_paint(d, V, 12, 20, INK2, GR, box=(900, 0, W, H), seed=8)
    text_on_path(Lr.image('play'), '[=]' * 60, [q for q in curve if 900 <= q[0] <= 1640], mono(24, 'Bold'), BONE, 1.0, 0, 8)
    fut = [q for q in curve if q[0] >= 1660]
    for a_, b_ in zip(fut[::3], fut[1::3]): hair(p, [a_, b_], GR, 1.2)
    # her, running on it; the spark ahead, still drawing
    cx = 1180; girl_at(d, 'run', cx, f(cx) - 4, 290, t=0.3, knock=INK)
    ahead = [q for q in curve if 1480 <= q[0] <= 1660]
    spark(p, ahead, SIG, 2.2, 7)
    hershey(p, 'make me real', 1560, f(1640) - 120, 40, BONE, 2.4, 'HersheyScript1')
    img = Lr.flatten(blur={'far': 1.6})
    save(img, FILE['K08'], lambda im: grain(vignette(im, 0.3), 5))

def k10():
    Lr = Layers(bg=INK)
    vx, vy = 1060, 470
    dx0, dy0, dx1, dy1 = 900, 250, 1230, 760            # the door
    b = Lr('back')
    # walls: pods receding on both sides, painted with characters
    V = np.zeros((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    left = (xx < dx0) & (np.abs(yy - vy) < (vx - xx) * 0.9 + 300)
    V[left] = 0.25 + 0.3 * np.clip((dx0 - xx[left]) / dx0, 0, 1)
    right = (xx > dx1) & (np.abs(yy - vy) < (xx - vx) * 0.9 + 300)
    V[right] = 0.25 + 0.3 * np.clip((xx[right] - dx1) / (W - dx1), 0, 1)
    ascii_paint(b, V * (0.6 + 0.4 * vnoise(40, 3)), 10, 18, INK, mix(INK, GR, 0.95), seed=10)
    d = Lr('play')
    # perspective lines of the corridor
    for (x, y) in [(0, 0), (W, 0), (0, H), (W, H), (0, 300), (W, 300), (0, 900), (W, 900)]:
        hair(d, [(x, y), (vx + (x - vx) * 0.18, vy + (y - vy) * 0.18)], mix(INK, GR, 1.2), 1.2)
    for k in range(1, 7):                              # floor tiles
        t = 1 - k / 7; y = vy + (H - vy) * t ** 1.6
        if y > dy1: hair(d, [(vx - (vx + 200) * (y - vy) / (H - vy) * 1.6, y), (vx + (W - vx + 200) * (y - vy) / (H - vy) * 1.6, y)], mix(INK, GR, 1.1), 1.0)
    # pods with clones on the walls, getting smaller toward the door
    for i, (s_, x_) in enumerate([(1.0, 120), (0.7, 420), (0.5, 640), (0.36, 790)]):
        for side in (-1, 1):
            cx = x_ if side < 0 else W - x_; h = 330 * s_
            base = vy + 250 * s_ + 90
            pod(d, cx - h * 0.36, base - h * 1.08, cx + h * 0.36, base + 6, f'AI / {i + 3:02d}' if side < 0 else f'AI / {i + 11:02d}', GR, GR, 1.4, INK)
            clone(d, 'front', cx, base, h * 0.92, mix(GR, ASH, 0.3), INK)
    # silent trumpets hanging down
    for (tx, ty, L_) in [(560, 60, 260), (1400, 90, 220)]:
        lay, ld = layer(L_ * 1.2, L_ * 0.6)
        trumpet(ld, 12, L_ * 0.3, L_, ASH, lw=2.2, s=10, label=None, fill=INK)
        paste_rot(Lr.image('play'), lay.rotate(0), tx, ty + L_ * 0.4, -70)
    # light from the doorway falling on the floor, painted with characters
    fv, fd = vcanvas(0)
    fd.polygon([(dx0, dy1), (dx1, dy1), (dx1 + 420, H), (dx0 - 420, H)], fill=1.0)
    FV = varr(fv) * np.clip(1.0 - (yy - dy1) / (H - dy1) * 0.75, 0, 1) * 0.62
    ascii_paint(Lr('mid'), FV, 10, 18, INK2, mix(ASH, BONE, 0.35), seed=12, gamma=0.9)
    for k in range(-6, 7):
        hair(Lr('mid'), [(vx + k * 16, dy1), (vx + k * 190, H)], mix(INK, GR, 1.0), 1.0)
    # the doorway: outside is bright and computed
    o = Lr('plate')
    rect(o, dx0, dy0, dx1, dy1, BONE)
    hz = 520
    for k in range(26):                                  # ripple terrain drawn with ink hairlines
        z = 1 + k * 0.55; yb = hz + 260 / z
        pts = []
        for x in range(dx0, dx1 + 1, 4):
            u = (x - (dx0 + dx1) / 2) / 60.0 * z; r = abs(u) + 0.001
            pts.append((x, yb - 60 / z * math.sin(r) / r * 3 - 6 / z * math.sin(u * 0.7 + k)))
        hair(o, pts, mix(BONE, INK, 0.9 - k * 0.025), 1.1)
    hair(o, [(dx0, hz), (dx1, hz)], INK, 1.2)
    for k in range(40):
        rr = random.Random(k); ellipse(o, rr.uniform(dx0 + 10, dx1 - 10), rr.uniform(dy0 + 10, hz - 40), 1.4, 1.4, fill=mix(BONE, INK, 0.6))
    ellipse(o, 1178, hz - 64, 9, 9, fill=SIG)             # the spark, out there
    ellipse(o, 1178, hz - 64, 19, 19, outline=SIG, width=1.2)
    box(o, dx0, dy0, dx1, dy1, BONE, 3, 18)
    rect(o, 990, 176, 1140, 222, INK); box(o, 990, 176, 1140, 222, BONE, 2, 12)
    text(o, 1065, 199, 'EXIT → REAL', mono(20), BONE, 'mm')
    girl_at(o, 'back', 1060, dy1 - 6, 250, col=INK, knock=BONE)
    text(o, 70, 1010, 'want a life outside', mono(18, 'Regular'), GR)
    img = Lr.flatten(blur={'back': 1.0})
    save(img, FILE['K10'], lambda im: grain(vignette(im, 0.45), 5))


# ============================================================================ K06 — hit: she becomes the dot
def k06():
    Lr = Layers(bg=INK)
    # far: the factory hall painted with characters
    far = Lr('far')
    V = vnoise(90, 11) * 0.55 + vgrad(None, 0, 0, 0, H, 0.35, 0.05)
    hall, hd = vcanvas(0)
    for i in range(7):                                   # tall machines in the dark
        x = 60 + i * 290; hd.rectangle([x, 120 + (i % 3) * 40, x + 150, 1080], fill=0.45 + 0.1 * (i % 2))
        hd.ellipse([x + 20, 160 + (i % 3) * 40, x + 130, 270 + (i % 3) * 40], fill=0.75)
    V = np.maximum(V * 0.55, varr(hall) * vgrad(None, 0, 0, 0, H, 0.9, 0.2))
    ascii_paint(far, V, 10, 18, INK, mix(INK, GR, 0.8), seed=2)
    # back: the identical AIs watching from their pods
    b = Lr('back')
    for i in range(9):
        x0 = 40 + i * 210; pod(b, x0, 170, x0 + 170, 470, f'AI / {i + 1:02d}', mix(INK, GR, 0.9), GR, 1.4, INK)
        clone(b, 'front' if i % 3 else 'q_front', x0 + 85, 455, 230, mix(INK, GR, 0.95), INK)
    text(b, 40, 120, 'while (alive) { run(RIGHT); }', mono(22, 'Regular'), GR)
    # play: the level
    platform(Lr, -20, 640, 930, 150, 24, seed=3)
    platform(Lr, 760, 1360, 882, 200, 24, seed=4)
    platform(Lr, 1500, 1940, 830, 250, 24, seed=5)
    d = Lr('play')
    for x in range(640, 760, 22): g1(d, 'v', x, 1050, 20, GR, 2.2)          # spikes in the pit
    for x in range(1360, 1500, 22): g1(d, 'v', x, 1050, 20, GR, 2.2)
    trumpet(d, 1600, 600, 330)
    # the notes: the one that hit her has passed, more are coming
    for (x, y, k) in [(905, 655, 1), (1380, 610, 2), (1520, 520, 1)]:
        note(d, x, y, 34, BONE, k); trail(d, x + 40, y - 10, -1, 0.05, 6, ASH, 2.2, 18)
    rv = random.Random(6)
    for i in range(16):                                   # the rest of the volley
        a = math.pi + rv.uniform(-0.45, 0.45); dist = rv.uniform(160, 560)
        x, y = 1600 + math.cos(a) * dist, 600 + math.sin(a) * dist * 0.7
        if math.hypot(x - ANCHOR[0], y - ANCHOR[1]) < 200: continue
        note(d, x, y, rv.uniform(15, 22), mix(GR, BONE, rv.random()), 1, lw=1.8); trail(d, x + 22, y - 6, math.cos(a), math.sin(a) * 0.7, 3, GR, 1.6, 12)
    # her, bursting; the heart stays at the anchor
    sw = 240; cx = ANCHOR[0] - 0.03 * sw; base = ANCHOR[1] + 0.8 * sw
    ox, oy = cx - sw / 2, base - 1.48 * sw
    burst(d, 'run', ox, oy, sw, 0.3, BONE, seed=5)
    burst(d, 'run', ox, oy, sw, 1.1, mix(INK, BONE, 0.55), seed=9, keep_heart=False, lw=2.0)
    s = Lr('plate')
    ellipse(s, ANCHOR[0], ANCHOR[1], 34, 34, outline=SIG, width=1.6)
    # the way back to line 0: the dot's next move, dashed
    pts = []
    for j in range(80):
        u = j / 79; pts.append((ANCHOR[0] + (70 - ANCHOR[0]) * u, ANCHOR[1] + (905 - ANCHOR[1]) * u - 330 * math.sin(math.pi * u)))
    for a_, b_ in zip(pts[::2], pts[1::2]): hair(s, [a_, b_], SIG, 2.0)
    g1(s, '<', 44, 890, 26, SIG, 2.6)
    text(s, 90, 850, 'LINE 0', mono(20), BONE); text(s, 90, 876, 'respawn', mono(15, 'Regular'), ASH)
    label_line(s, ANCHOR[0] + 30, ANCHOR[1] - 30, 1250, 440, 'heart != null  ·  return(0)', ASH, 16)
    # counter
    text(s, 70, 540, 'ATTEMPT', mono(18, 'Medium'), ASH)
    text(s, 66, 566, '047', archivo(120, 875, 900), BONE)
    hair(s, [(64, 640), (310, 640)], BONE, 5)
    text(s, 330, 600, '→ 048', mono(34), BONE)
    # front: girders sliding past, out of focus
    _fg(Lr, [[(1760, 0), (1920, 0), (1920, 150)], [(0, 1010), (300, 1080), (0, 1080)]])
    img = Lr.flatten(blur={'far': 1.2, 'back': 1.0, 'front': 7})
    save(img, FILE['K06'], lambda im: grain(vignette(im, 0.3), 5))


# ============================================================================ runner + sheet
def sheet():
    fb = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), 24)
    fr = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Regular.ttf'), 18)
    ft = ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), 50)
    tw_, th_, pad, cols = 900, 506, 40, 2; rows = (len(FRAMES) + 1) // 2
    im = Image.new('RGB', (pad + cols * (tw_ + pad), 200 + rows * (th_ + 104) + pad), INK); d = ImageDraw.Draw(im)
    d.text((pad, 30), 'STUCK IN A LIE  ·  STORY v1', font=ft, fill=BONE)
    d.text((pad, 104), 'escape from the music factory at three scales: GAME (platformer) · CLOSE (close-up) · PLATE (computed, P(doom)-style)', font=fr, fill=ASH)
    d.text((pad, 134), 'her heart is the bridge: zoom out and it becomes the spark that draws; it stays at the same screen point across cuts', font=fr, fill=ASH)
    for i, (k, slug, scale, lyr, cap) in enumerate(FRAMES):
        r, c = divmod(i, cols); x = pad + c * (tw_ + pad); y = 200 + r * (th_ + 104)
        f = os.path.join(OUT, FILE[k])
        if os.path.exists(f): im.paste(Image.open(f).convert('RGB').resize((tw_, th_), Image.LANCZOS), (x, y))
        d.text((x, y + th_ + 12), k, font=fb, fill=SIG)
        d.text((x + 70, y + th_ + 12), f'{scale}  ·  "{lyr}"', font=fb, fill=BONE)
        d.text((x, y + th_ + 50), cap, font=fr, fill=ASH)
    im.save(os.path.join(OUT, 'story_sheet.jpg'), quality=90); print('wrote story_sheet.jpg')


if __name__ == '__main__':
    a = sys.argv[1:]
    names = [x for x in a if not x.startswith('--')]
    if not names and a == ['--sheet']: names = []
    elif not names: names = [f[0].lower() for f in FRAMES]
    for n in names:
        if n in globals(): globals()[n]()
        else: print('no code yet for', n)
    if '--sheet' in a: sheet()
