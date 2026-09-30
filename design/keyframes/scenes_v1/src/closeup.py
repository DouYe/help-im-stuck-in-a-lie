"""Close-ups of the girl (Hon 2026-09-30: "包括这种特写镜头也可以来点" + reference image
design/references/2026-09-30_hon_closeup-reference.png).

The SAME rig (vgirl.pose) rasterised on a finer symbol grid (k times 17 x 27), so at close-up size her lines are
chains of small symbols; the hair mass is filled with strands that follow the hair contour; the eyes / nose come
from the rig; the heart is the same three-row symbol heart, each of its strokes hatched with small '/'.
Plus `streams()` — the horizontal symbol data streams behind her.
"""
from kit import *
from vgirl import raster as vraster


def _resample_n(pl, n):
    pts = resample(pl, 1e-9 + sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pl, pl[1:])) / (n - 1))
    pts = [(x, y) for x, y, _ in pts]
    while len(pts) < n: pts.append(pl[-1])
    return pts[:n]


def hair_strands(S, n=10, m=90):
    """Polylines between the outer hair contour and the inner edge (face window / back of the neck)."""
    out = S.get('hair_out', []); inn = S.get('hair_in', [])
    if not out: return []
    outer = out[0]
    if inn:
        inner = inn[0]
        if math.hypot(outer[0][0] - inner[0][0], outer[0][1] - inner[0][1]) > math.hypot(outer[0][0] - inner[-1][0], outer[0][1] - inner[-1][1]):
            inner = inner[::-1]
        ia = min(range(len(inner)), key=lambda i: inner[i][1]); oa = min(range(len(outer)), key=lambda i: outer[i][1])
        if 0 < ia < len(inner) - 1 and 0 < oa < len(outer) - 1:
            # a face window (front / 3/4): split at the top so strands fall from the parting down each side
            halves = [(outer[:oa + 1][::-1], inner[:ia + 1][::-1]), (outer[oa:], inner[ia:])]
        else:
            halves = [(outer, inner)]
        res = []
        fan = len(halves) == 2
        for o_, i_ in halves:
            A, B = _resample_n(o_, m), _resample_n(i_, m)
            for s in [(i + 0.5) / n for i in range(n)]:
                pl = []
                for j, (a, b) in enumerate(zip(A, B)):
                    # with a parting: every strand starts at the parting and fans out over the first ~third
                    w = min(1.0, (j / (m - 1)) / 0.32) ** 0.8 if fan else 1.0
                    pl.append((a[0] + (b[0] - a[0]) * s * w, a[1] + (b[1] - a[1]) * s * w))
                res.append(pl)
        return res
    # back view: vertical strands from the crown to the hem of the hair
    xs = [p[0] for p in outer]; x0, x1 = min(xs), max(xs); res = []
    for i in range(n * 2):
        u = (i + 0.5) / (n * 2); x = x0 + (x1 - x0) * u
        top = min((p[1] for p in _resample_n(outer, 200) if abs(p[0] - x) < 0.02), default=0.1)
        res.append([(x + (0.5 - x) * 0.12, top + 0.02), (x, 0.5), (x - (0.5 - x) * 0.02, 0.84)])
    return res


def fringe_strands(S, n=16):
    """Strands from the parting down to the fringe edge (front / 3/4 views): they fill the top of the head."""
    inn = S.get('hair_in', []); out = S.get('hair_out', [])
    if not inn or not out: return []
    inner, outer = inn[0], out[0]
    ia = min(range(len(inner)), key=lambda i: inner[i][1]); oa = min(range(len(outer)), key=lambda i: outer[i][1])
    if not (0 < ia < len(inner) - 1): return []
    P = (outer[oa][0], outer[oa][1] + 0.03)
    arc = [p for p in inner if p[1] < inner[ia][1] + 0.1]
    if len(arc) < 3: return []
    pts = _resample_n(arc, n + 2)[1:-1]
    res = []
    for Q in pts:
        side = 1 if Q[0] > P[0] else -1
        C = ((P[0] + Q[0]) / 2 + side * 0.035, (P[1] + Q[1]) / 2 - 0.01)
        res.append([((1 - u) ** 2 * P[0] + 2 * (1 - u) * u * C[0] + u * u * Q[0], (1 - u) ** 2 * P[1] + 2 * (1 - u) * u * C[1] + u * u * (Q[1] - 0.006)) for u in [i / 10 for i in range(11)]])
    return res


def closeup(d, name, ox, oy, sw, k=5, t=0.0, flip=False, col=BONE, hair=ASH, hot=SIG, knock=INK, lw=None,
            n_strands=9, n_fringe=16, heart=True, heart_scale=1.0, eye_o=2.4, S=None, face_soft=True, chin=0.14):
    """Draw her at close-up scale: rig box at (ox, oy), width sw (so she is 1.6*sw tall; crop with the frame).
    Returns info: {'cell': (cw, ch), 'rows': {frame_y: (x0, x1)}, 'heart': (x, y), 'S': polylines}."""
    S = S or girl_pose(name, t)
    F = (lambda pl: [(1 - x, y) for x, y in pl]) if flip else (lambda pl: pl)
    cols, rows = 17 * k, 27 * k
    cw, ch = sw / cols, sw * 1.6 / rows
    lw = lw or max(2.0, 0.17 * ch)
    main = [F(pl) for g, v in S.items() if g not in ('heart', 'eyes', 'nose', 'over', 'face') for pl in v]
    cells = vraster(main, cols, rows)
    # the chin line: at close-up size a full-strength chin reads as a grin, so it is trimmed and drawn softer
    def _trim(pl, f=0.14):
        pts = _resample_n(pl, 40); n = len(pts); return pts[int(n * f): n - int(n * f)]
    fcells = {kk: g for kk, g in vraster([_trim(F(pl), chin) for pl in S.get('face', [])], cols, rows).items() if kk not in cells} if (face_soft and chin < 0.5) else {}
    if not face_soft and chin < 0.5: cells.update(vraster([F(pl) for pl in S.get('face', [])], cols, rows))
    cells.update(vraster([F(pl) for pl in S.get('over', [])], cols, rows))
    strands = [F(pl) for pl in hair_strands(S, n_strands) + fringe_strands(S, n_fringe)]
    scells = {kk: g for kk, g in vraster(strands, cols, rows).items() if kk not in cells}
    top = {}
    for pl in S.get('eyes', []):
        pl = F(pl)
        if len(pl) == 1: top[('o',) + tuple(pl[0])] = 'o'
        else:
            for kk, g in vraster([pl], cols, rows).items(): top[kk] = '-'
    nose = vraster([F(pl) for pl in S.get('nose', [])], cols, rows)
    for kk in list(top) + list(nose): cells.pop(kk, None); scells.pop(kk, None)
    info = {'cell': (cw, ch), 'rows': {}, 'S': S}
    if knock:
        rw = {}
        for (r, c) in list(cells) + list(scells) + list(fcells):
            lo, hi = rw.get(r, (c, c)); rw[r] = (min(lo, c), max(hi, c))
        px = max(lw, cw * 0.5)
        for r, (c0, c1) in rw.items():
            y0 = oy + r * ch; d.rectangle([(ox + c0 * cw - px) * SS, (y0 - px * 0.4) * SS, (ox + (c1 + 1) * cw + px) * SS, (y0 + ch + px * 0.4) * SS], fill=knock)
            info['rows'][y0] = (ox + c0 * cw, ox + (c1 + 1) * cw)
    for (r, c), g in scells.items(): G(d, g, ox + c * cw, oy + r * ch, cw, ch, hair, lw * 0.8)
    for (r, c), g in fcells.items(): G(d, g, ox + c * cw, oy + r * ch, cw, ch, hair, lw * 0.85)
    for (r, c), g in cells.items(): G(d, g, ox + c * cw, oy + r * ch, cw, ch, col, lw)
    for (r, c), g in nose.items(): G(d, g, ox + c * cw, oy + r * ch, cw, ch, col, lw)
    for kk, g in top.items():
        if kk[0] == 'o':
            x, y = ox + kk[1] * sw, oy + kk[2] * sw; s = cw * eye_o
            G(d, 'o', x - s / 2, y - s / 2, s, s, col, lw * 1.1)
        else:
            r, c = kk; G(d, g, ox + c * cw, oy + r * ch, cw, ch, col, lw * 1.25)
    if heart and 'heart' in S:
        hx, hy, _ = S['heart']
        if flip: hx = 1 - hx
        big = heart_scale * (1.35 if name == 'heart' else 1.0)
        hcx, hcy = ox + hx * sw, oy + hy * sw
        heart_hatched(d, hcx, hcy, sw / 17 * 0.72 * big, sw * 1.6 / 27 * 0.58 * big, hot, fine=cw * 0.62, lw=max(1.8, lw * 0.85))
        info['heart'] = (hcx, hcy)
    return info


def heart_hatched(d, cx, cy, hw, hh, col, fine=10, lw=2.2, width=None):
    """The symbol heart ( /\\/\\ · \\  / · \\/ ) centred on (cx, cy), cell hw x hh; each stroke is a band of small '/'
    symbols (the texture of Hon's reference) with '+' at the stroke ends."""
    width = width or hw * 0.34
    x0, y0 = cx - 2 * hw, cy - 1.5 * hh
    for r, row in enumerate(HEART):
        for c, g in enumerate(row):
            if g == ' ': continue
            for pl in fs_glyphs[g]:
                pts = [(x0 + (c + u) * hw, y0 + (r + v) * hh) for u, v in pl]
                (ax, ay), (bx, by) = pts[0], pts[-1]
                L = math.hypot(bx - ax, by - ay) or 1; nx, ny = -(by - ay) / L, (bx - ax) / L
                for j in range(2):
                    o = (j - 0.5) * width * 0.7
                    sym_curve(d, [(ax + nx * o, ay + ny * o), (bx + nx * o, by + ny * o)], col, lw, fine, glyph='/')
                for (px, py) in (pts[0], pts[-1]): G(d, '+', px - fine / 2, py - fine / 2, fine, fine, col, lw)


def streams(d, x0, x1, y0, y1, gap=30, seed=1, size=13, lw=2.0, cols=None, density=0.8, arrows=0.25, cursors=0.1,
            bright=None):
    """Horizontal data streams of symbols between y0 and y1 (one every `gap` px): runs of '-', '.', ':', '=',
    arrow runs '>>>>' / '<<<<', block cursors. cols: palette to pick from (default greys + some bone)."""
    rnd = random.Random(seed); cols = cols or [GR, GR, ASH, mix(GR, INK, 0.4)]
    y = y0
    while y < y1:
        if rnd.random() < density:
            x = x0 + rnd.uniform(-200, 300)
            end = x1 - rnd.uniform(-200, 400)
            c = rnd.choice(cols) if not (bright and rnd.random() < 0.12) else bright
            while x < end:
                kind = rnd.random()
                n = rnd.randint(4, 22)
                if kind < arrows:
                    g = rnd.choice(['>', '<']); step = size * 0.62
                    for i in range(rnd.randint(3, 7)): G(d, g, x + i * step, y - size / 2, size * 0.7, size, c, lw)
                    x += step * 8
                elif kind < arrows + cursors:
                    rect(d, x, y - size * 0.62, x + size * 0.62, y + size * 0.62, rnd.choice([ASH, BONE])); x += size * 1.4
                else:
                    g = rnd.choice(['-', '-', '-', '.', '.', ':', '=', '-'])
                    for i in range(n): G(d, g, x + i * size * 0.8, y - size / 2, size * 0.72, size, c, lw)
                    x += n * size * 0.8
                x += rnd.choice([0, 0, size, size * 3, size * 8])
        y += gap * rnd.uniform(0.75, 1.25)
