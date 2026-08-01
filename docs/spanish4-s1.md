# スペイン語検定4級 — S1（骨格）

`APP_PROFILE=SPANISH4` で起動する科目プロファイルです。  
問題データ（`exam.sqlite`）の投入は運用側で行います。

---

## S1 でできること

| 機能 | 状態 |
|---|---|
| メニュー（一問一答 1〜4 / 分野別 1〜6 / 試験形式 35問） | ✅ |
| 制限時間（一問一答・分野別10分・試験60分） | ✅ |
| 合格ライン表示（70%） | ✅（S1は正答率ベース） |
| 4択 UI | ✅（現行のまま） |
| 2択・3択の正しい表示 | ❌ S2 |
| ヒアリング再生（2回制限） | ❌ S3 |
| 配点加重採点（100点満点） | ❌ S4 |

S1 では分野3〜6も **4択UIで出題可能** です（DBに a1〜a4 を入れておけば動く）。  
本番どおりの2択/3択/音声は後続段階です。

---

## 起動方法

```bash
# backend/.env
APP_PROFILE=SPANISH4
```

```bash
cd backend
APP_PROFILE=SPANISH4 .venv/bin/python -c \
  "from menu_service import build_main_menu; from unittest.mock import patch; \
   import json; \
   patch('menu_service.getStatus', return_value=0).start(); \
   patch('menu_service.getLoginName', return_value='t@example.com').start(); \
   print(json.dumps(build_main_menu(1), ensure_ascii=False, indent=2))"
```

本番（別パス）:

```
https://traveltokio.com/spanish4/  → APP_PROFILE=SPANISH4 + 専用 exam.sqlite
```

Flutter は同じアプリでサーバー URL を  
`https://traveltokio.com/spanish4` に変更するだけです。

---

## 問題 DB の CATEGORY 番号（必須）

`knowledge_base.category` に次を入れてください。

| 分野 | CATEGORY | 問数（分野別） | 形式（将来） | 一問一答 |
|---|---|---|---|---|
| 文法4択 | **11** | 10 | 4択 | ✅ 91 |
| 会話4択 | **21** | 5 | 4択 | ✅ 92 |
| 文法3択 | **31** | 5 | 3択 | ✅ 93 |
| 会話3択 | **41** | 5 | 3択 | ✅ 94 |
| リーディング2択 | **51** | 5 | 2択 | — |
| ヒアリング3択 | **61** | 5 | 3択 | — |

試験形式（category 70）は上記を **10+5+5+5+5+5=35問** で組み合わせます。

### カラム（現行スキーマ）

| カラム | 内容 |
|---|---|
| number | 問題ID（主キー） |
| category | 上表の番号 |
| level | 通常 `1` |
| q | 問題文（HTML可） |
| a1〜a4 | 選択肢（S1は4つ埋める。2/3択は余分を空でも可だが UI は4つ出る） |
| cid1〜cid4 | 解説コメントID |
| flag | 任意 |

バンクは分野別・模擬で重複抽選されないよう、**各 CATEGORY に十分な件数**（目安: 分野別の2〜3倍以上）を用意してください。

---

## メニュー ↔ exam category

| メニュー | exam category | 時間 |
|---|---|---|
| 一問一答 文法4択 | 91 | 1分 |
| 一問一答 会話4択 | 92 | 2分 |
| 一問一答 文法3択 | 93 | 2分 |
| 一問一答 会話3択 | 94 | 2分 |
| 分野別 文法4択 | 10 | 10分 / 10問 |
| 分野別 会話4択 | 20 | 10分 / 5問 |
| 分野別 文法3択 | 30 | 10分 / 5問 |
| 分野別 会話3択 | 40 | 10分 / 5問 |
| 分野別 リーディング | 50 | 10分 / 5問 |
| 分野別 ヒアリング | 60 | 10分 / 5問 |
| 模擬試験 | 70 | 60分 / 35問 |

---

## 次の段階

- **S2:** 2択・3択の UI/API（`choices[]`）  
- **S3:** ヒアリング音声・再生2回  
- **S4:** 配点加重（合計100点・70点合格）
