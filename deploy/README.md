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
