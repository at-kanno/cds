#!/usr/bin/env bash
# Build a release App Bundle for cds, spanish4, or toeic.
# Usage:
#   bash scripts/build_android.sh cds
#   bash scripts/build_android.sh spanish4
#   bash scripts/build_android.sh toeic
set -euo pipefail

cd "$(dirname "$0")/.."

FLAVOR="${1:-}"
if [[ "$FLAVOR" != "cds" && "$FLAVOR" != "spanish4" && "$FLAVOR" != "toeic" ]]; then
  echo "Usage: $0 cds|spanish4|toeic"
  exit 1
fi

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is not installed or not on PATH."
  exit 1
fi

case "$FLAVOR" in
  cds)
    API_URL="${API_BASE_URL:-https://traveltokio.com/cds}"
    APP_TITLE="${APP_TITLE:-CDS}"
    ;;
  spanish4)
    API_URL="${API_BASE_URL:-https://traveltokio.com/spanish4}"
    APP_TITLE="${APP_TITLE:-スペイン語検定4級}"
    ;;
  toeic)
    API_URL="${API_BASE_URL:-https://traveltokio.com/toeic}"
    APP_TITLE="${APP_TITLE:-TOEIC 模擬試験}"
    ;;
esac

BUILD_NAME="${BUILD_NAME:-}"
BUILD_NUMBER="${BUILD_NUMBER:-}"

echo "Building Android App Bundle"
echo "  flavor   : $FLAVOR"
echo "  API URL  : $API_URL (hidden in UI)"
echo "  APP_TITLE: $APP_TITLE"
[[ -n "$BUILD_NAME" ]] && echo "  version  : $BUILD_NAME"
[[ -n "$BUILD_NUMBER" ]] && echo "  build    : $BUILD_NUMBER"

BUILD_ARGS=(
  build appbundle
  --flavor "$FLAVOR"
  --release
  --dart-define="APP_FLAVOR=$FLAVOR"
  --dart-define="APP_TITLE=$APP_TITLE"
  --dart-define="API_BASE_URL=$API_URL"
)
if [[ -n "$BUILD_NAME" ]]; then
  BUILD_ARGS+=(--build-name="$BUILD_NAME")
fi
if [[ -n "$BUILD_NUMBER" ]]; then
  BUILD_ARGS+=(--build-number="$BUILD_NUMBER")
fi

flutter "${BUILD_ARGS[@]}"

echo
echo "Output: build/app/outputs/bundle/${FLAVOR}Release/app-${FLAVOR}-release.aab"
