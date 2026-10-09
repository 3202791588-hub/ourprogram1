#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TARGET_PROJECT=${1:-/Users/cc/WeChatProjects/miniprogram-3}
TARGET_DIR="$TARGET_PROJECT/miniprogram"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/personality-miniapp.XXXXXX")

cleanup() {
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT INT TERM

if [ ! -f "$TARGET_PROJECT/project.config.json" ]; then
  printf '微信项目不存在或缺少 project.config.json: %s\n' "$TARGET_PROJECT" >&2
  exit 1
fi

SCENE_COUNT=$(find "$PROJECT_DIR/miniapp/assets/questions" -mindepth 2 -maxdepth 2 -name 'scene.jpg' -type f | wc -l | tr -d ' ')
if [ "$SCENE_COUNT" -ne 24 ]; then
  printf '发布版题目图片应为24张，当前为%s张；请先运行: ./.venv/bin/python scripts/build_question_assets.py\n' "$SCENE_COUNT" >&2
  exit 1
fi

(cd "$PROJECT_DIR/miniapp" && ./node_modules/.bin/tsc --outDir "$BUILD_DIR")

rsync -a \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'assets/questions/**/scene-v*.png' \
  --exclude 'assets/questions/**/scene.webp' \
  --exclude '*.ts' \
  --exclude 'package.json' \
  --exclude 'package-lock.json' \
  --exclude 'tsconfig.json' \
  --exclude 'project.config.json' \
  "$PROJECT_DIR/miniapp/" "$BUILD_DIR/"

# Intentionally do not use --delete: cloud template files, envList.js and other
# project-owned files in miniprogram-3 must remain intact.
rsync -a "$BUILD_DIR/" "$TARGET_DIR/"

# Remove only the obsolete generated WebP files from the DevTools copy. The
# approved PNG masters remain in the source project and are never deleted.
sequence=1
while [ "$sequence" -le 24 ]; do
  number=$(printf '%02d' "$sequence")
  rm -f "$TARGET_DIR/assets/questions/q$number/scene.webp"
  sequence=$((sequence + 1))
done

python3 "$PROJECT_DIR/scripts/configure_miniprogram3.py" "$TARGET_PROJECT" >/dev/null

printf '%s\n' "$TARGET_DIR"
