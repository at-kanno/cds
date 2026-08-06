# TOEIC — ストア登録 / TestFlight チェックリスト

既に揃っているもの:

- バックエンド: `https://traveltokio.com/toeic`（`/api/health` OK）
- Android flavor: `toeic` → `jp.co.olivenet.toeic` / ホーム画面名 **TOEIC**
- iOS アイコンセット: `AppIcon-Toeic.appiconset`
- 1024px 原画: `frontend/branding/toeic/app_icon_1024.png`

---

## いまやること（ストア側・先に枠を作る）

### Apple（TOEIC・新規）

1. [Developer → Identifiers](https://developer.apple.com/account/resources/identifiers/list)  
   - Bundle ID: **`jp.co.olivenet.toeic`**（無ければ作成）
2. [App Store Connect](https://appstoreconnect.apple.com/) → **新規 App**
   - 名前: **TOEIC**（または希望のストア名）
   - プライマリ言語: 日本語
   - Bundle ID: `jp.co.olivenet.toeic`
   - SKU: 例 `toeic-001`

### Google Play（任意・後で可）

- 別アプリとして作成、package: `jp.co.olivenet.toeic`

---

## iOS IPA（TestFlight）

```bash
cd ~/Projects/CDS/frontend
bash scripts/build_ios.sh toeic
```

成果物:

```
build/ios/ipa/TOEIC.ipa
```

| 項目 | 値 |
|---|---|
| Bundle ID | `jp.co.olivenet.toeic` |
| 表示名 | TOEIC |
| Version / Build | 1.0.0 (1)（初回デフォルト） |
| API | `https://traveltokio.com/toeic`（画面には出ない） |

Transporter で **＋ → TOEIC.ipa** → 配信  
→ App Store Connect の **TOEIC** アプリ → **配信 / TestFlight** → iOS ビルドで **1.0.0 (1)** を確認。

---

## Android AAB（任意）

```bash
bash scripts/build_android.sh toeic
# → build/app/outputs/bundle/toeicRelease/app-toeic-release.aab
```

署名: CDS と同じ `key.properties` / upload keystore で可（アプリが別なので初回アップロード時に Play アプリ署名を有効化）。
