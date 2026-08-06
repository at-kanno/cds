# CDS / スペイン語 — 2アプリ配布ガイド

同じ Flutter コードから **科目別アプリ** をビルドして配布します。  
ユーザーには URL を見せず、接続先はビルド時に埋め込みます。

ストア登録:
- 西検４級: [`store-registration-seiken4.md`](store-registration-seiken4.md)
- TOEIC: [`store-registration-toeic.md`](store-registration-toeic.md)

| | CDS | スペイン語 | TOEIC |
|---|---|---|---|
| Android applicationId | `jp.co.olivenet.cds` | `jp.co.olivenet.spanish4` | `jp.co.olivenet.toeic` |
| iOS Bundle ID | `jp.co.olivenet.cds` | `jp.co.olivenet.spanish4` | `jp.co.olivenet.toeic` |
| ホーム画面名（ストア正式名） | CDS | **西検４級** | **TOEIC** |
| ログイン表示名 | CDS | スペイン語検定4級 | TOEIC 模擬試験 |
| API | `https://traveltokio.com/cds` | `https://traveltokio.com/spanish4` | `https://traveltokio.com/toeic` |
| アイコン | `android/.../src/cds/` | `android/.../src/spanish4/` | `android/.../src/toeic/` |

---

## あなたが用意するもの

1. **アイコン（1024×1024 PNG）**  
   - スペイン語: `frontend/branding/spanish4/app_icon_1024.png`  
   - CDS: `frontend/branding/cds/app_icon_1024.png`  
   - 詳細: `frontend/branding/README.md`（小さいサイズは後で自動生成）
2. **ストアのアプリ枠を2つ**（CDS 用・スペイン語用）  
   - Google Play / App Store Connect それぞれ
3. **テスター名簿**（内部テスト → 一般公開）

---

## Android（すぐ使える）

### 内部テスト用 AAB

```bash
cd frontend
bash scripts/build_android.sh cds
bash scripts/build_android.sh spanish4
```

出力例:

- `build/app/outputs/bundle/cdsRelease/app-cds-release.aab`
- `build/app/outputs/bundle/spanish4Release/app-spanish4-release.aab`

Play Console で **アプリを2つ作成**し、それぞれ内部テストトラックへアップロードします。

### 開発実行

```bash
# 本番 URL 埋め込み（サーバー欄は非表示）
bash scripts/run_subject.sh spanish4

# ローカル API を手入力したいとき（サーバー欄を出す）
API_BASE_URL= bash scripts/run_subject.sh spanish4
```

---

## iOS

現状の Xcode プロジェクト既定は **CDS**（`jp.co.olivenet.cds`）です。

### CDS（既存）

```bash
cd frontend
flutter build ipa --release \
  --dart-define=APP_FLAVOR=cds \
  --dart-define=APP_TITLE=CDS \
  --dart-define=API_BASE_URL=https://traveltokio.com/cds
```

### スペイン語（初回セットアップ）

1. App Store Connect で Bundle ID `jp.co.olivenet.spanish4` を登録  
2. Xcode で spanish4 用 Configuration / Scheme を追加（または別ターゲット）  
   - `PRODUCT_BUNDLE_IDENTIFIER = jp.co.olivenet.spanish4`  
   - `APP_DISPLAY_NAME = 西検４級`  
3. スペイン語用 AppIcon をセット  
4. ビルド:

```bash
# 推奨（scheme 未作成でも dart-define でビルド可）
bash scripts/build_ios.sh spanish4

# または scheme 作成後:
flutter build ipa --release --flavor spanish4 \
  --dart-define=APP_FLAVOR=spanish4 \
  --dart-define=APP_TITLE=スペイン語検定4級 \
  --dart-define=API_BASE_URL=https://traveltokio.com/spanish4
```

（`--flavor spanish4` は Xcode 側の scheme 名と一致させる必要があります。未作成なら CDS と同様の `flutter build ipa` + Bundle ID 差し替えでも可。）

TestFlight → 内部グループ → 一般公開、の順で進めます。

---

## URL を見せない仕組み

`--dart-define=API_BASE_URL=...` が入っているビルドでは、ログイン画面の **サーバー URL 欄を出しません。**  
開発時だけ定義を外すと、従来どおり入力欄が出ます。

---

## 公開までの目安

1. アイコン配置  
2. Android: 両 flavor の内部テスト  
3. iOS: CDS TestFlight → スペイン語 Bundle ID / scheme 整備 → TestFlight  
4. 問題なければ各ストアで本番リリース
