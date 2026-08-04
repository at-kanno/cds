# 複数科目デプロイ（同一 EC2）

1 インスタンスで科目ごとにプロセスを分けます。

| 科目 | ディレクトリ | `.env` | ポート | URL | systemd |
|---|---|---|---|---|---|
| CDS | `/home/ubuntu/cds` | `APP_PROFILE=CDS` | 8080 | `/cds/` | `cds` |
| SPANISH4 | `/home/ubuntu/spanish4` | `APP_PROFILE=SPANISH4` | 8081 | `/spanish4/` | `spanish4` |

科目の切り替えは今も **`backend/.env` の `APP_PROFILE`** です（プロセス単位）。

---

## こちらで用意したもの（リポジトリ）

- `deploy/cds.service.example` / `deploy/spanish4.service.example`
- `deploy/apache/multi-subject-proxy-snippet.conf`
- `deploy/setup-multi-subject.sh`（EC2 初回セットアップ）
- `deploy/deploy-backend.sh`（CDS + SPANISH4 を更新・再起動）

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

### 4. Apache に `/spanish4/` を追加

`deploy/apache/multi-subject-proxy-snippet.conf` の内容を、既存の SSL VirtualHost  
（例: `/etc/apache2/sites-available/000-default-le-ssl.conf`）に追加。

```bash
sudo a2enmod proxy proxy_http headers ssl rewrite
sudo apache2ctl configtest
sudo systemctl reload apache2
```

`/cds/` が既にあれば SPANISH4 部分だけ足せば十分です。

### 5. sudoers を更新（Deploy Actions 用）

```bash
sudo visudo -f /etc/sudoers.d/cds-deploy
```

```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart cds, /bin/systemctl is-active cds, /bin/systemctl restart spanish4, /bin/systemctl is-active spanish4
```

### 6. 動作確認

```bash
curl -fsS http://127.0.0.1:8080/api/health
curl -fsS http://127.0.0.1:8081/api/health
```

ブラウザ:

- https://traveltokio.com/cds/
- https://traveltokio.com/spanish4/

---

## 日常運用

| 操作 | コマンド |
|---|---|
| CDS 起動/停止/再起動 | `sudo systemctl start\|stop\|restart cds` |
| SPANISH4 起動/停止/再起動 | `sudo systemctl start\|stop\|restart spanish4` |
| 状態 | `sudo systemctl status cds spanish4` |

`main` への push 後、Deploy が **両方** を更新・再起動します  
（`/home/ubuntu/spanish4` が存在するとき）。

### 科目ごとの DB

- CDS: `exam-CDS.sqlite` または従来の `exam.sqlite`
- SPANISH4: `exam-SPANISH4.sqlite`
- deploy は sqlite を上書きしません

---

## 新規科目（TOEIC など）を足すとき

1. `spanish4` と同様にディレクトリ・`.env`・systemd・Apache パスを追加
2. `deploy-backend.sh` と sudoers にサービス名を追加
