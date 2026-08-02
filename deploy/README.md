# Subject deployment (Phase 1)

Each server instance serves **one subject**. Set the active profile in `backend/.env`:

```bash
cp backend/.env.example backend/.env
# Edit APP_PROFILE to match a section in backend/static/config.json
APP_PROFILE=CDS
```

## Add a new subject (e.g. TOEIC / SPANISH4)

1. Add or copy a profile block in `backend/static/config.json` (`menu`, `areas`, `exam_catalog`, `status_rules`).
2. Prepare `exam.sqlite` with questions whose categories match `areas`.
3. Deploy a separate service (or directory) with `APP_PROFILE=SPANISH4` (or `TOEIC`) in `.env`.
4. Configure Apache to proxy `/spanish4/` (or `/toeic/`) to that Gunicorn instance.
5. Point the Flutter app login URL to that path — no app update required.

Spanish Level 4 S1 notes: `docs/spanish4-s1.md`

See `deploy/apache/cds-proxy-snippet.conf` for the Apache proxy pattern.

## 科目ごとの DB（exam-{PROFILE}.sqlite）

- 科目ごとに **別ファイル**（利用者・問題・履歴を分離）。詳細: `docs/per-subject-database.md`
- 例: `exam-CDS.sqlite` / `exam-SPANISH4.sqlite`（CDS は従来の `exam.sqlite` も可）
- **deploy では上書きしない**（バックアップは別途運用）

```bash
cd ~/cds
git update-index --skip-worktree backend/exam.sqlite 2>/dev/null || true
git update-index --skip-worktree backend/exam-CDS.sqlite 2>/dev/null || true
git update-index --skip-worktree backend/exam-SPANISH4.sqlite 2>/dev/null || true
```

## sudo（Deploy Actions 用）

GitHub Actions から `systemctl restart` するには、ubuntu ユーザーが **パスワードなし sudo** できる必要があります。EC2 で1回:

```bash
sudo visudo -f /etc/sudoers.d/cds-deploy
```

```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart cds, /bin/systemctl is-active cds
```
