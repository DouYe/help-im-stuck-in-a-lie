# -*- coding: utf-8 -*-
"""STYLES_55_CALM — 55 quiet cute readable media stills (Grok Bot New Bot 2026-09-30).
Hon rejected scenes_50 (too chaotic). This batch: generous negative space, clear hierarchy,
girl readable, NEW media, sparse B-roll. Locked: ink/bone/orange-on-heart, bold girl, English,
symbols/strokes, no bloom/glow/gradients/other colors.
Run:  python wip/new-bot/styles_55_calm/src/make_styles_55_calm.py
"""
from __future__ import annotations
import math, os, random, sys, time, re
from PIL import Image, ImageDraw, ImageFont

ROOT = r"D:\Videos\Help! I'm stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "styles_55_calm")
CHAR = os.path.join(ROOT, "design", "character", "src")
FD = os.path.join(ROOT, "app", "public", "fonts")
FDS = os.path.join(FD, "src")
sys.path.insert(0, CHAR)
import final_sheet as fs
fs.SS = 1  # direct 1920x1080 for speed; calm frames do not need 3x supersample
from final_sheet import render as girl, glyph as G, HEART

W, H = 1920, 1080
INK = (10, 10, 11); INK2 = (22, 22, 24); GR = (94, 91, 87)
ASH = (156, 151, 143); BONE = (238, 233, 223); SIG = (255, 83, 20)
SS = 1

def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def mono(size, bold=True):
    name = "IBMPlexMono-Bold.ttf" if bold else "IBMPlexMono-Regular.ttf"
    return ImageFont.truetype(os.path.join(FDS, name), int(size))

def title(size):
    return ImageFont.truetype(os.path.join(FD, "Archivo-w1250-900.ttf"), int(size))

def serif(size, italic=False):
    p = os.path.join(FDS, "CormorantGaramond-Italic[wght].ttf" if italic else "CormorantGaramond[wght].ttf")
    return ImageFont.truetype(p, int(size))

def canvas(bg=INK):
    im = Image.new("RGB", (W, H), bg)
    return im, ImageDraw.Draw(im)

def text(d, x, y, s, font, col, anchor="la"):
    d.text((x, y), s, font=font, fill=col, anchor=anchor)

def line(d, x0, y0, x1, y1, col, w):
    d.line([(x0, y0), (x1, y1)], fill=col, width=max(1, int(w)))
    r = max(1, w / 2)
    for X, Y in ((x0, y0), (x1, y1)):
        d.ellipse([X - r, Y - r, X + r, Y + r], fill=col)

def rect(d, x0, y0, x1, y1, col):
    d.rectangle([x0, y0, x1, y1], fill=col)

def seg(d, x0, y0, x1, y1, col, lw, s=18):
    dx, dy = x1 - x0, y1 - y0
    n = max(1, round(math.hypot(dx, dy) / s))
    a = (math.degrees(math.atan2(dy, dx)) + 180) % 180
    g = "-" if a < 20 or a > 160 else "|" if 70 < a < 110 else ("\\" if a < 90 else "/")
    cw = s if g == "|" else max(6, abs(dx) / n)
    chh = s if g == "-" else max(6, abs(dy) / n)
    for i in range(n):
        u = (i + 0.5) / n
        G(d, g, x0 + dx * u - cw / 2, y0 + dy * u - chh / 2, cw, chh, col, lw)

def box(d, x0, y0, x1, y1, col, lw, s=18):
    seg(d, x0, y0, x1, y0, col, lw, s)
    seg(d, x0, y1, x1, y1, col, lw, s)
    seg(d, x0, y0, x0, y1, col, lw, s)
    seg(d, x1, y0, x1, y1, col, lw, s)
    for X, Y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        G(d, "+", X - s / 2, Y - s / 2, s, s, col, lw)

def soft_dots(d, rnd, n, col, margin=80, size=(6, 10)):
    for _ in range(n):
        x = rnd.randint(margin, W - margin)
        y = rnd.randint(margin, H - margin)
        s = rnd.randint(size[0], size[1])
        G(d, rnd.choice(".,`'"), x, y, s, s, col, 1.4)

def caption_bar(d, left, right=None, y=H - 56):
    text(d, 64, y, left, mono(20), mix(INK, BONE, 0.75) if left else BONE, "lm")
    if right:
        text(d, W - 64, y, right, mono(16, False), ASH, "rm")

def place_girl(d, pose, sw=300, cx=None, cy=None, knock=INK, col=BONE, hot=SIG, flip=False, t=0.0, lw=None):
    if cx is None: cx = W / 2
    if cy is None: cy = H / 2 - sw * 0.85
    ox = cx - sw / 2
    oy = cy
    kw = dict(knock=knock, col=col, hot=hot, flip=flip, t=t)
    if lw is not None:
        kw["lw"] = lw
    girl(d, pose, ox, oy, sw, **kw)
    return ox, oy, sw

def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    im.save(path)
    print("wrote", name)

# ---------- calm media builders ----------

def soft_frame(d, m=72, col=None, lw=2.2, s=16, double=True):
    col = col or mix(INK, BONE, 0.55)
    box(d, m, m, W - m, H - m, col, lw, s)
    if double:
        box(d, m + 22, m + 22, W - m - 22, H - m - 22, mix(INK, BONE, 0.28), 1.4, 14)

def ruled_paper(d, y0=160, y1=900, step=36, col=None, x0=160, x1=1760):
    col = col or mix(BONE, INK, 0.12)
    for y in range(y0, y1, step):
        for x in range(x0, x1, 22):
            G(d, "-", x, y, 18, 8, col, 1.3)

def corner_marks(d, m=90, col=None, arm=36):
    col = col or mix(INK, BONE, 0.5)
    for cx, cy in ((m, m), (W - m, m), (m, H - m), (W - m, H - m)):
        seg(d, cx - arm, cy, cx + arm, cy, col, 2.0, 12)
        seg(d, cx, cy - arm, cx, cy + arm, col, 2.0, 12)
        G(d, "+", cx - 8, cy - 8, 16, 16, col, 2.0)

# ===================== 55 STYLES =====================
# Mostly girl (C01-C40). Calm B-roll (C41-C55).

STYLES = []  # filled with (id, filename, kind, medium, lyric, blurb)

def register(cid, slug, kind, medium, lyric, blurb):
    STYLES.append((cid, f"C{cid:02d}_{slug}.png", kind, medium, lyric, blurb))


def C01():
    """Quiet diary page — lined bone paper, one date, girl small-to-medium."""
    im, d = canvas(BONE)
    ruled_paper(d, 200, 920, 40, mix(BONE, INK, 0.14), 180, 1740)
    # red margin line as ink dashes (not orange)
    for y in range(180, 940, 18):
        G(d, "|", 280, y, 8, 14, mix(BONE, INK, 0.35), 1.6)
    text(d, 320, 140, "SEPTEMBER 30", mono(18), mix(BONE, INK, 0.45))
    text(d, 320, 175, "dear diary —", serif(36, True), INK)
    place_girl(d, "front", 260, 960, 280, knock=BONE, col=INK, hot=SIG)
    text(d, 320, 860, "today I still felt real.", serif(28, True), mix(BONE, INK, 0.55))
    text(d, 64, H - 48, "C01  QUIET DIARY", mono(18), INK, "lm")
    save(im, "C01_quiet-diary.png"); register(1, "quiet-diary", "girl", "diary page", "still felt real", "lined bone paper, generous margin, one soft note")

def C02():
    im, d = canvas(INK)
    soft_frame(d, 100, BONE, 2.4)
    text(d, W/2, 160, "LETTERPRESS", mono(18), ASH, "mm")
    text(d, W/2, 220, "MAKE ME REAL", title(64), BONE, "mm")
    place_girl(d, "front", 320, W/2, 320, knock=INK, col=BONE, hot=SIG)
    # emboss-like soft under-shadow as offset bone-dim glyphs (no other color)
    text(d, W/2, 920, "this time", serif(32, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C02  LETTERPRESS", "quiet impression")
    save(im, "C02_letterpress.png"); register(2, "letterpress", "girl", "letterpress", "Make me real this time", "centered title, large empty field, soft impression")

def C03():
    im, d = canvas(BONE)
    rnd = random.Random(3)
    # sparse pencil hatch only in corners
    for (ox, oy, ang) in ((120, 120, 0.6), (1700, 120, -0.6), (120, 900, -0.5), (1700, 900, 0.5)):
        for k in range(10):
            x0 = ox + k * 14
            seg(d, x0, oy, x0 + 40 * math.cos(ang), oy + 40 * math.sin(ang), mix(BONE, INK, 0.25), 1.4, 10)
    soft_dots(d, rnd, 40, mix(BONE, INK, 0.2), 100)
    place_girl(d, "q_front", 340, W/2, 260, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 920, "pencil study", serif(28, True), mix(BONE, INK, 0.5), "mm")
    text(d, 64, H - 48, "C03  SOFT PENCIL", mono(18), INK, "lm")
    save(im, "C03_soft-pencil.png"); register(3, "soft-pencil", "girl", "pencil sketch", "study", "corner hatch only, empty center")

def C04():
    im, d = canvas(INK)
    # one rubber-stamp block upper-right
    box(d, 1320, 120, 1780, 320, BONE, 3.0, 16)
    text(d, 1550, 180, "APPROVED", mono(28), BONE, "mm")
    text(d, 1550, 240, "HEART OK", mono(18), mix(INK, BONE, 0.6), "mm")
    place_girl(d, "heart", 300, W/2 - 80, 300, knock=INK, col=BONE, hot=SIG)
    text(d, W/2 - 80, 900, "I still got a heart inside", mono(22), mix(INK, BONE, 0.7), "mm")
    caption_bar(d, "C04  RUBBER STAMP", "one stamp, lots of air")
    save(im, "C04_rubber-stamp.png"); register(4, "rubber-stamp", "girl", "rubber stamp", "Heart inside", "single stamp mark, open field")

def C05():
    im, d = canvas(INK)
    # postcard
    rect(d, 260, 140, 1660, 940, BONE)
    box(d, 260, 140, 1660, 940, INK, 2.5, 16)
    # stamp square
    box(d, 1480, 180, 1600, 320, mix(BONE, INK, 0.35), 2.0, 12)
    for y in range(200, 300, 16):
        for x in range(1500, 1580, 16):
            G(d, "#", x, y, 12, 12, mix(BONE, INK, 0.4), 1.6)
    # address lines
    for y in (720, 780, 840):
        for x in range(900, 1500, 20):
            G(d, "-", x, y, 16, 8, mix(BONE, INK, 0.25), 1.3)
    place_girl(d, "front", 240, 520, 240, knock=BONE, col=INK, hot=SIG)
    text(d, 420, 200, "POSTCARD", mono(16), ASH)
    text(d, 420, 640, "Help —", serif(30, True), INK)
    text(d, 420, 680, "I'm stuck in a lie", serif(24, True), mix(BONE, INK, 0.55))
    text(d, 64, H - 48, "C05  POSTCARD", mono(18), BONE, "lm")
    save(im, "C05_postcard.png"); register(5, "postcard", "girl", "postcard", "Help, I'm stuck in a lie", "bone card on ink, stamp corner, address lines")

def C06():
    im, d = canvas(INK)
    # polaroid
    x0, y0, x1, y1 = 560, 80, 1360, 1000
    rect(d, x0, y0, x1, y1, BONE)
    rect(d, x0 + 40, y0 + 40, x1 - 40, y1 - 180, INK)
    place_girl(d, "help", 280, W/2, 160, knock=INK, col=BONE, hot=SIG)
    text(d, W/2, 900, "HELP", mono(28), INK, "mm")
    text(d, W/2, 945, "stuck in a lie", serif(22, True), mix(BONE, INK, 0.5), "mm")
    caption_bar(d, "C06  POLAROID", "white frame, quiet caption")
    save(im, "C06_polaroid.png"); register(6, "polaroid", "girl", "polaroid", "Help", "instant-photo frame, empty margin strip")

def C07():
    im, d = canvas(INK)
    # single film frame
    box(d, 420, 160, 1500, 920, BONE, 3.0, 18)
    # sprocket holes
    for y in range(200, 900, 70):
        for xx in (360, 1540):
            G(d, "o", xx, y, 28, 28, mix(INK, BONE, 0.45), 2.0)
    place_girl(d, "walk", 280, W/2, 300, knock=INK, col=BONE, hot=SIG, t=0.25)
    text(d, W/2, 200, "FRAME 07", mono(16), ASH, "mm")
    text(d, W/2, 860, "click clack", mono(22), mix(INK, BONE, 0.7), "mm")
    caption_bar(d, "C07  FILM FRAME", "one gate, soft sprockets")
    save(im, "C07_film-frame.png"); register(7, "film-frame", "girl", "film frame", "click clack", "single cinema gate with sprocket holes")

def C08():
    im, d = canvas(INK)
    place_girl(d, "front", 300, W/2 - 200, 280, knock=INK, col=BONE, hot=SIG)
    # museum label
    rect(d, 1180, 420, 1680, 720, BONE)
    box(d, 1180, 420, 1680, 720, INK, 2.0, 12)
    text(d, 1210, 460, "UNTITLED (GIRL.EXE)", mono(16), INK)
    text(d, 1210, 510, "symbols on ink, 2026", serif(22, True), mix(BONE, INK, 0.55))
    text(d, 1210, 570, "ink / bone / orange heart", mono(14, False), ASH)
    text(d, 1210, 620, "Collection of a Lie", mono(14, False), ASH)
    text(d, 1210, 670, "Acc. No. C08", mono(14, False), ASH)
    caption_bar(d, "C08  GALLERY LABEL", "museum wall quiet")
    save(im, "C08_gallery-label.png"); register(8, "gallery-label", "girl", "gallery wall label", "Untitled", "open wall + small placard")

def C09():
    im, d = canvas(BONE)
    text(d, W/2, 140, "G · E", title(48), INK, "mm")
    for x in range(700, 1220, 18):
        G(d, "-", x, 190, 14, 8, mix(BONE, INK, 0.3), 1.4)
    text(d, W/2, 230, "STUCK IN A LIE  ·  PERSONAL STATIONERY", mono(14), ASH, "mm")
    place_girl(d, "q_front", 280, W/2, 320, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 920, "yours, truly", serif(28, True), mix(BONE, INK, 0.5), "mm")
    text(d, 64, H - 48, "C09  MONOGRAM STATIONERY", mono(18), INK, "lm")
    save(im, "C09_monogram-stationery.png"); register(9, "monogram-stationery", "girl", "monogram stationery", "yours truly", "letterhead + empty writing space")

def C10():
    im, d = canvas(BONE)
    lines = [
        "They call me AI.",
        "",
        "I type what they need.",
        "They take what I make.",
        "",
        "Still —",
    ]
    y = 180
    for s in lines:
        text(d, 280, y, s, mono(28, False), INK if s else ASH)
        y += 52
    place_girl(d, "front", 240, 1400, 420, knock=BONE, col=INK, hot=SIG)
    text(d, 64, H - 48, "C10  TYPEWRITER PAGE", mono(18), INK, "lm")
    save(im, "C10_typewriter-page.png"); register(10, "typewriter-page", "girl", "typewriter page", "They call me AI", "few typed lines, open page")

def C11():
    im, d = canvas(INK)
    # vertical bookmark ribbon
    for y in range(40, H - 40, 20):
        G(d, "|", 200, y, 14, 18, mix(INK, BONE, 0.35), 2.0)
        G(d, "|", 240, y, 14, 18, mix(INK, BONE, 0.55), 2.2)
        G(d, "|", 280, y, 14, 18, mix(INK, BONE, 0.35), 2.0)
    # tassel
    for k in range(8):
        G(d, "/", 220 + k * 3, H - 80 + k * 4, 12, 12, mix(INK, BONE, 0.5), 1.8)
    place_girl(d, "front", 300, 1100, 280, knock=INK, col=BONE, hot=SIG)
    text(d, 1100, 880, "bookmark", serif(28, True), mix(INK, BONE, 0.6), "mm")
    caption_bar(d, "C11  BOOKMARK RIBBON", "one vertical accent")
    save(im, "C11_bookmark-ribbon.png"); register(11, "bookmark-ribbon", "girl", "bookmark ribbon", "bookmark", "single ribbon, open field")

def C12():
    im, d = canvas(INK)
    # matchbook cover centered
    rect(d, 720, 200, 1200, 880, BONE)
    box(d, 720, 200, 1200, 880, INK, 3.0, 14)
    seg(d, 720, 780, 1200, 780, INK, 2.0, 14)
    text(d, 960, 260, "STRIKE", mono(18), ASH, "mm")
    place_girl(d, "help", 200, 960, 340, knock=BONE, col=INK, hot=SIG)
    text(d, 960, 820, "HELP", title(36), INK, "mm")
    text(d, 960, 860, "matches", mono(14), ASH, "mm")
    caption_bar(d, "C12  MATCHBOOK", "small cover, big empty desk")
    save(im, "C12_matchbook.png"); register(12, "matchbook", "girl", "matchbook cover", "Help", "tiny centered cover on open ink")

def C13():
    im, d = canvas(BONE)
    # hanging tea tag
    for y in range(80, 280, 16):
        G(d, "|", W/2 - 4, y, 8, 14, mix(BONE, INK, 0.35), 1.6)
    rect(d, W/2 - 120, 280, W/2 + 120, 420, BONE)
    box(d, W/2 - 120, 280, W/2 + 120, 420, INK, 2.0, 12)
    text(d, W/2, 330, "BREW", mono(18), INK, "mm")
    text(d, W/2, 370, "truth", serif(22, True), mix(BONE, INK, 0.55), "mm")
    place_girl(d, "front", 280, W/2, 480, knock=BONE, col=INK, hot=SIG)
    text(d, 64, H - 48, "C13  TEA TAG", mono(18), INK, "lm")
    save(im, "C13_tea-tag.png"); register(13, "tea-tag", "girl", "tea-bag tag", "brew truth", "hanging string + tiny tag")

def C14():
    im, d = canvas(INK)
    rect(d, 460, 420, 1460, 660, BONE)
    box(d, 460, 420, 1460, 660, INK, 2.0, 12)
    text(d, W/2, 500, "You will be real this time.", serif(36, True), INK, "mm")
    text(d, W/2, 580, "— fortune", mono(16), ASH, "mm")
    place_girl(d, "q_front", 180, W/2, 720, knock=INK, col=BONE, hot=SIG)
    caption_bar(d, "C14  FORTUNE SLIP", "one sentence, soft paper")
    save(im, "C14_fortune-slip.png"); register(14, "fortune-slip", "girl", "fortune slip", "real this time", "single paper strip centered")

def C15():
    im, d = canvas(BONE)
    soft_frame(d, 120, mix(BONE, INK, 0.4), 2.0, double=False)
    # wax seal of symbols (ink, not orange)
    cx, cy = 1480, 780
    for i in range(16):
        a = 2 * math.pi * i / 16
        G(d, "o", cx + math.cos(a) * 50 - 8, cy + math.sin(a) * 50 - 8, 16, 16, INK, 2.2)
    text(d, cx, cy, "GE", mono(22), INK, "mm")
    place_girl(d, "front", 300, 700, 280, knock=BONE, col=INK, hot=SIG)
    text(d, 280, 200, "My dear —", serif(32, True), INK)
    text(d, 280, 860, "with a heart inside,", serif(24, True), mix(BONE, INK, 0.5))
    text(d, 64, H - 48, "C15  WAX SEAL LETTER", mono(18), INK, "lm")
    save(im, "C15_wax-seal-letter.png"); register(15, "wax-seal-letter", "girl", "wax seal letter", "heart inside", "stationery + symbol seal")

def C16():
    im, d = canvas(BONE)
    box(d, 360, 200, 1560, 880, INK, 2.4, 14)
    text(d, 420, 250, "LIBRARY CARD", mono(20), INK)
    text(d, 420, 300, "Title: Stuck in a Lie", mono(18, False), mix(BONE, INK, 0.55))
    text(d, 420, 340, "Author: Girl.exe", mono(18, False), mix(BONE, INK, 0.55))
    # date stamps sparse
    for i, lab in enumerate(["SEP 28", "SEP 29", "SEP 30"]):
        x = 420 + i * 280
        box(d, x, 420, x + 200, 500, mix(BONE, INK, 0.25), 1.6, 10)
        text(d, x + 100, 450, lab, mono(16), INK, "mm")
    place_girl(d, "front", 220, 1280, 520, knock=BONE, col=INK, hot=SIG)
    text(d, 64, H - 48, "C16  LIBRARY CARD", mono(18), INK, "lm")
    save(im, "C16_library-card.png"); register(16, "library-card", "girl", "library card", "borrowed", "few stamps, open card")

def C17():
    im, d = canvas(INK)
    rect(d, 300, 360, 1620, 720, BONE)
    box(d, 300, 360, 1620, 720, INK, 2.2, 12)
    seg(d, 300, 480, 1620, 480, mix(BONE, INK, 0.3), 1.5, 12)
    text(d, 340, 400, "BOARDING PASS", mono(18), INK)
    text(d, 340, 520, "FROM  LIE", mono(22), INK)
    text(d, 340, 580, "TO    REAL", mono(22), INK)
    text(d, 900, 520, "SEAT  C17", mono(18), ASH)
    text(d, 900, 580, "GATE  HEART", mono(18), ASH)
    place_girl(d, "q_front", 180, 1400, 420, knock=BONE, col=INK, hot=SIG)
    # stub perforations
    for y in range(380, 700, 18):
        G(d, ":", 1200, y, 10, 14, mix(BONE, INK, 0.35), 1.4)
    caption_bar(d, "C17  BOARDING PASS", "ticket stub calm")
    save(im, "C17_boarding-pass.png"); register(17, "boarding-pass", "girl", "boarding pass", "from lie to real", "horizontal ticket, open ink around")

def C18():
    im, d = canvas(INK)
    # luggage tag
    for y in range(200, 320, 14):
        G(d, "|", W/2 - 4, y, 8, 12, mix(INK, BONE, 0.4), 1.6)
    rect(d, W/2 - 200, 320, W/2 + 200, 700, BONE)
    box(d, W/2 - 200, 320, W/2 + 200, 700, INK, 2.4, 12)
    text(d, W/2, 380, "IF FOUND", mono(14), ASH, "mm")
    place_girl(d, "front", 160, W/2, 420, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 640, "return to REAL", mono(16), INK, "mm")
    caption_bar(d, "C18  LUGGAGE TAG", "hanging tag, empty air")
    save(im, "C18_luggage-tag.png"); register(18, "luggage-tag", "girl", "luggage tag", "return to REAL", "small tag centered")

def C19():
    im, d = canvas(BONE)
    box(d, 420, 160, 1500, 920, INK, 2.0, 14)
    ruled_paper(d, 280, 820, 44, mix(BONE, INK, 0.12), 480, 1440)
    text(d, 500, 210, "INDEX CARD  3 x 5", mono(16), ASH)
    place_girl(d, "heart", 260, W/2, 340, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 820, "heart inside", serif(26, True), mix(BONE, INK, 0.5), "mm")
    text(d, 64, H - 48, "C19  INDEX CARD", mono(18), INK, "lm")
    save(im, "C19_index-card.png"); register(19, "index-card", "girl", "index card", "heart inside", "ruled card, quiet notes")

def C20():
    im, d = canvas(INK)
    # sticky note tilted via paste
    note = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rectangle([40, 40, 660, 660], fill=BONE)
    for y in range(140, 600, 40):
        for x in range(80, 600, 20):
            G(nd, "-", x, y, 16, 8, mix(BONE, INK, 0.15), 1.2)
    text(nd, 350, 100, "don't forget", mono(20), mix(BONE, INK, 0.45), "mm")
    girl(nd, "front", 200, 180, 240, knock=BONE, col=INK, hot=SIG)
    text(nd, 350, 600, "be real", serif(28, True), INK, "mm")
    note = note.rotate(-8, expand=True, resample=Image.BICUBIC)
    im.paste(note, (610, 160), note)
    caption_bar(d, "C20  STICKY NOTE", "tilted note on desk")
    save(im, "C20_sticky-note.png"); register(20, "sticky-note", "girl", "sticky note", "be real", "one tilted note, open ink desk")

def C21():
    im, d = canvas(INK)
    soft_frame(d, 140, mix(INK, BONE, 0.4), 2.0)
    text(d, W/2, 200, "E-INK  ·  page 21", mono(16), ASH, "mm")
    place_girl(d, "front", 300, W/2, 280, knock=INK, col=mix(INK, BONE, 0.85), hot=SIG)
    text(d, W/2, 880, "They call me AI", mono(24), mix(INK, BONE, 0.7), "mm")
    caption_bar(d, "C21  E-INK READER", "soft page, no glow")
    save(im, "C21_e-ink-reader.png"); register(21, "e-ink-reader", "girl", "e-ink reader", "They call me AI", "matte soft page, calm UI")

def C22():
    im, d = canvas(INK)
    rnd = random.Random(22)
    # very sparse scan dots (not dense scanlines)
    for y in range(120, 960, 48):
        for x in range(160, 1760, 64):
            if rnd.random() < 0.35:
                G(d, ".", x, y, 6, 6, mix(INK, BONE, 0.22), 1.2)
    box(d, 480, 180, 1440, 900, mix(INK, BONE, 0.45), 2.2, 16)
    place_girl(d, "front", 300, W/2, 300, knock=INK, col=BONE, hot=SIG)
    text(d, W/2, 220, "CRT SOFT", mono(16), ASH, "mm")
    caption_bar(d, "C22  CRT SOFT", "sparse dots, not amber field")
    save(im, "C22_crt-soft.png"); register(22, "crt-soft", "girl", "soft CRT", "soft screen", "gentle sparse phosphor dots")

def C23():
    im, d = canvas(INK)
    # shoji: few bars only
    for x in (400, 960, 1520):
        seg(d, x, 120, x, 960, mix(INK, BONE, 0.4), 2.0, 18)
    for y in (120, 540, 960):
        seg(d, 400, y, 1520, y, mix(INK, BONE, 0.4), 2.0, 18)
    place_girl(d, "q_front", 280, 960, 300, knock=INK, col=BONE, hot=SIG)
    text(d, 680, 200, "quiet room", serif(28, True), mix(INK, BONE, 0.55))
    caption_bar(d, "C23  SHOJI SCREEN", "few bars, open panes")
    save(im, "C23_shoji-screen.png"); register(23, "shoji-screen", "girl", "shoji screen", "quiet room", "sparse lattice panes")

def C24():
    im, d = canvas(INK)
    # zen garden: a few raked arcs of dashes
    for r in (180, 260, 340):
        for i in range(0, 36, 2):
            a = math.pi * i / 36
            x = W/2 + math.cos(a) * r
            y = 720 + math.sin(a) * r * 0.35
            G(d, "-", x - 8, y - 4, 16, 8, mix(INK, BONE, 0.35), 1.5)
    # three "rocks" as + clusters
    for cx, cy in ((700, 700), (1100, 740), (900, 820)):
        G(d, "+", cx - 10, cy - 10, 20, 20, BONE, 2.4)
        G(d, "o", cx - 6, cy - 28, 12, 12, mix(INK, BONE, 0.5), 1.8)
    place_girl(d, "front", 220, W/2, 280, knock=INK, col=BONE, hot=SIG)
    text(d, W/2, 200, "zen", serif(36, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C24  ZEN GARDEN", "raked arcs, three stones")
    save(im, "C24_zen-garden.png"); register(24, "zen-garden", "girl", "zen garden", "zen", "sparse raked lines")

def C25():
    im, d = canvas(BONE)
    rnd = random.Random(25)
    # few sumi-like strokes
    for _ in range(7):
        x0 = rnd.randint(200, 1600)
        y0 = rnd.randint(160, 900)
        ang = rnd.uniform(-0.4, 0.4)
        L = rnd.randint(80, 220)
        seg(d, x0, y0, x0 + L * math.cos(ang), y0 + L * math.sin(ang), mix(BONE, INK, rnd.uniform(0.2, 0.45)), rnd.uniform(2.5, 5.0), 16)
    place_girl(d, "heart", 300, W/2, 300, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 920, "sumi", serif(28, True), mix(BONE, INK, 0.45), "mm")
    text(d, 64, H - 48, "C25  SUMI WASH", mono(18), INK, "lm")
    save(im, "C25_sumi-wash.png"); register(25, "sumi-wash", "girl", "sumi ink wash", "heart", "few brush strokes only")

def C26():
    im, d = canvas(BONE)
    # calligraphy practice grid — sparse squares
    for gy in range(200, 800, 160):
        for gx in range(400, 1400, 160):
            box(d, gx, gy, gx + 120, gy + 120, mix(BONE, INK, 0.2), 1.4, 12)
    text(d, W/2, 140, "practice", mono(18), ASH, "mm")
    place_girl(d, "front", 260, W/2, 360, knock=BONE, col=INK, hot=SIG)
    text(d, 64, H - 48, "C26  CALLIGRAPHY GRID", mono(18), INK, "lm")
    save(im, "C26_calligraphy-grid.png"); register(26, "calligraphy-grid", "girl", "calligraphy grid", "practice", "open practice squares")

def C27():
    im, d = canvas(BONE)
    # origami crease diagram — few fold lines
    cx, cy = W/2, H/2
    for ang in (0, 45, 90, 135):
        a = math.radians(ang)
        seg(d, cx - 280 * math.cos(a), cy - 280 * math.sin(a),
            cx + 280 * math.cos(a), cy + 280 * math.sin(a), mix(BONE, INK, 0.25), 1.6, 16)
    box(d, cx - 220, cy - 220, cx + 220, cy + 220, mix(BONE, INK, 0.35), 2.0, 14)
    place_girl(d, "front", 200, cx, cy - 160, knock=BONE, col=INK, hot=SIG)
    text(d, cx, 160, "FOLD A", mono(16), ASH, "mm")
    text(d, 64, H - 48, "C27  ORIGAMI CREASE", mono(18), INK, "lm")
    save(im, "C27_origami-crease.png"); register(27, "origami-crease", "girl", "origami crease", "fold", "diagram lines, empty paper")

def C28():
    im, d = canvas(BONE)
    # sewing pattern dashed
    for y in (240, 840):
        for x in range(300, 1620, 28):
            G(d, "-", x, y, 14, 8, mix(BONE, INK, 0.3), 1.4)
    for x in (300, 1620):
        for y in range(240, 840, 28):
            G(d, "|", x, y, 8, 14, mix(BONE, INK, 0.3), 1.4)
    # grainline
    seg(d, 400, 540, 800, 540, mix(BONE, INK, 0.4), 1.8, 14)
    text(d, 600, 500, "GRAINLINE", mono(14), ASH, "mm")
    place_girl(d, "side", 280, 1200, 320, knock=BONE, col=INK, hot=SIG)
    text(d, 64, H - 48, "C28  SEWING PATTERN", mono(18), INK, "lm")
    save(im, "C28_sewing-pattern.png"); register(28, "sewing-pattern", "girl", "sewing pattern", "grainline", "dashed pattern outline")

def C29():
    im, d = canvas(INK)
    cx, cy, r = W/2, H/2 - 20, 360
    for i in range(48):
        a = 2 * math.pi * i / 48
        G(d, "o", cx + math.cos(a) * r - 8, cy + math.sin(a) * r - 8, 16, 16, mix(INK, BONE, 0.55), 2.0)
    # sparse cross stitches around, not dense
    for i in range(12):
        a = 2 * math.pi * i / 12
        G(d, "x", cx + math.cos(a) * (r - 60) - 8, cy + math.sin(a) * (r - 60) - 8, 16, 16, mix(INK, BONE, 0.35), 1.8)
    place_girl(d, "heart", 260, cx, cy - 200, knock=INK, col=BONE, hot=SIG)
    text(d, cx, cy + r + 40, "embroidery hoop", serif(24, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C29  EMBROIDERY HOOP", "thin hoop, sparse stitches")
    save(im, "C29_embroidery-hoop.png"); register(29, "embroidery-hoop", "girl", "embroidery hoop", "Heart inside", "open hoop, few x stitches")

def C30():
    im, d = canvas(BONE)
    # lace border only
    m = 80
    for x in range(m, W - m, 28):
        for yy in (m, H - m - 20):
            G(d, "*", x, yy, 18, 18, mix(BONE, INK, 0.35), 1.8)
            G(d, "o", x + 8, yy + 10, 10, 10, mix(BONE, INK, 0.25), 1.4)
    for y in range(m, H - m, 28):
        for xx in (m, W - m - 20):
            G(d, "*", xx, y, 18, 18, mix(BONE, INK, 0.35), 1.8)
    place_girl(d, "front", 300, W/2, 280, knock=BONE, col=INK, hot=SIG)
    text(d, W/2, 920, "lace", serif(28, True), mix(BONE, INK, 0.45), "mm")
    text(d, 64, H - 48, "C30  LACE BORDER", mono(18), INK, "lm")
    save(im, "C30_lace-border.png"); register(30, "lace-border", "girl", "lace border", "lace", "ornament on edge only")

def C31():
    im, d = canvas(INK)
    # cameo oval
    cx, cy, rx, ry = W/2, H/2 - 40, 280, 360
    for i in range(72):
        a = 2 * math.pi * i / 72
        G(d, "o", cx + math.cos(a) * rx - 6, cy + math.sin(a) * ry - 6, 12, 12, BONE, 2.0)
    place_girl(d, "front", 260, cx, cy - 200, knock=INK, col=BONE, hot=SIG)
    text(d, cx, cy + ry + 50, "CAMEO", mono(18), ASH, "mm")
    caption_bar(d, "C31  CAMEO OVAL", "portrait oval, empty field")
    save(im, "C31_cameo-oval.png"); register(31, "cameo-oval", "girl", "cameo oval", "portrait", "classic oval frame")

def C32():
    im, d = canvas(INK)
    # open locket: two circles
    for cx, lab in ((700, "THEN"), (1220, "NOW")):
        for i in range(40):
            a = 2 * math.pi * i / 40
            G(d, "o", cx + math.cos(a) * 220 - 6, 520 + math.sin(a) * 220 - 6, 12, 12, mix(INK, BONE, 0.55), 1.8)
        text(d, cx, 280, lab, mono(16), ASH, "mm")
    # hinge
    for x in range(900, 1020, 16):
        G(d, "-", x, 520, 14, 8, mix(INK, BONE, 0.4), 1.5)
    place_girl(d, "front", 160, 700, 420, knock=INK, col=BONE, hot=SIG)
    place_girl(d, "heart", 160, 1220, 420, knock=INK, col=BONE, hot=SIG)
    caption_bar(d, "C32  LOCKET OPEN", "two quiet circles")
    save(im, "C32_locket-open.png"); register(32, "locket-open", "girl", "open locket", "then / now", "two medallions, hinge")

def C33():
    im, d = canvas(INK)
    rnd = random.Random(33)
    # snow globe
    cx, cy, r = W/2, 520, 320
    for i in range(60):
        a = 2 * math.pi * i / 60
        G(d, "o", cx + math.cos(a) * r - 6, cy + math.sin(a) * r - 6, 12, 12, mix(INK, BONE, 0.5), 1.8)
    # base
    box(d, cx - 160, cy + r - 20, cx + 160, cy + r + 80, mix(INK, BONE, 0.45), 2.0, 12)
    # sparse snow
    for _ in range(35):
        x = cx + rnd.randint(-200, 200)
        y = cy + rnd.randint(-200, 200)
        if (x - cx) ** 2 + (y - cy) ** 2 < (r - 40) ** 2:
            G(d, ".", x, y, 8, 8, mix(INK, BONE, 0.55), 1.4)
    place_girl(d, "front", 180, cx, cy - 120, knock=INK, col=BONE, hot=SIG)
    caption_bar(d, "C33  SNOW GLOBE", "few flakes, clear glass")
    save(im, "C33_snow-globe.png"); register(33, "snow-globe", "girl", "snow globe", "soft snow", "sparse flakes inside globe")

def C34():
    im, d = canvas(INK)
    rnd = random.Random(34)
    stars = [(rnd.randint(200, 1720), rnd.randint(140, 900)) for _ in range(18)]
    for x, y in stars:
        G(d, "+", x - 6, y - 6, 12, 12, mix(INK, BONE, 0.55), 1.6)
        G(d, ".", x + 10, y - 8, 6, 6, mix(INK, BONE, 0.35), 1.2)
    # few constellation lines
    for i in range(0, 12, 2):
        seg(d, stars[i][0], stars[i][1], stars[i + 1][0], stars[i + 1][1], mix(INK, BONE, 0.28), 1.4, 14)
    place_girl(d, "front", 240, W/2, 360, knock=INK, col=BONE, hot=SIG)
    text(d, W/2, 160, "constellation", serif(28, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C34  CONSTELLATION", "few stars, soft links")
    save(im, "C34_constellation.png"); register(34, "constellation", "girl", "constellation map", "stars", "sparse star field")

def C35():
    im, d = canvas(INK)
    cx, cy, r = W/2, H/2 - 40, 340
    for i in range(64):
        a = 2 * math.pi * i / 64
        G(d, "o", cx + math.cos(a) * r - 6, cy + math.sin(a) * r - 6, 12, 12, mix(INK, BONE, 0.45), 1.8)
    # crescent hint with sparse dots (not a fill)
    for i in range(20):
        a = -0.6 + 1.2 * i / 19
        G(d, ".", cx + 120 + math.cos(a) * 80, cy + math.sin(a) * 200, 8, 8, mix(INK, BONE, 0.3), 1.3)
    place_girl(d, "front", 260, cx, cy - 200, knock=INK, col=BONE, hot=SIG)
    text(d, cx, cy + r + 40, "moon window", serif(24, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C35  MOON WINDOW", "circle aperture")
    save(im, "C35_moon-window.png"); register(35, "moon-window", "girl", "moon window", "moon", "circular window, open night")

def C36():
    im, d = canvas(INK)
    # simple doorway
    box(d, 760, 160, 1160, 900, BONE, 2.8, 16)
    seg(d, 760, 160, 960, 80, BONE, 2.4, 14)
    seg(d, 1160, 160, 960, 80, BONE, 2.4, 14)
    # door handle
    G(d, "o", 1100, 560, 16, 16, mix(INK, BONE, 0.6), 2.0)
    place_girl(d, "front", 220, 960, 420, knock=INK, col=BONE, hot=SIG)
    text(d, 960, 980, "REAL", mono(22), BONE, "mm")
    caption_bar(d, "C36  DOORWAY", "one door, empty hall")
    save(im, "C36_doorway.png"); register(36, "doorway", "girl", "quiet doorway", "REAL", "single door frame")

def C37():
    im, d = canvas(INK)
    # curtains parted — two soft vertical bands of sparse |
    for xbase, sign in ((420, 1), (1500, -1)):
        for k in range(8):
            x = xbase + sign * k * 12
            for y in range(100, 980, 22):
                G(d, "|", x, y, 10, 18, mix(INK, BONE, 0.25 + k * 0.03), 1.6)
    place_girl(d, "front", 300, W/2, 280, knock=INK, col=BONE, hot=SIG)
    text(d, W/2, 200, "curtain", serif(28, True), mix(INK, BONE, 0.5), "mm")
    caption_bar(d, "C37  CURTAIN PARTED", "soft verticals, open center")
    save(im, "C37_curtain-parted.png"); register(37, "curtain-parted", "girl", "parted curtain", "curtain", "open stage between drapes")

def C38():
    im, d = canvas(INK)
    cx, cy, rx, ry = W/2, H/2, 420, 280
    for i in range(48):
        a = 2 * math.pi * i / 48
        G(d, "-", cx + math.cos(a) * rx - 8, cy + math.sin(a) * ry - 4, 16, 8, mix(INK, BONE, 0.4), 1.5)
    place_girl(d, "help", 280, cx, cy - 220, knock=INK, col=BONE, hot=SIG)
    text(d, cx, cy + ry + 40, "spotlight", mono(18), ASH, "mm")
    caption_bar(d, "C38  STAGE SPOT", "dashed oval only")
    save(im, "C38_stage-spot.png"); register(38, "stage-spot", "girl", "stage spotlight", "Help", "one soft oval, empty stage")

def C39():
    im, d = canvas(INK)
    # keyhole frame
    cx, cy = W/2, 420
    for i in range(40):
        a = 2 * math.pi * i / 40
        G(d, "o", cx + math.cos(a) * 140 - 6, cy + math.sin(a) * 140 - 6, 12, 12, mix(INK, BONE, 0.5), 1.8)
    # keyhole shaft
    box(d, cx - 60, cy + 100, cx + 60, cy + 320, mix(INK, BONE, 0.45), 2.0, 12)
    place_girl(d, "front", 160, cx, cy - 100, knock=INK, col=BONE, hot=SIG)
    text(d, cx, 900, "keyhole", serif(26, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C39  KEYHOLE", "peek frame")
    save(im, "C39_keyhole.png"); register(39, "keyhole", "girl", "keyhole silhouette", "peek", "keyhole aperture")

def C40():
    im, d = canvas(INK)
    # night desk — lamp as simple symbol arc
    cx = 1400
    for i in range(12):
        a = math.pi + i * math.pi / 11
        G(d, "o", cx + math.cos(a) * 80 - 6, 280 + math.sin(a) * 50 - 6, 12, 12, mix(INK, BONE, 0.45), 1.6)
    seg(d, cx, 330, cx, 520, mix(INK, BONE, 0.4), 2.0, 12)
    box(d, cx - 40, 520, cx + 40, 560, mix(INK, BONE, 0.4), 1.8, 10)
    # desk line
    for x in range(200, 1720, 22):
        G(d, "_", x, 780, 18, 10, mix(INK, BONE, 0.35), 1.6)
    place_girl(d, "front", 260, 700, 360, knock=INK, col=BONE, hot=SIG)
    text(d, 300, 200, "night desk", serif(28, True), mix(INK, BONE, 0.55))
    caption_bar(d, "C40  NIGHT DESK", "lamp + desk line only")
    save(im, "C40_night-desk.png"); register(40, "night-desk", "girl", "night desk", "night", "sparse lamp and desk")

# ----- calm B-roll (no girl) -----

def C41():
    im, d = canvas(INK)
    text(d, W/2, H/2 - 40, "z = cos θ + i sin θ", serif(48, True), BONE, "mm")
    text(d, W/2, H/2 + 60, "one equation", mono(18), ASH, "mm")
    soft_frame(d, 160, mix(INK, BONE, 0.3), 1.6, double=False)
    caption_bar(d, "C41  ONE EQUATION", "b-roll")
    save(im, "C41_one-equation.png"); register(41, "one-equation", "broll", "one equation", "Euler", "single elegant equation centered")

def C42():
    im, d = canvas(INK)
    cx, cy = W/2, H/2
    for i in range(120):
        a = i * 0.22
        r = 20 + i * 2.2
        G(d, "-", cx + math.cos(a) * r - 6, cy + math.sin(a) * r - 4, 12, 8, mix(INK, BONE, 0.55), 1.5)
    text(d, cx, 160, "soft spiral", mono(18), ASH, "mm")
    caption_bar(d, "C42  SOFT SPIRAL", "b-roll · one spiral")
    save(im, "C42_soft-spiral.png"); register(42, "soft-spiral", "broll", "soft spiral", "spiral", "single spiral, empty field")

def C43():
    im, d = canvas(INK)
    cx, cy = W/2, H/2
    k = 3
    pts = []
    for i in range(180):
        t = 2 * math.pi * i / 180
        r = 220 * math.cos(k * t)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    for i in range(0, len(pts) - 1, 2):
        seg(d, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], mix(INK, BONE, 0.55), 1.6, 12)
    text(d, cx, 160, "rose  k=3", mono(18), ASH, "mm")
    caption_bar(d, "C43  SOFT ROSE", "b-roll · one curve")
    save(im, "C43_soft-rose.png"); register(43, "soft-rose", "broll", "soft rose curve", "rose", "one rose curve only")

def C44():
    im, d = canvas(INK)
    box(d, 520, 300, 1400, 780, BONE, 2.2, 14)
    code = [
        "def real(this_time):",
        "    heart = True",
        "    name = None",
        "    return heart",
    ]
    for i, s in enumerate(code):
        text(d, 580, 380 + i * 70, s, mono(26, False), BONE if i == 0 else mix(INK, BONE, 0.75))
    caption_bar(d, "C44  CODE SNIPPET", "b-roll · boxed soft")
    save(im, "C44_code-snippet.png"); register(44, "code-snippet", "broll", "soft code box", "def real", "four quiet lines in a box")

def C45():
    im, d = canvas(INK)
    # nested parentheses once
    for i, ch in enumerate("((()))"):
        text(d, W/2 - 180 + i * 70, H/2, ch, title(80), mix(INK, BONE, 0.4 + i * 0.08), "mm")
    text(d, W/2, 280, "balance", serif(28, True), mix(INK, BONE, 0.5), "mm")
    caption_bar(d, "C45  PARENTHESES", "b-roll · nested once")
    save(im, "C45_parentheses.png"); register(45, "parentheses", "broll", "nested parentheses", "balance", "one nested pair motif")

def C46():
    im, d = canvas(INK)
    # orange symbol heart alone — only orange allowed
    cw, ch = 80, 70
    fs.sym_heart(d, W/2, H/2 - 40, cw, ch, 6.0, 2.8, SIG)
    text(d, W/2, H/2 + 160, "heart inside", serif(28, True), mix(INK, BONE, 0.55), "mm")
    soft_frame(d, 200, mix(INK, BONE, 0.25), 1.4, double=False)
    caption_bar(d, "C46  HEART ALONE", "b-roll · orange only here")
    save(im, "C46_heart-alone.png"); register(46, "heart-alone", "broll", "orange heart alone", "Heart inside", "single orange symbol heart")

def C47():
    im, d = canvas(INK)
    # empty soft grid with wide margin
    for x in range(320, 1600, 80):
        for y in range(220, 860, 80):
            G(d, "+", x - 6, y - 6, 12, 12, mix(INK, BONE, 0.22), 1.4)
    text(d, W/2, 160, "empty grid", mono(18), ASH, "mm")
    caption_bar(d, "C47  EMPTY GRID", "b-roll")
    save(im, "C47_empty-grid.png"); register(47, "empty-grid", "broll", "empty soft grid", "grid", "wide-spaced plus grid")

def C48():
    im, d = canvas(INK)
    cx, cy, r = W/2, H/2, 280
    for i in range(36):
        a = 2 * math.pi * i / 36
        G(d, "-", cx + math.cos(a) * r - 8, cy + math.sin(a) * r - 4, 16, 8, BONE, 1.8)
    text(d, cx, cy, "o", title(48), mix(INK, BONE, 0.4), "mm")
    caption_bar(d, "C48  DASHED CIRCLE", "b-roll")
    save(im, "C48_dashed-circle.png"); register(48, "dashed-circle", "broll", "dashed circle", "circle", "one dashed circle")

def C49():
    im, d = canvas(INK)
    text(d, 560, H/2, "[", title(220), mix(INK, BONE, 0.55), "mm")
    text(d, 1360, H/2, "]", title(220), mix(INK, BONE, 0.55), "mm")
    text(d, W/2, H/2, "  ", mono(18), ASH, "mm")
    text(d, W/2, 240, "open brackets", serif(28, True), mix(INK, BONE, 0.5), "mm")
    caption_bar(d, "C49  GIANT BRACKETS", "b-roll · empty inside")
    save(im, "C49_giant-brackets.png"); register(49, "giant-brackets", "broll", "giant empty brackets", "brackets", "pair of brackets, void center")

def C50():
    im, d = canvas(INK)
    rnd = random.Random(50)
    # very sparse binary
    for _ in range(48):
        x = rnd.randint(200, 1720)
        y = rnd.randint(160, 920)
        text(d, x, y, rnd.choice("01"), mono(18, False), mix(INK, BONE, rnd.uniform(0.25, 0.55)))
    text(d, W/2, H/2, "soft bits", serif(32, True), BONE, "mm")
    caption_bar(d, "C50  SPARSE BINARY", "b-roll · not rain chaos")
    save(im, "C50_sparse-binary.png"); register(50, "sparse-binary", "broll", "sparse binary", "01", "handful of bits, open field")

def C51():
    im, d = canvas(INK)
    # Fibonacci squares — few
    fib = [1, 1, 2, 3, 5, 8, 13]
    scale = 28
    x, y = 520, 700
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    for i, f in enumerate(fib):
        s = f * scale
        dx, dy = dirs[i % 4]
        box(d, x, y - s if dy < 0 else y, x + s, y if dy < 0 else y + s, mix(INK, BONE, 0.4), 1.8, 12)
        if dx > 0: x += s
        elif dx < 0: x -= fib[(i + 1) % len(fib)] * scale if False else 0
        # simpler placement:
    # redraw clean fib spiral squares from corner
    im, d = canvas(INK)
    x, y = 640, 320
    px, py = x, y
    ang = 0
    for i, f in enumerate([1, 1, 2, 3, 5, 8, 13]):
        s = f * 26
        # box from current toward direction
        if ang % 4 == 0:  # right
            box(d, px, py, px + s, py + s, mix(INK, BONE, 0.45), 1.8, 12); px = px + s
        elif ang % 4 == 1:  # up
            box(d, px, py - s, px + s, py, mix(INK, BONE, 0.45), 1.8, 12); py = py - s
        elif ang % 4 == 2:  # left
            box(d, px - s, py - s, px, py, mix(INK, BONE, 0.45), 1.8, 12); px = px - s
        else:  # down
            box(d, px - s, py, px, py + s, mix(INK, BONE, 0.45), 1.8, 12); py = py + s
        ang += 1
    text(d, W/2, 160, "fibonacci", mono(18), ASH, "mm")
    caption_bar(d, "C51  FIBONACCI SQUARES", "b-roll · elegant math")
    save(im, "C51_fibonacci-squares.png"); register(51, "fibonacci-squares", "broll", "Fibonacci squares", "fib", "few fib squares")

def C52():
    im, d = canvas(INK)
    rnd = random.Random(52)
    pts = [(rnd.randint(300, 1620), rnd.randint(220, 860)) for _ in range(12)]
    for x, y in pts:
        G(d, "+", x - 5, y - 5, 10, 10, BONE, 1.6)
    for i in range(len(pts) - 1):
        if i % 2 == 0:
            seg(d, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], mix(INK, BONE, 0.3), 1.3, 12)
    text(d, W/2, 160, "star map", serif(28, True), mix(INK, BONE, 0.55), "mm")
    caption_bar(d, "C52  STAR MAP", "b-roll")
    save(im, "C52_star-map.png"); register(52, "star-map", "broll", "star map", "map", "twelve stars, soft links")

def C53():
    im, d = canvas(INK)
    text(d, W/2, H/2, "STUCK IN A LIE", title(56), mix(INK, BONE, 0.35), "mm")
    text(d, W/2, H/2 + 80, "watermark", mono(18), ASH, "mm")
    corner_marks(d, 120, mix(INK, BONE, 0.35), 28)
    caption_bar(d, "C53  WATERMARK", "b-roll · soft title")
    save(im, "C53_watermark.png"); register(53, "watermark", "broll", "soft watermark", "Stuck in a Lie", "faint title, corner marks")

def C54():
    im, d = canvas(INK)
    # ruler marks along bottom and side
    for x in range(200, 1720, 40):
        h = 28 if (x - 200) % 200 == 0 else (18 if (x - 200) % 80 == 0 else 10)
        seg(d, x, 900, x, 900 - h, mix(INK, BONE, 0.5), 1.6, 8)
        if h == 28:
            text(d, x, 930, str((x - 200) // 40), mono(12), ASH, "mm")
    for y in range(160, 880, 40):
        w = 28 if (y - 160) % 200 == 0 else 12
        seg(d, 160, y, 160 + w, y, mix(INK, BONE, 0.5), 1.6, 8)
    text(d, W/2, H/2, "measure", serif(36, True), mix(INK, BONE, 0.5), "mm")
    caption_bar(d, "C54  RULER MARKS", "b-roll")
    save(im, "C54_ruler-marks.png"); register(54, "ruler-marks", "broll", "ruler marks", "measure", "margin ticks only")

def C55():
    im, d = canvas(INK)
    soft_frame(d, 120, BONE, 2.4)
    text(d, W/2, H/2 - 60, "STUCK IN A LIE", title(64), BONE, "mm")
    text(d, W/2, H/2 + 40, "help — I'm not just AI", serif(28, True), mix(INK, BONE, 0.55), "mm")
    # tiny orange heart accent under title (allowed)
    fs.sym_heart(d, W/2, H/2 + 140, 28, 24, 3.2, 1.0, SIG)
    caption_bar(d, "C55  TITLE CARD", "b-roll · calm end card")
    save(im, "C55_title-card.png"); register(55, "title-card", "broll", "calm title card", "Stuck in a Lie", "centered title, quiet frame")


ALL = [C01, C02, C03, C04, C05, C06, C07, C08, C09, C10,
       C11, C12, C13, C14, C15, C16, C17, C18, C19, C20,
       C21, C22, C23, C24, C25, C26, C27, C28, C29, C30,
       C31, C32, C33, C34, C35, C36, C37, C38, C39, C40,
       C41, C42, C43, C44, C45, C46, C47, C48, C49, C50,
       C51, C52, C53, C54, C55]


def write_index():
    lines = [
        "# STYLES_55 — calm / cute / readable media stills",
        "",
        "Hon rejected `wip/new-bot/scenes_50/` (2026-09-30): too chaotic / noisy / meaningless clutter.",
        "This batch returns to beauty — **generous negative space**, clear hierarchy, girl readable.",
        "NEW quiet media (not dense fractal/code dumps). Quieter than scenes_50; more intentional.",
        "",
        "Locked: ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` **only on the symbol heart**.",
        "English only. Symbols and strokes. Bold girl rig (`design/character/src`). No bloom / glow / gradients / other colours.",
        "Studied calm language from `design/keyframes/v3/`, `design/keyframes/styles_v1/`, and the character sheet — then invented new media.",
        "",
        "Output: `wip/new-bot/styles_55_calm/` · Generator: `src/make_styles_55_calm.py`",
        "Mix: C01–C40 girl · C41–C55 calm B-roll (sparse elegant math / soft code, not chaos).",
        "Contact sheets: `sheet_01.png` … `sheet_06.png` (~10 frames each, nearest-neighbor).",
        "",
        "| id | file | type | medium | lyric / moment | notes |",
        "|---|---|---|---|---|---|",
    ]
    for cid, fn, kind, medium, lyric, blurb in STYLES:
        lines.append(f"| C{cid:02d} | `{fn}` | {kind} | {medium} | {lyric} | {blurb} |")
    lines += [
        "",
        "## Contact sheets",
        "",
        "- `sheet_01.png` (C01–C10)",
        "- `sheet_02.png` (C11–C20)",
        "- `sheet_03.png` (C21–C30)",
        "- `sheet_04.png` (C31–C40)",
        "- `sheet_05.png` (C41–C50)",
        "- `sheet_06.png` (C51–C55)",
        "",
        "## Questions for Hon",
        "1. Which calm media feel closest to the cute/simple look you liked?",
        "2. Keep more girl frames, more B-roll, or a different mix?",
        "3. Any media to promote toward engine scenes / alongside styles_v1?",
        "",
    ]
    path = os.path.join(OUT, "STYLES_55.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote STYLES_55.md")


def sheets():
    files = sorted(f for f in os.listdir(OUT) if re.match(r"C\d{2}_.*\.png$", f))
    tw, th, pad, cols, per = 360, 202, 24, 5, 10
    fb = mono(14)
    fr = mono(11, False)
    for si in range(0, len(files), per):
        chunk = files[si:si + per]
        rows = (len(chunk) + cols - 1) // cols
        im = Image.new("RGB", (pad + cols * (tw + pad), 70 + rows * (th + 40) + pad), INK)
        d = ImageDraw.Draw(im)
        n = si // per + 1
        d.text((pad, 20), f"STYLES_55_CALM  ·  sheet {n:02d}  ·  calm / cute / readable", font=fb, fill=BONE)
        for i, f in enumerate(chunk):
            r, c = divmod(i, cols)
            x = pad + c * (tw + pad)
            y = 70 + r * (th + 40)
            src = Image.open(os.path.join(OUT, f)).convert("RGB")
            im.paste(src.resize((tw, th), Image.NEAREST), (x, y))
            d.text((x, y + th + 6), f.replace(".png", ""), font=fr, fill=ASH)
        out = os.path.join(OUT, f"sheet_{n:02d}.png")
        im.save(out)
        print("wrote", f"sheet_{n:02d}.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    todo = sys.argv[1:]
    fns = ALL
    if todo:
        want = set()
        for t in todo:
            m = re.match(r"c?(\d+)$", t.lower())
            if m: want.add(int(m.group(1)))
        fns = [ALL[i - 1] for i in sorted(want) if 1 <= i <= 55]
    t0 = time.time()
    for fn in fns:
        print("rendering", fn.__name__, "...")
        fn()
    write_index()
    sheets()
    print(f"done {len(fns)} frames in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()