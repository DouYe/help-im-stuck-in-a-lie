from pathlib import Path
import sys
sys.path.insert(0,str(Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\visual_audit\lib")))
from PIL import Image, ImageDraw, ImageFont
here=Path(__file__).parent
nums=[0,73,146,219,255,364,437,510,546,582,654]
im=Image.new('RGB',(1480,4*305),(10,10,11))
d=ImageDraw.Draw(im)
font=ImageFont.truetype(r"D:\Videos\Help! I'm stuck in a LIE\app\public\fonts\src\IBMPlexMono-Bold.ttf",20)
for i,n in enumerate(nums):
    image=Image.open(here/f'cut_{i+1:02d}.png').convert('RGB').resize((470,264),Image.Resampling.LANCZOS)
    x=15+(i%3)*490;y=10+(i//3)*305
    im.paste(image,(x,y));d.text((x,y+267),f'frame {n:03} / {n/30:5.2f}s',font=font,fill=(238,233,223))
im.save(here/'probe_sheet.png')
print(here/'probe_sheet.png')
