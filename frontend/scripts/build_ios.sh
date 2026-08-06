#!/usr/bin/env bash
# Build a release IPA for cds, spanish4, or toeic (Mac + Xcode required).
# Usage:
#   bash scripts/build_ios.sh cds
#   bash scripts/build_ios.sh spanish4
#   bash scripts/build_ios.sh toeic
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

FLAVOR_XCCONFIG="ios/Flutter/Flavor.xcconfig"

restore_flavor_xcconfig() {
  cat > "$FLAVOR_XCCONFIG" <<'EOF'
// Subject branding — overwritten by scripts/build_ios.sh per flavor.
// Defaults = CDS. Do not put secrets here.
APP_DISPLAY_NAME=CDS
APP_BUNDLE_IDENTIFIER=jp.co.olivenet.cds
APP_ICON_NAME=AppIcon
EOF
}
trap restore_flavor_xcconfig EXIT

case "$FLAVOR" in
  cds)
    API_URL="${API_BASE_URL:-https://traveltokio.com/cds}"
    APP_TITLE="${APP_TITLE:-CDS}"
    DISPLAY_NAME="${APP_DISPLAY_NAME:-CDS}"
    BUNDLE_ID="jp.co.olivenet.cds"
    APP_ICON="AppIcon"
    BUILD_NAME="${BUILD_NAME:-}"
    BUILD_NUMBER="${BUILD_NUMBER:-}"
    ;;
  spanish4)
    API_URL="${API_BASE_URL:-https://traveltokio.com/spanish4}"
    APP_TITLE="${APP_TITLE:-スペイン語検定4級}"
    DISPLAY_NAME="${APP_DISPLAY_NAME:-西検４級}"
    BUNDLE_ID="jp.co.olivenet.spanish4"
    APP_ICON="AppIcon-Spanish4"
    # First store build defaults; override with BUILD_NAME / BUILD_NUMBER if needed.
    BUILD_NAME="${BUILD_NAME:-1.0.0}"
    BUILD_NUMBER="${BUILD_NUMBER:-1}"
    ;;
  toeic)
    API_URL="${API_BASE_URL:-https://traveltokio.com/toeic}"
    APP_TITLE="${APP_TITLE:-TOEIC 模擬試験}"
    DISPLAY_NAME="${APP_DISPLAY_NAME:-TOEIC}"
    BUNDLE_ID="jp.co.olivenet.toeic"
    APP_ICON="AppIcon-Toeic"
    BUILD_NAME="${BUILD_NAME:-1.0.0}"
    BUILD_NUMBER="${BUILD_NUMBER:-1}"
    ;;
esac

cat > "$FLAVOR_XCCONFIG" <<EOF
// Generated for flavor: $FLAVOR — restored to CDS on script exit.
APP_DISPLAY_NAME=$DISPLAY_NAME
APP_BUNDLE_IDENTIFIER=$BUNDLE_ID
APP_ICON_NAME=$APP_ICON
EOF

echo "Building iOS IPA"
echo "  flavor       : $FLAVOR"
echo "  bundle id    : $BUNDLE_ID"
echo "  display name : $DISPLAY_NAME"
echo "  API URL      : $API_URL (hidden in UI)"
echo "  app icon     : $APP_ICON"

BUILD_ARGS=(
  build ipa
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

if xcodebuild -list -project ios/Runner.xcodeproj 2>/dev/null | grep -q "^[[:space:]]*${FLAVOR}$"; then
  BUILD_ARGS+=(--flavor "$FLAVOR")
fi

flutter "${BUILD_ARGS[@]}"

echo
echo "IPA under: build/ios/ipa/"
echo "Upload with Transporter, then assign in App Store Connect / TestFlight."
