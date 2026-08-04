#!/usr/bin/env bash
# Run a subject flavor on a connected device/emulator (dev).
# Usage:
#   bash scripts/run_subject.sh cds
#   bash scripts/run_subject.sh spanish4
# Optional: API_BASE_URL=http://192.168.x.x:8081 bash scripts/run_subject.sh spanish4
set -euo pipefail

cd "$(dirname "$0")/.."

FLAVOR="${1:-}"
DEVICE="${2:-}"
if [[ "$FLAVOR" != "cds" && "$FLAVOR" != "spanish4" ]]; then
  echo "Usage: $0 cds|spanish4 [device_id]"
  exit 1
fi

case "$FLAVOR" in
  cds)
    DEFAULT_API="https://traveltokio.com/cds"
    APP_TITLE="CDS"
    ;;
  spanish4)
    DEFAULT_API="https://traveltokio.com/spanish4"
    APP_TITLE="スペイン語検定4級"
    ;;
esac

# For local backend testing, leave API_BASE_URL empty to show the server field.
API_URL="${API_BASE_URL-}"
if [[ -z "${API_BASE_URL+x}" ]]; then
  API_URL="$DEFAULT_API"
fi

ARGS=(run --flavor "$FLAVOR")
if [[ -n "$DEVICE" ]]; then
  ARGS+=(-d "$DEVICE")
fi
ARGS+=(
  --dart-define="APP_FLAVOR=$FLAVOR"
  --dart-define="APP_TITLE=$APP_TITLE"
)
if [[ -n "$API_URL" ]]; then
  ARGS+=(--dart-define="API_BASE_URL=$API_URL")
fi

echo "flutter ${ARGS[*]}"
flutter "${ARGS[@]}"
