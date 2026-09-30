"""Alternate 50.53 s keyframe: the real threshold narrows around the approved glyph girl."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

BASE = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(BASE / "wip/codex/visual_audit/lib"))
sys.path.insert(0, str(BASE / "design/character/src"))

from PIL import Image, ImageDraw, ImageFont
from final_sheet import render as draw_girl, glyph as draw_glyph

SS = 3
W, H = 1920, 1080
INK = (10, 10, 11)
INK2 = (22, 22, 24)
GRAPHITE = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
FONT = BASE / "app/public/fonts/src/IBMPlexMono-Bold.ttf"
OUT = BASE / "wip/codex/root/50_53_real_threshold.png"

im = Image.new("RGB", (W * SS, H * SS), INK)
d = ImageDraw.Draw(im)
rng = random.Random(2036053)


def sym(g: str, x: float, y: float, cell=20.0, col=BONE, weight=2.1):
    draw_glyph(d, g, x, y, cell, cell, col, weight)


def line_of_symbols(x0, y0, x1, y1, char, cell=23, col=ASH, weight=2.2):
    dx, dy = x1-x0, y1-y0
    steps = max(2, round(math.hypot(dx, dy) / cell))
    for i in range(steps+1):
        u = i / steps
        sym(char, x0+dx*u-cell/2, y0+dy*u-cell/2, cell, col, weight)


# The former code world has solid architectural courses, not decorative specks.
for c in range(0, 28):
    x = 46 + c * 25
    for r in range(0, 42):
        y = 70 + r * 22
        if c % 5 == 0:
            g = '+' if r % 7 == 0 else '|'
        elif r % 7 == 0:
            g = '-'
        elif (c + 2*r) % 13 in (0, 1):
            g = '/' if r % 2 else '\\'
        else:
            continue
        col = ASH if x > 490 else GRAPHITE
        sym(g, x, y, 20, col, 1.8 if x < 490 else 2.3)

for c in range(0, 28):
    x = 1215 + c * 25
    for r in range(0, 42):
        y = 70 + r * 22
        if c % 5 == 0:
            g = '+' if r % 7 == 0 else '|'
        elif r % 7 == 0:
            g = '-'
        elif (c + r) % 11 in (0, 1):
            g = '\\' if r % 2 else '/'
        else:
            continue
        col = ASH if x < 1420 else GRAPHITE
        sym(g, x, y, 20, col, 2.3 if x < 1420 else 1.8)

# The code becomes a physical gate: receding nested glyph courses converge on her.
for n in range(7, -1, -1):
    left, right = 678 - n * 31, 1205 + n * 31
    top, bottom = 170 - n * 15, 912 + n * 15
    col = GRAPHITE if n > 4 else (ASH if n > 1 else BONE)
    cell = 22
    for x in range(left+cell, right-cell, cell):
        sym('-', x, top, cell, col, 1.9)
        if n in (0, 3, 6): sym('-', x, bottom, cell, col, 1.9)
    for y in range(top+cell, bottom-cell, cell):
        sym('|', left, y, cell, col, 1.9)
        sym('|', right-cell, y, cell, col, 1.9)
    for x, y in ((left, top), (right-cell, top), (left, bottom-cell), (right-cell, bottom-cell)):
        sym('+', x, y, cell, col, 2.3)

# Directional force: broad banks of slashes shove toward the center on the downbeat.
for k in range(11):
    y = 225 + k * 58
    line_of_symbols(250, y-46, 645, y+36, '/', 26, GRAPHITE if k%3 else ASH, 2.0)
    line_of_symbols(1305, y+36, 1670, y-46, '\\', 26, GRAPHITE if k%3 else ASH, 2.0)

# The gap around the figure is an absence in the character wall.
for y in range(222, 930, 24):
    sym('[', 735, y, 20, BONE, 2.5)
    sym(']', 1130, y, 20, BONE, 2.5)
for x in range(755, 1130, 23):
    sym('-', x, 214, 20, BONE, 2.4)

# Approved Q1 model and literal glyph heart, enlarged only for this proposed emotional insert.
draw_girl(d, 'q_front', 834, 445, 245, 0.0)
for x in range(742, 1138, 22):
    sym('=', x, 845, 20, BONE, 2.5)
for x in range(600, 742, 22):
    sym('=', x, 845, 20, ASH, 2.2)
for x in range(1138, 1290, 22):
    sym('=', x, 845, 20, ASH, 2.2)

# The one sung word at this time is part of the lintel, not a subtitle panel.
font_real = ImageFont.truetype(str(FONT), 64 * SS)
text = 'REAL'
bbox = d.textbbox((0,0), text, font=font_real)
d.text(((W*SS-(bbox[2]-bbox[0]))/2, 270*SS), text, font=font_real, fill=BONE)

OUT.parent.mkdir(parents=True, exist_ok=True)
im.resize((W,H), Image.Resampling.LANCZOS).save(OUT)
print(OUT)
