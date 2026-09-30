"""ASCII-built boss lock keyframe, 50.6 s (Edit master).

Uses the project's locked 17x27 bold glyph girl. All architecture is
typeset from actual glyphs, rather than a textured image under code.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LIB = ROOT / "wip" / "codex" / "visual_audit" / "lib"
sys.path.insert(0, str(LIB))
sys.path.insert(0, str(ROOT / "design" / "character" / "src"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from final_sheet import render as render_girl  # noqa: E402

OUT = Path(__file__).with_name("KF10_real_this_time_syntax_lock.png")
W, H, S = 1920, 1080, 3
INK = (10, 10, 11)
LOW = (22, 22, 24)
GREY = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
ORANGE = (255, 83, 20)
FONT_ROOT = ROOT / "app" / "public" / "fonts" / "src"
REGULAR = FONT_ROOT / "IBMPlexMono-Regular.ttf"
BOLD = FONT_ROOT / "IBMPlexMono-Bold.ttf"
random.seed(506)

im = Image.new("RGB", (W * S, H * S), INK)
d = ImageDraw.Draw(im)


def font(px: float, bold: bool = False):
    return ImageFont.truetype(str(BOLD if bold else REGULAR), int(px * S))


def txt(x, y, s, px=18, col=BONE, bold=False, anchor=None):
    d.text((int(x * S), int(y * S)), s, font=font(px, bold), fill=col, anchor=anchor)


def line(points, col=GREY, width=1):
    d.line([(int(x * S), int(y * S)) for x, y in points], fill=col, width=int(width * S), joint="curve")


def polygon(points, fill=LOW):
    d.polygon([(int(x * S), int(y * S)) for x, y in points], fill=fill)


def char_mask(points, char_px, step_x, step_y, palette, chars, jitter=0, seed=0):
    """Fill a geometry mask with monospaced symbols. Character values create its material."""
    r = random.Random(seed)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(points, fill=255)
    bb = mask.getbbox()
    if bb is None:
        return
    f = font(char_px)
    for y in range(max(0, bb[1]), min(H, bb[3]), step_y):
        for x in range(max(0, bb[0]), min(W, bb[2]), step_x):
            xx = x + int(r.uniform(-jitter, jitter)) if jitter else x
            yy = y + int(r.uniform(-jitter, jitter)) if jitter else y
            if 0 <= xx < W and 0 <= yy < H and mask.getpixel((xx, yy)):
                z = r.random()
                index = min(len(chars) - 1, int(z * len(chars)))
                col = palette[(index + int((x / W) * 2)) % len(palette)]
                d.text((xx * S, yy * S), chars[index], font=f, fill=col)


def char_polyline(points, symbol="=", spacing=15, size=16, col=BONE, phase=0):
    """Symbols, not a drawn stroke, form a visible structural rail."""
    f = font(size, True)
    carry = -phase
    for a, b in zip(points, points[1:]):
        x0, y0 = a
        x1, y1 = b
        length = math.hypot(x1 - x0, y1 - y0)
        if not length:
            continue
        while carry < length:
            if carry >= 0:
                u = carry / length
                x = x0 + (x1 - x0) * u
                y = y0 + (y1 - y0) * u
                ch = symbol[int(carry // spacing) % len(symbol)]
                d.text((x * S, y * S), ch, font=f, fill=col, anchor="mm")
            carry += spacing
        carry -= length


def ascii_word(cx, cy, word, col=BONE):
    """Use a word stencil only to place visible, discrete ASCII characters."""
    letter_size = 270
    letter_font = ImageFont.truetype(str(BOLD), letter_size)
    word_mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(word_mask).text((cx, cy), word, font=letter_font,
                                   fill=255, anchor="mm")
    # Knockout is black; the final white shape is made exclusively of glyphs.
    d.text((cx * S, cy * S), word, font=font(letter_size, True),
           fill=INK, anchor="mm")
    box = word_mask.getbbox()
    if box is None:
        return
    chars = "@%#x+=@#%"
    f = font(14, True)
    for yy in range(box[1], box[3], 12):
        for xx in range(box[0], box[2], 9):
            if word_mask.getpixel((xx, yy)):
                ch = chars[(xx // 9 + yy // 12) % len(chars)]
                d.text((xx * S, yy * S), ch, font=f,
                       fill=col if (xx + yy) % 11 else ASH)


# 1. Five-depth void. Dots are tiny background glyphs, not particles.
for row in range(10, 43):
    y = row * 22 + (row % 3) * 3
    for col in range(11, 166):
        x = col * 12
        if random.random() < (0.095 if row < 20 else 0.065):
            txt(x, y, "." if random.random() < .8 else ":", 11, GREY)

# Distant hanging false branches, low value.
for bx, h in [(158, 570), (257, 450), (1660, 500), (1760, 650), (100, 330), (1840, 350)]:
    for yy in range(0, h, 27):
        txt(bx + 18 * math.sin(yy / 51 + bx), yy, "|", 19, LOW)
        if yy % 81 == 0:
            txt(bx - 20, yy + 5, "}", 15, GREY)

# 2. The compiler gate is a single floating machine with six typeset planes.
# Its facets use distinct character sizes and densities for depth.
far_left = [(290, 154), (582, 125), (672, 300), (705, 748), (580, 880), (271, 809)]
far_right = [(1338, 299), (1421, 124), (1715, 151), (1740, 808), (1420, 880), (1302, 748)]
char_mask(far_left, 15, 11, 17, [LOW, GREY, GREY], ".:+%=#", seed=1)
char_mask(far_right, 15, 11, 17, [LOW, GREY, GREY], ".:+%=#", seed=2)

lintel = [(571, 111), (1350, 111), (1455, 267), (464, 267)]
char_mask(lintel, 17, 12, 18, [GREY, GREY, ASH], "x#@%+=", seed=3)
char_polyline([(571, 111), (1350, 111), (1455, 267)], "=x", 14, 17, ASH)
char_polyline([(464, 267), (571, 111)], "/x", 13, 16, GREY)
txt(682, 146, "if (heart == true) {", 45, BONE, True)
txt(682, 214, "// THE LOCK EVALUATES YOU", 18, ASH)

# The two side plates close sideways on the variable in the center.
left_plate = [(537, 270), (819, 267), (829, 755), (715, 836), (515, 805)]
right_plate = [(1102, 267), (1383, 270), (1402, 805), (1205, 836), (1090, 755)]
char_mask(left_plate, 17, 11, 18, [GREY, ASH, GREY, ASH], "x#@%+=", seed=4)
char_mask(right_plate, 17, 11, 18, [GREY, ASH, GREY, ASH], "x#@%+=", seed=5)
char_polyline([(537, 270), (819, 267), (829, 755), (715, 836)], "=|", 13, 17, BONE)
char_polyline([(1102, 267), (1383, 270), (1402, 805), (1205, 836)], "=|", 13, 17, BONE)

# Depth shadow cutout: a carved void, bounded entirely by text.
opening = [(829, 292), (1090, 292), (1171, 360), (1171, 728), (1090, 800),
           (829, 800), (749, 728), (749, 360)]
polygon(opening, INK)
char_polyline(opening + [opening[0]], "/=\\|", 10, 16, ASH)
inner = [(835, 340), (1083, 340), (1130, 398), (1130, 690),
         (1083, 750), (835, 750), (790, 690), (790, 398)]
char_polyline(inner + [inner[0]], "<>=|", 12, 15, GREY)

# Flat planes recede into the lock, represented as nested code brackets.
for i in range(6):
    inset = i * 21
    L = 807 + inset
    R = 1114 - inset
    top = 351 + inset * .63
    bot = 735 - inset * .5
    ch = ":" if i % 2 else "="
    char_polyline([(L, top), (R, top), (R, bot), (L, bot), (L, top)],
                  ch, 13 + i, 14 - i * .6, GREY if i < 3 else LOW)

# The hexagonal variable core cuts through the side plates. Its edges are
# code rails, while the large lyric inside is printed from literal ASCII.
core = [(711, 366), (1209, 366), (1291, 489), (1209, 617),
        (711, 617), (629, 489)]
polygon(core, INK)
char_polyline(core + [core[0]], "=<>", 11, 17, ASH)
for xx in range(690, 1240, 18):
    txt(xx, 381, ":" if xx % 3 else ".", 12, GREY)
    txt(xx, 594, ":" if xx % 3 else ".", 12, GREY)

# The opposite braces are *moving jaws*: the carved symbols themselves
# define the geometry, and the central seam is the unsafe contact point.
for yy in range(329, 749, 24):
    u = (yy - 329) / 420
    jaw = 55 * math.exp(-((u - .5) / .17) ** 2)
    lx = 621 - jaw
    rx = 1299 + jaw
    txt(lx - 34, yy, "{{{", 27, BONE if yy % 72 else ASH, True)
    txt(rx, yy, "}}}", 27, BONE if yy % 72 else ASH, True)
    if yy % 48 == 17:
        txt(lx - 98, yy, "0", 18, GREY)
        txt(rx + 100, yy, "1", 18, GREY)

# REAL is assembled from dense, exact @/%/#/x glyphs in the variable slot.
ascii_word(960, 482, "REAL", col=BONE)
char_polyline([(960, 647), (960, 735)], "|", 14, 20, ASH)
txt(960, 687, "?", 32, BONE, True, "mt")

# Two condition branches project out as playable platforms. One terminates.
left_path = [(0, 904), (226, 829), (527, 831), (710, 783), (771, 790),
             (632, 920), (483, 977), (247, 978), (0, 1053)]
char_mask(left_path, 16, 12, 18, [LOW, GREY, GREY, ASH], ".:+%=#", seed=6)
char_polyline([(0, 904), (226, 829), (527, 831), (710, 783), (771, 790)],
              "==>", 13, 18, BONE)
char_polyline([(0, 1053), (247, 978), (483, 977), (632, 920), (771, 790)],
              "==>", 13, 18, GREY)

right_path = [(1920, 905), (1703, 824), (1406, 827), (1217, 782), (1140, 792),
              (1300, 915), (1462, 970), (1694, 978), (1920, 1050)]
char_mask(right_path, 16, 12, 18, [LOW, GREY, GREY, ASH], ".:+%=#", seed=7)
char_polyline([(1920, 905), (1703, 824), (1406, 827), (1217, 782), (1140, 792)],
              "<==", 13, 18, BONE)
char_polyline([(1920, 1050), (1694, 978), (1462, 970), (1300, 915), (1140, 792)],
              "<==", 13, 18, GREY)

# A void/fork, not a conventional corridor. The bridge is a code branch.
bridge = [(716, 836), (827, 776), (1093, 776), (1214, 836),
          (1075, 972), (844, 972)]
char_mask(bridge, 17, 12, 19, [GREY, GREY, ASH, GREY], "=+x%@#", seed=8)
char_polyline([(716, 836), (827, 776), (1093, 776), (1214, 836)],
              "==", 11, 18, BONE)
char_polyline([(844, 972), (1075, 972)], "=+", 14, 18, ASH)
txt(980, 846, "return REAL;", 27, BONE, True, "mt")

# The false route folds into a dead-end boss paw, deliberately readable.
txt(1450, 816, "} else {", 29, ASH, True)
txt(1497, 858, "LOCK();", 31, BONE, True)
for j in range(6):
    txt(1481 + j * 19, 925, "x", 22, GREY)

# Literal code rain acts as hanging load-bearing chains attached to the gate.
for base, y0, y1 in [(493, 250, 774), (1444, 250, 754), (603, 270, 696),
                     (1325, 270, 685)]:
    for yy in range(y0, y1, 22):
        txt(base, yy, "{}" if yy % 44 else "[]", 16, GREY)
    txt(base - 27, y1 - 10, "}>", 21, ASH)

# Girl and the only orange. Same project rig, same bold stroke, true knockout.
# She is the near-plane playable sprite, facing 45 degrees toward the lock.
render_girl(d, "q_frontwalk", 335, 646, 205, t=.25,
            knock=INK, col=BONE, hot=ORANGE)

# Local gameplay labels stay English and under the lyric.
txt(83, 70, "LEVEL 09  /  CONDITIONAL LOCK", 20, ASH, True)
txt(1510, 70, "01 / 02", 18, GREY, True)
txt(281, 996, "IF TRUE  >>>", 23, BONE, True)
txt(1267, 997, "<<<  IF FALSE", 22, GREY, True)
txt(960, 1011, "ASSERT(REAL)", 36, BONE, True, "mt")

im.resize((W, H), Image.Resampling.LANCZOS).save(OUT)
print(OUT)
