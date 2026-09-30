"""Package three new, unapproved static AI-factory story proposals."""

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
WIP = PROJECT / "wip/codex/music_factory_lab_v1"
DEST = PROJECT / "design/keyframes/codex_music_factory_lab_v1"
FRAMES = [
    ("F01", "factory_line_identical_ai_v1.png", "F01_music_factory_identical_ai.png", "IDENTICAL AI / ONE HEART"),
    ("F02", "respawn_line_zero_v1.png", "F02_return_to_line_zero.png", "DEATH / RETURN TO START"),
    ("F03", "brass_press_lyric_attack_v1.png", "F03_trumpet_lyric_attack.png", "BRASS ENEMY / LYRIC HAZARD"),
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = []
    for ident, source_name, output_name, title in FRAMES:
        source = WIP / source_name
        output = DEST / output_name
        if not source.is_file() or output.exists():
            raise RuntimeError(f"Missing source or existing delivery: {source} / {output}")
        with Image.open(source) as image:
            if image.size != (1920, 1080):
                raise ValueError(f"Wrong size: {source}: {image.size}")
        shutil.copy2(source, output)
        digest = sha256(source)
        if sha256(output) != digest:
            raise IOError(f"Copy mismatch: {output_name}")
        manifest.append({"id": ident, "file": output_name, "title": title, "sha256": digest})

    ink, cell, bone, grey, orange = "#0A0A0B", "#161618", "#EEE9DF", "#9C978F", "#FF5314"
    width, height = 1810, 521
    sheet = Image.new("RGB", (width, height), ink)
    draw = ImageDraw.Draw(sheet)
    font = Path("C:/Windows/Fonts/consola.ttf")
    bold = Path("C:/Windows/Fonts/consolab.ttf")
    title_font = ImageFont.truetype(str(bold), 26)
    caption_font = ImageFont.truetype(str(bold), 21)
    small_font = ImageFont.truetype(str(font), 17)
    draw.text((42, 24), "NEW STATIC STORY STUDIES / AI FACTORY", fill=bone, font=title_font)
    draw.text((1258, 31), "Codex proposal v1", fill=grey, font=small_font)
    for i, (ident, _, output_name, title) in enumerate(FRAMES):
        x = 40 + i * 590
        y = 91
        draw.rectangle((x, y, x + 559, y + 357), fill=cell)
        draw.text((x + 14, y + 11), ident, fill=orange, font=caption_font)
        draw.text((x + 78, y + 12), title, fill=bone, font=caption_font)
        with Image.open(DEST / output_name) as image:
            sheet.paste(image.convert("RGB").resize((560, 315), Image.Resampling.LANCZOS), (x, y + 43))
    draw.text((42, 480), "New candidates only. Earlier images retained. Animation and exact edit timing remain open.",
              fill=grey, font=small_font)
    sheet.save(DEST / "factory_story_review_sheet.png", optimize=True)
    (DEST / "manifest.json").write_text(
        json.dumps({"status": "new static proposals; no final shot approval", "frames": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Packaged {len(manifest)} verified stills into {DEST}")


if __name__ == "__main__":
    main()
