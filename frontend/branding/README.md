# アプリアイコン（1024×1024）の置き場

**ここに 1024×1024 の PNG を1枚置くだけでOKです。**  
`mipmap-*` の細かいサイズは、あとでスクリプトで自動生成します。

## 配置場所（絶対パスの目安）

| アプリ | 置くファイル |
|---|---|
| スペイン語 | `frontend/branding/spanish4/app_icon_1024.png` |
| CDS | `frontend/branding/cds/app_icon_1024.png` |
| TOEIC | `frontend/branding/toeic/app_icon_1024.png` |

Windows のフルパス例（スペイン語）:

```
C:\Users\kanno\Documents\MockSystem\cds\frontend\branding\spanish4\app_icon_1024.png
```

## 手順

1. 作った 1024×1024 PNG を、上のファイル名でコピーする  
2. 次で各サイズを生成する:

```bash
cd frontend
python scripts/generate_app_icons.py
```

（Pillow が必要: `pip install pillow`）

生成先:

| 科目 | Android | iOS |
|---|---|---|
| CDS | `android/app/src/cds/res/mipmap-*/ic_launcher.png` | `ios/.../AppIcon.appiconset/` |
| スペイン語 | `android/app/src/spanish4/res/mipmap-*/ic_launcher.png` | `ios/.../AppIcon-Spanish4.appiconset/` |
| TOEIC | `android/app/src/toeic/res/mipmap-*/ic_launcher.png` | `ios/.../AppIcon-Toeic.appiconset/` |

※ `mipmap-*` に直接 1024 を置く必要はありません。
