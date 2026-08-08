# 複数科目デプロイ（同一 EC2）

1 インスタンスで科目ごとにプロセスを分けます。

| 科目 | ディレクトリ | `.env` | ポート | URL | systemd |
|---|---|---|---|---|---|
| CDS | `/home/ubuntu/cds` | `APP_PROFILE=CDS` | 8080 | `/cds/` | `cds` |
| SPANISH4 | `/home/ubuntu/spanish4` | `APP_PROFILE=SPANISH4` | 8081 | `/spanish4/` | `spanish4` |
| TOEIC | `/home/ubuntu/toeic` | `APP_PROFILE=TOEIC` | 8082 | `/toeic/` | `toeic` |

科目の切り替えは今も **`backend/.env` の `APP_PROFILE`** です（プロセス単位）。

---

## こちらで用意したもの（リポジトリ）

- `deploy/cds.service.example` / `deploy/spanish4.service.example` / `deploy/toeic.service.example`
- `deploy/apache/multi-subject-proxy-snippet.conf`
- `deploy/setup-multi-subject.sh`（EC2 初回セットアップ: CDS + SPANISH4）
- `deploy/deploy-backend.sh`（CDS + SPANISH4 + TOEIC を更新・再起動）

---

## あなたが EC2 でやること（初回のみ）

### 1. 最新コードを pull

```bash
cd /home/ubuntu/cds
git fetch origin main
git reset --hard origin/main
```

### 2. 初回セットアップスクリプト

```bash
cd /home/ubuntu/cds
bash deploy/setup-multi-subject.sh
```

これで SPANISH4 用クローン・venv・systemd（`cds` / `spanish4`）まで作成します。

### 3. SPANISH4 の DB を置く

ローカルの `exam-SPANISH4.sqlite` を配置:

```bash
# ローカル（Windows）から例:
scp backend/exam-SPANISH4.sqlite ubuntu@<EC2_HOST>:/home/ubuntu/spanish4/backend/
```

EC2 で:

```bash
sudo systemctl restart spanish4
```

### 3b. ヒアリング mp3 を置く（git 外）

```bash
sudo mkdir -p /home/ubuntu/spanish4/backend/audio
# 例: 6101.mp3 → /home/ubuntu/spanish4/backend/audio/6101.mp3
scp path/to/*.mp3 ubuntu@<EC2_HOST>:/home/ubuntu/spanish4/backend/audio/
sudo systemctl restart spanish4
```

別ディレクトリにする場合は `.env` に `EXAM_AUDIO_DIR=/path/to/audio` を設定。

### 4. Apache にパスを追加

`deploy/apache/multi-subject-proxy-snippet.conf` を、既存の SSL VirtualHost  
（例: `/etc/apache2/sites-available/000-default-le-ssl.conf`）に追加。

```bash
sudo a2enmod proxy proxy_http headers ssl rewrite
sudo apache2ctl configtest
sudo systemctl reload apache2
```

### 5. sudoers を更新（Deploy Actions 用）

```bash
sudo visudo -f /etc/sudoers.d/cds-deploy
```

```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart cds, /bin/systemctl is-active cds, /bin/systemctl restart spanish4, /bin/systemctl is-active spanish4, /bin/systemctl restart toeic, /bin/systemctl is-active toeic
```

### 6. 動作確認

```bash
curl -fsS http://127.0.0.1:8080/api/health
curl -fsS http://127.0.0.1:8081/api/health
curl -fsS http://127.0.0.1:8082/api/health
```

ブラウザ:

- https://traveltokio.com/cds/
- https://traveltokio.com/spanish4/
- https://traveltokio.com/toeic/

---

## TOEIC を足すとき（初回）

SPANISH4 と同様です。

```bash
# 例: cds と同リポジトリを別ディレクトリに clone
git clone https://github.com/at-kanno/cds.git /home/ubuntu/toeic
cd /home/ubuntu/toeic
git checkout main
git reset --hard origin/main

# .env
cp backend/.env.example backend/.env
# APP_PROFILE=TOEIC を設定（PORT=8082 任意）

cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# exam-TOEIC.sqlite を配置

sudo cp /home/ubuntu/cds/deploy/toeic.service.example /etc/systemd/system/toeic.service
sudo systemctl daemon-reload
sudo systemctl enable --now toeic
```

Apache に `/toeic/`（8082）を追加し、sudoers に `toeic` を含めてください。  
以降の `main` push では `deploy-backend.sh` が TOEIC も git sync / restart します  
（`toeic.service` がある場合は WorkingDirectory からパスを自動解決）。

---

## 日常運用

| 操作 | コマンド |
|---|---|
| CDS 起動/停止/再起動 | `sudo systemctl start\|stop\|restart cds` |
| SPANISH4 起動/停止/再起動 | `sudo systemctl start\|stop\|restart spanish4` |
| TOEIC 起動/停止/再起動 | `sudo systemctl start\|stop\|restart toeic` |
| 状態 | `sudo systemctl status cds spanish4 toeic` |

`main` への push 後、Deploy が **存在する科目** を更新・再起動します。

### 科目ごとの DB

- CDS: `exam-CDS.sqlite` または従来の `exam.sqlite`
- SPANISH4: `exam-SPANISH4.sqlite`
- TOEIC: `exam-TOEIC.sqlite`
- deploy は sqlite を上書きしません
