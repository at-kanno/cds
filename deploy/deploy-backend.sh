#!/usr/bin/env bash
set -euo pipefail

# Guard: CI may inject empty strings via envs; treat empty as unset.
APP_DIR="${APP_DIR:-/home/ubuntu/cds}"
BRANCH="${DEPLOY_BRANCH:-main}"
HEALTHCHECK_URL="${HEALTHCHECK_URL:-https://traveltokio.com/cds/api/health}"
if [ -z "$APP_DIR" ]; then APP_DIR=/home/ubuntu/cds; fi
if [ -z "$HEALTHCHECK_URL" ]; then HEALTHCHECK_URL=https://traveltokio.com/cds/api/health; fi

cd "$APP_DIR"

echo "==> Deploy target: APP_DIR=$APP_DIR BRANCH=$BRANCH"

# Live DBs must survive git reset. skip-worktree alone is fragile when the
# working tree is dirty ("Entry 'backend/exam.sqlite' not uptodate").
preserve_and_sync_git() {
  local branch="$1"
  local backup_dir
  backup_dir="$(mktemp -d)"

  echo "==> Sync git from origin/${branch}"
  git fetch origin "${branch}"
  git checkout "${branch}"

  echo "==> Back up live sqlite DBs"
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

  echo "==> Restore live sqlite DBs"
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

if [ "${SKIP_GIT_SYNC:-0}" != "1" ]; then
  preserve_and_sync_git "${BRANCH}"
fi

echo "==> Install backend dependencies"
cd backend
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ -f .env.example ] && [ ! -f .env ]; then
  cp .env.example .env
  echo "Created backend/.env from .env.example"
fi
if [ -f .env ] && ! grep -q '^APP_PROFILE=' .env; then
  echo 'APP_PROFILE=CDS' >> .env
  echo "Added APP_PROFILE=CDS to backend/.env"
fi

echo "==> Restart CDS service"
if ! sudo -n systemctl restart cds; then
  echo "ERROR: sudo systemctl requires a password. Add NOPASSWD for systemctl on this host."
  exit 1
fi
sudo -n systemctl is-active cds

echo "==> Health check: $HEALTHCHECK_URL"
for attempt in 1 2 3 4 5; do
  if curl -fsS "$HEALTHCHECK_URL"; then
    echo
    echo "Deploy completed successfully."
    exit 0
  fi
  echo "Health check attempt ${attempt}/5 failed; retrying in 3s..."
  sleep 3
done

echo "ERROR: Health check failed after 5 attempts."
exit 1
