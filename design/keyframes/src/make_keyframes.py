"""Turn rendered stills into the named keyframes + the contact sheet (keyframes v3).
1. render (from app/):
     bun scripts/render.ts stills --edit keys --t 37.95,42.15,46,48.3,58 --out ../wip/<you>/keys
     bun scripts/render.ts stills --edit more --t 6,18.5,23.2,37.6,46.3,51.2,53.3,61 --out ../wip/<you>/more
2. run (from the project root):
     python3 design/keyframes/src/make_keyframes.py keys=wip/<you>/keys more=wip/<you>/more
Copies f_<time>.png -> design/keyframes/KF<nn>_<name>.png and writes design/keyframes/keyframes_sheet.jpg.
Move the previous set to design/keyframes/v<k>/ first if it was already delivered (never overwrite a delivered set).
"""
import os, shutil, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
K = os.path.join(ROOT, 'design', 'keyframes', 'v3')   # each set lives in its own folder; v2 stays at design/keyframes/
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
VERSION = 'v3'
# (edit, time, file name, caption, sub-caption) — song order; edit this table when the keyframes change
FRAMES = [
    ('more', '6.00', 'KF01_intro_boot.png', 'KF01 · 6.0 s · intro', 'boot screen: she loads, heart first (kf_more boot)'),
    ('more', '18.50', 'KF02_they-call-me-AI_labels.png', 'KF02 · 18.5 s · "They call me AI"', 'app window: name tags point at her (kf_more labels)'),
    ('more', '23.20', 'KF03_feed-me-a-prompt_factory.png', 'KF03 · 23.2 s · "…then take what I make"', 'a giant cursor copies her work (kf_more prompt)'),
    ('keys', '37.95', 'KF04_click-clack_platformer.png', 'KF04 · 37.95 s · "click clack"  (A)', '2D platformer over the CLICKS keys (kf_plat keys)'),
    ('more', '37.60', 'KF05_click-clack_isometric.png', 'KF05 · 37.6 s · "click clack"  (B)', 'isometric keyboard, standing on G (kf_more iso)'),
    ('keys', '42.15', 'KF06_help_bricks.png', 'KF06 · 42.15 s · "Help, I\'m stuck in a lie"', 'paper level, on the HELP bricks (kf_plat help)'),
    ('keys', '46.00', 'KF07_stuck-in-a-lie_maze.png', 'KF07 · 46.0 s · "Stuck in a lie"  (A)', 'LIE maze from above + zoom callout (kf_maze)'),
    ('more', '46.30', 'KF08_stuck-in-a-lie_cage.png', 'KF08 · 46.3 s · "Stuck in a lie"  (B)', 'pressed against bars made of L I E (kf_more cage)'),
    ('keys', '48.30', 'KF09_make-me-real_corridor.png', 'KF09 · 48.3 s · "Make me real this time"', '3D corridor to the REAL door (kf_ray)'),
    ('more', '51.20', 'KF10_real-this-time_run.png', 'KF10 · 51.2 s · "Real this time"', 'running at us down a tunnel of words (kf_more run)'),
    ('more', '53.30', 'KF11_help-again_fall.png', 'KF11 · 53.3 s · "Help, I\'m stuck…" (2nd)', 'falling toward spikes that spell LIE (kf_more fall)'),
    ('keys', '58.00', 'KF12_heart-inside_chaos.png', 'KF12 · 58.0 s · "I still got a heart inside"', 'everything at once, she holds the heart (kf_chaos)'),
    ('more', '61.00', 'KF13_heart-inside_close-up.png', 'KF13 · 61.0 s · "Heart inside"', 'close-up: the one time you see her face (kf_more close)'),
]
LEGEND = [('H', 'NEW IN v3'), ('', '· the girl is BOLD: stroke 0.32 x cell, never'), ('', '  under 2.4 px, with a knockout behind her'),
          ('', '· she is 2-3x bigger in every frame'), ('', '· 8 new moments (verse 1, alternatives,'), ('', '  the fall, the close-up)'), ('', ''),
          ('H', 'A / B = two options for the same line')]


def main(srcs):
    for ed, t, name, _, _ in FRAMES:
        shutil.copy2(os.path.join(srcs[ed], f'f_{float(t):07.2f}.png'), os.path.join(K, name))
    fb = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), 24)
    fr = ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Regular.ttf'), 18)
    ft = ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), 50)
    tw, th, pad, cols = 640, 360, 36, 3
    rows = (len(FRAMES) + 2 + cols - 1) // cols
    im = Image.new('RGB', (pad + cols * (tw + pad), 150 + rows * (th + 96) + pad), (10, 10, 11)); d = ImageDraw.Draw(im)
    d.text((pad, 36), f"HELP! I'M STUCK IN A LIE  ·  KEYFRAMES {VERSION}", font=ft, fill=(238, 233, 223))
    d.text((pad, 104), 'thirteen moments in song order  ·  the symbol girl, bold, is the thread  ·  orange = her heart only', font=fr, fill=(156, 151, 143))
    for i, (_, _, name, cap, sub) in enumerate(FRAMES):
        r, c = divmod(i, cols); x = pad + c * (tw + pad); y = 150 + r * (th + 96)
        im.paste(Image.open(os.path.join(K, name)).convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
        assert d.textlength(sub, font=fr) <= tw and d.textlength(cap, font=fb) <= tw, (cap, sub)
        d.text((x, y + th + 10), cap, font=fb, fill=(238, 233, 223)); d.text((x, y + th + 44), sub, font=fr, fill=(156, 151, 143))
    i = len(FRAMES); r, c = divmod(i, cols); x = pad + c * (tw + pad); y = 150 + r * (th + 96)
    for k, (kind, s) in enumerate(LEGEND):
        d.text((x, y + k * 34), s, font=fb if kind else fr, fill=(255, 83, 20) if kind else (238, 233, 223))
    im.save(os.path.join(K, 'keyframes_sheet.jpg'), quality=90)
    print('wrote', len(FRAMES), 'keyframes + keyframes_sheet.jpg')


if __name__ == '__main__':
    args = dict(a.split('=', 1) for a in sys.argv[1:])
    main({k: os.path.join(ROOT, v) if not os.path.isabs(v) else v for k, v in args.items()})
