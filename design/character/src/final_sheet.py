"""THE GIRL, style 1 (final): turnaround with the Q1 45-degree view, walks, platformer actions, from above."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glyphs import G
from PIL import Image, ImageDraw
from vgirl import pose, raster, above
from PIL import ImageFont
import os
SS = 3
INK = (10, 10, 11); BONE = (238, 233, 223); SIG = (255, 83, 20); GR = (94, 91, 87); ASH = (156, 151, 143)
FD = os.environ.get('FONTS', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'public', 'fonts')) + '/'
def font(name, size): return ImageFont.truetype(FD + name, size)
COLS, ROWS = 17, 27
HEART = ['/\\/\\', '\\  /', ' \\/ ']
def glyph(d, g, x, y, cw, ch, col, lw):
    w = max(1, int(lw * SS))
    for poly in G[g]:
        pts = [((x + u * cw) * SS, (y + v * ch) * SS) for u, v in poly]
        if len(pts) == 2 and abs(pts[0][0] - pts[1][0]) < 1 and abs(pts[0][1] - pts[1][1]) < 1:
            X, Y = pts[0]; r = w * 0.8; d.ellipse([X - r, Y - r, X + r, Y + r], fill=col); continue
        d.line(pts, fill=col, width=w, joint='curve')
        for X, Y in (pts[0], pts[-1]): r = w / 2; d.ellipse([X - r, Y - r, X + r, Y + r], fill=col)
LW, MIN_PX = 0.32, 2.4        # BOLD since 2026-09-29 (Hon: the girl was too hard to see) — same as app/src/game/girl.ts
def sym_heart(d, cx, cy, cw, ch, lw, big=1.0, col=SIG):
    hw, hh = cw * 0.72 * big, ch * 0.58 * big
    lw = max(1.6, min(lw, hw * 0.42))
    x0, y0 = cx - 2 * hw, cy - 1.5 * hh
    for r, row in enumerate(HEART):
        for c, g in enumerate(row):
            if g != ' ': glyph(d, g, x0 + c * hw, y0 + r * hh, hw, hh, col, lw)
def render(d, name, ox, oy, sw, t=0.0, flip=False, view=None, big=1.0, wall=False, knock=INK, col=BONE, hot=SIG, sub=None, lw=None):
    """Draw the girl. knock: background colour for the knockout (None = no knockout); col / hot: line and heart
    colours; sub(glyph) -> glyph or None: restyle her body symbols (not the eyes/nose), e.g. 'x' for cross-stitch;
    lw: stroke as a fraction of the cell height (default LW)."""
    S = pose(name, t)
    if view == 'above': S = above(S)
    sh = sw * 1.6; cw, ch = sw / COLS, sh / ROWS; lw = max(MIN_PX, (LW if lw is None else lw) * ch)
    F = (lambda pl: [(1 - x, y) for x, y in pl]) if flip else (lambda pl: pl)
    cells = raster([F(pl) for g, v in S.items() if g not in ('heart', 'eyes', 'nose', 'over') for pl in v], COLS, ROWS)
    cells.update(raster([F(pl) for pl in S.get('over', [])], COLS, ROWS))    # 'over': in front of everything else
    cwu, chu = 1.0 / COLS, 1.6 / ROWS
    one = lambda x, y: (int(y / chu), int(x / cwu))
    top = {}
    for pl in S.get('eyes', []):
        pl = F(pl)
        if len(pl) == 1:                                            # an open eye: one 'o'
            top[one(*pl[0])] = 'o'
        elif len(pl) == 2 and abs(pl[0][1] - pl[1][1]) < 1e-6:     # a dash eye: one symbol, on top of everything
            top[one((pl[0][0] + pl[1][0]) / 2, pl[0][1])] = '-'
        else:
            for k, g in raster([pl], COLS, ROWS).items(): top[k] = 'o'
    for pl in S.get('nose', []):
        pl = F(pl); top[one(*pl[1])] = '<' if flip else '>'
    for k in top: cells.pop(k, None)
    if knock:                                 # knockout: her silhouette in the background colour, row by row
        rows = {}
        for (r, c) in list(cells) + list(top): lo, hi = rows.get(r, (c, c)); rows[r] = (min(lo, c), max(hi, c))
        px = max(lw * 0.9, cw * 0.45)
        for r, (c0, c1) in rows.items():
            d.rectangle([(ox + c0 * cw - px) * SS, (oy + r * ch - px * 0.6) * SS, (ox + (c1 + 1) * cw + px) * SS, (oy + (r + 1) * ch + px * 0.6) * SS], fill=knock)
    for (r, c), g in cells.items():
        g = sub(g) if sub else g
        if g: glyph(d, g, ox + c * cw, oy + r * ch, cw, ch, col, lw)
    for (r, c), g in top.items(): glyph(d, g, ox + c * cw, oy + r * ch, cw, ch, col, lw)
    if 'heart' in S:
        hx, hy, hs = S['heart']
        if flip: hx = 1 - hx
        sym_heart(d, ox + hx * sw, oy + hy * sh / 1.6, cw, ch, lw * 0.95, big * (1.35 if name == 'heart' else 1.0), hot)
    if wall:
        x = ox + (0.86 if not flip else 0.14) * sw
        for k in range(int(sh / ch)): glyph(d, '|', x - cw / 2, oy + k * ch, cw, ch, BONE, lw * 1.4)
if __name__ == '__main__':
    Wd, Hd = 2800, 2130
    im = Image.new('RGB', (Wd * SS, Hd * SS), INK); d = ImageDraw.Draw(im)
    fT = font('Archivo-w1250-900.ttf', 44 * SS); fH = font('src/IBMPlexMono-Bold.ttf', 24 * SS); fL = font('src/IBMPlexMono-Regular.ttf', 15 * SS); fS = font('src/IBMPlexMono-Regular.ttf', 13 * SS)
    def text(x, y, s, f, col=BONE): d.text((x * SS, y * SS), s, font=f, fill=col)
    def section(y, title, sub):
        d.line([(60 * SS, y * SS), ((Wd - 60) * SS, y * SS)], fill=GR, width=SS)
        text(60, y + 14, title, fH); text(60, y + 48, sub, fL, ASH)
    text(60, 40, 'THE GIRL  ·  STYLE 1  ·  BOLD', fT)
    text(62, 100, 'one clean BOLD line of symbols on a 17 x 27 grid (stroke 0.32 x cell, never under 2.4 px) with a knockout behind her.  eyes on top.  the heart is symbols:  / \\ / \\  over  \\ /  (the only orange)', fL, ASH)
    section(160, '1  TURNAROUND  ·  8 DIRECTIONS', 'front, 45 (Q1), side, 45 back, back, and the other side')
    dirs = [('front', False, 'front'), ('q_front', False, '45 front R'), ('side', False, 'side R'), ('q_back', False, '45 back R'), ('back', False, 'back'),
            ('q_back', True, '45 back L'), ('side', True, 'side L'), ('q_front', True, '45 front L')]
    x = 60
    for nm, fl, lab in dirs:
        render(d, nm, x, 250, 200, 0, fl); text(x + 30, 250 + 320 + 18, lab, fS, ASH); x += 330
    section(640, '2  WALKING  ·  4 DIRECTIONS  (the maze)', 'two steps each: toward you, away, to each side, and at 45 degrees')
    x = 60
    for nm, fl, lab, tts in [('frontwalk', False, 'toward', (0.25, 0.75)), ('backwalk', False, 'away', (0.25, 0.75)), ('walk', False, 'right', (0.25, 0.75)), ('walk', True, 'left', (0.25, 0.75)), ('q_frontwalk', False, '45 walk', (0.25, 0.75))]:
        for tt in tts:
            render(d, nm, x, 730, 170, tt, fl); x += 215
        text(x - 400, 730 + 272 + 18, lab, fS, ASH); x += 40
    section(1100, '3  PLATFORMER  (side)', 'walk cycle, jump, fall, stuck against a wall, HELP, holding the heart')
    x = 60
    for nm, tt, lab in [('walk', 0.0, 'walk 1'), ('walk', 0.25, 'walk 2'), ('walk', 0.5, 'walk 3'), ('walk', 0.75, 'walk 4'), ('jump', 0, 'jump'), ('fall', 0, 'fall'), ('stuck', 0, 'stuck'), ('help', 0, 'HELP'), ('heart', 0, 'heart')]:
        render(d, nm, x, 1190, 190, tt, wall=(nm == 'stuck')); text(x + 30, 1190 + 304 + 18, lab, fS, ASH); x += 290
    section(1600, '4  FROM ABOVE  ·  45 DEGREES DOWN  (the 3D maze)', 'the camera looks down on her: the body shortens under the head')
    x = 60
    for nm, fl, lab in [('front', False, 'above · front'), ('q_front', False, 'above · 45'), ('side', False, 'above · side'), ('back', False, 'above · back')]:
        render(d, nm, x, 1690, 200, 0, fl, view='above'); text(x + 30, 1690 + 320 + 18, lab, fS, ASH); x += 300
    gx = 1400; gy = 2020
    text(gx, 1690, 'real size in the game', fS, ASH)
    for k in range(0, 1300, 12): d.line([((gx + k) * SS, gy * SS), ((gx + k + 7) * SS, gy * SS)], fill=GR, width=2 * SS)
    for j, (sw, nm, tt, fl) in enumerate([(60, 'walk', 0.25, False), (80, 'front', 0, False), (100, 'jump', 0, False), (130, 'q_front', 0, False), (160, 'walk', 0.25, True)]):
        render(d, nm, gx + 40 + j * 240, gy - sw * 1.6 * 0.94 - (60 if nm == 'jump' else 0), sw, tt, fl)
    text(gx, gy + 14, '60 · 80 · 100 · 130 · 160 px wide  (in a 1920 x 1080 frame)', fS, ASH)
    out = im.resize((Wd, Hd), Image.LANCZOS)
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'GIRL_style1_final.png')); print(out.size)
