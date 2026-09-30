"""One original cut-paper gravity-flip keyframe, 55.15 s on the Edit master.

The generated plate supplies distant architecture. Exact letterforms, character,
direction cues, and visible glyph surface marks are deterministic overlays.
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
from final_sheet import render, SS  # approved bold 17x27 glyph rig

W, H = 1920, 1080
INK = (10, 10, 11)
BONE = (238, 233, 223)
ASH = (156, 151, 143)
GREY = (94, 91, 87)
CHAR = (22, 22, 24)
ORANGE = (255, 83, 20)
FONT_DIR = ROOT / "app" / "public" / "fonts"
F_HEAVY = FONT_DIR / "Archivo-w1250-900.ttf"
F_MONO = FONT_DIR / "src" / "IBMPlexMono-Bold.ttf"
F_REG = FONT_DIR / "src" / "IBMPlexMono-Regular.ttf"


def font(path: Path, n: int):
    return ImageFont.truetype(str(path), n)


def draw_glyph_hatch(im: Image.Image, mask: Image.Image, color, step=32, seed=1):
    """Legible source-code rows clipped to the paper letter surface."""
    rng = random.Random(seed)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = font(F_REG, 22)
    lines = [
        "if (truth) { return real; }",
        "while (stuck) { fall(); }",
        "else { heart.keep(); }",
        "for (let i = 0; i < lie.length; i++) {",
        "  if (name === 'GIRL') break; }",
        "const exit = real ? this : lie;",
    ]
    for y in range(0, H + step, step):
        line = lines[(y // step + seed) % len(lines)]
        x = -rng.randint(0, 220)
        while x < W:
            d.text((x, y + rng.randint(-2, 2)), line, font=f, fill=color + (255,))
            x += int(d.textlength(line, font=f)) + 30
    alpha = Image.composite(lay.getchannel("A"), Image.new("L", im.size, 0), mask)
    lay.putalpha(alpha)
    im.alpha_composite(lay)


def structural_letter(im: Image.Image, letter: str, x: int, y: int, size: int,
                      face, side, angle=0, seed=0):
    """A legible letter as a physical paper slab with dark depth and glyph grain."""
    f = font(F_HEAVY, size)
    box = f.getbbox(letter)
    tw, th = box[2] - box[0], box[3] - box[1]
    pad = 70
    mask0 = Image.new("L", (tw + pad * 2, th + pad * 2), 0)
    d0 = ImageDraw.Draw(mask0)
    d0.text((pad - box[0], pad - box[1]), letter, font=f, fill=255)
    mask = mask0.rotate(angle, Image.Resampling.BICUBIC, expand=True)
    ox, oy = x, y
    # Heavy right/down paper thickness; hard-edged and without light spill.
    for delta in range(34, 0, -2):
        p = Image.new("RGBA", mask.size, side + (255,))
        im.paste(p, (ox + delta, oy + int(delta * 0.52)), mask)
    im.paste(Image.new("RGBA", mask.size, face + (255,)), (ox, oy), mask)
    full = Image.new("L", im.size, 0)
    full.paste(mask, (ox, oy))
    draw_glyph_hatch(im, full, CHAR if face == BONE else ASH,
                     step=31, seed=seed)
    return full


def code_strip(im: Image.Image, x: int, y: int, w: int, h: int,
               code: str, face=BONE, ink=INK, side=GREY, text_size=37):
    """A single code statement is an actual floating paper platform."""
    d = ImageDraw.Draw(im)
    depth = 16
    d.polygon([(x + depth, y + depth), (x + w + depth, y + depth),
               (x + w + depth, y + h + depth), (x + depth, y + h + depth)], fill=INK)
    d.polygon([(x, y + h), (x + w, y + h),
               (x + w + depth, y + h + depth), (x + depth, y + h + depth)], fill=side)
    d.polygon([(x + w, y), (x + w + depth, y + depth),
               (x + w + depth, y + h + depth), (x + w, y + h)], fill=CHAR)
    d.rectangle((x, y, x + w, y + h), fill=face)
    f = font(F_MONO, text_size)
    d.text((x + 23, y + (h - text_size) // 2 - 9), code, font=f, fill=ink)
    d.text((x + w - 36, y + h - 27), "[]", font=font(F_REG, 17), fill=GREY)


def paper_slit(d: ImageDraw.ImageDraw, points, n=35, col=ASH):
    for a, b in zip(points[:-1], points[1:]):
        for j in range(n):
            t = (j + 0.5) / n
            x = a[0] * (1 - t) + b[0] * t
            y = a[1] * (1 - t) + b[1] * t
            glyph = "/" if j % 5 == 0 else "-"
            d.text((x, y), glyph, font=font(F_REG, 17), fill=col)


def add_approved_girl(im: Image.Image):
    # Render using the shared authoritative Python rig at its own 3x supersample.
    # Pose is rotated to show the new rightward gravity while keeping both eyes
    # and her orange symbol heart, which remain the only colored pixels.
    sw = 225
    low = Image.new("RGBA", (500 * SS, 500 * SS), (0, 0, 0, 0))
    render(ImageDraw.Draw(low), "front", 76, 56, sw, knock=INK)
    low = low.resize((500, 500), Image.Resampling.LANCZOS)
    bbox = low.getbbox()
    girl = low.crop(bbox)
    girl = girl.rotate(-90, Image.Resampling.BICUBIC, expand=True)
    # A hard black void cut out of the paper ensures every character is readable.
    cx, cy = 965, 568
    back = Image.new("RGBA", (495, 295), INK + (250,))
    im.alpha_composite(back, (cx - 247, cy - 148))
    im.alpha_composite(girl, (cx - girl.width // 2, cy - girl.height // 2))
    return girl.size


def main():
    plate = Image.open(HERE / "paper_architecture_plate.png").convert("RGB")
    plate = ImageOps.fit(plate, (W, H), method=Image.Resampling.LANCZOS)
    # Distant third dimension recedes; close paper ledges stay high contrast.
    plate = ImageEnhance.Contrast(plate).enhance(0.78)
    bg = Image.blend(plate, Image.new("RGB", (W, H), INK), 0.75).convert("RGBA")
    d = ImageDraw.Draw(bg)

    # Stage boundary: the intact frame remains level as the entire level shifts.
    d.rectangle((40, 42, W - 40, H - 42), outline=GREY, width=2)
    d.line((63, 130, 63, 930), fill=ASH, width=3)
    d.line((1850, 130, 1850, 930), fill=ASH, width=3)
    # Torn strips and folded planes sweep towards the right, in the new gravity.
    d.polygon([(50, 742), (510, 756), (665, 848), (50, 884)], fill=CHAR)
    d.polygon([(60, 742), (520, 755), (544, 779), (60, 771)], fill=ASH)
    d.polygon([(1420, 130), (1850, 104), (1850, 195), (1502, 212)], fill=CHAR)
    d.polygon([(1410, 125), (1848, 100), (1848, 119), (1420, 149)], fill=ASH)

    structural_letter(bg, "L", 82, 265, 675, BONE, GREY, angle=0, seed=13)
    structural_letter(bg, "I", 810, -290, 720, GREY, CHAR, angle=0, seed=25)
    structural_letter(bg, "E", 1280, 150, 750, BONE, GREY, angle=0, seed=33)
    # Indented source lines form the staircase. As gravity rotates, syntax that
    # used to be text becomes a sequence of playable ledges around the girl.
    code_strip(bg, 430, 115, 628, 65, "if (real) {", BONE, INK, GREY, 40)
    code_strip(bg, 526, 200, 725, 65, "  return heart;", ASH, INK, GREY, 39)
    code_strip(bg, 614, 286, 665, 65, "} else {", BONE, INK, GREY, 40)
    code_strip(bg, 1158, 764, 630, 72, "  gravity = 90;", BONE, INK, GREY, 39)
    code_strip(bg, 1212, 863, 576, 72, "  fall('LIE');", ASH, INK, GREY, 39)
    d = ImageDraw.Draw(bg)
    # Exact glyph seams, paper rivets, hinge and fold marks in several depth planes.
    mono = font(F_MONO, 21)
    for x0, y0, count, dx, dy in [
        (112, 210, 22, 24, 0), (1350, 148, 16, 27, 0),
        (117, 837, 27, 23, 0), (1810, 193, 25, 0, 26),
    ]:
        for j in range(count):
            d.text((x0 + j * dx, y0 + j * dy), "[ ]" if j % 4 == 0 else "+", font=mono, fill=ASH)

    # The former floor is a vertical wall. Its dashed ghost shows the rotation.
    for i in range(29):
        y = 160 + 26 * i
        d.text((94, y), "|" if i % 3 else "+", font=font(F_REG, 20), fill=BONE)
    for i in range(34):
        x = 210 + 40 * i
        d.text((x, 956), "_" if i % 5 else "+", font=font(F_REG, 19), fill=GREY)

    # Pictographic game grammar: the new gravity moves RIGHT.
    for i in range(10):
        d.text((612 + i * 73, 832 + (i % 2) * 3), ">", font=font(F_MONO, 46), fill=ASH)
    d.text((475, 910), "GRAVITY 90°", font=font(F_MONO, 30), fill=BONE)
    d.text((740, 910), "|> |> |> |> |> |> |> |> |> |> |> |>", font=font(F_MONO, 30), fill=ASH)

    girl_size = add_approved_girl(bg)
    d = ImageDraw.Draw(bg)
    # Dashed fall path deliberately reads as movement traces, not decorative particles.
    for i in range(17):
        x, y = 560 + i * 24, 570 + int(16 * math.sin(i / 3))
        d.text((x, y), "-" if i % 3 else "+", font=font(F_MONO, 22), fill=ASH)
    # A margin stamp synchronizes to the lyric onset without covering the scene.
    d.rectangle((95, 73, 413, 145), fill=INK, outline=BONE, width=3)
    d.text((112, 84), "STUCK", font=font(F_HEAVY, 53), fill=BONE)
    d.text((99, 991), "02 / PAPER GRAVITY", font=font(F_REG, 20), fill=ASH)
    d.text((1570, 991), "LEVEL ROTATED 90°", font=font(F_REG, 20), fill=ASH)
    bg.convert("RGB").save(HERE / "KF_55p15_stuck_paper_gravity.png", quality=96)
    print(f"saved 1920x1080; rotated girl sprite {girl_size}")


if __name__ == "__main__":
    main()
