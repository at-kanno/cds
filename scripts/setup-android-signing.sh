#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ANDROID_DIR="$ROOT/frontend/android"
KEYSTORE="$ANDROID_DIR/app/upload-keystore.jks"
PROPS="$ANDROID_DIR/key.properties"

echo "==> Android upload keystore setup (Google Play)"
echo "    App ID: jp.co.olivenet.cds"
echo

if [ -f "$KEYSTORE" ]; then
  echo "Keystore already exists: $KEYSTORE"
  echo "Skip keytool or delete the file to recreate."
else
  echo "Create upload keystore (remember passwords — required for every release):"
  keytool -genkeypair -v \
    -keystore "$KEYSTORE" \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias upload \
    -storetype JKS
fi

if [ ! -f "$PROPS" ]; then
  cp "$ANDROID_DIR/key.properties.example" "$PROPS"
  echo
  echo "Created $PROPS — edit storePassword and keyPassword to match keytool."
else
  echo "key.properties already exists: $PROPS"
fi

echo
echo "Next:"
echo "  1. Edit frontend/android/key.properties"
echo "  2. bash scripts/build-android-aab.sh"
echo "  3. Upload AAB in Google Play Console → Internal testing"
echo "  See docs/google-play-internal-test.md"
