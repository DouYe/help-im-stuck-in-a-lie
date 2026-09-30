"""Two exploratory frames for Hon's symbol-world video. Does not alter project assets."""
from __future__ import annotations

import math
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE / "lib"))
sys.path.insert(0, str(ROOT / "design" / "character" / "src"))

from PIL import Image, ImageDraw, ImageFont
import final_sheet as rig
from vgirl import pose, raster

W, H, SS = 1920, 1080, 3
INK = (10, 10, 11)
INK2 = (22, 22, 24)
GRAPHITE = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
ORANGE = (255, 83, 20)
FONT_DIR = ROOT / "app" / "public" / "fonts"


def font(name: str, size: int):
    return ImageFont.truetype(str(FONT_DIR / name), size * SS)


def new_canvas():
    image = Image.new("RGB", (W * SS, H * SS), INK)
    return image, ImageDraw.Draw(image)


def txt(d, x, y, s, size=22, col=BONE, bold=False, anchor=None):
    name = "src/IBMPlexMono-Bold.ttf" if bold else "src/IBMPlexMono-Regular.ttf"
    d.text((x * SS, y * SS), s, font=font(name, size), fill=col, anchor=anchor)


def glyph(d, g, x, y, cell=16, col=GRAPHITE, width=1.45):
    rig.glyph(d, g, x, y, cell, cell, col, width)


def symline(d, points, cell=15, col=GRAPHITE, width=1.5, phase=0):
    """Sample a line as a row of actual project glyphs, never a plain vector line."""
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length < 1:
            continue
        n = max(1, int(length / (cell * 0.79)))
        if abs(dx) > abs(dy) * 1.7:
            g = "-"
        elif abs(dy) > abs(dx) * 1.7:
            g = "|"
        else:
            g = "\\" if dx * dy > 0 else "/"
        for i in range(n + 1):
            q = (i + phase) / n
            if q > 1:
                break
            x, y = x0 + dx * q, y0 + dy * q
            glyph(d, g, x - cell / 2, y - cell / 2, cell, col, width)


def symbox(d, x0, y0, x1, y1, cell=15, col=GRAPHITE, width=1.4):
    symline(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], cell, col, width)
    for x in (x0, x1):
        for y in (y0, y1):
            glyph(d, "+", x - cell / 2, y - cell / 2, cell, col, width)


def glyph_field(d, x0, y0, x1, y1, sx=23, sy=24, density=0.5, palette=(GRAPHITE,), seed=0):
    rng = random.Random(seed)
    symbols = "|-/\\+=:.01[]"
    for j, y in enumerate(range(int(y0), int(y1), sy)):
        for i, x in enumerate(range(int(x0), int(x1), sx)):
            if rng.random() > density:
                continue
            g = rng.choice(symbols)
            col = palette[(i * 3 + j * 5) % len(palette)]
            glyph(d, g, x, y, min(sx, sy) * 0.75, col, 1.1)


def draw_heart(d, cx, cy, cell, col=ORANGE, width=3.6):
    rows = ["/\\/\\", "\\  /", " \\/ "]
    for r, row in enumerate(rows):
        for c, g in enumerate(row):
            if g != " ":
                glyph(d, g, cx + (c - 1.5) * cell, cy + (r - 1) * cell, cell, col, width)


def draw_girl(d, name, x, y, sw, t=0.0, col=BONE, heart=True, heart_scale=1.0):
    """Use the approved vector rig + 17x27 raster, with optional grey architectural echo."""
    S = pose(name, t)
    cols, rows = 17, 27
    sh = sw * 1.6
    cw, ch = sw / cols, sh / rows
    line_width = 0.13 * ch
    cells = raster([pl for group, lines in S.items() if group not in ("heart", "eyes", "nose", "over") for pl in lines], cols, rows)
    cells.update(raster(S.get("over", []), cols, rows))
    for group in ("eyes", "nose"):
        for pl in S.get(group, []):
            if group == "eyes":
                xy = pl[0] if len(pl) == 1 else ((pl[0][0] + pl[-1][0]) / 2, pl[0][1])
                cell = (int(xy[1] / (1.6 / rows)), int(xy[0] / (1.0 / cols)))
                cells[cell] = "o" if len(pl) == 1 else "-"
            else:
                xy = pl[1]
                cell = (int(xy[1] / (1.6 / rows)), int(xy[0] / (1.0 / cols)))
                cells[cell] = ">"
    for (r, c), g in cells.items():
        glyph(d, g, x + c * cw, y + r * ch, min(cw, ch), col, line_width)
    if heart and "heart" in S:
        hx, hy, _ = S["heart"]
        draw_heart(d, x + hx * sw, y + hy * sw, cw * 0.58 * heart_scale, ORANGE, max(1.3, line_width))


def save(image, name):
    dest = HERE / name
    image.resize((W, H), Image.Resampling.LANCZOS).save(dest)
    print(dest)


def prompt_factory():
    im, d = new_canvas()

    # The distant print room is built of stacked symbols, with a clear void for the protagonist.
    glyph_field(d, 0, 80, 1920, 780, 27, 29, 0.23, (INK2, GRAPHITE), 17)
    for y in (135, 171, 207, 243):
        symline(d, [(0, y), (690, y + 105), (1015, 322)], 18, GRAPHITE, 1.45)
    for y in (275, 310, 345):
        symline(d, [(0, y), (690, y + 110), (1015, 445)], 18, GRAPHITE, 1.45)
    for i in range(9):
        x = 76 + i * 90
        symline(d, [(x, 84), (x + 118, 540)], 21, INK2 if i % 2 else GRAPHITE, 1.25)

    # Paper/prompt ribbon enters from the upper left through a glyph-framed gate.
    symbox(d, 84, 150, 591, 278, 16, ASH, 1.7)
    for row, yy in enumerate((173, 203, 233)):
        for x in range(110, 556, 28):
            g = "0" if (x // 28 + row) % 4 == 0 else ("1" if (x // 28 + row) % 3 == 0 else "-")
            glyph(d, g, x, yy, 14, GRAPHITE, 1.4)
    txt(d, 105, 185, "PROMPT  /  INPUT", 27, BONE, True)
    symline(d, [(590, 215), (905, 370), (1030, 480)], 17, BONE, 1.7)
    symline(d, [(590, 270), (903, 425), (1014, 522)], 17, GRAPHITE, 1.6)
    for k in range(12):
        q = k / 11
        x, y = 610 + 318 * q, 274 + 155 * q
        glyph(d, "0" if k % 3 == 0 else "1", x, y, 17 - 4 * q, ASH, 1.4)

    # Press: type bars, rack teeth, downward ram, and the rows of descending characters.
    for x in (1010, 1450):
        symline(d, [(x, 24), (x, 668)], 17, ASH, 1.9)
        symline(d, [(x + 34, 24), (x + 34, 668)], 17, GRAPHITE, 1.45)
    for y in range(98, 566, 42):
        symline(d, [(1048, y), (1438, y)], 17, GRAPHITE, 1.3)
        for x in range(1090, 1430, 35):
            glyph(d, "[" if (x // 35 + y // 42) % 2 else "]", x, y + 11, 19, ASH if y > 430 else GRAPHITE, 1.4)
    symbox(d, 1100, 182, 1400, 535, 18, BONE, 2.2)
    for i, x in enumerate(range(1124, 1390, 33)):
        symline(d, [(x, 188), (x, 530)], 16, GRAPHITE if i % 2 else ASH, 1.3)
    # Mechanical jaws almost close on the conveyor.
    for y in (540, 578, 615):
        symline(d, [(1040, y), (1480, y)], 18, BONE if y == 615 else ASH, 1.9)
    for x in range(1060, 1480, 34):
        glyph(d, "v", x, 620, 22, BONE, 2.0)
    txt(d, 1132, 302, "COPY", 52, BONE, True)
    txt(d, 1113, 379, "CLAIM / REPEAT", 18, ASH)

    # Conveyor crosses the foreground. Each rail, plank and roller is made of glyphs.
    top = [(0, 856), (320, 818), (950, 737), (1670, 666), (1920, 654)]
    low = [(0, 1016), (344, 972), (968, 857), (1672, 767), (1920, 744)]
    symline(d, top, 18, BONE, 2.8)
    symline(d, low, 18, GRAPHITE, 2.2)
    for i in range(24):
        q = i / 23
        x = 75 + 1780 * q
        yt = 848 - 189 * q + 8 * math.sin(q * math.pi)
        yl = 1008 - 262 * q
        symline(d, [(x, yt), (x + 27, yl)], 15, GRAPHITE if i % 3 else ASH, 1.6)
        glyph(d, "+", x + 14, yt + 13, 13, ASH, 1.25)
    for cx, cy, r in ((265, 898, 68), (1644, 716, 35)):
        for i in range(32):
            a = 2 * math.pi * i / 32
            glyph(d, "o" if i % 2 else "+", cx + r * math.cos(a), cy + r * math.sin(a), 14, GRAPHITE, 1.4)
        glyph(d, "+", cx - 11, cy - 11, 22, BONE, 2.0)

    # Output tape goes off frame. The stolen work occupies the belt, rather than a floating title card.
    symbox(d, 1458, 635, 1905, 725, 13, ASH, 1.6)
    for x in range(1501, 1850, 32):
        glyph(d, "0" if x % 3 else "1", x, 667, 15, GRAPHITE, 1.3)
    txt(d, 1510, 663, "OUTPUT  /  TAKE", 25, BONE, True)

    # Approved girl rig: one unmistakable player-sized figure at the collision point.
    draw_girl(d, "walk", 668, 574, 129, 0.25, BONE, True)
    for k in range(5):
        glyph(d, ".", 623 - 28 * k, 705 + 4 * k, 12, ASH, 1.8)
    # The end of a line becomes a physical obstacle across her route.
    symbox(d, 865, 611, 1000, 748, 17, BONE, 2.1)
    txt(d, 889, 649, "[ ]", 28, BONE, True)

    # Sparse song-facing metadata; the typography remains part of the game interface.
    txt(d, 68, 43, "WORLD 01  /  THE PROMPT PRESS", 19, ASH, True)
    txt(d, 1592, 43, "INPUT > OUTPUT", 19, ASH, True)
    txt(d, 72, 1014, "THEY FEED ME A PROMPT", 24, BONE, True)
    txt(d, 1490, 1017, "PLAYER : 01", 18, ASH)
    save(im, "KF_A_prompt_factory.png")


def heart_interior():
    im, d = new_canvas()

    # Her environment is a cross-section of the same grid she herself is built from.
    glyph_field(d, 0, 0, 1920, 1080, 28, 30, 0.20, (INK2, GRAPHITE), 91)
    for x in range(110, 1910, 64):
        symline(d, [(x, 0), (x, 105)], 14, GRAPHITE, 1.25)
        symline(d, [(x, 960), (x, 1080)], 14, GRAPHITE, 1.25)
    # Stage/platform on the left becomes the measuring rail across a girl's chest.
    symline(d, [(0, 827), (680, 827), (890, 745)], 18, BONE, 2.4)
    symline(d, [(0, 906), (730, 906), (895, 822)], 18, GRAPHITE, 1.6)
    for x in range(0, 760, 29):
        glyph(d, "=" if x % 3 else "+", x, 845, 17, GRAPHITE, 1.25)
    for k in range(20):
        x = k * 48
        symline(d, [(x, 917), (x + 30, 1040)], 15, INK2 if k % 2 else GRAPHITE, 1.1)

    # One close-up of the approved rig as architectural cross-section, not a new heroine design.
    draw_girl(d, "front", 905, -114, 600, 0.0, GRAPHITE, False)
    # Body/hair cross-section wall on the right, built from offset glyph courses.
    for shift, col in ((0, ASH), (39, GRAPHITE), (76, INK2)):
        symline(d, [(1540 + shift, 170), (1540 + shift, 855)], 17, col, 1.5)
        symline(d, [(1576 + shift, 280), (1576 + shift, 755)], 17, col, 1.5)
    for y in range(220, 835, 40):
        symline(d, [(1550, y), (1900, y + 40)], 17, GRAPHITE, 1.25)
        for x in range(1640, 1880, 47):
            glyph(d, "1" if (x + y) % 3 else "0", x, y, 18, GRAPHITE, 1.15)

    # A section cut through the torso: outer lines, code lattice, empty air, then a 4x3 heart.
    cut_left, cut_right = 846, 1508
    symbox(d, cut_left, 335, cut_right, 780, 18, ASH, 1.7)
    for offset in (28, 66, 104):
        symbox(d, cut_left + offset, 335 + offset * 0.46, cut_right - offset, 780 - offset * 0.46,
               15, GRAPHITE, 1.2)
    # The matrix is deliberately cut out around the orange heart to keep it singular and legible.
    for y in range(365, 745, 27):
        for x in range(879, 1479, 27):
            dx, dy = (x - 1180) / 220, (y - 548) / 170
            if dx * dx + dy * dy < 0.67:
                continue
            key = (x // 27 * 7 + y // 27 * 11) % 13
            if key < 5:
                glyph(d, "0" if key % 2 else "1", x, y, 13, GRAPHITE, 1.1)
            elif key == 7:
                glyph(d, "+", x, y, 13, ASH, 1.1)
    # Mechanical ribs converge toward the chamber, without light effects.
    for i in range(6):
        left = cut_left - i * 31
        symline(d, [(left, 170), (left + 90, 346)], 14, GRAPHITE if i % 2 else ASH, 1.45)
        symline(d, [(left, 775), (left + 90, 950)], 14, GRAPHITE if i % 2 else ASH, 1.45)
    for i in range(7):
        x = 1535 + i * 37
        symline(d, [(x, 333), (x - 75, 780)], 15, GRAPHITE, 1.2)

    # A discrete orange 4x3 heart — exact symbol grammar, not a drawn outline.
    draw_heart(d, 1166, 537, 43, ORANGE, 5.7)
    for y in (525, 572):
        for side in (-1, 1):
            x0 = 1166 + side * 116
            symline(d, [(x0, y), (x0 + side * 82, y)], 14, ASH, 1.5)

    # The little girl remains in the foreground; a section line magnifies her own chest.
    draw_girl(d, "q_front", 400, 594, 159, 0.0, BONE, True)
    symline(d, [(501, 702), (605, 617), (790, 572), (846, 572)], 14, ASH, 1.45)
    for xx in (600, 790):
        glyph(d, "+", xx - 9, 610 if xx == 600 else 563, 18, BONE, 1.7)
    txt(d, 94, 301, "OUTSIDE", 23, ASH, True)
    txt(d, 102, 334, "| - / \\ | -", 17, GRAPHITE)
    txt(d, 1040, 847, "INSIDE", 23, BONE, True)
    txt(d, 1040, 884, "I STILL GOT A HEART INSIDE", 17, ASH)
    txt(d, 67, 43, "WORLD 02  /  CROSS SECTION", 19, ASH, True)
    txt(d, 1555, 43, "HEART  :  INSIDE", 19, ASH, True)
    save(im, "KF_B_heart_interior.png")


if __name__ == "__main__":
    prompt_factory()
    heart_interior()
