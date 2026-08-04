# 試験プラン YAML（非エンジニア向け）

各科目の試験メニュー・出題配分は、このフォルダの `{科目名}.exams.yaml` で編集します。

| ファイル | 対応する APP_PROFILE |
|---|---|
| `cds.exams.yaml` | `CDS` |
| `spanish4.exams.yaml` | `SPANISH4` |

`config.json` にはログイン URL・合格点・メール文面など**システム共通設定**のみ残しています。  
試験の問題数・制限時間・メニュー表示・出題スロットは **YAML のみ** を編集してください。

## 編集の基本

1. メニューに表示する試験 ID を `menu.sections[].items` に列挙
2. 各試験の詳細を `exams` に定義（ID は文字列 `"10"` など）
3. 保存後、Flask アプリを再起動（PyCharm の **Flask app** を再実行）

## スロットの書き方

```yaml
exams:
  "101":
    mode: multi
    action: makeExam
    title: 文法4択1：確認問題
    time_limit_seconds: 600
    menu:
      label: 文法4択1【10問】
      color: "#642852"
    slots:
      - repeat: 10
        from: [11, 12]               # 各問をリストから等確率で選択（いちばん簡単）
```

```yaml
slots:
  - area: org_culture                # 1問固定
  - repeat: 5
    area: info_technology            # 同カテゴリを5問
  - pick:                            # 重み付き確率で1問
      - { area: new_service_practice, weight: 50 }
      - { area: user_support_practice, weight: 50 }
  - use: full_exam                   # 共通配分（sequences）を参照
    take: 10
```

### スロット種別

| 種別 | 書き方 | 用途 |
|---|---|---|
| プール | `- repeat: 10` + `from: [11, 12]` | リストから等確率で N 問（推奨） |
| 固定 | `- area: grammar4` | 指定カテゴリ1問 |
| 繰り返し | `- repeat: 10` + `area:` | 同カテゴリを N 問 |
| 確率 | `- pick:` + `weight` | 重み付きランダム |
| 共通配分 | `- use: full_exam` | 模擬試験40問など |

## 選択肢数（2択 / 3択 / 4択）

`areas` に `choice_count` を書くと、出題時のシャッフルと画面表示に使われます。

```yaml
grammar3:
  categories: [31]
  choice_count: 3   # A–C のみ表示（D は出さない）
```

| choice_count | 画面 |
|---|---|
| 4 | A B C D |
| 3 | A B C |
| 2 | A B |

DB の A4（4択目）にダミー文字があっても、`choice_count: 3` なら D は出ません。  
新規出題から有効です（古い試験の examlist は作成時の並びのまま）。

## CDS 専用: topics

CDS は画面表示用 `areas`（4領域）と、出題参照用 `topics`（10カテゴリ）を分けています。  
スロットの `area:` には **topics のキー名**（例: `org_culture`）を指定します。

## 新しい科目を追加する

1. `static/subjects/{profile}.exams.yaml` を新規作成（既存ファイルをコピーして編集）
2. `.env` の `APP_PROFILE` をその科目名に設定
3. 再起動してメニューを確認

YAML が無い科目（TOEIC など）は従来どおり `config.json` の `exam_catalog` / `menu` を使います。
