"""Mirror the shared four-frame proposal pack to this task's outputs without replacing old files."""

import hashlib
import shutil
import zipfile
from pathlib import Path

from PIL import Image


source = Path(r"D:\Videos\Help! I'm stuck in a LIE\design\keyframes\codex_music_factory_lab_v2")
outputs = Path(r"C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs")
destination = outputs / "help_stuck_lie_ai_factory_story_v2"
archive = outputs / "help_stuck_lie_ai_factory_story_v2.zip"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not source.is_dir():
        raise FileNotFoundError(source)
    if destination.exists() or archive.exists():
        raise FileExistsError("v2 output already exists; preserving delivered files")
    pngs = sorted(source.glob("F??_*.png"))
    if len(pngs) != 4:
        raise ValueError(f"Expected four full-size frames, found {len(pngs)}")
    for png in pngs:
        with Image.open(png) as im:
            if im.size != (1920, 1080):
                raise ValueError(f"Unexpected dimensions: {png} {im.size}")
    outputs.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    originals = sorted(p for p in source.iterdir() if p.is_file())
    for original in originals:
        if digest(original) != digest(destination / original.name):
            raise IOError(f"Copy checksum differs: {original.name}")
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file in sorted(destination.iterdir()):
            if file.is_file():
                zf.write(file, file.name)
    with zipfile.ZipFile(archive) as zf:
        if len(zf.namelist()) != len(originals) or zf.testzip() is not None:
            raise IOError("ZIP verification failed")
    print(f"Copied {len(originals)} files; {len(pngs)} frames, 1920x1080 each")
    print(f"Output: {destination}")
    print(f"Archive: {archive} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
