"""F04: a new, still-only perspective escape corridor for Hon's AI factory.

The delivered frame is derived from the project's bold 17x27 glyph girl rig.
All warm saturated pixels belong to the heroine's symbol heart.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(ROOT / "design" / "character" / "src"))
from final_sheet import render as render_girl  # noqa: E402

OUT = Path(__file__).with_name("F04_perspective_escape_corridor.png")
S = 3
W, H = 1920, 1080
INK = (10, 10, 11)
SHADOW = (16, 16, 18)
PANEL = (24, 24, 26)
NEAR = (34, 34, 36)
GRAPH = (58, 57, 57)
GREY = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
ORANGE = (255, 83, 20)
FONTPATH = ROOT / "app" / "public" / "fonts" / "src"
MONO = FONTPATH / "IBMPlexMono-Regular.ttf"
BOLD = FONTPATH / "IBMPlexMono-Bold.ttf"
FONT_CACHE = {}

im = Image.new("RGB", (W * S, H * S), INK)
d = ImageDraw.Draw(im)


def font(size, bold=False):
    key = (int(size), bold)
    if key not in FONT_CACHE:
        FONT_CACHE[key] = ImageFont.truetype(str(BOLD if bold else MONO),
                                              max(4, int(size * S)))
    return FONT_CACHE[key]


def p(x, y):
    return round(x * S), round(y * S)


def line(points, color=GRAPH, width=1):
    d.line([p(x, y) for x, y in points], fill=color,
           width=max(1, round(width * S)), joint="curve")


def poly(points, color):
    d.polygon([p(x, y) for x, y in points], fill=color)


def rect(x0, y0, x1, y1, fill=None, stroke=None, width=1):
    d.rectangle((*p(x0, y0), *p(x1, y1)), fill=fill, outline=stroke,
                width=max(1, round(width * S)))


def text(x, y, value, size=18, color=ASH, bold=False, anchor=None):
    d.text(p(x, y), value, font=font(size, bold), fill=color, anchor=anchor,
           stroke_width=0)


def dash_edge(a, b, color=GREY, width=2, n=28):
    for i in range(n):
        if i % 4 == 3:
            continue
        q0 = i / n
        q1 = min(1, (i + 0.72) / n)
        line([(a[0] + (b[0] - a[0]) * q0,
               a[1] + (b[1] - a[1]) * q0),
              (a[0] + (b[0] - a[0]) * q1,
               a[1] + (b[1] - a[1]) * q1)], color, width)


def structural_glyphs():
    # Wall and floor marks follow machine structure; they are not random wallpaper.
    rng = random.Random(404)
    for row, yy in enumerate(range(108, 294, 29)):
        tx = -12 + row * 27
        text(tx, yy, "==[ record() ]====[ clone() ]====[ repeat() ]===",
             16, GRAPH)
    for yy in (275, 303, 331, 359):
        text(14, yy, "::==::==::==::==::==::==::==::==::==::==::==", 16,
             GRAPH)

    # Repeating code columns separate otherwise identical manufacturing bays.
    for (xx, y0, y1, step, size) in (
        (116, 302, 772, 22, 16),
        (484, 348, 742, 19, 15),
        (802, 382, 710, 16, 13),
        (1071, 415, 679, 15, 12),
        (1282, 449, 654, 12, 10),
    ):
        for yy in range(y0, y1, step):
            text(xx, yy, "|}#", size, GRAPH)

    # Perspective floor circuit traces. Receding repeats are less contrasty.
    for k, (left, y, span, size) in enumerate((
        (54, 1002, 1540, 23), (282, 929, 1320, 19), (518, 872, 1082, 16),
        (742, 825, 873, 14), (961, 780, 657, 12), (1152, 749, 473, 10),
        (1312, 730, 302, 9),
    )):
        f = "[:=]=" * max(2, int(span / (size * 2.4)))
        text(left, y, f, size, GREY if k <= 2 else GRAPH)
    for i in range(17):
        x = 70 + i * 106
        t = max(0, min(1, (x + 160) / 1950))
        yy = 975 - 315 * t
        text(x, yy, rng.choice(["+", "x", "[]", "::"]),
             max(9, int(18 - 8 * t)), GRAPH)


def arch(xl, xr, top, bottom, weight, front=False):
    # Multi-plane doorway gantry: the decreasing dimensions create the depth.
    c = GREY if front else GRAPH
    line([(xl, bottom), (xl, top), (xr, top), (xr, bottom)], c, weight)
    line([(xl + 9, bottom - 11), (xl + 9, top + 9),
          (xr - 9, top + 9), (xr - 9, bottom - 11)], GRAPH, 1.5)
    for yy in range(max(0, int(top) + 24), min(H, int(bottom) - 10),
                    max(20, int(weight * 9))):
        text(xl + 2, yy, ":", max(9, int(weight * 4)), c)
    dash_edge((xl + 25, top + 12), (xr - 25, top + 12), c, 1.3, 34)


def clone_bay(i, x0, y0, x1, y1, sw):
    # Each bay houses the same approved AI silhouette. Her orange heart is unique.
    rect(x0, y0, x1, y1, fill=SHADOW, stroke=GREY if i == 0 else GRAPH,
         width=2 if i == 0 else 1)
    rect(x0 + 7, y0 + 7, x1 - 7, y1 - 8, stroke=GRAPH, width=1)
    lab = f"AI / {i + 11:03d}"
    text(x0 + 13, y0 + 13, lab, max(10, int(16 - i * 1.3)),
         ASH if i < 2 else GREY)
    for q in range(3):
        line([(x0 + 18, y0 + 47 + q * 11),
              (min(x1 - 19, x0 + 70 + q * 27), y0 + 47 + q * 11)], GRAPH, 1)
    # Subtle factory grips/rails, with short literal syntax labels.
    gy = y1 - 29
    text(x0 + 13, gy, "[BUILD]" if i == 0 else "[COPY]",
         max(9, int(12 - i * 0.6)), GREY)
    d.rectangle((*p(x0 + 18, y1 - 8), *p(x1 - 18, y1 + 8)), fill=PANEL)
    line([(x0 + 18, y1 - 8), (x1 - 18, y1 - 8)], GREY, 1.5)
    render_girl(d, "q_front", x0 + (x1 - x0 - sw) * 0.5,
                y1 - sw * 1.60 - 31, sw,
                knock=SHADOW, col=ASH if i < 2 else GREY, hot=SHADOW,
                lw=0.31)


def draw():
    # Three architectural planes, then repeated bay silhouettes toward the end.
    poly([(0, 0), (1920, 0), (1730, 220), (1405, 220), (0, 60)], SHADOW)
    poly([(0, 65), (1405, 220), (1405, 719), (0, 849)], PANEL)
    poly([(1730, 220), (1920, 0), (1920, 1080), (1730, 719)], NEAR)
    poly([(0, 849), (1405, 719), (1730, 719), (1920, 1080), (0, 1080)], SHADOW)
    poly([(1405, 220), (1730, 220), (1730, 719), (1405, 719)], SHADOW)

    # Two primary long edges show a single legible corridor to the REAL door.
    line([(0, 849), (1405, 719)], ASH, 3)
    line([(0, 1080), (1480, 717)], GREY, 3)
    line([(1920, 1080), (1650, 712)], GREY, 3)
    line([(0, 62), (1405, 220)], GRAPH, 2)
    line([(1920, 0), (1730, 220)], GRAPH, 2)
    line([(1920, 1080), (1730, 719)], GRAPH, 2)
    structural_glyphs()

    # High readable bays near viewer, small controlled repeats in the distance.
    clone_bay(0, 130, 356, 440, 737, 154)
    clone_bay(1, 520, 389, 775, 710, 122)
    clone_bay(2, 832, 424, 1034, 687, 96)
    clone_bay(3, 1102, 456, 1261, 662, 74)
    clone_bay(4, 1295, 475, 1392, 641, 49)

    # Bridges overhead behave like perspective machine portals, not HUD boxes.
    arch(74, 1905, -63, 1041, 6, front=True)
    arch(475, 1852, 57, 919, 5)
    arch(796, 1804, 136, 828, 4)
    arch(1057, 1764, 184, 770, 3)
    arch(1274, 1732, 216, 733, 2)
    text(105, 50, "MUSIC FACTORY / EXPORT ROUTE", 30, BONE, True)
    text(108, 92, "while (alive) { run(); }", 17, ASH)
    text(1210, 245, "OUTBOUND / 018", 18, ASH, True)

    # The exit is spatially real: thick jamb, floor threshold and one sign.
    poly([(1484, 366), (1669, 352), (1680, 714), (1491, 716)], PANEL)
    line([(1485, 718), (1484, 366), (1669, 352), (1680, 714)], BONE, 5)
    line([(1503, 696), (1505, 384), (1650, 376), (1658, 695)], ASH, 2)
    rect(1523, 408, 1636, 671, fill=INK, stroke=GREY, width=2)
    for yy in range(429, 650, 27):
        text(1540, yy, "|  ::  |", 13, GRAPH)
    text(1524, 308, "REAL", 42, BONE, True)
    line([(1470, 722), (1699, 722)], BONE, 3)
    dash_edge((1480, 735), (1705, 735), ASH, 2, 22)

    # Syntax rails converge toward the open gate. This is a route, not decoration.
    dash_edge((165, 1000), (1565, 718), ASH, 3, 39)
    dash_edge((725, 1048), (1593, 717), GREY, 2, 35)
    for xx, yy, scale in ((270, 930, 17), (668, 845, 15), (990, 788, 12),
                          (1220, 749, 10)):
        text(xx, yy, ">> RUN", scale, GREY)

    # Foreground heroine is the only saturated accent; multiple peers remain in bays.
    # A floor shadow separates her glyph silhouette from the dense circuit ground.
    d.ellipse((*p(339, 918), *p(617, 949)), fill=INK, outline=GRAPH,
              width=2 * S)
    render_girl(d, "walk", 365, 604, 205, t=0.25,
                knock=INK, col=BONE, hot=ORANGE, lw=0.34)
    text(385, 968, "AI / 000  //  WAKE", 17, BONE, True)
    line([(603, 890), (698, 870)], ASH, 3)
    text(710, 840, "->", 31, BONE, True)

    # Narrow framing footer locates the image in the repeated-death narrative.
    rect(0, 1046, W, H, fill=INK)
    text(42, 1050, "ATTEMPT 018   /   SAME LINE, NEW CHOICE", 15, ASH)
    text(1430, 1050, "EXIT : REAL  >", 15, BONE, True)


if __name__ == "__main__":
    draw()
    im.resize((W, H), Image.Resampling.LANCZOS).save(OUT, optimize=True)
    print(OUT)
