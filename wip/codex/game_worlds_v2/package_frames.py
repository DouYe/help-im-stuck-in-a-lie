"""Copy reviewed proposals to the shared design folder and make selection boards."""
from pathlib import Path
import json
import shutil
import sys
sys.path.insert(0,str(Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\visual_audit\lib")))
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(r"D:\Videos\Help! I'm stuck in a LIE")
WIP=ROOT/"wip/codex/game_worlds_v2"
DESIGN=ROOT/"design/keyframes/codex_game_worlds_v2"
USER=Path(r"C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs\help_stuck_lie_game_worlds_v2")
SPEC=[
    ("01",42.012,"CAVERN / side-scroller","Parallax bridge and ruins; painterly symbols","cavern/KF06_HELP_cavern_game.png"),
    ("02",46.858,"CONTROL FLOW / tactics","Inverted maze with playable if / else routes","tactical/tactical_false_routes_46_858.png"),
    ("03",48.300,"INDENT / HD-2D diorama","Oblique code terraces with deep ASCII planes","diorama/KF09_make-me-real_code-diorama.png"),
    ("04",50.533,"SYNTAX LOCK / boss puzzle","Perspective gate made from code branches","syntax_lock/KF10_real_this_time_syntax_lock.png"),
    ("05",54.126,"HELP() / bullet hell","Punctuation waves leave one safe path","arcade/KF11_HELP_code_bullet_hell.png"),
    ("06",55.148,"GRAVITY / folding puzzle","ASCII paper rooms rotate through 90 degrees","paper/KF_55p15_stuck_paper_gravity_ASCII.png"),
    ("07",58.974,"HEART / painted chamber","Mechanical space; the approved symbol heart","chamber/KF12_HEART_painted_chamber.png"),
    ("08",61.402,"MEMORY VAULT / text adventure","Close heroine in an ASCII depth chamber","heart_close/KF13_heart_inside_ascii_vault.png"),
]
ALT=("07B",58.974,"HEART / ASCII chamber","Same room rebuilt entirely from glyph values","chamber/KF12_HEART_ascii_chamber.png")

fontdir=ROOT/"app/public/fonts"
def font(name,size): return ImageFont.truetype(str(fontdir/name),size)
F_TITLE=font("Archivo-w1250-900.ttf",42)
F_CARD=font("Archivo-w1250-900.ttf",30)
F_MONO=font("src/IBMPlexMono-Regular.ttf",19)
INK=(10,10,11); BONE=(238,233,223); ASH=(156,151,143); GR=(94,91,87)

for directory in (DESIGN,USER): directory.mkdir(parents=True,exist_ok=True)
records=[]
for num,t,title,desc,relative in SPEC+[ALT]:
    source=WIP/relative
    if not source.is_file(): raise FileNotFoundError(source)
    with Image.open(source) as check:
        if check.width/check.height < 1.70 or check.width/check.height > 1.85:
            raise ValueError((source,check.size))
    dest=f"{num}_{Path(relative).name}"
    for directory in (DESIGN,USER):
        with Image.open(source) as im:
            if im.size == (1920,1080): shutil.copy2(source,directory/dest)
            else: im.convert("RGB").resize((1920,1080),Image.Resampling.LANCZOS).save(directory/dest)
    records.append(dict(id=num,time=t,title=title,description=desc,source=str(source),file=dest))

def card(d,canvas,rec,x,y,w=915,imgh=515):
    src=USER/rec["file"]
    with Image.open(src) as im:
        thumb=ImageOps.fit(im.convert("RGB"),(w,imgh),method=Image.Resampling.LANCZOS)
    canvas.paste(thumb,(x,y))
    d.rectangle((x,y,x+w,y+imgh),outline=GR,width=2)
    d.text((x,y+imgh+13),f"{rec['id']}   {rec['time']:.3f}s   {rec['title']}",font=F_CARD,fill=BONE)
    d.text((x,y+imgh+56),rec["description"],font=F_MONO,fill=ASH)

board=Image.new("RGB",(1920,2635),INK)
d=ImageDraw.Draw(board)
d.text((30,24),"EIGHT GAME WORLDS / ONE SYMBOL GIRL",font=F_TITLE,fill=BONE)
d.text((31,77),"Codex proposals for chorus 1   |   ASCII code as light, shadow and terrain   |   not yet selected",font=F_MONO,fill=ASH)
for i,rec in enumerate(records[:8]):
    col,row=i%2,i//2
    card(d,board,rec,30+col*945,132+row*618)
for directory in (DESIGN,USER): board.save(directory/"selection_sheet.png")

ab=Image.new("RGB",(1920,720),INK)
ad=ImageDraw.Draw(ab)
ad.text((30,22),"HEART CHAMBER / TWO TREATMENTS",font=F_TITLE,fill=BONE)
ad.text((31,74),"Painted mechanical space (07) and the same space translated into visible ASCII (07B)",font=F_MONO,fill=ASH)
for i,rec in enumerate((records[6],records[8])): card(ad,ab,rec,30+i*945,123)
for directory in (DESIGN,USER): ab.save(directory/"chamber_A_B.png")

for directory in (DESIGN,USER):
    (directory/"frames.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
print("packaged",len(records),"frames into",DESIGN,"and",USER)
