"""Light visual-delivery checks for the three static frames."""

import hashlib
from pathlib import Path

from PIL import Image


PROJECT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
DELIVERY = PROJECT / "design/keyframes/codex_music_factory_lab_v1"
FRAMES = sorted(p for p in DELIVERY.glob("*.png") if p.name.startswith(("F01_", "F02_", "F03_")))
assert len(FRAMES) == 3, FRAMES
for path in FRAMES:
    with Image.open(path) as original:
        image = original.convert("RGB")
        assert image.size == (1920, 1080), (path, image.size)
        colored = []
        for i, (red, green, blue) in enumerate(image.getdata()):
            if red > 125 and red > green * 1.35 and red > blue * 1.25:
                colored.append((i % 1920, i // 1920))
        assert colored, f"No orange heart found: {path}"
        bounds = (
            min(x for x, _ in colored), min(y for _, y in colored),
            max(x for x, _ in colored), max(y for _, y in colored),
        )
        # A warm-colored leak outside the heroine's small heart would violate the palette.
        assert bounds[2] - bounds[0] < 90 and bounds[3] - bounds[1] < 90, (path, bounds)
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        print(path.name, image.size, f"orange={len(colored)}", bounds, checksum)
