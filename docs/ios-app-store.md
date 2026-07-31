# iPhone アプリ登録ガイド（TestFlight / App Store）

対象: `frontend/` Flutter アプリ  
Bundle ID: `jp.co.olivenet.cds`  
Team ID: `RS53Q9YX93`（Xcode 設定）

---

## 前提

- Mac に Xcode 最新版
- [Apple Developer Program](https://developer.apple.com/programs/) 登録（年 $99）
- iPhone 実機（テスト用）

---

## 1. App Store Connect でアプリを作成

1. [App Store Connect](https://appstoreconnect.apple.com/) にログイン
2. **マイ App** → **＋** → **新規 App**
3. 入力例:

| 項目 | 値 |
|---|---|
| プラットフォーム | iOS |
| 名前 | 模擬試験（または CDS） |
| プライマリ言語 | 日本語 |
| バンドル ID | `jp.co.olivenet.cds`（Developer ポータルで事前登録） |
| SKU | 任意（例: `cds-mock-exam-001`） |

---

## 2. Developer ポータルで Bundle ID 確認

1. [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/identifiers/list)
2. **Identifiers** → `jp.co.olivenet.cds` があるか確認
3. なければ **App IDs** → **＋** で登録

---

## 3. Xcode で署名設定

```bash
cd frontend
open ios/Runner.xcworkspace
```

1. 左の **Runner** → **Signing & Capabilities**
2. **Team**: 自分のチーム（`RS53Q9YX93`）
3. **Bundle Identifier**: `jp.co.olivenet.cds`
4. **Automatically manage signing** を ON

---

## 4. Release ビルド（実機 / TestFlight 用）

本番 API を向ける:

```bash
cd frontend
flutter build ios --release \
  --dart-define=API_BASE_URL=https://traveltokio.com/cds
```

実機に直接インストールして試す場合:

```bash
flutter run --release -d <device-id> \
  --dart-define=API_BASE_URL=https://traveltokio.com/cds
```

---

## 5. Archive と TestFlight アップロード

1. Xcode で **Product** → **Destination** → **Any iOS Device (arm64)**
2. **Product** → **Archive**
3. Organizer が開いたら **Distribute App**
4. **App Store Connect** → **Upload**
5. 完了後、App Store Connect → **TestFlight** でビルド処理（10〜30分）

---

## 6. TestFlight テスター

1. App Store Connect → **TestFlight**
2. **内部テスト** または **外部テスト** にグループ作成
3. テスターの Apple ID を追加
4. iPhone に **TestFlight** アプリをインストール → 招待を受けてインストール

---

## 7. App Store 本番公開（任意）

TestFlight 確認後:

1. **App Store** タブ → **＋バージョン**
2. スクリーンショット、説明文、プライバシーポリシー URL を入力
3. ビルドを選択 → **審査に提出**

---

## 表示名について

現在のホーム画面名は **CDS**（`Info.plist` の `CFBundleDisplayName`）。  
複数科目対応アプリとして出す場合は **「模擬試験」** など汎用名への変更を検討してください。

変更箇所:

- `frontend/ios/Runner/Info.plist` → `CFBundleDisplayName`
- `frontend/pubspec.yaml` → `description`（任意）

---

## よくある問題

| 症状 | 対処 |
|---|---|
| 実機でアイコンから起動できない | `--release` ビルドを使う |
| ログインできない | ログイン画面のサーバー URL が `https://traveltokio.com/cds` か確認 |
| Archive がグレーアウト | Destination を実機または Any iOS Device に変更 |
| Signing エラー | Developer ポータルで Bundle ID / 証明書を確認 |
