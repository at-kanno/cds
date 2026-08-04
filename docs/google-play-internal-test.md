# Google Play 内部テスト（Android）

**アプリ名:** 模試システム（CDS） / スペイン語は別アプリ  
**Application ID:** `jp.co.olivenet.cds` または `jp.co.olivenet.spanish4`  
**配布:** Google Play **内部テスト**（TestFlight に相当）

科目を2アプリで配る手順の全体像は [`multi-app-distribution.md`](multi-app-distribution.md) を参照。

---

## 全体の流れ

```
① Google Play 開発者登録（$25）
        ↓
② Play Console でアプリ作成
        ↓
③ 署名用 keystore 作成（Mac、1回）
        ↓
④ AAB ビルド → Play Console にアップロード
        ↓
⑤ 内部テスト → テスターの Gmail を追加
```

---

## ① Google Play 開発者アカウント

1. [Google Play Console](https://play.google.com/console/) に Google アカウントでログイン  
2. 開発者登録（**$25、一度きり**）  
3. 本人確認・利用規約同意（数時間〜数日かかることがある）

---

## ② Play Console でアプリを作成

1. **すべてのアプリ** → **アプリを作成**  
2. 入力例:

| 項目 | 値 |
|---|---|
| アプリ名 | 模試システム |
| デフォルトの言語 | 日本語 |
| アプリ / ゲーム | アプリ |
| 無料 / 有料 | 無料 |

3. **作成**  
4. ダッシュボードの **アプリの設定を完了**（チェックリスト）  
   - プライバシーポリシー URL（必須）  
     - 例: `https://traveltokio.com/cds/` のページ、または会社サイトのポリシー URL  
   - コンテンツのレーティング（アンケート）  
   - ターゲット層  
   - データの安全性（簡易フォーム）

※ 内部テストだけでも、初回はこれらの入力が求められることが多いです。

---

## ③ 署名用 keystore（Mac で1回）

Google Play に載せる AAB は **リリース署名** が必要です。

```bash
cd ~/Projects/CDS
bash scripts/setup-android-signing.sh
```

- パスワードを **必ずメモ**（紛失すると同じキーで更新不可）  
- 生成物:
  - `frontend/android/app/upload-keystore.jks`（**Git に含めない**）
  - `frontend/android/key.properties`（**Git に含めない**）

`key.properties` を編集:

```properties
storePassword=（keytool で設定したパスワード）
keyPassword=（通常同じ）
keyAlias=upload
storeFile=upload-keystore.jks
```

---

## ④ AAB ビルド

```bash
cd ~/Projects/CDS
bash scripts/build-android-aab.sh
```

出力:

```
frontend/build/app/outputs/bundle/release/app-release.aab
```

別 URL 用:

```bash
API_BASE_URL=https://traveltokio.com/toeic bash scripts/build-android-aab.sh
```

---

## ⑤ 内部テストにアップロード

1. Play Console → **模試システム**  
2. 左メニュー **テスト** → **内部テスト**  
3. **新しいリリースを作成**  
4. **App Bundle をアップロード** → 上記 `app-release.aab`  
5. リリース名・リリースノート（例: `初回内部テスト`）  
6. **確認** → **内部テストに公開**

初回は **Play アプリ署名** で Google が署名キーを管理する旨の確認 → **続行** で OK。

---

## ⑥ テスターを追加

1. **内部テスト** → **テスター** タブ  
2. **メーリングリストを作成**（例: `受講生-android`）  
3. テスターの **Gmail / Google アカウントのメール** を追加  
4. **変更を保存**

### テスターへの案内

```
1. 招待メール、または次のリンクから参加:
   Play Console の「内部テスト」→「テスター向けのリンクをコピー」
2. Android 端末でリンクを開く → Play Store から「模試システム」をインストール
3. 起動後、サーバー URL: https://traveltokio.com/cds
   メール・パスワードでログイン
```

**TestFlight との違い:** Android は **Google アカウントのメール** が必要（Apple ID ではない）。

---

## iOS TestFlight との対応

| | iOS | Android |
|---|---|---|
| 配布 | TestFlight 外部テスト | Play 内部テスト |
| テスターの ID | **Apple ID** | **Google アカウント** |
| 審査 | ベータ版審査（1〜2日） | 内部テストは **通常すぐ** |
| 実機（開発者） | あり | なくても AAB ビルド可 |

---

## バージョン更新時

`frontend/pubspec.yaml` のバージョンを上げる:

```yaml
version: 1.0.1+2   # 1.0.1=表示、+2=versionCode（必ず増やす）
```

その後:

```bash
bash scripts/build-android-aab.sh
```

→ Play Console に新しい AAB をアップロード。

---

## トラブルシュート

| 症状 | 対処 |
|---|---|
| `key.properties not found` | `bash scripts/setup-android-signing.sh` |
| アップロードで署名エラー | release keystore でビルドしているか確認 |
| テスターに表示されない | Gmail がリストに入っているか、公開済みか |
| ログインできない | サーバー URL `https://traveltokio.com/cds` |

---

## チェックリスト

- [ ] Play 開発者登録（$25）
- [ ] アプリ「模試システム」作成
- [ ] プライバシーポリシー URL 等の必須項目
- [ ] `setup-android-signing.sh` 実行
- [ ] `build-android-aab.sh` で AAB 生成
- [ ] 内部テストに AAB アップロード
- [ ] テスターの Gmail 追加
- [ ] テスター向けリンク共有
