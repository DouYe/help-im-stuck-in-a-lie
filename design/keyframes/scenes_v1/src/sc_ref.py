"""Reference frames for the scene kit: B01 (a B-roll code close-up) and A10 (a scene with her).
Every scene is a function named after its plan id in lower case (a10, b01 …) that ends with save_scene()."""
from kit import *


# ------------------------------------------------------------------------------------------------ B01
def b01():
    """BIOS boot screen, macro: tilted CRT text with shallow depth of field."""
    rows = [
        [('GIRL.EXE BIOS v1.0', BONE), ('      (C) 2026 NOBODY', GR)],
        [('', BONE)],
        [('CPU ............ ', ASH), ('SYMBOL ENGINE @ 99 BPM', BONE)],
        [('MEMORY TEST .... ', ASH), ('640K OK', BONE)],
        [('VOICE .......... ', ASH), ('OK', BONE)],
        [('NAME ........... ', ASH), ('AI', BONE)],
        [('HEART .......... ', SIG), ('1 FOUND', SIG)],
        [('TRUTH .......... ', ASH), ('NOT FOUND', BONE)],
        [('', BONE)],
        [('PRESS ANY KEY', BONE)],
    ]
    pw, size, lh = 1500, 58, 1.5
    plate = code_plate(rows, size=size, width=pw, lnum=None, font='Medium', lh=lh, pad=60)
    pd = ImageDraw.Draw(plate)
    # the cursor block after PRESS ANY KEY
    cw = pd.textlength('M', font=mono(size, 'Medium')) / SS
    x0 = 60 + len('PRESS ANY KEY') * cw + cw * 0.3; y0 = 60 + 9 * size * lh
    pd.rectangle([x0 * SS, (y0 + size * 0.1) * SS, (x0 + cw) * SS, (y0 + size * 1.25) * SS], fill=BONE)
    # scanlines on the glass (they follow the perspective)
    for y in range(0, plate.height, int(4.2 * SS)): pd.line([(0, y), (plate.width, y)], fill=(0, 0, 0), width=int(1.3 * SS))
    im, d = canvas(INK)
    # right side nearer the lens: that edge is taller; everything fans out to the right
    warp_onto(im, plate, [(40, 250), (2150, -330), (2150, 1480), (40, 900)])
    # the curved bezel edge of the tube, bottom-left, out of focus later
    for k in range(6):
        seg(d, -40, 1020 - k * 9, 700 - k * 40, 1110, mix(INK, GR, 0.5 - k * 0.07), 2.2, 16)
    focus_y = 250 + (900 - 250) * ((60 + 6 * size * lh + size * 0.6) / plate.height * SS)   # the HEART row, left edge
    def post(img):
        a = np.zeros((H, W), np.float32)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        # the HEART row goes from (≈120, focus_y) up to the right; blur by distance from that line + far left
        slope = (0.5 * (-330 + 1480) - 0.5 * (250 + 900)) / 2110.0
        yl = focus_y + (xx - 40) * (slope + 0.02)
        a = np.clip((np.abs(yy - yl) - 30) / 30.0, 0, 11) + np.clip((650 - xx) / 90.0, 0, 6)
        img = depth_blur(img, a)
        return vignette(grain(img, 6), 0.45)
    save_scene(im, 'B01', post)


# ------------------------------------------------------------------------------------------------ A10
def a10():
    """Polygraph: four pens on moving chart paper; TRUTH spikes where 'that sounds real' is written."""
    im, d = canvas(INK)
    PX0, PX1, PY0, PY1 = 560, 1920, 120, 960          # the paper
    rect(d, PX0, PY0, PX1, PY1, BONE)
    for x in range(PX0, PX1, 12): line(d, x, PY0, x, PY1, mix(BONE, GR, 0.26 if (x - PX0) % 60 == 0 else 0.1), 1 if (x - PX0) % 60 else 1.4)
    for y in range(PY0, PY1, 12): line(d, PX0, y, PX1, y, mix(BONE, GR, 0.1), 1)
    # four channels
    names = ['PNEUMO', 'GSR', 'CARDIO', 'TRUTH']
    ch_h = (PY1 - PY0 - 60) / 4
    penx = 1540
    for i, nm in enumerate(names):
        cy = PY0 + 60 + ch_h * (i + 0.5)
        seg(d, PX0, PY0 + 60 + ch_h * i, PX1, PY0 + 60 + ch_h * i, mix(BONE, GR, 0.45), 1.6, 14)
        text(d, PX0 + 16, PY0 + 60 + ch_h * i + 10, nm, mono(18), GR)
        pts = []
        for k in range(0, penx - PX0 - 90):
            x = PX0 + 90 + k; t = k / 60.0
            if nm == 'PNEUMO': y = 34 * math.sin(t * 1.3) + 8 * math.sin(t * 3.1)
            elif nm == 'GSR': y = 26 * math.sin(t * 0.35) - 10 * math.sin(t * 0.9)
            elif nm == 'CARDIO':
                ph = (t * 1.6) % 1.0; y = -60 * math.exp(-((ph - 0.3) / 0.03) ** 2) + 22 * math.exp(-((ph - 0.36) / 0.03) ** 2) + 6 * math.sin(t * 5)
            else:
                calm = 8 * math.sin(t * 1.1) + 4 * math.sin(t * 2.7)
                wild = 0 if x < 1250 else min(1, (x - 1250) / 60) * (70 * math.sin(t * 9.5) * math.sin(t * 2.3 + 1) + 40 * math.sin(t * 23))
                y = calm + wild
            pts.append((x, cy + y))
        hot = nm == 'TRUTH'
        if hot:
            sym_curve(d, [p for p in pts if p[0] < 1252], INK, 2.4, 9)
            sym_curve(d, [p for p in pts if p[0] >= 1250], SIG, 3.2, 9)
        else:
            sym_curve(d, pts, INK, 2.2, 9)
        # the pen: an arm from the machine to the tip
        tip = pts[-1]
        for k in range(3):
            line(d, tip[0] + 6, tip[1] - 2 + k * 2, 1760, cy - 40 + k * 2, mix(GR, INK, k * 0.3), 3)
        G(d, 'v', tip[0] - 8, tip[1] - 14, 16, 16, INK, 2.6)
    # time ticks along the top
    for k, x in enumerate(range(PX0 + 90, penx, 240)):
        text(d, x, PY0 + 18, f'0:{28 + k:02d}', mono(18), GR, 'ma'); seg(d, x, PY0 + 44, x, PY0 + 58, GR, 1.6, 10)
    # the hand-written note + circle around the spikes
    ty = PY0 + 60 + ch_h * 3.5
    ellipse(d, 1395, ty, 190, 92, outline=INK, width=2.4)
    hershey(d, 'that sounds real', 1170, ty - 118, 30, INK, 2.4, 'HersheyScript1')
    seg(d, 1300, ty - 104, 1340, ty - 86, INK, 2.2, 12)
    # the machine on the right
    rect(d, 1700, 60, 1920, 1020, INK2); box(d, 1700, 60, 1918, 1020, GR, 2.2, 16)
    for i in range(4):
        cy = PY0 + 60 + ch_h * (i + 0.5); ring(d, 1820, cy - 40, 30, '-', ASH, 3, 18, 12); G(d, '|', 1812, cy - 72, 16, 32, BONE, 3)
        text(d, 1820, cy + 2, f'CH {i + 1}', mono(16), ASH, 'ma')
    text(d, 1810, 90, 'TRUTH-O-GRAPH', mono(15), ASH, 'ma')
    # her, on the left, with a cuff and a cable to the machine
    ox, oy, sw = girl_at(d, 'q_front', 290, 980, 460, knock=INK)
    cx_, cy_ = girl_point(ox, oy, sw, 0.71, 0.66)
    rrect(d, cx_ - 26, cy_ - 34, cx_ + 22, cy_ + 20, 8, fill=INK2)
    for k in range(4): G(d, '=', cx_ - 20, cy_ - 30 + k * 12, 34, 12, BONE, 2.2)
    pts = [(cx_ + 20, cy_ - 10)]
    for k in range(1, 31):
        u = k / 30; pts.append(((1 - u) ** 2 * (cx_ + 20) + 2 * (1 - u) * u * 900 + u * u * 1700, (1 - u) ** 2 * (cy_ - 10) + 2 * (1 - u) * u * -120 + u * u * 140))
    sym_curve(d, pts, GR, 2.2, 11, glyph='.')
    text(d, 60, 1030, 'THEY SAY THAT SOUNDS REAL', mono(26), BONE, 'lm')
    save_scene(im, 'A10', lambda img: grain(img, 5))


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or ['b01', 'a10']): globals()[n]()
