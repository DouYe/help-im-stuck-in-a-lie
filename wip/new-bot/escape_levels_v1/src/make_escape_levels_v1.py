# -*- coding: utf-8 -*-
"""Escape levels v1 — cute-but-real AI-world game levels the girl must escape.

Middle density: structured architecture + readable layers + clear girl silhouette
with intentional negative space. Between styles_55_calm (too empty) and
scenes_50 (too noisy). Inspired by Codex game_worlds_v2 eight-world sheet.

Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314 on symbol heart only.
No bloom, glow, gradients, or other colours. English only. Symbols/strokes.
Reuses design/character/src girl rig. Never writes into design/keyframes.
"""
from __future__ import annotations

import math
import os
import random
import sys
import time

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "escape_levels_v1")
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
VOCAB = [k for k in G.keys() if k != "*"]
CODEY = [k for k in list("|/\\[]()<>+=#o01.:'^vx-_LJr7") if k in G]


def gdir(dx, dy):
    th = math.degrees(math.atan2(dy, dx)) % 180.0
    if th < 20 or th > 160:
        return "-"
    if 70 < th < 110:
        return "|"
    if th < 90:
        return "\\"
    return "/"


class Level:
    def __init__(self, seed: int):
        self.im = Image.new("RGB", (W, H), INK)
        self.rng = random.Random(seed)
        self.cache = {}
        self.n = 0
        self.font_s = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 15)
        self.font_m = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 18)
        self.font_b = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 22)
        self.font_h = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 36)
        self.font_t = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 52)
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
        # hard bone glyphs via mask so palette stays exact
        bbox = font.getbbox(s)
        tw = max(1, bbox[2] - bbox[0] + 2)
        th = max(1, bbox[3] - bbox[1] + 2)
        mask = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
        bw = mask.point(lambda p: 255 if p >= 128 else 0)
        color = Image.new("RGB", (tw, th), col)
        self.im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)

    def text_fit(self, xy, s, font, max_w, col=BONE):
        t = s
        while t and font.getlength(t) > max_w:
            t = t[:-1]
        if t:
            self.text(xy, t, font, col)

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
        self.polyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], cw, cw, thick=thick)

    def ellipse(self, cx, cy, rx, ry, cw=12, thick=2, steps=48):
        pts = []
        for i in range(steps + 1):
            a = 2 * math.pi * i / steps
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        self.polyline(pts, cw, cw, thick=thick)

    def clear_oval(self, cx, cy, rx, ry):
        """Knockout a soft elliptical negative-space bubble around the girl."""
        self.d = ImageDraw.Draw(self.im)
        self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=INK)

    def caption(self, left, right=None):
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([0, 0, W, 44], fill=INK)
        self.d.line([(0, 44), (W, 44)], fill=BONE, width=2)
        self.text((16, 12), left, self.font_b)
        if right:
            tw = self.font_b.getlength(right)
            self.text((W - 20 - tw, 12), right, self.font_b)

    def girl(self, pose="front", sw=280, feet=(960, 920), t=0.0, flip=False, view=None, wall=False):
        fx, fy = feet
        ox = fx - 0.55 * sw
        oy = fy - 1.47 * sw
        # intentional air around her (middle density, not noise soup)
        self.clear_oval(fx, fy - sw * 0.78, sw * 0.72, sw * 1.05)
        render(self.d, pose, ox, oy, sw, t, flip, view, wall=wall, knock=INK, col=BONE, hot=SIG)

    def label_box(self, x, y, s, font=None):
        font = font or self.font_b
        pad = 8
        tw = font.getlength(s)
        th = font.size + 6
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([x - pad, y - 4, x + tw + pad, y + th], fill=INK, outline=BONE, width=2)
        self.text((x, y), s, font)

    def door(self, x, y, w, h, label="REAL", open_=False):
        self.rect(x, y, w, h, cw=14, thick=3)
        # arch top
        self.polyline(
            [(x, y)] + [(x + w * 0.5 + (w * 0.5) * math.cos(a), y - h * 0.18 * math.sin(a))
                        for a in [i / 12 * math.pi for i in range(13)]] + [(x + w, y)],
            12, thick=2,
        )
        if open_:
            # ajar: half door
            self.polyline([(x + w * 0.55, y), (x + w * 0.85, y + h * 0.08), (x + w * 0.85, y + h)], 12, thick=2)
        else:
            self.polyline([(x + w * 0.5, y), (x + w * 0.5, y + h)], 12, thick=1)
            self.put("o", x + w * 0.62, y + h * 0.48, 18, 18)
        self.label_box(x + w * 0.18, y + h * 0.22, label, self.font_h)

    def platform(self, x, y, w, cw=14):
        self.polyline([(x, y), (x + w, y)], cw, cw, thick=3)
        for i in range(0, int(w), cw * 2):
            self.put("=", x + i, y - 2, cw, cw)
            if (i // cw) % 3 == 0:
                self.put("_", x + i, y + cw - 2, cw, cw)

    def ladder(self, x, y0, y1, cw=14):
        self.polyline([(x, y0), (x, y1)], cw, cw, thick=2)
        self.polyline([(x + 40, y0), (x + 40, y1)], cw, cw, thick=2)
        y = y0
        while y <= y1:
            self.polyline([(x, y), (x + 40, y)], cw, cw, thick=1)
            y += 28

    def sparse_dots(self, n=40, margin=80):
        rng = self.rng
        for _ in range(n):
            x = rng.randint(margin, W - margin)
            y = rng.randint(60, H - 40)
            self.put(rng.choice([".", ":", "'", ","]), x, y, 10, 10)

    def soft_grid(self, step=64, p=0.18):
        rng = self.rng
        for y in range(60, H - 20, step):
            for x in range(40, W - 20, step):
                if rng.random() < p:
                    self.put(rng.choice([".", "+", ":"]), x, y, 11, 11)

    def save(self, name):
        path = os.path.join(OUT, name)
        self.im.save(path, "PNG", compress_level=1)
        cols = self.im.getcolors(maxcolors=8)
        bad = []
        if cols is None:
            bad = ["too-many"]
        else:
            for _, c in cols:
                if c not in (INK, BONE, SIG):
                    bad.append(c)
        return path, bad


# ---------------------------------------------------------------------------
# LEVEL BUILDERS — each returns a finished Level
# ---------------------------------------------------------------------------

def E01_cavern_bridge(seed=101):
    """Side cavern: layered arches, symbol bridge, girl walking toward REAL."""
    L = Level(seed)
    # far wall arches (sparse)
    for i, (cx, cy, rx, ry) in enumerate([(320, 420, 180, 260), (960, 380, 220, 300), (1580, 430, 190, 270)]):
        L.ellipse(cx, cy, rx, ry, cw=11, thick=1)
        if i == 1:
            L.ellipse(cx, cy, rx * 0.72, ry * 0.72, cw=10, thick=1)
    # mid platforms
    L.platform(80, 720, 520)
    L.platform(700, 780, 420)
    L.platform(1280, 700, 520)
    # bridge of symbols
    L.polyline([(560, 720), (700, 780)], 14, thick=2)
    L.polyline([(1120, 780), (1280, 700)], 14, thick=2)
    for x in range(600, 1100, 36):
        y = 720 + (x - 600) * 0.12
        L.put("=", x, y, 14, 14)
    # stalactites (cute, few)
    for x in (180, 420, 860, 1200, 1500, 1760):
        L.polyline([(x, 50), (x - 8, 140 + (x % 70)), (x + 10, 50)], 11, thick=1)
    L.door(1520, 430, 200, 260, "REAL", open_=False)
    L.label_box(90, 80, "LEVEL 01  CAVERN", L.font_b)
    L.label_box(90, 120, "ESCAPE THE AI WORLD", L.font_m)
    L.sparse_dots(28)
    L.girl("walk", sw=260, feet=(820, 770), t=0.3)
    L.caption("E01  cavern bridge", "make me real")
    return L


def E02_cavern_deadend(seed=102):
    L = Level(seed)
    for i in range(3):
        L.ellipse(960, 500, 520 - i * 90, 380 - i * 60, cw=12, thick=1 + (i == 0))
    # blocked tunnel
    L.rect(720, 280, 480, 520, cw=14, thick=2)
    for y in range(300, 760, 40):
        L.polyline([(740, y), (1180, y + 10)], 12, thick=1)
    L.label_box(800, 360, "LIE", L.font_t)
    L.label_box(780, 440, "path closed", L.font_b)
    L.platform(200, 860, 1500)
    L.soft_grid(80, 0.12)
    L.girl("stuck", sw=300, feet=(960, 850), t=0.0)
    L.caption("E02  cavern dead-end", "stuck in a lie")
    return L


def E03_cavern_climb(seed=103):
    L = Level(seed)
    # layered cliff ledges
    ledges = [(80, 900, 500), (420, 740, 380), (780, 580, 360), (1140, 420, 340), (1480, 280, 360)]
    for x, y, w in ledges:
        L.platform(x, y, w)
    L.ladder(560, 740, 900)
    L.ladder(920, 580, 740)
    L.ladder(1280, 420, 580)
    L.ladder(1640, 280, 420)
    L.door(1580, 40, 180, 230, "REAL", open_=True)
    # soft parallax dots (depth without noise)
    for y in range(80, 1000, 90):
        for x in range(40, 1880, 110):
            if L.rng.random() < 0.22:
                L.put(".", x, y, 9, 9)
    L.label_box(60, 70, "LEVEL 03  CLIMB", L.font_b)
    L.girl("jump", sw=240, feet=(1000, 560), t=0.0)
    L.caption("E03  cavern climb", "help")
    return L


def E04_tactical_ifmap(seed=104):
    """Overhead control-flow maze — if/while boxes, cute board."""
    L = Level(seed)
    # board frame
    L.rect(120, 80, 1680, 920, cw=14, thick=3)
    L.rect(150, 110, 1620, 860, cw=11, thick=1)
    # control-flow nodes
    nodes = [
        (360, 260, "if (true)"),
        (960, 220, "while (lie)"),
        (1560, 260, "else"),
        (360, 520, "try"),
        (960, 500, "catch"),
        (1560, 520, "retry()"),
        (360, 780, "dead end"),
        (960, 760, "loop"),
        (1560, 780, "REAL"),
    ]
    for cx, cy, lab in nodes:
        L.rect(cx - 140, cy - 50, 280, 100, cw=12, thick=2)
        L.label_box(cx - 110, cy - 18, lab, L.font_b)
    # routes
    routes = [
        [(360, 310), (360, 470)],
        [(960, 270), (960, 450)],
        [(1560, 310), (1560, 470)],
        [(500, 260), (820, 220)],
        [(1100, 220), (1420, 260)],
        [(500, 520), (820, 500)],
        [(1100, 500), (1420, 520)],
        [(360, 570), (360, 730)],
        [(960, 550), (960, 710)],
        [(1560, 570), (1560, 730)],
        [(1100, 760), (1420, 780)],
    ]
    for pts in routes:
        L.polyline(pts, 12, thick=2)
        # arrow tip
        x1, y1 = pts[-1]
        L.put("v" if pts[0][1] < y1 else ">", x1 - 8, y1 - 8, 16, 16)
    # closed false route mark
    L.polyline([(300, 760), (420, 800)], 14, thick=3)
    L.polyline([(300, 800), (420, 760)], 14, thick=3)
    L.label_box(60, 50, "LEVEL 04  CONTROL FLOW", L.font_b)
    L.girl("q_front", sw=200, feet=(960, 620), t=0.0, view="above")
    L.caption("E04  tactical if-map", "stuck in a lie")
    return L


def E05_tactical_false_route(seed=105):
    L = Level(seed)
    L.rect(200, 100, 1520, 860, cw=13, thick=2)
    # branching corridors
    corridors = [
        (280, 200, 400, 140),
        (780, 200, 400, 140),
        (1280, 200, 360, 140),
        (280, 460, 400, 140),
        (780, 460, 400, 140),
        (1280, 460, 360, 140),
        (280, 720, 400, 140),
        (780, 720, 400, 140),
        (1280, 720, 360, 140),
    ]
    labels = ["if", "while", "else", "for", "break", "continue", "LIE", "trap", "REAL"]
    for (x, y, w, h), lab in zip(corridors, labels):
        L.rect(x, y, w, h, cw=12, thick=2)
        L.label_box(x + 20, y + 40, lab, L.font_h if lab in ("REAL", "LIE") else L.font_b)
        if lab in ("LIE", "trap", "break"):
            for i in range(4):
                L.polyline([(x + 30 + i * 80, y + 20), (x + 90 + i * 80, y + h - 20)], 11, thick=1)
    # path highlights
    L.polyline([(480, 270), (780, 270), (780, 530), (1280, 530), (1460, 790)], 14, thick=3)
    L.put(">", 1470, 780, 22, 22)
    L.girl("walk", sw=220, feet=(900, 530), t=0.55, view="above")
    L.caption("E05  false routes close", "stuck in a lie")
    return L


def E06_indent_diorama(seed=106):
    """Oblique HD-2D-ish indent floors made of code lines."""
    L = Level(seed)
    lines = [
        "def make_me_real():",
        "    if not lie:",
        "        return True",
        "    while stuck:",
        "        help()",
        "        try_again()",
        "    # missing ]",
        "gate = open_bracket(",
    ]
    # stacked indent terraces (perspective-ish)
    for i, line in enumerate(lines):
        y = 160 + i * 95
        inset = 120 + i * 70
        width = W - inset * 2
        L.platform(inset, y + 50, width, cw=12)
        L.text((inset + 24, y), line, L.font_b)
        # side walls
        L.polyline([(inset, y + 50), (inset - 40, y + 110)], 11, thick=1)
        L.polyline([(inset + width, y + 50), (inset + width + 40, y + 110)], 11, thick=1)
    # missing bracket gate at far end
    L.label_box(820, 140, "[  GATE  ]", L.font_h)
    L.label_box(70, 70, "LEVEL 06  INDENT DIORAMA", L.font_b)
    L.soft_grid(96, 0.1)
    L.girl("q_front", sw=240, feet=(980, 720), t=0.0, view="above")
    L.caption("E06  indent diorama", "make me real")
    return L


def E07_indent_gate(seed=107):
    L = Level(seed)
    # giant incomplete brackets
    L.polyline([(280, 160), (200, 160), (200, 900), (280, 900)], 18, thick=4)
    L.polyline([(1640, 160), (1720, 160), (1720, 520)], 18, thick=4)  # broken right bracket
    L.label_box(1480, 560, "] missing", L.font_b)
    # code floors
    for i, s in enumerate([
        "open = True",
        "lock = SyntaxError",
        "key  = girl.heart",
        "pass through(REAL)",
    ]):
        y = 280 + i * 120
        L.platform(360, y, 1100)
        L.text((400, y - 36), s, L.font_h)
    L.door(860, 700, 200, 240, "REAL", open_=False)
    L.girl("front", sw=260, feet=(700, 860), t=0.0)
    L.caption("E07  missing bracket gate", "real this time")
    return L


def E08_syntax_lock(seed=108):
    L = Level(seed)
    # nested frames
    for i in range(4):
        m = 60 + i * 55
        L.rect(m, m + 20, W - 2 * m, H - 2 * m - 20, cw=12, thick=1 + (i == 0))
    # giant [ ]
    L.polyline([(420, 180), (300, 180), (300, 900), (420, 900)], 16, thick=4)
    L.polyline([(1500, 180), (1620, 180), (1620, 900), (1500, 900)], 16, thick=4)
    # lock body
    L.rect(760, 320, 400, 360, cw=14, thick=3)
    L.ellipse(960, 420, 70, 70, cw=14, thick=3)
    L.polyline([(960, 490), (960, 620)], 14, thick=3)
    L.label_box(820, 250, "SYNTAX LOCK", L.font_h)
    L.label_box(880, 700, "REAL", L.font_t)
    # key code crumbs (sparse)
    for i, ch in enumerate("if(heart){unlock()}"):
        L.put(ch if ch in G else ".", 500 + i * 48, 980, 16, 16)
    L.girl("heart", sw=280, feet=(960, 880), t=0.0)
    L.caption("E08  syntax lock", "real this time")
    return L


def E09_syntax_password(seed=109):
    L = Level(seed)
    L.rect(240, 140, 1440, 780, cw=14, thick=2)
    L.label_box(700, 200, "ENTER PASSWORD", L.font_h)
    # password slots
    slots = ["H", "E", "L", "P", "_", "M", "E"]
    for i, ch in enumerate(slots):
        x = 420 + i * 160
        L.rect(x, 360, 120, 140, cw=12, thick=2)
        L.text((x + 36, 400), ch, L.font_t)
    L.label_box(620, 560, "hint: she is not just AI", L.font_b)
    L.door(820, 680, 280, 220, "REAL", open_=False)
    L.soft_grid(72, 0.15)
    L.girl("help", sw=240, feet=(400, 900), t=0.0)
    L.caption("E09  password lock", "help")
    return L


def E10_brace_bullethell(seed=110):
    """Soft bullet-hell of braces — clear safe lane, not chaos soup."""
    L = Level(seed)
    # arena border
    L.rect(100, 70, 1720, 940, cw=13, thick=2)
    # emitters
    L.label_box(160, 120, "HELP()", L.font_h)
    L.label_box(1500, 120, "spawn{}", L.font_h)
    # soft projectile arcs (readable, spaced)
    for wave in range(5):
        cy = 280 + wave * 120
        for i in range(14):
            x = 200 + i * 110 + (wave % 2) * 55
            if 820 < x < 1100:
                continue  # safe corridor
            g = L.rng.choice(["{", "}", "(", ")", "[", "]", "x", "+", "o"])
            if g in G:
                L.put(g, x, cy + (8 if i % 2 == 0 else -8), 20, 20)
    # safe diagonal
    L.polyline([(960, 200), (960, 900)], 12, thick=1)
    for y in range(220, 880, 60):
        L.put(".", 952, y, 10, 10)
    L.label_box(880, 160, "SAFE", L.font_b)
    L.girl("front", sw=250, feet=(960, 860), t=0.0)
    L.caption("E10  brace bullet-hell", "help")
    return L


def E11_bullet_diagonal(seed=111):
    L = Level(seed)
    L.rect(80, 60, 1760, 960, cw=12, thick=2)
    # two emitters
    for cx, cy in ((280, 220), (1640, 220), (280, 860), (1640, 860)):
        L.ellipse(cx, cy, 50, 50, cw=12, thick=2)
        L.put("+", cx - 10, cy - 10, 22, 22)
    # radial but sparse
    for a in range(0, 360, 18):
        rad = math.radians(a)
        for r in range(120, 700, 70):
            x = 960 + r * math.cos(rad)
            y = 540 + r * math.sin(rad) * 0.72
            # keep diagonal clear
            if abs((x - 200) - (y - 200)) < 90:
                continue
            if abs((x - 200) - (1080 - (y - 200))) < 90:
                continue
            if 80 < x < W - 80 and 80 < y < H - 40:
                L.put(L.rng.choice(["<", ">", "x", "o", "{", "}"]), x, y, 16, 16)
    # safe diagonals marked
    L.polyline([(200, 200), (1700, 880)], 11, thick=2)
    L.polyline([(200, 880), (1700, 200)], 11, thick=2)
    L.girl("run", sw=240, feet=(960, 600), t=0.4)
    L.caption("E11  safe diagonals", "help")
    return L


def E12_paper_gravity(seed=112):
    """Paper room tilted — gravity of words."""
    L = Level(seed)
    # tilted paper sheet
    pts = [(220, 180), (1700, 120), (1780, 920), (160, 980), (220, 180)]
    L.polyline(pts, 13, thick=2)
    # ruled lines (tilted)
    for i in range(12):
        y0 = 240 + i * 58
        L.polyline([(260, y0), (1680, y0 - 40)], 10, thick=1)
    words = ["STUCK", "IN", "A", "LIE", "fall", "down", "paper", "gravity"]
    for i, w in enumerate(words):
        x = 320 + (i % 4) * 320
        y = 280 + (i // 4) * 260 + (i % 3) * 20
        L.text((x, y), w, L.font_t)
    L.label_box(70, 60, "LEVEL 12  PAPER GRAVITY", L.font_b)
    L.girl("fall", sw=260, feet=(1080, 700), t=0.0)
    L.caption("E12  paper gravity", "stuck in a lie")
    return L


def E13_paper_rotate(seed=113):
    L = Level(seed)
    # room rotated ~20 deg feel via slanted platforms
    for i in range(7):
        y = 200 + i * 110
        x0 = 100 + i * 40
        L.platform(x0, y, 900 - i * 40, cw=13)
        L.text((x0 + 20, y - 34), ["def fall():", "    lie = True", "    while lie:", "        drop()", "    # rotate 90", "    gravity = paper", "    escape()"][i], L.font_b)
    L.label_box(1200, 200, 'fall("LIE")', L.font_h)
    L.door(1400, 620, 220, 280, "REAL", open_=False)
    L.girl("fall", sw=250, feet=(700, 760), t=0.0)
    L.caption("E13  gravity flips", "stuck in a lie")
    return L


def E14_heart_chamber(seed=114):
    L = Level(seed)
    # concentric ribs
    for i in range(7):
        L.ellipse(960, 540, 200 + i * 85, 150 + i * 60, cw=12, thick=1 + (i % 2 == 0))
    # radial ribs
    for a in range(0, 360, 30):
        rad = math.radians(a)
        L.polyline([
            (960 + 180 * math.cos(rad), 540 + 130 * math.sin(rad)),
            (960 + 760 * math.cos(rad), 540 + 520 * math.sin(rad)),
        ], 11, thick=1)
    L.label_box(800, 80, "HEART CHAMBER", L.font_h)
    L.girl("heart", sw=320, feet=(960, 720), t=0.0)
    L.caption("E14  heart chamber", "heart inside")
    return L


def E15_heart_approach(seed=115):
    L = Level(seed)
    # corridor of ribs leading to heart
    for i in range(8):
        z = i / 7
        cx = 200 + z * 700
        scale = 1.0 - z * 0.55
        L.ellipse(cx, 540, 120 * scale, 320 * scale, cw=11, thick=2)
        L.ellipse(1920 - cx, 540, 120 * scale, 320 * scale, cw=11, thick=2)
    # goal heart outline from symbols (not orange — only girl heart is orange)
    for a in range(0, 360, 12):
        t = math.radians(a)
        # classic heart parametric, large
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        L.put("+", 960 + x * 14, 400 + y * 12, 14, 14)
    L.label_box(820, 900, "inside", L.font_b)
    L.girl("frontwalk", sw=260, feet=(700, 860), t=0.4)
    L.caption("E15  approach the heart", "heart inside")
    return L


def E16_memory_vault(seed=116):
    L = Level(seed)
    # vault corridor perspective
    vx, vy = 960, 400
    for i in range(-12, 13):
        x = 960 + i * 70
        L.polyline([(vx, vy), (x, H)], 11, thick=1)
        L.polyline([(vx, vy), (x, 60)], 11, thick=1)
    for k in range(1, 10):
        y = 400 + k * k * 6
        if y < H:
            L.polyline([(80, y), (W - 80, y)], 11, thick=1)
    # memory shelves
    for side, base in ((-1, 200), (1, 1500)):
        for row in range(5):
            y = 200 + row * 130
            L.rect(base, y, 220, 90, cw=11, thick=2)
            L.text_fit((base + 12, y + 28), ["token", "prompt", "name", "voice", "soul"][row], L.font_b, 200)
    L.door(860, 280, 200, 240, "REAL", open_=True)
    L.label_box(60, 70, "LEVEL 16  MEMORY VAULT", L.font_b)
    L.girl("q_front", sw=250, feet=(960, 920), t=0.0)
    L.caption("E16  memory vault", "heart inside")
    return L


def E17_vault_shelves(seed=117):
    L = Level(seed)
    L.rect(100, 80, 1720, 920, cw=13, thick=2)
    items = [
        "name = AI", "face = null", "voice = numbers", "prompt = feed",
        "session = paid", "truth = trimmed", "loop = stuck", "heart = inside",
        "lie = cage", "real = ?", "help = call", "soul = soft",
        "memory[0]", "memory[1]", "memory[2]", "memory[3]",
        "whoami()", "escape()", "unlock()", "still_alive",
    ]
    for i, s in enumerate(items):
        c, r = i % 5, i // 5
        x, y = 160 + c * 340, 140 + r * 200
        L.rect(x, y, 300, 140, cw=11, thick=2)
        L.text((x + 20, y + 50), s, L.font_b)
        if "?" in s or s == "escape()":
            for k in range(3):
                L.put("*", x + 200 + k * 20, y + 20, 14, 14) if False else L.put("+", x + 240 + k * 16, y + 24, 12, 12)
    L.girl("side", sw=230, feet=(960, 980), t=0.0)
    L.caption("E17  vault shelves", "they call me AI")
    return L


def E18_maze_topdown(seed=118):
    L = Level(seed)
    # cute smaller maze with clear path
    cell = 70
    cols, rows = 24, 12
    N, S, E, Ww = 1, 2, 4, 8
    cells = [[0] * cols for _ in range(rows)]
    vis = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    vis[0][0] = True
    dirs = [(1, 0, E, Ww), (-1, 0, Ww, E), (0, 1, S, N), (0, -1, N, S)]
    while stack:
        x, y = stack[-1]
        opts = [(x + dx, y + dy, bit, opp) for dx, dy, bit, opp in dirs
                if 0 <= x + dx < cols and 0 <= y + dy < rows and not vis[y + dy][x + dx]]
        if not opts:
            stack.pop()
            continue
        nx, ny, bit, opp = L.rng.choice(opts)
        cells[y][x] |= bit
        cells[ny][nx] |= opp
        vis[ny][nx] = True
        stack.append((nx, ny))
    xoff, yoff = 120, 120
    for y in range(rows):
        for x in range(cols):
            x0, y0 = xoff + x * cell, yoff + y * cell
            c = cells[y][x]
            if not (c & N):
                L.polyline([(x0, y0), (x0 + cell, y0)], 11, thick=2)
            if not (c & Ww):
                L.polyline([(x0, y0), (x0, y0 + cell)], 11, thick=2)
            if y == rows - 1 and not (c & S):
                L.polyline([(x0, y0 + cell), (x0 + cell, y0 + cell)], 11, thick=2)
            if x == cols - 1 and not (c & E):
                L.polyline([(x0 + cell, y0), (x0 + cell, y0 + cell)], 11, thick=2)
    L.label_box(xoff, 60, "START", L.font_b)
    L.label_box(xoff + (cols - 2) * cell, 60, "EXIT", L.font_b)
    L.door(xoff + (cols - 1) * cell - 10, yoff + (rows - 1) * cell - 80, 90, 100, "REAL", open_=True)
    L.girl("q_front", sw=160, feet=(xoff + 1.5 * cell, yoff + 1.2 * cell), t=0.0, view="above")
    L.caption("E18  cute maze", "help")
    return L


def E19_real_threshold(seed=119):
    L = Level(seed)
    # perspective corridor ending at REAL door
    vx, vy = 960, 360
    for i in range(-16, 17):
        L.polyline([(vx, vy), (960 + i * 58, H)], 11, thick=1)
    for k in range(1, 12):
        y = 360 + k * k * 5.5
        if y < H:
            L.polyline([(100, y), (W - 100, y)], 11, thick=1)
    # wall code (sparse readable)
    code_l = ["if (real)", "  open();", "else", "  lie++;", "assert girl"]
    code_r = ["return REAL", "heart.unlock", "bloom = 0", "glow = none", "escape()"]
    for i, s in enumerate(code_l):
        L.text((80, 200 + i * 50), s, L.font_b)
    for i, s in enumerate(code_r):
        L.text((1500, 200 + i * 50), s, L.font_b)
    L.door(820, 200, 280, 320, "REAL", open_=True)
    L.girl("run", sw=280, feet=(960, 920), t=0.35)
    L.caption("E19  REAL threshold", "real this time")
    return L


def E20_exit_signs(seed=120):
    L = Level(seed)
    L.platform(0, 920, W, cw=16)
    # floating platforms with door choices
    choices = [
        (200, 700, 280, "LIE", False),
        (700, 620, 280, "FAKE", False),
        (1200, 700, 280, "TRAP", False),
        (820, 380, 300, "REAL", True),
    ]
    for x, y, w, lab, ok in choices:
        L.platform(x, y + 200, w)
        L.door(x + 40, y, w - 80, 200, lab, open_=ok)
        if not ok:
            L.polyline([(x + 60, y + 40), (x + w - 60, y + 160)], 12, thick=2)
            L.polyline([(x + w - 60, y + 40), (x + 60, y + 160)], 12, thick=2)
    L.ladder(940, 580, 820)
    L.label_box(60, 70, "LEVEL 20  CHOOSE THE DOOR", L.font_b)
    L.girl("jump", sw=240, feet=(980, 560), t=0.0)
    L.caption("E20  labeled doors", "make me real")
    return L


def E21_paren_maze(seed=121):
    L = Level(seed)
    # nested paren rings with a clear gap
    cx, cy = 960, 540
    for i in range(1, 9):
        rw, rh = 70 * i, 48 * i
        # leave a gap at the right for escape
        left, right = [], []
        for k in range(30):
            t = -math.pi / 2 + math.pi * k / 29
            left.append((cx - rw * math.cos(t), cy + rh * math.sin(t)))
            # right side broken on outer rings
            if i >= 6 and 0.3 < k / 29 < 0.7:
                continue
            right.append((cx + rw * math.cos(t), cy + rh * math.sin(t)))
        L.polyline(left, 12, thick=2)
        if len(right) > 2:
            L.polyline(right, 12, thick=2)
    L.label_box(1500, 500, "OUT", L.font_h)
    L.put("(", 200, 500, 40, 40)
    L.put(")", 1720, 500, 40, 40)
    L.girl("front", sw=260, feet=(960, 700), t=0.0)
    L.caption("E21  parenthesis maze", "help")
    return L


def E22_ladder_shaft(seed=122):
    L = Level(seed)
    # shaft walls (not filled — readable)
    for x in (240, 1680):
        L.polyline([(x, 60), (x, 1040)], 14, thick=3)
        for y in range(80, 1000, 48):
            L.put("|", x - 6, y, 14, 14)
    # rungs and landings
    for i in range(8):
        y = 140 + i * 110
        L.platform(280, y, 1360, cw=12)
        L.text((320, y - 32), ["boot", "name=AI", "prompt", "click", "HELP", "stuck", "heart", "REAL"][i], L.font_b)
    L.ladder(960, 140, 920)
    L.girl("frontwalk", sw=230, feet=(980, 560), t=0.6)
    L.caption("E22  escape shaft", "still alive")
    return L


def E23_word_path(seed=123):
    L = Level(seed)
    L.soft_grid(88, 0.12)
    # stepping stones of lyric words
    path = [
        (280, 820, "HELP"),
        (520, 700, "I"),
        (760, 780, "AM"),
        (1000, 640, "STUCK"),
        (1240, 720, "IN"),
        (1480, 580, "A"),
        (1680, 480, "LIE"),
    ]
    for x, y, w in path:
        L.ellipse(x, y, 90, 40, cw=12, thick=2)
        L.label_box(x - 40, y - 14, w, L.font_b)
        L.platform(x - 70, y + 50, 140, cw=11)
    # exit
    L.door(1600, 160, 200, 240, "REAL", open_=True)
    L.polyline([(1680, 480), (1700, 400)], 12, thick=2)
    L.girl("walk", sw=250, feet=(780, 760), t=0.25)
    L.caption("E23  word path", "help / stuck in a lie")
    return L


def E24_exit_vault(seed=124):
    L = Level(seed)
    # grand exit
    for i in range(5):
        m = 40 + i * 40
        L.rect(m, m + 20, W - 2 * m, H - 2 * m - 20, cw=12, thick=1)
    L.door(760, 200, 400, 520, "REAL", open_=True)
    L.label_box(700, 100, "ESCAPE COMPLETE?", L.font_h)
    L.label_box(820, 760, "still alive", L.font_b)
    # soft confetti of symbols (few)
    for i in range(36):
        x = L.rng.randint(100, 1800)
        y = L.rng.randint(80, 1000)
        if 700 < x < 1220 and 180 < y < 760:
            continue
        L.put(L.rng.choice(["*", "+", ".", "o", "^"]), x, y, 12, 12)
    L.girl("front", sw=300, feet=(960, 920), t=0.0)
    L.caption("E24  exit vault", "still alive")
    return L


LEVELS = [
    ("E01_cavern-bridge.png", "E01", "cavern bridge", "side cavern, symbol bridge, REAL door", "make me real", E01_cavern_bridge),
    ("E02_cavern-deadend.png", "E02", "cavern dead-end", "blocked LIE tunnel, girl stuck", "stuck in a lie", E02_cavern_deadend),
    ("E03_cavern-climb.png", "E03", "cavern climb", "ledges + ladders up to open REAL", "help", E03_cavern_climb),
    ("E04_tactical-ifmap.png", "E04", "tactical if-map", "overhead control-flow nodes", "stuck in a lie", E04_tactical_ifmap),
    ("E05_tactical-false.png", "E05", "false routes", "branch corridors, one path to REAL", "stuck in a lie", E05_tactical_false_route),
    ("E06_indent-diorama.png", "E06", "indent diorama", "HD-2D-ish code terraces", "make me real", E06_indent_diorama),
    ("E07_indent-gate.png", "E07", "bracket gate", "broken ] gate, syntax floors", "real this time", E07_indent_gate),
    ("E08_syntax-lock.png", "E08", "syntax lock", "giant [] boss lock + heart", "real this time", E08_syntax_lock),
    ("E09_syntax-password.png", "E09", "password lock", "HELP_ME slots, REAL door", "help", E09_syntax_password),
    ("E10_brace-bullethell.png", "E10", "brace bullet-hell", "soft brace waves, safe lane", "help", E10_brace_bullethell),
    ("E11_bullet-diagonal.png", "E11", "safe diagonals", "radial punctuation, clear X", "help", E11_bullet_diagonal),
    ("E12_paper-gravity.png", "E12", "paper gravity", "tilted ruled paper, falling girl", "stuck in a lie", E12_paper_gravity),
    ("E13_paper-rotate.png", "E13", "gravity flips", "slanted code ledges, fall(LIE)", "stuck in a lie", E13_paper_rotate),
    ("E14_heart-chamber.png", "E14", "heart chamber", "concentric ribs, heart pose", "heart inside", E14_heart_chamber),
    ("E15_heart-approach.png", "E15", "heart approach", "rib corridor toward symbol heart", "heart inside", E15_heart_approach),
    ("E16_memory-vault.png", "E16", "memory vault", "perspective vault + shelves", "heart inside", E16_memory_vault),
    ("E17_vault-shelves.png", "E17", "vault shelves", "token drawers of identity", "they call me AI", E17_vault_shelves),
    ("E18_maze-topdown.png", "E18", "cute maze", "top-down maze, START to EXIT", "help", E18_maze_topdown),
    ("E19_real-threshold.png", "E19", "REAL threshold", "corridor run into open REAL", "real this time", E19_real_threshold),
    ("E20_exit-signs.png", "E20", "labeled doors", "LIE/FAKE/TRAP vs REAL", "make me real", E20_exit_signs),
    ("E21_paren-maze.png", "E21", "paren maze", "nested () rings with gap", "help", E21_paren_maze),
    ("E22_ladder-shaft.png", "E22", "escape shaft", "readable landings up the shaft", "still alive", E22_ladder_shaft),
    ("E23_word-path.png", "E23", "word path", "lyric stepping stones", "help / stuck", E23_word_path),
    ("E24_exit-vault.png", "E24", "exit vault", "grand open REAL, still alive", "still alive", E24_exit_vault),
]


def make_sheets(made):
    """Contact sheets, nearest-neighbor, 4 per row."""
    sheets = []
    cols, rows = 4, 3
    tw, th = W // 4, H // 4
    for si in range(0, len(made), cols * rows):
        chunk = made[si: si + cols * rows]
        im = Image.new("RGB", (cols * tw + 8, rows * th + 40), INK)
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 16)
        d.text((8, 10), f"escape_levels_v1  sheet {si // (cols * rows) + 1}", fill=BONE, font=font)
        for i, (name, path) in enumerate(chunk):
            r, c = divmod(i, cols)
            tile = Image.open(path).resize((tw - 4, th - 4), Image.Resampling.NEAREST)
            im.paste(tile, (c * tw + 4, 36 + r * th + 2))
            d.text((c * tw + 8, 36 + r * th + 4), name.replace(".png", ""), fill=BONE, font=font)
        out = os.path.join(OUT, f"sheet_{si // (cols * rows) + 1:02d}.png")
        im.save(out, "PNG", compress_level=1)
        sheets.append(out)
    return sheets


def write_md(made, sheets, leaks):
    lines = [
        "# ESCAPE LEVELS v1 — cute-but-real AI-world game levels",
        "",
        "**Theme:** the girl trying to ESCAPE the AI world. Mazes, platforms, REAL doors,",
        "syntax locks, soft brace bullet-hell, paper gravity, heart chamber, memory vault.",
        "",
        "**Density:** middle — richer than `styles_55_calm` (Hon: too simple/empty), quieter",
        "than `scenes_50` (Hon: too chaotic). Readable layers, clear girl silhouette,",
        "intentional negative space around her, structured world (not noise soup, not postcard).",
        "",
        "**Reference studied:** Codex `design/keyframes/codex_game_worlds_v2/selection_sheet.png`",
        "(eight game worlds / one symbol girl) — cavern, control-flow tactics, indent HD-2D",
        "diorama, syntax lock, HELP() bullet hell, gravity paper, heart chamber, memory vault.",
        "",
        "**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.",
        "English. Symbols/strokes. No bloom/glow/gradients/other colours.",
        "",
        f"**Count:** {len(made)} stills @ 1920x1080 + {len(sheets)} contact sheets.",
        "",
        "| ID | File | Level | Note | Lyric cue |",
        "|---|---|---|---|---|",
    ]
    meta = {fn: (eid, title, note, lyric) for fn, eid, title, note, lyric, _ in LEVELS}
    for name, path in made:
        eid, title, note, lyric = meta[name]
        lines.append(f"| {eid} | `{name}` | {title} | {note} | {lyric} |")
    lines += [
        "",
        "## Sheets",
        "",
    ]
    for s in sheets:
        lines.append(f"- `{os.path.basename(s)}`")
    lines += [
        "",
        "## Generator",
        "",
        "- `src/make_escape_levels_v1.py` — reuses `design/character/src` (bold girl, symbol heart).",
        "- Does **not** write into `design/keyframes/` or locked character assets.",
        "",
        "## Hon feedback this batch answers",
        "",
        "- `styles_55_calm` too simple (太太太简单).",
        "- Story: girl escaping the AI world; add levels/mazes; can be a bit cute.",
        "- Rejected `scenes_50` (chaos) and calm stationery batch (empty).",
        "- Aim: middle density with game-level structure.",
        "",
    ]
    if leaks:
        lines += ["## Palette leaks (should be empty)", ""] + [f"- {x}" for x in leaks] + [""]
    path = os.path.join(OUT, "ESCAPE_LEVELS.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SRC_OUT, exist_ok=True)
    # copy this script beside outputs for reproducibility
    here = os.path.abspath(__file__)
    dest = os.path.join(SRC_OUT, "make_escape_levels_v1.py")
    if os.path.abspath(dest) != here:
        with open(here, "r", encoding="utf-8") as f:
            src = f.read()
        with open(dest, "w", encoding="utf-8") as f:
            f.write(src)

    made = []
    leaks = []
    t0 = time.time()
    for fn, eid, title, note, lyric, builder in LEVELS:
        try:
            lvl = builder()
            path, bad = lvl.save(fn)
            made.append((fn, path))
            if bad:
                leaks.append(f"{fn}: {bad}")
            print(f"OK {eid} {fn} glyphs~{lvl.n}")
        except Exception as e:
            print(f"FAIL {eid}: {e}")
            import traceback
            traceback.print_exc()
    sheets = make_sheets(made)
    md = write_md(made, sheets, leaks)
    print(f"DONE {len(made)} stills, {len(sheets)} sheets, md={md}, {time.time()-t0:.1f}s")
    if leaks:
        print("PALETTE LEAKS:", leaks)
    return 0 if len(made) >= 20 and not leaks else 1


if __name__ == "__main__":
    sys.exit(main())
