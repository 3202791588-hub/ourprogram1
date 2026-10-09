#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR="$PROJECT_DIR/dist"
STAGE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/personality-cloudrun.XXXXXX")

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT INT TERM

mkdir -p "$DIST_DIR"
rsync -a \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.pytest_cache' \
  --exclude 'test.sqlite3' \
  "$PROJECT_DIR/backend/" "$STAGE_DIR/"

cp "$PROJECT_DIR/cloudrun/Dockerfile" "$STAGE_DIR/Dockerfile"
cp "$PROJECT_DIR/cloudrun/start.sh" "$STAGE_DIR/start.sh"
cp "$PROJECT_DIR/cloudrun/.dockerignore" "$STAGE_DIR/.dockerignore"
cp "$PROJECT_DIR/cloudrun/README_UPLOAD.md" "$STAGE_DIR/README_UPLOAD.md"

chmod +x "$STAGE_DIR/start.sh"
(cd "$STAGE_DIR" && zip -qr "$DIST_DIR/personality-api-cloudrun.zip" .)

printf '%s\n' "$DIST_DIR/personality-api-cloudrun.zip"
