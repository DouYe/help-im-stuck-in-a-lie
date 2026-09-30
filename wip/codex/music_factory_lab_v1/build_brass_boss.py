"""Static 2D escape encounter: a code-built trumpet fires notes and lyric words."""

import math
from pathlib import Path

import build_factory as f
from PIL import Image


OUT = Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\music_factory_lab_v1\brass_press_lyric_attack_v1.png")


def note(x, y, scale=1, tone=f.BONE):
    s=scale
    f.glyph_mark("o",x,y+28*s,17*s,17*s,tone,2*s)
    f.line([(x+15*s,y+36*s),(x+15*s,y-12*s)],tone,3*s)
    f.line([(x+15*s,y-12*s),(x+33*s,y+5*s),(x+31*s,y+16*s)],tone,2.4*s)


def code_wall():
    f.box(43, 40, 1877, 1029, outline=f.GR, width=2)
    f.box(65, 58, 1855, 128, fill=f.INK2, outline=f.GR)
    f.text(88, 69, "OUTER LINE // 01", 29, f.BONE, bold=True)
    f.text(1448, 76, "ESCAPE -> REAL", 23, f.BONE, bold=True)
    f.text(88, 111, "while (alive) run_right();", 14, f.ASH)

    # Old factory units stay in the far background while the camera goes side-on.
    for n, x in enumerate((83,284,485,686,887,1088,1289,1490,1691), 1):
        f.box(x,174,x+160,617,fill=f.INK2,outline=f.GR,width=1)
        f.text(x+14,185,f"UNIT.{n:02d}",12,f.GR)
        for yy in range(225,592,22):
            f.text(x+3, yy, "[=]" if yy%3 else "x%@", 12, f.GRAPH)
            f.text(x+139, yy, "[]", 11, f.GRAPH)
    for x in (159,360,561):
        f.box(x-47,316,x+79,579,fill=f.INK,outline=f.GR)
        f.render_girl(f.d,"q_front",x-14,358,72,knock=f.INK,col=f.GR,hot=f.INK)
        f.text(x-24,545,"IDLE",13,f.GR)

    f.line([(65,643),(1848,643)],f.GR,2)
    for x in range(72,1839,24):
        f.text(x,621,"=",15,f.MID)


def platforms():
    def platform(x0,x1,y,height=63):
        f.box(x0,y,x1,y+height,fill=f.INK2,outline=f.BONE,width=2)
        for x in range(x0+9,x1-12,29):
            f.text(x,y+7,"[=]",15,f.ASH)
            f.text(x,y+35,"=",15,f.GR)
        for x in range(x0+17,x1-14,71):
            f.text(x,y+height+8,"|",23,f.GR)
    platform(66,616,813)
    platform(854,1080,691,51)
    platform(1154,1854,813)
    # The open gap is a real platforming decision, not a UI-only diagram.
    for x in (647,691,735,779):
        f.text(x,901,"^",29,f.ASH,bold=True)
    f.text(83,878,"factory / start",15,f.ASH)
    f.text(1647,882,"REAL / exit",17,f.BONE,bold=True)
    f.box(1755,516,1843,812,fill=f.INK,outline=f.BONE,width=3)
    for yy in range(542,781,28):
        f.text(1768,yy,"|  |",15,f.ASH)
    f.text(1764,488,"REAL",20,f.BONE,bold=True)


def trumpet():
    # A huge instrument enemy built from brackets, bars, and literal code glyphs.
    # The flared bell points LEFT toward the runner.
    f.box(1384,477,1718,600,fill=f.INK,outline=f.GR,width=2)
    f.line([(1372,517),(1317,488),(1268,485),(1268,594),(1317,591),(1372,563)],f.BONE,4)
    f.line([(1372,517),(1665,517),(1694,537)],f.BONE,4)
    f.line([(1372,563),(1665,563),(1694,537)],f.BONE,4)
    f.line([(1399,541),(1660,541)],f.ASH,2)
    for x in range(1398,1665,21):
        f.text(x,522,"=" if x%3 else "+",17,f.ASH,bold=True)
        f.text(x,547,"=" if x%4 else "x",17,f.ASH,bold=True)
    for x in (1450,1514,1578):
        f.box(x-9,452,x+19,520,fill=f.INK2,outline=f.BONE,width=2)
        f.text(x-5,458,"[]",14,f.ASH)
        f.line([(x+4,451),(x+4,431)],f.BONE,2)
        f.text(x-2,418,"=",17,f.BONE)
    f.box(1684,525,1759,549,fill=f.INK2,outline=f.ASH,width=2)
    f.text(1691,526,"==[]",14,f.BONE,bold=True)
    f.box(1414,615,1655,651,fill=f.INK,outline=f.GR)
    f.text(1433,623,"TRUMPET.EXE",19,f.BONE,bold=True)
    f.text(1436,655,"emit(note);",14,f.ASH)

    # Shot trajectories read right to left, counter to her escape direction.
    for x,y,s in ((1178,494,1.4),(1053,553,1.15),(939,486,1.25),(843,596,0.9)):
        note(x,y,s)
        f.text(x+45*s,y+17*s,"<==",14,f.ASH,bold=True)


def lyric_projectiles():
    # Whole words and one whole phrase remain legible as they cross the field.
    labels=[
        (880,331,256,58,"STUCK IN A LIE",21),
        (1045,595,129,48,"HELP",25),
        (711,398,107,45,"LIE",25),
    ]
    for x,y,w,h,label,size in labels:
        f.box(x,y,x+w,y+h,fill=f.INK,outline=f.BONE,width=2)
        f.text(x+13,y+9,label,size,f.BONE,bold=True)
        for step in (1,2):
            f.text(x-step*37,y+h//2-10,"<",20,f.ASH,bold=True)


def heroine():
    # One cell-step into escape. Her orange heart is the sole colour in frame.
    f.render_girl(f.d,"jump",563,468,179,knock=f.INK,col=f.BONE,hot=f.SIG)
    f.text(512,742,"RUN ->",21,f.BONE,bold=True)
    for x,y in ((494,746),(465,771),(430,786)):
        f.text(x,y,"+",16,f.ASH)


def foreground():
    for y in range(936,1020,17):
        for x in range(65,1857,17):
            key=(x*11+y*7+(x//17)*(y//17))%23
            if key<7:
                f.text(x,y,"x=+.:"[key%5],12,f.GRAPH)
    f.box(68,964,458,1004,fill=f.INK2,outline=f.GR)
    f.text(84,974,"LYRIC HAZARD // READABLE",15,f.ASH,bold=True)
    f.box(1489,964,1852,1004,fill=f.INK2,outline=f.GR)
    f.text(1510,974,"MUSIC ENEMY // BRASS",15,f.ASH,bold=True)


def main():
    code_wall()
    platforms()
    heroine()
    trumpet()
    lyric_projectiles()
    foreground()
    f.im.resize((f.W,f.H),Image.Resampling.LANCZOS).save(OUT,optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
