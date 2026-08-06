# TOEIC / question media

Media packs live in subfolders (tracked in git):

| パック | 内容 |
|---|---|
| `TOEIC-1/` | Part1 写真 `{NUMBER}.png` + 選択肢 `{NUMBER}-A.mp3` … `D` |
| `TOEIC-2/` | Part2 設問 `{NUMBER}-Q.mp3` + 選択肢 `{NUMBER}-A.mp3` … `C` |
| `TOEIC-3/` | Part3 `{FLAG}.mp3` / 任意で `{FLAG}.png`（FLAG=セット先頭。3問とも同じファイル） |

西検など従来の1ファイル音声は `backend/audio/{NUMBER}.mp3`。

Override roots with `EXAM_IMAGE_DIR` / `EXAM_AUDIO_DIR` if needed.
