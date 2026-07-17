#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is not installed or not on PATH."
  exit 1
fi

API_URL="${API_BASE_URL:-}"
RUN_ARGS=(run -d ios)

if [[ -n "$API_URL" ]]; then
  RUN_ARGS+=(--dart-define="API_BASE_URL=$API_URL")
fi

echo "Starting CDS on iOS simulator..."
flutter "${RUN_ARGS[@]}"
