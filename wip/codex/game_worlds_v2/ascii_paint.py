"""Turn a monochrome depth/value plate into literal ASCII brushstrokes."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\visual_audit\lib")))
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
FONT = ROOT / "app/public/fonts/src/IBMPlexMono-Regular.ttf"
if not FONT.exists(): FONT = ROOT / "app/public/fonts/IBMPlexMono-Regular.ttf"

def paint(src, size=(1920,1080), cell=(11,16), supersample=2):
    """Sample a plate's values; rebuild *all* visible tones from drawn glyphs.

    Returns an RGB canvas at supersampled dimensions. Callers can add the
    approved rig/text at this scale, then downsample once at export.
    """
    W,H = size; sx,sy = cell; S=supersample
    cols,rows = (W+sx-1)//sx,(H+sy-1)//sy
    mono = src.convert("L").resize((cols,rows), Image.Resampling.BOX)
    out = Image.new("RGB",(W*S,H*S),(10,10,11))
    d = ImageDraw.Draw(out)
    font = ImageFont.truetype(str(FONT), 15*S)
    # Dense groups use alternating symbols so tonal blocks resemble an ASCII
    # painting, as in the supplied S5 reference, not repeated paragraphs.
    groups = ["", ".", ".:", ":;", "-+=", "+=x", "xX#", "#%X", "%@#", "@%#"]
    pix = mono.load()
    for row in range(rows):
        for col in range(cols):
            v = pix[col,row]
            band = max(0,min(9,int(v/26)))
            if band == 0: continue
            variants = groups[band]
            glyph = variants[(col*17 + row*31 + col*row*3)%len(variants)]
            # Quantized grey, not a continuous gradient. The glyph's filled
            # area contributes the other half of tonal variation.
            tone = (65,82,99,117,138,165,188,210,232,238)[band]
            d.text((col*sx*S, row*sy*S - 4*S), glyph, font=font, fill=(tone,tone,tone))
    return out
