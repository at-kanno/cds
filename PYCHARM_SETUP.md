# PyCharm デバッグ設定ガイド

プロジェクト: `C:\Users\kanno\Documents\MockSystem\cds`

## 1. 仮想環境（済）

```powershell
cd C:\Users\kanno\Documents\MockSystem\cds\backend
C:\Users\kanno\PycharmProjects\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. PyCharm でインタープリタを設定（必須）

**この設定をしないと `ModuleNotFoundError: flask_cors` になります。**

1. **File → Settings**（Mac: **PyCharm → Settings**）
2. **Project: cds → Python Interpreter**
3. 右上 **Add Interpreter → Add Local Interpreter**
4. **Virtualenv Environment → Existing**
5. 次を指定:

```
C:\Users\kanno\Documents\MockSystem\cds\backend\.venv\Scripts\python.exe
```

6. **OK** → 一覧に `flask`, `flask-cors` が表示されることを確認
7. **Apply → OK**

> エラー「Python 3.12 (2) が見つからない」は、古い SDK 名が残っているためです。必ず `.venv` を選び直してください。

## 3. 実行設定（Run Configuration）

**`index.py` を直接 Debug しないでください。** 必ず **Flask app** を使います。

1. PyCharm 右上の実行設定で **Flask app** を選択（デフォルト設定済み）
2. **Debug**（虫アイコン）をクリック

| 項目 | 値 |
|------|-----|
| Script | `backend/app.py` ← **index.py ではない** |
| Interpreter | `backend/.venv/Scripts/python.exe` |
| Working directory | `backend` |
| URL | http://127.0.0.1:8080 |

`index.py` を右クリック → Debug すると、別の Python が使われて `flask_cors` エラーになります。

## 4. ソースルート

`backend` をソースルートに設定済み（`.idea/cds.iml`）。  
`import users` などのモジュール import エラーが出る場合:

1. プロジェクトツリーで `backend` を右クリック
2. **Mark Directory as → Sources Root**

## 5. よくあるエラー

| エラー | 対処 |
|--------|------|
| No Python interpreter | 上記 Step 2 で `.venv` を設定 |
| ModuleNotFoundError: flask | `.venv` で `pip install -r requirements.txt` |
| sqlite3.Error / no such table | `backend` に `exam.sqlite` または `exam-CDS.sqlite` が必要 |
| ポート使用中 | `.env` に `PORT=8081` を追加 |

## 6. データベース

本番 DB ファイル（`exam.sqlite` 等）がリポジトリに含まれない場合、別途配置が必要です。

`.env` でパスを指定できます:

```
EXAM_DB_PATH=C:\path\to\exam.sqlite
```

## 7. 動作確認（ターミナル）

```powershell
cd C:\Users\kanno\Documents\MockSystem\cds\backend
.\.venv\Scripts\activate
python app.py
```

ブラウザで http://127.0.0.1:8080 を開く。
