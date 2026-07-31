# Subject deployment (Phase 1)

Each server instance serves **one subject**. Set the active profile in `backend/.env`:

```bash
cp backend/.env.example backend/.env
# Edit APP_PROFILE to match a section in backend/static/config.json
APP_PROFILE=CDS
```

## Add a new subject (e.g. TOEIC)

1. Add or copy a profile block in `backend/static/config.json` (`menu`, `areas`, `exam_catalog`, `status_rules`).
2. Prepare `exam.sqlite` with questions whose categories match `areas`.
3. Deploy a separate service (or directory) with `APP_PROFILE=TOEIC` in `.env`.
4. Configure Apache to proxy `/toeic/` to that Gunicorn instance.
5. Point the Flutter app login URL to `https://your-host/toeic` — no app update required.

See `deploy/apache/cds-proxy-snippet.conf` for the Apache proxy pattern.

## exam.sqlite（本番 DB）

- 受験結果などが記録されるため、**サーバー上では常に変更がある**ファイルとして扱う。
- **deploy ではバックアップも上書きもしない**（バックアップは別途、運用側で管理）。
- git 管理下に残っている EC2 では、deploy 時に `skip-worktree` を設定し、`git reset` しても `exam.sqlite` を触らない。

初回セットアップ（EC2 で1回だけ）:

```bash
cd ~/cds
git update-index --skip-worktree backend/exam.sqlite
```

確認:

```bash
git ls-files -v backend/exam.sqlite
# 先頭が S なら skip-worktree 有効
```

## sudo（Deploy Actions 用）

GitHub Actions から `systemctl restart` するには、ubuntu ユーザーが **パスワードなし sudo** できる必要があります。EC2 で1回:

```bash
sudo visudo -f /etc/sudoers.d/cds-deploy
```

```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart cds, /bin/systemctl is-active cds
```
