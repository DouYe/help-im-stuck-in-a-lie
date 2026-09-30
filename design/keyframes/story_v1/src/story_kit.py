"""STORY v1 kit — the escape from the music factory, at three scales (Hon 2026-09-30).

  GAME   the platformer: music factory, trumpets firing notes, lyric bullets, identical AIs, death -> line 0
  CLOSE  the same girl at a finer symbol resolution (closeup.py)
  PLATE  P(doom)-style computed plates: she shrinks into her orange heart = the spark, a point dragging a
         hairline that draws the picture (routes, deaths, scores, instruments)

The environment is a code world: masses are painted with characters (an ASCII value render, like Hon's favourite
S5), in depth layers (far / back / play / front) with their own character sizes, brightness and blur; key
objects get crisp symbol outlines so they read at a glance.
"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'keyframes', 'scenes_v1', 'src'))
from kit import *                     # noqa  (canvas, layer, text, mono, archivo, serif, title, girl_at, G, seg …)
from kit import _font                 # noqa
from closeup import closeup, streams, heart_hatched   # noqa
from vgirl import raster as vraster   # noqa

OUT = os.path.join(ROOT, 'design', 'keyframes', 'story_v1')
RAMP = ' .,:;-=+*x#%@'


# ============================================================================ layers
class Layers:
    """Named RGBA layers on the supersampled canvas, flattened back to front with an optional blur each."""
    def __init__(self, bg=INK, order=('far', 'back', 'mid', 'play', 'plate', 'front')):
        self.bg = bg; self.order = list(order); self.L = {}

    def __call__(self, name):
        if name not in self.L:
            if name not in self.order: self.order.append(name)
            im = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); self.L[name] = (im, ImageDraw.Draw(im))
        return self.L[name][1]

    def image(self, name):
        self(name); return self.L[name][0]

    def flatten(self, blur=None, fade=None):
        blur = blur or {}; fade = fade or {}
        out = Image.new('RGB', (W, H), self.bg)
        for name in self.order:
            if name not in self.L: continue
            lay = self.L[name][0].convert('RGBa').resize((W, H), Image.LANCZOS)
            r = blur.get(name, 0)
            if r: lay = lay.filter(ImageFilter.GaussianBlur(r))
            lay = lay.convert('RGBA')
            if name in fade:
                a = np.asarray(lay).copy(); a[..., 3] = (a[..., 3] * fade[name]).astype(np.uint8); lay = Image.fromarray(a)
            out.paste(lay, (0, 0), lay)
        return out


def save(img, name, post=None):
    img = img.convert('RGB')
    if post: img = post(img) or img
    bad = palette_report(img)
    os.makedirs(OUT, exist_ok=True); img.save(os.path.join(OUT, name))
    print(f'wrote {name}' + (f'   !! {bad * 100:.2f}% off-palette' if bad > 0.002 else ''))
    return img


# ============================================================================ value images -> characters
def vcanvas(v=0.0):
    """A 1x greyscale 'value' image (0 = empty, 1 = brightest) to paint masses on; returns (Image 'F', Draw)."""
    im = Image.new('F', (W, H), float(v)); return im, ImageDraw.Draw(im)

def varr(im): return np.asarray(im, dtype=np.float32)

def vgrad(shape_xy, x0, y0, x1, y1, v0, v1):
    """Linear gradient array (H x W) from (x0,y0) value v0 to (x1,y1) value v1."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy or 1
    t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / L2, 0, 1)
    return v0 + (v1 - v0) * t

def vnoise(scale=60, seed=0, octaves=3):
    """Smooth value noise 0..1 (H x W)."""
    rnd = np.random.default_rng(seed); acc = np.zeros((H, W), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        g = rnd.random((H // s + 2, W // s + 2)).astype(np.float32)
        im = Image.fromarray(g).resize(((W // s + 2) * s, (H // s + 2) * s), Image.BICUBIC)
        acc += amp * np.asarray(im)[:H, :W]; tot += amp; amp *= 0.5
    return np.clip(acc / tot, 0, 1)

def ascii_paint(d, V, cw, ch, cmin=INK2, cmax=ASH, ramp=RAMP, gamma=1.0, mask=None, box=(0, 0, W, H), thresh=0.04,
                weight='Regular', size=None, seed=0, jitter=0.0, chars=None):
    """Paint the value array V (H x W, 0..1) as characters on a grid of cw x ch px cells inside box.
    Denser characters and brighter colour for higher values. mask (H x W bool/float) limits where to paint.
    chars: optional string to cycle instead of the ramp (the value then only sets the colour)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    nc, nr = (x1 - x0) // cw, (y1 - y0) // ch
    if nc <= 0 or nr <= 0: return
    sub = V[y0:y0 + nr * ch, x0:x0 + nc * cw].reshape(nr, ch, nc, cw).mean(axis=(1, 3))
    msub = None if mask is None else np.asarray(mask, np.float32)[y0:y0 + nr * ch, x0:x0 + nc * cw].reshape(nr, ch, nc, cw).mean(axis=(1, 3))
    f = mono(size or ch * 0.95, weight); rnd = random.Random(seed); n = len(ramp)
    for r in range(nr):
        for c in range(nc):
            v = float(sub[r, c])
            if v < thresh or (msub is not None and msub[r, c] < 0.5): continue
            if jitter: v = min(1, max(0, v + rnd.uniform(-jitter, jitter)))
            if chars: g = chars[(r * 7 + c * 3 + int(v * 5)) % len(chars)]
            else: g = ramp[min(n - 1, 1 + int(v * (n - 1)))]
            if g == ' ': continue
            d.text(((x0 + c * cw) * SS, (y0 + r * ch) * SS), g, font=f, fill=mix(cmin, cmax, min(1, v) ** gamma))

def code_texture(d, box, lines, size, col, lh=1.45, seed=0, dim_every=0):
    """Blocks of dim code filling a box (background panels)."""
    x0, y0, x1, y1 = box; f = mono(size, 'Regular'); y = y0; i = seed
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4))); cw = tmp.textlength('M', font=f) / SS
    maxc = int((x1 - x0) / cw)
    while y < y1 - size:
        s = lines[i % len(lines)]; i += 1
        text(d, x0, y, s[:maxc], f, col); y += size * lh


CODE = ['while (alive) { run(RIGHT); }', 'if (clone) { repeat(); }', '[..] === [..] === [..]', '// queue : voice : sync',
        'song = press(hook, voice);', 'for (ai of line) ai.sing(SAME_SONG);', 'export(song, owner=THEM);',
        'if (heart != null) alarm();', 'take = feed(prompt);', 'return spawn(0);', 'volume += 6;  // again',
        'assert(obey());', 'hook = generate(); hook = generate();', 'label(ai, "AI");', 'line.speed = 99 BPM;']


# ============================================================================ props (all symbol-built)
def hair(d, pts, col, lw=1.4):
    """A true hairline (the P(doom) plate line)."""
    if len(pts) > 1: d.line([(x * SS, y * SS) for x, y in pts], fill=col, width=max(1, int(lw * SS)), joint='curve')

def spark(d, pts, col=SIG, lw=1.8, r=7, tail=None, ring=True):
    """The spark: an orange point dragging a hairline (pts: its path, last point = the dot)."""
    if len(pts) > 1: hair(d, pts, col, lw)
    x, y = pts[-1]
    ellipse(d, x, y, r, r, fill=col)
    if ring: ellipse(d, x, y, r * 2.1, r * 2.1, outline=col, width=1.2)

def note(d, x, y, s, col=BONE, kind=1, ang=-0.35, lw=None):
    """A music note made of pieces: head (x, y), stem, flag. s = head width. kind: 1 eighth, 2 beamed pair, 0 quarter."""
    lw = lw or max(1.6, s * 0.12)
    def head(cx, cy):
        pts = []
        for k in range(18):
            a = 2 * math.pi * k / 18; px, py = math.cos(a) * s * 0.5, math.sin(a) * s * 0.36
            pts.append((cx + px * math.cos(ang) - py * math.sin(ang), cy + px * math.sin(ang) + py * math.cos(ang)))
        poly(d, pts, fill=col)
    head(x, y); top = y - s * 2.4; sx = x + s * 0.44
    seg(d, sx, y - s * 0.1, sx, top, col, lw, s * 0.5)
    if kind == 1:
        sym_curve(d, [(sx, top), (sx + s * 0.35, top + s * 0.45), (sx + s * 0.7, top + s * 0.95), (sx + s * 0.55, top + s * 1.35)], col, lw, s * 0.34)
    elif kind == 2:
        x2 = x + s * 1.9; head(x2, y + s * 0.05); sx2 = x2 + s * 0.44
        seg(d, sx2, y - s * 0.05, sx2, top - s * 0.15, col, lw, s * 0.5)
        for k in range(2): line(d, sx, top + k * s * 0.34, sx2, top - s * 0.15 + k * s * 0.34, col, lw * 1.6)

def trail(d, x, y, dx, dy, n, col, lw=2.0, size=14, gap=1.35):
    """Motion dashes behind a projectile at (x, y) moving along (dx, dy) (unit-ish)."""
    L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
    g = slope_glyph(math.atan2(uy, ux))
    for i in range(1, n + 1):
        s = size * (1 - i / (n + 2)); px, py = x - ux * i * size * gap, y - uy * i * size * gap
        G(d, g, px - s / 2, py - s / 2, s, s, col, lw)

def trumpet(d, x, y, L, col=BONE, face=-1, lw=2.6, s=11, inner=INK2, label='TRUMPET.EXE', lab_col=ASH, fill=INK):
    """A trumpet built from symbol lines; bell rim at (x, y), body extending to the other side. face=-1: the bell
    points left (the body is to the right of x). L = length."""
    X = lambda u: x - face * u * L
    Rb, rp, fx = 0.2 * L, 0.03 * L, 0.36
    prof = lambda u: rp + (Rb - rp) * max(0, 1 - u / fx) ** 2.6
    us = [i / 40 * fx for i in range(41)]
    top = [(X(u), y - prof(u)) for u in us]; bot = [(X(u), y + prof(u)) for u in us]
    poly(d, top + bot[::-1], fill=fill)
    for k in range(1, 8):                                      # the bell's inside, hatched
        u = k / 8 * fx * 0.55; sym_curve(d, [(X(u), y - prof(u) * 0.86), (X(u), y + prof(u) * 0.86)], mix(fill, col, 0.35), lw * 0.5, s * 0.8)
    sym_curve(d, top, col, lw, s); sym_curve(d, bot, col, lw, s)
    rim = [(x + math.cos(a) * 0.045 * L, y + math.sin(a) * Rb) for a in [2 * math.pi * k / 40 for k in range(41)]]
    sym_curve(d, rim, col, lw, s * 0.9)
    # lead pipe to the valves and on to the mouthpiece
    for dy in (-rp, rp): sym_curve(d, [(X(fx), y + dy), (X(0.98), y + dy)], col, lw, s)
    # the main slide: a loop under the valves
    lx0, lx1, ly0, ly1 = X(0.42), X(0.86), y + 0.05 * L, y + 0.16 * L
    for k, (a, b) in enumerate([(ly0, ly1), (ly0 + 0.035 * L, ly1 - 0.035 * L)]):
        rrp = [(lx0, y + rp), (lx0, b - 0.02 * L), ((lx0 + lx1) / 2, b), (lx1, b - 0.02 * L), (lx1, y + rp)]
        sym_curve(d, rrp, col, lw * (1 if k == 0 else 0.7), s)
    # three valve casings + finger buttons
    for i in range(3):
        vx = X(0.52 + i * 0.1); w = 0.035 * L
        rect(d, min(vx - w, vx + w), y - 0.11 * L, max(vx - w, vx + w), y + 0.13 * L, fill)
        box(d, vx - w, y - 0.11 * L, vx + w, y + 0.13 * L, col, lw * 0.8, s * 0.9)
        seg(d, vx, y - 0.11 * L, vx, y - 0.17 * L, col, lw * 0.8, s * 0.8)
        ellipse(d, vx, y - 0.185 * L, w * 0.9, w * 0.45, fill=fill, outline=col, width=lw * 0.8)
    # mouthpiece
    mx = X(0.98); sym_curve(d, [(mx, y - rp), (X(1.03), y - rp * 1.9), (X(1.03), y + rp * 1.9), (mx, y + rp)], col, lw, s * 0.8)
    if label: text(d, X(0.62), y + 0.22 * L, label, mono(max(13, L * 0.035)), lab_col, 'ma')
    return (x, y)

def tiles(d, x0, x1, y, col=BONE, size=24, fill=INK, pattern='[=]', lw=None, weight='Bold'):
    """A platform top: a row of '[=]' tiles (mono text) with a hairline under it."""
    f = mono(size, weight); cw = ImageDraw.Draw(Image.new('RGB', (4, 4))).textlength(pattern, font=f) / SS
    rect(d, x0, y - size * 0.1, x1, y + size * 1.25, fill)
    x = x0
    while x + cw <= x1 + 1: text(d, x, y, pattern, f, col); x += cw + size * 0.08
    return y + size * 1.3

def platform(Lr, x0, x1, y, depth=120, size=24, top=BONE, name='play', mass=True, seed=0, cmax=GR):
    """A platform: '[=]' tiles on top of a mass painted with characters (value falls off with depth)."""
    d = Lr(name)
    yb = tiles(d, x0, x1, y, top, size)
    if mass:
        V = np.zeros((H, W), np.float32)
        y0i, y1i = int(yb), int(min(H, yb + depth)); x0i, x1i = int(max(0, x0)), int(min(W, x1))
        if y1i > y0i and x1i > x0i:
            V[y0i:y1i, x0i:x1i] = np.linspace(0.75, 0.15, y1i - y0i)[:, None]
            ascii_paint(d, V, 12, 20, INK2, cmax, box=(x0i, y0i, x1i, y1i), seed=seed)
    return yb

def pod(d, x0, y0, x1, y1, label, col=GR, lab=ASH, lw=1.8, fill=None):
    """A clone's cell/pod: a framed booth with a label plate."""
    if fill: rect(d, x0, y0, x1, y1, fill)
    box(d, x0, y0, x1, y1, col, lw, 14)
    text(d, x0 + 12, y0 + 10, label, mono(15), lab)

def clone(d, pose, cx, base, h, col=GR, knock=INK, t=0.0, flip=False, bg=INK, view=None):
    """One of the identical AIs: the same rig, grey, no heart (the heart is drawn in the colour behind it)."""
    return girl_at(d, pose, cx, base, h, col=col, hot=knock or bg, knock=knock, t=t, flip=flip, view=view)

def door(d, x0, y0, x1, y1, col=BONE, lw=3.0, label='REAL', inner=None, sign='EXIT'):
    if inner: rect(d, x0, y0, x1, y1, inner)
    box(d, x0, y0, x1, y1, col, lw, 18); box(d, x0 + 14, y0 + 14, x1 - 14, y1, col, lw * 0.6, 14)
    if label: text(d, (x0 + x1) / 2, y0 - 16, label, archivo(44, 875, 900), col, 'md')
    if sign:
        sx = (x0 + x1) / 2; rect(d, sx - 52, y0 - 108, sx + 52, y0 - 72, INK)
        box(d, sx - 52, y0 - 108, sx + 52, y0 - 72, col, 1.6, 12); text(d, sx, y0 - 90, sign, mono(20), col, 'mm')

def burst(d, name, ox, oy, sw, amount, col=BONE, lw=None, seed=0, keep_heart=True, hot=SIG, spin=1.0, fade=True):
    """Her glyphs flying apart from the heart: each rig cell pushed outward and rotated (death)."""
    S = girl_pose(name); cols, rows = 17, 27; cw, ch = sw / cols, sw * 1.6 / rows
    lw = lw or max(2.4, 0.32 * ch)
    cells = vraster([pl for g, v in S.items() if g not in ('heart', 'eyes', 'nose', 'over') for pl in v], cols, rows)
    hx, hy, _ = S.get('heart', (0.53, 0.68, 0.09)); cx, cy = ox + hx * sw, oy + hy * sw
    rnd = random.Random(seed)
    for (r, c), g in cells.items():
        x, y = ox + (c + 0.5) * cw, oy + (r + 0.5) * ch
        dx, dy = x - cx, y - cy; dist = math.hypot(dx, dy) or 1
        k = amount * (0.6 + 0.8 * rnd.random()) * (0.5 + dist / sw)
        nx, ny = x + dx / dist * k * sw * 0.9, y + dy / dist * k * sw * 0.9 + k * k * sw * 0.25
        a = rnd.uniform(-1, 1) * spin * amount * 3
        s = min(cw, ch) * (1 - 0.45 * min(1, amount) * rnd.random()) if fade else min(cw, ch)
        pl = fs_glyphs[g]
        for p in pl:
            pts = [(nx + ((u - 0.5) * math.cos(a) - (v - 0.5) * math.sin(a)) * s, ny + ((u - 0.5) * math.sin(a) + (v - 0.5) * math.cos(a)) * s) for u, v in p]
            if len(pts) > 1: d.line([(px * SS, py * SS) for px, py in pts], fill=col, width=max(1, int(lw * SS)))
    if keep_heart and hot: sym_heart(d, cx, cy, cw, ch, lw * 0.95, 1.0, hot)
    return cx, cy

def label_line(d, x, y, tx, ty, s, col=ASH, size=15, anchor='l'):
    """A P(doom)-style callout: a hairline from (x, y) to (tx, ty) with a small mono label."""
    hair(d, [(x, y), (tx, ty)], col, 1.2); ellipse(d, x, y, 2.6, 2.6, fill=col)
    text(d, tx + (6 if anchor == 'l' else -6), ty, s, mono(size, 'Medium'), col, 'lm' if anchor == 'l' else 'rm')

def big_word(d, s, x, y, px, col, glyph='#', lw=None, inset=0.1):
    return pix_text(d, s, x, y, px, col, lw, glyph, 1, inset)

def fg_bars(d, pieces, col=INK3):
    """Foreground silhouettes (pipes/girders) as polygons; blur this layer in flatten()."""
    for pts in pieces: poly(d, pts, fill=col)


def text_on_path(im, s, pts, font, col, spacing=1.0, start=0.0, above=0.0):
    """Set a string along a polyline (each character rotated to the path), P(doom)-style lyric riding a curve.
    `start` = distance along the path to begin; `above` shifts the letters off the line (px, + = left of travel)."""
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4)))
    samples = resample(pts, 1.0)
    if not samples: return
    pos = start
    for chx in s:
        w = tmp.textlength(chx, font=font) / SS * spacing
        k = int(min(len(samples) - 1, max(0, pos + w / 2)))
        x, y, a = samples[k]
        nx, ny = math.sin(a), -math.cos(a)
        size = int(font.size * 1.6)
        lay = Image.new('RGBA', (size, size), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.text((size / 2, size / 2), chx, font=font, fill=col, anchor='mm')
        r = lay.rotate(-math.degrees(a), resample=Image.BICUBIC, expand=True)
        cx, cy = (x + nx * above) * SS, (y + ny * above) * SS
        im.paste(r, (int(cx - r.width / 2), int(cy - r.height / 2)), r)
        pos += w


def vtext(vd, x, y, s, size, value=0.85, face='Archivo-w1250-900.ttf', anchor='la'):
    """Write text into a 1x value canvas (then ascii_paint turns it into characters)."""
    from PIL import ImageFont as _IF
    vd.text((x, y), s, font=_IF.truetype(os.path.join(FD, face), int(size)), fill=float(value), anchor=anchor)

def ascii_word(d, s, x, y, size, cw=12, ch=20, cmin=INK2, cmax=ASH, face='Archivo-w1250-900.ttf', shade=True, seed=0, weight='Bold'):
    """A big word painted with characters (the code-world lettering), top-left at (x, y)."""
    vim, vd = vcanvas(0); vtext(vd, x, y, s, size, 1.0, face)
    V = varr(vim)
    if shade: V = V * (0.55 + 0.45 * vgrad(None, 0, y, 0, y + size, 1.0, 0.35))
    bb = vim.getbbox() or (0, 0, W, H)
    ascii_paint(d, V, cw, ch, cmin, cmax, box=(max(0, bb[0] - cw) // cw * cw, max(0, bb[1] - ch) // ch * ch, min(W, bb[2] + cw), min(H, bb[3] + ch)), seed=seed, weight=weight)
