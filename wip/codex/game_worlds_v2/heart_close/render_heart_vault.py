"""ASCII memory-vault keyframe for HEART INSIDE; original code-world game scene.

All scenery is painted with monospaced glyphs.  The character comes straight
from the project's approved 17 x 27 bold vector-to-symbol rig.
"""

from __future__ import annotations

import math
import os
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
CHARACTER_SRC = PROJECT / "design" / "character" / "src"
sys.path.insert(0, str(CHARACTER_SRC))
import final_sheet as girl  # noqa: E402


W, H = 1920, 1080
SS = girl.SS
INK = (10, 10, 11)
BONE = (238, 233, 223)
ASH = (156, 151, 143)
GREY = (94, 91, 87)
ORANGE = (255, 83, 20)
FONTS = PROJECT / "app" / "public" / "fonts"
MONO = FONTS / "src" / "IBMPlexMono-Regular.ttf"
MONO_BOLD = FONTS / "src" / "IBMPlexMono-Bold.ttf"
TITLE = FONTS / "Archivo-w1250-900.ttf"

im = Image.new("RGB", (W * SS, H * SS), INK)
d = ImageDraw.Draw(im)
cell_font = ImageFont.truetype(MONO, 16 * SS)
small_font = ImageFont.truetype(MONO, 18 * SS)
med_font = ImageFont.truetype(MONO_BOLD, 24 * SS)
title_font = ImageFont.truetype(TITLE, 54 * SS)
rng = random.Random(203)


def color(intensity: float) -> tuple[int, int, int]:
    """Constrain all tones to the project's ink/bone monochrome ramp."""
    a = min(1.0, max(0.0, intensity))
    return tuple(round(INK[k] * (1 - a) + BONE[k] * a) for k in range(3))


def ptext(x: float, y: float, value: str, font, shade=1.0) -> None:
    d.text((round(x * SS), round(y * SS)), value, font=font, fill=color(shade))


def segment_distance(x, y, x0, y0, x1, y1):
    vx, vy = x1 - x0, y1 - y0
    q = max(0.0, min(1.0, ((x - x0) * vx + (y - y0) * vy) / (vx * vx + vy * vy)))
    return math.hypot(x - (x0 + q * vx), y - (y0 + q * vy))


def field(x: float, y: float, u: int, v: int) -> tuple[str, float]:
    """Architecture as ASCII brushwork: ceiling, ribbed vault, columns, floor."""
    salt = ((u * 1051 + v * 1919) % 107) / 107.0
    z = 0.0
    hint = ""

    # Distant programmable night: deliberately sparse where the girl reads.
    if salt > 0.964 and y < 730:
        z, hint = 0.18 + 0.11 * salt, "."

    # An array of roof ribs converges on the chamber's vanishing point.
    for side in (-1, 1):
        for k, (x0, y0, x1, y1) in enumerate(
            (
                (960 + side * 68, 240, 960 + side * 340, 55),
                (960 + side * 130, 300, 960 + side * 700, 25),
                (960 + side * 250, 405, 960 + side * 1020, 35),
            )
        ):
            ds = segment_distance(x, y, x0, y0, x1, y1)
            if ds < (12 + k * 3):
                z = max(z, 0.23 + 0.12 * k + 0.16 * (1 - ds / (12 + k * 3)))
                hint = "/" if side > 0 else "\\"

    dx = abs(x - 960)

    # The rear chamber's three successive openings form an actual 2.5D route.
    for half, base, curve, bottom, level in (
        (180, 345, 0.0018, 746, 0.17),
        (290, 272, 0.00135, 806, 0.30),
        (420, 157, 0.00112, 852, 0.43),
    ):
        top = base + curve * dx * dx
        if dx < half and top < y < bottom:
            edge = min(half - dx, y - top, bottom - y)
            val = level * (0.68 + 0.32 * salt)
            if edge < 23:
                val = min(1.0, level + 0.32 * (1 - edge / 23))
                hint = "#" if edge < 9 else "%"
            elif edge < 58:
                hint = "x"
            z = max(z, val)
        # Lighter code-cut face around each opening, like glyph masonry.
        if abs(y - top) < 11 and dx < half + 12:
            val = level + (0.38 if half == 420 else 0.24)
            z = max(z, min(0.89, val))
            hint = "%" if half == 420 else "="

    # Cut the deepest portal hollow back out; this preserves a calm silhouette
    # behind the protagonist rather than covering her in background noise.
    if dx < 162 and y > 390 + 0.0018 * dx * dx and y < 746:
        z = min(z, 0.075)
        hint = "." if salt > 0.90 else ""

    # Paired foreground columns read like monumental game collision geometry.
    for side in (-1, 1):
        cx = 960 + side * 725
        across = abs(x - cx)
        if across < 105 and 204 < y < 1080:
            base = 0.36 + 0.12 * math.cos((x - cx) / 19.0) + 0.14 * salt
            if across > 78:
                base = max(base, 0.73)
                hint = "@"
            elif (int(y) - 204) % 88 < 14:
                base = max(base, 0.57)
                hint = "="
            z = max(z, min(0.86, base))
        if across < 137 and 193 < y < 260:
            z = max(z, 0.61 + 0.10 * salt)
            hint = "#"
        if across < 113 and 378 < y < 400:
            z = max(z, 0.54)
            hint = "="

    # A glyph-built tile floor actually extends under the character, so the
    # space feels traversable instead of an arbitrary text texture.
    if y > 756:
        depth = min(1.0, (y - 756) / 324)
        z = max(z, (0.055 + 0.17 * depth) * (0.4 + 0.6 * salt))
        if min(abs(y - yy) for yy in (776, 813, 873, 962, 1075)) < 10:
            z = max(z, 0.25 + 0.33 * depth)
            hint = "="
        for spread in (-1010, -630, -365, -170, 0, 170, 365, 630, 1010):
            xline = 960 + spread * (y - 756) / 324
            if abs(x - xline) < 10:
                z = max(z, 0.22 + 0.34 * depth)
                hint = "/" if spread < 0 else "\\" if spread > 0 else "|"
        # The near screen edge is deliberately much denser.
        if y > 985 and salt > 0.24:
            z = max(z, 0.25 + 0.19 * salt)

    # Fallen blocks of code: game-world debris, with bright broken rims.
    for bx, by, bw, bh in (
        (400, 775, 190, 72),
        (1335, 735, 163, 64),
        (86, 891, 215, 95),
        (1600, 878, 228, 97),
    ):
        inside = bx < x < bx + bw and by < y < by + bh
        if inside:
            rim = min(x - bx, bx + bw - x, y - by, by + bh - y)
            z = max(z, 0.22 + 0.23 * salt if rim > 17 else 0.59)
            hint = "#" if rim < 17 else "x"

    if z < 0.115 and not hint:
        return "", 0.0
    if hint and z >= 0.22:
        return hint, z
    ramp = ".:+=x#%@"
    index = max(0, min(len(ramp) - 1, int(z * (len(ramp) + 1))))
    return ramp[index], z


# The ASCII cells themselves create every mass and edge in the world.
CW, CH = 12, 18
for row, y in enumerate(range(0, H, CH)):
    for col, x in enumerate(range(0, W, CW)):
        ch, value = field(x + CW / 2, y + CH / 2, col, row)
        if ch:
            ptext(x, y - 3, ch, cell_font, value)

# Code exists on the walls as syntax carved into the level, not a separate HUD.
# It stays behind the protagonist and is laid out on the two flanking piers.
for x, y, lines in (
    (375, 448, ("if (heart) {", "  remember();", "} else {", "  erase();", "}")),
    (1322, 470, ("while (alive) {", "  keep = true;", "  break;", "}")),
):
    for i, line in enumerate(lines):
        ptext(x, y + i * 31, line, small_font, 0.40 + (0.07 if i in (0, 2) else 0))

# Camera framing: the approved clean-line girl stays sharply readable in front
# of the ASCII-painted gothic level.  Her symbol heart is enlarged for this beat.
girl.render(d, "heart", 707, 151, 506, big=2.32, knock=INK)

# A compact text-adventure dialogue tile, cut into the near plane of the
# environment.  The border is also literal code glyphs.
d.rectangle((52 * SS, 914 * SS, 674 * SS, 1072 * SS), fill=INK)
for x in range(48, 679, 13):
    ptext(x, 900, "=", cell_font, 0.62)
    ptext(x, 1060, "=", cell_font, 0.62)
for y in range(918, 1060, 18):
    ptext(42, y, "|", cell_font, 0.62)
    ptext(671, y, "|", cell_font, 0.62)
ptext(77, 931, "HEART INSIDE", title_font, 1.0)
ptext(78, 1015, "> SAVE THE LAST TRUE THING", small_font, 0.72)
ptext(1453, 50, "[ MEMORY VAULT ]", med_font, 0.65)

out = im.resize((W, H), Image.Resampling.LANCZOS)
out_path = HERE / "KF13_heart_inside_ascii_vault.png"
out.save(out_path, optimize=True)
print(out_path)
