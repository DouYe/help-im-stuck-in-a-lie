"""Original bone-white tactical maze keyframe at 46.858 s.

All visible architecture and tactical marks are assembled from symbols. The
approved bold 17x27 glyph-girl rig is imported, not redrawn.
"""
from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "wip/codex/visual_audit/lib"))
sys.path.insert(0, str(ROOT / "design/character/src"))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import render as render_girl, SS

W, H = 1920, 1080
INK = (10, 10, 11)
DEEP = (22, 22, 24)
GREY = (94, 91, 87)
ASH = (156, 151, 143)
BONE = (238, 233, 223)
ORANGE = (255, 83, 20)
FONTS = ROOT / "app/public/fonts"

im = Image.new("RGB", (W * SS, H * SS), BONE)
d = ImageDraw.Draw(im)
random.seed(461)


def font(size: int, bold=False, wide=False):
    if wide:
        p = FONTS / ("Archivo-w1250-900.ttf" if bold else "Archivo-w1250-500.ttf")
    else:
        p = FONTS / "src" / ("IBMPlexMono-Bold.ttf" if bold else "IBMPlexMono-Regular.ttf")
    return ImageFont.truetype(str(p), size * SS)


def box(x0, y0, x1, y1, fill, outline=None, width=1):
    d.rectangle((x0*SS,y0*SS,x1*SS,y1*SS), fill=fill,
                outline=outline, width=max(1,width*SS))


def line(points, fill, width=1):
    d.line([(x*SS,y*SS) for x,y in points], fill=fill, width=max(1,width*SS), joint="curve")


def poly(points, fill, outline=None, width=1):
    d.polygon([(x*SS,y*SS) for x,y in points], fill=fill)
    if outline:
        p2=points+[points[0]]
        line(p2,outline,width)


def label(x,y,s,size=18,color=INK,bold=False,wide=False,anchor=None):
    d.text((x*SS,y*SS),s,font=font(size,bold,wide),fill=color,anchor=anchor,
           stroke_width=0)


def code_label(x,y,s,size=18,color=INK,back=BONE,bold=True):
    f=font(size,bold)
    bounds=d.textbbox((0,0),s,font=f)
    ww=math.ceil((bounds[2]-bounds[0])/SS)
    hh=math.ceil((bounds[3]-bounds[1])/SS)
    box(x-5,y-2,x+ww+7,y+hh+8,back)
    label(x,y,s,size,color,bold)


def glyph_segment(x0,y0,x1,y1,color=INK,size=18,step=11):
    dist=math.hypot(x1-x0,y1-y0)
    if dist==0: return
    ang=math.atan2(y1-y0,x1-x0)
    ach=abs(math.cos(ang)); ash=abs(math.sin(ang))
    ch='-' if ach>0.84 else '|' if ash>0.84 else ('/' if (x1-x0)*(y1-y0)<0 else '\\')
    n=max(1,int(dist/step))
    for i in range(n+1):
        u=i/n
        label(x0+(x1-x0)*u,y0+(y1-y0)*u,ch,size,color)


def glyph_border(x0,y0,x1,y1,color=INK,size=19,step=11):
    for xa,ya,xb,yb in ((x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)):
        glyph_segment(xa,ya,xb,yb,color,size,step)
    for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1)):
        label(x,y,'+',size+1,color)


# An inverted, orthographic game surface. The map substrate itself is a
# low-contrast character field, as if empty memory were being displayed.
for y in range(138,1036,18):
    for x in range(346,1890,13):
        r=random.random()
        if r < .43:
            label(x,y,'.' if r<.24 else '+' if r<.35 else '=',10,ASH)

# Dense black control strip, almost like a monochrome handheld tactics RPG.
box(0,0,313,H,INK)
for x in range(319,1920,18):
    label(x,88,'-',16,GREY)
label(38,30,'TURN // 09',19,BONE,True)
label(38,78,'STUCK',50,BONE,True,True)
label(38,139,'IN A LIE',43,BONE,True,True)
label(39,216,'UNIT 01',18,ASH,True)
label(39,250,'girl.x   : 07',16,BONE)
label(39,281,'girl.y   : 11',16,BONE)
label(39,312,'exit()   : null',16,BONE)
glyph_border(32,355,280,509,GREY,14,12)
label(50,378,'CALL STACK',17,BONE,True)
label(50,415,'if truth:   X',17,ASH)
label(50,442,'while stuck: loop',15,ASH)
label(50,469,'else: lie()',17,BONE,True)
label(39,561,'COMMAND',17,ASH,True)
for i,(key,cmd) in enumerate((('>','MOVE'),('>','LOOK'),('>','WAIT'),('>','AGAIN'))):
    yy=607+i*54
    label(39,yy,key,24,BONE,True)
    label(73,yy,cmd,25,BONE,i==0)
    glyph_segment(45,yy+37,270,yy+37,GREY,12,12)
label(39,1002,'return: LIE',16,BONE,True)
label(1685,41,'46.858  /  BEAT 01',19,INK,True)
label(360,39,'FLOOR 03 : CONTROL FLOW',20,INK,True)


def slab(x0,y0,x1,y1,z=2,tone=BONE,seed=0):
    """Hard stepped elevation; top and side contain printed glyph texture."""
    drop={1:14,2:24,3:35,4:48}[z]
    # The side is a slab of repeating pipe glyphs, with a hard offset shadow.
    box(x0+8,y0+drop+7,x1+9,y1+drop+8,GREY)
    box(x0,y0+drop,x1,y1+drop,INK)
    box(x0,y0,x1,y1,BONE)
    rng=random.Random(seed)
    # The high-value tonal planes are rasterized from real printable code
    # glyphs, not vector hatching. x/@/% make the shadow density; +=. are
    # sparse air. This is the material of the rooms.
    paint = GREY if tone==BONE else INK
    xstep,ystep,fs=(13,18,12) if tone==BONE else (11,16,13) if tone==ASH else (9,14,14)
    for yy in range(y0+17,y1-16,ystep):
        for xx in range(x0+13,x1-15,xstep):
            r=rng.random()
            if tone==DEEP:
                g = '@' if r<.40 else '#' if r<.70 else '%' if r<.88 else 'x'
            else:
                g = '@' if r<.25 else '%' if r<.45 else 'x' if r<.64 else '+' if r<.79 else '=' if r<.90 else '.'
            if tone==BONE and r>.76:
                continue
            label(xx,yy,g,fs,paint)
    for yy in range(y1+4,y1+drop-2,13):
        for xx in range(x0+6,x1-4,15):
            label(xx,yy,'|' if ((xx+yy)//15)%3 else '/',12,BONE)
    # Printed contour edges, deliberately made from glyphs rather than strokes.
    glyph_border(x0+1,y0+1,x1-7,y1-8,INK,18,12)
    for yy in range(y0+33,y1-30,34):
        for xx in range(x0+29,x1-24,46):
            r=rng.random()
            if r < .58: continue
            label(xx,yy,'{' if r<.68 else '}' if r<.78 else '[' if r<.88 else ';',15,GREY)
    # One extra contour rail on the taller plates.
    if z>=3:
        glyph_border(x0+18,y0+19,x1-25,y1-31,GREY,12,13)


# Draw distant modules first, then bridges, then the center plateau. Heights
# and hard shadow offsets form a real depth hierarchy without lighting effects.
slab(431,184,740,419,3,ASH,1)
slab(902,139,1294,329,2,BONE,2)
slab(1483,183,1816,422,1,BONE,3)
slab(412,737,734,946,1,BONE,4)
slab(1497,702,1823,929,2,ASH,5)


def bridge(x0,y0,x1,y1,vertical=False):
    box(x0+5,y0+14,x1+5,y1+14,INK)
    box(x0,y0,x1,y1,ASH)
    glyph_border(x0,y0,x1,y1,INK,13,9)
    if vertical:
        for yy in range(y0+19,y1-8,26):
            label(x0+8,yy,'===>',15,INK,True)
    else:
        for xx in range(x0+18,x1-9,27):
            label(xx,y0+8,'=>',14,INK,True)


bridge(734,298,865,351)
bridge(1043,323,1131,475,True)
bridge(1394,287,1485,345)
bridge(720,782,858,835)
bridge(1424,746,1502,823)

# High central island is matte ink. It absorbs the pale world around it, so
# the approved glyph girl remains clear without a separate magnification box.
slab(794,390,1448,861,4,DEEP,6)
for y in range(445,805,35):
    for x in range(848,1390,35):
        if random.random()<.64:
            label(x,y,random.choice(['{','}','/',';']),12,GREY)
glyph_border(854,455,1374,807,ASH,15,13)

# False selectable routes are all monochrome. Orange is reserved for the
# heroine's approved symbol heart.
def route(points, light=False):
    color=INK
    for a,b in zip(points,points[1:]):
        x0,y0=a; x1,y1=b
        dist=math.hypot(x1-x0,y1-y0)
        n=max(1,int(dist/31))
        horizontal=abs(x1-x0)>=abs(y1-y0)*1.4
        token='=>' if horizontal else '||' if abs(y1-y0)>=abs(x1-x0)*1.4 else '//'
        for k in range(1,n+1):
            u=k/n
            x=x0+(x1-x0)*u; y=y0+(y1-y0)*u
            code_label(x,y,token,13,color,BONE)
    for x,y in points[1:-1]: code_label(x-7,y-10,'+',19,color,BONE)

route([(1118,620),(1306,620),(1306,488),(1512,488),(1512,332)])
route([(1060,620),(925,620),(925,826),(659,826)],True)
route([(1135,635),(1260,735),(1610,735),(1610,793)])

# Architectural walls, gates, elevators and collapsed stairs are visibly
# glyph-based; they do not resemble the older LIE-outline maze shot.
for xx in range(484,709,29):
    for yy in range(242,398,26):
        if xx in (484,687) or yy in (242,372):
            label(xx,yy,'{' if xx<580 else '}',24,INK,True)
code_label(500,270,'if truth:',22,INK,ASH)
code_label(518,312,'EXIT = ?;',23,INK,ASH)
code_label(520,358,'// sealed',17,INK,ASH)

for xx in range(1530,1790,26):
    label(xx,232,'[',24,INK,True)
    label(xx,378,']',24,INK,True)
for yy in range(252,380,25):
    label(1522,yy,'[',24,INK,True)
    label(1777,yy,']',24,INK,True)
code_label(1555,280,'return EXIT',25,INK,BONE)
code_label(1560,338,'// unreachable',16,INK,BONE)
for yy in range(245,370,28):
    label(1444,yy,'!=',23,INK,True)

code_label(465,780,'while stuck:',21,INK,BONE)
code_label(465,834,'return start()',22,INK,BONE)
for xx in range(476,704,23):
    label(xx,890,'}',24,INK,True)

for xx in range(1545,1795,25):
    label(xx,763,'[',24,INK,True)
    label(xx,870,']',24,INK,True)
code_label(1551,783,'else:',24,INK,ASH)
code_label(1551,817,'lie();',37,INK,ASH)
code_label(1554,874,'// dead end',16,INK,ASH)

# Tactical wayfinding bits; all white/black, no orange HUD trail.
code_label(925,166,'try: escape()',17,INK,BONE)
code_label(969,236,'except Lie:',20,INK,BONE)
code_label(837,411,'def move():',15,BONE,DEEP)
code_label(1258,411,'else: LIE',15,BONE,DEEP)
code_label(862,837,'return start()',15,BONE,DEEP)
for x,y,c in ((815,605,'<'),(1396,605,'>'),(1115,414,'^'),(1115,824,'v')):
    label(x,y,c,35,BONE,True)

# Local hard shadow and exact shared-rig character, seen from above at 45deg.
for i in range(13):
    label(1002+i*14,737,'_',18,GREY)
render_girl(d,'q_front',1018,475,178,0.0,False,view='above',big=1.0,knock=DEEP)
code_label(995,771,'UNIT 01',18,BONE,DEEP)
code_label(1002,803,'PATH = null',14,ASH,DEEP)

# Boundary rhythm and registration marks retain a game screenshot feeling.
glyph_border(331,103,1895,1027,GREY,11,16)
for x,y in ((342,116),(1880,116),(342,1010),(1880,1010)):
    label(x,y,'+',23,INK,True)

out=im.resize((W,H),Image.Resampling.LANCZOS)
out.save(HERE/'tactical_false_routes_46_858.png')
print(HERE/'tactical_false_routes_46_858.png')
