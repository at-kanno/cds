#!/usr/bin/env bash
# Build a release App Bundle for cds or spanish4.
# Usage:
#   bash scripts/build_android.sh cds
#   bash scripts/build_android.sh spanish4
set -euo pipefail

cd "$(dirname "$0")/.."

FLAVOR="${1:-}"
if [[ "$FLAVOR" != "cds" && "$FLAVOR" != "spanish4" ]]; then
  echo "Usage: $0 cds|spanish4"
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
esac

echo "Building Android App Bundle"
echo "  flavor   : $FLAVOR"
echo "  API URL  : $API_URL (hidden in UI)"
echo "  APP_TITLE: $APP_TITLE"

flutter build appbundle \
  --flavor "$FLAVOR" \
  --release \
  --dart-define="APP_FLAVOR=$FLAVOR" \
  --dart-define="APP_TITLE=$APP_TITLE" \
  --dart-define="API_BASE_URL=$API_URL"

echo
echo "Output: build/app/outputs/bundle/${FLAVOR}Release/app-${FLAVOR}-release.aab"
