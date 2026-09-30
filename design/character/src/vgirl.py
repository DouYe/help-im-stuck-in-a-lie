"""The girl as vector strokes (groups: hair_out, hair_in, strands, face, eyes, neck, body, legs, arms, over),
rasterized into a grid of symbol glyphs: each cell a stroke picks the glyph matching its direction."""
import math
def arc(cx, cy, rx, ry, a0, a1, n=12):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def pose(name, t=0.0):
    if name in ('q_front', 'q_frontwalk'):
        return turn(1.0, t, name == 'q_frontwalk')
    """dict group -> list of polylines, coordinates in a 1 x 1.6 box (y down)"""
    S = {}
    add = lambda g, pl: S.setdefault(g, []).append(pl)
    sway = 0.02 * math.sin(t * 2 * math.pi)
    if name in ('front', 'heart', 'help', 'frontwalk'):
        # hair: outer contour from the left end, over the crown, to the right end; the ends cut a little ragged
        add('hair_out', [(0.2, 0.8), (0.18, 0.5), (0.19, 0.24)] + arc(0.5, 0.26, 0.31, 0.25, math.pi, 2 * math.pi, 16) + [(0.81, 0.5), (0.8, 0.8)])
        add('hair_out', [(0.2, 0.8), (0.24, 0.84), (0.27, 0.8), (0.31, 0.83)])
        add('hair_out', [(0.8, 0.8), (0.76, 0.84), (0.73, 0.8), (0.69, 0.83)])
        # inner edge: down the cheeks, across the fringe (the face is a window in the hair)
        add('hair_in', [(0.31, 0.83), (0.31, 0.5), (0.32, 0.28)] + arc(0.5, 0.3, 0.18, 0.1, math.pi, 2 * math.pi, 10) + [(0.68, 0.5), (0.69, 0.83)])
        add('strands', [(0.36, 0.22), (0.39, 0.28)]); add('strands', [(0.5, 0.2), (0.5, 0.26)]); add('strands', [(0.64, 0.22), (0.61, 0.28)])
        add('face', [(0.35, 0.4), (0.4, 0.46), (0.5, 0.49), (0.6, 0.46), (0.65, 0.4)])
        if name == 'help':
            add('eyes', [(0.42, 0.33)]); add('eyes', [(0.58, 0.33)])          # wide open: one 'o' each
        else:
            add('eyes', [(0.39, 0.33), (0.45, 0.33)]); add('eyes', [(0.55, 0.33), (0.61, 0.33)])
        add('neck', [(0.46, 0.49), (0.46, 0.55)]); add('neck', [(0.54, 0.49), (0.54, 0.55)])
        add('body', [(0.38, 0.8), (0.37, 0.6), (0.4, 0.56), (0.6, 0.56), (0.63, 0.6), (0.62, 0.8)])
        add('body', [(0.38, 0.8), (0.27, 1.12), (0.73, 1.12), (0.62, 0.8)])
        add('body', [(0.38, 0.8), (0.62, 0.8)])
        if name == 'heart':
            add('arms', [(0.38, 0.6), (0.34, 0.72), (0.46, 0.7)]); add('arms', [(0.62, 0.6), (0.66, 0.72), (0.54, 0.7)])
        if name == 'help':
            # arms up like \o/ , in front of the hair ('over' is rasterized on top of the other lines)
            add('over', [(0.39, 0.58), (0.2, 0.45), (0.1, 0.27)]); add('over', [(0.61, 0.58), (0.8, 0.45), (0.9, 0.27)])
        st = 0.04 * math.sin(t * 2 * math.pi) if name == 'frontwalk' else 0
        add('legs', [(0.44, 1.12), (0.44, 1.44 - st)]); add('legs', [(0.56, 1.12), (0.56, 1.44 + st)])
        add('legs', [(0.41, 1.47 - st), (0.46, 1.47 - st)]); add('legs', [(0.54, 1.47 + st), (0.59, 1.47 + st)])
        S['heart'] = (0.53, 0.68, 0.09 if name != 'heart' else 0.15)
    elif name in ('q_front', 'q_frontwalk'):
        add('hair_out', [(0.21, 0.8), (0.2, 0.5), (0.23, 0.26)] + arc(0.52, 0.26, 0.29, 0.25, math.pi, 2 * math.pi, 16) + [(0.8, 0.5), (0.78, 0.8)])
        add('hair_out', [(0.21, 0.8), (0.26, 0.84), (0.3, 0.8), (0.34, 0.84), (0.39, 0.82)])
        add('hair_out', [(0.78, 0.8), (0.76, 0.83), (0.74, 0.81)])
        add('hair_in', [(0.39, 0.82), (0.4, 0.5), (0.43, 0.3)] + arc(0.6, 0.31, 0.17, 0.1, math.pi, 2 * math.pi, 10) + [(0.76, 0.5), (0.74, 0.81)])
        add('strands', [(0.48, 0.23), (0.51, 0.29)]); add('strands', [(0.62, 0.21), (0.62, 0.27)])
        add('face', [(0.46, 0.41), (0.52, 0.47), (0.6, 0.49), (0.68, 0.46), (0.73, 0.41)])
        add('eyes', [(0.48, 0.33), (0.54, 0.33)]); add('eyes', [(0.63, 0.33), (0.67, 0.33)])
        add('neck', [(0.54, 0.49), (0.54, 0.55)]); add('neck', [(0.62, 0.49), (0.62, 0.55)])
        add('body', [(0.46, 0.8), (0.44, 0.6), (0.48, 0.56), (0.66, 0.56), (0.7, 0.6), (0.68, 0.8)])
        add('body', [(0.46, 0.8), (0.35, 1.11), (0.77, 1.13), (0.68, 0.8)])
        add('body', [(0.46, 0.8), (0.68, 0.8)])
        st = 0.05 * math.sin(t * 2 * math.pi) if name == 'q_frontwalk' else 0
        add('legs', [(0.52, 1.12), (0.51 - st * 0.6, 1.44 + st)]); add('legs', [(0.64, 1.12), (0.65 + st * 0.6, 1.45 - st)])
        add('legs', [(0.48 - st * 0.6, 1.47 + st), (0.53 - st * 0.6, 1.47 + st)]); add('legs', [(0.63 + st * 0.6, 1.48 - st), (0.69 + st * 0.6, 1.48 - st)])
        S['heart'] = (0.6, 0.68, 0.09)
    elif name == 'q_back':
        add('hair_out', [(0.22, 0.86), (0.2, 0.5), (0.22, 0.26)] + arc(0.5, 0.26, 0.28, 0.25, math.pi, 2 * math.pi, 16) + [(0.78, 0.5), (0.77, 0.86)])
        add('hair_out', [(0.22, 0.86), (0.31, 0.9), (0.4, 0.86), (0.5, 0.9), (0.6, 0.86), (0.69, 0.9), (0.77, 0.86)])
        add('face', [(0.78, 0.3), (0.82, 0.36), (0.79, 0.43)])
        add('strands', [(0.57, 0.02), (0.57, 0.19)])
        for x in (0.32, 0.44, 0.66): add('strands', [(x, 0.32), (x + (0.55 - x) * 0.1, 0.8)])
        add('body', [(0.4, 0.9), (0.31, 1.12), (0.74, 1.13), (0.64, 0.9)])
        add('legs', [(0.46, 1.12), (0.46, 1.44)]); add('legs', [(0.59, 1.13), (0.6, 1.45)])
        add('legs', [(0.43, 1.47), (0.48, 1.47)]); add('legs', [(0.57, 1.48), (0.62, 1.48)])
    elif name in ('back', 'backwalk'):
        add('hair_out', [(0.2, 0.84), (0.18, 0.5), (0.19, 0.24)] + arc(0.5, 0.26, 0.31, 0.25, math.pi, 2 * math.pi, 16) + [(0.81, 0.5), (0.8, 0.84)])
        add('hair_out', [(0.2, 0.84), (0.3, 0.88), (0.4, 0.84), (0.5, 0.88), (0.6, 0.84), (0.7, 0.88), (0.8, 0.84)])
        add('strands', [(0.5, 0.02), (0.5, 0.2)])
        for x in (0.3, 0.4, 0.6, 0.7): add('strands', [(x, 0.3), (x + (0.5 - x) * 0.1, 0.78)])
        add('body', [(0.38, 0.88), (0.27, 1.12), (0.73, 1.12), (0.62, 0.88)])
        st = 0.04 * math.sin(t * 2 * math.pi) if name == 'backwalk' else 0
        add('legs', [(0.44, 1.12), (0.44, 1.44 + st)]); add('legs', [(0.56, 1.12), (0.56, 1.44 - st)])
        add('legs', [(0.41, 1.47 + st), (0.46, 1.47 + st)]); add('legs', [(0.54, 1.47 - st), (0.59, 1.47 - st)])
    else:
        # side view facing right; walk/jump vary the legs and the hair
        run = name in ('walk', 'jump')
        lift = 0.1 if name == 'jump' else (0.3 if name == 'fall' else 0.0)
        back_x = 0.22 - (0.05 if name == 'jump' else 0) + sway
        bx = 0.21 - (0.04 if name == 'jump' else 0) - (0.05 if name == 'run' else 0) + sway
        add('hair_out', [(0.68, 0.24), (0.66, 0.12), (0.6, 0.05), (0.5, 0.02), (0.38, 0.04), (0.28, 0.12), (0.23, 0.26), (bx + 0.01, 0.5), (bx, 0.8 - lift)])
        add('hair_out', [(bx, 0.8 - lift), (bx + 0.05, 0.84 - lift), (bx + 0.1, 0.8 - lift), (0.36, 0.83 - lift)])
        if name == 'fall':
            for k, x in enumerate((0.3, 0.38, 0.46)): add('strands', [(x, 0.06), (x - 0.06 + 0.02 * k, -0.08)])
        add('hair_in', [(0.36, 0.83 - lift), (0.39, 0.6), (0.43, 0.44), (0.46, 0.3), (0.52, 0.25), (0.68, 0.24)])
        add('strands', [(0.56, 0.12), (0.54, 0.2)]); add('strands', [(0.44, 0.1), (0.4, 0.2)])
        add('face', [(0.68, 0.24), (0.69, 0.29), (0.73, 0.34), (0.69, 0.36), (0.7, 0.4), (0.67, 0.45), (0.58, 0.47), (0.5, 0.46)])
        add('eyes', [(0.59, 0.31), (0.64, 0.31)])
        add('neck', [(0.52, 0.47), (0.52, 0.55)]); add('neck', [(0.6, 0.47), (0.6, 0.55)])
        add('body', [(0.48, 0.8), (0.47, 0.6), (0.5, 0.56), (0.62, 0.56), (0.65, 0.6), (0.64, 0.8)])
        add('body', [(0.48, 0.8), (0.4, 1.1), (0.75, 1.1), (0.64, 0.8)])
        add('body', [(0.48, 0.8), (0.64, 0.8)])
        if name == 'fall':
            add('arms', [(0.52, 0.58), (0.4, 0.44), (0.36, 0.3)]); add('arms', [(0.62, 0.58), (0.74, 0.44), (0.8, 0.32)])
        elif name == 'stuck':
            add('arms', [(0.62, 0.6), (0.74, 0.62), (0.82, 0.58)])
        elif name == 'run':
            add('arms', [(0.6, 0.6), (0.7, 0.7), (0.78, 0.64)])
        else:
            add('arms', [(0.6, 0.6), (0.62, 0.74), (0.66, 0.82)])
        if name in ('walk', 'run'):
            a = (0.55 if name == 'run' else 0.32) * math.sin(t * 2 * math.pi)
            for s in (1, -1):
                hip = (0.57, 1.1); L = 0.36
                foot = (hip[0] + L * math.sin(s * a), hip[1] + L * math.cos(s * a))
                add('legs', [hip, foot]); add('legs', [foot, (foot[0] + 0.06, foot[1])])
        elif name == 'jump':
            add('legs', [(0.53, 1.1), (0.45, 1.3), (0.4, 1.31)]); add('legs', [(0.62, 1.1), (0.56, 1.28), (0.51, 1.29)])
        else:
            add('legs', [(0.53, 1.1), (0.53, 1.44)]); add('legs', [(0.62, 1.1), (0.62, 1.44)])
            add('legs', [(0.53, 1.47), (0.58, 1.47)]); add('legs', [(0.62, 1.47), (0.67, 1.47)])
        S['heart'] = (0.58, 0.68, 0.09)
    return S

def raster(polys, cols, rows, W=1.0, H=1.6, step=0.18):
    """polylines -> {(r, c): (glyph, meanx, meany)} ; glyph by dominant direction"""
    cw, ch = W / cols, H / rows
    acc = {}
    for pl in polys:
        for (x0, y0), (x1, y1) in zip(pl[:-1], pl[1:]):
            L = math.hypot((x1 - x0) / cw, (y1 - y0) / ch)
            n = max(1, int(L / step))
            ang = math.atan2((y1 - y0) / ch, (x1 - x0) / cw)
            for i in range(n + 1):
                u = i / n; x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u
                c, r = int(x / cw), int(y / ch)
                fx, fy = x / cw - c, y / ch - r
                a = acc.setdefault((r, c), [0.0, 0.0, 0.0, 0.0, 0])
                a[0] += math.cos(2 * ang); a[1] += math.sin(2 * ang); a[2] += fx; a[3] += fy; a[4] += 1
    out = {}
    for (r, c), (ca, sa, sx, sy, n) in acc.items():
        coh = math.hypot(ca, sa) / n
        th = math.degrees(math.atan2(sa, ca) / 2) % 180   # 0 = horizontal, 90 = vertical (y down)
        fy = sy / n
        if coh < 0.12: g = '+'
        elif th < 22 or th > 158: g = '_' if fy > 0.72 else ('`' if fy < 0.28 else '-')
        elif 68 < th < 112: g = '|'
        elif th < 90: g = '\\'
        else: g = '/'
        out[(r, c)] = g
    return out


def chibi(S, k=1.2, body=0.8):
    """bigger head, shorter body: scale the head about the neck, compress below it"""
    nx, ny = 0.5, 0.5
    def f(p):
        x, y = p
        if y <= ny: return (nx + (x - nx) * k, ny + (y - ny) * k + 0.0)
        return (nx + (x - nx) * 1.0, ny + (y - ny) * body)
    out = {}
    for g, v in S.items():
        if g == 'heart': hx, hy, hs = v; out[g] = (hx, ny + (hy - ny) * body, hs); continue
        out[g] = [[f(p) for p in pl] for pl in v]
    # shift down so the feet stay on the ground line
    lift = 1.48 - (ny + (1.48 - ny) * body)
    for g, v in out.items():
        if g == 'heart': hx, hy, hs = v; out[g] = (hx, hy + lift, hs); continue
        out[g] = [[(x, y + lift) for x, y in pl] for pl in v]
    return out


def above(S):
    """seen from ~45 degrees above: the body shortens under the head, the crown shows"""
    ny = 0.5
    out = {}
    for g, v in S.items():
        if g == 'heart': hx, hy, hs = v; out[g] = (hx, ny + (hy - ny) * 0.62, hs); continue
        out[g] = [[(x, y if y <= ny else ny + (y - ny) * 0.66) for x, y in pl] for pl in v]
    out.setdefault('strands', []).append([(0.5, 0.0), (0.5, 0.12)])
    lift = 1.48 - (ny + (1.48 - ny) * 0.62)
    for g, v in out.items():
        if g == 'heart': hx, hy, hs = v; out[g] = (hx, hy + lift, hs); continue
        out[g] = [[(x, y + lift) for x, y in pl] for pl in v]
    return out


def turn(f, t=0.0, walk=False):
    """front (f=0) to three-quarter (f=1, about 45 degrees to her left) as one continuous rig"""
    L = lambda a, b: a + (b - a) * f
    P = lambda pa, pb: [(L(a[0], b[0]), L(a[1], b[1])) for a, b in zip(pa, pb)]
    S = {}
    add = lambda g, pl: S.setdefault(g, []).append(pl)
    cx, rx = L(0.5, 0.53), L(0.31, 0.29)
    lo, ro = L(0.2, 0.21), L(0.81, 0.79)
    add('hair_out', [(lo, 0.8), (lo - 0.01, 0.5), (cx - rx, 0.26)] + arc(cx, 0.26, rx, 0.25, math.pi, 2 * math.pi, 16) + [(ro, 0.5), (ro - 0.01, 0.8)])
    li, ri = L(0.31, 0.385), L(0.69, 0.765)
    add('hair_out', [(lo, 0.8), (lo + 0.04, 0.84), (lo + 0.07, 0.8), (li, 0.83)])
    add('hair_out', [(ro - 0.01, 0.8), (ro - 0.04, 0.84), (L(ro - 0.07, ro - 0.03), 0.81), (ri, 0.83)])
    fc, frx = (li + ri) / 2, (ri - li) / 2
    add('hair_in', [(li, 0.83), (li, 0.5), (li + 0.01, 0.3)] + arc(fc, 0.3, frx - 0.01, 0.08, math.pi, 2 * math.pi, 10) + [(ri - 0.01, 0.5), (ri, 0.83)])
    ne, fe, ew1, ew2 = L(0.42, 0.515), L(0.58, 0.665), L(0.03, 0.035), L(0.03, 0.024)
    S['eyes'] = [[(ne - ew1, 0.335), (ne + ew1, 0.335)], [(fe - ew2, 0.335), (fe + ew2, 0.335)]]
    if f > 0.3:
        k = (f - 0.3) / 0.7
        add('nose', [(L(0.6, 0.715), 0.35), (L(0.6, 0.715) + 0.022 * k, 0.385), (L(0.6, 0.715), 0.4)])
    add('face', P([(0.35, 0.4), (0.4, 0.46), (0.5, 0.49), (0.6, 0.46), (0.65, 0.4)], [(0.43, 0.41), (0.49, 0.47), (0.58, 0.49), (0.67, 0.46), (0.72, 0.41)]))
    n1, n2 = L(0.46, 0.53), L(0.54, 0.61)
    add('neck', [(n1, 0.49), (n1, 0.55)]); add('neck', [(n2, 0.49), (n2, 0.55)])
    add('body', P([(0.38, 0.8), (0.37, 0.6), (0.4, 0.56), (0.6, 0.56), (0.63, 0.6), (0.62, 0.8)], [(0.45, 0.8), (0.43, 0.6), (0.47, 0.56), (0.66, 0.56), (0.7, 0.6), (0.68, 0.8)]))
    add('body', P([(0.38, 0.8), (0.27, 1.12), (0.73, 1.12), (0.62, 0.8)], [(0.45, 0.8), (0.34, 1.11), (0.77, 1.13), (0.68, 0.8)]))
    add('body', P([(0.38, 0.8), (0.62, 0.8)], [(0.45, 0.8), (0.68, 0.8)]))
    st = 0.05 * math.sin(t * 2 * math.pi) if walk else 0
    l1, l2 = L(0.44, 0.51), L(0.56, 0.64)
    add('legs', [(l1, 1.12), (l1 - st * 0.6, 1.44 + st)]); add('legs', [(l2, 1.12), (l2 + st * 0.6, 1.45 - st)])
    add('legs', [(l1 - 0.03 - st * 0.6, 1.47 + st), (l1 + 0.02 - st * 0.6, 1.47 + st)]); add('legs', [(l2 - 0.01 + st * 0.6, 1.48 - st), (l2 + 0.05 + st * 0.6, 1.48 - st)])
    S['heart'] = (L(0.53, 0.6), 0.68, 0.09)
    return S
