#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND="$ROOT/frontend"
PROPS="$FRONTEND/android/key.properties"
API_URL="${API_BASE_URL:-https://traveltokio.com/cds}"

if [ ! -f "$PROPS" ]; then
  echo "ERROR: $PROPS not found."
  echo "Run: bash scripts/setup-android-signing.sh"
  exit 1
fi

cd "$FRONTEND"
flutter pub get
flutter build appbundle --release \
  --dart-define="API_BASE_URL=$API_URL"

AAB="$FRONTEND/build/app/outputs/bundle/release/app-release.aab"
echo
echo "Built: $AAB"
echo "Upload this file to Google Play Console → Internal testing → Create release"
