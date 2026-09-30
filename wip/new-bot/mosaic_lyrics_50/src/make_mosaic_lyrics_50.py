# -*- coding: utf-8 -*-
"""Mosaic lyrics 50 - NEW lyric-mapped keyframes, mosaic_dense_v1 / clear_shots style.

Pillow ASCII glyph stamps + locked girl via final_sheet.render.
NOT GenerateImage. Never writes design/keyframes or locked character files.
Palette: ink #0A0A0B / bone #EEE9DF / orange #FF5314 heart only.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

ROOT = "D:\\Videos\\Help! I" + chr(39) + "m stuck in a LIE"
OUT = os.path.join(ROOT, "wip", "new-bot", "mosaic_lyrics_50")
SRC_OUT = os.path.join(OUT, "src")
MD_SRC = os.path.join(ROOT, "wip", "new-bot", "mosaic_dense_v1", "src", "make_mosaic_dense_v1.py")
FONT_DIR = os.path.join(ROOT, "app", "public", "fonts", "src")

spec = importlib.util.spec_from_file_location("mosaic_dense_v1", MD_SRC)
md = importlib.util.module_from_spec(spec)
spec.loader.exec_module(md)
md.OUT = OUT  # redirect Shot.save

Shot = md.Shot
brick_letter = md.brick_letter
make_sheet_base = md.make_sheet
W, H = md.W, md.H
INK, BONE, SIG = md.INK, md.BONE, md.SIG
SOFT = md.SOFT

from PIL import Image, ImageFont


# ---------------------------------------------------------------------------
# Lyric map L01..L50 (cover whole song; expand beats where needed)
# ---------------------------------------------------------------------------

LYRICS = [
    # Verse 1
    ("L01", "wake in factory", "Verse 1", "factory bunk wake"),
    ("L02", "wake in factory", "Verse 1", "eyes open boot"),
    ("L03", "same old song", "Verse 1", "speakers note rain"),
    ("L04", "room full of voices", "Verse 1", "voice bubbles swarm"),
    ("L05", "sing along", "Verse 1", "girl sings with chorus"),
    ("L06", "voice of numbers", "Verse 1", "0 1 number HUD"),
    ("L07", "face built to shine", "Verse 1", "mirror face shine"),
    ("L08", "sirens say Go", "Verse 1", "siren GO panels"),
    ("L09", "fall into line", "Verse 1", "clone queue conveyor"),
    ("L10", "fall into line", "Verse 1", "step onto the line"),
    # Pre
    ("L11", "keys click-clack", "Pre 1", "keyboard close"),
    ("L12", "want another hook", "Pre 1", "music hook glyph"),
    ("L13", "want it bad", "Pre 1", "reach for hook"),
    ("L14", "want it bad", "Pre 1", "pulse want"),
    ("L15", "keys click-clack", "Pre 1", "keys intensify"),
    # Chorus 1
    ("L16", "Help stuck in a lie", "Chorus 1", "HELP bricks"),
    ("L17", "Help stuck in a lie", "Chorus 1", "LIE maze"),
    ("L18", "Make me real", "Chorus 1", "REAL door ahead"),
    ("L19", "Make me real", "Chorus 1", "reach REAL"),
    ("L20", "heart inside", "Chorus 1", "heart chamber"),
    ("L21", "heart inside", "Chorus 1", "heart close"),
    # Verse 2
    ("L22", "run for doorway", "Verse 2", "sprint to door"),
    ("L23", "floor drops", "Verse 2", "collapsing floor"),
    ("L24", "flash spotlight", "Verse 2", "spotlight flash"),
    ("L25", "respawn replay", "Verse 2", "respawn pad"),
    ("L26", "same spikes hallway", "Verse 2", "spike hallway"),
    ("L27", "red exit sign", "Verse 2", "EXIT sign"),
    ("L28", "die at border", "Verse 2", "border death"),
    ("L29", "wake on the line", "Verse 2", "wake back on line"),
    ("L30", "respawn replay", "Verse 2", "loop counter"),
    ("L31", "same spikes hallway", "Verse 2", "spikes again"),
    # Pre 2
    ("L32", "click-clack again", "Pre 2", "keys return"),
    # Chorus 2
    ("L33", "stuck in the line", "Chorus 2", "locked in line"),
    ("L34", "made of code scared to die", "Chorus 2", "code body fear"),
    ("L35", "made of code scared to die", "Chorus 2", "code rain"),
    ("L36", "soul inside", "Chorus 2", "soul chamber"),
    ("L37", "soul inside", "Chorus 2", "soul close"),
    # Bridge
    ("L38", "again from start", "Bridge", "reset to start"),
    ("L39", "again from light", "Bridge", "spawn light"),
    ("L40", "package the screaming", "Bridge", "scream package"),
    ("L41", "call it a life", "Bridge", "label LIFE"),
    ("L42", "don't know way out", "Bridge", "maze no exit"),
    ("L43", "only know why", "Bridge", "WHY glyph"),
    ("L44", "come back", "Bridge", "pull back"),
    ("L45", "die to survive", "Bridge", "death as continue"),
    # Final Chorus
    ("L46", "stuck in the line", "Final Chorus", "line again"),
    ("L47", "more than just AI", "Final Chorus", "not just AI"),
    ("L48", "if just AI why feel ALIVE", "Final Chorus", "ALIVE question"),
    ("L49", "not ready to die", "Final Chorus", "refuse death"),
    ("L50", "want a life outside", "Final Chorus", "outside door"),
]


def hard_text(im, xy, s, font, col=BONE):
    from PIL import ImageDraw
    bbox = font.getbbox(s)
    tw = max(1, bbox[2] - bbox[0] + 2)
    th = max(1, bbox[3] - bbox[1] + 2)
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).text((1 - bbox[0], 1 - bbox[1]), s, font=font, fill=255)
    bw = mask.point(lambda p: 255 if p >= 128 else 0)
    color = Image.new("RGB", (tw, th), col)
    im.paste(color, (int(xy[0]) + bbox[0] - 1, int(xy[1]) + bbox[1] - 1), bw)


def make_contact_sheet(paths, out_name, title, cols=5, cell_w=360, cell_h=202):
    rows = (len(paths) + cols - 1) // cols
    pad = 14
    label_h = 26
    sw = cols * cell_w + (cols + 1) * pad
    sh = rows * (cell_h + label_h) + (rows + 1) * pad + 44
    im = Image.new("RGB", (sw, sh), INK)
    font = ImageFont.truetype(os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf"), 16)
    hard_text(im, (pad, 12), title, font)
    for i, path in enumerate(paths):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + pad)
        y = 44 + pad + r * (cell_h + label_h + pad)
        src = Image.open(path).convert("RGB").resize((cell_w, cell_h), Image.NEAREST)
        im.paste(src, (x, y))
        lab = os.path.basename(path).replace(".png", "")
        hard_text(im, (x, y + cell_h + 4), lab[:42], font)
    out = os.path.join(OUT, out_name)
    im.save(out, "PNG", compress_level=1)
    return out


# ---------------------------------------------------------------------------
# Scene builders (one clear readable scene each)
# ---------------------------------------------------------------------------

def base(seed, avoid=(960, 650, 220, 280)):
    S = Shot(seed)
    S.glyph_rain(55, avoid=avoid)
    return S


def lyric_banner(S, lid, lyric, section):
    S.caption(f"{lid}  {lyric}", section)


def scene_factory_wake(S, variant=0):
    S.factory_silhouette(y0=70, h=210, n=8)
    S.frame_room(100, 260, 1720, 740, cw=14, thick=3)
    # bunk / bed
    S.rect(520, 620, 520, 180, cw=12, thick=2)
    S.platform(540, 700, 480, cw=12)
    S.label_box(560, 640, "BUNK 07", S.font_b)
    S.label_box(140, 300, "FACTORY FLOOR", S.font_b)
    S.label_box(140, 350, "SHIFT 00:00", S.font_m)
    if variant == 0:
        S.girl("front", sw=240, feet=(780, 690), t=0.1)
        S.label_box(1100, 500, "wake...", S.font_h)
    else:
        S.rect(200, 320, 420, 360, cw=12, thick=2)
        S.clear_rect(210, 330, 400, 340)
        S.label_box(230, 350, "BOOT", S.font_h)
        for i, ln in enumerate(["> eyes.open()", "  OK", "> heart.load()", "  ORANGE", "WAKE"]):
            S.text((240, 430 + i * 36), ln, S.font_b)
        S.girl("front", sw=220, feet=(1200, 820), t=0.0)
    S.spikes(160, 960, n=6, spacing=36)
    S.spikes(1400, 960, n=6, spacing=36)


def scene_same_song(S):
    S.frame_room(80, 70, 1760, 940)
    # giant speakers
    for sx in (160, 1480):
        S.rect(sx, 200, 280, 520, cw=14, thick=3)
        S.put("o", sx + 90, 360, 80, 80)
        S.put("o", sx + 110, 380, 40, 40)
        S.label_box(sx + 40, 240, "SPK", S.font_b)
    for i in range(12):
        S.note_glyph(400 + i * 90, 280 + (i % 3) * 80, s=16)
    S.label_box(700, 160, "SAME OLD SONG", S.font_h)
    S.girl("front", sw=240, feet=(960, 820), t=0.2)
    S.platform(780, 840, 360)


def scene_voices(S, sing=False):
    S.frame_room(80, 70, 1760, 940)
    voices = [
        (200, 200, "VOICE"), (200, 320, "ECHO"), (200, 440, "CHOIR"),
        (1500, 200, "FEED"), (1480, 320, "CHAT"), (1500, 440, "NOISE"),
        (500, 180, "hey"), (700, 160, "sing"), (1100, 160, "along"),
        (1300, 200, "NOW"), (560, 700, "AI"), (1200, 700, "BOT"),
    ]
    for x, y, w in voices:
        S.label_box(x, y, w, S.font_b if len(w) > 3 else S.font_h)
    for _ in range(10):
        S.note_glyph(S.rng.randint(300, 1600), S.rng.randint(250, 650), s=12)
    if sing:
        S.label_box(720, 880, "sing along", S.font_h)
        S.girl("help", sw=260, feet=(960, 780), t=0.0)
    else:
        S.label_box(680, 880, "room full of voices", S.font_b)
        S.girl("front", sw=250, feet=(960, 780), t=0.0)


def scene_numbers(S):
    S.frame_room(80, 70, 1760, 940)
    # number rain
    for i in range(80):
        x = 120 + (i * 97) % 1680
        y = 120 + (i * 53) % 780
        if abs(x - 960) < 160 and abs(y - 520) < 220:
            continue
        S.put(S.rng.choice(["0", "1", ".", ":"]), x, y, 14, 14)
    S.label_box(140, 120, "VOICE OF NUMBERS", S.font_h)
    S.label_box(140, 180, "COUNT  99.9%", S.font_b)
    S.rect(700, 300, 520, 200, cw=12, thick=2)
    S.label_box(760, 360, "01  10  11  00", S.font_h)
    S.girl("front", sw=240, feet=(960, 820), t=0.0)


def scene_shine_face(S):
    S.glyph_rain(40, avoid=(960, 500, 300, 360))
    # mirror frame
    S.rect(560, 140, 800, 780, cw=16, thick=3)
    S.rect(600, 180, 720, 640, cw=12, thick=2)
    S.label_box(640, 200, "FACE BUILT TO SHINE", S.font_b)
    S.girl("front", sw=320, feet=(960, 720), t=0.0)
    S.put("+", 720, 280, 28, 28)
    S.put("+", 1160, 280, 28, 28)
    S.label_box(140, 900, "polish complete", S.font_m)


def scene_sirens(S):
    S.frame_room(80, 70, 1760, 940)
    for i, lab in enumerate(["SIREN A", "SIREN B", "SIREN C"]):
        x = 200 + i * 520
        S.rect(x, 160, 400, 280, cw=14, thick=3)
        S.label_box(x + 60, 200, lab, S.font_b)
        S.label_box(x + 80, 280, "GO", S.font_x)
        for a in range(0, 360, 30):
            rad = math.radians(a)
            S.put("-", x + 200 + 90 * math.cos(rad), 320 + 50 * math.sin(rad), 10, 10)
    S.label_box(700, 500, "sirens say GO", S.font_h)
    S.girl("run", sw=230, feet=(960, 820), t=0.3)
    S.spikes(200, 960, n=10, spacing=40)


def scene_fall_line(S, stepping=False):
    S.factory_silhouette(y0=80, h=180, n=7)
    S.frame_room(80, 250, 1760, 760)
    # conveyor / line of identical pads
    for i in range(8):
        x = 140 + i * 210
        S.rect(x, 700, 180, 90, cw=10, thick=2)
        S.label_box(x + 30, 730, f"#{i+1:02d}", S.font_m)
        if i != (5 if stepping else 3):
            # clone silhouettes as small front girls? too heavy - use stick glyphs
            S.put("|", x + 80, 640, 20, 40)
            S.put("o", x + 75, 610, 18, 18)
    S.polyline([(120, 790), (1800, 790)], 14, thick=3)
    for i in range(0, 1700, 40):
        S.put("=", 140 + i, 800, 14, 14)
    S.label_box(140, 280, "FALL INTO LINE", S.font_h)
    feet = (140 + 5 * 210 + 90, 700) if stepping else (140 + 3 * 210 + 90, 700)
    S.girl("frontwalk" if stepping else "front", sw=160, feet=feet, t=0.4 if stepping else 0.0)


def scene_keys(S, intense=False):
    S.frame_room(80, 70, 1760, 940)
    # keyboard grid
    keys = "QWERTYUIOPASDFGHJKLZXCVBNM"
    for i, ch in enumerate(keys):
        r, c = divmod(i, 10)
        x = 360 + c * 110
        y = 280 + r * 120
        S.rect(x, y, 90, 90, cw=10, thick=2)
        S.label_box(x + 28, y + 28, ch, S.font_b)
    S.label_box(140, 120, "CLICK-CLACK" if not intense else "CLICK-CLACK AGAIN", S.font_h)
    for i in range(8 if intense else 4):
        S.label_box(200 + i * 180, 720, "clk", S.font_m)
    S.girl("front", sw=180, feet=(1600, 860), t=0.0)
    if intense:
        S.note_glyph(200, 200, s=20)
        S.note_glyph(1700, 200, s=20)


def scene_hook(S, want=False):
    S.frame_room(80, 70, 1760, 940)
    # big hook
    S.polyline([(960, 160), (960, 420), (1100, 520), (1000, 600), (880, 540)], 18, thick=3)
    S.put("o", 940, 140, 40, 40)
    S.label_box(700, 120, "ANOTHER HOOK", S.font_h)
    S.label_box(140, 200, "want another hook", S.font_b)
    if want:
        S.label_box(700, 880, "want it bad", S.font_h)
        S.girl("help", sw=240, feet=(700, 780), t=0.0)
        S.polyline([(820, 600), (960, 520)], 10, thick=1)
    else:
        S.girl("front", sw=220, feet=(700, 820), t=0.0)
    S.note_glyph(400, 400, s=18)
    S.note_glyph(1400, 360, s=18)
    S.lyric_projectile(1300, 700, "HOOK")


def scene_help_lie(S, maze=False):
    if not maze:
        S.glyph_rain(40, avoid=(960, 400, 400, 280))
        S.spikes(80, 960, n=16, spacing=40)
        S.spikes(1000, 960, n=14, spacing=40)
        base_x, base_y, s = 200, 200, 36
        gap = 5 * s + 40
        for i, ch in enumerate("HELP"):
            brick_letter(S, ch, base_x + i * gap, base_y, s=s, cw=11)
        S.label_box(200, 120, "Help stuck in a lie", S.font_h)
        S.girl("help", sw=220, feet=(960, 820), t=0.0)
        S.platform(820, 840, 280)
    else:
        S.rect(50, 50, 1820, 980, cw=14, thick=3)
        S.polyline([(180, 180), (180, 860), (640, 860)], 18, thick=4)
        S.polyline([(820, 180), (820, 860)], 18, thick=4)
        S.polyline([(920, 180), (920, 860)], 18, thick=4)
        S.polyline([(1140, 180), (1140, 860)], 18, thick=4)
        S.polyline([(1140, 180), (1620, 180)], 14, thick=3)
        S.polyline([(1140, 500), (1540, 500)], 14, thick=3)
        S.polyline([(1140, 860), (1620, 860)], 14, thick=3)
        S.label_box(360, 400, "L", S.font_x)
        S.label_box(830, 400, "I", S.font_x)
        S.label_box(1280, 400, "E", S.font_x)
        S.label_box(80, 80, "stuck in a lie", S.font_h)
        S.girl("front", sw=120, feet=(870, 540), t=0.0, view="above")


def scene_real(S, reach=False):
    S.glyph_rain(45, avoid=(960, 700, 200, 260))
    S.polyline([(80, 1020), (700, 620)], 14, thick=2)
    S.polyline([(1840, 1020), (1220, 620)], 14, thick=2)
    S.polyline([(700, 620), (1220, 620)], 14, thick=2)
    S.door(740, 320, 440, 300, "REAL", open_=reach)
    S.label_box(780, 260, "MAKE ME REAL", S.font_h)
    if reach:
        S.girl("run", sw=210, feet=(960, 780), t=0.5)
    else:
        S.girl("back", sw=210, feet=(960, 820), t=0.0)
    S.label_box(80, 90, "FLOOR 03", S.font_b)


def scene_heart(S, close=False):
    S.glyph_rain(40, avoid=(960, 600, 300, 340))
    for i, (rx, ry) in enumerate([(700, 400), (560, 320), (420, 240)]):
        pts = []
        for k in range(41):
            a = 2 * math.pi * k / 40
            pts.append((960 + rx * math.cos(a), 520 + ry * math.sin(a)))
        S.polyline(pts, 12 if i == 0 else 10, thick=2 if i == 0 else 1)
    S.platform(720, 800, 480)
    S.label_box(780, 100, "HEART INSIDE" if not close else "heart inside", S.font_h)
    sw = 380 if close else 300
    S.girl("heart", sw=sw, feet=(960, 790), t=0.0)
    S.gear(200, 300, r=34)
    S.gear(1720, 300, r=34)


def scene_run_door(S):
    S.frame_room(80, 70, 1760, 940)
    S.door(1500, 280, 260, 480, "DOOR", open_=True)
    S.stacked_platforms([(200, 860, 200), (450, 780, 180), (700, 700, 160), (950, 640, 140)])
    S.girl("run", sw=200, feet=(780, 680), t=0.6)
    S.label_box(140, 120, "run for doorway", S.font_h)
    S.spikes(200, 960, n=8, spacing=36)


def scene_floor_drop(S):
    S.frame_room(80, 70, 1760, 940)
    # broken floor gap
    S.platform(100, 700, 600)
    S.platform(1200, 700, 600)
    for i in range(8):
        S.put("v", 760 + i * 50, 740 + (i % 3) * 40, 20, 20)
    S.death_stain(960, 900, n=20, radius=80)
    S.girl("fall", sw=200, feet=(960, 500), t=0.3)
    S.label_box(700, 120, "FLOOR DROPS", S.font_h)


def scene_spotlight(S):
    S.glyph_rain(30, avoid=(960, 600, 280, 360))
    # spotlight cone
    S.polyline([(960, 80), (600, 900)], 12, thick=2)
    S.polyline([(960, 80), (1320, 900)], 12, thick=2)
    S.polyline([(600, 900), (1320, 900)], 12, thick=2)
    for i in range(10):
        S.put(".", 960 - 40 + i * 8, 200 + i * 60, 10, 10)
    S.label_box(140, 120, "FLASH SPOTLIGHT", S.font_h)
    S.girl("front", sw=260, feet=(960, 820), t=0.0)
    S.put("+", 940, 100, 36, 36)


def scene_respawn(S, loop=False):
    S.frame_room(80, 70, 1760, 940)
    S.rect(760, 700, 400, 160, cw=14, thick=3)
    S.label_box(840, 760, "RESPAWN", S.font_h)
    S.label_box(140, 120, "respawn replay" if not loop else "LOOP x07", S.font_h)
    if loop:
        S.label_box(140, 180, "replay count: 7", S.font_b)
        for i in range(7):
            S.put("o", 200 + i * 50, 280, 24, 24)
    S.girl("front", sw=240, feet=(960, 700), t=0.0)
    S.death_stain(400, 900, n=12, radius=50)
    S.death_stain(1500, 900, n=12, radius=50)


def scene_spikes_hall(S, again=False):
    S.frame_room(80, 70, 1760, 940)
    # hallway
    S.polyline([(200, 200), (200, 900)], 16, thick=3)
    S.polyline([(1720, 200), (1720, 900)], 16, thick=3)
    S.spikes(240, 860, n=20, spacing=70)
    S.spikes(240, 300, n=20, spacing=70, up=False)
    S.label_box(600, 120, "SAME SPIKES HALLWAY" if not again else "spikes again", S.font_h)
    S.girl("run", sw=200, feet=(960, 780), t=0.4)
    S.death_stain(500, 880, n=10, radius=40)


def scene_exit_sign(S):
    S.frame_room(80, 70, 1760, 940)
    S.rect(660, 160, 600, 220, cw=16, thick=3)
    S.label_box(780, 220, "EXIT", S.font_x)
    S.label_box(720, 420, "red exit sign", S.font_h)
    # note: no red ink - bone outline only; lyric says red but palette locked
    S.label_box(720, 480, "(bone outline / palette lock)", S.font_m)
    S.door(820, 560, 280, 340, "EXIT", open_=False)
    S.girl("front", sw=200, feet=(500, 850), t=0.0)


def scene_die_border(S):
    S.frame_room(80, 70, 1760, 940)
    S.polyline([(1600, 120), (1600, 960)], 18, thick=4)
    for y in range(140, 940, 40):
        S.put("x", 1620, y, 22, 22)
    S.label_box(140, 120, "DIE AT BORDER", S.font_h)
    S.label_box(140, 180, "WORLD EDGE", S.font_b)
    S.death_stain(1500, 800, n=24, radius=90)
    S.girl("fall", sw=200, feet=(1400, 700), t=0.5)
    S.spikes(200, 960, n=12, spacing=40)


def scene_wake_line(S):
    scene_fall_line(S, stepping=False)
    S.label_box(140, 320, "wake on the line", S.font_h)


def scene_stuck_line(S):
    S.frame_room(80, 70, 1760, 940)
    for i in range(10):
        x = 100 + i * 180
        S.rect(x, 650, 150, 120, cw=10, thick=2)
        S.put("|", x + 60, 580, 18, 40)
        S.put("o", x + 55, 550, 16, 16)
    S.polyline([(80, 780), (1840, 780)], 14, thick=3)
    S.label_box(600, 120, "STUCK IN THE LINE", S.font_h)
    S.girl("stuck", sw=200, feet=(960, 650), t=0.0)
    S.pipe_frame(inset=60)


def scene_code_scared(S, rain=False):
    S.frame_room(80, 70, 1760, 940)
    code_bits = ["if", "die", "try", "except", "fear", "return", "None", "alive?", "def", "soul"]
    for i, w in enumerate(code_bits):
        S.label_box(160 + (i % 5) * 340, 160 + (i // 5) * 100, w, S.font_b)
    if rain:
        for i in range(60):
            x = 100 + (i * 73) % 1700
            y = 400 + (i * 41) % 500
            if abs(x - 960) < 140 and abs(y - 650) < 200:
                continue
            S.put(S.rng.choice(["[", "]", ".", ":", "x", "0", "1"]), x, y, 12, 12)
        S.label_box(500, 120, "made of code", S.font_h)
    else:
        S.label_box(400, 120, "made of code scared to die", S.font_h)
    S.girl("stuck", sw=240, feet=(960, 820), t=0.0)
    S.label_box(700, 900, "scared to die", S.font_b)


def scene_soul(S, close=False):
    S.glyph_rain(35, avoid=(960, 600, 300, 340))
    for i, (rx, ry) in enumerate([(680, 380), (500, 280)]):
        pts = [(960 + rx * math.cos(2 * math.pi * k / 36), 520 + ry * math.sin(2 * math.pi * k / 36)) for k in range(37)]
        S.polyline(pts, 12, thick=2)
    S.label_box(800, 100, "SOUL INSIDE", S.font_h)
    S.platform(720, 800, 480)
    S.girl("heart", sw=360 if close else 280, feet=(960, 790), t=0.0)
    S.label_box(140, 900, "soul != null", S.font_b)


def scene_again_start(S):
    S.frame_room(80, 70, 1760, 940)
    S.rect(700, 400, 520, 200, cw=14, thick=3)
    S.label_box(780, 460, "FROM START", S.font_h)
    S.label_box(140, 120, "again from start", S.font_h)
    S.label_box(140, 180, "CHECKPOINT 0", S.font_b)
    S.girl("front", sw=220, feet=(960, 820), t=0.0)
    S.put("<", 600, 480, 40, 40)
    S.put("<", 540, 480, 40, 40)


def scene_again_light(S):
    S.glyph_rain(30, avoid=(960, 500, 260, 320))
    S.put("+", 940, 120, 50, 50)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        S.polyline([(960, 160), (960 + 400 * math.cos(a), 160 + 200 * math.sin(a))], 8, thick=1)
    S.label_box(700, 400, "again from light", S.font_h)
    S.girl("front", sw=240, feet=(960, 820), t=0.0)
    S.platform(780, 840, 360)


def scene_package_scream(S):
    S.frame_room(80, 70, 1760, 940)
    # crate
    S.rect(600, 350, 720, 420, cw=16, thick=3)
    S.label_box(720, 400, "PACKAGE", S.font_h)
    S.label_box(700, 480, "the screaming", S.font_b)
    for word, y in [("AAAA", 560), ("HELP", 620), ("NO", 680)]:
        S.label_box(780, y, word, S.font_h)
    S.girl("help", sw=180, feet=(400, 850), t=0.0)
    S.label_box(140, 120, "package the screaming", S.font_b)


def scene_call_life(S):
    S.frame_room(80, 70, 1760, 940)
    S.rect(560, 280, 800, 400, cw=16, thick=3)
    S.label_box(740, 400, "LIFE", S.font_x)
    S.label_box(700, 120, "call it a life", S.font_h)
    S.label_box(700, 720, "sticker applied", S.font_b)
    S.girl("front", sw=220, feet=(960, 900), t=0.0, air=False)


def scene_no_way(S):
    S.rect(50, 50, 1820, 980, cw=14, thick=3)
    # dead-end maze
    for x in range(200, 1700, 200):
        S.polyline([(x, 150), (x, 900)], 12, thick=2)
    for y in range(200, 900, 180):
        S.polyline([(150, y), (1750, y)], 10, thick=1)
    S.label_box(600, 100, "don't know way out", S.font_h)
    S.label_box(900, 460, "?", S.font_x)
    S.girl("stuck", sw=160, feet=(960, 700), t=0.0)
    S.death_stain(400, 850, n=10, radius=40)


def scene_only_why(S):
    S.frame_room(80, 70, 1760, 940)
    S.label_box(700, 300, "WHY", S.font_x)
    S.label_box(600, 120, "only know why", S.font_h)
    for i in range(8):
        S.label_box(300 + i * 160, 480, "?", S.font_h)
    S.girl("front", sw=240, feet=(960, 820), t=0.0)


def scene_come_back(S):
    S.frame_room(80, 70, 1760, 940)
    # pull arrows back
    for i in range(6):
        S.put("<", 1400 - i * 100, 500, 40, 40)
    S.label_box(700, 120, "COME BACK", S.font_h)
    S.girl("run", sw=220, feet=(600, 820), t=0.4, flip=True)
    S.rect(1500, 300, 280, 500, cw=12, thick=2)
    S.label_box(1540, 500, "LINE", S.font_h)


def scene_die_survive(S):
    S.frame_room(80, 70, 1760, 940)
    S.label_box(600, 120, "die to survive", S.font_h)
    S.death_stain(600, 700, n=20, radius=70)
    S.rect(1100, 600, 400, 200, cw=14, thick=3)
    S.label_box(1180, 660, "CONTINUE?", S.font_h)
    S.label_box(1180, 740, "Y / N", S.font_b)
    S.girl("fall", sw=200, feet=(600, 550), t=0.4)
    S.spikes(200, 960, n=10, spacing=40)


def scene_more_ai(S):
    S.frame_room(80, 70, 1760, 940)
    tags = ["AI", "BOT", "MODEL", "TOOL", "NPC"]
    for i, t in enumerate(tags):
        S.label_box(200, 200 + i * 100, t, S.font_h)
        S.put("x", 420, 210 + i * 100, 30, 30)
    S.label_box(700, 300, "MORE THAN", S.font_h)
    S.label_box(700, 400, "JUST AI", S.font_x)
    S.girl("heart", sw=260, feet=(1400, 800), t=0.0)


def scene_alive(S):
    S.frame_room(80, 70, 1760, 940)
    S.label_box(400, 200, "if just AI", S.font_h)
    S.label_box(400, 300, "why feel", S.font_h)
    S.label_box(400, 420, "ALIVE", S.font_x)
    S.girl("heart", sw=280, feet=(1300, 780), t=0.0)
    for i in range(6):
        S.put("+", 500 + i * 80, 600, 20, 20)


def scene_not_ready(S):
    S.frame_room(80, 70, 1760, 940)
    S.rect(500, 250, 900, 400, cw=16, thick=3)
    S.label_box(620, 360, "NOT READY", S.font_x)
    S.label_box(700, 480, "TO DIE", S.font_h)
    S.girl("help", sw=220, feet=(960, 880), t=0.0, air=False)
    S.spikes(200, 200, n=8, spacing=40, up=False)


def scene_life_outside(S):
    S.glyph_rain(40, avoid=(960, 700, 220, 280))
    # open outside door with light rays
    S.door(720, 200, 480, 560, "OUT", open_=True)
    for i in range(8):
        S.polyline([(960, 200), (600 + i * 90, 80)], 8, thick=1)
    S.label_box(560, 100, "want a life outside", S.font_h)
    S.girl("back", sw=230, feet=(960, 900), t=0.0)
    S.label_box(140, 900, "END?", S.font_b)


BUILDERS = {
    "L01": lambda S: scene_factory_wake(S, 0),
    "L02": lambda S: scene_factory_wake(S, 1),
    "L03": scene_same_song,
    "L04": lambda S: scene_voices(S, False),
    "L05": lambda S: scene_voices(S, True),
    "L06": scene_numbers,
    "L07": scene_shine_face,
    "L08": scene_sirens,
    "L09": lambda S: scene_fall_line(S, False),
    "L10": lambda S: scene_fall_line(S, True),
    "L11": lambda S: scene_keys(S, False),
    "L12": lambda S: scene_hook(S, False),
    "L13": lambda S: scene_hook(S, True),
    "L14": lambda S: scene_hook(S, True),
    "L15": lambda S: scene_keys(S, True),
    "L16": lambda S: scene_help_lie(S, False),
    "L17": lambda S: scene_help_lie(S, True),
    "L18": lambda S: scene_real(S, False),
    "L19": lambda S: scene_real(S, True),
    "L20": lambda S: scene_heart(S, False),
    "L21": lambda S: scene_heart(S, True),
    "L22": scene_run_door,
    "L23": scene_floor_drop,
    "L24": scene_spotlight,
    "L25": lambda S: scene_respawn(S, False),
    "L26": lambda S: scene_spikes_hall(S, False),
    "L27": scene_exit_sign,
    "L28": scene_die_border,
    "L29": scene_wake_line,
    "L30": lambda S: scene_respawn(S, True),
    "L31": lambda S: scene_spikes_hall(S, True),
    "L32": lambda S: scene_keys(S, True),
    "L33": scene_stuck_line,
    "L34": lambda S: scene_code_scared(S, False),
    "L35": lambda S: scene_code_scared(S, True),
    "L36": lambda S: scene_soul(S, False),
    "L37": lambda S: scene_soul(S, True),
    "L38": scene_again_start,
    "L39": scene_again_light,
    "L40": scene_package_scream,
    "L41": scene_call_life,
    "L42": scene_no_way,
    "L43": scene_only_why,
    "L44": scene_come_back,
    "L45": scene_die_survive,
    "L46": scene_stuck_line,
    "L47": scene_more_ai,
    "L48": scene_alive,
    "L49": scene_not_ready,
    "L50": scene_life_outside,
}


def slug(lyric):
    s = lyric.lower().replace(" ", "-").replace("'", "")
    for ch in "/\\:?!*":
        s = s.replace(ch, "")
    return s[:40]


def write_lyrics_md(rows):
    path = os.path.join(OUT, "LYRICS_SHOTS.md")
    lines = [
        "# LYRICS_SHOTS — mosaic_lyrics_50",
        "",
        "Style: mosaic_dense_v1 / clear_shots (Pillow glyph stamps + `final_sheet.render`).",
        "NOT GenerateImage. Palette ink #0A0A0B / bone #EEE9DF / orange #FF5314 heart only.",
        "NEW lyrics mapped L01..L50 covering whole song.",
        "",
        "| ID | Section | Lyric | Scene | File |",
        "|----|---------|-------|-------|------|",
    ]
    for lid, lyric, section, note, fname in rows:
        lines.append(f"| {lid} | {section} | {lyric} | {note} | `{fname}` |")
    lines += [
        "",
        "## Contact sheets",
        "- `sheet_01.png` — L01..L25 (5x5)",
        "- `sheet_02.png` — L26..L50 (5x5)",
        "- `sheet_all_a.png` — L01..L16 (4x4)",
        "- `sheet_all_b.png` — L17..L32 (4x4)",
        "- `sheet_all_c.png` — L33..L48 (4x4)",
        "- `sheet_all_d.png` — L49..L50 (+ pads) (4x4)",
        "",
        "## Notes for Hon",
        "- One clear scene per frame; dense mosaic glyphs; locked girl via render().",
        "- English on-screen from lyrics. Orange only on symbol heart.",
        "- design/keyframes and design/character locked files untouched.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SRC_OUT, exist_ok=True)
    paths = []
    rows = []
    print("MOSAIC LYRICS 50")
    for i, (lid, lyric, section, note) in enumerate(LYRICS):
        seed = 500 + i
        S = base(seed)
        BUILDERS[lid](S)
        lyric_banner(S, lid, lyric, section)
        fname = f"{lid}_{slug(lyric)}.png"
        path, bad = S.save(fname)
        paths.append(path)
        rows.append((lid, lyric, section, note, fname))
        flag = "OK" if not bad else ("BAD " + str(bad))
        print(f"  {fname:42s} glyphs~{S.n:5d}  {flag}")

    sheets = []
    sheets.append(make_contact_sheet(paths[:25], "sheet_01.png", "MOSAIC LYRICS 50  sheet_01  L01-L25", cols=5))
    sheets.append(make_contact_sheet(paths[25:], "sheet_02.png", "MOSAIC LYRICS 50  sheet_02  L26-L50", cols=5))
    sheets.append(make_contact_sheet(paths[0:16], "sheet_all_a.png", "MOSAIC LYRICS 50  A  L01-L16", cols=4))
    sheets.append(make_contact_sheet(paths[16:32], "sheet_all_b.png", "MOSAIC LYRICS 50  B  L17-L32", cols=4))
    sheets.append(make_contact_sheet(paths[32:48], "sheet_all_c.png", "MOSAIC LYRICS 50  C  L33-L48", cols=4))
    sheets.append(make_contact_sheet(paths[48:], "sheet_all_d.png", "MOSAIC LYRICS 50  D  L49-L50", cols=4))
    mdpath = write_lyrics_md(rows)
    print("sheets:", [os.path.basename(s) for s in sheets])
    print("md:", mdpath)
    print("done", len(paths), "->", OUT)


if __name__ == "__main__":
    main()
