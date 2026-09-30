"""ASCII-only visible 2D cut-paper gravity puzzle frame for 55.15 s.

Generated paper architecture is read only as a luminance/depth map, then every
visible surface is re-rendered from actual monospaced ASCII characters.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\visual_audit\lib")
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "design" / "character" / "src"))
from final_sheet import render, SS

W, H = 1920, 1080
INK = (10, 10, 11)
CHAR = (22, 22, 24)
GREY = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
FONT_DIR = ROOT / "app" / "public" / "fonts"
F_MONO = FONT_DIR / "src" / "IBMPlexMono-Regular.ttf"
F_BOLD = FONT_DIR / "src" / "IBMPlexMono-Bold.ttf"
F_BLOCK = FONT_DIR / "Archivo-w1250-900.ttf"


def font(p, n):
    return ImageFont.truetype(str(p), n)


def mask_letter(letter, x, y, size, path=F_BLOCK):
    f = font(path, size)
    bounds = f.getbbox(letter)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text((x - bounds[0], y - bounds[1]), letter, font=f, fill=255)
    return m


def mask_poly(points):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(points, fill=255)
    return m


def shift_mask(mask, dx, dy):
    m = Image.new("L", (W, H), 0)
    m.paste(mask, (dx, dy))
    return m


def glyph_field(d, mask, chars, palette, cell_w=13, cell_h=18, seed=1):
    """Dense exact glyphs, clipped by a paper/letter mask."""
    rng = random.Random(seed)
    small = mask.resize((math.ceil(W/cell_w), math.ceil(H/cell_h)), Image.Resampling.BOX)
    p = small.load()
    f = font(F_MONO, 18)
    for row in range(small.height):
        for col in range(small.width):
            if p[col, row] < 100:
                continue
            idx = (row * 17 + col * 11 + rng.randrange(len(chars))) % len(chars)
            d.text((col*cell_w, row*cell_h-4), chars[idx], font=f,
                   fill=palette[(row + 3*col) % len(palette)])


def distant_ascii(d, plate):
    """Render four tonal planes from ASCII, never displaying the source pixels."""
    cell_w, cell_h = 14, 19
    gray = ImageEnhance.Contrast(ImageOps.grayscale(plate)).enhance(1.28)
    s = gray.resize((math.ceil(W/cell_w), math.ceil(H/cell_h)), Image.Resampling.BOX)
    p = s.load()
    f = font(F_MONO, 17)
    for row in range(s.height):
        for col in range(s.width):
            v = p[col,row]
            if v < 36: continue
            if v < 62: ch, color = '.', GREY
            elif v < 90: ch, color = ':', GREY
            elif v < 125: ch, color = '+', GREY
            elif v < 165: ch, color = 'x', ASH
            elif v < 205: ch, color = '%', ASH
            else: ch, color = '@', ASH
            d.text((col*cell_w, row*cell_h-3), ch, font=f, fill=color)


def structural_letter(im, letter, x, y, size, seed):
    face = mask_letter(letter, x, y, size)
    side = shift_mask(face, 26, 19)
    # The old plane is cut away before each nearer paper layer is assembled.
    im.paste(INK, (0,0), side)
    d = ImageDraw.Draw(im)
    glyph_field(d, side, '=+.x', [GREY, GREY, CHAR], seed=seed+40)
    im.paste(INK, (0,0), face)
    d = ImageDraw.Draw(im)
    glyph_field(d, face, '@%#x', [BONE, ASH, BONE], seed=seed)
    # Fine fold seams at the letter edges, also made of literal symbols.
    return face


def ascii_paper_strip(d, x, y, w, h, code, shade, size=36):
    """A line of source code whose indented paper strip is a traversable ledge."""
    f = font(F_MONO, 17)
    d.rectangle((x-7, y-16, x+w+21, y+h+29), fill=INK)
    for r in range(2, 0, -1):
        yy = y + h + r*9
        for xx in range(x+17, x+w+17, 13):
            d.text((xx, yy), '=', font=f, fill=GREY)
    for yy in range(y, y+h, 18):
        for xx in range(x, x+w, 13):
            k = (xx//13 + yy//18) % 5
            d.text((xx, yy), '@' if k == 0 else ('%' if k < 3 else 'x'),
                   font=f, fill=shade)
    for xx in range(x, x+w, 13):
        d.text((xx, y-12), '=', font=f, fill=BONE)
        d.text((xx, y+h-6), '=', font=f, fill=ASH)
    # Erase a thin dark strip behind text for one-step readability, maintaining
    # the ASCII upper and lower structural surfaces.
    d.rectangle((x+12,y+8,x+w-13,y+h-8), fill=INK)
    d.text((x+24, y+6), code, font=font(F_BOLD,size), fill=BONE)


def approved_girl_rotated(d_canvas):
    # Uses the approved 17x27, bold stroke, knockout, symbol-heart implementation.
    high = Image.new('RGBA', (570*SS, 570*SS), (0,0,0,0))
    render(ImageDraw.Draw(high), 'front', 100, 62, 220, knock=INK)
    low = high.resize((570,570), Image.Resampling.LANCZOS)
    girl = low.crop(low.getbbox()).rotate(-90, Image.Resampling.BICUBIC, expand=True)
    cx, cy = 963, 582
    # The void is a literal code block, bounded by big braces; black is the
    # negative space that lets the bold girl survive a complex ASCII world.
    d_canvas.alpha_composite(girl, (cx-girl.width//2, cy-girl.height//2))
    return girl.size


def main():
    source = Image.open(HERE/'paper_architecture_plate.png').convert('RGB')
    source = ImageOps.fit(source, (W,H), method=Image.Resampling.LANCZOS)
    im = Image.new('RGB', (W,H), INK)
    d = ImageDraw.Draw(im)
    distant_ascii(d, source)

    # Foreground paper planes read as form and shadow solely through glyph
    # density. The sideways L, dropped I, and open E never form one flat word.
    glyph_field(d, mask_poly([(0,723),(521,743),(672,809),(0,849)]),
                '%@x', [GREY, ASH], seed=101)
    glyph_field(d, mask_poly([(1430,107),(1920,79),(1920,150),(1510,171)]),
                '=+x', [ASH, GREY], seed=102)
    structural_letter(im, 'L', 118, 290, 610, 11)
    structural_letter(im, 'I', 846, -155, 620, 22)
    structural_letter(im, 'E', 1385, 195, 660, 33)
    d = ImageDraw.Draw(im)

    # The level is runnable code: indentation creates actual steps; a later
    # return drops the character into the lower else branch.
    ascii_paper_strip(d, 365, 134, 618, 60, 'if (real) {', ASH, 39)
    ascii_paper_strip(d, 469, 225, 682, 62, '  return heart;', GREY, 36)
    ascii_paper_strip(d, 584, 316, 586, 62, '} else {', ASH, 39)
    ascii_paper_strip(d, 1160, 809, 650, 64, '  gravity = 90;', GREY, 35)
    ascii_paper_strip(d, 1245, 916, 566, 65, '  fall("LIE");', ASH, 35)

    # A physical uncompiled void opens between those branches. Braces are the
    # near-plane gate and make the paper stage's code grammar unmistakable.
    d.rectangle((738, 409, 1195, 735), fill=INK)
    glyph_field(d, mask_letter('{', 752, 464, 288, F_BOLD), '=+x', [GREY, ASH], seed=210)
    glyph_field(d, mask_letter('}', 1105, 464, 288, F_BOLD), '=+x', [GREY, ASH], seed=211)
    for j in range(34):
        xx = 770+j*13
        d.text((xx,404), '=', font=font(F_MONO,17), fill=ASH)
        d.text((xx,725), '=', font=font(F_MONO,17), fill=ASH)

    # Past route across the left edge, now a wall; newly horizontal acceleration.
    for j in range(47):
        d.text((64, 150+j*17), '|' if j%5 else '+', font=font(F_MONO,19), fill=ASH)
    for j in range(26):
        xx = 1020+j*29
        d.text((xx, 746), '>' if j%3 else '>>', font=font(F_MONO,25), fill=GREY)
    for j in range(19):
        xx = 522+j*25
        d.text((xx, 579 + int(9*math.sin(j/3))), '-' if j%4 else '+',
               font=font(F_MONO,22), fill=ASH)

    # Lyric and rotation information are in-scene, exact and small. No HUD box.
    d.text((101, 78), 'STUCK', font=font(F_BOLD,57), fill=BONE)
    d.text((115, 1000), 'rotate(90);', font=font(F_MONO,24), fill=ASH)

    layer = im.convert('RGBA')
    size = approved_girl_rotated(layer)
    out = HERE/'KF_55p15_stuck_paper_gravity_ASCII.png'
    layer.convert('RGB').save(out)
    print(f'{out} {size} 1920x1080')

if __name__ == '__main__':
    main()
