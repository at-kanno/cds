# Listening audio

Place mp3 files here (or set `EXAM_AUDIO_DIR`). `*.mp3` is tracked in git.

- Normal: `{NUMBER}.mp3` (example: `6101.mp3`)
- Shared conversation (optional): `{FLAG}.mp3` with FLAG in 201–299
- TOEIC Part1 choice clips live next to PNG in `backend/image/` (`{NUMBER}-A.mp3` … `D`)

EC2: pull/deploy the repo (or sync `backend/audio/`), then restart the service.
