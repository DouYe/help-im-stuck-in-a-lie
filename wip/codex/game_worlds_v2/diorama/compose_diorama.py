"""Compose the project's bold glyph girl over the isolated HD-2D diorama plate."""

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
sys.path.insert(0, str(PROJECT / "wip" / "codex" / "visual_audit" / "lib"))
sys.path.insert(0, str(PROJECT / "design" / "character" / "src"))

from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402
import final_sheet as girl  # noqa: E402


def to_ascii_world(plate: Image.Image) -> Image.Image:
    """Use an HD-2D depth plate as a tone map, then build every value from glyphs."""
    width, height = plate.size
    cell_w, cell_h = 9, 14
    cols = (width + cell_w - 1) // cell_w
    rows = (height + cell_h - 1) // cell_h
    values = ImageOps.grayscale(plate).resize((cols, rows), Image.Resampling.BOX)
    font_path = PROJECT / "app" / "public" / "fonts" / "src" / "IBMPlexMono-Regular.ttf"
    if not font_path.exists():
        font_path = PROJECT / "app" / "public" / "fonts" / "src" / "IBMPlexMono-Bold.ttf"
    font = ImageFont.truetype(str(font_path), 13)
    world = Image.new("RGB", (width, height), girl.INK)
    draw = ImageDraw.Draw(world)
    limits = (18, 31, 47, 67, 91, 119, 153, 192, 226)
    glyphs = (" ", ".", ":", "=", "+", "x", "%", "@", "#", "#")
    for row in range(rows):
        for col in range(cols):
            lum = values.getpixel((col, row))
            if lum < limits[0]:
                continue
            tone = sum(lum >= cut for cut in limits)
            char = glyphs[tone]
            # A small deterministic alternation makes the printed terrain read
            # like code gibberish, without bringing back photographic shading.
            h = (col * 17 + row * 31 + col * row * 3) % 13
            if tone == 4 and h < 3:
                char = "-"
            elif tone == 5 and h < 3:
                char = "+"
            elif tone == 6 and h < 3:
                char = "x"
            elif tone == 7 and h < 3:
                char = "%"
            amount = min(1.0, (lum / 255.0) ** 0.77 * 1.17)
            color = tuple(round(a + (b - a) * amount) for a, b in zip(girl.INK, girl.BONE))
            draw.text((col * cell_w, row * cell_h - 2), char, font=font, fill=color)
    return world


def main() -> None:
    plate = Image.open(HERE / "code_diorama_background.png").convert("RGB")
    width, height = plate.size

    base = to_ascii_world(plate)
    base.save(HERE / "code_diorama_ascii_plate.png", optimize=True)

    ss = girl.SS
    image = base.resize((width * ss, height * ss), Image.Resampling.BICUBIC)
    draw = ImageDraw.Draw(image)

    # The feet meet the broad middle-island plane; the nearby stairs can pass
    # in front of her in the animated shot. The shadow is neutral, not a glow.
    draw.ellipse((814 * ss, 654 * ss, 961 * ss, 677 * ss), fill=(18, 18, 19))
    girl.render(draw, "q_front", 790, 395, 185, view="above", big=1.35, knock=girl.INK)

    font_path = PROJECT / "app" / "public" / "fonts" / "src" / "IBMPlexMono-Bold.ttf"
    heading = ImageFont.truetype(str(font_path), 66 * ss)
    draw.text((604 * ss, 71 * ss), "MAKE ME REAL", fill=girl.BONE, font=heading)

    final = image.resize((width, height), Image.Resampling.LANCZOS)
    final.save(HERE / "KF09_make-me-real_code-diorama.png", optimize=True)
    print(f"saved {HERE / 'KF09_make-me-real_code-diorama.png'} {final.size}")


if __name__ == "__main__":
    main()
