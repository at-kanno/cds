#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is not installed or not on PATH."
  exit 1
fi

# Prefer scripts/run_subject.sh cds|spanish4 for flavored runs.
API_URL="${API_BASE_URL:-}"
FLAVOR="${FLAVOR:-cds}"
APP_TITLE="${APP_TITLE:-CDS}"
RUN_ARGS=(run --flavor "$FLAVOR" -d android)
RUN_ARGS+=(--dart-define="APP_FLAVOR=$FLAVOR")
RUN_ARGS+=(--dart-define="APP_TITLE=$APP_TITLE")

if [[ -n "$API_URL" ]]; then
  RUN_ARGS+=(--dart-define="API_BASE_URL=$API_URL")
fi

echo "Starting $FLAVOR on Android emulator..."
flutter "${RUN_ARGS[@]}"
