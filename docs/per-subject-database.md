# 科目ごとのデータベース（exam-{PROFILE}.sqlite）

利用者が科目ごとに異なるため、**問題・ユーザー・受験履歴は科目専用の sqlite** に分離します。

---

## ルール

| APP_PROFILE | DB ファイル |
|---|---|
| `CDS` | `exam-CDS.sqlite`（無ければ従来の `exam.sqlite`） |
| `SPANISH4` | `exam-SPANISH4.sqlite` |
| `TOEIC` | `exam-TOEIC.sqlite` |

任意で上書き:

```bash
EXAM_DB_PATH=/absolute/or/relative/path/to/file.sqlite
```

---

## Mac（ローカル）

```bash
cd ~/Projects/CDS/backend

# スペイン語用（いま exam.sqlite に入れたデータを移す例）
mv exam.sqlite exam-SPANISH4.sqlite

# CDS 用は別名で保持
# mv exam-cds-backup.sqlite exam-CDS.sqlite
# または従来名のまま: exam.sqlite （APP_PROFILE=CDS のときだけフォールバック）

# .env
APP_PROFILE=SPANISH4
```

起動:

```bash
python app.py
# → exam-SPANISH4.sqlite を使用
```

CDS を試すとき:

```bash
# .env を APP_PROFILE=CDS に変更して再起動
# → exam-CDS.sqlite または exam.sqlite
```

**同じ Mac で同時に両方**動かす場合は、ディレクトリまたはポートを分ける（8080=CDS、8081=SPANISH4）か、起動のたびに `.env` とプロセスを切り替える。

---

## 本番 EC2（推奨構成）

手順の詳細: `deploy/README.md` と `deploy/setup-multi-subject.sh`

```
/home/ubuntu/cds/backend/
  .env                 → APP_PROFILE=CDS
  exam-CDS.sqlite      ← CDS 利用者（または従来 exam.sqlite）

/home/ubuntu/spanish4/backend/
  .env                 → APP_PROFILE=SPANISH4
  exam-SPANISH4.sqlite ← スペイン語利用者
```

Apache:

- `/cds/` → ポート 8080（CDS）
- `/spanish4/` → ポート 8081（SPANISH4）

既存 CDS を移す場合（EC2）:

```bash
cd ~/cds/backend
# 互換のままにするなら何もしない（exam.sqlite 継続可）
# 名前を揃えるなら:
cp -a exam.sqlite exam-CDS.sqlite
# .env に APP_PROFILE=CDS があることを確認
# 動作確認後、必要なら exam.sqlite はバックアップとして残す
```

---

## 確認方法

```bash
cd backend
APP_PROFILE=SPANISH4 python -c "import constant; print(constant.db_path)"
# → .../exam-SPANISH4.sqlite

APP_PROFILE=CDS python -c "import constant; print(constant.db_path)"
# → .../exam-CDS.sqlite または .../exam.sqlite
```
