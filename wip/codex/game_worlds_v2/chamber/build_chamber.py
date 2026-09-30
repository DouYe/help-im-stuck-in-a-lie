"""Code-glyph painted inner-heart chamber, using the approved girl and heart."""
from pathlib import Path
import sys

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / "wip/codex/visual_audit/lib"))
sys.path.insert(0, str(ROOT / "design/character/src"))
sys.path.insert(0, str(HERE.parent))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import render, sym_heart, SS, INK, BONE, SIG, ASH
from ascii_paint import paint

W,H = 1920,1080
plate = Image.open(HERE / "chamber_plate.png")
im = paint(plate,(W,H),cell=(11,16),supersample=SS)
d=ImageDraw.Draw(im)
font_path=ROOT / "app/public/fonts/src/IBMPlexMono-Bold.ttf"
if not font_path.exists(): font_path=ROOT / "app/public/fonts/IBMPlexMono-Bold.ttf"
def txt(x,y,s,size,col=BONE):
    d.text((x*SS,y*SS),s,font=ImageFont.truetype(str(font_path),size*SS),fill=col)

# Readable syntax has physical consequences: the return statement is the
# bridge; the condition at the valve selects whether the heart remains.
txt(613,567,"if (heart) {",38,ASH)
txt(758,613,"return REAL;",40,BONE)
render(d,"q_front",416,516,147,knock=INK)
# Only the two symbol hearts carry orange; the big one is the level goal.
sym_heart(d,1515,500,24,30,7,big=1.0)

out=im.resize((W,H),Image.Resampling.LANCZOS)
target=HERE/"KF12_HEART_ascii_chamber.png"
out.save(target)
print(target)
