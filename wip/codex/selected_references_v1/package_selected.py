"""Copy Hon's selected Codex stills and build a selected-only review sheet."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
SOURCE = PROJECT / "design/keyframes/codex_game_worlds_v2"
DEST = PROJECT / "design/keyframes/codex_selected_references_v1"
FRAMES = [
    ("02", "02_tactical_false_routes_46_858.png", "TACTICAL / FALSE ROUTES"),
    ("03", "03_KF09_make-me-real_code-diorama.png", "CODE DIORAMA / DEPTH"),
    ("04", "04_KF10_real_this_time_syntax_lock.png", "SYNTAX LOCK / BOSS"),
    ("05", "05_KF11_HELP_code_bullet_hell.png", "CODE BULLET HELL"),
    ("06", "06_KF_55p15_stuck_paper_gravity_ASCII.png", "PAPER GRAVITY / ASCII"),
    ("07B", "07B_KF12_HEART_ascii_chamber.png", "ASCII HEART CHAMBER"),
    ("08", "08_KF13_heart_inside_ascii_vault.png", "MEMORY VAULT / CLOSE VIEW"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "consolab.ttf" if bold else "consola.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    entries = []
    for ident, name, title in FRAMES:
        src = SOURCE / name
        dst = DEST / name
        if not src.is_file():
            raise FileNotFoundError(src)
        if dst.exists():
            raise FileExistsError(f"Refusing to overwrite a selected reference: {dst}")
        with Image.open(src) as im:
            if im.size != (1920, 1080):
                raise ValueError(f"Expected 1920x1080 for {src}: {im.size}")
        shutil.copy2(src, dst)
        digest = sha256(src)
        if sha256(dst) != digest:
            raise IOError(f"Copy hash mismatch: {name}")
        entries.append({"id": ident, "file": name, "title": title, "sha256": digest})

    background = "#0A0A0B"
    cell = "#161618"
    bone = "#EEE9DF"
    grey = "#9C978F"
    orange = "#FF5314"
    margin, gap, thumb_w = 30, 20, 900
    thumb_h, header_h = 506, 57
    card_h = thumb_h + header_h
    width = margin * 2 + thumb_w * 2 + gap
    height = margin * 2 + card_h * 4 + gap * 3
    sheet = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(sheet)
    label_font = font(24, bold=True)
    id_font = font(28, bold=True)
    info_font = font(25)
    small_font = font(19)

    for index, (ident, name, title) in enumerate(FRAMES):
        col, row = index % 2, index // 2
        x = margin + col * (thumb_w + gap)
        y = margin + row * (card_h + gap)
        draw.rectangle((x, y, x + thumb_w - 1, y + card_h - 1), fill=cell)
        draw.text((x + 20, y + 12), ident, fill=orange, font=id_font)
        draw.text((x + 90, y + 14), title, fill=bone, font=label_font)
        with Image.open(DEST / name) as source_image:
            thumb = source_image.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y + header_h))

    x = margin + thumb_w + gap
    y = margin + 3 * (card_h + gap)
    draw.rectangle((x, y, x + thumb_w - 1, y + card_h - 1), fill=cell)
    lines = [
        ("SELECTED REFERENCES", bone, label_font),
        ("7 stills / for cross-model review", grey, info_font),
        ("01  REJECTED: not a code world", orange, info_font),
        ("07  REJECTED: too realistic", orange, info_font),
        ("07B is the selected code version", bone, info_font),
        ("Still images only; animation later.", grey, small_font),
    ]
    for line_index, (label, color, line_font) in enumerate(lines):
        draw.text((x + 28, y + 40 + line_index * 67), label, fill=color, font=line_font)

    sheet.save(DEST / "selected_references_sheet.png", optimize=True)
    (DEST / "selected_manifest.json").write_text(
        json.dumps({"status": "selected visual references, not final animated shots", "frames": entries}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"Copied {len(entries)} verified 1920x1080 stills to {DEST}")
    print(f"Sheet: {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
