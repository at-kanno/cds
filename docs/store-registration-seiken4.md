# 西検４級 / CDS — ストア登録チェックリスト（案A）

既に揃っているもの:

- バックエンド: `https://traveltokio.com/spanish4`（HTTPS 稼働）
- Android flavor: `spanish4` → `jp.co.olivenet.spanish4` / ホーム画面名 **西検４級**
- Android アイコン: `frontend/android/app/src/spanish4/res/mipmap-*/`
- iOS アイコンセット: `AppIcon-Spanish4.appiconset`
- 1024px 原画: `frontend/branding/spanish4/`
- 詳細コマンド: `docs/multi-app-distribution.md`

---

## いまやること（ストア側・先に枠を作る）

### Apple（西検４級・新規）

1. [Developer → Identifiers](https://developer.apple.com/account/resources/identifiers/list)  
   - Bundle ID: **`jp.co.olivenet.spanish4`**（無ければ作成）
2. [App Store Connect](https://appstoreconnect.apple.com/) → **新規 App**
   - 名前: **西検４級**
   - プライマリ言語: 日本語
   - Bundle ID: `jp.co.olivenet.spanish4`
   - SKU: 例 `seiken4-001`
3. アプリのアイコン（1024）は後からビルドでも可。ストア用は  
   `frontend/branding/spanish4/store_icon_1024.png`

CDS は既存の `jp.co.olivenet.cds` を継続利用。

### Google Play（西検４級・新規）

1. [Play Console](https://play.google.com/console/) → **アプリを作成**
2. アプリ名: **西検４級**
3. Application ID（パッケージ名）は AAB 側で  
   **`jp.co.olivenet.spanish4`**（後から変更不可）
4. 内部テストトラックを用意

CDS 用アプリ（`jp.co.olivenet.cds`）とは **別アプリ** として作成。

---

## ビルド（Mac で git pull してから）

```bash
cd ~/Projects/CDS
git pull origin main
cd frontend
```

### Android（西検４級）

署名 (`android/key.properties` + keystore) があること。

```bash
bash scripts/build_android.sh spanish4
# → build/app/outputs/bundle/spanish4Release/app-spanish4-release.aab
```

Play Console の **西検４級** → 内部テストへアップロード。

### Android（CDS・更新する場合）

```bash
bash scripts/build_android.sh cds
```

### iOS（西検４級）

初回は Xcode で次を設定（Signing / Bundle ID / 表示名 / アイコン）:

| 項目 | 値 |
|---|---|
| Bundle ID | `jp.co.olivenet.spanish4` |
| Display Name | `西検４級` |
| App Icon | `AppIcon-Spanish4` |
| Team | 既存（例: RS53Q9YX93） |

```bash
bash scripts/build_ios.sh spanish4
# または
flutter build ipa --release \
  --dart-define=APP_FLAVOR=spanish4 \
  --dart-define=APP_TITLE=スペイン語検定4級 \
  --dart-define=API_BASE_URL=https://traveltokio.com/spanish4
```

Transporter でアップロード → TestFlight（外部テストは審査あり）。

ログイン画面のサーバー URL は **出ません**（本番 URL 埋め込み）。

---

## 接続先の対応

| アプリ | API |
|---|---|
| 西検４級 | `https://traveltokio.com/spanish4` |
| CDS | `https://traveltokio.com/cds` |

DB はサーバー側で科目分離済み（利用者が混ざらない）。

---

## 公開前チェック

- [ ] `curl -fsS https://traveltokio.com/spanish4/api/health`
- [ ] Android AAB を内部テスターでインストール → ログイン・出題
- [ ] iOS TestFlight で同様
- [ ] ホーム画面名が **西検４級**、アイコンがスペイン語用
- [ ] CDS アプリと **両方インストールできる**（ID が違うので共存可）
