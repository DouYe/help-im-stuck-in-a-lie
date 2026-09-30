"""Two original, precisely matched glyph-world keyframes.

All visible geometry is a stroke glyph from the project's locked alphabet.
The girl is rasterized from the project's locked Python rig, read-only.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
OUT = PROJECT / "wip" / "codex" / "tech_audit"
sys.path.insert(0, str(PROJECT / "design" / "character" / "src"))
from glyphs import G  # noqa: E402
from vgirl import pose, raster  # noqa: E402

S = 2
W, H = 1920, 1080
INK = (10, 10, 11)
INK2 = (22, 22, 24)
GRAPHITE = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
ORANGE = (255, 83, 20)
FAINT_DARK = (47, 46, 45)
FAINT_LIGHT = (201, 197, 188)
FONT_DIR = PROJECT / "app" / "public" / "fonts"
FONT_DISPLAY = FONT_DIR / "Archivo-w1250-900.ttf"
FONT_MONO = FONT_DIR / "src" / "IBMPlexMono-SemiBold.ttf"
HEART = ["/\\/\\", "\\  /", " \\/ "]
ANCHOR = (960, 560)
GIRL_WIDTH = 135


def ip(v: float) -> int:
    return int(round(v * S))


def canvas(bg: tuple[int, int, int]):
    im = Image.new("RGB", (W * S, H * S), bg)
    return im, ImageDraw.Draw(im)


def glyph(d: ImageDraw.ImageDraw, ch: str, x: float, y: float, cw: float,
          hh: float, color: tuple[int, int, int], lw: float = 1.5):
    if ch == " ":
        return
    paths = G.get(ch)
    if paths is None:
        raise ValueError(f"unknown glyph: {ch!r}")
    weight = max(1, ip(lw))
    for path in paths:
        pts = [(ip(x + u * cw), ip(y + v * hh)) for u, v in path]
        if len(pts) == 2 and pts[0] == pts[1]:
            px, py = pts[0]
            rr = max(1, weight)
            d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=color)
        else:
            d.line(pts, fill=color, width=weight, joint="curve")
            rr = max(1, weight // 2)
            for px, py in (pts[0], pts[-1]):
                d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=color)


def glyph_line(d: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float],
               step: float, color: tuple[int, int, int], weight: float = 1.7,
               chars: str | None = None):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = max(1, int(math.hypot(dx, dy) / step))
    if chars is None:
        if abs(dx) > abs(dy) * 2.0:
            chars = "-="
        elif abs(dy) > abs(dx) * 2.0:
            chars = "|"
        else:
            chars = "\\" if dx * dy > 0 else "/"
    for i in range(n + 1):
        t = i / n
        ch = chars[i % len(chars)]
        xx = a[0] + dx * t
        yy = a[1] + dy * t
        glyph(d, ch, xx - step * .48, yy - step * .48, step * .96, step * .96, color, weight)


def glyph_poly(d: ImageDraw.ImageDraw, pts: list[tuple[float, float]],
               step: float, color: tuple[int, int, int], weight: float = 1.7,
               chars: str | None = None):
    for a, b in zip(pts[:-1], pts[1:]):
        glyph_line(d, a, b, step, color, weight, chars)


def mono(d: ImageDraw.ImageDraw, xy: tuple[float, float], s: str,
         size: int, col: tuple[int, int, int]):
    f = ImageFont.truetype(str(FONT_MONO), size * S)
    d.text((ip(xy[0]), ip(xy[1])), s, font=f, fill=col)


def glyph_title(d: ImageDraw.ImageDraw, word: str, x: int, y: int,
                font_size: int, cell: int, color: tuple[int, int, int],
                pattern: str = r"|-/\+", spacing: int = 0):
    """Set a word in the glyph alphabet by using a type mask as a stencil."""
    f = ImageFont.truetype(str(FONT_DISPLAY), font_size)
    bbox = f.getbbox(word, stroke_width=0)
    tw, th = bbox[2] - bbox[0] + 6, bbox[3] - bbox[1] + 6
    mask = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(mask)
    md.text((3 - bbox[0], 3 - bbox[1]), word, font=f, fill=255, spacing=spacing)
    for yy in range(0, th, cell):
        for xx in range(0, tw, cell):
            sample = mask.crop((xx, yy, min(xx + cell, tw), min(yy + cell, th)))
            if sum(sample.get_flattened_data()) / max(1, sample.width * sample.height) > 95:
                ch = pattern[((xx // cell) * 7 + (yy // cell) * 11) % len(pattern)]
                glyph(d, ch, x + xx, y + yy, cell * .94, cell * .94, color, max(1.15, cell * .17))
    return tw, th


def heart(d: ImageDraw.ImageDraw, cx: float, cy: float, big: float = 1.0):
    # Exact match-cut anchor in both frames: the same seven orange stroke glyphs.
    cw, ch = 10.8 * big, 10.4 * big
    x0, y0 = cx - 2 * cw, cy - 1.5 * ch
    for r, row in enumerate(HEART):
        for c, g in enumerate(row):
            if g != " ":
                glyph(d, g, x0 + c * cw, y0 + r * ch, cw, ch, ORANGE, 2.25 * big)


def girl(d: ImageDraw.ImageDraw, name: str, color: tuple[int, int, int],
         anchor: tuple[int, int] = ANCHOR, width: int = GIRL_WIDTH):
    """Project's locked 17x27 rig; only pose changes across the cut."""
    shape = pose(name, 0.0)
    hx, hy, _ = shape["heart"]
    ox, oy = anchor[0] - hx * width, anchor[1] - hy * width
    cw, ch = width / 17, width * 1.6 / 27
    main = [pl for group, paths in shape.items() if group not in ("heart", "eyes", "nose", "over") for pl in paths]
    cells = raster(main, 17, 27)
    cells.update(raster(shape.get("over", []), 17, 27))
    top: dict[tuple[int, int], str] = {}
    for pl in shape.get("eyes", []):
        ex, ey = pl[0]
        if len(pl) == 1:
            top[(int(ey / (1.6 / 27)), int(ex / (1 / 17)))] = "o"
        else:
            mx = (pl[0][0] + pl[-1][0]) / 2
            top[(int(ey / (1.6 / 27)), int(mx / (1 / 17)))] = "-"
    for pl in shape.get("nose", []):
        nx, ny = pl[1]
        top[(int(ny / (1.6 / 27)), int(nx / (1 / 17)))] = ">"
    for k in top:
        cells.pop(k, None)
    for (r, c), g in cells.items():
        glyph(d, g, ox + c * cw, oy + r * ch, cw, ch, color, 1.9)
    for (r, c), g in top.items():
        glyph(d, g, ox + c * cw, oy + r * ch, cw, ch, color, 1.9)
    heart(d, *anchor)


def rows(d: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float,
         cw: float, ch: float, pattern: str, color: tuple[int, int, int],
         weight: float = 1.2, phase: int = 0):
    for row in range(int(h / ch)):
        for col in range(int(w / cw)):
            g = pattern[(col * 3 + row * 5 + phase) % len(pattern)]
            glyph(d, g, x + col * cw, y + row * ch, cw, ch, color, weight)


def arrow_band(d: ImageDraw.ImageDraw, x0: float, x1: float, y: float,
               cell: float, color: tuple[int, int, int], count: int = 3):
    for row in range(count):
        yy = y + row * cell * 1.4
        for x in range(int(x0), int(x1), int(cell * 2.4)):
            glyph(d, ">", x, yy, cell, cell, color, 1.35)


def make_a():
    im, d = canvas(INK)
    # A dense, regular machine inscription, never a random particle field.
    for y in range(80, 1040, 44):
        for x in range(60, 1860, 44):
            if (x // 44 + y // 44) % 7 == 0:
                glyph(d, ".", x, y, 5, 5, FAINT_DARK, 1.0)

    glyph_line(d, (60, 70), (1860, 70), 16, ASH, 1.4, "-=")
    mono(d, (70, 86), "STAGE 02 / FALSE FLOOR", 22, ASH)
    mono(d, (1510, 86), "NO EXIT  /  00:46", 19, ASH)
    glyph_title(d, "STUCK", 68, 138, 170, 9, BONE)
    glyph_title(d, "IN A LIE", 70, 322, 93, 7, ASH)
    # Typography becomes physical confinement: the last line of glyphs flows into the chute.
    for j in range(7):
        glyph_line(d, (85, 447 + j * 16), (735 - j * 15, 447 + j * 16), 13, FAINT_DARK if j > 2 else GRAPHITE, 1.15, "-_=+")

    # Long left-hand symbol platform and visible broken support ribs.
    for y in (703, 714, 728, 741):
        glyph_line(d, (56, y), (865, y), 11, BONE if y == 703 else GRAPHITE, 1.7, "=+-")
    for x in range(70, 850, 60):
        glyph_line(d, (x, 752), (x + 12, 1060), 11, GRAPHITE, 1.35, "|/1")
        glyph_line(d, (x, 772), (x + 58, 838), 11, FAINT_DARK, 1.1, "\\")
    rows(d, 58, 760, 815, 250, 17, 19, r"|0/1\-+", FAINT_DARK, 1.0)
    # The step she expected is a glyph skeleton, severed at the next beat.
    glyph_line(d, (868, 705), (1015, 705), 9, BONE, 1.8, "-=")
    glyph_line(d, (874, 735), (955, 735), 10, GRAPHITE, 1.4, "-_")
    glyph_poly(d, [(1016, 660), (1035, 700), (1010, 725), (1039, 770)], 9, BONE, 2.0, "/\\")
    glyph_line(d, (880, 795), (1050, 1050), 13, FAINT_DARK, 1.3, "\\")

    # Right: a funnel of 0/1/| glyphs, architecturally packed and falling away.
    upper1, upper2 = (1084, 296), (1850, 625)
    lower1, lower2 = (1074, 724), (1850, 1010)
    for j in range(15):
        q = j / 14
        a = (upper1[0] * (1 - q) + lower1[0] * q,
             upper1[1] * (1 - q) + lower1[1] * q)
        b = (upper2[0] * (1 - q) + lower2[0] * q,
             upper2[1] * (1 - q) + lower2[1] * q)
        glyph_line(d, a, b, 12 + q * 4, GRAPHITE if j % 4 else BONE, 1.2 if j % 4 else 1.8, r"/\|01")
    for q in [i / 12 for i in range(13)]:
        a = (upper1[0] * (1 - q) + upper2[0] * q,
             upper1[1] * (1 - q) + upper2[1] * q)
        b = (lower1[0] * (1 - q) + lower2[0] * q,
             lower1[1] * (1 - q) + lower2[1] * q)
        glyph_line(d, a, b, 13, FAINT_DARK if int(q * 12) % 3 else ASH, 1.2, "|1")
    glyph_line(d, upper1, upper2, 11, BONE, 2.3, "/\\")
    glyph_line(d, lower1, lower2, 11, BONE, 2.3, "/\\")
    glyph_line(d, (1070, 317), (1070, 676), 9, BONE, 2.1, "|1")
    glyph_line(d, (1052, 338), (1052, 638), 12, ASH, 1.25, "|")
    arrow_band(d, 416, 794, 566, 12, GRAPHITE)
    mono(d, (1540, 1010), "DROP / 0x00", 20, ASH)

    # Matched figure and orange centre remain at exactly the same pixel coordinates in B.
    girl(d, "stuck", BONE)
    glyph_line(d, (60, 1040), (1860, 1040), 16, GRAPHITE, 1.1, "-")
    mono(d, (70, 1000), "STUCK IN A LIE   /   THE GROUND REFUSES TO HOLD", 18, ASH)
    out = OUT / "01_stuck_side_chute.png"
    im.resize((W, H), Image.Resampling.LANCZOS).save(out)
    return out


def project(x: float, z: float, elevation: float = 0.0):
    f = 1.0 / (z + 1.2)
    return (960 + x * 700 * f, 228 + (860 - elevation * 620) * f)


def wall(d: ImageDraw.ImageDraw, p0: tuple[float, float], p1: tuple[float, float],
         height: float, rows_n: int = 10, cols_n: int = 36,
         emphasis: bool = False):
    """Extruded maze wall, with every surface mark a glyph."""
    bot0, bot1 = project(*p0), project(*p1)
    top0, top1 = project(*p0, height), project(*p1, height)
    for ri in range(rows_n + 1):
        v = ri / rows_n
        for ci in range(cols_n + 1):
            u = ci / cols_n
            xa = top0[0] * (1 - u) + top1[0] * u
            ya = top0[1] * (1 - u) + top1[1] * u
            xb = bot0[0] * (1 - u) + bot1[0] * u
            yb = bot0[1] * (1 - u) + bot1[1] * u
            px = xa * (1 - v) + xb * v
            py = ya * (1 - v) + yb * v
            if -30 <= px < W + 30 and -30 <= py < H + 30:
                # Tile size follows perspective. No gradients or glow: distinct two-tone planes.
                size = 5 + 9 / (min(p0[1], p1[1]) + 1.1)
                pattern = r"|/-\+01"
                ch = pattern[(ci * 3 + ri * 5) % len(pattern)]
                col = INK if emphasis or ri in (0, rows_n) or ci in (0, cols_n) else GRAPHITE
                glyph(d, ch, px - size / 2, py - size / 2, size, size, col, 1.3 if col == INK else 1.0)
    glyph_line(d, top0, top1, 8, INK, 2.0, "-+")
    glyph_line(d, bot0, bot1, 8, INK, 1.55, "-=")
    glyph_line(d, top0, bot0, 8, INK, 1.8, "|")
    glyph_line(d, top1, bot1, 8, INK, 1.8, "|")


def make_b():
    im, d = canvas(BONE)
    # A clean editorial strip. Inversion is the beat-cut impact, not a glow effect.
    # This frame is 47.5s: only MAKE has been sung. ME and REAL arrive later.
    glyph_title(d, "MAKE", 610, 32, 190, 8, INK, r"|-/\+")
    glyph_line(d, (72, 218), (1848, 218), 13, INK, 1.7, "-+")
    mono(d, (77, 232), "FLOOR 03 / RECURSIVE MAZE", 20, GRAPHITE)
    mono(d, (1567, 232), "EXIT: UNDEFINED", 19, GRAPHITE)

    # The floor itself recedes into a deep vanishing grid of stroke symbols.
    for x in [i * .5 for i in range(-8, 9)]:
        glyph_line(d, project(x, 0), project(x, 12), 12, FAINT_LIGHT, 1.0, "/")
    for z in [0, .36, .8, 1.4, 2.1, 3.1, 4.6, 6.6, 9.3, 12]:
        glyph_line(d, project(-4.4, z), project(4.4, z), 11, FAINT_LIGHT, 1.0, "-")

    # A genuine branching maze, rendered far to near. Low walls expose the plan
    # from a steep pitch: staggered crossbars force a left/right/left/right route.
    segments = [
        ((-3.9, 8.5), (3.9, 8.5), .62),
        ((-3.9, 7.6), (-.4, 7.6), .63), ((-.4, 7.6), (-.4, 6.8), .63),
        ((.8, 6.8), (3.9, 6.8), .66), ((.8, 6.8), (.8, 5.9), .66),
        ((-3.9, 5.7), (1.4, 5.7), .7), ((1.4, 5.7), (1.4, 4.9), .7),
        ((-.2, 4.8), (3.9, 4.8), .7), ((-.2, 4.8), (-.2, 3.7), .7),
        ((-3.9, 3.7), (.3, 3.7), .74), ((.3, 3.7), (.3, 2.9), .74),
        ((1.5, 2.8), (3.9, 2.8), .78), ((1.5, 2.8), (1.5, 2.0), .78),
        ((-3.9, 1.9), (-1.3, 1.9), .8), ((-1.3, 1.9), (-1.3, 1.15), .8),
        ((-3.9, 8.5), (-3.9, 1.9), .55),
        ((3.9, 8.5), (3.9, 2.8), .55),
        ((1.25, .7), (4.2, .7), .56),
        ((-4.2, .35), (-1.5, .35), .56),
    ]
    for p0, p1, hh in segments:
        wall(d, p0, p1, hh, 7 if min(p0[1], p1[1]) > 4 else 9,
             24 if min(p0[1], p1[1]) > 4 else 34,
             emphasis=min(p0[1], p1[1]) < 2)

    # Route forks: fixed graphic chevrons, with no motion blur or atmospheric wash.
    for z in (.8, 1.2, 1.7, 2.4, 3.2, 4.5):
        for x in (-.55, 0, .55):
            px, py = project(x, z)
            size = max(7, 19 / (z + 1))
            glyph(d, "^", px - size / 2, py - size / 2, size, size, GRAPHITE, 1.3)

    # A nested threshold, not a photo-real door: each jamb is a stack of | and 1.
    for zz in (9.5, 8.3, 7.1):
        ltop = project(-.75, zz, 1.25)
        rtop = project(.75, zz, 1.25)
        lbot = project(-.75, zz)
        rbot = project(.75, zz)
        glyph_poly(d, [lbot, ltop, rtop, rbot], 8, INK, 1.9, "|+-")

    # Same location, width and symbol-heart geometry as A; she turns toward the maze.
    girl(d, "q_front", INK)
    glyph_line(d, (74, 1010), (1844, 1010), 15, GRAPHITE, 1.2, "-+")
    mono(d, (77, 1024), "ONE BODY / MANY POSSIBLE EXITS", 18, GRAPHITE)
    mono(d, (1516, 1024), "PATH 000 / 001", 18, GRAPHITE)
    out = OUT / "02_make_me_real_deep_maze.png"
    im.resize((W, H), Image.Resampling.LANCZOS).save(out)
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (make_a, make_b):
        print(fn())
