#!/usr/bin/env python3
"""Cross-check current backend content, mini-program manifest, and runtime images."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from apps.tests.content_v3 import QUESTION_V3  # noqa: E402


def main() -> None:
    asset_root = ROOT / "miniapp" / "assets" / "questions"
    runtime_manifest = (ROOT / "miniapp" / "services" / "scene-manifest.ts").read_text(
        encoding="utf-8"
    )
    runtime_wxml = (ROOT / "miniapp" / "pages" / "test-run" / "index.wxml").read_text(
        encoding="utf-8"
    )
    scenes_service = (ROOT / "miniapp" / "services" / "scenes.ts").read_text(encoding="utf-8")
    manifest = json.loads((asset_root / "manifest.json").read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    if len(QUESTION_V3) != 24 or len(scenes) != 24:
        raise ValueError("Backend content and scene manifest must both contain 24 questions")

    total_bytes = 0
    for sequence, (question, scene) in enumerate(zip(QUESTION_V3, scenes), 1):
        expected = f"/assets/questions/q{sequence:02d}/scene.jpg"
        if scene["sequence"] != sequence:
            raise ValueError(f"Manifest sequence mismatch at Q{sequence:02d}")
        if question["scene_key"] != scene["sceneKey"]:
            raise ValueError(f"Scene key mismatch at Q{sequence:02d}")
        api_asset_prefix = f"/assets/questions/q{sequence:02d}/scene."
        if not question["scene_asset"].startswith(api_asset_prefix):
            raise ValueError(f"Backend scene reference mismatch at Q{sequence:02d}")
        if scene["sceneAsset"] != expected:
            raise ValueError(f"Runtime scene asset mismatch at Q{sequence:02d}")
        if expected not in runtime_manifest:
            raise ValueError(f"Runtime TypeScript manifest mismatch at Q{sequence:02d}")
        if f'src="{expected}"' not in runtime_wxml:
            raise ValueError(f"Static packager reference missing at Q{sequence:02d}")
        if len(question["options"]) != 4:
            raise ValueError(f"Q{sequence:02d} must contain four options")
        runtime_asset = asset_root / f"q{sequence:02d}" / "scene.jpg"
        if not runtime_asset.is_file():
            raise FileNotFoundError(runtime_asset)
        total_bytes += runtime_asset.stat().st_size

    if 'require("../assets/questions/manifest.json")' in scenes_service:
        raise ValueError("WeChat runtime must not require the JSON asset manifest")

    modes = [question["response_mode"] for question in QUESTION_V3]
    if modes.count("behavior") != 12 or modes.count("need") != 12:
        raise ValueError("V3 must contain 12 behavior and 12 need questions")

    print(f"OK: 24 questions, 96 options, 12 behavior + 12 need, 24 scene mappings, {total_bytes} runtime bytes")


if __name__ == "__main__":
    main()
