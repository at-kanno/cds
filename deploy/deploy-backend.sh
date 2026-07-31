#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/home/ubuntu/cds}"
BRANCH="${DEPLOY_BRANCH:-main}"
HEALTHCHECK_URL="${HEALTHCHECK_URL:-https://traveltokio.com/cds/api/health}"

cd "$APP_DIR"

echo "==> Fetch and checkout ${BRANCH}"
git fetch origin "${BRANCH}"
git checkout "${BRANCH}"

# exam.sqlite is live data (always dirty). Deploy must not touch it.
if git ls-files --error-unmatch backend/exam.sqlite >/dev/null 2>&1; then
  git update-index --skip-worktree backend/exam.sqlite
fi
git checkout -- backend/static/config.json 2>/dev/null || true
git reset --hard "origin/${BRANCH}"

echo "==> Install backend dependencies"
cd backend
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ -f .env.example ] && [ ! -f .env ]; then
  echo "WARNING: backend/.env is missing. Copy .env.example and set APP_PROFILE."
fi
if [ -f .env ] && ! grep -q '^APP_PROFILE=' .env; then
  echo "WARNING: APP_PROFILE is not set in backend/.env (defaults to CDS at runtime)."
fi

echo "==> Restart CDS service"
sudo systemctl restart cds
sudo systemctl is-active cds

echo "==> Health check"
curl -fsS "${HEALTHCHECK_URL}"
echo
echo "Deploy completed successfully."
