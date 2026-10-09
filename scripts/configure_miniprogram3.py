#!/usr/bin/env python3
"""Preserve the WeChat project settings while excluding unused starter files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


IGNORES = [
    {"type": "folder", "value": "images"},
    {"type": "folder", "value": "components/cloudTipModal"},
    {"type": "folder", "value": "pages/example"},
    {"type": "folder", "value": "pages/index"},
    {"type": "file", "value": "envList.js"},
]

QUESTION_ASSET_INCLUDE = {"type": "folder", "value": "assets/questions"}
HOME_ASSET_INCLUDE = {"type": "folder", "value": "assets/home"}


def main() -> None:
    project_root = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/cc/WeChatProjects/miniprogram-3")
    config_path = project_root / "project.config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    pack_options = config.setdefault("packOptions", {})
    current = pack_options.setdefault("ignore", [])
    for rule in IGNORES:
        if rule not in current:
            current.append(rule)
    includes = pack_options.setdefault("include", [])
    if QUESTION_ASSET_INCLUDE not in includes:
        includes.append(QUESTION_ASSET_INCLUDE)
    if HOME_ASSET_INCLUDE not in includes:
        includes.append(HOME_ASSET_INCLUDE)

    # Scene image paths are selected from question metadata at runtime. The
    # static unused-file analyzer cannot reliably see those references, so it
    # must not remove the images from remote-debug or upload packages.
    setting = config.setdefault("setting", {})
    setting["ignoreDevUnusedFiles"] = False
    setting["ignoreUploadUnusedFiles"] = False
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    private_config_path = project_root / "project.private.config.json"
    if private_config_path.exists():
        private_config = json.loads(private_config_path.read_text(encoding="utf-8"))
        private_setting = private_config.setdefault("setting", {})
        private_setting["ignoreDevUnusedFiles"] = False
        private_setting["ignoreUploadUnusedFiles"] = False
        private_config_path.write_text(
            json.dumps(private_config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(config_path)


if __name__ == "__main__":
    main()
