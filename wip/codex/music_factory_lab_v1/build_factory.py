"""A static, orthographic code-world music factory study for Hon.

This makes one new still. It reuses the approved bold symbol-girl renderer;
it does not modify the rig, existing selected references, or video engine.
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(PROJECT / "design/character/src"))
from final_sheet import ASH, BONE, GR, INK, SIG, SS, glyph, render as render_girl  # noqa: E402


W, H = 1920, 1080
INK2 = (22, 22, 24)
GRAPH = (43, 42, 42)
MID = (70, 68, 67)
FONT_ROOT = PROJECT / "app/public/fonts"
OUT = PROJECT / "wip/codex/music_factory_lab_v1/factory_lab_draft_v2.png"

im = Image.new("RGB", (W * SS, H * SS), INK)
d = ImageDraw.Draw(im)


def pt(x, y):
    return (round(x * SS), round(y * SS))


def line(points, fill=ASH, width=1):
    d.line([pt(x, y) for x, y in points], fill=fill, width=max(1, round(width * SS)), joint="curve")


def box(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle((*pt(x0, y0), *pt(x1, y1)), fill=fill, outline=outline, width=max(1, round(width * SS)))


def oval(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.ellipse((*pt(x0, y0), *pt(x1, y1)), fill=fill, outline=outline, width=max(1, round(width * SS)))


@lru_cache(maxsize=40)
def fnt(size, bold=False, display=False):
    if display:
        path = FONT_ROOT / "Archivo-w1250-900.ttf"
    else:
        path = FONT_ROOT / "src" / ("IBMPlexMono-Bold.ttf" if bold else "IBMPlexMono-Regular.ttf")
    return ImageFont.truetype(str(path), size * SS)


def text(x, y, value, size=16, fill=ASH, bold=False, display=False, anchor=None):
    d.text(pt(x, y), value, font=fnt(size, bold, display), fill=fill, anchor=anchor)


def glyph_mark(char, x, y, cw=11, ch=14, fill=ASH, lw=1.5):
    glyph(d, char, x, y, cw, ch, fill, lw)


def ascii_wall():
    """Value shading appears only where the wall or supports physically exist."""
    # First and last bays, pillars, and a low wall: S5-like glyph brushwork.
    for col in range(0, 145):
        x = 47 + col * 12.8
        for row in range(0, 29):
            y = 160 + row * 16
            pillar = min(abs(x - p) for p in (54, 354, 654, 954, 1254, 1554, 1854))
            low_wall = y > 500
            if not (pillar < 34 or low_wall):
                continue
            # Every other tile is open air, leaving the monitors and people readable.
            key = (col * 37 + row * 19 + col * row * 7) % 17
            if key > (11 if pillar < 27 else 5):
                continue
            ch = "@#%xx+=:."[(col * 5 + row * 3) % 9]
            tone = GRAPH if key < 12 else MID
            text(x, y, ch, 12, tone)

    # The floor is a coding surface rather than a flat grey slab.
    for row in range(14):
        y = 853 + row * 17
        for col in range(137):
            x = 44 + col * 13.4
            key = (col * 13 + row * 29 + (col // 5) * 7) % 19
            if key > 9:
                continue
            ch = ".:+==x%#"[(col * 3 + row * 5) % 8]
            text(x, y, ch, 12, GRAPH if row < 6 else (36, 35, 35))


def structural_shell():
    box(44, 37, 1875, 1026, outline=GR, width=2)
    box(62, 52, 1856, 134, fill=INK2, outline=ASH, width=2)
    for x in range(82, 1846, 29):
        text(x, 139, "=", 19, MID, bold=True)
    text(87, 66, "MUSIC FACTORY", 48, BONE, display=True)
    text(1335, 80, "LAB // 07", 24, ASH, bold=True)
    text(1335, 110, "ONE LINE : MANY HANDS", 15, GR)

    # Orthographic modules: no vanishing point; all workers share one plane.
    box(62, 174, 1856, 651, fill=INK2, outline=GR, width=2)
    for i in range(7):
        x = 64 + i * 298.5
        box(x, 172, x + 24, 650, fill=GRAPH, outline=GR, width=1)
        for yy in range(193, 638, 36):
            text(x + 4, yy, "[]", 13, MID)
    box(62, 651, 1856, 834, fill=INK, outline=ASH, width=2)
    line([(62, 845), (1856, 845)], GR, 2)
    line([(62, 857), (1856, 857)], GRAPH, 3)
    for x in range(78, 1850, 72):
        text(x, 830, "+==+", 12, GR)

    # Overhead waveform bus feeds every station.
    line([(92, 192), (1822, 192)], ASH, 2)
    line([(92, 215), (1822, 215)], GR, 1)
    for x in range(92, 1810, 37):
        text(x, 181, "=" if (x // 37) % 5 else "+", 19, MID)
    for x in (224, 512, 800, 1088, 1376, 1664):
        line([(x, 193), (x, 253)], GR, 2)
        text(x - 7, 217, "|", 20, ASH)


def monitor(x, index, title, expression):
    y = 258
    box(x, y, x + 240, y + 144, fill=INK, outline=ASH, width=2)
    box(x + 8, y + 8, x + 232, y + 136, outline=GRAPH, width=1)
    text(x + 16, y + 16, f"{index:02d} / {title}", 18, BONE, bold=True)
    text(x + 17, y + 47, expression, 13, ASH)
    # Each screen shows a different audible operation, rather than random code.
    for j in range(22):
        cx = x + 18 + j * 9.6
        if index == 1:
            level = [1, 1, 4, 1, 1, 7, 1, 1][j % 8]
        elif index == 2:
            level = 4 + 3 * math.sin(j * 0.74)
        elif index == 3:
            level = [2, 4, 7, 3, 6, 2, 5][j % 7]
        elif index == 4:
            level = 3 + 4 * abs(math.sin(j * 0.4) * math.cos(j * 0.12))
        elif index == 5:
            level = 2 + 5 * abs(math.sin(j * 0.72))
        else:
            level = 6 if j in (2, 6, 10, 14, 18) else 2
        top = y + 119 - level * 5
        for yy in range(int(top), y + 119, 9):
            text(cx, yy, "|", 12, ASH if j % 3 else BONE)
    text(x + 17, y + 121, "[]==[]==[]==[]==[]", 11, MID)
    line([(x + 120, y + 144), (x + 120, 455)], GR, 2)
    box(x + 76, 443, x + 164, 455, fill=GRAPH, outline=GR)


def draw_monitors():
    stations = [
        (91, 1, "INPUT", "read(prompt);") ,
        (382, 2, "BEAT", "quantize(time);") ,
        (673, 3, "TUNE", "fold(melody);") ,
        (964, 4, "VOICE", "humanize(take);") ,
        (1255, 5, "MIX", "sum(tracks);") ,
        (1546, 6, "EXPORT", "return song;") ,
    ]
    for args in stations:
        monitor(*args)


def draw_worker(cx, top, scale, variant, facing=1, tone=ASH):
    """A set of distinct small lab coworkers made from simple symbol strokes."""
    s = scale
    x, y = cx, top
    head_y = y + 31 * s
    # Face and hair have different code-built silhouettes by station.
    # Faces are octagonal stroke cells: / - \\ | glyph language, never smooth portraits.
    head = [
        (x-13*s,head_y-27*s),(x+13*s,head_y-27*s),
        (x+23*s,head_y-17*s),(x+23*s,head_y+17*s),
        (x+13*s,head_y+28*s),(x-13*s,head_y+28*s),
        (x-23*s,head_y+17*s),(x-23*s,head_y-17*s),
        (x-13*s,head_y-27*s),
    ]
    d.polygon([pt(*p) for p in head], fill=INK)
    line(head, tone, 2.2*s)
    if variant == 0:  # cap
        line([(x - 26*s,y+17*s),(x-15*s,y+2*s),(x+18*s,y+2*s),(x+28*s,y+17*s)], tone, 3*s)
        line([(x-29*s,y+18*s),(x+32*s,y+18*s)], tone, 3*s)
    elif variant == 1:  # bun
        oval(x-35*s,y+8*s,x-19*s,y+24*s,outline=tone,width=2*s)
        for off in (-17,-5,7,19):
            glyph_mark("/" if off < 0 else "\\", x+off*s, y+5*s, 11*s, 12*s, tone, 1.5*s)
    elif variant == 2:  # goggles
        line([(x-20*s,y+29*s),(x+20*s,y+29*s)], tone, 2*s)
        box(x-19*s,y+33*s,x-3*s,y+43*s,outline=tone,width=2*s)
        box(x+3*s,y+33*s,x+19*s,y+43*s,outline=tone,width=2*s)
    elif variant == 3:  # headphones
        line([(x-27*s,y+41*s),(x-27*s,y+17*s),(x-15*s,y+2*s),(x+15*s,y+2*s),(x+27*s,y+17*s),(x+27*s,y+41*s)], tone, 2*s)
        box(x-31*s,y+33*s,x-22*s,y+49*s,fill=INK,outline=tone,width=2*s)
        box(x+22*s,y+33*s,x+31*s,y+49*s,fill=INK,outline=tone,width=2*s)
    elif variant == 4:  # cropped hair
        for off in range(-18,19,9):
            text(x+off*s, y+1*s, "x", max(9,int(13*s)), tone)
    elif variant == 5:  # hood
        line([(x-32*s,y+56*s),(x-32*s,y+17*s),(x-18*s,y-2*s),(x+18*s,y-2*s),(x+32*s,y+17*s),(x+32*s,y+56*s)], tone, 2.4*s)
    else:  # side sweep
        line([(x-20*s,y+11*s),(x-5*s,y+1*s),(x+20*s,y+8*s),(x+27*s,y+24*s)], tone, 2.4*s)
        line([(x+19*s,y+11*s),(x-14*s,y+19*s)], tone, 2*s)

    # Eyes / nose remain simple at this scale.
    if variant != 2:
        glyph_mark("o", x-14*s, y+30*s, 8*s, 9*s, tone, 1.2*s)
        glyph_mark("o", x+6*s, y+30*s, 8*s, 9*s, tone, 1.2*s)
    line([(x-4*s,y+54*s),(x+6*s,y+54*s)], tone, 1.4*s)

    # All are working at the *same* conveyor; their hands aim to a shared rail.
    shoulders = y + 68*s
    coat_bottom = y + 159*s
    body = [(x-34*s,shoulders),(x+34*s,shoulders),(x+43*s,coat_bottom),(x-43*s,coat_bottom)]
    d.polygon([pt(*p) for p in body], fill=INK, outline=tone, width=max(1,round(2*s*SS)))
    line([(x,shoulders+5*s),(x,coat_bottom-4*s)], GR, 1.4*s)
    text(x-23*s, shoulders+39*s, "[ ]", max(9,int(14*s)), GR)
    for yy in (shoulders+31*s, shoulders+54*s, shoulders+77*s):
        glyph_mark("+", x+12*s, yy, 6*s, 8*s, tone, 1.2*s)

    hand_y = y + 132*s
    hand_x = x + facing*60*s
    arm_path = [(x+facing*30*s,shoulders+8*s),(x+facing*51*s,shoulders+40*s),(hand_x,hand_y)]
    line(arm_path, tone, 3.2*s)
    line([(x-facing*30*s,shoulders+9*s),(x-facing*49*s,shoulders+54*s),(x-facing*30*s,hand_y+4*s)], tone, 2.7*s)
    glyph_mark("+", hand_x-5*s, hand_y-5*s, 10*s, 10*s, tone, 1.8*s)
    # Legs / boots are partly masked by the belt fascia, like a side-view game.
    foot_y = y + 216*s
    for dx in (-17*s,17*s):
        line([(x+dx,coat_bottom),(x+dx,foot_y)],tone,2.4*s)
        line([(x+dx-9*s,foot_y),(x+dx+11*s,foot_y)],tone,2.4*s)


def draw_workers():
    workers = [
        (145, 496, 1.00, 0, +1, GR),
        (300, 483, 1.07, 2, -1, ASH),
        (456, 509, 0.94, 1, +1, GR),
        (616, 486, 1.05, 3, -1, ASH),
        (1049, 493, 1.04, 4, +1, ASH),
        (1213, 502, 0.97, 5, -1, GR),
        (1370, 484, 1.07, 6, +1, ASH),
        (1530, 511, 0.93, 2, -1, GR),
        (1685, 490, 1.02, 1, +1, ASH),
        (1818, 511, 0.88, 0, -1, GR),
    ]
    for worker in workers:
        draw_worker(*worker)

    # The locked protagonist is the largest worker, with the only orange.
    # Her own glyph-rig and bold knockout distinguish her from other employees.
    box(767, 467, 969, 727, fill=INK, outline=GR, width=1)
    for yy in range(479, 716, 21):
        text(780, yy, ":=+" if yy % 2 else "x@%", 13, GRAPH)
    render_girl(d, "q_front", 792, 451, 152, knock=INK, col=BONE, hot=SIG)
    # A working arm joins the same rail as everyone else's, without changing her rig.
    line([(927, 595), (954, 612), (973, 623)], BONE, 3)
    glyph_mark("+", 967, 615, 11, 13, BONE, 2.2)
    box(796, 438, 944, 462, fill=INK, outline=GR)
    text(808, 440, "WORKER // ?", 15, BONE, bold=True)


def product_cards():
    # Progression is legible left to right: prompt -> beat -> tune -> voice -> mix -> song.
    box(111, 633, 209, 693, fill=INK, outline=ASH, width=2)
    text(124, 643, "PROMPT", 14, BONE, bold=True)
    text(126, 668, "[0101]", 12, ASH)

    box(368, 641, 515, 698, fill=INK, outline=ASH, width=2)
    text(386, 649, "BEAT GRID", 13, BONE, bold=True)
    for j, height in enumerate((7,15,7,7,19,7,12,7,7,19,7)):
        line([(385+j*11,687),(385+j*11,687-height)],ASH,2)

    box(660, 634, 781, 699, fill=INK, outline=ASH, width=2)
    text(672, 645, "TUNE", 14, BONE, bold=True)
    line([(675,681),(689,669),(703,681),(717,658),(731,681),(745,671),(761,681)],ASH,2)

    box(982, 634, 1110, 700, fill=INK, outline=BONE, width=2)
    text(997, 644, "VOICE", 15, BONE, bold=True)
    for x in range(996,1096,9):
        height=8+int(13*abs(math.sin(x*0.17)))
        line([(x,686-height),(x,686)],ASH,2)

    box(1275, 635, 1415, 700, fill=INK, outline=ASH, width=2)
    text(1290, 645, "MIX [4]", 15, BONE, bold=True)
    for j in range(4):
        y=666+j*8
        text(1291,y,"=+=+=+=+=+=",11,ASH)

    box(1603, 626, 1787, 704, fill=INK, outline=BONE, width=2)
    text(1620, 637, "SONG.WAV", 19, BONE, bold=True)
    text(1621, 668, "return song;", 13, ASH)
    for x in (1578,1798):
        text(x, 652, ">", 21, ASH, bold=True)


def conveyor():
    # One unbroken assembly line. The stations attach to a common mechanical bus.
    box(74, 690, 1846, 765, fill=INK2, outline=BONE, width=2)
    line([(77,703),(1843,703)],ASH,2)
    line([(78,728),(1842,728)],GR,2)
    line([(78,757),(1842,757)],ASH,2)
    for x in range(84,1840,38):
        text(x, 712, "[=]", 15, ASH)
        text(x, 741, "=", 16, MID, bold=True)
    for x in (95, 380, 667, 954, 1241, 1528, 1824):
        box(x-31,777,x+31,837,fill=INK,outline=GRAPH,width=1)
        for angle in range(0,360,30):
            a=math.radians(angle)
            glyph_mark("o" if angle%60 else "+", x+24*math.cos(a)-6, 807+24*math.sin(a)-7, 12, 14, ASH, 1.4)
        for angle in range(0,360,90):
            a=math.radians(angle)
            line([(x+4*math.cos(a),807+4*math.sin(a)),(x+17*math.cos(a),807+17*math.sin(a))],GR,2)
        line([(x,765),(x,778)],ASH,2)
    for x in (210, 555, 900, 1245, 1590):
        line([(x,764),(x,855)],GR,3)
        text(x-11,828,"||",14,GR)

    # The belt is literally executable syntax. Symbols also define its rails.
    text(97, 795, "while (beat) { assemble(song); }", 15, ASH)
    text(1509, 795, "OUTPUT >>", 15, BONE, bold=True)


def footer():
    # Ordered deep-floor machinery, not unrelated noise.
    line([(68, 951), (1854, 951)], GR, 1)
    for x in range(76, 1847, 99):
        text(x, 872, "[====]", 14, GR)
        line([(x+13,900),(x+13,949)],GRAPH,2)
        text(x+29,916,"x+",12,GRAPH)
    box(62, 973, 1856, 1011, fill=INK2, outline=GR)
    text(86, 981, "IN  : prompt    /    PROCESS : rhythm + voice    /    OUT : song", 18, ASH, bold=True)
    text(1702, 983, "LINE // 01", 15, BONE, bold=True)


def main():
    ascii_wall()
    structural_shell()
    draw_monitors()
    draw_workers()
    product_cards()
    conveyor()
    footer()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.resize((W,H), Image.Resampling.LANCZOS).save(OUT, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
