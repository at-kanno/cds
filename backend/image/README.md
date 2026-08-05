# Question images / Part1 media (not in git)

Place files here (or set `EXAM_IMAGE_DIR`).

| 種別 | ファイル名 |
|---|---|
| 写真（Part1） | `{NUMBER}.png`（`.jpg` / `.webp` も可） |
| 音声（Part1） | `{NUMBER}-A.mp3` … `{NUMBER}-D.mp3`（選択肢ごと） |

例: 問題番号 `101` → `101.png` + `101-A.mp3` … `101-D.mp3`

- 西検など従来のヒアリングは `backend/audio/{NUMBER}.mp3`（1問1ファイル）
- Part1 の選択肢 mp3 は `image/` 同居のままで可（`audio/` にあっても可）
