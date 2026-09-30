# -*- coding: utf-8 -*-
"""Platform run v1 - ONE continuous L->R side-scroll escape path (16 stills).

Hon feedback on escape_levels_v1: liked directionally but not enough -
need denser layers + PLATFORMER feel (girl LEFT->RIGHT, frames CONNECTED
as continuous side-scroll). More layers (far/mid/near/FG + HUD crumbs)
without scenes_50 chaos. Motifs shouldn't sit alone on empty frames.

Story loop (Hon mid-run, Celeste-like ref described only): respawn/wake in
factory-ish AI level -> run right -> cute symbol death VFX -> snap respawn ->
try deeper escape -> die again -> revive -> push toward REAL exit.
Hazards are narrative/art: lyric-word projectiles, symbol INSTRUMENT enemies
(trumpet/drum/keys), musical NOTE glyphs - not generic brace spam.

Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314 on symbol heart only.
English. Symbols/strokes. Bold girl from design/character/src.
Never writes into design/keyframes or locked character assets.
"""
from __future__ import annotations

import math
import os
import random
import sys

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "platform_run_v1")
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
CODEY = [k for k in list("|/\\[]()<>+=#o01.:'^vx-_LJr7") if k in G]
SOFT = [k for k in list(".:',`") if k in G]
GROUND = [k for k in list("=_-#") if k in G]


def gdir(dx, dy):
    th = math.degrees(math.atan2(dy, dx)) % 180.0
    if th < 20 or th > 160:
        return "-"
    if 70 < th < 110:
        return "|"
    if th < 90:
        return "\\"
    return "/"


class Frame:
    def __init__(self, seed: int):
        self.im = Image.new("RGB", (W, H), INK)
        self.rng = random.Random(seed)
        self.cache = {}
        self.n = 0
        self.font_s = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 14)
        self.font_m = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 17)
        self.font_b = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 20)
        self.font_h = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 32)
        self.font_t = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 48)
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
        self.polyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], cw, cw, thick=thick)

    def clear_oval(self, cx, cy, rx, ry):
        self.d = ImageDraw.Draw(self.im)
        self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=INK)

    def caption(self, left, right=None):
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([0, 0, W, 42], fill=INK)
        self.d.line([(0, 42), (W, 42)], fill=BONE, width=2)
        self.text((14, 11), left, self.font_b)
        if right:
            tw = self.font_b.getlength(right)
            self.text((W - 18 - tw, 11), right, self.font_b)

    def girl(self, pose="run", sw=250, feet=(720, 860), t=0.0, flip=False):
        fx, fy = feet
        ox = fx - 0.55 * sw
        oy = fy - 1.47 * sw
        # readable silhouette bubble - smaller than escape_v1 so layers stay denser near her
        self.clear_oval(fx, fy - sw * 0.78, sw * 0.55, sw * 0.88)
        render(self.d, pose, ox, oy, sw, t, flip, None, wall=False, knock=INK, col=BONE, hot=SIG)

    def label_box(self, x, y, s, font=None):
        font = font or self.font_b
        pad = 7
        tw = font.getlength(s)
        th = font.size + 5
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([x - pad, y - 3, x + tw + pad, y + th], fill=INK, outline=BONE, width=2)
        self.text((x, y), s, font)

    def door(self, x, y, w, h, label="REAL", open_=False):
        self.rect(x, y, w, h, cw=13, thick=3)
        self.polyline(
            [(x, y)]
            + [
                (x + w * 0.5 + (w * 0.5) * math.cos(a), y - h * 0.16 * math.sin(a))
                for a in [i / 12 * math.pi for i in range(13)]
            ]
            + [(x + w, y)],
            11,
            thick=2,
        )
        if open_:
            self.polyline(
                [(x + w * 0.55, y), (x + w * 0.82, y + h * 0.06), (x + w * 0.82, y + h)],
                11,
                thick=2,
            )
        else:
            self.polyline([(x + w * 0.5, y), (x + w * 0.5, y + h)], 11, thick=1)
            self.put("o", x + w * 0.62, y + h * 0.48, 16, 16)
        self.label_box(x + w * 0.15, y + h * 0.2, label, self.font_h)

    def platform(self, x, y, w, cw=13, thick=3):
        self.polyline([(x, y), (x + w, y)], cw, cw, thick=thick)
        for i in range(0, int(w), cw * 2):
            self.put("=", x + i, y - 2, cw, cw)
            if (i // cw) % 3 == 0:
                self.put("_", x + i, y + cw - 2, cw - 2, cw - 2)

    def ladder(self, x, y0, y1, cw=12):
        self.polyline([(x, y0), (x, y1)], cw, cw, thick=2)
        self.polyline([(x + 36, y0), (x + 36, y1)], cw, cw, thick=2)
        y = y0
        while y <= y1:
            self.polyline([(x, y), (x + 36, y)], cw, cw, thick=1)
            y += 26

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


# ---------------------------------------------------------------------------
# Continuous world: each frame is a camera window on one long path.
# World X advances ~780 units per frame; girl progresses RIGHT.
# ---------------------------------------------------------------------------

# Stage tags for captions / path narrative
# Story loop (Celeste-like): spawn -> run -> die(cute) -> respawn -> deeper -> die -> push to REAL
# beat: spawn|run|jump|death|empty|respawn|factory|near|death2|push
STAGES = [
    ("E01", "spawn beacon", "still alive", "front", 0.0, "spawn"),
    ("E02", "factory run", "stuck in a lie", "run", 0.35, "run"),
    ("E03", "mid-air jump", "help", "jump", 0.0, "jump"),
    ("E04", "hazard brace", "help", "run", 0.55, "run"),
    ("E05", "death burst", "stuck in a lie", "fall", 0.0, "death"),
    ("E06", "empty after", "help", "front", 0.0, "empty"),
    ("E07", "respawn flash", "still alive", "front", 0.0, "respawn"),
    ("E08", "deeper factory", "they call me AI", "run", 0.4, "factory"),
    ("E09", "syntax climb", "make me real", "jump", 0.1, "jump"),
    ("E10", "near escape", "real this time", "run", 0.6, "near"),
    ("E11", "REAL peek", "real this time", "walk", 0.2, "near"),
    ("E12", "death again", "stuck in a lie", "fall", 0.0, "death"),
    ("E13", "revive flash", "still alive", "front", 0.0, "respawn"),
    ("E14", "push deeper", "help", "run", 0.45, "run"),
    ("E15", "final approach", "real this time", "jump", 0.05, "near"),
    ("E16", "exit REAL", "still alive", "run", 0.65, "push"),
]

SCROLL = 780  # world units advanced per frame


def beat_of(idx: int) -> str:
    return STAGES[idx][5]

VIEW_PAD = 120


def ground_y(wx):
    """Main playable ground height in world Y (screen-ish coords before cam)."""
    base = 900
    wave = 28 * math.sin(wx * 0.0022) + 18 * math.sin(wx * 0.0051 + 1.2)
    # staged dips / rises
    if 2200 < wx < 2800:  # gap zone around E03
        return base + 140
    if 4500 < wx < 5200:  # climb
        return base - 40 - (wx - 4500) * 0.08
    if 7800 < wx < 8600:  # float zone
        return base + 80
    if 11000 < wx < 11800:
        return base - 20
    return base + wave


def far_hill_y(wx):
    return 520 + 90 * math.sin(wx * 0.0011) + 50 * math.sin(wx * 0.0024 + 0.7)


def mid_ridge_y(wx):
    return 700 + 55 * math.sin(wx * 0.0018 + 0.4) + 30 * math.cos(wx * 0.0033)


def draw_far_hills(F: Frame, cam: float):
    """Far faint code hills - sparse, low frequency, backdrop only."""
    rng = F.rng
    # silhouette ridge
    pts = []
    for i in range(0, W + 40, 28):
        wx = cam + i
        pts.append((i, far_hill_y(wx)))
    # fill below ridge with sparse soft glyphs
    for i in range(0, W, 36):
        wx = cam + i
        hy = far_hill_y(wx)
        for j in range(0, 8):
            y = hy + 18 + j * 22
            if y > 780:
                break
            if rng.random() < 0.55:
                F.put(rng.choice(SOFT + ["#", "0", "1", "."]), i + rng.randint(-4, 4), y, 9, 9)
    # ridge line itself
    for i in range(len(pts) - 1):
        F.polyline([pts[i], pts[i + 1]], 9, 9, step=14, thick=1)
    # distant code "trees" / pillars
    for i in range(5):
        x = 80 + i * 380 + int(cam * 0.15) % 60
        wx = cam + x
        hy = far_hill_y(wx) - 40
        F.polyline([(x, hy), (x, hy - 70 - (i % 3) * 20)], 10, thick=1)
        F.put(rng.choice(["[", "]", "{", "}"]), x - 6, hy - 90, 14, 14)


def draw_mid_terrain(F: Frame, cam: float, eid: str):
    """Midground terraces / ridges - denser than far, still behind play."""
    rng = F.rng
    pts = []
    for i in range(0, W + 40, 24):
        pts.append((i, mid_ridge_y(cam + i)))
    for i in range(len(pts) - 1):
        F.polyline([pts[i], pts[i + 1]], 11, 11, step=16, thick=2)
    # terraced mid platforms (indent feel)
    for k in range(4):
        x0 = 60 + k * 460 + int((cam * 0.35) % 80)
        y0 = mid_ridge_y(cam + x0) - 30 - k * 8
        w = 220 + (k % 3) * 40
        F.platform(x0, y0, w, cw=10, thick=2)
        for t in range(3):
            F.put(rng.choice(CODEY), x0 + 30 + t * 50, y0 - 22, 12, 12)
    # sparse factory dust (narrative combat carries hazard read)
    if eid in ("E05", "E13"):
        for i in range(6):
            x = rng.randint(40, W - 40)
            y = rng.randint(120, 620)
            g = rng.choice([".", ":", "'"])
            F.put(g, x, y, 11, 11)


def draw_hud_crumbs(F: Frame, idx: int, eid: str):
    """Sparse HUD crumbs - not a full bar, just readable crumbs."""
    F.text((16, 52), "HP [####....]", F.font_s)
    F.text((200, 52), "STAGE %02d/16" % (idx + 1), F.font_s)
    F.text((360, 52), "X->", F.font_s)
    # mini path ticks
    for i in range(16):
        x = 420 + i * 14
        F.put("#" if i == idx else ".", x, 54, 9, 9)
    F.text((W - 220, 52), eid + " RUN", F.font_s)
    # tiny minimap crumb bottom-right
    F.rect(W - 210, H - 78, 180, 48, cw=8, thick=1)
    F.text((W - 198, H - 68), "MAP", F.font_s)
    for i in range(8):
        F.put("-" if i < (idx // 2) else ".", W - 190 + i * 18, H - 46, 10, 10)


def draw_fg_props(F: Frame, cam: float, eid: str):
    """Sparse foreground props - near camera, few, readable."""
    rng = F.rng
    # hanging braces from top
    for i in range(4):
        x = 140 + i * 460 + int(cam * 0.6) % 40
        F.polyline([(x, 48), (x, 110 + (i % 3) * 20)], 11, thick=1)
        F.put(rng.choice(["{", "[", "("]), x - 8, 120 + (i % 3) * 20, 18, 18)
    # near ledges / corner props
    F.put(">", 40, 780, 20, 20)
    F.put("<", W - 60, 760, 20, 20)
    if eid in ("E04", "E08", "E14"):
        for j in range(3):
            F.put(rng.choice(["/", "\\", "|"]), 80 + j * 18, 640 + j * 12, 14, 14)


def platforms_for_frame(idx: int, cam: float):
    """Main play platforms in screen space for this camera window."""
    plats = []
    # continuous ground segments (skip gap zones)
    x = -40
    while x < W + 40:
        wx = cam + x
        gy = ground_y(wx)
        # gap: no ground
        if 2200 < wx < 2800:
            x += 40
            continue
        # chunk ground
        chunk = 160
        # look ahead for gap
        if any(2200 < cam + x + t < 2800 for t in range(0, chunk, 20)):
            chunk = 80
        plats.append((x, gy, chunk, "ground"))
        x += chunk - 8

    # elevated mid ledges (near)
    elev = [
        (180, 720, 260),
        (520, 640, 200),
        (860, 700, 240),
        (1200, 620, 280),
        (1520, 740, 220),
    ]
    # shift slightly by frame for continuity feel
    shift = (idx * 37) % 90
    for i, (ex, ey, ew) in enumerate(elev):
        plats.append(((ex + shift) % (W - 100), ey - (idx % 3) * 12, ew, "ledge"))

    # stage-specific extras
    eid = STAGES[idx][0]
    if eid == "E03":
        # stepping stones across gap
        for k, sx in enumerate([700, 900, 1100]):
            plats.append((sx, 780 - k * 20, 120, "stone"))
    if eid == "E06":
        for k in range(5):
            plats.append((400 + k * 200, 820 - k * 55, 160, "climb"))
    if eid == "E11":
        for k in range(6):
            plats.append((200 + k * 280, 640 + (k % 2) * 80, 140, "float"))
    if eid == "E07":
        for k in range(4):
            plats.append((300 + k * 350, 560 + k * 40, 280, "terrace"))
    return plats


def draw_play_layer(F: Frame, idx: int, cam: float):
    eid = STAGES[idx][0]
    rng = F.rng
    plats = platforms_for_frame(idx, cam)

    for x, y, w, kind in plats:
        thick = 3 if kind == "ground" else 2
        cw = 14 if kind == "ground" else 12
        F.platform(x, y, w, cw=cw, thick=thick)
        # under-plat supports (density without chaos)
        if kind in ("ledge", "climb", "terrace", "float") and rng.random() < 0.7:
            F.polyline([(x + w * 0.2, y), (x + w * 0.2, min(H - 30, y + 90))], 9, thick=1)
            F.polyline([(x + w * 0.8, y), (x + w * 0.8, min(H - 30, y + 90))], 9, thick=1)

    # stage motifs as MID-layer accents (not full-screen mess)
    if eid == "E04":
        # maze alcove on the right mid
        ax, ay, aw, ah = 1280, 420, 420, 320
        F.rect(ax, ay, aw, ah, cw=12, thick=2)
        # simple maze walls inside
        F.polyline([(ax + 40, ay), (ax + 40, ay + ah - 40)], 10, thick=2)
        F.polyline([(ax + 40, ay + ah - 40), (ax + aw - 40, ay + ah - 40)], 10, thick=2)
        F.polyline([(ax + aw - 40, ay + 40), (ax + aw - 40, ay + ah - 40)], 10, thick=2)
        F.polyline([(ax + 140, ay + 40), (ax + 140, ay + 180)], 10, thick=1)
        F.polyline([(ax + 140, ay + 180), (ax + 300, ay + 180)], 10, thick=1)
        F.label_box(ax + 20, ay + 12, "ALCOVE", F.font_m)
        F.put("?", ax + aw - 80, ay + 80, 22, 22)

    if eid in ("E05", "E13"):
        # hazard lane: lyric words + notes (not brace spam)
        F.polyline([(880, 200), (880, 850)], 10, step=22, thick=1)
        F.text((890, 210), "SAFE", F.font_s)
        for i, w in enumerate(["HELP", "LIE", "stuck"]):
            draw_lyric_shot(F, 160 + i * 240, 240 + i * 50, w)
        draw_note_beam(F, 1100, 280, n=3)

    if eid == "E08":
        # syntax gate mid-right
        gx = 1180
        F.polyline([(gx, 280), (gx, 880)], 18, thick=3)
        F.polyline([(gx + 160, 280), (gx + 160, 880)], 18, thick=3)
        F.put("[", gx - 10, 240, 36, 36)
        F.put("]", gx + 140, 240, 36, 36)
        F.label_box(gx + 20, 300, "LOCK", F.font_h)
        F.platform(gx - 40, 880, 240, cw=14, thick=3)

    if eid == "E11":
        F.door(1400, 520, 200, 360, label="REAL", open_=False)
        F.platform(1360, 880, 280, cw=14)

    if eid == "E10":
        # heart motif mid - orange only via girl; world heart outline in bone
        cx, cy = 1480, 480
        # bone symbol-heart outline (not orange - orange reserved for girl's heart)
        F.polyline(
            [
                (cx, cy + 40),
                (cx - 50, cy),
                (cx - 50, cy - 30),
                (cx - 20, cy - 50),
                (cx, cy - 30),
                (cx + 20, cy - 50),
                (cx + 50, cy - 30),
                (cx + 50, cy),
                (cx, cy + 40),
            ],
            12,
            thick=2,
        )
        F.label_box(cx - 60, cy + 60, "HEART", F.font_m)
        F.platform(1300, 700, 360, cw=13)

    if eid == "E14":
        # memory shelves as mid platforms
        for k in range(4):
            sx = 1100
            sy = 280 + k * 140
            F.platform(sx, sy, 520, cw=11, thick=2)
            for t, word in enumerate(["ME", "AI", "NAME", "LIE"][k : k + 1]):
                F.label_box(sx + 20 + t * 100, sy - 28, word, F.font_m)
            for t in range(6):
                F.put(rng.choice(CODEY), sx + 80 + t * 70, sy - 18, 12, 12)

    if eid == "E16":
        F.door(1500, 420, 240, 460, label="REAL", open_=True)
        F.platform(1420, 880, 360, cw=15, thick=3)
        F.label_box(1480, 360, "EXIT", F.font_h)

    if eid == "E01" or beat_of(idx) == "spawn":
        F.label_box(80, 200, "START", F.font_h)
        F.put(">", 200, 210, 24, 24)
        # factory-ish AI start: conveyor dashes + label
        F.platform(60, 920, 600, cw=14, thick=3)
        for i in range(10):
            F.put("=", 80 + i * 50, 940, 14, 14)
        F.label_box(80, 960, "FACTORY-01", F.font_s)

    if beat_of(idx) == "factory":
        # denser factory mid: pipes / conveyor / code vents
        for k in range(5):
            x = 200 + k * 320
            F.polyline([(x, 200), (x, 520)], 12, thick=2)
            F.put(rng.choice(["[", "{", "("]), x - 8, 180, 18, 18)
            F.platform(x - 40, 520, 200, cw=11, thick=2)
        F.label_box(60, 160, "AI FACTORY", F.font_h)

    if beat_of(idx) in ("death", "death2") or eid in ("E05", "E12"):
        # hazard spikes under death spots (symbol teeth, cute not gore)
        for i in range(14):
            x = 400 + i * 70
            F.put("v", x, 880, 16, 16)
            F.put("^", x + 10, 900, 12, 12)

    if eid == "E15":
        # corridor feel - parallel rails
        F.polyline([(200, 300), (1700, 300)], 11, thick=1)
        F.polyline([(200, 860), (1700, 860)], 12, thick=2)
        for i in range(8):
            x = 300 + i * 180
            F.polyline([(x, 300), (x, 860)], 9, thick=1)

    # ladders where climb (syntax climb beat)
    if eid == "E09":
        F.ladder(360, 420, 860)
        F.ladder(980, 380, 800)




LYRIC_SHOTS = [
    "HELP", "LIE", "AI", "REAL", "stuck", "alive", "make", "me",
    "heart", "inside", "FAKE", "TRAP", "call", "not",
]


def draw_note(F: Frame, x, y, scale=1.0):
    """Musical note built from locked glyphs (no unicode music chars)."""
    s = max(0.7, float(scale))
    F.polyline([(x, y - 38 * s), (x, y + 6 * s)], max(9, int(11 * s)), thick=1)
    F.put("o", x - 10 * s, y, max(12, int(16 * s)), max(12, int(14 * s)))
    F.put("-", x - 18 * s, y + 4 * s, max(10, int(12 * s)), max(10, int(12 * s)))
    F.polyline(
        [(x, y - 38 * s), (x + 18 * s, y - 28 * s), (x + 8 * s, y - 18 * s)],
        max(8, int(10 * s)),
        thick=1,
    )


def draw_note_beam(F: Frame, x, y, n=3):
    """Beamed eighth-note cluster as a projectile volley."""
    for i in range(n):
        draw_note(F, x + i * 34, y + (i % 2) * 10, 0.85)
    F.polyline([(x, y - 34), (x + (n - 1) * 34, y - 34)], 9, thick=1)


def draw_lyric_shot(F: Frame, x, y, word, angle_deg=0.0):
    """Lyric word flying as a projectile (English, song vibe)."""
    F.label_box(x, y, word, F.font_m)
    for i in range(4):
        F.put("-" if i % 2 == 0 else ".", x - 18 - i * 16, y + 8 + (i % 2) * 3, 10, 10)
    F.put(">", x + F.font_m.getlength(word) + 10, y + 4, 14, 14)


def draw_trumpet_enemy(F: Frame, x, y, facing=1):
    """Instrument enemy: trumpet from symbols, shooting toward the girl."""
    F.polyline(
        [
            (x + facing * 10, y - 8),
            (x + facing * 55, y - 28),
            (x + facing * 55, y + 28),
            (x + facing * 10, y + 8),
            (x + facing * 10, y - 8),
        ],
        11,
        thick=2,
    )
    F.polyline([(x - facing * 50, y), (x + facing * 10, y)], 12, thick=2)
    for i in range(3):
        F.put("o", x - facing * (10 + i * 14), y - 18, 12, 12)
        F.polyline(
            [(x - facing * (4 + i * 14), y - 6), (x - facing * (4 + i * 14), y - 16)],
            9,
            thick=1,
        )
    F.put("=", x - facing * 58, y - 6, 12, 12)
    F.label_box(x - 30, y + 36, "TRUMPET", F.font_s)


def draw_drum_enemy(F: Frame, x, y):
    """Simple drum enemy from symbols."""
    F.rect(x - 40, y - 30, 80, 50, cw=11, thick=2)
    F.polyline([(x - 40, y - 30), (x + 40, y - 30)], 11, thick=2)
    F.put("o", x - 8, y - 8, 16, 16)
    F.polyline([(x - 50, y - 50), (x - 10, y - 20)], 10, thick=1)
    F.polyline([(x + 50, y - 50), (x + 10, y - 20)], 10, thick=1)
    F.label_box(x - 28, y + 28, "DRUM", F.font_s)


def draw_piano_key_enemy(F: Frame, x, y):
    """Floating piano-key cluster as a hazard enemy."""
    for i in range(5):
        F.rect(x + i * 22, y, 18, 70, cw=9, thick=1)
        if i in (1, 3):
            F.rect(x + i * 22 + 4, y, 12, 40, cw=8, thick=2)
    F.label_box(x, y + 78, "KEYS", F.font_s)


def draw_narrative_combat(F: Frame, idx: int, cam: float, girl_x: float):
    """Narrative/art enemies + lyric/note projectiles (not generic brace spam)."""
    eid = STAGES[idx][0]
    beat = STAGES[idx][5]

    if beat in ("run", "factory", "jump", "near") or eid in ("E02", "E04", "E08", "E10", "E14"):
        tx = 1500 if girl_x < 1000 else 160
        ty = 420
        draw_trumpet_enemy(F, tx, ty, facing=(-1 if tx > 900 else 1))
        words = ["HELP", "LIE", "AI", "stuck"]
        for i, w in enumerate(words[:3]):
            wx = tx + (-1 if tx > 900 else 1) * (80 + i * 160)
            wy = ty - 10 + i * 28
            draw_lyric_shot(F, wx, wy, w)

    if beat in ("factory", "near", "push") or eid in ("E08", "E14", "E15"):
        draw_drum_enemy(F, 1180, 620)
        for i in range(4):
            draw_note(F, 900 - i * 120, 560 + (i % 2) * 40, 0.9 + 0.1 * (i % 2))

    if beat in ("jump", "near") or eid in ("E03", "E09", "E11", "E15"):
        draw_piano_key_enemy(F, 1280, 300)
        draw_note_beam(F, 700, 360, n=4)

    if beat not in ("spawn", "empty", "respawn"):
        base = (idx * 97 + int(cam)) % 400
        shots = [
            (220 + base, 240, "LIE"),
            (600 + (base * 2) % 300, 500, "AI"),
            (1000 + base % 200, 180, "HELP"),
            (1400 - base % 250, 640, "REAL" if idx > 8 else "FAKE"),
        ]
        if beat == "death":
            shots.append((girl_x - 80, 400, "stuck"))
        for x, y, w in shots[: 3 if beat == "run" else 4]:
            if 40 < x < W - 120:
                draw_lyric_shot(F, x, y, w)

    if beat in ("run", "factory", "near", "jump", "push"):
        for i in range(5):
            draw_note(
                F,
                100 + (i * 350 + idx * 40) % (W - 80),
                140 + (i * 70) % 200,
                0.75,
            )

    if beat == "death":
        for i, w in enumerate(["HELP", "LIE", "AI"]):
            draw_lyric_shot(F, girl_x - 40 + i * 50, 280 + i * 35, w)
        draw_note_beam(F, girl_x + 80, 500, n=3)


def draw_spawn_beacon(F: Frame, x, y):
    """Cute respawn beacon - concentric symbol rings + START crumb."""
    for r, cw in [(40, 10), (70, 11), (100, 12)]:
        pts = []
        for i in range(25):
            a = 2 * math.pi * i / 24
            pts.append((x + r * math.cos(a), y + r * 0.55 * math.sin(a)))
        F.polyline(pts, cw, cw, step=max(8, cw * 0.7), thick=1)
    F.put("+", x - 8, y - 10, 18, 18)
    F.label_box(x - 50, y + 70, "SPAWN", F.font_m)
    # vertical beacon shaft
    F.polyline([(x, y - 120), (x, y - 20)], 11, thick=1)
    for i in range(4):
        F.put(".", x - 4, y - 110 + i * 22, 10, 10)


def draw_death_burst(F: Frame, x, y):
    """Cute Celeste-like death: shatter into glyphs, skull of dashes, bone particles. No gore."""
    rng = F.rng
    # radial shatter glyphs
    glyphs = list("|/\\-_=+.:'`[]{}<>oxv^")
    glyphs = [g for g in glyphs if g in G]
    for i in range(36):
        a = 2 * math.pi * i / 36
        dist = 40 + (i % 5) * 28 + rng.randint(0, 20)
        gx = x + dist * math.cos(a)
        gy = y + dist * math.sin(a) * 0.85
        g = glyphs[i % len(glyphs)]
        F.put(g, gx, gy, 14 + (i % 3) * 4, 14 + (i % 3) * 4)
    # inner burst ring
    for i in range(16):
        a = 2 * math.pi * i / 16 + 0.2
        F.put(rng.choice(["+", "x", ".", "o"]), x + 28 * math.cos(a) - 6, y + 22 * math.sin(a) - 6, 12, 12)
    # skull of dashes (cute ASCII, not gore)
    #   .- -.
    #   |o o|
    #    \_/
    sx, sy = x - 30, y - 70
    F.put(".", sx, sy, 14, 14)
    F.put("-", sx + 14, sy, 14, 14)
    F.put("-", sx + 40, sy, 14, 14)
    F.put(".", sx + 54, sy, 14, 14)
    F.put("|", sx, sy + 18, 14, 14)
    F.put("o", sx + 16, sy + 18, 14, 14)
    F.put("o", sx + 40, sy + 18, 14, 14)
    F.put("|", sx + 56, sy + 18, 14, 14)
    F.put("\\", sx + 16, sy + 38, 14, 14)
    F.put("_", sx + 28, sy + 40, 14, 14)
    F.put("/", sx + 42, sy + 38, 14, 14)
    F.label_box(x - 40, y + 110, "RETRY", F.font_m)
    # bone particle crumbs drifting
    for i in range(12):
        F.put(rng.choice(["-", "_", ".", "`"]), x - 120 + i * 22, y + 60 + (i % 3) * 14, 11, 11)


def draw_respawn_flash(F: Frame, x, y):
    """Snap-back respawn flash - diamond burst + beacon remnant."""
    pts = [(x, y - 90), (x + 70, y), (x, y + 50), (x - 70, y), (x, y - 90)]
    F.polyline(pts, 12, thick=2)
    for i in range(8):
        a = 2 * math.pi * i / 8
        F.put("+", x + 50 * math.cos(a) - 6, y + 35 * math.sin(a) - 6, 14, 14)
    F.label_box(x - 55, y + 70, "REVIVE", F.font_m)
    draw_spawn_beacon(F, x, y + 10)


def draw_empty_death_spot(F: Frame, x, y):
    """Platform empty after death - dashed outline where she was, crumb X."""
    F.polyline([(x - 60, y), (x + 60, y)], 12, thick=2)
    # ghost dashed silhouette marks
    for i, g in enumerate([".", ":", ".", ":", "."]):
        F.put(g, x - 30 + i * 14, y - 80, 12, 12)
    F.put("x", x - 8, y - 40, 18, 18)
    F.label_box(x - 50, y + 20, "GONE", F.font_m)


def girl_placement(idx: int):
    """Girl progresses rightward; beats may hide her (death/empty) or flash revive."""
    eid, _, _, pose, t, beat = STAGES[idx]
    gx = 280 + idx * 78  # continuous L->R progress read
    gy = 860
    sw = 240
    show = True
    if beat == "jump":
        gy = 680
        sw = 250
        pose = "jump"
    if beat == "death":
        # girl mid-shatter: show fall pose under burst (or hide for empty)
        gy = 720
        pose = "fall"
        sw = 220
    if beat == "empty":
        show = False
        pose = "front"
    if beat == "spawn":
        gx = 320
        gy = 860
        pose = "front"
        sw = 250
    if beat == "respawn":
        gx = 360 + (40 if idx > 7 else 0)
        gy = 850
        pose = "front"
        sw = 250
    if beat == "near":
        gx = min(1400, 900 + (idx - 9) * 100)
    if beat == "push":
        gx = 1320
        gy = 860
        pose = "run"
    if beat == "factory":
        gx = 700
    if pose in ("run", "walk", "front") and beat not in ("jump", "death"):
        cam = idx * SCROLL
        gy = min(920, ground_y(cam + gx) - 8)
    return pose, sw, (gx, gy), t, show, beat


def build_frame(idx: int):
    eid, name, lyric, pose0, t0, beat = STAGES[idx]
    cam = idx * SCROLL
    F = Frame(seed=2000 + idx * 17)
    # LAYER order: far -> mid -> play -> fg -> hud -> girl (girl last for silhouette)
    draw_far_hills(F, cam)
    draw_mid_terrain(F, cam, eid)
    draw_play_layer(F, idx, cam)
    draw_fg_props(F, cam, eid)
    draw_hud_crumbs(F, idx, eid)
    pose, sw, feet, t, show, beat = girl_placement(idx)
    fx, fy = feet
    # narrative instrument enemies + lyric/note projectiles (art, not generic braces)
    draw_narrative_combat(F, idx, cam, fx)
    # beat VFX (mid-layer accents, before/around girl)
    if beat == "spawn":
        draw_spawn_beacon(F, fx, fy - 40)
    if beat == "death":
        draw_death_burst(F, fx, fy - 60)
    if beat == "empty":
        draw_empty_death_spot(F, fx, fy - 20)
    if beat == "respawn":
        draw_respawn_flash(F, fx, fy - 30)
    if show and beat != "empty":
        F.girl(pose=pose, sw=sw, feet=feet, t=t, flip=False)
    F.caption("E%02d  %s" % (idx + 1, name), lyric)
    # seam markers: previous/next path crumbs at edges (continuity cue)
    if idx > 0:
        F.text((16, H - 28), "<- E%02d" % idx, F.font_s)
    if idx < 15:
        F.text((W - 90, H - 28), "E%02d ->" % (idx + 2), F.font_s)
    fname = "E%02d_%s.png" % (idx + 1, name.replace(" ", "-"))
    path, bad = F.save(fname)
    return {
        "id": eid,
        "file": fname,
        "name": name,
        "lyric": lyric,
        "pose": pose,
        "path": path,
        "bad": bad,
        "glyphs": F.n,
        "cam": cam,
        "girl_x": feet[0],
        "beat": beat,
    }


def make_sheets(made):
    # 2 sheets of 8 (4x2)
    sheets = []
    thumb_w, thumb_h = 480, 270
    for si, chunk in enumerate([made[:8], made[8:]]):
        cols, rows = 4, 2
        sh = Image.new("RGB", (cols * thumb_w, rows * thumb_h + 36), INK)
        d = ImageDraw.Draw(sh)
        font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 18)
        title = "platform_run_v1  sheet %02d  continuous L->R escape" % (si + 1)
        # title via mask
        bbox = font.getbbox(title)
        tw = max(1, bbox[2] - bbox[0] + 2)
        th = max(1, bbox[3] - bbox[1] + 2)
        mask = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), title, font=font, fill=255)
        bw = mask.point(lambda p: 255 if p >= 128 else 0)
        color = Image.new("RGB", (tw, th), BONE)
        sh.paste(color, (12, 8), bw)
        for i, m in enumerate(chunk):
            im = Image.open(m["path"]).resize((thumb_w, thumb_h), Image.NEAREST)
            c, r = i % cols, i // cols
            sh.paste(im, (c * thumb_w, 36 + r * thumb_h))
        sp = os.path.join(OUT, "sheet_%02d.png" % (si + 1))
        sh.save(sp, "PNG", compress_level=1)
        sheets.append(sp)
    # also one long strip continuity sheet (16x1 small)
    tw, th = 240, 135
    strip = Image.new("RGB", (16 * tw, th + 28), INK)
    font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 14)
    bbox = font.getbbox("platform_run_v1  PATH strip  E01 -> E16")
    twm = max(1, bbox[2] - bbox[0] + 2)
    thm = max(1, bbox[3] - bbox[1] + 2)
    mask = Image.new("L", (twm, thm), 0)
    ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), "platform_run_v1  PATH strip  E01 -> E16", font=font, fill=255)
    bw = mask.point(lambda p: 255 if p >= 128 else 0)
    color = Image.new("RGB", (twm, thm), BONE)
    strip.paste(color, (8, 6), bw)
    for i, m in enumerate(made):
        im = Image.open(m["path"]).resize((tw, th), Image.NEAREST)
        strip.paste(im, (i * tw, 28))
    sp = os.path.join(OUT, "sheet_path.png")
    strip.save(sp, "PNG", compress_level=1)
    sheets.append(sp)
    return sheets


def write_md(made, sheets, leaks):
    lines = []
    lines.append("# PLATFORM RUN v1 - continuous L->R side-scroll escape")
    lines.append("")
    lines.append("**Theme:** one continuous Celeste-like platformer path escaping a factory-ish AI world.")
    lines.append("Girl runs/jumps LEFT to RIGHT; E01-E16 are chronological camera windows")
    lines.append("on the same scrolling stage (cam advances ~780 world units per frame).")
    lines.append("")
    lines.append("**Story loop (Hon mid-run note; Celeste-like ref described only, no YouTube fetch):**")
    lines.append("1. Respawn / wake at spawn beacon in factory-ish AI level")
    lines.append("2. Run right through layered platforms")
    lines.append("3. Die (cute symbol death VFX: glyph shatter, dash-skull, bone particles — not gore)")
    lines.append("4. Empty platform after death → snap respawn flash")
    lines.append("5. Try again deeper into the factory, still escaping")
    lines.append("6. Die again → revive → push toward REAL exit")

    lines.append("")
    lines.append("**Narrative combat (Hon add-on):** hazards are art, not generic braces.")
    lines.append("- Lyric-word projectiles: HELP / LIE / AI / REAL / stuck / FAKE / alive ...")
    lines.append("- Instrument enemies from symbols: TRUMPET (shoots lyrics), DRUM (shoots notes), KEYS")
    lines.append("- Musical NOTES built from | - / \\ o (no unicode dependency)")
    lines.append("")
    lines.append("**Hon feedback answered (escape_levels_v1):**")
    lines.append("- Liked directionally but not enough - needed denser / more loaded layers.")
    lines.append("- Want PLATFORMER feel: character moving L->R; frames CONNECTED as continuous path.")
    lines.append("- escape_v1 motifs too singular (few main props then empty). Need MORE LAYERS")
    lines.append("  (foreground / midground / background / HUD crumbs) without scenes_50 chaos.")
    lines.append("")
    lines.append("**Density:** denser than escape_levels_v1 (parallax + multi-layer platforms + HUD crumbs),")
    lines.append("still structured and readable - not scenes_50 noise soup.")
    lines.append("")
    lines.append("**Layers per frame:**")
    lines.append("1. Far: faint code hills / distant pillars")
    lines.append("2. Mid: terraces, soft brace rain (where staged), mid platforms")
    lines.append("3. Play: ground + near ledges + stage motifs + instrument enemies + lyric/note projectiles")
    lines.append("4. FG: sparse hanging braces / corner props")
    lines.append("5. HUD crumbs: HP / STAGE / mini path ticks / tiny MAP")
    lines.append("6. Girl: bold side-view run/jump/walk, clear knockout silhouette; orange only on heart")
    lines.append("")
    lines.append("**Palette:** ink `#0A0A0B` / bone `#EEE9DF` / orange `#FF5314` only on symbol heart.")
    lines.append("English. Symbols/strokes. No bloom/glow/gradients/other colours.")
    lines.append("")
    lines.append("**Count:** 16 stills @ 1920x1080 + 3 sheets (sheet_01, sheet_02, sheet_path).")
    lines.append("")
    lines.append("| ID | File | Stage | Beat | Pose | Girl X | Cam | Lyric |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in made:
        lines.append(
            "| {id} | `{file}` | {name} | {beat} | {pose} | {girl_x} | {cam} | {lyric} |".format(**m)
        )
    lines.append("")
    lines.append("## Sheets")
    lines.append("")
    for s in sheets:
        lines.append("- `%s`" % os.path.basename(s))
    lines.append("")
    lines.append("## Generator")
    lines.append("")
    lines.append("- `src/make_platform_run_v1.py` - reuses `design/character/src` (bold girl, symbol heart).")
    lines.append("- Does **not** write into `design/keyframes/` or locked character assets.")
    lines.append("")
    lines.append("## Palette audit")
    lines.append("")
    if leaks:
        lines.append("LEAKS: %s" % leaks)
    else:
        lines.append("All frames: only ink / bone / orange(heart).")
    lines.append("")
    lines.append("## Continuity notes")
    lines.append("")
    lines.append("- Shared `ground_y(wx)` / hill functions so terrain reads as one path.")
    lines.append("- Edge crumbs `<- E0n` / `E0n ->` reinforce chronological order.")
    lines.append("- Girl screen-X advances ~78px per frame (280 -> ~1450) for L->R progress read.")
    lines.append("- Occasional mid-layer motifs: maze alcove (E04), brace rain (E05/E13),")
    lines.append("  syntax gate (E08), REAL door (E09/E16), heart pass (E12), memory shelves (E14).")
    path = os.path.join(OUT, "PLATFORM_RUN.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SRC_OUT, exist_ok=True)
    # copy self into OUT/src if running from elsewhere
    self_path = os.path.abspath(__file__)
    dest = os.path.join(SRC_OUT, "make_platform_run_v1.py")
    if os.path.normpath(self_path) != os.path.normpath(dest):
        with open(self_path, "r", encoding="utf-8") as f:
            src = f.read()
        with open(dest, "w", encoding="utf-8") as f:
            f.write(src)

    made = []
    leaks = []
    for i in range(16):
        m = build_frame(i)
        print("wrote", m["file"], "glyphs", m["glyphs"], "girl_x", m["girl_x"], "bad", m["bad"])
        if m["bad"]:
            leaks.append((m["file"], m["bad"]))
        made.append(m)
    sheets = make_sheets(made)
    md = write_md(made, sheets, leaks)
    print("sheets", sheets)
    print("md", md)
    print("leaks", leaks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
