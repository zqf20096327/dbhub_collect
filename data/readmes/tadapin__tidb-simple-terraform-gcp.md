# TiDB Cloud Dedicated on GCP — Terraform サンプル

Terraform で **TiDB Cloud Dedicated クラスタ** を GCP（既定: 東京 `asia-northeast1`）に 1 つ作る、最小構成のサンプルです。root module は 1 つだけで、`terraform apply` 以外に必要な操作はありません。

```
terraform (tidbcloud provider)
        │
        │  data "tidbcloud_projects"      ← プロジェクト「名」から ID を解決
        ▼
Project (例: my-project)
        │
        ├─ Network container  (GCP asia-northeast1, 172.16.0.0/19)  ← VPC を先に確保
        │        │
        │        ▼
        └─ TiDB Cloud Dedicated cluster
             ├─ TiDB   4C16G × 1        ← SQL layer
             ├─ TiKV   4C16G × 3 / 200GiB (Basic)   ← row store
             └─ TiFlash 8C64G × 2 / 200GiB (Basic)  ← 任意 (enable_tiflash = true)
```

数値の project ID を調べる必要はありません。コンソールに表示されている
**プロジェクト名**を `project_name` に書けば、`tidbcloud_projects` データソース経由で
ID を解決します。ネットワークコンテナ（TiDB Cloud 側 VPC）も明示的に作るので、
CIDR を自分で決められます。

> **注意**: ネットワークコンテナがない場合の削除は `terraform destroy` で可能ですが、ネットワークコンテナがある場合は`bash scripts/destroy.sh` してください（素の `terraform destroy` は[ネットワークコンテナが削除できない](#ネットワークコンテナは削除できない)ため失敗します）。
> Webコンソールから Pause も可能です。

## 前提

- Terraform >= 1.5
- TiDB Cloud の API キー（[TiDB Cloud console](https://tidbcloud.com) > Organization Settings > API Keys）
- 接続確認用に `mysql` クライアント（任意）
- `scripts/*.sh` 用に `curl` と `python3`（任意）

## 使い方

### 1. スペック確認（任意）

リージョンと node spec の**実際に有効な値**を API から一覧します。

```bash
export TIDBCLOUD_PUBLIC_KEY=...  TIDBCLOUD_PRIVATE_KEY=...
bash scripts/list_specs.sh
# 別リージョンを見たい場合:
REGION_ID=gcp-us-west1 bash scripts/list_specs.sh
```

### 2. 変数の設定

```bash
cp terraform.tfvars.example terraform.tfvars
# terraform.tfvars に API キーと root_password を記入
```

`terraform.tfvars` は `.gitignore` 済みです。

### 3. クラスタ作成

```bash
terraform init
terraform plan
terraform apply        # 作成完了まで 30 分ほどかかります
terraform output
```

### 4. 接続確認

```bash
terraform output mysql_connect_command    # そのまま貼れる mysql コマンド

# もしくはスクリプトで疎通確認
export TIDB_HOST=$(terraform output -json public_endpoint | python3 -c 'import json,sys;print(json.load(sys.stdin)["host"])')
export TIDB_PASSWORD=...                  # terraform.tfvars の root_password
bash scripts/connect.sh
```

> TLSを利用するためにはWebコンソールからca.pemのダウンロードが必要です。

### 5. 後片付け

```bash
terraform destroy
```

または

```bash
bash scripts/destroy.sh
```

このスクリプトはクラスタのみを destroy します。
 `terraform destroy` はネットワークコンテナの削除で失敗するため、ネットワークコンテナを含む場合はこのスクリプトを利用します。

## 変数リファレンス

| 変数 | 既定値 | 説明 |
|---|---|---|
| `tidbcloud_public_key` | (必須) | TiDB Cloud API public key |
| `tidbcloud_private_key` | (必須) | TiDB Cloud API private key |
| `project_name` | (必須) | プロジェクト**名**。ここから ID を解決 |
| `project_page_size` | `100` | プロジェクト名解決時の取得件数。組織のプロジェクトが多い場合は増やす |
| `create_network_container` | `true` | ネットワークコンテナを明示的に作るか |
| `network_cidr` | `172.16.0.0/19` | ネットワークコンテナの CIDR |
| `display_name` | `tidb-dedicated-sample` | クラスタ表示名 |
| `region_id` | `gcp-asia-northeast1` | リージョン ID |
| `root_password` | (必須) | root パスワード |
| `tidb_node_spec_key` | `4C16G` | TiDB ノードスペック |
| `tidb_node_count` | `1` | TiDB ノード数（HA なら 2 以上） |
| `tikv_node_spec_key` | `4C16G` | TiKV ノードスペック |
| `tikv_node_count` | `3` | TiKV ノード数（3 の倍数） |
| `tikv_storage_gi` | `200` | TiKV ストレージ／ノード (GiB) |
| `storage_type` | `Basic` | ストレージ種別 |
| `enable_tiflash` | `false` | TiFlash を追加するか |
| `tiflash_node_spec_key` | `8C64G` | TiFlash ノードスペック |
| `tiflash_node_count` | `2` | TiFlash ノード数 |
| `tiflash_storage_gi` | `200` | TiFlash ストレージ／ノード (GiB) |

### GCP `asia-northeast1` で選択できる node spec

| コンポーネント | nodeSpecKey | ストレージ (min/default/max GiB) | storage type |
|---|---|---|---|
| TiDB | `2C8G` `4C16G` `8C16G` `8C32G`(既定) `16C32G` `16C64G` `32C64G` `32C128G` `64C128G` | 指定不要 | — |
| TiKV | `2C8G` `4C16G` `8C32G`(既定) `8C64G` `16C64G` `32C128G` `64C256G` | 200 / 500 / 500〜4096 | `Basic` のみ |
| TiFlash | `8C64G` `16C128G`(既定) `32C128G` | 200 / 500 / 2048〜6144 | `Basic` のみ |

## プロジェクト名の解決とネットワークコンテナ

### プロジェクト名 → ID

`project.tf` が `tidbcloud_projects` データソースで一覧を引き、`project_name` に
一致するものの ID を取り出します。0 件または複数一致した場合は、apply 前に
**候補のプロジェクト名一覧つきでエラー**にします（precondition）。

```
Could not uniquely resolve project_name = "no-such-project".
Matched 0 project(s) out of 46 visible to this API key.
Available project names: 3layerProject, DEMO, ...
```

### ネットワークコンテナ

ネットワークコンテナは **プロジェクト × リージョンごとに 1 つ**の、TiDB Cloud 側 VPC です。VPC ピアリングで自社 VPC と接続する際、レンジが衝突しないように指定します。`cluster.tf` の `depends_on` で順序を保証しています。

**GCP の CIDR 制約**:

| 項目 | 制約 |
|---|---|
| プレフィックス長 | **`/19` または `/20`**（それ以外は `CIDR block size must be between /19 and /20.`） |
| レンジ | `10.0.0.0/8` と `172.16.0.0/12` のみ。**`192.168.0.0/16` は拒否**（パブリック IP も不可） |
| 重複 | 同一プロジェクト × リージョンで既存 CIDR と重なると `CIDR already exists.` |

`network_cidr` にはこの 3 つを反映した `validation` を付けてあります。
既にそのプロジェクト × リージョンにコンテナがある場合は、作成をスキップします:

```bash
terraform apply -var create_network_container=false
```

既存コンテナの確認（`projectId` を付けないとデフォルトプロジェクト分しか返りません）:

```bash
curl -sS --digest -u "$TIDBCLOUD_PUBLIC_KEY:$TIDBCLOUD_PRIVATE_KEY" \
  "https://dedicated.tidbapi.com/v1beta1/networkContainers?projectId=<PROJECT_ID>"
```

### ネットワークコンテナは削除できない

> **一度 `ACTIVE` になったネットワークコンテナは削除できません。**
> 削除する場合はサポートまでお知らせください。

TiDB Cloud は払い出した VPC を再利用のため保持し続けます。

このためネットワークコンテナを含む**`terraform destroy` は必ずコンテナの削除で失敗します**。クラスタのみを削除する場合は、`scripts/destroy.sh` を使ってください。

## TiFlash（HTAP）を使う

```bash
terraform apply -var enable_tiflash=true
```

作成後、列指向レプリカを張ってから分析クエリを流します。

```sql
ALTER TABLE <db>.<table> SET TIFLASH REPLICA 1;
SELECT * FROM information_schema.tiflash_replica;   -- AVAILABLE=1, PROGRESS=1 を待つ
EXPLAIN SELECT col, COUNT(*) FROM <db>.<table> GROUP BY col;  -- cop[tiflash] が出れば OK
```

## 注意点

- **`storage_type` は GCP では `Basic` のみ**です。`Standard` / `Performance` / `Plus` は AWS 向けで、
  GCP で指定すると作成に失敗します。
- **TiKV は 3 ノード以上（3 の倍数）／200 GiB 以上**が必須です。
- **`root_password` は write-only** です。API から読み戻せないため
  `lifecycle { ignore_changes = [root_password] }` を設定しています。
  コンソールでパスワードを変更しても Terraform 側は追随しません（逆も同様）。
- **ネットワークコンテナはプロジェクト × リージョンに 1 つだけ**です。既にある状態で
  作ろうとすると `CIDR already exists.` になります。`create_network_container = false` にしてください。
- **ネットワークコンテナは一度 `ACTIVE` になると削除できません。** そのため
  `terraform destroy` は失敗します。その場合は `scripts/destroy.sh` を使ってください
- クラスタ作成は 30 分程度かかります。`terraform apply` はその間ブロックします。

## ファイル構成

| パス | 役割 |
|---|---|
| `providers.tf` | `tidbcloud` provider の宣言 |
| `variables.tf` | 入力変数（バリデーション付き） |
| `project.tf` | プロジェクト名 → ID の解決（`tidbcloud_projects` データソース） |
| `network.tf` | `tidbcloud_dedicated_network_container`（TiDB Cloud 側 VPC） |
| `cluster.tf` | `tidbcloud_dedicated_cluster` 本体 |
| `outputs.tf` | project_id / network_container / cluster_id / エンドポイント / 接続コマンド |
| `terraform.tfvars` | 実値（gitignore 対象） |
| `terraform.tfvars.example` | 記入テンプレート |
| `scripts/list_specs.sh` | リージョン・node spec の一覧取得 |
| `scripts/connect.sh` | mysql での疎通確認 |
| `scripts/destroy.sh` | クラスタのみ destroy（コンテナは削除できないため） |

## 参考

- [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)
- [TiDB Cloud Dedicated API (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated)
- [TiDB Cloud 料金](https://www.pingcap.com/pricing/)
