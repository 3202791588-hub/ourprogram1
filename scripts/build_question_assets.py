#!/usr/bin/env python3
"""Build compact mini-program question images from the approved PNG masters."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = PROJECT_ROOT / "miniapp" / "assets" / "questions"
MANIFEST_PATH = ASSET_ROOT / "manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    sequences = [scene["sequence"] for scene in scenes]
    if sequences != list(range(1, 25)):
        raise ValueError("Question asset manifest must contain Q01-Q24 in order")

    width = int(manifest["width"])
    quality = int(manifest["quality"])
    runtime_format = manifest.get("runtimeFormat", "JPEG").upper()
    if runtime_format != "JPEG":
        raise ValueError("Mini-program runtime images must use JPEG for true-device compatibility")
    total_bytes = 0

    for scene in scenes:
        source = ASSET_ROOT / scene["sourceFile"]
        target = ASSET_ROOT / scene["sceneAsset"].removeprefix("/assets/questions/")
        if not source.is_file():
            raise FileNotFoundError(source)

        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            height = round(image.height * width / image.width)
            published = image.convert("RGB").resize(
                (width, height), Image.Resampling.LANCZOS
            )
            published.save(
                target,
                "JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )

        total_bytes += target.stat().st_size
        print(f"Q{scene['sequence']:02d} {source.name} -> {target.name} ({target.stat().st_size} bytes)")

    print(f"Built {len(scenes)} images: {total_bytes} bytes ({total_bytes / 1048576:.2f} MiB)")


if __name__ == "__main__":
    main()
