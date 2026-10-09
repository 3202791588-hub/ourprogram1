#!/usr/bin/env python3
"""Build the compact mini-program homepage image from its PNG master."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "docs" / "assets" / "home" / "home-tree-gateway-v1.png"
TARGET = PROJECT_ROOT / "miniapp" / "assets" / "home" / "tree-gateway.jpg"
WIDTH = 768
QUALITY = 78


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as image:
        height = round(image.height * WIDTH / image.width)
        published = image.convert("RGB").resize(
            (WIDTH, height), Image.Resampling.LANCZOS
        )
        published.save(
            TARGET,
            "JPEG",
            quality=QUALITY,
            optimize=True,
            progressive=True,
            subsampling=2,
        )

    size = TARGET.stat().st_size
    print(f"Homepage {SOURCE.name} -> {TARGET.name} ({WIDTH}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
