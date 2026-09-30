"""SCENES v1 kit — shared drawing helpers for the ~50 scene frames (Hon 2026-09-30: "直接五十个场景" + B-roll).

Everything here draws on a supersampled canvas (SS = 3): you pass coordinates in 1920x1080 frame pixels, the
helpers multiply by SS. `save_scene(im, '12A')` downsamples to 1920x1080, runs optional 1x post effects,
checks the palette and writes design/keyframes/scenes_v1/<file from plan.py>.

Import in a scene module:   from kit import *
Rules that every frame must follow are in plan.py (RULES) and design/STYLE_BIBLE.md.
"""
import math, os, re, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'character', 'src'))
sys.path.insert(0, os.path.join(ROOT, 'design', 'keyframes', 'styles_v1', 'src'))
sys.path.insert(0, HERE)
import final_sheet as fs
from final_sheet import render as girl, glyph as G, SS, HEART, sym_heart
from vgirl import pose as girl_pose
import make_styles as ms
from make_styles import (text, tw, line, rect, seg, box, pixword, pixwidth, clip_line, hatch, ring, paste_layer,
                         panel, balloon, mix, PIX)
from plan import PLAN, BY_ID

OUT = os.path.join(ROOT, 'design', 'keyframes', 'scenes_v1')
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
W, H = 1920, 1080

# ---------------------------------------------------------------- palette (locked: black / white / greys + ONE orange)
INK = (10, 10, 11)      # near-black
INK2 = (22, 22, 24)     # raised black
INK3 = (36, 35, 36)     # panel black
GR = (94, 91, 87)       # mid grey
ASH = (156, 151, 143)   # light grey
PAPER = (214, 209, 199) # grey paper
BONE = (238, 233, 223)  # off-white
SIG = (255, 83, 20)     # THE orange (#FF5314)
SIG_D = mix(INK, SIG, 0.55)   # dark orange (orange mixed with black)
SIG_L = mix(BONE, SIG, 0.45)  # pale orange


# ---------------------------------------------------------------- fonts (project fonts only, so it runs on Hon's PC too)
_fc = {}
def _font(path, size, var=None):
    k = (path, int(size * SS), var)
    if k not in _fc:
        f = ImageFont.truetype(os.path.join(FD, path), int(size * SS))
        if var:
            try: f.set_variation_by_name(var)
            except Exception: pass
        _fc[k] = f
    return _fc[k]

def mono(size, weight='Bold'):
    """IBM Plex Mono. weight: Light, Regular, Medium, SemiBold, Bold, Italic."""
    return _font(os.path.join('src', f'IBMPlexMono-{weight}.ttf'), size)

def archivo(size, width=1000, weight=700):
    """Archivo grotesque. width: 620 (extra condensed) 750 875 1000 1125 1250 (expanded); weight 300 500 700 900."""
    return _font(f'Archivo-w{width}-{weight}.ttf', size)

def title(size): return archivo(size, 1250, 900)          # the wide black title face used in the sheets

def archivo_italic(size, width=1000, weight=800): return _font(f'ArchivoItalic-w{width}-{weight}.ttf', size)

def serif(size, italic=False, weight='Regular'):
    """Cormorant Garamond (variable). weight: Light Regular Medium SemiBold Bold."""
    return _font(os.path.join('src', 'CormorantGaramond-Italic[wght].ttf' if italic else 'CormorantGaramond[wght].ttf'), size, weight)


# ---------------------------------------------------------------- canvas & layers
def canvas(bg=INK):
    im = Image.new('RGB', (W * SS, H * SS), bg)
    return im, ImageDraw.Draw(im)

def layer(w, h, bg=(0, 0, 0, 0)):
    """A transparent (or filled) RGBA layer of w x h frame pixels; draw on it with the same helpers."""
    im = Image.new('RGBA', (int(w * SS), int(h * SS)), bg)
    return im, ImageDraw.Draw(im)

def paste(im, lay, x, y):
    """Paste an RGBA layer with its top-left at frame (x, y)."""
    im.paste(lay, (int(x * SS), int(y * SS)), lay if lay.mode == 'RGBA' else None)

def paste_rot(im, lay, cx, cy, angle):
    """Rotate an RGBA layer by `angle` degrees (counter-clockwise) and paste it centred on frame (cx, cy)."""
    r = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.paste(r, (int(cx * SS - r.width / 2), int(cy * SS - r.height / 2)), r)

def poly(d, pts, fill=None, outline=None, width=1):
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=outline, width=max(1, int(width * SS)) if outline else 0)

def ellipse(d, cx, cy, rx, ry, fill=None, outline=None, width=1):
    d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=fill, outline=outline,
              width=max(1, int(width * SS)) if outline else 0)

def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS, fill=fill, outline=outline,
                        width=max(1, int(width * SS)) if outline else 0)

def g1(d, g, x, y, size, col, lw):
    """One stroke glyph (see design/character/src/glyphs.py: | - = / \\ _ ` . : ' , + x ^ v < > [ ] ( ) # o 0 1 L J r 7)
    in a size x size cell with its top-left at (x, y)."""
    G(d, g, x, y, size, size, col, lw)

def glyph_row(d, s, x, y, size, col, lw, gap=0.0):
    """A row of stroke glyphs (only the characters glyphs.py knows; others are skipped)."""
    for i, ch in enumerate(s):
        if ch in fs_glyphs: G(d, ch, x + i * size * (1 + gap), y, size, size, col, lw)
    return len(s) * size * (1 + gap)

from glyphs import G as fs_glyphs


# ---------------------------------------------------------------- the girl
GIRL_H = 1.47   # her height (hair top to feet) in units of the rig width `sw`

def girl_at(d, name, cx, base, height, **kw):
    """Draw her centred on x = cx with her feet on y = base, `height` frame pixels tall (hair to feet).
    kw go to final_sheet.render: t (walk/run phase 0..1), flip, view='above', knock (bg colour for the knockout,
    None = none), col (line colour), hot (heart colour), sub (glyph -> glyph restyle, e.g. lambda g: 'x'), lw.
    Poses: front, heart (hands on the heart, bigger heart), help (arms up, o eyes), frontwalk, q_front (45°, THE
    default 3/4 view), q_frontwalk, q_back, back, backwalk, side (standing, facing right), walk, run, jump, fall, stuck.
    Returns (ox, oy, sw) — the rig box: x from ox to ox+sw, y from oy to oy+1.6*sw."""
    sw = height / GIRL_H
    ox, oy = cx - sw / 2, base - 1.48 * sw
    girl(d, name, ox, oy, sw, **kw)
    return ox, oy, sw

def girl_point(ox, oy, sw, u, v):
    """Frame position of rig coordinate (u, v) (u 0..1 across, v 0..1.6 down) — e.g. her heart is ~(0.53, 0.68)."""
    return ox + u * sw, oy + v * sw

def girl_polys(name, t=0.0):
    """Her raw vector strokes: dict group -> list of polylines in the 1 x 1.6 rig box (for constellations etc.)."""
    return girl_pose(name, t)


# ---------------------------------------------------------------- symbol drawing helpers
def dashed(d, x0, y0, x1, y1, col, lw, dash=14, gap=10):
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / (dash + gap)))
    for i in range(n + 1):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        line(d, x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b, col, lw)

def dotted(d, x0, y0, x1, y1, col, r=1.6, step=9):
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / step))
    for i in range(n + 1):
        u = i / n; ellipse(d, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, r, r, fill=col)

def sym_polyline(d, pts, col, lw, s=16):
    for a, b in zip(pts, pts[1:]): seg(d, a[0], a[1], b[0], b[1], col, lw, s)

def resample(pts, step):
    """Points every `step` px along a polyline (by arc length), with the local direction angle (radians)."""
    out = []; acc = 0.0; nxt = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        if L == 0: continue
        a = math.atan2(y1 - y0, x1 - x0)
        while nxt <= acc + L:
            u = (nxt - acc) / L; out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, a)); nxt += step
        acc += L
    return out

def slope_glyph(a):
    """'-', '/', '|' or '\\' for a direction angle (screen coords, y down)."""
    deg = (math.degrees(a) + 180) % 180
    return '-' if deg < 22.5 or deg >= 157.5 else '\\' if deg < 67.5 else '|' if deg < 112.5 else '/'

def sym_curve(d, pts, col, lw, s=12, glyph=None, size=None):
    """A curve as a chain of symbols: every `s` px along the polyline one glyph that follows the direction
    ('-' '\\' '|' '/'), or always `glyph` (e.g. '.', 'o', '+', 'x'). size = glyph cell (default s)."""
    size = size or s
    for x, y, a in resample(pts, s):
        G(d, glyph or slope_glyph(a), x - size / 2, y - size / 2, size, size, col, lw)

def big_heart(d, cx, cy, size, col=SIG, lw=None):
    """The symbol heart ( /\\/\\ over \\  / over  \\/ ) centred on (cx, cy); `size` = its width in frame px."""
    cw = size / 4 / 0.72; ch = cw * 1.6 * 0.58 / 0.72 * 0.72
    sym_heart(d, cx, cy, cw, cw * 1.6 / 1.0 * 0.62, lw or max(2.4, size * 0.07), 1.0, col)

def pix_text(d, s, x, y, px, col, lw=None, glyph='#', gap=1, inset=0.12):
    """Big blocky letters from the engine's 5x7 pixel font, each lit pixel drawn as a stroke glyph (default '#')."""
    lw = lw or max(1.6, px * 0.12)
    return pixword(s, lambda X, Y, p: G(d, glyph, X + p * inset, Y + p * inset, p * (1 - 2 * inset), p * (1 - 2 * inset), col, lw), x, y, px, gap)

def pix_blocks(d, s, x, y, px, col, gap=1, inset=0.06):
    """5x7 pixel-font letters drawn as filled squares (LED / arcade look)."""
    return pixword(s, lambda X, Y, p: rect(d, X + p * inset, Y + p * inset, X + p * (1 - inset), Y + p * (1 - inset), col), x, y, px, gap)

def pix_dots(d, s, x, y, px, col, gap=1, r=0.36):
    """5x7 pixel-font letters drawn as round dots (LED matrix / dot-matrix printer)."""
    return pixword(s, lambda X, Y, p: ellipse(d, X + p / 2, Y + p / 2, p * r, p * r, fill=col), x, y, px, gap)

# seven-segment digits
_SEG = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc', '7': 'abc',
        '8': 'abcdefg', '9': 'abcfgd', '-': 'g', ' ': '', 'E': 'afged', 'r': 'eg', 'o': 'cdeg', 'H': 'bcefg',
        'P': 'abefg', 'L': 'def', 'A': 'abcefg', 'b': 'cdefg', 'd': 'bcdeg', 'C': 'adef', 'F': 'aefg', 'S': 'afgcd'}
def seven(d, s, x, y, h, col, lw=None, dim=None, gap=0.28, slant=0.1):
    """Seven-segment text (digits, '-', some letters). h = digit height. dim: colour for the unlit segments."""
    w = h * 0.5; lw = lw or h * 0.11; cx = x
    for ch in s:
        if ch in '.:':
            ellipse(d, cx + lw, y + h - lw, lw * 0.7, lw * 0.7, fill=col) if ch == '.' else (ellipse(d, cx + lw, y + h * 0.3, lw * 0.7, lw * 0.7, fill=col), ellipse(d, cx + lw, y + h * 0.7, lw * 0.7, lw * 0.7, fill=col))
            cx += lw * 3; continue
        on = _SEG.get(ch, '')
        P = {'a': ((0, 0), (1, 0)), 'b': ((1, 0), (1, 0.5)), 'c': ((1, 0.5), (1, 1)), 'd': ((0, 1), (1, 1)),
             'e': ((0, 0.5), (0, 1)), 'f': ((0, 0), (0, 0.5)), 'g': ((0, 0.5), (1, 0.5))}
        for k, ((u0, v0), (u1, v1)) in P.items():
            c = col if k in on else dim
            if c is None: continue
            X0 = cx + u0 * w + (1 - v0) * slant * h; X1 = cx + u1 * w + (1 - v1) * slant * h
            sh = lw * 0.9
            if u0 == u1: line(d, X0, y + v0 * h + sh, X1, y + v1 * h - sh, c, lw)
            else: line(d, X0 + sh, y + v0 * h, X1 - sh, y + v1 * h, c, lw)
        cx += w * (1 + gap) + lw
    return cx - x

def cursor_arrow(d, x, y, s, fill=INK, outline=BONE, lw=2.2, ang=0.0):
    """The classic arrow pointer, tip at (x, y), about 20*s px tall; ang in radians."""
    pts = [(0, 0), (0, 17), (4, 13), (7, 20), (9.4, 19), (6.5, 12.2), (12, 12)]
    P = [(x + (u * s) * math.cos(ang) - (v * s) * math.sin(ang), y + (u * s) * math.sin(ang) + (v * s) * math.cos(ang)) for u, v in pts]
    poly(d, P, fill=fill)
    if outline:
        for i in range(len(P)):
            a0, a1 = P[i], P[(i + 1) % len(P)]; line(d, a0[0], a0[1], a1[0], a1[1], outline, lw)

def stamp(im, s, cx, cy, angle=8, col=SIG, size=56, pad=26, font=None, frame=True):
    """A rubber stamp: framed text on its own layer, rotated and pasted."""
    font = font or title(size)
    tmp = Image.new('RGB', (10, 10)); td = ImageDraw.Draw(tmp)
    tw_ = td.textlength(s, font=font) / SS; th_ = size * 1.05
    lay, ld = layer(tw_ + 2 * pad + 20, th_ + 2 * pad + 20)
    if frame: box(ld, 10, 10, tw_ + 2 * pad + 10, th_ + 2 * pad + 10, col, max(3, size * 0.09), max(14, size * 0.38))
    ld.text(((tw_ / 2 + pad + 10) * SS, (th_ / 2 + pad + 10) * SS), s, font=font, fill=col, anchor='mm')
    paste_rot(im, lay, cx, cy, angle)

def hatch_rect(d, x0, y0, x1, y1, angle, spacing, col, lw, s=12):
    hatch(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], angle, spacing, col, lw, s)

def stipple(d, x0, y0, x1, y1, density, col, r=1.4, seed=0, fn=None):
    """Random dots in a rectangle; fn(x, y) -> 0..1 modulates the density."""
    rnd = random.Random(seed); n = int((x1 - x0) * (y1 - y0) * density / 1000)
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if fn is None or rnd.random() < fn(x, y): ellipse(d, x, y, r, r, fill=col)

def text_block(d, x, y, lines, font, col, lh=1.35, anchor='la', size=None):
    """Several lines of text; `lines` may hold (string, colour) tuples. size = the font size (for line height)."""
    size = size or font.size / SS
    for i, ln in enumerate(lines):
        s, c = (ln if isinstance(ln, tuple) else (ln, col))
        text(d, x, y + i * size * lh, s, font, c, anchor)

def wrap(s, font, width):
    """Greedy word wrap to `width` frame px."""
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4))); out, cur = [], ''
    for w_ in s.split():
        t = (cur + ' ' + w_).strip()
        if tmp.textlength(t, font=font) / SS <= width: cur = t
        else: out.append(cur); cur = w_
    if cur: out.append(cur)
    return out


# ---------------------------------------------------------------- Hershey single-stroke fonts (vector-display look)
_HF = {}
def _hershey(name):
    if name not in _HF:
        src = open(os.path.join(FD, 'stroke', name + '.svg'), encoding='utf-8').read()
        dflt = float(re.search(r'<font[^>]*horiz-adv-x="([\d.]+)"', src).group(1))
        gl = {}
        for m in re.finditer(r'<glyph([^>]*)/?>', src):
            a = m.group(1); u = re.search(r'unicode="([^"]*)"', a)
            if not u: continue
            ch = u.group(1).replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
            adv = re.search(r'horiz-adv-x="([\d.]+)"', a); pd = re.search(r' d="([^"]*)"', a)
            strokes, cur = [], []
            if pd:
                for cmd, xs, ys in re.findall(r'([ML])\s*(-?[\d.]+)\s+(-?[\d.]+)', pd.group(1)):
                    if cmd == 'M' and cur: strokes.append(cur); cur = []
                    cur.append((float(xs), float(ys)))
                if cur: strokes.append(cur)
            gl[ch] = (float(adv.group(1)) if adv else dflt, strokes)
        _HF[name] = gl
    return _HF[name]

def hershey(d, s, x, y, size, col, lw=2.0, font='HersheySans1', anchor='l', spacing=1.0):
    """Single-stroke vector text (oscilloscope / plotter / radar labels). size = cap height in px. y = baseline.
    fonts: HersheySans1, HersheyScript1, EMSAllure, EMSFelix, EMSOsmotron, EMSReadability, EMSTech."""
    gl = _hershey(font); k = size / 700.0
    width = sum(gl.get(c, gl.get(' ', (400, [])))[0] for c in s) * k * spacing
    cx = x - (width if anchor == 'r' else width / 2 if anchor == 'm' else 0)
    for c in s:
        adv, strokes = gl.get(c, gl.get(' ', (400, [])))
        for st in strokes:
            pts = [((cx + px * k) * SS, (y - py * k) * SS) for px, py in st]
            if len(pts) > 1: d.line(pts, fill=col, width=max(1, int(lw * SS)), joint='curve')
            for P in (pts[0], pts[-1]):
                r = lw * SS / 2; d.ellipse([P[0] - r, P[1] - r, P[0] + r, P[1] + r], fill=col)
        cx += adv * k * spacing
    return width


# ---------------------------------------------------------------- perspective & post (post effects work on the 1x image)
def _coeffs(dst, src):
    A, B = [], []
    for (x, y), (X, Y) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y]); B.append(X)
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y]); B.append(Y)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def warp(src, quad, size, fill=(0, 0, 0, 0)):
    """Perspective-map the whole `src` image onto the quad [(tl), (tr), (br), (bl)] (pixel coords of the output
    image of `size`). Returns an RGBA image of `size`; paste it with its alpha."""
    s = src.convert('RGBA'); w, h = s.size
    c = _coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    return s.transform(size, Image.PERSPECTIVE, c, Image.BICUBIC, fillcolor=fill)

def warp_onto(im, src, quad):
    """Warp `src` onto the frame quad (frame px) and composite it into the SS canvas `im`."""
    q = [(x * SS, y * SS) for x, y in quad]
    im.alpha_composite(warp(src, q, im.size)) if im.mode == 'RGBA' else im.paste(w_ := warp(src, q, im.size), (0, 0), w_)

def depth_blur(img, radius_map, levels=(0, 1.2, 2.5, 4.5, 7.5, 12)):
    """Depth of field on a 1x image: radius_map is an HxW float array of blur radii in px (0 = sharp)."""
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    stack = [a if r == 0 else np.asarray(img.convert('RGB').filter(ImageFilter.GaussianBlur(r))).astype(np.float32) for r in levels]
    rm = np.clip(radius_map, 0, levels[-1]); out = np.zeros_like(a)
    idx = np.searchsorted(levels, rm, side='right') - 1; idx = np.clip(idx, 0, len(levels) - 2)
    lo = np.array(levels)[idx]; hi = np.array(levels)[idx + 1]; t = ((rm - lo) / (hi - lo))[..., None]
    for i in range(len(levels) - 1):
        m = (idx == i)[..., None]
        out += m * (stack[i] * (1 - t) + stack[i + 1] * t)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def dof_band(img, y_focus, half=60, max_r=10, slope=1 / 140, axis='y', x_focus=None):
    """Sharp band around y_focus (or around a point if x_focus is given), blurring with distance."""
    hh, ww = img.height, img.width
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    if x_focus is None: dist = np.abs(yy - y_focus)
    else: dist = np.hypot((xx - x_focus) * 0.6, yy - y_focus)
    return depth_blur(img, np.clip((dist - half) * slope * max_r / 1.0, 0, max_r))

def grain(img, amount=7.0, seed=1):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    n = np.random.default_rng(seed).normal(0, amount, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))

def vignette(img, strength=0.35, power=2.2):
    a = np.asarray(img.convert('RGB')).astype(np.float32); hh, ww = a.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    r = np.hypot((xx - ww / 2) / (ww / 2), (yy - hh / 2) / (hh / 2)) / math.sqrt(2)
    f = 1 - strength * np.clip(r, 0, 1) ** power
    return Image.fromarray(np.clip(a * f[..., None], 0, 255).astype(np.uint8))

def scanlines(img, step=4, alpha=60):
    o = img.convert('RGB').copy(); dd = ImageDraw.Draw(o, 'RGBA')
    for y in range(0, o.height, step): dd.line([(0, y), (o.width, y)], fill=(0, 0, 0, alpha))
    return o

def pixel_grid(img, cell=4, alpha=36):
    """Fine screen-door grid (a macro look at a display) — greys only."""
    o = img.convert('RGB').copy(); dd = ImageDraw.Draw(o, 'RGBA')
    for x in range(0, o.width, cell): dd.line([(x, 0), (x, o.height)], fill=(0, 0, 0, alpha))
    for y in range(0, o.height, cell): dd.line([(0, y), (o.width, y)], fill=(0, 0, 0, alpha))
    return o

def chain(*fns):
    """post=chain(f1, f2, ...) runs several 1x post effects in order (each takes and returns an image)."""
    def run(img):
        for f in fns: img = f(img)
        return img
    return run


# ---------------------------------------------------------------- code plates (B-roll)
KW = set('function const let var if else return class extends while true false break throw new import from def for in '
         'try except raise None null undefined self this await async static final public private void int bool'.split())

def code_plate(lines, size=34, width=1600, bg=INK, fg=BONE, kw=ASH, dim=GR, hot=SIG, hot_words=(), lnum=1,
               font='Regular', lh=1.55, pad=36, squiggle=(), gutter=True):
    """Render code to an RGB image (at SS). lines: strings, or lists of (text, colour) spans for full control.
    Plain strings get light syntax colouring: keywords `kw`, comments (// or #) `dim`, words in hot_words `hot`.
    squiggle: list of (line_index, substring) to underline with an orange wavy line. lnum: first line number
    (None = no gutter). Returns the image; its size is (width, pad*2 + n*size*lh) frame px times SS."""
    f = mono(size, font); fb = mono(size, 'SemiBold')
    n = len(lines); hh = pad * 2 + n * size * lh
    im = Image.new('RGB', (int(width * SS), int(hh * SS)), bg); d = ImageDraw.Draw(im)
    gx = pad + (size * 2.6 if lnum is not None else 0)
    cw = d.textlength('M', font=f) / SS
    for i, ln in enumerate(lines):
        y = pad + i * size * lh
        if lnum is not None: text(d, pad + size * 1.6, y, str(lnum + i), f, dim, 'ra')
        spans = ln if isinstance(ln, list) else _colour(ln, fg, kw, dim, hot, hot_words)
        x = gx
        for s, c in spans:
            text(d, x, y, s, fb if c == hot else f, c); x += len(s) * cw
        for (li, sub) in squiggle:
            if li == i:
                src = ln if isinstance(ln, str) else ''.join(s for s, _ in ln)
                k = src.find(sub)
                if k >= 0:
                    x0, x1 = gx + k * cw, gx + (k + len(sub)) * cw; yy = y + size * 1.22
                    pts = [(x0 + j * 3, yy + (2.2 if (j % 4) in (1, 2) else -0.2)) for j in range(int((x1 - x0) / 3) + 1)]
                    d.line([(px * SS, py * SS) for px, py in pts], fill=hot, width=int(2.4 * SS))
    return im

def _colour(ln, fg, kw, dim, hot, hot_words):
    out = []; ci = None
    for mark in ('//', '#'):
        k = ln.find(mark)
        if k >= 0 and (ci is None or k < ci) and (mark == '//' or k == 0 or ln[k - 1] == ' '): ci = k
    body, com = (ln[:ci], ln[ci:]) if ci is not None else (ln, '')
    for tok in re.findall(r'\w+|\s+|[^\w\s]', body):
        c = hot if tok in hot_words else kw if tok in KW else fg if re.match(r'\w', tok) else (mix(fg, dim, 0.5) if tok.strip() else fg)
        out.append((tok, c))
    if com: out.append((com, dim))
    return out


# ---------------------------------------------------------------- palette check & save
def palette_report(img):
    """Fraction of pixels with a hue that is not neutral grey or orange (the palette is black/white/greys + ONE orange)."""
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    mx, mn = a.max(2), a.min(2); ch = mx - mn
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.degrees(np.arctan2(math.sqrt(3) * (g - b), 2 * r - g - b)) % 360
    bad = (ch > 18) & ~((hue >= 4) & (hue <= 44))
    return float(bad.mean())

def save_scene(im, sid, post=None):
    """Downsample the SS canvas to 1920x1080, run post (1x effects), check the palette, write the plan's file name."""
    p = BY_ID[sid]
    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    if post: out = post(out) or out
    bad = palette_report(out)
    os.makedirs(OUT, exist_ok=True)
    fn = p['file']; out.save(os.path.join(OUT, fn))
    print(f'wrote {fn}' + (f'   !! {bad * 100:.2f}% off-palette pixels' if bad > 0.002 else ''))
    return out
