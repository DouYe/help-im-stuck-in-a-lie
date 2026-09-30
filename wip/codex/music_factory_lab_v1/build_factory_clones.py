"""Revise the music factory so every worker is the same AI model.

The earlier varied-worker drafts remain untouched. Only the protagonist's
symbol heart is orange. Her factory peers have no visible heart.
"""

from pathlib import Path

import build_factory as f


def identical_ai_workers():
    peers = [
        (96, 482, 132, "side", False),
        (258, 482, 132, "q_front", False),
        (420, 482, 132, "side", True),
        (582, 482, 132, "q_front", True),
        (1002, 482, 132, "side", False),
        (1164, 482, 132, "q_front", False),
        (1326, 482, 132, "side", True),
        (1488, 482, 132, "q_front", True),
        (1650, 482, 132, "side", False),
    ]
    for index, (x, y, width, pose, flip) in enumerate(peers, 1):
        f.render_girl(f.d, pose, x, y, width, flip=flip,
                      knock=f.INK, col=f.ASH if index % 2 else f.GR, hot=f.INK)
        f.text(x + 22, 673, f"AI.{index:02d}", 11, f.MID)

    # The awakening is visible in one small, non-repeatable difference.
    f.box(773, 463, 954, 716, fill=f.INK, outline=f.GR, width=1)
    for yy in range(477, 704, 21):
        f.text(785, yy, "x@%" if (yy // 21) % 2 else ":=+", 13, f.GRAPH)
    f.render_girl(f.d, "q_front", 792, 471, 140,
                  knock=f.INK, col=f.BONE, hot=f.SIG)
    f.line([(916, 594), (942, 613), (970, 626)], f.BONE, 3)
    f.glyph_mark("+", 965, 620, 12, 12, f.BONE, 2)
    f.box(793, 439, 933, 466, fill=f.INK, outline=f.GR)
    f.text(805, 442, "AI.00 / AWAKE", 14, f.BONE, bold=True)


f.draw_workers = identical_ai_workers
f.OUT = Path(r"D:\Videos\Help! I'm stuck in a LIE\wip\codex\music_factory_lab_v1\factory_line_identical_ai_v1.png")

if __name__ == "__main__":
    f.main()
