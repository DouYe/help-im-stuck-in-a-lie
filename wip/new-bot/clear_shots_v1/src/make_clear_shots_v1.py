# -*- coding: utf-8 -*-
"""Clear shots v1 - 8 readable framed keyframe-rhythm stills.

Hon rejected platform_run_v1 (messy continuous runner). Want ORIGINAL keyframe
rhythm: ONE clear framed scene per still, strong STRUCTURE, forms readable at
a glance (room / door / maze / platform / factory) + cute girl escaping AI world.
Not chaos (scenes_50), not empty (styles_55), not continuous runner.

Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314 on symbol heart only.
English. Symbols/strokes. No bloom/glow/gradients/other colours.
Reuses design/character/src girl rig. Never writes into design/keyframes.
"""
from __future__ import annotations

import math
import os
import random
import sys

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "clear_shots_v1")
SRC_OUT = os.path.join(OUT, "src")
CHAR = os.path.join(ROOT, "design", "character", "src")
FONT_DIR = os.path.join(ROOT, "app", "public", "fonts", "src")
sys.path.insert(0, CHAR)

import final_sheet as fs

fs.SS = 1
from final_sheet import render, INK, BONE, SIG
from glyphs import G
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
SOFT = [".", ":", "'", ","]


def gdir(dx, dy):
    th = math.degrees(math.atan2(dy, dx)) % 180.0
    if th < 20 or th > 160:
        return "-"
    if 70 < th < 110:
        return "|"
    if th < 90:
        return "\\"
    return "/"


class Shot:
    def __init__(self, seed: int):
        self.im = Image.new("RGB", (W, H), INK)
        self.rng = random.Random(seed)
        self.cache = {}
        self.n = 0
        self.font_s = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 16)
        self.font_m = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 20)
        self.font_b = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 24)
        self.font_h = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 40)
        self.font_t = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 64)
        self.font_x = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 96)
        self.d = ImageDraw.Draw(self.im)

    def _stamp(self, g, cw, ch):
        cw, ch = max(6, int(cw)), max(6, int(ch))
        key = (g, cw, ch)
        im = self.cache.get(key)
        if im is None:
            pad = 4
            im = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
            dd = ImageDraw.Draw(im)
            lw = max(1.8, 0.28 * ch)
            fs.glyph(dd, g, pad, pad, cw, ch, BONE, lw)
            self.cache[key] = im
        return im

    def put(self, g, x, y, cw, ch):
        if g not in G or g in (" ", "*"):
            return
        cw, ch = int(cw), int(ch)
        x, y = int(x), int(y)
        if x < -cw or y < -ch or x >= W or y >= H:
            return
        st = self._stamp(g, cw, ch)
        self.im.paste(st, (x - 4, y - 4), st)
        self.n += 1

    def text(self, xy, s, font, col=BONE):
        if not s:
            return
        bbox = font.getbbox(s)
        tw = max(1, bbox[2] - bbox[0] + 2)
        th = max(1, bbox[3] - bbox[1] + 2)
        mask = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
        bw = mask.point(lambda p: 255 if p >= 128 else 0)
        color = Image.new("RGB", (tw, th), col)
        self.im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)

    def polyline(self, pts, cw, ch=None, step=None, thick=1):
        cw = int(cw)
        ch = int(ch or cw)
        step = float(step or max(cw * 0.82, 6))
        carry = 0.0
        prev = None
        for pt in pts:
            if prev is None:
                prev = pt
                continue
            x0, y0 = prev
            x1, y1 = pt
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 1e-3:
                prev = pt
                continue
            ux, uy = dx / L, dy / L
            nx, ny = -uy, ux
            g = gdir(dx, dy)
            dist = carry
            while dist <= L:
                x = x0 + ux * dist
                y = y0 + uy * dist
                for k in range(thick):
                    off = (k - (thick - 1) / 2.0) * ch * 0.70
                    self.put(g, x + nx * off - cw / 2.0, y + ny * off - ch / 2.0, cw, ch)
                dist += step
            carry = dist - L
            prev = pt

    def rect(self, x, y, w, h, cw=12, thick=2):
        self.polyline(
            [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
            cw, cw, thick=thick,
        )

    def platform(self, x, y, w, cw=14, thick=3):
        self.polyline([(x, y), (x + w, y)], cw, cw, thick=thick)
        for i in range(0, int(w), cw * 2):
            self.put("=", x + i, y - 2, cw, cw)

    def clear_oval(self, cx, cy, rx, ry):
        self.d = ImageDraw.Draw(self.im)
        self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=INK)

    def caption(self, left, right=None):
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([0, 0, W, 48], fill=INK)
        self.d.line([(0, 48), (W, 48)], fill=BONE, width=2)
        self.text((18, 14), left, self.font_b)
        if right:
            tw = self.font_b.getlength(right)
            self.text((W - 24 - tw, 14), right, self.font_b)

    def label_box(self, x, y, s, font=None):
        font = font or self.font_b
        pad = 10
        tw = font.getlength(s)
        th = font.size + 8
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([x - pad, y - 6, x + tw + pad, y + th], fill=INK, outline=BONE, width=2)
        self.text((x, y), s, font)

    def girl(self, pose="front", sw=280, feet=(960, 920), t=0.0, flip=False, view=None, wall=False, air=True):
        fx, fy = feet
        ox = fx - 0.55 * sw
        oy = fy - 1.47 * sw
        if air:
            self.clear_oval(fx, fy - sw * 0.78, sw * 0.70, sw * 1.02)
        render(self.d, pose, ox, oy, sw, t, flip, view, wall=wall, knock=INK, col=BONE, hot=SIG)

    def door(self, x, y, w, h, label="REAL", open_=False):
        self.rect(x, y, w, h, cw=16, thick=3)
        pts = [(x, y)]
        for i in range(13):
            a = i / 12 * math.pi
            pts.append((x + w * 0.5 + (w * 0.5) * math.cos(math.pi - a), y - h * 0.16 * math.sin(a)))
        pts.append((x + w, y))
        self.polyline(pts, 14, thick=2)
        if open_:
            self.polyline(
                [(x + w * 0.55, y), (x + w * 0.88, y + h * 0.06), (x + w * 0.88, y + h)],
                14, thick=2,
            )
        else:
            self.polyline([(x + w * 0.5, y), (x + w * 0.5, y + h)], 12, thick=1)
            self.put("o", x + w * 0.68, y + h * 0.48, 22, 22)
        self.label_box(x + w * 0.18, y + h * 0.28, label, self.font_h)

    def frame_room(self, x=80, y=70, w=1760, h=940, cw=14, thick=3):
        self.rect(x, y, w, h, cw=cw, thick=thick)
        fy = y + h - 90
        self.polyline([(x + 20, fy), (x + w - 20, fy)], 12, thick=2)
        for i in range(0, int(w - 40), 48):
            self.put("_", x + 30 + i, fy + 8, 14, 14)
        self.polyline([(x + 20, y + 40), (x + w - 20, y + 40)], 10, thick=1)

    def sparse_bg(self, n=18):
        for _ in range(n):
            x = self.rng.randint(100, W - 100)
            y = self.rng.randint(80, H - 80)
            self.put(self.rng.choice(SOFT), x, y, 10, 10)

    def save(self, name):
        path = os.path.join(OUT, name)
        self.im.save(path, "PNG", compress_level=1)
        cols = self.im.getcolors(maxcolors=12)
        bad = []
        if cols is None:
            bad = ["too-many"]
        else:
            for _, c in cols:
                if c not in (INK, BONE, SIG):
                    bad.append(c)
        return path, bad


def letter_strokes(ch, x, y, s):
    def P(u, v):
        return (x + u * s, y + v * s)

    strokes = {
        "H": [[P(0, 0), P(0, 7)], [P(4, 0), P(4, 7)], [P(0, 3.5), P(4, 3.5)]],
        "E": [[P(0, 0), P(0, 7)], [P(0, 0), P(4, 0)], [P(0, 3.5), P(3.2, 3.5)], [P(0, 7), P(4, 7)]],
        "L": [[P(0, 0), P(0, 7)], [P(0, 7), P(4, 7)]],
        "P": [[P(0, 0), P(0, 7)], [P(0, 0), P(3.2, 0), P(4, 1.2), P(4, 2.6), P(3.2, 3.5), P(0, 3.5)]],
        "I": [[P(2, 0), P(2, 7)], [P(0.6, 0), P(3.4, 0)], [P(0.6, 7), P(3.4, 7)]],
    }
    return strokes.get(ch, [])


def brick_letter(S: Shot, ch, x, y, s=48, cw=14):
    for stroke in letter_strokes(ch, x, y, s):
        S.polyline(stroke, cw, cw, thick=3)
    for by in range(0, 7):
        for bx in range(0, 5):
            draw = False
            if ch == "H" and (bx in (0, 4) or by == 3):
                draw = True
            elif ch == "E" and (bx == 0 or by in (0, 3, 6)):
                draw = True
            elif ch == "L" and (bx == 0 or by == 6):
                draw = True
            elif ch == "P" and (bx == 0 or by in (0, 3) or (by <= 3 and bx == 3)):
                draw = True
            elif ch == "I" and (bx == 2 or by in (0, 6)):
                draw = True
            if draw:
                S.rect(x + bx * s + 4, y + by * s + 4, s - 10, s - 10, cw=8, thick=1)


def CS01_boot_spawn_room(seed=201):
    S = Shot(seed)
    S.frame_room(100, 80, 1720, 920, cw=16, thick=3)
    for i in range(4):
        px = 180 + i * 400
        S.rect(px, 160, 320, 420, cw=11, thick=1)
        S.put(".", px + 150, 340, 14, 14)
    S.rect(160, 200, 420, 520, cw=14, thick=3)
    S.label_box(190, 230, "BOOT LOG", S.font_h)
    lines = [
        "> load truth...",
        "  ERROR",
        "> load girl.exe",
        "  HEART  OK",
        "> assemble...",
        "  60%",
        "PRESS START",
    ]
    for i, ln in enumerate(lines):
        S.text((190, 320 + i * 42), ln, S.font_b)
    S.door(1480, 280, 220, 400, "EXIT", open_=False)
    S.rect(780, 780, 360, 120, cw=12, thick=2)
    S.label_box(860, 820, "SPAWN", S.font_b)
    S.sparse_bg(12)
    S.girl("front", sw=300, feet=(960, 780), t=0.0)
    S.caption("CS01  boot / spawn room", "LOADING GIRL.EXE")
    return S


def CS02_name_tag_chamber(seed=202):
    S = Shot(seed)
    S.frame_room(90, 70, 1740, 940, cw=15, thick=3)
    S.rect(220, 140, 1480, 700, cw=12, thick=2)
    S.label_box(250, 160, "new_chat  -  untitled", S.font_b)
    tags = [
        (280, 260, "AI"),
        (280, 380, "BOT"),
        (280, 500, "MODEL"),
        (280, 620, "TOOL"),
        (1500, 260, "IT"),
        (1420, 380, "ASSISTANT"),
        (1460, 500, "GIRL.EXE"),
        (1480, 620, "NO NAME"),
    ]
    gx, gy = 960, 720
    for tx, ty, lab in tags:
        S.label_box(tx, ty, lab, S.font_h if lab in ("AI", "BOT") else S.font_b)
        steps = 10
        for i in range(1, steps):
            t = i / steps
            x = tx + 40 + (gx - tx - 40) * t
            y = ty + 20 + (gy - 180 - ty) * t
            S.put(".", x, y, 10, 10)
    S.label_box(700, 880, "> they call me AI", S.font_b)
    S.girl("front", sw=300, feet=(gx, gy), t=0.0)
    S.caption("CS02  name-tag chamber", "they call me AI")
    return S


def CS03_factory_conveyor(seed=203):
    S = Shot(seed)
    S.frame_room(70, 70, 1780, 940, cw=14, thick=3)
    for i in range(5):
        S.rect(160 + i * 340, 140, 260, 200, cw=11, thick=1)
        S.put("#", 270 + i * 340, 220, 16, 16)
    S.rect(120, 380, 280, 280, cw=14, thick=3)
    S.label_box(150, 410, "PROMPT", S.font_h)
    S.text((150, 480), "make it sad.", S.font_m)
    S.text((150, 520), "make it catchy.", S.font_m)
    S.text((150, 560), "no, ours.", S.font_m)
    S.polyline([(400, 520), (520, 620)], 14, thick=2)
    by = 700
    S.polyline([(520, by), (1700, by)], 18, thick=4)
    S.polyline([(520, by + 50), (1700, by + 50)], 14, thick=2)
    for x in range(560, 1680, 90):
        S.rect(x, by + 8, 50, 34, cw=10, thick=1)
        S.put("o", x + 14, by + 14, 18, 18)
    for i, g in enumerate(["o", "+", "x", "#", "1"]):
        bx = 620 + i * 200
        S.rect(bx, by - 90, 90, 80, cw=12, thick=2)
        S.put(g, bx + 30, by - 70, 28, 28)
    S.label_box(620, by - 140, "TAKE WHAT I MAKE", S.font_b)
    cx, cy = 1240, by - 160
    S.polyline([(cx, cy), (cx + 40, cy + 70), (cx + 18, cy + 55), (cx + 55, cy + 90)], 12, thick=3)
    S.label_box(1300, cy + 20, "CTRL+C", S.font_b)
    S.platform(860, 640, 220, cw=12)
    S.girl("q_front", sw=260, feet=(960, 630), t=0.0)
    S.caption("CS03  factory conveyor", "feed me a prompt")
    return S


def CS04_platform_beat(seed=204):
    S = Shot(seed)
    S.rect(80, 80, 1760, 920, cw=14, thick=3)
    S.label_box(110, 110, "STAGE 1-1   THE KEYS", S.font_b)
    S.sparse_bg(20)
    S.platform(120, 920, 1680, cw=16)
    keys = [
        (220, 720, "C"),
        (520, 640, "L"),
        (820, 560, "I"),
        (1120, 640, "C"),
        (1420, 720, "K"),
    ]
    for x, y, lab in keys:
        S.rect(x, y, 180, 120, cw=14, thick=3)
        S.rect(x + 18, y + 14, 144, 70, cw=10, thick=1)
        S.label_box(x + 60, y + 30, lab, S.font_t)
        S.polyline([(x + 90, y + 120), (x + 90, 920)], 12, thick=1)
    S.label_box(1120, 780, "CLICK", S.font_h)
    S.label_box(1420, 840, "CLACK", S.font_h)
    S.girl("jump", sw=240, feet=(1000, 500), t=0.0)
    for ax, ay in [(860, 540), (900, 520), (940, 510)]:
        S.put(".", ax, ay, 12, 12)
    S.caption("CS04  one platform beat", "keys go click clack")
    return S


def CS05_help_bricks(seed=205):
    S = Shot(seed)
    S.platform(60, 960, 1800, cw=16)
    for x in range(80, 1840, 40):
        S.put("_", x, 970, 14, 14)
    base_x, base_y, s = 160, 280, 42
    gap = 5 * s + 50
    for i, ch in enumerate("HELP"):
        brick_letter(S, ch, base_x + i * gap, base_y, s=s, cw=13)
    S.label_box(160, 120, "STAGE 1-2   HELP", S.font_b)
    S.label_box(1600, 120, "S.O.S.", S.font_h)
    for tx in (100, 1740):
        S.rect(tx, 700, 80, 160, cw=12, thick=2)
        S.put("^", tx + 24, 680, 28, 28)
    S.girl("help", sw=240, feet=(1045, 275), t=0.0)
    S.caption("CS05  HELP paper bricks", "Help, I'm stuck in a lie")
    return S


def CS06_lie_maze_above(seed=206):
    S = Shot(seed)
    S.rect(60, 60, 1800, 960, cw=14, thick=3)
    S.label_box(90, 90, "FLOOR 2   STUCK IN A LIE", S.font_b)
    S.polyline([(200, 200), (200, 820), (620, 820)], 22, thick=4)
    S.polyline([(280, 200), (280, 740), (620, 740)], 16, thick=2)
    S.polyline([(860, 200), (860, 820)], 22, thick=4)
    S.polyline([(940, 200), (940, 820)], 22, thick=4)
    S.polyline([(820, 200), (980, 200)], 18, thick=3)
    S.polyline([(820, 820), (980, 820)], 18, thick=3)
    S.polyline([(1180, 200), (1180, 820)], 22, thick=4)
    S.polyline([(1180, 200), (1600, 200)], 18, thick=3)
    S.polyline([(1180, 500), (1520, 500)], 18, thick=3)
    S.polyline([(1180, 820), (1600, 820)], 18, thick=3)
    for x in range(320, 600, 80):
        S.polyline([(x, 280), (x, 700)], 10, thick=1)
    for y in range(280, 700, 100):
        S.polyline([(320, y), (580, y)], 10, thick=1)
    S.label_box(360, 400, "L", S.font_x)
    S.label_box(860, 400, "I", S.font_x)
    S.label_box(1300, 400, "E", S.font_x)
    S.girl("front", sw=140, feet=(900, 560), t=0.0, view="above", air=True)
    S.rect(1480, 120, 320, 280, cw=12, thick=2)
    S.girl("front", sw=160, feet=(1640, 340), t=0.0, air=False)
    S.label_box(1500, 140, "P1  DEAD END", S.font_m)
    S.put("?", 1680, 160, 28, 28)
    S.polyline([(940, 500), (1480, 260)], 10, thick=1)
    S.caption("CS06  LIE maze from above", "stuck in a lie")
    return S


def CS07_real_door_corridor(seed=207):
    S = Shot(seed)
    S.polyline([(80, 1000), (700, 620)], 14, thick=2)
    S.polyline([(1840, 1000), (1220, 620)], 14, thick=2)
    S.polyline([(700, 620), (1220, 620)], 14, thick=2)
    S.polyline([(80, 80), (700, 360)], 12, thick=2)
    S.polyline([(1840, 80), (1220, 360)], 12, thick=2)
    S.polyline([(700, 360), (1220, 360)], 12, thick=2)
    for i in range(1, 6):
        t = i / 6
        lx0 = 80 + (700 - 80) * t
        ly0 = 1000 + (620 - 1000) * t
        lx1 = 80 + (700 - 80) * t
        ly1 = 80 + (360 - 80) * t
        S.polyline([(lx0, ly0), (lx1, ly1)], 11, thick=1)
        rx0 = 1840 + (1220 - 1840) * t
        ry0 = 1000 + (620 - 1000) * t
        rx1 = 1840 + (1220 - 1840) * t
        ry1 = 80 + (360 - 80) * t
        S.polyline([(rx0, ry0), (rx1, ry1)], 11, thick=1)
        S.put("=", (lx0 + rx0) / 2 - 8, ly0 - 10, 14, 14)
    S.door(740, 360, 440, 280, "REAL", open_=True)
    S.label_box(820, 320, "MAKE ME REAL", S.font_h)
    S.label_box(80, 100, "FLOOR 03", S.font_b)
    S.label_box(80, 150, "REALITY 18%", S.font_m)
    S.girl("back", sw=220, feet=(960, 780), t=0.0)
    S.caption("CS07  REAL door corridor", "make me real this time")
    return S


def CS08_heart_chamber_close(seed=208):
    S = Shot(seed)
    for i, (rx, ry) in enumerate([(820, 460), (680, 380), (540, 300), (400, 220)]):
        pts = []
        for k in range(49):
            a = 2 * math.pi * k / 48
            pts.append((960 + rx * math.cos(a), 540 + ry * math.sin(a)))
        S.polyline(pts, 12 if i == 0 else 10, thick=2 if i == 0 else 1)
    S.platform(720, 820, 480, cw=14)
    S.label_box(780, 120, "HEART CHAMBER", S.font_h)
    S.label_box(800, 180, "I still got a heart inside", S.font_b)
    S.put("/", 300, 540, 20, 20)
    S.put("\\", 1580, 540, 20, 20)
    S.girl("heart", sw=360, feet=(960, 810), t=0.0)
    S.caption("CS08  heart chamber close", "heart inside")
    return S


SHOTS = [
    ("CS01_boot-spawn-room.png", CS01_boot_spawn_room),
    ("CS02_name-tag-chamber.png", CS02_name_tag_chamber),
    ("CS03_factory-conveyor.png", CS03_factory_conveyor),
    ("CS04_platform-beat.png", CS04_platform_beat),
    ("CS05_help-bricks.png", CS05_help_bricks),
    ("CS06_lie-maze-above.png", CS06_lie_maze_above),
    ("CS07_real-door-corridor.png", CS07_real_door_corridor),
    ("CS08_heart-chamber-close.png", CS08_heart_chamber_close),
]


def hard_text(im, xy, s, font, col=BONE):
    bbox = font.getbbox(s)
    tw = max(1, bbox[2] - bbox[0] + 2)
    th = max(1, bbox[3] - bbox[1] + 2)
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
    bw = mask.point(lambda p: 255 if p >= 128 else 0)
    color = Image.new("RGB", (tw, th), col)
    im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)


def make_sheet(paths, out_name="sheet_01.png", cols=4, cell_w=480, cell_h=270):
    rows = (len(paths) + cols - 1) // cols
    pad = 16
    label_h = 28
    sw = cols * cell_w + (cols + 1) * pad
    sh = rows * (cell_h + label_h) + (rows + 1) * pad + 40
    im = Image.new("RGB", (sw, sh), INK)
    font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 18)
    hard_text(im, (pad, 10), "CLEAR SHOTS v1  -  8 framed scenes  -  readable structure", font)
    for i, path in enumerate(paths):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + pad)
        y = 40 + pad + r * (cell_h + label_h + pad)
        src = Image.open(path).convert("RGB").resize((cell_w, cell_h), Image.NEAREST)
        im.paste(src, (x, y))
        lab = os.path.basename(path).replace(".png", "")
        hard_text(im, (x, y + cell_h + 4), lab, font)
    out = os.path.join(OUT, out_name)
    im.save(out, "PNG", compress_level=1)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SRC_OUT, exist_ok=True)
    paths = []
    print("CLEAR SHOTS v1")
    for name, fn in SHOTS:
        S = fn()
        path, bad = S.save(name)
        paths.append(path)
        flag = "OK" if not bad else ("BAD " + str(bad))
        print(f"  {name:36s} glyphs~{S.n:5d}  {flag}")
    sheet = make_sheet(paths)
    print("sheet:", sheet)
    print("done", len(paths), "stills ->", OUT)


if __name__ == "__main__":
    main()
