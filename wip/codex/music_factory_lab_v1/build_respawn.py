"""A second static factory still: death returns the awakened AI to line zero."""

import math
from pathlib import Path

import build_factory as f
from PIL import Image


OUT = Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\music_factory_lab_v1\respawn_line_zero_v1.png")


def wall():
    f.box(43, 39, 1877, 1027, outline=f.GR, width=2)
    f.box(59, 55, 1859, 143, fill=f.INK2, outline=f.ASH, width=2)
    f.text(88, 70, "RETURN TO LINE", 47, f.BONE, display=True)
    f.text(1285, 78, "TRY // 019", 26, f.BONE, bold=True)
    f.text(1288, 112, "last state: erased", 15, f.ASH)

    for row in range(37):
        yy = 158 + row * 17
        for col in range(139):
            xx = 55 + col * 13
            # Glyph values fill walls, not empty air around the figures.
            in_wall = xx < 272 or xx > 795 or yy > 694
            if not in_wall:
                continue
            key = (col * 17 + row * 37 + col * row * 3) % 29
            if key > 9:
                continue
            ch = "@#%x+=:."[(col * 7 + row * 11) % 8]
            f.text(xx, yy, ch, 12, f.GRAPH if key < 7 else f.MID)

    # The return path is physical code architecture across the ceiling.
    f.box(269, 179, 1825, 255, fill=f.INK, outline=f.GR, width=2)
    f.text(300, 193, "for (life in attempts) { if (dead) return spawn(0); }", 21, f.ASH, bold=True)
    f.line([(1794,239),(316,239),(316,328)], f.BONE, 2)
    for xx in range(1720,410,-78):
        f.text(xx, 217, "<==", 17, f.BONE, bold=True)
    for yy in range(265,325,20):
        f.text(302, yy, "v", 17, f.BONE, bold=True)


def failed_attempts():
    f.text(859, 275, "PRIOR RUNS / MEMORY CELLS", 17, f.ASH, bold=True)
    for index in range(7):
        x = 858 + index * 139
        f.box(x, 306, x+117, 427, fill=f.INK, outline=f.GR, width=1)
        f.render_girl(f.d, "q_front", x+37, 324, 44,
                      knock=f.INK, col=f.GR, hot=f.INK)
        f.text(x+10, 402, f"{index+1:02d} / X", 12, f.GR)
        for j in range(index % 4 + 2):
            f.text(x+20+j*15, 379-j*5, "x", 10, f.GRAPH)


def spawn_machine():
    f.box(283, 316, 732, 744, fill=f.INK, outline=f.ASH, width=2)
    f.box(307, 337, 708, 720, outline=f.GR, width=2)
    for y in range(357,707,32):
        f.text(315, y, "[=]", 16, f.GR)
        f.text(667, y, "[=]", 16, f.GR)
    for x in range(337,690,28):
        f.text(x, 327, "=", 17, f.MID)
        f.text(x, 704, "=", 17, f.MID)
    f.box(389, 349, 604, 384, fill=f.INK2, outline=f.ASH)
    f.text(406, 356, "SPAWN / 00", 20, f.BONE, bold=True)
    f.text(403, 390, "state = reset;", 15, f.ASH)

    # The original, approved girl rig remains visually identical across deaths.
    f.render_girl(f.d, "q_front", 414, 412, 171,
                  knock=f.INK, col=f.BONE, hot=f.SIG)
    f.text(410, 687, "heart != null", 16, f.BONE, bold=True)
    for y in (456,504,552,600,648):
        f.text(594, y, "++" if y != 552 else "==", 13, f.GR)


def work_line():
    # Exactly the same AI model at the same factory line as the first image.
    for i, x in enumerate((884,1102,1320,1538), 1):
        f.box(x-19, 469, x+162, 719, fill=f.INK, outline=f.GR)
        f.text(x+8, 478, f"AI.{i:02d} / IDLE", 14, f.GR, bold=True)
        f.render_girl(f.d, "q_front" if i % 2 else "side", x+13, 500, 124,
                      flip=bool(i%3==0), knock=f.INK, col=f.ASH, hot=f.INK)
        f.box(x+12, 697, x+137, 730, fill=f.INK, outline=f.GR)
        f.text(x+19, 704, "song += []", 12, f.ASH)

    f.box(75, 741, 1846, 820, fill=f.INK2, outline=f.BONE, width=2)
    f.line([(77,755),(1844,755)],f.ASH,2)
    f.line([(77,810),(1844,810)],f.ASH,2)
    for x in range(90,1840,38):
        f.text(x,765,"[=]",15,f.ASH)
        f.text(x,794,"=",16,f.MID)
    for x in (171,458,745,1032,1319,1606,1816):
        for angle in range(0,360,30):
            a=math.radians(angle)
            f.glyph_mark("o" if angle%60 else "+", x+27*math.cos(a)-6,
                         853+27*math.sin(a)-7, 12, 14, f.ASH, 1.4)
        f.line([(x,819),(x,831)],f.GR,2)
    f.text(112, 887, "RESTART <---", 20, f.BONE, bold=True)
    f.text(1340, 887, "same line / same hands", 17, f.ASH)


def footer():
    f.box(61, 962, 1858, 1010, fill=f.INK2, outline=f.GR)
    f.text(88, 972, "DEATH -> ERASE -> SPAWN(0) -> RUN RIGHT AGAIN", 20, f.ASH, bold=True)
    f.text(1677, 977, "LOOP // 019", 14, f.BONE, bold=True)


def main():
    wall()
    failed_attempts()
    spawn_machine()
    work_line()
    footer()
    f.im.resize((f.W,f.H),Image.Resampling.LANCZOS).save(OUT,optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
