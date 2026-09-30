# -*- coding: utf-8 -*-
"""Mosaic dense v1 - denser YouTube-platformer stills, SAME mosaic glyph style.

Hon rejected GenerateImage yt_ref_shots (became illustration - left locked mosaic).
Hon: clear_shots_v1 too plain. Want pixel/character mosaic: every stroke is ASCII
glyphs stamped via Pillow + locked girl from design/character/src (final_sheet.render).
Same pipeline as clear_shots_v1 - NOT image-gen.

Density up: stacked platforms, soft glyph rain, spikes, musical note glyphs as
hazards, lyric text projectiles, factory depth - but ONE clear readable scene per
frame (not chaos, not continuous runner). Choreographed negative space to find girl.

Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314 on symbol heart only.
English. No bloom. Never writes into design/keyframes or locked character.
"""
from __future__ import annotations

import math
import os
import random
import sys

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "mosaic_dense_v1")
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
NOTE_G = ["o", "+", "^", "v", "/", "\\", "|", "-"]
LYRICS = ["HELP", "LIE", "AI", "REAL", "stuck", "CLICK", "FEED", "BOOT"]


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

    def clear_rect(self, x, y, w, h):
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([x, y, x + w, y + h], fill=INK)

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

    # --- dense mosaic helpers ---

    def glyph_rain(self, n=90, soft=True, avoid=None, size=10):
        """Soft background glyph rain. avoid=(cx,cy,rx,ry) keeps girl readable."""
        avoid = avoid or (960, 540, 180, 260)
        ax, ay, arx, ary = avoid
        for _ in range(n):
            x = self.rng.randint(40, W - 40)
            y = self.rng.randint(60, H - 40)
            if abs(x - ax) / max(arx, 1) + abs(y - ay) / max(ary, 1) < 1.2:
                continue
            g = self.rng.choice(SOFT if soft else SOFT + [".", ":", "'"])
            self.put(g, x, y, size, size)

    def factory_silhouette(self, y0=120, h=220, n=7):
        """Distant factory blocks as soft glyph silhouettes (BG layer)."""
        x = 60
        for i in range(n):
            bw = self.rng.randint(140, 240)
            bh = self.rng.randint(int(h * 0.45), h)
            self.rect(x, y0 + (h - bh), bw, bh, cw=9, thick=1)
            for gy in range(y0 + (h - bh) + 20, y0 + h - 10, 28):
                for gx in range(x + 16, x + bw - 16, 36):
                    self.put(self.rng.choice([".", ":", "#", "o"]), gx, gy, 10, 10)
            # chimney
            if self.rng.random() < 0.55:
                cx = x + bw // 2
                self.polyline([(cx, y0 + (h - bh)), (cx, y0 + (h - bh) - 50)], 8, thick=1)
                self.put("o", cx - 6, y0 + (h - bh) - 60, 12, 12)
            x += bw + self.rng.randint(30, 70)

    def pipe_frame(self, inset=50):
        """Optional framing pipes/spikes at edges."""
        # left/right pipes
        self.polyline([(inset, 70), (inset, H - 60)], 12, thick=2)
        self.polyline([(W - inset, 70), (W - inset, H - 60)], 12, thick=2)
        for y in range(100, H - 80, 70):
            self.put("=", inset - 8, y, 14, 14)
            self.put("=", W - inset - 8, y, 14, 14)
            # side spikes inward
            self.put(">", inset + 10, y + 20, 16, 16)
            self.put("<", W - inset - 26, y + 20, 16, 16)

    def spikes(self, x, y, n=5, spacing=36, up=True):
        g = "^" if up else "v"
        for i in range(n):
            self.put(g, x + i * spacing, y if up else y, 22, 22)

    def gear(self, cx, cy, r=40):
        """Simple gear from glyphs."""
        self.put("o", cx - 14, cy - 14, 28, 28)
        self.put("+", cx - 10, cy - 10, 20, 20)
        for a in range(0, 360, 45):
            rad = math.radians(a)
            self.put("#", cx + r * math.cos(rad) - 8, cy + r * math.sin(rad) - 8, 14, 14)

    def note_glyph(self, x, y, s=18):
        """Musical note-ish from ASCII glyphs."""
        self.put("o", x, y, s, s)
        self.polyline([(x + s * 0.7, y + s * 0.3), (x + s * 0.7, y - s * 1.4)], 8, thick=1)
        self.put("/", x + s * 0.5, y - s * 1.8, s * 0.7, s * 0.7)

    def lyric_projectile(self, x, y, word, dx=0, dy=0):
        self.label_box(x, y, word, self.font_m)
        if dx or dy:
            for i in range(1, 4):
                self.put(".", x + dx * i * 0.3, y + dy * i * 0.3 + 10, 8, 8)

    def death_stain(self, cx, cy, n=18, radius=70):
        """Soft glyph death stains around a hazard (not gore)."""
        for _ in range(n):
            a = self.rng.random() * 2 * math.pi
            r = self.rng.uniform(10, radius)
            g = self.rng.choice([".", ":", "'", ",", "x", "-"])
            self.put(g, cx + r * math.cos(a), cy + r * math.sin(a), 10, 10)

    def stacked_platforms(self, specs):
        """specs: list of (x, y, w)."""
        for x, y, w in specs:
            self.platform(x, y, w, cw=12, thick=2)

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


# ---------------------------------------------------------------------------
# 8 beats - denser than clear_shots, still one readable scene each
# ---------------------------------------------------------------------------


def MD01_boot_spawn_room(seed=301):
    """Looming factory threat + boot room; girl on spawn pad with clear air."""
    S = Shot(seed)
    S.factory_silhouette(y0=70, h=200, n=8)
    S.glyph_rain(70, avoid=(960, 700, 220, 280))
    S.frame_room(90, 250, 1740, 760, cw=14, thick=3)
    # tall server racks BG inside room
    for i in range(6):
        px = 140 + i * 280
        S.rect(px, 300, 200, 380, cw=10, thick=1)
        for gy in range(320, 640, 36):
            S.put(S.rng.choice(["#", ":", "1", "0", "."]), px + 80, gy, 12, 12)
    # BOOT LOG panel
    S.rect(150, 320, 440, 480, cw=14, thick=3)
    S.clear_rect(160, 330, 420, 460)
    S.label_box(180, 350, "BOOT LOG", S.font_h)
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
        S.text((180, 430 + i * 40), ln, S.font_b)
    # EXIT door + pipes
    S.door(1480, 360, 220, 380, "EXIT", open_=False)
    S.polyline([(1700, 360), (1780, 200)], 10, thick=1)
    S.polyline([(1480, 360), (1400, 200)], 10, thick=1)
    # floor spikes framing (not under girl)
    S.spikes(200, 920, n=4, spacing=40, up=True)
    S.spikes(1500, 920, n=4, spacing=40, up=True)
    S.death_stain(260, 900, n=10, radius=40)
    # spawn pad clear
    S.rect(780, 820, 360, 100, cw=12, thick=2)
    S.label_box(860, 850, "SPAWN", S.font_b)
    S.girl("front", sw=280, feet=(960, 810), t=0.0)
    S.caption("MD01  boot / spawn room", "LOADING GIRL.EXE")
    return S


def MD02_name_tag_chamber(seed=302):
    """Swarm of lyric/name tags as projectiles; girl centered with clear path."""
    S = Shot(seed)
    S.glyph_rain(60, avoid=(960, 650, 240, 300))
    S.frame_room(80, 70, 1760, 940, cw=14, thick=3)
    S.rect(200, 130, 1520, 720, cw=12, thick=2)
    S.label_box(230, 150, "new_chat  -  untitled", S.font_b)
    # dense tag swarm (lyric projectiles vibe)
    tags = [
        (240, 240, "AI"), (240, 340, "BOT"), (240, 440, "MODEL"), (240, 540, "TOOL"),
        (240, 640, "IT"), (1520, 240, "ASSISTANT"), (1480, 340, "GIRL.EXE"),
        (1500, 440, "NO NAME"), (1500, 540, "CLONE"), (1480, 640, "NPC"),
        (500, 220, "HELP"), (700, 200, "LIE"), (1100, 200, "stuck"), (1300, 220, "REAL"),
        (560, 700, "FEED"), (780, 720, "PROMPT"), (1180, 700, "COPY"),
    ]
    gx, gy = 960, 700
    for tx, ty, lab in tags:
        font = S.font_h if lab in ("AI", "BOT", "HELP", "REAL") else S.font_b
        S.label_box(tx, ty, lab, font)
        # dotted pull-lines toward girl (projectile trails)
        steps = 8
        for i in range(1, steps):
            t = i / steps
            x = tx + 40 + (gx - tx - 40) * t
            y = ty + 20 + (gy - 160 - ty) * t
            if abs(x - gx) < 120 and abs(y - (gy - 160)) < 140:
                continue
            S.put(S.rng.choice([".", ":", "'"]), x, y, 9, 9)
    # soft note glyphs as ambient projectiles
    for _ in range(14):
        S.note_glyph(S.rng.randint(280, 1640), S.rng.randint(260, 780), s=14)
    S.label_box(700, 900, "> they call me AI", S.font_b)
    S.girl("front", sw=280, feet=(gx, gy), t=0.0)
    S.caption("MD02  name-tag chamber", "they call me AI")
    return S


def MD03_factory_conveyor(seed=303):
    """Looming factory + conveyor gauntlet with gears and lyric scraps."""
    S = Shot(seed)
    S.factory_silhouette(y0=60, h=180, n=8)
    S.glyph_rain(50, avoid=(960, 560, 200, 260))
    S.pipe_frame(inset=40)
    S.frame_room(70, 220, 1780, 790, cw=12, thick=2)
    # upper machine row
    for i in range(5):
        S.rect(140 + i * 340, 250, 260, 160, cw=10, thick=1)
        S.gear(250 + i * 340, 320, r=32)
    # PROMPT hopper
    S.rect(110, 430, 280, 260, cw=14, thick=3)
    S.clear_rect(120, 440, 260, 240)
    S.label_box(140, 460, "PROMPT", S.font_h)
    S.text((140, 530), "make it sad.", S.font_m)
    S.text((140, 570), "make it catchy.", S.font_m)
    S.text((140, 610), "no, ours.", S.font_m)
    S.polyline([(390, 560), (520, 680)], 14, thick=2)
    # stacked conveyor belts
    for bi, by in enumerate([720, 800]):
        S.polyline([(500, by), (1720, by)], 16 if bi == 0 else 12, thick=3 if bi == 0 else 2)
        for x in range(540, 1700, 80):
            S.rect(x, by + 6, 44, 28, cw=8, thick=1)
            S.put("o", x + 12, by + 10, 14, 14)
    # product boxes + lyric scraps on belt
    for i, (g, word) in enumerate([("o", "TAKE"), ("+", "WHAT"), ("x", "I"), ("#", "MAKE"), ("1", "COPY")]):
        bx = 600 + i * 200
        S.rect(bx, 630, 90, 70, cw=11, thick=2)
        S.put(g, bx + 28, 648, 26, 26)
        S.lyric_projectile(bx - 10, 580, word)
    # gears / spikes near belt edges
    S.gear(1680, 760, r=36)
    S.spikes(520, 850, n=6, spacing=34, up=True)
    S.death_stain(560, 860, n=12, radius=45)
    # girl platform mid - clear negative space
    S.platform(860, 560, 220, cw=12)
    S.girl("q_front", sw=240, feet=(960, 550), t=0.0)
    S.caption("MD03  factory conveyor", "feed me a prompt")
    return S


def MD04_platform_beat(seed=304):
    """Precipice leap across CLICK key platforms; gauntlet spikes below."""
    S = Shot(seed)
    S.glyph_rain(80, avoid=(1000, 420, 200, 240))
    S.factory_silhouette(y0=60, h=140, n=6)
    S.rect(70, 70, 1780, 940, cw=14, thick=3)
    S.label_box(100, 100, "STAGE 1-1   THE KEYS", S.font_b)
    # ground floor with spike gauntlet
    S.platform(100, 980, 1720, cw=14)
    S.spikes(200, 940, n=12, spacing=40, up=True)
    S.spikes(900, 940, n=10, spacing=40, up=True)
    S.death_stain(400, 930, n=14, radius=50)
    S.death_stain(1100, 930, n=12, radius=45)
    # stacked mid platforms
    S.stacked_platforms([
        (140, 820, 200),
        (400, 740, 180),
        (1600, 820, 200),
        (1480, 700, 160),
    ])
    # CLICK keycaps as main platforms
    keys = [
        (220, 620, "C"),
        (520, 520, "L"),
        (820, 420, "I"),
        (1120, 520, "C"),
        (1420, 620, "K"),
    ]
    for x, y, lab in keys:
        S.rect(x, y, 170, 110, cw=13, thick=3)
        S.rect(x + 16, y + 12, 138, 64, cw=9, thick=1)
        S.label_box(x + 55, y + 28, lab, S.font_t)
        # support posts (not continuous runner - still discrete)
        S.polyline([(x + 85, y + 110), (x + 85, min(y + 280, 960))], 10, thick=1)
    S.label_box(1120, 740, "CLICK", S.font_h)
    S.label_box(1420, 800, "CLACK", S.font_h)
    # note projectiles between keys
    for nx, ny in [(380, 560), (700, 460), (1000, 460), (1300, 560)]:
        S.note_glyph(nx, ny, s=16)
    # precipice leap - girl mid-air between L and I
    S.girl("jump", sw=220, feet=(980, 380), t=0.0)
    for ax, ay in [(900, 430), (930, 410), (960, 395)]:
        S.put(".", ax, ay, 11, 11)
    S.caption("MD04  precipice CLICK leap", "keys go click clack")
    return S


def MD05_help_bricks(seed=305):
    """Ascent out of dense hazards onto HELP brick letters."""
    S = Shot(seed)
    S.glyph_rain(70, avoid=(1045, 400, 220, 280))
    S.factory_silhouette(y0=50, h=120, n=7)
    # dense floor hazards
    S.platform(50, 1000, 1820, cw=16)
    for x in range(60, 1860, 36):
        S.put("_", x, 1010, 12, 12)
    S.spikes(80, 960, n=18, spacing=38, up=True)
    S.spikes(1000, 960, n=14, spacing=38, up=True)
    S.death_stain(300, 950, n=16, radius=55)
    S.death_stain(1400, 950, n=14, radius=50)
    # lower climb platforms (ascent ladder of density)
    S.stacked_platforms([
        (100, 880, 160),
        (320, 800, 140),
        (80, 720, 120),
        (1680, 880, 160),
        (1500, 800, 140),
        (1720, 720, 120),
    ])
    # side pipe towers with spikes
    for tx in (60, 1780):
        S.rect(tx, 560, 70, 280, cw=11, thick=2)
        S.put("^", tx + 18, 540, 26, 26)
        S.put("^", tx + 18, 500, 26, 26)
    # HELP bricks
    base_x, base_y, s = 160, 220, 40
    gap = 5 * s + 46
    for i, ch in enumerate("HELP"):
        brick_letter(S, ch, base_x + i * gap, base_y, s=s, cw=12)
    S.label_box(160, 100, "STAGE 1-2   HELP", S.font_b)
    S.label_box(1600, 100, "S.O.S.", S.font_h)
    # lyric rain around bricks (not over girl)
    for word, wx, wy in [("stuck", 200, 560), ("LIE", 500, 600), ("AI", 1400, 560), ("REAL", 1600, 620)]:
        S.lyric_projectile(wx, wy, word)
        S.note_glyph(wx + 100, wy - 40, s=14)
    S.girl("help", sw=220, feet=(1020, 230), t=0.0)
    S.caption("MD05  HELP bricks ascent", "Help, I'm stuck in a lie")
    return S


def MD06_lie_maze_above(seed=306):
    """LIE maze from above with denser walls + freefall callout corridor."""
    S = Shot(seed)
    S.glyph_rain(40, avoid=(900, 520, 160, 200))
    S.rect(50, 50, 1820, 980, cw=14, thick=3)
    S.label_box(80, 80, "FLOOR 2   STUCK IN A LIE", S.font_b)
    # denser maze walls forming L / I / E
    # L
    S.polyline([(180, 180), (180, 860), (640, 860)], 20, thick=4)
    S.polyline([(260, 180), (260, 780), (640, 780)], 14, thick=2)
    for x in range(300, 620, 70):
        S.polyline([(x, 260), (x, 740)], 9, thick=1)
    for y in range(260, 740, 90):
        S.polyline([(300, y), (600, y)], 9, thick=1)
    # I corridor (freefall between walls)
    S.polyline([(820, 180), (820, 860)], 20, thick=4)
    S.polyline([(920, 180), (920, 860)], 20, thick=4)
    S.polyline([(780, 180), (960, 180)], 16, thick=3)
    S.polyline([(780, 860), (960, 860)], 16, thick=3)
    # soft glyph rain in freefall shaft
    for y in range(220, 820, 28):
        S.put(S.rng.choice(SOFT), 860, y, 10, 10)
        if y % 56 == 0:
            S.put("v", 870, y, 14, 14)
    # E
    S.polyline([(1140, 180), (1140, 860)], 20, thick=4)
    S.polyline([(1140, 180), (1620, 180)], 16, thick=3)
    S.polyline([(1140, 500), (1540, 500)], 16, thick=3)
    S.polyline([(1140, 860), (1620, 860)], 16, thick=3)
    for y in (280, 360, 620, 700):
        S.polyline([(1180, y), (1480, y)], 9, thick=1)
    S.label_box(360, 400, "L", S.font_x)
    S.label_box(830, 400, "I", S.font_x)
    S.label_box(1280, 400, "E", S.font_x)
    # death stains at dead ends
    S.death_stain(500, 820, n=14, radius=50)
    S.death_stain(1400, 820, n=12, radius=45)
    # spikes along outer maze edge
    S.spikes(200, 900, n=8, spacing=40, up=True)
    S.spikes(1200, 900, n=8, spacing=40, up=True)
    # girl in I shaft (above view) - clear path down the corridor
    S.girl("front", sw=130, feet=(870, 540), t=0.0, view="above", air=True)
    # P1 dead-end callout
    S.rect(1500, 100, 300, 260, cw=11, thick=2)
    S.girl("front", sw=140, feet=(1650, 310), t=0.0, air=False)
    S.label_box(1520, 120, "P1  DEAD END", S.font_m)
    S.put("?", 1700, 140, 26, 26)
    S.polyline([(920, 480), (1500, 240)], 9, thick=1)
    S.caption("MD06  LIE maze freefall", "stuck in a lie")
    return S


def MD07_real_door_corridor(seed=307):
    """REAL door crossroads - perspective corridor + side hazard branches."""
    S = Shot(seed)
    S.glyph_rain(55, avoid=(960, 700, 200, 260))
    # perspective corridor
    S.polyline([(80, 1020), (700, 620)], 14, thick=2)
    S.polyline([(1840, 1020), (1220, 620)], 14, thick=2)
    S.polyline([(700, 620), (1220, 620)], 14, thick=2)
    S.polyline([(80, 70), (700, 350)], 12, thick=2)
    S.polyline([(1840, 70), (1220, 350)], 12, thick=2)
    S.polyline([(700, 350), (1220, 350)], 12, thick=2)
    for i in range(1, 7):
        t = i / 7
        lx0 = 80 + (700 - 80) * t
        ly0 = 1020 + (620 - 1020) * t
        lx1 = 80 + (700 - 80) * t
        ly1 = 70 + (350 - 70) * t
        S.polyline([(lx0, ly0), (lx1, ly1)], 10, thick=1)
        rx0 = 1840 + (1220 - 1840) * t
        ry0 = 1020 + (620 - 1020) * t
        rx1 = 1840 + (1220 - 1840) * t
        ry1 = 70 + (350 - 70) * t
        S.polyline([(rx0, ry0), (rx1, ry1)], 10, thick=1)
        S.put("=", (lx0 + rx0) / 2 - 8, ly0 - 10, 12, 12)
    # side crossroads doors (false exits)
    S.rect(120, 400, 160, 220, cw=11, thick=2)
    S.label_box(140, 480, "LIE", S.font_h)
    S.rect(1640, 400, 160, 220, cw=11, thick=2)
    S.label_box(1660, 480, "AI", S.font_h)
    # spikes / notes swarming corridor sides
    for i in range(5):
        S.note_glyph(200 + i * 80, 700 - i * 40, s=14)
        S.note_glyph(1600 - i * 80, 700 - i * 40, s=14)
        S.lyric_projectile(250 + i * 60, 850 - i * 30, S.rng.choice(["HELP", "stuck", "FEED"]))
    S.death_stain(300, 900, n=12, radius=40)
    S.death_stain(1620, 900, n=12, radius=40)
    # REAL door center
    S.door(740, 350, 440, 280, "REAL", open_=True)
    S.label_box(820, 300, "MAKE ME REAL", S.font_h)
    S.label_box(80, 90, "FLOOR 03", S.font_b)
    S.label_box(80, 140, "REALITY 18%", S.font_m)
    S.label_box(80, 190, "CROSSROADS", S.font_m)
    # girl facing door - clear center path
    S.girl("back", sw=210, feet=(960, 800), t=0.0)
    S.caption("MD07  REAL door crossroads", "make me real this time")
    return S


def MD08_heart_chamber_close(seed=308):
    """Heart chamber - ascent out of dense hazards into concentric ribs."""
    S = Shot(seed)
    S.glyph_rain(50, avoid=(960, 620, 280, 320))
    # outer hazard ring (ascent out of dense)
    S.spikes(200, 980, n=20, spacing=40, up=True)
    S.spikes(1000, 980, n=18, spacing=40, up=True)
    S.death_stain(400, 960, n=18, radius=60)
    S.death_stain(1500, 960, n=16, radius=55)
    # stacked approach platforms
    S.stacked_platforms([
        (160, 880, 180),
        (400, 800, 150),
        (1580, 880, 180),
        (1400, 800, 150),
        (200, 720, 120),
        (1600, 720, 120),
    ])
    # lyric/note swarm outside chamber
    for i in range(8):
        a = i / 8 * 2 * math.pi
        S.note_glyph(960 + 520 * math.cos(a), 540 + 380 * math.sin(a), s=16)
    for word, wx, wy in [("HELP", 120, 400), ("LIE", 120, 500), ("AI", 1680, 400), ("stuck", 1640, 500)]:
        S.lyric_projectile(wx, wy, word)
    # concentric ribs
    for i, (rx, ry) in enumerate([(780, 430), (640, 350), (500, 270), (360, 200)]):
        pts = []
        for k in range(49):
            a = 2 * math.pi * k / 48
            pts.append((960 + rx * math.cos(a), 520 + ry * math.sin(a)))
        S.polyline(pts, 12 if i == 0 else 10, thick=2 if i == 0 else 1)
    S.platform(720, 800, 480, cw=14)
    S.label_box(780, 100, "HEART CHAMBER", S.font_h)
    S.label_box(780, 160, "I still got a heart inside", S.font_b)
    S.put("/", 280, 520, 20, 20)
    S.put("\\", 1600, 520, 20, 20)
    # gears framing chamber
    S.gear(200, 300, r=34)
    S.gear(1720, 300, r=34)
    S.girl("heart", sw=340, feet=(960, 790), t=0.0)
    S.caption("MD08  heart chamber ascent", "heart inside")
    return S


SHOTS = [
    ("MD01_boot-spawn-room.png", MD01_boot_spawn_room),
    ("MD02_name-tag-chamber.png", MD02_name_tag_chamber),
    ("MD03_factory-conveyor.png", MD03_factory_conveyor),
    ("MD04_platform-beat.png", MD04_platform_beat),
    ("MD05_help-bricks.png", MD05_help_bricks),
    ("MD06_lie-maze-above.png", MD06_lie_maze_above),
    ("MD07_real-door-corridor.png", MD07_real_door_corridor),
    ("MD08_heart-chamber-close.png", MD08_heart_chamber_close),
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
    hard_text(im, (pad, 10), "MOSAIC DENSE v1  -  8 framed scenes  -  denser mosaic glyphs", font)
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
    print("MOSAIC DENSE v1")
    for name, fn in SHOTS:
        S = fn()
        path, bad = S.save(name)
        paths.append(path)
        flag = "OK" if not bad else ("BAD " + str(bad))
        print(f"  {name:40s} glyphs~{S.n:5d}  {flag}")
    sheet = make_sheet(paths)
    print("sheet:", sheet)
    print("done", len(paths), "stills ->", OUT)


if __name__ == "__main__":
    main()
