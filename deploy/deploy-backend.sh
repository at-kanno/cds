#!/usr/bin/env bash
set -euo pipefail

# Guard: CI may inject empty strings via envs; treat empty as unset.
APP_DIR="${APP_DIR:-/home/ubuntu/cds}"
SPANISH4_DIR="${SPANISH4_DIR:-/home/ubuntu/spanish4}"
TOEIC_DIR="${TOEIC_DIR:-/home/ubuntu/toeic}"
BRANCH="${DEPLOY_BRANCH:-main}"
HEALTHCHECK_URL="${HEALTHCHECK_URL:-https://traveltokio.com/cds/api/health}"
SPANISH4_HEALTHCHECK_URL="${SPANISH4_HEALTHCHECK_URL:-https://traveltokio.com/spanish4/api/health}"
TOEIC_HEALTHCHECK_URL="${TOEIC_HEALTHCHECK_URL:-https://traveltokio.com/toeic/api/health}"
if [ -z "$APP_DIR" ]; then APP_DIR=/home/ubuntu/cds; fi
if [ -z "$HEALTHCHECK_URL" ]; then HEALTHCHECK_URL=https://traveltokio.com/cds/api/health; fi
if [ -z "$SPANISH4_DIR" ]; then SPANISH4_DIR=/home/ubuntu/spanish4; fi
if [ -z "$SPANISH4_HEALTHCHECK_URL" ]; then SPANISH4_HEALTHCHECK_URL=https://traveltokio.com/spanish4/api/health; fi
if [ -z "$TOEIC_DIR" ]; then TOEIC_DIR=/home/ubuntu/toeic; fi
if [ -z "$TOEIC_HEALTHCHECK_URL" ]; then TOEIC_HEALTHCHECK_URL=https://traveltokio.com/toeic/api/health; fi

# Live DBs must survive git reset. skip-worktree alone is fragile when the
# working tree is dirty ("Entry 'backend/exam.sqlite' not uptodate").
preserve_and_sync_git() {
  local app_dir="$1"
  local branch="$2"
  local backup_dir
  backup_dir="$(mktemp -d)"

  echo "==> Sync git in $app_dir from origin/${branch}"
  cd "$app_dir"
  git fetch origin "${branch}"
  git checkout "${branch}"

  echo "==> Back up live sqlite DBs ($app_dir)"
  shopt -s nullglob
  for db in backend/exam.sqlite backend/exam-*.sqlite; do
    if [ -f "$db" ]; then
      cp -a "$db" "$backup_dir/"
      echo "    saved $(basename "$db")"
    fi
  done
  shopt -u nullglob

  echo "==> Clear skip-worktree on tracked DBs so reset can proceed"
  shopt -s nullglob
  for db in backend/exam.sqlite backend/exam-*.sqlite; do
    if git ls-files --error-unmatch "$db" >/dev/null 2>&1; then
      git update-index --no-skip-worktree "$db" 2>/dev/null || true
    fi
  done
  shopt -u nullglob

  git checkout -- backend/static/config.json 2>/dev/null || true
  git reset --hard "origin/${branch}"

  echo "==> Restore live sqlite DBs ($app_dir)"
  shopt -s nullglob
  for db in "$backup_dir"/*; do
    if [ -f "$db" ]; then
      cp -a "$db" "backend/$(basename "$db")"
      echo "    restored $(basename "$db")"
    fi
  done
  shopt -u nullglob
  rm -rf "$backup_dir"

  shopt -s nullglob
  for db in backend/exam.sqlite backend/exam-*.sqlite; do
    if [ -f "$db" ] && git ls-files --error-unmatch "$db" >/dev/null 2>&1; then
      git update-index --skip-worktree "$db" 2>/dev/null || true
    fi
  done
  shopt -u nullglob
}

install_backend_deps() {
  local app_dir="$1"
  local default_profile="$2"

  echo "==> Install backend dependencies ($app_dir)"
  cd "$app_dir/backend"
  if [ ! -d .venv ]; then
    python3 -m venv .venv
  fi
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt

  if [ -f .env.example ] && [ ! -f .env ]; then
    cp .env.example .env
    echo "Created $app_dir/backend/.env from .env.example"
  fi
  if [ -f .env ] && ! grep -q '^APP_PROFILE=' .env; then
    echo "APP_PROFILE=${default_profile}" >> .env
    echo "Added APP_PROFILE=${default_profile} to $app_dir/backend/.env"
  fi
}

resolve_subject_dir() {
  # Prefer systemd WorkingDirectory (.../backend) when the unit exists.
  local unit="$1"
  local default_dir="$2"
  local wd=""
  if systemctl cat "${unit}.service" >/dev/null 2>&1; then
    wd="$(systemctl show -p WorkingDirectory --value "${unit}.service" 2>/dev/null || true)"
    if [ -n "$wd" ] && [ "$wd" != "/" ] && [ -d "$wd" ]; then
      dirname "$wd"
      return 0
    fi
  fi
  printf '%s\n' "$default_dir"
}

sync_subject_checkout() {
  local unit="$1"
  local default_dir="$2"
  local profile="$3"
  local dir
  dir="$(resolve_subject_dir "$unit" "$default_dir")"

  if [ -d "${dir}/.git" ]; then
    preserve_and_sync_git "${dir}" "${BRANCH}"
    install_backend_deps "${dir}" "${profile}"
  else
    echo "==> ${unit}: checkout not found (${dir}); skip (clone once or set path env)"
  fi
}

restart_service_if_present() {
  local unit="$1"
  if systemctl list-unit-files "${unit}.service" >/dev/null 2>&1 \
    && systemctl cat "${unit}.service" >/dev/null 2>&1; then
    echo "==> Restart ${unit}"
    if ! sudo -n systemctl restart "${unit}"; then
      echo "ERROR: sudo systemctl requires NOPASSWD for ${unit}."
      echo "       Update /etc/sudoers.d/cds-deploy to include:"
      echo "       /bin/systemctl restart ${unit}, /bin/systemctl is-active ${unit}"
      exit 1
    fi
    sudo -n systemctl is-active "${unit}"
  else
    echo "==> Skip restart: ${unit}.service not installed"
  fi
}

healthcheck() {
  local url="$1"
  local label="$2"
  echo "==> Health check (${label}): $url"
  for attempt in 1 2 3 4 5; do
    if curl -fsS "$url"; then
      echo
      echo "Health check OK (${label})"
      return 0
    fi
    echo "Health check attempt ${attempt}/5 failed (${label}); retrying in 3s..."
    sleep 3
  done
  echo "ERROR: Health check failed after 5 attempts (${label}): $url"
  return 1
}

echo "==> Deploy target: APP_DIR=$APP_DIR BRANCH=$BRANCH"

if [ "${SKIP_GIT_SYNC:-0}" != "1" ]; then
  preserve_and_sync_git "${APP_DIR}" "${BRANCH}"
fi

install_backend_deps "${APP_DIR}" "CDS"

# CDS may already be synced by Actions bootstrap; always refresh other subjects.
sync_subject_checkout spanish4 "${SPANISH4_DIR}" "SPANISH4"
sync_subject_checkout toeic "${TOEIC_DIR}" "TOEIC"

restart_service_if_present cds
restart_service_if_present spanish4
restart_service_if_present toeic

healthcheck "${HEALTHCHECK_URL}" "CDS"
if systemctl cat spanish4.service >/dev/null 2>&1; then
  healthcheck "${SPANISH4_HEALTHCHECK_URL}" "SPANISH4"
fi
if systemctl cat toeic.service >/dev/null 2>&1; then
  healthcheck "${TOEIC_HEALTHCHECK_URL}" "TOEIC"
fi

echo "Deploy completed successfully."
