#!/usr/bin/env bash
# One-time EC2 setup: CDS (8080) + SPANISH4 (8081) on the same instance.
# Run as ubuntu (not root):  bash deploy/setup-multi-subject.sh
set -euo pipefail

CDS_DIR="${CDS_DIR:-/home/ubuntu/cds}"
SPANISH4_DIR="${SPANISH4_DIR:-/home/ubuntu/spanish4}"
REPO_URL="${REPO_URL:-https://github.com/at-kanno/cds.git}"

echo "==> CDS_DIR=$CDS_DIR"
echo "==> SPANISH4_DIR=$SPANISH4_DIR"

if [ ! -d "$CDS_DIR/.git" ]; then
  echo "ERROR: $CDS_DIR is not a git checkout. Clone cds there first."
  exit 1
fi

echo "==> Ensure CDS .env uses APP_PROFILE=CDS"
if [ ! -f "$CDS_DIR/backend/.env" ]; then
  cp "$CDS_DIR/backend/.env.example" "$CDS_DIR/backend/.env"
fi
if grep -q '^APP_PROFILE=' "$CDS_DIR/backend/.env"; then
  sed -i 's/^APP_PROFILE=.*/APP_PROFILE=CDS/' "$CDS_DIR/backend/.env"
else
  echo 'APP_PROFILE=CDS' >> "$CDS_DIR/backend/.env"
fi

echo "==> Create SPANISH4 checkout (shared remote, separate .env/DB)"
if [ ! -d "$SPANISH4_DIR/.git" ]; then
  git clone "$REPO_URL" "$SPANISH4_DIR"
fi
cd "$SPANISH4_DIR"
git fetch origin main
git checkout main
git reset --hard origin/main

echo "==> SPANISH4 .env"
if [ ! -f "$SPANISH4_DIR/backend/.env" ]; then
  cp "$SPANISH4_DIR/backend/.env.example" "$SPANISH4_DIR/backend/.env"
fi
if grep -q '^APP_PROFILE=' "$SPANISH4_DIR/backend/.env"; then
  sed -i 's/^APP_PROFILE=.*/APP_PROFILE=SPANISH4/' "$SPANISH4_DIR/backend/.env"
else
  echo 'APP_PROFILE=SPANISH4' >> "$SPANISH4_DIR/backend/.env"
fi
# Prefer 8081 when using app.py locally; gunicorn bind is in the unit file.
if ! grep -q '^PORT=' "$SPANISH4_DIR/backend/.env"; then
  echo 'PORT=8081' >> "$SPANISH4_DIR/backend/.env"
fi

echo "==> SPANISH4 venv + dependencies"
cd "$SPANISH4_DIR/backend"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ ! -f exam-SPANISH4.sqlite ]; then
  echo ""
  echo "WARNING: $SPANISH4_DIR/backend/exam-SPANISH4.sqlite がありません。"
  echo "         ローカルの exam-SPANISH4.sqlite を scp で配置してください。"
  echo ""
fi

echo "==> Install systemd units"
sudo cp "$CDS_DIR/deploy/cds.service.example" /etc/systemd/system/cds.service
sudo cp "$CDS_DIR/deploy/spanish4.service.example" /etc/systemd/system/spanish4.service
sudo systemctl daemon-reload
sudo systemctl enable cds spanish4
sudo systemctl restart cds spanish4
sudo systemctl is-active cds spanish4

echo ""
echo "==> sudoers (Deploy Actions 用) — 未設定なら一度だけ:"
echo "    sudo visudo -f /etc/sudoers.d/cds-deploy"
echo "    内容:"
echo "    ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart cds, /bin/systemctl is-active cds, /bin/systemctl restart spanish4, /bin/systemctl is-active spanish4"
echo ""
echo "==> Apache: deploy/apache/multi-subject-proxy-snippet.conf を"
echo "    既存の SSL VirtualHost に追加し、reload してください。"
echo ""
echo "Done. Check:"
echo "  curl -fsS http://127.0.0.1:8080/api/health"
echo "  curl -fsS http://127.0.0.1:8081/api/health"
echo "  https://traveltokio.com/cds/"
echo "  https://traveltokio.com/spanish4/"
