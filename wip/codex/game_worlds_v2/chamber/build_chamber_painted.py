"""Painted mechanical chamber variation of the keyframe Hon had just seen."""
from pathlib import Path
import sys
ROOT=Path(r"D:\Videos\Help! I'm stuck in a LIE")
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/"wip/codex/visual_audit/lib"))
sys.path.insert(0,str(ROOT/"design/character/src"))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import SS, render, sym_heart, INK, BONE

W,H=1920,1080
src=Image.open(HERE/"chamber_plate.png").convert("L").resize((W,H),Image.Resampling.LANCZOS)
# Discrete painted values keep the plate illustrative and in the project's
# greyscale palette; no coloured light or continuous bloom is introduced.
steps=[10,20,34,51,72,98,128,160,195,225,238]
lut=[min(steps,key=lambda z:abs(z-v)) for v in range(256)]
src=src.point(lut)
im=Image.merge("RGB",(src,src,src)).resize((W*SS,H*SS),Image.Resampling.NEAREST)
d=ImageDraw.Draw(im)
render(d,"q_front",416,516,147,knock=INK)
sym_heart(d,1515,500,24,30,7,big=1.0)
fontpath=ROOT/"app/public/fonts/src/IBMPlexMono-Bold.ttf"
if not fontpath.exists(): fontpath=ROOT/"app/public/fonts/IBMPlexMono-Bold.ttf"
font=ImageFont.truetype(str(fontpath),30*SS)
d.text((764*SS,1007*SS),"I STILL GOT A HEART INSIDE",font=font,fill=BONE)
out=im.resize((W,H),Image.Resampling.LANCZOS)
target=HERE/"KF12_HEART_painted_chamber.png"
out.save(target)
print(target)
