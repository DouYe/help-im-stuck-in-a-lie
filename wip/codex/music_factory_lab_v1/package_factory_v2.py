"""Preserve v1 and make a separate four-frame review pack with perspective variation."""

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
ORIGINAL = PROJECT / "design/keyframes/codex_music_factory_lab_v1"
VARIANT = PROJECT / "wip/codex/music_factory_lab_v1/perspective_variant"
DEST = PROJECT / "design/keyframes/codex_music_factory_lab_v2"
FRAMES = [
    ("F01", ORIGINAL / "F01_music_factory_identical_ai.png", "IDENTICAL AI / ONE HEART"),
    ("F02", ORIGINAL / "F02_return_to_line_zero.png", "DEATH / RETURN TO START"),
    ("F03", ORIGINAL / "F03_trumpet_lyric_attack.png", "BRASS ENEMY / LYRICS"),
    ("F04", VARIANT / "F04_perspective_escape_corridor.png", "3D CODE CORRIDOR / EXIT"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if DEST.exists():
        raise FileExistsError(f"Versioned destination already exists: {DEST}")
    for _, source, _ in FRAMES:
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as image:
            if image.size != (1920, 1080):
                raise ValueError(f"Not 1920x1080: {source}")
    DEST.mkdir(parents=True)
    entries = []
    for ident, source, title in FRAMES:
        target = DEST / (ident + "_" + source.name.split("_", 1)[1])
        shutil.copy2(source, target)
        if sha(source) != sha(target):
            raise IOError(f"Hash mismatch: {source}")
        entries.append({"id": ident, "file": target.name, "title": title, "sha256": sha(target)})

    bg, cell, bone, grey, orange = "#0A0A0B", "#161618", "#EEE9DF", "#9C978F", "#FF5314"
    width, height = 1904, 1260
    sheet = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(sheet)
    font = Path("C:/Windows/Fonts/consola.ttf")
    bold = Path("C:/Windows/Fonts/consolab.ttf")
    header_font = ImageFont.truetype(str(bold), 28)
    caption_font = ImageFont.truetype(str(bold), 23)
    foot_font = ImageFont.truetype(str(font), 18)
    draw.text((42, 23), "AI FACTORY / ESCAPE / RESET     FOUR STATIC PROPOSALS", fill=bone, font=header_font)
    draw.text((42, 1228), "v2 adds one depth-view study. v1 and all earlier images remain untouched; no animation.",
              fill=grey, font=foot_font)
    for i, (ident, _, title) in enumerate(FRAMES):
        col, row = i % 2, i // 2
        x, y = 42 + col * 930, 85 + row * 574
        draw.rectangle((x, y, x + 887, y + 550), fill=cell)
        draw.text((x + 15, y + 10), ident, fill=orange, font=caption_font)
        draw.text((x + 82, y + 11), title, fill=bone, font=caption_font)
        with Image.open(DEST / entries[i]["file"]) as image:
            thumb = image.convert("RGB").resize((888, 500), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y + 43))
    sheet.save(DEST / "factory_story_review_sheet_v2.png", optimize=True)
    (DEST / "manifest.json").write_text(
        json.dumps({"status": "new static proposals awaiting Hon review", "frames": entries}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Packaged {len(entries)} source-matched stills in {DEST}")


if __name__ == "__main__":
    main()
