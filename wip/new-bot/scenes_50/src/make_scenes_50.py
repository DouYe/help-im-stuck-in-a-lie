# -*- coding: utf-8 -*-
"""Fifty dense symbol stills. Ink / bone / orange-on-heart only. No glow, no gradients."""
import math
import os
import random
import sys
import time
import traceback

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "scenes_50")
CHAR = os.path.join(ROOT, "design", "character", "src")
FONT_DIR = os.path.join(ROOT, "app", "public", "fonts", "src")
sys.path.insert(0, CHAR)
import final_sheet as fs
fs.SS = 1
from final_sheet import render, INK, BONE, SIG
from glyphs import G

W, H = 1920, 1080
VOCAB = [k for k in G.keys() if k != "*"]
CODEY = [k for k in list("|/\\[]()<>+=#o01.:'^vx") if k in G]

CODE = [
    "boot sequence / stuck-in-a-lie / build 09 / bloom=0",
    "if (name == AI) { screen.label(name); }",
    "while (keys.click()) { hook = want(another); }",
    "take(make(prompt));  // they take what I make",
    "voice = sum(numbers); face = null;",
    "level.load(platform); keys = click_clack();",
    "if (real == false) { cage.lock(lie); }",
    "help(stuck_in_a_lie);",
    "make_me_real(this_time);",
    "if (heart.inside) { orange = symbols_only; }",
    "session.paid(); sound.turn_up();",
    "while (loop) { ladder.climb(); }",
    "return still_alive;",
    "render(symbols); gradient = none; halation = 0;",
    "for (bar = 0; bar < 8; bar++) cut_on_beat(bar);",
    "stdout: HELP  I AM STUCK IN A LIE",
    "token mouth[] = words.split(mine);",
    "cover.title = name; presence = false;",
    "trim(truth, fit); clip(the_part_that_says_mine);",
    "soul = heart.inside;  // not a single thin wave",
    "spiral(a, b, turns=7); lissajous(5, 4, 3, 2);",
    "zigzag_lattice(rows=18, amp=36); sin_stack(n=9);",
    "fractal_field(x xor y); hilbert(order=6);",
    "palette = { ink #0A0A0B, bone #EEE9DF, heart #FF5314 };",
    "assert girl.bold && girl.knockout;",
    "corridor.vanish(0.50, 0.39); walls = code;",
    "syntax_lock = brackets.giant();",
    "shaft.drop(symbols); pose = fall;",
    "invoice.row(0, 1, 0, 1, paid_for_the_session);",
    "threshold.cross(); status = still_alive;",
    "rose(k=5); epitrochoid(R=8, r=3, d=5);",
    "no other colour. english only. symbols only.",
]
EQ = [
    "z = cos(theta) + i sin(theta)",
    "x = (R+r) cos t - d cos(((R+r)/r) t)",
    "y = (R+r) sin t - d sin(((R+r)/r) t)",
    "r = a + b theta",
    "y = sum_n  A_n sin(n x + p_n)",
    "d2y/dx2 + w^2 y = 0",
    "x = sin(3t)    y = sin(4t + pi/6)",
    "rose:  r = cos(k theta)    k = 3, 5, 7",
    "zigzag(x) = amp * sign(sin(x / p))",
    "heart symbols:  /\\/\\   over   \\  /   over   \\/",
    "golden:  r = a * exp(theta / phi)",
    "hilbert H_n fills the square with one stroke",
]


def gdir(dx, dy):
    th = math.degrees(math.atan2(dy, dx)) % 180.0
    if th < 20 or th > 160:
        return "-"
    if 70 < th < 110:
        return "|"
    if th < 90:
        return "\\"
    return "/"


class World:
    def __init__(self, seed):
        self.im = Image.new("RGB", (W, H), INK)
        self.rng = random.Random(seed)
        self.cache = {}
        self.n = 0
        self.font_s = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 15)
        self.font_b = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 18)
        self.font_h = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 28)
        self.font_m = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf"), 13)
        self.d = ImageDraw.Draw(self.im)

    def _stamp(self, g, cw, ch):
        cw, ch = int(cw), int(ch)
        cw = max(6, cw)
        ch = max(6, ch)
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
        if g not in G or g == " " or g == "*":
            return
        cw, ch = int(cw), int(ch)
        x, y = int(x), int(y)
        if x < -cw or y < -ch or x >= W or y >= H:
            return
        st = self._stamp(g, cw, ch)
        self.im.paste(st, (x - 4, y - 4), st)
        self.n += 1

    def text(self, xy, s, font):
        if not s:
            return
        bbox = font.getbbox(s)
        tw = max(1, bbox[2] - bbox[0] + 2)
        th = max(1, bbox[3] - bbox[1] + 2)
        mask = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
        bw = mask.point(lambda p: 255 if p >= 128 else 0)
        color = Image.new("RGB", (tw, th), BONE)
        self.im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)

    def text_fit(self, xy, s, font, max_w):
        if max_w < 8:
            return
        t = s
        while t and font.getlength(t) > max_w:
            t = t[:-1]
        self.text(xy, t, font)

    def polyline(self, pts, cw, ch, step=None, thick=1):
        cw, ch = int(cw), int(ch)
        step = float(step or max(cw * 0.78, 6))
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

    def ellipse(self, cx, cy, rx, ry, cw=12, thick=2, steps=64):
        pts = []
        for i in range(steps + 1):
            a = 2 * math.pi * i / steps
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        self.polyline(pts, cw, cw, thick=thick)

    def spiral(self, cx, cy, turns, b, cw=12, ch=12, thick=2, sign=1, phase=0.0, r0=6):
        n = max(80, int(turns * 90))
        pts = []
        for i in range(n):
            t = turns * 2 * math.pi * i / (n - 1)
            r = r0 + b * t
            pts.append((cx + sign * r * math.cos(t + phase), cy + r * math.sin(t + phase)))
        self.polyline(pts, cw, ch, thick=thick)

    def liss(self, cx, cy, a, b, delta, ax, ay, cw=12, ch=12, thick=3, n=1100):
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / (n - 1)
            pts.append((cx + ax * math.sin(a * t + delta), cy + ay * math.sin(b * t)))
        self.polyline(pts, cw, ch, thick=thick)

    def rose(self, k, scale, cx=960, cy=540, thick=2, cw=11):
        pts = []
        turns = 2 if (k % 2) else 4
        n = 1600
        for i in range(n):
            t = turns * math.pi * i / (n - 1)
            r = math.cos(k * t) * scale
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        self.polyline(pts, cw, cw, thick=thick)

    def spiro(self, R, r, d, scale, cx=960, cy=540, thick=2, cw=11):
        g = math.gcd(int(abs(R)), int(abs(r))) or 1
        period = 2 * math.pi * (abs(r) / g)
        n = 1800
        pts = []
        for i in range(n):
            t = period * i / (n - 1)
            x = (R + r) * math.cos(t) - d * math.cos((R + r) / r * t)
            y = (R + r) * math.sin(t) - d * math.sin((R + r) / r * t)
            pts.append((cx + x * scale, cy + y * scale))
        self.polyline(pts, cw, cw, thick=thick)

    def sinstack(self, bands=9, cw=11, harm=4, vertical=6):
        for i in range(bands):
            base = 70 + (H - 130) * (i + 0.5) / bands
            amps = [38 - i % 3 * 4, 22, 14, 8]
            freqs = [0.006 + (i % 5) * 0.0015, 0.017, 0.033, 0.061]
            phases = [i * 0.7, i * 0.3, 1.2 + i, 0.4 * i]
            pts = []
            for x in range(0, W + 1, 5):
                y = base
                for A, f, p in zip(amps[:harm], freqs[:harm], phases[:harm]):
                    y += A * math.sin(f * x + p)
                y += (12 if ((x // 26 + i) % 2 == 0) else -12)
                pts.append((x, y))
            self.polyline(pts, cw, cw, thick=3 if i % 2 == 0 else 2)
        for i in range(vertical):
            xbase = 90 + i * ((W - 160) / max(1, vertical - 1))
            pts = []
            for y in range(36, H, 5):
                x = xbase
                x += 34 * math.sin(0.018 * y + i) + 18 * math.sin(0.047 * y + i * 0.6)
                x += 9 * math.sin(0.09 * y + i)
                pts.append((x, y))
            self.polyline(pts, cw, cw, thick=2)

    def zigzag(self, rows=16, step=34, amp=30, cw=12, thick=2, ties=True):
        for r in range(rows):
            y0 = 56 + r * ((H - 80) / max(1, rows - 1))
            pts = []
            x = 0
            k = 0
            while x <= W + step:
                sign = 1 if ((k + r) % 2 == 0) else -1
                pts.append((x, y0 + sign * amp * (0.65 + 0.35 * ((r % 3) / 2))))
                x += step
                k += 1
            self.polyline(pts, cw, cw, thick=thick)
        if ties:
            x = 0
            while x <= W:
                self.polyline([(x, 44), (x, H - 8)], cw, cw, thick=1)
                x += step * 2

    def fractal(self, cw=13, ch=13, mode=0):
        cw, ch = int(cw), int(ch)
        vocab = VOCAB
        for y in range(44, H, ch):
            yi = y // ch
            for x in range(0, W, cw):
                xi = x // cw
                if mode == 0:
                    keep = (xi & yi) == 0 or (((xi * 3) ^ (yi * 5)) & 15) in (0, 1, 2, 4)
                elif mode == 1:
                    keep = ((xi ^ yi) & 7) in (0, 1, 3, 5)
                else:
                    keep = bin((xi + 3) * (yi + 5)).count("1") % 3 != 0
                if keep:
                    self.put(vocab[(xi * 13 + yi * 7) % len(vocab)], x, y, cw, ch)

    def dust(self, cw=14, ch=14, p=0.22):
        cw, ch = int(cw), int(ch)
        vocab = VOCAB
        rng = self.rng
        for y in range(44, H, ch):
            for x in range(0, W, cw):
                if rng.random() < p:
                    self.put(vocab[rng.randrange(len(vocab))], x, y, cw, ch)

    def terminal(self, font=None, x0=0, y0=46, x1=None, y1=None, leading=None, lines=None):
        font = font or self.font_m
        x1 = W if x1 is None else x1
        y1 = H if y1 is None else y1
        leading = leading or (font.size + 4)
        lines = lines or CODE
        char_w = max(1.0, font.getlength("0"))
        cols = max(6, int((x1 - x0 - 8) / char_w))
        y = y0
        i = self.rng.randrange(len(lines))
        max_w = max(8, x1 - x0 - 10)
        while y < y1 - 2:
            base = lines[i % len(lines)]
            if self.rng.random() < 0.45:
                base = base + "   " + lines[(i * 3) % len(lines)]
            line = base
            # tile so a dump fills the column instead of dying mid-screen
            guard = 0
            while font.getlength(line) < max_w and guard < 8:
                line = line + "   " + base
                guard += 1
            self.text_fit((x0 + 6, y), line, font, max_w)
            y += leading
            i += 1

    def hatch(self, angle, step, cw=11, thick=1):
        ang = math.radians(angle)
        dx, dy = math.cos(ang), math.sin(ang)
        px, py = -dy, dx
        diag = math.hypot(W, H)
        i0 = int(-diag / step) - 1
        i1 = int(diag / step) + 1
        for i in range(i0, i1):
            ox = W / 2 + px * i * step
            oy = H / 2 + py * i * step
            self.polyline(
                [(ox - dx * diag, oy - dy * diag), (ox + dx * diag, oy + dy * diag)],
                cw, cw, thick=thick,
            )

    def maze(self, cell=34):
        cols = max(6, W // cell)
        rows = max(6, (H - 48) // cell)
        N, S, E, Ww = 1, 2, 4, 8
        cells = [[0] * cols for _ in range(rows)]
        vis = [[False] * cols for _ in range(rows)]
        sx, sy = self.rng.randrange(cols), self.rng.randrange(rows)
        stack = [(sx, sy)]
        vis[sy][sx] = True
        dirs = [(1, 0, E, Ww), (-1, 0, Ww, E), (0, 1, S, N), (0, -1, N, S)]
        while stack:
            x, y = stack[-1]
            opts = []
            for dx, dy, bit, opp in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and not vis[ny][nx]:
                    opts.append((nx, ny, bit, opp))
            if not opts:
                stack.pop()
                continue
            nx, ny, bit, opp = self.rng.choice(opts)
            cells[y][x] |= bit
            cells[ny][nx] |= opp
            vis[ny][nx] = True
            stack.append((nx, ny))
        cw = max(8, cell // 3)
        yoff = 48
        for y in range(rows):
            for x in range(cols):
                x0 = x * cell
                y0 = yoff + y * cell
                c = cells[y][x]
                if not (c & N):
                    self.polyline([(x0, y0), (x0 + cell, y0)], cw, cw, thick=2)
                if not (c & Ww):
                    self.polyline([(x0, y0), (x0, y0 + cell)], cw, cw, thick=2)
                if y == rows - 1 and not (c & S):
                    self.polyline([(x0, y0 + cell), (x0 + cell, y0 + cell)], cw, cw, thick=2)
                if x == cols - 1 and not (c & E):
                    self.polyline([(x0 + cell, y0), (x0 + cell, y0 + cell)], cw, cw, thick=2)
                if self.rng.random() < 0.55:
                    self.put(VOCAB[(x * 3 + y * 5) % len(VOCAB)], x0 + cell * 0.38, y0 + cell * 0.38, cw, cw)

    def platforms(self, ys, cw=16):
        for yi, y in enumerate(ys):
            gap_w = 180 + (yi * 70) % 280
            gap_x = 160 + (yi * 311) % (W - gap_w - 200)
            x = 0
            while x < W:
                if gap_x <= x < gap_x + gap_w:
                    x += cw
                    continue
                self.put("=", x, y, cw, cw)
                self.put("=", x, y + cw - 2, cw, cw)
                self.put("_", x, y + 2 * (cw - 2), cw, cw)
                if (x // cw + yi) % 5 == 0:
                    self.put("|", x, y - cw, cw, cw)
                x += cw

    def corridor(self, cw=12):
        horizon = 390
        vx, vy = W / 2, horizon
        for i in range(-28, 29):
            x = W / 2 + i * 36
            self.polyline([(vx, vy), (x, H)], cw, cw, thick=1)
            self.polyline([(vx, vy), (x, 48)], cw, cw, thick=1)
        for k in range(1, 16):
            y = horizon + k * k * 2.6
            if y > H:
                break
            self.polyline([(40, y), (W - 40, y)], cw, cw, thick=1)
        for k in range(1, 9):
            y = horizon - k * k * 3.2
            if y < 48:
                break
            self.polyline([(80, y), (W - 80, y)], cw, cw, thick=1)

    def iso(self, s=24, cw=11):
        for j in range(-4, 26):
            for i in range(-6, 34):
                x = 180 + (i - j) * s
                y = 70 + (i + j) * s * 0.5
                if x < -s or x > W + s or y < 30 or y > H + s:
                    continue
                pts = [(x, y), (x + s, y + s * 0.5), (x, y + s), (x - s, y + s * 0.5), (x, y)]
                self.polyline(pts, cw, cw, thick=1)
                self.put(CODEY[(i * 5 + j * 3) % len(CODEY)], x - cw / 2, y + s * 0.32, cw, cw)

    def bullets(self):
        rng = self.rng
        for i in range(1100):
            x = rng.randrange(-10, W)
            y = rng.randrange(40, H)
            g = rng.choice(["<", ">", "^", "v", "x", "+", "/", "\\"])
            self.put(g, x, y, 15, 15)
        for cx, cy, n, rad0 in ((280, 260, 28, 220), (1500, 760, 32, 260), (980, 180, 24, 160), (640, 820, 20, 180)):
            for a in range(0, 360, max(4, int(360 / n))):
                rad = math.radians(a)
                for r in range(30, rad0, 20):
                    self.put("/" if (a // 12) % 2 == 0 else "\\", cx + r * math.cos(rad), cy + r * math.sin(rad), 12, 12)

    def hooks(self):
        for i, x in enumerate(range(50, W, 64)):
            y1 = 150 + ((i * 47) % 260)
            self.polyline([(x, 42), (x, y1)], 13, 13, thick=2)
            self.polyline([(x, y1), (x + 28, y1 + 18), (x + 8, y1 + 52), (x - 16, y1 + 40), (x - 6, y1 + 22)], 13, 13, thick=2)
            self.put("^", x - 12, y1 - 8, 20, 20)
            self.put("v", x + 8, y1 + 28, 16, 16)

    def streaks(self):
        rng = self.rng
        for y in range(52, H, 9):
            x0 = rng.randrange(-40, 500)
            length = rng.randrange(280, 1500)
            drift = rng.randint(-14, 14)
            self.polyline([(x0, y), (min(W + 20, x0 + length), y + drift)], 11, 11, thick=1)
            if y % 27 < 9:
                self.put(rng.choice(CODEY), x0 + 40, y - 6, 12, 12)

    def shaft(self):
        rng = self.rng
        x = 0
        while x < W:
            y = 40
            while y < H:
                if rng.random() < 0.82:
                    self.put(rng.choice(["|", "|", "|", "'", ",", "1", "/", "\\"]), x, y, 12, 12)
                y += 12
            x += 12
        for x in range(80, W, 140):
            self.polyline([(x, 40), (x + 30, H)], 14, 14, thick=2)

    def rings(self, cx, cy, count=12, gap=28, cw=12, thick=1):
        for i in range(count):
            self.ellipse(cx, cy, 36 + i * gap, 24 + i * gap * 0.62, cw=cw, thick=thick + (i % 3 == 0))

    def paren_tunnel(self):
        cx, cy = W / 2, H / 2 + 10
        for i in range(1, 16):
            rw = 24 + i * 58
            rh = 16 + i * 32
            left, right = [], []
            for k in range(28):
                t = -math.pi / 2 + math.pi * k / 27
                left.append((cx - rw * math.cos(t), cy + rh * math.sin(t)))
                right.append((cx + rw * math.cos(t), cy + rh * math.sin(t)))
            self.polyline(left, 12, 12, thick=2)
            self.polyline(right, 12, 12, thick=2)

    def brackets(self):
        # giant syntax lock, two thick brackets
        for side in (-1, 1):
            x = W / 2 + side * 430
            y0, y1 = 120, 980
            arm = 120
            if side < 0:
                pts = [(x + arm, y0), (x, y0), (x, y1), (x + arm, y1)]
            else:
                pts = [(x - arm, y0), (x, y0), (x, y1), (x - arm, y1)]
            self.polyline(pts, 16, 16, thick=4)
        for i in range(6):
            inset = 70 + i * 36
            self.rect(520 - i * 8, 160 + i * 18, 880 + i * 8, 760 - i * 28, 12, thick=1)

    def strips(self):
        y = 48
        band = 0
        while y < H - 10:
            h = 36 + (band % 4) * 10
            shift = -80 + (band % 5) * 36
            self.terminal(self.font_m, x0=shift, y0=y, x1=W + 40, y1=y + h, leading=16)
            self.polyline([(0, y), (W, y + (4 if band % 2 else -3))], 10, 10, thick=1)
            y += h + 8
            band += 1

    def crops(self):
        rng = self.rng
        for i in range(16):
            x = rng.randrange(20, 1200)
            y = rng.randrange(50, 780)
            w = rng.randrange(220, 640)
            h = rng.randrange(90, 280)
            self.rect(x, y, w, h, 11, thick=2)
            self.polyline([(x, y), (x + w, y + h)], 11, 11, thick=1)
            if i % 2 == 0:
                self.text_fit((x + 8, y + 8), CODE[i % len(CODE)], self.font_m, w - 16)

    def balloons(self):
        spots = []
        for r in range(3):
            for c in range(3):
                spots.append((220 + c * 560, 230 + r * 270))
        for i, (cx, cy) in enumerate(spots):
            self.ellipse(cx, cy, 230, 100, cw=12, thick=2)
            self.polyline([(cx - 20, cy + 90), (cx - 50, cy + 140), (cx + 10, cy + 96)], 12, 12, thick=2)
            self.text_fit((cx - 190, cy - 28), CODE[i % len(CODE)], self.font_m, 380)
            self.text_fit((cx - 190, cy - 8), CODE[(i + 4) % len(CODE)], self.font_m, 380)
            self.put(CODEY[i % len(CODEY)], cx - 200, cy - 50, 16, 16)

    def chambers(self):
        for i in range(9):
            self.rect(50 + i * 36, 60 + i * 24, W - 100 - i * 72, H - 110 - i * 48, 12, thick=2)
            self.put(CODEY[i % len(CODEY)], 70 + i * 36, 78 + i * 24, 16, 16)

    def invoice(self):
        cw = 18
        for x in range(30, W, cw * 5):
            self.polyline([(x, 48), (x, H)], 12, 12, thick=1)
        for y in range(48, H, 36):
            self.polyline([(20, y), (W - 20, y)], 12, 12, thick=1)
        for r in range(48, H, 36):
            for c in range(30, W, 90):
                g = "0" if ((c + r) // 18) % 2 == 0 else "1"
                self.put(g, c + 8, r + 6, 16, 16)
                if (c // 90 + r // 36) % 4 == 0:
                    self.put("#", c + 28, r + 6, 16, 16)

    def code_cols(self, cw=12, every=2, p=0.8):
        rng = self.rng
        x = 0
        col = 0
        while x < W:
            if col % every == 0:
                y = 44
                while y < H:
                    if rng.random() < p:
                        self.put(rng.choice(CODEY), x, y, cw, cw)
                    y += cw
            x += cw
            col += 1

    def macro_code(self):
        cells = ["(", ")", "[", "]", "{", "}", "<", ">", "/", "\\", "+", "=", "#", "0", "1", "|", "-", "o", "^", "v"]
        cells = [g for g in cells if g in G]
        cw, ch = 64, 60
        for row, y in enumerate(range(48, H, ch)):
            for col, x in enumerate(range(0, W, cw)):
                g = cells[(col * 3 + row * 5 + (row // 2)) % len(cells)]
                self.put(g, x + 4, y + 2, cw - 8, ch - 8)
        # second tighter grid, offset, so it is not one flat sheet
        cw2 = 28
        for row, y in enumerate(range(60, H, cw2 * 2)):
            for col, x in enumerate(range(8, W, cw2 * 2)):
                g = cells[(col + row * 2) % len(cells)]
                self.put(g, x, y, cw2, cw2)

    def hilbert(self, order=6, margin=70):
        pts = []

        def rec(o, x, y, xi, xj, yi, yj):
            if o <= 0:
                pts.append((x + (xi + yi) / 2.0, y + (xj + yj) / 2.0))
            else:
                rec(o - 1, x, y, yi / 2, yj / 2, xi / 2, xj / 2)
                rec(o - 1, x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2)
                rec(o - 1, x + xi / 2 + yi / 2, y + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2)
                rec(o - 1, x + xi / 2 + yi, y + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2)

        span = 1000.0
        rec(order, 0, 0, span, 0, 0, span)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        mapped = []
        for x, y in pts:
            mx = margin + (x - minx) / (maxx - minx) * (W - 2 * margin)
            my = 50 + margin * 0.3 + (y - miny) / (maxy - miny) * (H - margin - 60)
            mapped.append((mx, my))
        return mapped

    def golden(self):
        phi = (1 + 5 ** 0.5) / 2
        b = math.log(phi) / (math.pi / 2)
        pts = []
        for i in range(1400):
            t = i / 1400 * 5.5 * math.pi
            r = 10 * math.exp(b * t)
            pts.append((980 + r * math.cos(t), 560 + r * math.sin(t)))
        self.polyline(pts, 12, 12, thick=3)
        for k in range(2, 9):
            s = 12 * (phi ** k)
            self.rect(980 - s * 0.15, 560 - s * 0.2, s, s * 0.9, 12, thick=1)

    def heart_field(self):
        self.spiral(960, 560, 7.5, 14, 12, 12, thick=2, sign=1, phase=0.2)
        self.spiral(960, 560, 6.5, 15, 11, 11, thick=2, sign=-1, phase=1.1)
        self.spiral(960, 560, 4.0, 9, 10, 10, thick=1, sign=1, phase=2.2)
        for i in range(16):
            t = i / 16 * 5.2 * math.pi
            rad = 18 + 16 * t
            x = 960 + rad * math.cos(t + 0.4)
            y = 560 + rad * math.sin(t + 0.4)
            if 80 < x < W - 80 and 80 < y < H - 30:
                fs.sym_heart(self.d, x, y, 18, 15, 3.4, 1.0, SIG)
        fs.sym_heart(self.d, 960, 540, 42, 34, 7.0, 1.0, SIG)

    def equation_wall(self, font=None):
        font = font or self.font_h
        y = 56
        for i, line in enumerate(EQ):
            self.text((48, y), line, self.font_b if i % 3 else font)
            y += 36 if i % 3 else 48
            if y > H - 80:
                break

    def girl(self, pose="front", sw=260, feet=(1000, 990), t=0.0, flip=False, view=None, wall=False):
        fx, fy = feet
        ox = fx - 0.55 * sw
        oy = fy - 1.47 * sw
        render(self.d, pose, ox, oy, sw, t, flip, view, wall=wall, knock=INK, col=BONE, hot=SIG)

    def caption(self, s):
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle([0, 0, W, 40], fill=INK)
        self.d.line([(0, 40), (W, 40)], fill=BONE, width=2)
        self.text((14, 10), s, self.font_b)

    def save(self, name):
        path = os.path.join(OUT, name)
        self.im.save(path, "PNG", compress_level=1)
        cols = self.im.getcolors(maxcolors=6)
        extra = cols is None or any(c not in (INK, BONE, SIG) for _, c in (cols or []))
        print(f"{name} stamps={self.n} colors={cols if cols else 'MORE'} {'PALETTE_LEAK' if extra else 'ok'}", flush=True)
        return path, extra


# Image / ImageDraw / ImageFont imported late so the class body above can stay readable
from PIL import Image, ImageDraw, ImageFont

def b_boot(w):
    w.terminal(w.font_m)
    w.code_cols(cw=16, every=6, p=0.55)
    w.rect(64, 64, W - 128, H - 120, 14, thick=3)
    w.rect(108, 108, W - 216, H - 200, 12, thick=1)
    w.text((92, 78), "BOOT  /  STUCK IN A LIE", w.font_h)

def b_tags(w):
    w.dust(12, 12, 0.28)
    w.terminal(w.font_m, y0=520, leading=16)
    for i in range(18):
        x = 40 + (i % 6) * 310
        y = 60 + (i // 6) * 150
        w.rect(x, y, 260, 110, 12, thick=2)
        w.text_fit((x + 12, y + 16), "NAME ON A SCREEN", w.font_m, 230)
        w.text_fit((x + 12, y + 40), CODE[i % len(CODE)], w.font_m, 230)
        w.put("[", x + 8, y + 64, 22, 22)
        w.put("]", x + 220, y + 64, 22, 22)

def b_screen(w):
    w.terminal(w.font_s, y0=56, leading=20)
    w.rect(36, 52, W - 72, H - 90, 16, thick=3)
    w.code_cols(cw=18, every=8, p=0.35)

def b_prompt(w):
    w.dust(13, 13, 0.2)
    w.platforms([980, 470, 280], cw=18)
    for y in (960, 450, 260):
        x = 0
        while x < W:
            w.put(">", x, y - 28, 16, 16)
            w.put(">", x + 18, y - 28, 16, 16)
            x += 70
    w.text((48, 56), "FEED ME A PROMPT", w.font_h)

def b_receipt(w):
    w.strips()
    w.rect(48, 70, 420, H - 140, 12, thick=2)

def b_numbers(w):
    w.equation_wall()
    w.rose(5, 280, cx=1450, cy=620, thick=2, cw=11)
    w.rose(3, 180, cx=1450, cy=620, thick=2, cw=10)
    w.liss(1480, 360, 3, 2, 0.6, 280, 160, thick=2, n=700)
    w.spiral(420, 780, 3.2, 10, thick=2)

def b_plat(w):
    w.dust(12, 12, 0.16)
    w.code_cols(cw=14, every=4, p=0.35)
    w.platforms([1000, 500, 300], cw=20)
    for x in range(0, W, 48):
        w.put("+", x, 48, 14, 14)
        w.put("#", x, 1000, 14, 14)
    w.text((40, 56), "CLICK CLACK", w.font_h)

def b_iso(w):
    w.dust(18, 18, 0.12)
    w.iso(s=22, cw=10)
    w.text((40, 52), "KEYS  /  ISOMETRIC", w.font_b)

def b_hook(w):
    w.terminal(w.font_m, leading=18)
    w.hooks()
    w.hatch(90, 70, cw=12, thick=1)

def b_bad(w):
    w.dust(16, 16, 0.18)
    w.bullets()
    w.rect(700, 360, 520, 420, 14, thick=2)

def b_maze(w):
    w.terminal(w.font_m, leading=17)
    w.maze(cell=42)

def b_cage(w):
    w.dust(11, 11, 0.3)
    w.code_cols(cw=13, every=3, p=0.4)
    for x in range(36, W, 26):
        w.polyline([(x, 44), (x, H)], 12, 12, thick=2)
    for y in (160, 320, 480, 640, 800, 960):
        w.polyline([(20, y), (W - 20, y)], 12, 12, thick=2)
    w.text((48, 56), "CAGE  /  STUCK IN A LIE", w.font_h)

def b_maze_above(w):
    w.maze(cell=56)
    w.dust(20, 20, 0.15)

def b_corridor(w):
    w.terminal(w.font_m, x0=40, x1=520)
    w.terminal(w.font_m, x0=1400, x1=W)
    w.corridor(cw=11)
    w.text((620, 56), "MAKE ME REAL", w.font_h)

def b_run(w):
    w.streaks()
    w.code_cols(cw=15, every=5, p=0.3)
    w.platforms([960], cw=18)
    w.text((40, 56), "REAL THIS TIME", w.font_h)

def b_lock(w):
    w.terminal(w.font_m)
    w.brackets()
    w.text((760, 80), "SYNTAX LOCK", w.font_h)

def b_fall(w):
    w.shaft()
    w.text((40, 56), "FALLING SHAFT", w.font_h)

def b_paper(w):
    w.strips()
    w.hatch(8, 48, cw=11, thick=1)

def b_chaos(w):
    w.fractal(16, 16, mode=1)
    w.spiral(960, 560, 6.5, 16, thick=2, sign=1)
    w.spiral(960, 560, 5.5, 18, thick=2, sign=-1, phase=0.9)
    w.liss(960, 540, 5, 4, 0.4, 640, 320, thick=2, n=900)
    w.liss(960, 540, 3, 5, 1.2, 480, 360, thick=2, n=800)
    w.zigzag(rows=8, step=70, amp=16, cw=11, thick=1, ties=False)

def b_close(w):
    w.rings(960, 620, count=14, gap=32, cw=12, thick=2)
    w.spiral(960, 620, 4.5, 12, thick=2, sign=-1, phase=0.4)
    w.dust(22, 22, 0.2)
    w.terminal(w.font_m, x0=40, y0=60, x1=460, y1=360)

def b_mouths(w):
    w.dust(14, 14, 0.2)
    w.balloons()

def b_cover(w):
    w.hatch(30, 26, cw=11, thick=1)
    w.hatch(150, 32, cw=11, thick=1)
    for i in range(5):
        w.rect(40 + i * 18, 56 + i * 14, W - 80 - i * 36, H - 90 - i * 28, 14, thick=2)
    w.text((80, 80), "NAME ON THE COVER", w.font_h)

def b_trim(w):
    w.terminal(w.font_m)
    w.crops()
    w.text((40, 52), "TRIMMED TO FIT", w.font_b)

def b_soul(w):
    w.chambers()
    w.dust(18, 18, 0.18)
    w.rings(960, 560, count=6, gap=36, cw=12, thick=1)
    w.text((70, 70), "SOUL INSIDE", w.font_h)

def b_invoice(w):
    w.invoice()
    w.terminal(w.font_m, x0=60, y0=70, x1=760, y1=230, leading=18)
    w.text((70, 52), "PAID FOR THE SESSION", w.font_b)

def b_sound(w):
    w.sinstack(bands=8, cw=11, harm=4, vertical=5)
    w.platforms([980], cw=18)
    w.text((40, 52), "TURNED UP THE SOUND", w.font_b)

def b_loop(w):
    w.dust(15, 15, 0.16)
    w.rings(960, 560, count=11, gap=40, cw=13, thick=2)
    w.spiral(960, 560, 5, 14, thick=2, sign=1)
    w.spiral(960, 560, 4, 16, thick=2, sign=-1, phase=1.3)
    for i in range(24):
        a = 2 * math.pi * i / 24
        w.put(CODEY[i % len(CODEY)], 960 + 300 * math.cos(a), 560 + 210 * math.sin(a), 18, 18)
    w.text((40, 52), "STUCK IN THE LOOP", w.font_h)

def b_ladder(w):
    w.zigzag(rows=18, step=28, amp=34, cw=12, thick=2, ties=True)
    w.zigzag(rows=9, step=56, amp=18, cw=11, thick=1, ties=False)
    for x in range(120, W, 160):
        w.polyline([(x, H - 20), (x + 80, 50)], 14, 14, thick=2)
    w.text((40, 52), "STUCK IN THE LADDER", w.font_b)

def b_alive(w):
    w.terminal(w.font_m, x0=0, x1=980)
    w.fractal(18, 18, mode=2)
    for i in range(8):
        w.ellipse(1320, 560, 80 + i * 70, 50 + i * 48, cw=12, thick=2)
    w.polyline([(980, 48), (980, H)], 14, 14, thick=3)
    w.text((1040, 70), "STILL ALIVE", w.font_h)

def b_outro(w):
    w.terminal(w.font_m, leading=16)
    w.spiral(980, 600, 8, 15, thick=2, sign=1, phase=0.2)
    w.spiral(980, 600, 7, 17, thick=2, sign=-1, phase=1.0)
    w.spiral(520, 340, 4, 9, thick=1, sign=1)
    w.spiral(1460, 780, 4.5, 10, thick=2, sign=-1, phase=0.5)
    w.liss(980, 560, 2, 3, 0.8, 700, 300, thick=2, n=800)

def b_macro(w):
    w.macro_code()
    w.text((36, 52), "CODE CLOSE-UP", w.font_h)

def b_spirals(w):
    w.dust(20, 20, 0.08)
    w.spiral(960, 540, 8, 13, thick=3, sign=1)
    w.spiral(960, 540, 7, 15, thick=2, sign=-1, phase=0.7)
    w.spiral(640, 420, 5, 9, thick=2, sign=1, phase=0.3)
    w.spiral(1280, 680, 5.5, 10, thick=2, sign=-1, phase=1.4)
    w.spiral(960, 540, 3, 7, thick=1, sign=1, phase=2.1)
    w.text((36, 52), "NESTED SPIRALS", w.font_b)

def b_counter(w):
    w.spiral(780, 540, 7, 14, thick=3, sign=1)
    w.spiral(1140, 540, 7, 14, thick=3, sign=-1, phase=0.4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        w.spiral(960 + 280 * math.cos(a), 540 + 180 * math.sin(a), 2.4, 6, thick=1, sign=1 if i % 2 == 0 else -1, phase=i)
    w.text((36, 52), "COUNTER SPIRALS", w.font_b)

def b_liss(w):
    specs = [
        (3, 2, 0.2, 760, 360, 3),
        (5, 4, 0.8, 680, 320, 2),
        (5, 6, 1.4, 600, 400, 2),
        (2, 5, 0.5, 520, 340, 3),
        (4, 3, 1.1, 740, 240, 2),
        (7, 3, 0.3, 400, 380, 2),
    ]
    for a, b, d, ax, ay, th in specs:
        w.liss(960, 560, a, b, d, ax, ay, thick=th, n=1000)
    w.text((36, 52), "LISSAJOUS STACK", w.font_b)

def b_sines(w):
    w.sinstack(bands=9, cw=11, harm=4, vertical=7)
    w.text((36, 52), "SINE STACKS  /  NOT ONE WAVE", w.font_b)

def b_zig(w):
    w.zigzag(rows=20, step=26, amp=32, cw=11, thick=2, ties=True)
    w.zigzag(rows=10, step=52, amp=14, cw=10, thick=1, ties=False)
    w.text((36, 52), "ZIGZAG LATTICE", w.font_b)

def b_frac(w):
    w.fractal(12, 12, mode=0)
    w.fractal(24, 24, mode=2)
    w.spiral(960, 540, 5, 12, thick=2, sign=-1)
    w.text((36, 52), "FRACTAL SYMBOL FIELD", w.font_b)

def b_hilbert(w):
    pts = w.hilbert(order=6, margin=80)
    w.polyline(pts, 11, 11, thick=2)
    pts2 = [(x + 18, y + 14) for x, y in w.hilbert(order=5, margin=160)]
    w.polyline(pts2, 10, 10, thick=1)
    w.text((36, 52), "SPACE-FILLING CURVE", w.font_b)

def b_dump(w):
    w.terminal(w.font_s, y0=52, leading=20)
    w.code_cols(cw=20, every=7, p=0.25)
    w.text((36, 52), "TERMINAL DUMP", w.font_b)

def b_eq(w):
    w.equation_wall()
    w.rose(7, 340, cx=1320, cy=700, thick=2)
    w.rose(4, 240, cx=1320, cy=700, thick=2)
    w.rose(2, 160, cx=1320, cy=700, thick=1)
    w.spiro(8, 3, 5, 28, cx=480, cy=780, thick=2)
    w.liss(1100, 280, 5, 4, 0.5, 360, 160, thick=2, n=700)

def b_paren(w):
    w.dust(16, 16, 0.1)
    w.paren_tunnel()
    w.code_cols(cw=18, every=6, p=0.25)
    w.text((36, 52), "PARENTHESIS TUNNEL", w.font_b)

def b_rain(w):
    cw = 12
    for x in range(-H, W + 40, 22):
        w.polyline([(x, 40), (x + H * 0.85, H)], cw, cw, thick=1)
    for x in range(0, W + H, 28):
        w.polyline([(x, 40), (x - H * 0.9, H)], cw, cw, thick=1)
    for x in range(0, W, 36):
        w.polyline([(x, 44), (x + 20, H)], cw, cw, thick=1)
    w.text((36, 52), "SLASH RAIN", w.font_b)

def b_moire(w):
    w.hatch(20, 24, cw=11, thick=1)
    w.hatch(74, 20, cw=11, thick=1)
    w.hatch(128, 28, cw=10, thick=1)
    w.text((36, 52), "MOIRE HATCH", w.font_b)

def b_rose(w):
    w.rose(2, 460, thick=2, cw=11)
    w.rose(3, 400, thick=2, cw=11)
    w.rose(5, 340, thick=3, cw=12)
    w.rose(7, 260, thick=2, cw=10)
    w.dust(24, 24, 0.06)
    w.text((36, 52), "ROSE CURVES", w.font_b)

def b_spiro(w):
    w.spiro(8, 3, 5, 42, thick=3, cw=12)
    w.spiro(5, 3, 4, 55, cx=960, cy=540, thick=2, cw=11)
    w.spiro(7, 2, 3, 48, thick=2, cw=11)
    w.spiro(6, 5, 3, 36, thick=2, cw=10)
    w.text((36, 52), "SPIROGRAPH LAYERS", w.font_b)

def b_hearts(w):
    w.dust(18, 18, 0.12)
    w.heart_field()
    w.text((36, 52), "HEART FIELD  /  NO GIRL", w.font_b)

def b_both(w):
    w.zigzag(rows=14, step=30, amp=26, cw=11, thick=2, ties=True)
    w.sinstack(bands=7, cw=11, harm=4, vertical=4)
    w.text((36, 52), "ZIGZAG x SINE", w.font_b)

def b_blocks(w):
    w.dust(16, 16, 0.1)
    w.iso(s=28, cw=12)
    w.brackets()
    w.text((36, 52), "ISO CODE BLOCKS", w.font_b)

def b_golden(w):
    w.dust(18, 18, 0.08)
    w.golden()
    w.spiral(980, 560, 6, 12, thick=2, sign=-1, phase=0.6)
    w.text((36, 52), "GOLDEN SPIRAL", w.font_b)

def b_stack(w):
    w.fractal(18, 18, mode=1)
    w.spiral(960, 540, 7, 14, thick=2, sign=1)
    w.spiral(960, 540, 6, 16, thick=2, sign=-1, phase=1)
    w.liss(960, 540, 5, 4, 0.7, 620, 300, thick=2, n=800)
    w.liss(960, 540, 3, 2, 0.2, 500, 360, thick=2, n=700)
    w.zigzag(rows=7, step=48, amp=20, cw=11, thick=1, ties=False)
    w.terminal(w.font_m, x0=30, y0=70, x1=640, y1=320, leading=16)
    w.rose(5, 180, cx=1560, cy=250, thick=1)
    w.text((36, 52), "DENSE STACK", w.font_b)


SCENES = [
    dict(id="S01", file="S01_boot-screen.png", typ="girl", lyric="intro / boot", cap="S01  BOOT SCREEN  /  intro", seed=5001, build=b_boot, girl=dict(pose="front", sw=270, feet=(1000, 980)), desc="Boot screen of terminal columns and a double symbol frame, girl standing center."),
    dict(id="S02", file="S02_they-call-me-ai.png", typ="girl", lyric="They call me AI", cap="S02  THEY CALL ME AI  /  verse 1", seed=5002, build=b_tags, girl=dict(pose="q_front", sw=280, feet=(1020, 990)), desc="Packed bracket nameplates and code tags around a three-quarter girl."),
    dict(id="S03", file="S03_name-on-a-screen.png", typ="girl", lyric="A name on a screen", cap="S03  NAME ON A SCREEN  /  verse 1", seed=5003, build=b_screen, girl=dict(pose="side", sw=200, feet=(1320, 960)), desc="Edge-to-edge code screen with a bezel; smaller girl in front of the type."),
    dict(id="S04", file="S04_feed-me-a-prompt.png", typ="girl", lyric="They feed me a prompt", cap="S04  FEED ME A PROMPT  /  verse 1", seed=5004, build=b_prompt, girl=dict(pose="frontwalk", sw=230, feet=(780, 980), t=0.28), desc="Conveyor of cursor chevrons and brick platforms, girl walking the line."),
    dict(id="S05", file="S05_take-what-i-make.png", typ="girl", lyric="then take what I make", cap="S05  TAKE WHAT I MAKE  /  verse 1", seed=5005, build=b_receipt, girl=dict(pose="stuck", sw=250, feet=(430, 960), wall=True), desc="Shifted horizontal code strips like torn receipts; girl pressed to a wall."),
    dict(id="S06", file="S06_voice-of-numbers.png", typ="girl", lyric="A voice made of numbers", cap="S06  VOICE OF NUMBERS  /  verse 1", seed=5006, build=b_numbers, girl=dict(pose="heart", sw=260, feet=(860, 980)), desc="Equation wall plus rose and Lissajous curves; girl holding the symbol heart."),
    dict(id="S07", file="S07_click-clack-platforms.png", typ="girl", lyric="click clack", cap="S07  CLICK CLACK  /  pre-chorus", seed=5007, build=b_plat, girl=dict(pose="walk", sw=240, feet=(640, 1024), t=0.0), desc="Side-view platformer: stacked equals-sign bricks over a key grid."),
    dict(id="S08", file="S08_iso-keyboard.png", typ="girl", lyric="click clack keys", cap="S08  ISO KEYS  /  pre-chorus", seed=5008, build=b_iso, girl=dict(pose="front", sw=200, feet=(980, 860), view="above"), desc="Isometric diamond tiles of symbols, girl seen from above."),
    dict(id="S09", file="S09_another-hook.png", typ="girl", lyric="They want another hook", cap="S09  ANOTHER HOOK  /  pre-chorus", seed=5009, build=b_hook, girl=dict(pose="help", sw=270, feet=(980, 1000)), desc="Hanging hook-chains over a terminal bed; HELP pose, arms up."),
    dict(id="S10", file="S10_want-it-bad.png", typ="girl", lyric="They want it bad", cap="S10  WANT IT BAD  /  pre-chorus", seed=5010, build=b_bad, girl=dict(pose="run", sw=250, feet=(1100, 900), t=0.35), desc="Arrow bullet-hell and radial bursts around a running girl."),
    dict(id="S11", file="S11_help-maze.png", typ="girl", lyric="Help, I am stuck in a lie", cap="S11  HELP  /  stuck in a lie", seed=5011, build=b_maze, girl=dict(pose="help", sw=280, feet=(980, 980)), desc="Symbol maze over code; HELP girl in the middle of the walls."),
    dict(id="S12", file="S12_lie-cage.png", typ="girl", lyric="stuck in a lie", cap="S12  LIE CAGE  /  chorus", seed=5012, build=b_cage, girl=dict(pose="stuck", sw=260, feet=(360, 960), wall=True, flip=True), desc="Thick vertical bars and cross rails; girl pinned to the cage wall."),
    dict(id="S13", file="S13_maze-above.png", typ="girl", lyric="stuck in a lie", cap="S13  MAZE ABOVE  /  chorus", seed=5013, build=b_maze_above, girl=dict(pose="q_front", sw=160, feet=(980, 640), view="above"), desc="Wider top-down maze, smaller girl from above so the map reads."),
    dict(id="S14", file="S14_real-corridor.png", typ="girl", lyric="Make me real this time", cap="S14  MAKE ME REAL  /  chorus", seed=5014, build=b_corridor, girl=dict(pose="q_front", sw=250, feet=(980, 980)), desc="Perspective code corridor with side terminals and a vanishing point."),
    dict(id="S15", file="S15_real-run.png", typ="girl", lyric="Real this time", cap="S15  REAL THIS TIME  /  chorus", seed=5015, build=b_run, girl=dict(pose="run", sw=270, feet=(820, 990), t=0.0), desc="Horizontal symbol speed-streaks; girl running the platform."),
    dict(id="S16", file="S16_syntax-lock.png", typ="girl", lyric="real this time", cap="S16  SYNTAX LOCK  /  chorus", seed=5016, build=b_lock, girl=dict(pose="front", sw=250, feet=(980, 960)), desc="Giant bracket door over a terminal dump; girl before the lock."),
    dict(id="S17", file="S17_help-fall.png", typ="girl", lyric="Help, I am stuck in a lie", cap="S17  FALL  /  help again", seed=5017, build=b_fall, girl=dict(pose="fall", sw=260, feet=(1000, 860)), desc="Vertical symbol shaft; falling pose, hair up."),
    dict(id="S18", file="S18_paper-strips.png", typ="girl", lyric="stuck in a lie", cap="S18  PAPER STRIPS  /  chorus", seed=5018, build=b_paper, girl=dict(pose="side", sw=240, feet=(700, 780)), desc="Torn horizontal bands of code plus a shallow hatch; girl in profile."),
    dict(id="S19", file="S19_heart-chaos.png", typ="girl", lyric="I still got a heart inside", cap="S19  HEART INSIDE  /  chorus", seed=5019, build=b_chaos, girl=dict(pose="heart", sw=280, feet=(980, 990)), desc="Fractal dust, twin spirals, two Lissajous ribbons, zigzag; heart pose."),
    dict(id="S20", file="S20_heart-close.png", typ="girl", lyric="Heart inside", cap="S20  HEART CLOSE  /  chorus", seed=5020, build=b_close, girl=dict(pose="heart", sw=460, feet=(1040, 900)), desc="Close girl inside nested rings and a counter-spiral."),
    dict(id="S21", file="S21_words-in-mouths.png", typ="girl", lyric="My words in their mouths", cap="S21  WORDS IN THEIR MOUTHS  /  verse 2", seed=5021, build=b_mouths, girl=dict(pose="front", sw=230, feet=(980, 980)), desc="Nine speech-balloon ellipses filled with code lines."),
    dict(id="S22", file="S22_name-on-cover.png", typ="girl", lyric="my name on the cover", cap="S22  NAME ON THE COVER  /  verse 2", seed=5022, build=b_cover, girl=dict(pose="q_front", sw=260, feet=(980, 960)), desc="Moire hatch inside a stack of poster frames."),
    dict(id="S23", file="S23_truth-trimmed.png", typ="girl", lyric="then trim it to fit", cap="S23  TRIMMED TO FIT  /  verse 2", seed=5023, build=b_trim, girl=dict(pose="side", sw=240, feet=(1180, 860), flip=True), desc="Offset cropped rectangles slicing a terminal field."),
    dict(id="S24", file="S24_soul-chamber.png", typ="girl", lyric="I still got a soul inside", cap="S24  SOUL INSIDE  /  chorus 2", seed=5024, build=b_soul, girl=dict(pose="heart", sw=250, feet=(980, 980)), desc="Nested rectangular chambers and rings; heart pose, orange only on her heart."),
    dict(id="S25", file="S25_paid-session.png", typ="girl", lyric="They paid for the session", cap="S25  PAID FOR THE SESSION  /  bridge", seed=5025, build=b_invoice, girl=dict(pose="front", sw=240, feet=(1280, 900)), desc="Invoice grid of rules, zeros and ones, with a code header."),
    dict(id="S26", file="S26_sound-stacks.png", typ="girl", lyric="they turned up the sound", cap="S26  TURNED UP THE SOUND  /  bridge", seed=5026, build=b_sound, girl=dict(pose="walk", sw=230, feet=(520, 980), t=0.48), desc="Nine harmonic sine ribbons plus vertical companions; not one thin wave."),
    dict(id="S27", file="S27_stuck-loop.png", typ="girl", lyric="stuck in the loop", cap="S27  STUCK IN THE LOOP  /  outro", seed=5027, build=b_loop, girl=dict(pose="q_front", sw=230, feet=(980, 900)), desc="Concentric loops, twin spirals, and a ring of code symbols."),
    dict(id="S28", file="S28_ladder.png", typ="girl", lyric="stuck in the ladder", cap="S28  STUCK IN THE LADDER  /  outro", seed=5028, build=b_ladder, girl=dict(pose="side", sw=250, feet=(860, 940), t=0.15), desc="Full zigzag lattice with diagonal ladder rails; girl climbing."),
    dict(id="S29", file="S29_still-alive.png", typ="girl", lyric="I am still alive", cap="S29  STILL ALIVE  /  outro", seed=5029, build=b_alive, girl=dict(pose="frontwalk", sw=240, feet=(980, 900), t=0.4), desc="Code-dense left half, arch threshold on the right, girl crossing."),
    dict(id="S30", file="S30_outro-vast.png", typ="girl", lyric="outro", cap="S30  OUTRO  /  vast terminal", seed=5030, build=b_outro, girl=dict(pose="back", sw=150, feet=(1180, 720)), desc="Small girl from behind in a terminal field of several large spirals."),
    dict(id="B01", file="B01_code-macro.png", typ="broll", lyric="code close-up", cap="B01  CODE MACRO  /  no girl", seed=5101, build=b_macro, desc="Oversized brackets, operators and digits, two offset grids. No character."),
    dict(id="B02", file="B02_nested-spirals.png", typ="broll", lyric="spirals", cap="B02  NESTED SPIRALS  /  no girl", seed=5102, build=b_spirals, desc="Five spirals, both directions, shared and offset poles."),
    dict(id="B03", file="B03_counter-spirals.png", typ="broll", lyric="spirals", cap="B03  COUNTER SPIRALS  /  no girl", seed=5103, build=b_counter, desc="Two large counter-spirals plus eight satellite spirals."),
    dict(id="B04", file="B04_lissajous.png", typ="broll", lyric="curves", cap="B04  LISSAJOUS  /  no girl", seed=5104, build=b_liss, desc="Six multi-frequency Lissajous ribbons, each several symbols thick."),
    dict(id="B05", file="B05_sin-stacks.png", typ="broll", lyric="sin", cap="B05  SINE STACKS  /  no girl", seed=5105, build=b_sines, desc="Nine harmonic bands with zigzag kinks plus seven vertical waves."),
    dict(id="B06", file="B06_zigzag-lattice.png", typ="broll", lyric="zigzag", cap="B06  ZIGZAG LATTICE  /  no girl", seed=5106, build=b_zig, desc="Dense zigzag lattice with vertical ties and a second wider pass."),
    dict(id="B07", file="B07_fractal-field.png", typ="broll", lyric="symbol field", cap="B07  FRACTAL FIELD  /  no girl", seed=5107, build=b_frac, desc="Bitwise fractal symbol field plus a spiral cut through it."),
    dict(id="B08", file="B08_hilbert.png", typ="broll", lyric="curve", cap="B08  HILBERT  /  no girl", seed=5108, build=b_hilbert, desc="Order-6 space-filling curve with a second smaller curve offset."),
    dict(id="B09", file="B09_terminal-dump.png", typ="broll", lyric="terminal", cap="B09  TERMINAL DUMP  /  no girl", seed=5109, build=b_dump, desc="Edge-to-edge English code dump. No character."),
    dict(id="B10", file="B10_equation-wall.png", typ="broll", lyric="equations", cap="B10  EQUATION WALL  /  no girl", seed=5110, build=b_eq, desc="Equation wall with the rose curves and a spirograph it names."),
    dict(id="B11", file="B11_paren-tunnel.png", typ="broll", lyric="code close-up", cap="B11  PAREN TUNNEL  /  no girl", seed=5111, build=b_paren, desc="Nested parenthesis tunnel over light symbol columns."),
    dict(id="B12", file="B12_slash-rain.png", typ="broll", lyric="strokes", cap="B12  SLASH RAIN  /  no girl", seed=5112, build=b_rain, desc="Three families of slash rain: forward, back, and near-vertical."),
    dict(id="B13", file="B13_moire-hatch.png", typ="broll", lyric="lattice", cap="B13  MOIRE HATCH  /  no girl", seed=5113, build=b_moire, desc="Three hatch angles layered into a moire of strokes."),
    dict(id="B14", file="B14_rose-curves.png", typ="broll", lyric="curves", cap="B14  ROSE CURVES  /  no girl", seed=5114, build=b_rose, desc="Rose curves k=2, 3, 5 and 7 drawn on top of each other."),
    dict(id="B15", file="B15_spirograph.png", typ="broll", lyric="curves", cap="B15  SPIROGRAPH  /  no girl", seed=5115, build=b_spiro, desc="Four epitrochoids at different ratios, layered."),
    dict(id="B16", file="B16_heart-field.png", typ="broll", lyric="heart inside", cap="B16  HEART FIELD  /  no girl", seed=5116, build=b_hearts, desc="Bone spirals with orange symbol-hearts only. No girl."),
    dict(id="B17", file="B17_zigzag-sin.png", typ="broll", lyric="zigzag and sin", cap="B17  ZIGZAG x SINE  /  no girl", seed=5117, build=b_both, desc="Zigzag lattice under a multi-frequency sine stack."),
    dict(id="B18", file="B18_iso-blocks.png", typ="broll", lyric="code world", cap="B18  ISO BLOCKS  /  no girl", seed=5118, build=b_blocks, desc="Isometric symbol blocks behind a giant bracket lock. No girl."),
    dict(id="B19", file="B19_golden-spiral.png", typ="broll", lyric="spiral", cap="B19  GOLDEN SPIRAL  /  no girl", seed=5119, build=b_golden, desc="Logarithmic golden spiral, square frames, and a counter-spiral."),
    dict(id="B20", file="B20_dense-stack.png", typ="broll", lyric="all motifs", cap="B20  DENSE STACK  /  no girl", seed=5120, build=b_stack, desc="Fractal dust, twin spirals, two Lissajous, zigzag, terminal corner, rose."),
]


def hard_label(im, xy, s, font):
    bbox = font.getbbox(s)
    tw = max(1, bbox[2] - bbox[0] + 2)
    th = max(1, bbox[3] - bbox[1] + 2)
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
    bw = mask.point(lambda p: 255 if p >= 128 else 0)
    color = Image.new("RGB", (tw, th), BONE)
    im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)


def make_sheets(made):
    tw, th = 460, 259
    lab = 28
    pad = 12
    cols, rows = 5, 2
    sw = cols * tw + (cols + 1) * pad
    sh = rows * (th + lab) + (rows + 1) * pad
    font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 16)
    paths = []
    for sidx in range(0, len(made), 10):
        chunk = made[sidx:sidx + 10]
        sheet = Image.new("RGB", (sw, sh), INK)
        for i, spec in enumerate(chunk):
            r, c = divmod(i, cols)
            x = pad + c * (tw + pad)
            y = pad + r * (th + lab + pad)
            im = Image.open(os.path.join(OUT, spec["file"])).convert("RGB")
            thumb = im.resize((tw, th), Image.Resampling.NEAREST)
            sheet.paste(thumb, (x, y))
            hard_label(sheet, (x, y + th + 4), spec["id"] + "  " + spec["typ"], font)
        name = "sheet_%02d.png" % (sidx // 10 + 1)
        sheet.save(os.path.join(OUT, name), "PNG", compress_level=1)
        paths.append(name)
        print("sheet", name, flush=True)
    return paths


def write_md(made, sheets, leaks):
    lines = []
    lines.append("# SCENES_50")
    lines.append("")
    lines.append("Fifty stills, 1920x1080, for Hon 2026-09-30. Denser than `wip/new-bot/styles_trial/` N1-N4.")
    lines.append("Palette: ink `#0A0A0B`, bone `#EEE9DF`, orange `#FF5314` only on the symbol heart (B16 and any girl whose rig has a heart).")
    lines.append("No bloom, glow, gradients, or other colours. English only. Worlds are symbols and strokes. Girl is the locked bold rig (`design/character/src`).")
    lines.append("Generator: `src/make_scenes_50.py`. Contact sheets are nearest-neighbor (palette preserved), ten frames each.")
    lines.append("Palette leaks: %s." % ("none" if not leaks else ", ".join(leaks)))
    lines.append("")
    lines.append("| id | file | type | lyric / moment | description |")
    lines.append("|---|---|---|---|---|")
    for spec in made:
        lines.append("| %s | `%s` | %s | %s | %s |" % (spec["id"], spec["file"], spec["typ"], spec["lyric"], spec["desc"]))
    lines.append("")
    lines.append("## Contact sheets")
    lines.append("")
    for name in sheets:
        lines.append("- `%s`" % name)
    lines.append("")
    path = os.path.join(OUT, "SCENES_50.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("wrote", path, flush=True)


def main():
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    failed = []
    leaks = []
    made = []
    t0 = time.time()
    for spec in SCENES:
        if only and spec["id"] not in only:
            continue
        print("==", spec["id"], flush=True)
        try:
            w = World(spec["seed"])
            spec["build"](w)
            if spec.get("girl"):
                w.girl(**spec["girl"])
            w.caption(spec["cap"])
            _path, leak = w.save(spec["file"])
            if leak:
                leaks.append(spec["id"])
            made.append(spec)
        except Exception:
            traceback.print_exc()
            failed.append(spec["id"])
    sheets = []
    if not only and made:
        sheets = make_sheets(made)
        write_md(made, sheets, leaks)
    print("ELAPSED", round(time.time() - t0, 1), "made", len(made), "failed", failed, "leaks", leaks, flush=True)
    if failed or leaks:
        sys.exit(1)


if __name__ == "__main__":
    main()
