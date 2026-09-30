"""Build an original layered 2D cavern keyframe from a generated plate and the approved glyph girl."""
from pathlib import Path
import sys

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(ROOT / "wip/codex/visual_audit/lib"))
sys.path.insert(0, str(ROOT / "design/character/src"))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import render, SS, INK, BONE, ASH

HERE = Path(__file__).parent
SOURCE = HERE / "cavern_plate.png"
OUTPUT = HERE / "KF06_HELP_cavern_game.png"
W, H = 1920, 1080

plate = Image.open(SOURCE).convert("RGB")
plate = plate.resize((W * SS, H * SS), Image.Resampling.LANCZOS)
# Restrict the rendered scene to an ordered ink/bone grey scale. The generated
# plate contains subtle continuum tones; 12 levels keep the depth without
# introducing a second hue or photographic blur.
pixels = plate.load()
steps = [10, 17, 27, 39, 53, 68, 85, 104, 126, 150, 176, 205, 232]
lut = [min(steps, key=lambda v: abs(v - i)) for i in range(256)]
for y in range(0, H * SS):
    for x in range(0, W * SS):
        r, g, b = pixels[x, y]
        v = lut[round(0.2126 * r + 0.7152 * g + 0.0722 * b)]
        pixels[x, y] = (v, v, v)

d = ImageDraw.Draw(plate)
# Place the heroine on the playable bridge. Her own row-by-row knockout is
# deliberately black, matching the bridge silhouette while preserving every
# approved glyph/eye/heart in the canonical rig.
render(d, "walk", 873, 526, 155, t=0.25, knock=INK)

# Sung lyric as one piece of level signage. The other game-world studies use
# wholly different typography and UI.
font_path = ROOT / "app/public/fonts/src/IBMPlexMono-Bold.ttf"
if not font_path.exists():
    font_path = ROOT / "app/public/fonts/IBMPlexMono-Bold.ttf"
font = ImageFont.truetype(str(font_path), 76 * SS)
d.text((1510 * SS, 636 * SS), "HELP", font=font, fill=BONE, stroke_width=1 * SS, stroke_fill=INK)

out = plate.resize((W, H), Image.Resampling.LANCZOS)
out.save(OUTPUT)
print(OUTPUT)
