# Listening audio (not in git)

Place mp3 files here (or set `EXAM_AUDIO_DIR`).

- Normal: `{NUMBER}.mp3` (example: `6101.mp3`)
- Shared conversation (optional): `{FLAG}.mp3` with FLAG in 201–299

EC2 example:

```bash
sudo mkdir -p /home/ubuntu/spanish4/backend/audio
# copy *.mp3 into that directory
sudo systemctl restart spanish4
```
