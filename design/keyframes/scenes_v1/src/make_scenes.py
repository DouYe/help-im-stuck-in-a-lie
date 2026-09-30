"""Render scenes and contact sheets for design/keyframes/scenes_v1/.

  python3 design/keyframes/scenes_v1/src/make_scenes.py A10 B01 ...      render these frames
  python3 design/keyframes/scenes_v1/src/make_scenes.py all              render every frame that has code
  python3 design/keyframes/scenes_v1/src/make_scenes.py --sheets         contact sheets (per kind + song order)
  python3 design/keyframes/scenes_v1/src/make_scenes.py --mini OUT.jpg A01 A02 ...   a quick review sheet

Each frame is a function named after its plan id in lower case (a10, b01, c05, m03 …) in one of the sc_*.py
modules here. Modules are imported only when one of their frames is requested, so a broken module never stops
the others.
"""
import os, re, sys, glob, importlib, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from plan import PLAN, BY_ID, KIND_NAME
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'design', 'keyframes', 'scenes_v1')
FD = os.path.join(ROOT, 'app', 'public', 'fonts')
INK = (10, 10, 11); BONE = (238, 233, 223); ASH = (156, 151, 143); GR = (94, 91, 87); SIG = (255, 83, 20)


def where():
    """id -> module name, by reading the sc_*.py sources (no import)."""
    m = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'sc_*.py'))):
        src = open(f, encoding='utf-8').read()
        for fid in re.findall(r'^def ([abcm]\d\d)\(', src, re.M): m[fid.upper()] = os.path.basename(f)[:-3]
    return m


def render(ids):
    w = where(); mods = {}
    for sid in ids:
        sid = sid.upper()
        if sid not in w: print(f'{sid}: no code yet'); continue
        mn = w[sid]
        try:
            if mn not in mods: mods[mn] = importlib.import_module(mn)
            t = time.time(); getattr(mods[mn], sid.lower())(); print(f'   {sid} {time.time() - t:.1f}s')
        except Exception as e:
            import traceback; traceback.print_exc(); print(f'{sid}: FAILED ({e})')


def tkey(p):
    """Song-order key from the plan's time string (Edit seconds; 'Final x' passages sit at Edit 114.66)."""
    t = p['t']
    if t.startswith('Final'): return 114.7 + float(re.findall(r'[\d.]+', t)[0]) / 1000
    return float(re.findall(r'[\d.]+', t)[0])


def _fonts():
    return (ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Bold.ttf'), 24),
            ImageFont.truetype(os.path.join(FD, 'src', 'IBMPlexMono-Regular.ttf'), 18),
            ImageFont.truetype(os.path.join(FD, 'Archivo-w1250-900.ttf'), 50))


def sheet(items, out, heading, sub, cols=3, tw_=600):
    fb, fr, ft = _fonts(); th_ = tw_ * 9 // 16; pad = 36; cap = 74
    rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (pad + cols * (tw_ + pad), 160 + rows * (th_ + cap + 22) + pad), INK); d = ImageDraw.Draw(im)
    d.text((pad, 30), heading, font=ft, fill=BONE); d.text((pad, 100), sub, font=fr, fill=ASH)
    for i, p in enumerate(items):
        r, c = divmod(i, cols); x = pad + c * (tw_ + pad); y = 160 + r * (th_ + cap + 22)
        f = os.path.join(OUT, p['file'])
        if os.path.exists(f): im.paste(Image.open(f).convert('RGB').resize((tw_, th_), Image.LANCZOS), (x, y))
        else: d.rectangle([x, y, x + tw_, y + th_], outline=GR); d.text((x + tw_ // 2, y + th_ // 2), 'not rendered', font=fr, fill=GR, anchor='mm')
        lab = f"{p['id']}  {p['medium'].upper()}"
        while d.textlength(lab, font=fb) > tw_ and len(lab) > 8: lab = lab[:-2]
        d.text((x, y + th_ + 10), lab, font=fb, fill=SIG if p['kind'] == 'C' else BONE)
        lyr = f"{p['section']} · {p['t']} s · \"{p['lyric']}\"" if p['kind'] != 'M' or p['lyric'][0] != '(' else f"{p['section']} · {p['t']} s"
        while d.textlength(lyr, font=fr) > tw_ and len(lyr) > 8: lyr = lyr[:-2]
        d.text((x, y + th_ + 42), lyr, font=fr, fill=ASH)
    im.save(out, quality=88); print('wrote', os.path.relpath(out, ROOT), im.size)


def sheets():
    for k in 'ACMB':
        items = [p for p in PLAN if p['kind'] == k]
        sub = {'A': 'she stays the same bold symbol girl; the world changes medium from shot to shot · in song order',
               'B': 'no girl · code and machine close-ups, tilted with shallow depth of field · in song order',
               'C': "close-ups of her in the manner of Hon's reference: finer symbols, data streams, hatched orange heart",
               'M': 'mathematical figures drawn with symbols · layered, never a single line · in song order'}[k]
        sheet(items, os.path.join(OUT, f'sheet_{k}_{KIND_NAME[k].split(" ·")[0].lower().replace(" ", "-")}.jpg'),
              f'SCENES v1 · {k} · {KIND_NAME[k]}', sub, cols=3 if len(items) > 6 else 2, tw_=600 if len(items) > 6 else 900)
    allp = sorted(PLAN, key=tkey)
    sheet(allp, os.path.join(OUT, 'sheet_0_all-in-song-order.jpg'), 'STUCK IN A LIE · SCENES v1 · ALL %d IN SONG ORDER' % len(allp),
          'A = with her · B = B-roll (no girl) · C = close-up · M = math figure · times on the Edit master', cols=6, tw_=400)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == '--sheets': sheets()
    elif a[0] == '--mini':
        ids = [x.upper() for x in a[2:]]; sheet([BY_ID[i] for i in ids], a[1], 'REVIEW', ' '.join(ids), cols=3, tw_=600)
    elif a[0] == 'all': render(sorted(where()))
    else: render(a)
