"""C — close-ups of her, in the manner of Hon's reference (design/references/2026-09-30_hon_closeup-reference.png)."""
from kit import *
from closeup import closeup, streams, heart_hatched


def c05():
    """'I still got a heart inside' — 3/4 bust, streams behind, hatched orange heart. Closest to the reference."""
    im, d = canvas(INK)
    streams(d, 0, W, 20, H, gap=32, seed=5, size=14, lw=2.0, bright=BONE)
    sw = 1160
    info = closeup(d, 'q_front', 1010 - 0.53 * sw, 40, sw, k=5, knock=INK, heart_scale=1.35)
    save_scene(im, 'C05', lambda img: grain(img, 5))


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or ['c05']): globals()[n]()
