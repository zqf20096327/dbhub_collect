# TiDB Game Backend

TiDB のトランザクションやロックを、オンライン RPG 風の API で試すための学習用バックエンドです。Rust、Axum、SQLx で実装されています。

プレイヤー作成、アイテム購入、戦闘結果登録、所持品・戦闘履歴・ランキング取得を扱います。特に、同じプレイヤーの所持金を並列に更新したときの悲観的トランザクション、行ロック、競合、リトライを観察しやすい作りになっています。大量データ作成用のシードツールと、並列 HTTP リクエストを送る負荷生成ツールも含みます。

これは完成したゲームサーバーではありません。認証・認可、Web UI、リアルタイム通信、マッチメイキング、課金、本番用インフラなどは対象外です。

## このリポジトリで確認できること

- 複数テーブルをまとめて更新するトランザクション
- `BEGIN PESSIMISTIC` と `SELECT ... FOR UPDATE` による悲観ロック
- 同じ wallet 行へ更新が集中したときの lock contention と hot row
- TiDB が再試行可能と通知したトランザクションエラーのリトライ
- 複合 secondary index を使う履歴・ランキングクエリ
- 大量の battle log を挿入したときの性能と Region の変化
- connection pool、構造化ログ、HTTP レイテンシ
- TiDB/TiKV/PD の障害やスケジューリングを観察するためのワークロード

## アプリケーションの全体像

クライアントから受けたリクエストは、次の順に処理されます。

```text
curl / load generator
        |
        v
Axum routes          HTTP、JSON、入力値の検証
        |
        v
service              ゲームルール、トランザクション、リトライ
        |
        v
repository + SQLx    SQL の実行
        |
        v
TiDB                  データ保存、ロック、分散トランザクション
```

読み取り API は routes から repository を直接呼びます。書き込み API は service でゲームルールとトランザクション境界を管理します。ORM は使わず、実行する SQL とロック対象をコードから追えるようにしています。

主な技術要素は次のとおりです。

| 分類 | 使用技術 |
|---|---|
| HTTP server | Rust 1.97、Tokio、Axum |
| Database access | SQLx の MySQL driver |
| Database | TiDB |
| JSON | Serde |
| Log | tracing、tracing-subscriber |
| Load generation | Rust、Reqwest |

## 最短で起動する

### 1. 必要なもの

- TiDB の接続先と、作成済みのデータベース
- `curl`
- Rust を管理する `rustup`
- Python 3.11 以上
- crates.io へ接続できるネットワーク

TiDB Cloud とローカルの TiDB のどちらでも構いません。通常の MySQL ではなく TiDB が必要です。初期 migration が TiDB 固有の `AUTO_RANDOM` を使用します。

Rust をまだ導入していない場合は、次のコマンドで `rustup` と Cargo を導入します。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
rustup show
```

このリポジトリを開いて Cargo を実行すると、`rust-toolchain.toml` に固定された Rust 1.97.0、rustfmt、Clippy が rustup によって選択されます。

### 2. TiDB の接続情報を設定する

サンプルをコピーします。

```bash
cp .env.example .env
chmod 600 .env
```

`.env` の `DATABASE_URL` を自分の接続情報に置き換えてください。

```dotenv
# TiDB Cloud の例
DATABASE_URL=mysql://USER:PASSWORD@HOST:4000/test?ssl-mode=verify_identity

# TLS を使わないローカル TiDB の例
# DATABASE_URL=mysql://root@127.0.0.1:4000/test
```

パスワードに `@`、`:`、`/` などが含まれる場合は URL encode します。接続案内で CA file が指定されている場合は、絶対パスを追加します。

```dotenv
DATABASE_URL=mysql://USER:PASSWORD@HOST:4000/test?ssl-mode=verify_identity&ssl-ca=/absolute/path/to/ca.pem
```

`.env`、`*.pem`、`*.key` は Git の管理対象外です。本番相当の環境では `.env` を配置せず、secret manager などからプロセス環境変数へ渡してください。

### 3. テストする

TiDB に接続しない単体テストは、サーバーを起動する前に実行できます。

```bash
scripts/cargo-checked.sh test
```

### 4. サーバーを起動する

```bash
scripts/cargo-checked.sh run --release --bin tidb-game-backend
```

起動時に connection pool を作成し、`migrations/` にある未適用の migration を実行してから、既定では `0.0.0.0:8080` で HTTP リクエストを待ち受けます。終了は `Ctrl+C` です。

別の terminal で接続を確認します。

```bash
curl -sS http://127.0.0.1:8080/health
```

成功例です。`tidb_version` の値は接続先によって異なります。

```json
{
  "status": "ok",
  "database": "ok",
  "tidb_version": "8.x.x-TiDB-..."
}
```

## API を一通り試す

以降の例では、サーバーが `http://127.0.0.1:8080` で動いているものとします。返されたプレイヤー ID を `PLAYER_ID` と `OTHER_ID` に入れてください。TiDB の `AUTO_RANDOM` で生成されるため、ID が連番になるとは限りません。

### プレイヤーを2人作る

```bash
curl -sS -X POST http://127.0.0.1:8080/players \
  -H 'content-type: application/json' \
  -d '{"name":"player-001"}'

curl -sS -X POST http://127.0.0.1:8080/players \
  -H 'content-type: application/json' \
  -d '{"name":"player-002"}'
```

プレイヤーには 10,000 gold と season 1 の rating 1,000 が付与されます。

```json
{
  "id": 123456,
  "name": "player-001",
  "gold": 10000,
  "rating": 1000,
  "created_at": "2026-08-24T12:00:00"
}
```

プレイヤーを取得します。

```bash
curl -sS http://127.0.0.1:8080/players/PLAYER_ID
```

### アイテムを購入する

初期 migration では次の商品が登録されます。

| `item_id` | 商品 | 価格 |
|---:|---|---:|
| 10 | Small Potion | 100 gold |
| 20 | Iron Sword | 1,000 gold |
| 30 | Traveler Armor | 2,500 gold |
| 40 | Revival Stone | 5,000 gold |

Iron Sword を1個購入します。

```bash
curl -sS -X POST http://127.0.0.1:8080/players/PLAYER_ID/purchases \
  -H 'content-type: application/json' \
  -d '{"item_id":20,"quantity":1}'
```

```json
{
  "purchase_id": 234567,
  "player_id": 123456,
  "item_id": 20,
  "item_name": "Iron Sword",
  "quantity": 1,
  "inventory_quantity": 1,
  "total_price": 1000,
  "gold_remaining": 9000,
  "transaction_retries": 0
}
```

所持品を取得します。

```bash
curl -sS http://127.0.0.1:8080/players/PLAYER_ID/items
```

### 戦闘結果を登録する

```bash
curl -sS -X POST http://127.0.0.1:8080/battles \
  -H 'content-type: application/json' \
  -d '{"player_id":PLAYER_ID,"enemy_id":OTHER_ID,"result":"win","damage":1250}'
```

報酬と rating の変化量はクライアントから指定せず、サーバーが決めます。

| `result` | gold 報酬 | rating 変化 |
|---|---:|---:|
| `win` | +500 | +25 |
| `loss` | +100 | -10。ただし rating は 0 未満にならない |

```json
{
  "battle_id": 345678,
  "player_id": 123456,
  "result": "win",
  "reward_gold": 500,
  "rating_delta": 25,
  "rating": 1025,
  "season_id": 1,
  "transaction_retries": 0
}
```

直近の戦闘と season 1 のランキングを取得します。

```bash
curl -sS 'http://127.0.0.1:8080/players/PLAYER_ID/battles?limit=100'
curl -sS 'http://127.0.0.1:8080/rankings/1?limit=100'
```

## API リファレンス

| Method | Path | 成功時 | 内容 |
|---|---|---:|---|
| `GET` | `/health` | 200 | DB への接続と TiDB version を確認 |
| `POST` | `/players` | 201 | プレイヤー、wallet、初期 ranking を作成 |
| `GET` | `/players/{player_id}` | 200 | gold と season 1 の rating を含むプレイヤーを取得 |
| `GET` | `/players/{player_id}/items` | 200 | 所持品を item ID 順で取得 |
| `POST` | `/players/{player_id}/purchases` | 200 | アイテムを購入 |
| `POST` | `/battles` | 201 | 戦闘履歴を追加し、gold と season 1 の rating を更新 |
| `GET` | `/players/{player_id}/battles?limit=100` | 200 | 新しい順に戦闘履歴を取得 |
| `GET` | `/rankings/{season_id}?limit=100` | 200 | rating の高い順にランキングを取得 |

主な入力制約は次のとおりです。

- ID はすべて 1 以上
- プレイヤー名は、前後の空白を除いて 1〜64 文字
- 購入数は 1〜1,000
- 戦闘結果は `win` または `loss`
- damage は 0 以上
- 一覧 API の `limit` は 1〜100、省略時は 100

戦闘を登録する `player_id` は既存プレイヤーである必要があります。`enemy_id` は正の値であることだけを検証し、対応するプレイヤーが存在するかは確認しません。

エラーは共通の JSON 形式です。たとえば gold が足りない購入は HTTP 409 を返します。

```json
{
  "code": "insufficient_gold",
  "message": "insufficient gold: available=500, required=1000"
}
```

主な status code は 400 `invalid_request`、404 `not_found`、409 `insufficient_gold` または `conflict`、500 `database_error` または `internal_error` です。すべての HTTP response には追跡用の `x-request-id` header が付き、同じ ID が application log にも記録されます。

## トランザクションとロック

### プレイヤー作成

1つの悲観的トランザクションで `players`、`wallets`、`rankings` を作成します。途中で失敗した場合は3テーブルとも rollback され、プレイヤーの一部だけが残らないようにします。

### アイテム購入

購入は、このリポジトリで並列実行とロックを観察する中心的な処理です。

```text
BEGIN PESSIMISTIC
SELECT gold FROM wallets WHERE player_id = ? FOR UPDATE
残高と商品価格を確認
UPDATE wallets
INSERT または UPDATE player_items
INSERT purchase_logs
COMMIT
```

同じプレイヤーに購入が集中すると、すべてのリクエストが同じ wallet 行をロックしようとします。成功した処理だけが gold、inventory、purchase log をまとめて更新するため、gold は 0 未満になりません。

### 戦闘結果登録

1つの悲観的トランザクションで battle log を追加し、ranking と wallet を更新します。対象プレイヤーが存在しない場合は、先に挿入した battle log も含めて rollback します。

購入と戦闘では、TiDB/MySQL error code `1205`、`1213`、`8028`、`9007` だけを再試行可能として扱います。待ち時間は 10 ms から始まる上限付き exponential backoff です。`TRANSACTION_MAX_RETRIES=3` なら、最初の実行に加えて最大3回再試行します。実際の再試行回数は response の `transaction_retries` と log に残ります。

## データモデル

| Table | 役割 | 主な key / index |
|---|---|---|
| `players` | プレイヤーの名前と作成日時 | `id` は `AUTO_RANDOM` primary key |
| `wallets` | プレイヤーごとの gold | `player_id` が primary key、gold は 0 以上 |
| `shop_items` | 商品マスター | `id` が primary key |
| `player_items` | プレイヤーの所持数 | `(player_id, item_id)` が primary key |
| `purchase_logs` | 購入履歴 | `(player_id, created_at)` index |
| `battle_logs` | 戦闘履歴 | `(player_id, created_at)` index |
| `rankings` | season ごとの rating | `(season_id, player_id)` が primary key、`(season_id, rating DESC)` index |

外部 key は定義していません。書き込みの整合性は service のトランザクションで保ちます。この構成により、アプリケーション側の整合性管理と TiDB のロック挙動を明示的に観察できます。

## 大量データを作る

`seed` binary は API を経由せず、複数行の `INSERT` でプレイヤーと battle log を作ります。既定の batch size は500行です。

```bash
scripts/cargo-checked.sh run --release --bin seed -- \
  --players 100000 \
  --battle-logs 1000000
```

作成するプレイヤーには 10,000 gold と指定 season の ranking が付きます。シードされた rating は 800〜2,800 です。battle log の乱数 seed は既定で42で、`--seed` を指定すると生成に使う疑似乱数列を固定できます。

既存プレイヤーだけを対象に battle log を1,000万件追加する例です。

```bash
scripts/cargo-checked.sh run --release --bin seed -- \
  --players 0 \
  --battle-logs 10000000 \
  --batch-size 500 \
  --season-id 1 \
  --seed 42
```

`--players 0` の場合は、DB に存在するすべてのプレイヤー ID を使います。battle log のシードは性能測定用の直接 INSERT であり、通常の戦闘 API と違って wallet と ranking は更新しません。大量データ投入の途中に失敗した場合、すでに完了した batch は残ります。

利用可能なオプションは次のコマンドでも確認できます。

```bash
scripts/cargo-checked.sh run --release --bin seed -- --help
```

## 並列負荷をかける

`load` binary は起動中の HTTP server にリクエストを送り、成功数、gold 不足数、失敗数、throughput、p50/p95/p99 latency を表示します。

### 同じ wallet 行への100並列購入

初期 gold が 10,000 の新規プレイヤーに、価格1,000の Iron Sword を100回、最大100並列で購入させます。追加の戦闘報酬がなければ成功は最大10件になり、残りは gold 不足になります。

```bash
scripts/cargo-checked.sh run --release --bin load -- \
  --scenario same-player \
  --player-ids PLAYER_ID \
  --item-id 20 \
  --quantity 1 \
  --requests 100 \
  --concurrency 100
```

この結果から、並列度を 1、10、50、100、200 と変えたときの throughput の頭打ちや p95/p99 の増加を比較できます。同じ条件を比較するときは、毎回新しいプレイヤーを用意して初期 gold を揃えてください。

### ゲーム API の mixed workload

```bash
scripts/cargo-checked.sh run --release --bin load -- \
  --scenario mixed \
  --player-ids ID1,ID2,ID3 \
  --requests 10000 \
  --concurrency 100
```

mixed scenario は、指定したプレイヤーからランダムに対象を選び、次の比率でリクエストします。

| 処理 | 比率 |
|---|---:|
| 戦闘結果登録 | 50% |
| アイテム購入 | 20% |
| 戦闘履歴取得 | 15% |
| ランキング取得 | 10% |
| 所持品取得 | 5% |

同じ player ID を繰り返したり、少数の ID だけを渡したりすると、hot row を作れます。大量 battle log の投入前後で履歴 API のレイテンシと実行計画を比べると、データ量と複合 index の影響を確認できます。負荷中に TiDB Dashboard や監視基盤を確認すれば、lock wait、transaction latency、Region split、node 障害時の変化も観察できます。

利用可能な全オプションは次のコマンドで確認できます。

```bash
scripts/cargo-checked.sh run --release --bin load -- --help
```

## 設定

| 環境変数 | 必須 | 既定値 | 内容 |
|---|---|---|---|
| `DATABASE_URL` | yes | なし | TiDB の MySQL protocol 接続 URL |
| `SERVER_ADDR` | no | `0.0.0.0:8080` | HTTP server の listen address |
| `DATABASE_MAX_CONNECTIONS` | no | `32` | connection pool の最大接続数 |
| `DATABASE_MIN_CONNECTIONS` | no | `1` | connection pool の最小接続数 |
| `DATABASE_ACQUIRE_TIMEOUT_SECONDS` | no | `10` | pool から接続を取得する timeout 秒数 |
| `TRANSACTION_MAX_RETRIES` | no | `3` | 再試行可能な transaction error の最大再試行回数 |
| `RUST_LOG` | no | `tidb_game_backend=info` | tracing の filter |

`DATABASE_MIN_CONNECTIONS` が `DATABASE_MAX_CONNECTIONS` より大きい場合は起動に失敗します。SQL を含む詳細ログが必要なら、たとえば `RUST_LOG=tidb_game_backend=debug,sqlx=debug` を指定します。接続 URL 自体は application log に出しません。

## 開発時のコマンド

このリポジトリでは、依存 crate を取得・コンパイル・実行する Cargo command に `scripts/cargo-checked.sh` を使います。

```bash
# format の確認。rustfmt は依存 crate を実行しないため直接 Cargo を使う
cargo fmt --all -- --check

# unit test
scripts/cargo-checked.sh test

# lint
scripts/cargo-checked.sh clippy --all-targets --all-features -- -D warnings

# すべての binary を build
scripts/cargo-checked.sh build --bins
```

wrapper は次の順番で処理します。

1. `Cargo.lock` 内の全 crates.io dependency が公開から14日以上経過し、yank されていないことを crates.io API で確認する
2. `cargo fetch --locked` で lockfile に固定された crate を取得する
3. `cargo --locked --offline` で build、test、Clippy、run などを実行する

検査中の API・network error は安全側に倒して失敗します。`--offline` は Cargo の追加 network access を止めますが、build script や procedural macro を OS level で隔離するものではありません。

依存を変更したときは、コンパイルする前に lockfile と公開日を確認します。

```bash
cargo generate-lockfile
python3 scripts/check_dependency_age.py --minimum-days 14 --suggest
```

直接 dependency は `Cargo.toml` で完全な version に固定し、`Cargo.lock` も commit します。緊急時に公開14日未満の version を許可する `--allow CRATE@VERSION` は公開日の例外だけで、yank 済みや未知の source は許可しません。例外を使う場合は理由を code review に残してください。`cargo-deny` を信頼できる経路で導入済みなら、license、advisory、source policy の追加確認として `cargo deny check` も実行できます。

## ディレクトリ構成

```text
.
├── src/
│   ├── main.rs             HTTP server の entry point
│   ├── config.rs           環境変数の読み込みと検証
│   ├── database.rs         connection pool と migration
│   ├── routes/             HTTP routing、JSON、入力検証
│   ├── service/            transaction とゲームルール
│   ├── repository/         SQL query
│   ├── domain/             response に使うデータ型
│   └── bin/
│       ├── seed.rs         大量データ作成ツール
│       └── load.rs         HTTP 負荷生成ツール
├── migrations/             table、index、初期商品を作る SQL
├── scripts/                dependency 検査付き Cargo wrapper
├── experiments/            実験条件、結果、実行計画、観察結果の記録欄
├── Cargo.toml              Rust package と直接 dependency
├── Cargo.lock              固定された全 dependency
├── rust-toolchain.toml     Rust version と component
├── deny.toml               dependency policy
└── .env.example            ローカル設定のサンプル
```

`experiments/` には、基本トランザクション、悲観ロック、同一プレイヤー競合、secondary index、1,000万件の battle log、hot row、Region split、TiKV node 障害の8テーマを記録するためのファイルがあります。現時点では実験手順と仮説が中心で、実測結果は未記入です。

## 現在の制約

- 認証・認可がなく、API を知っているクライアントは誰でも操作できます。
- season の初期値と戦闘による更新先は season 1 固定です。
- API pagination はなく、履歴とランキングは最大100件です。
- shop item を取得・変更する API はありません。初期商品は migration で固定されます。
- プレイヤー名は一意ではなく、戦闘の `enemy_id` に対する存在確認もありません。
- 外部 key を使わないため、DB へ直接不整合なデータを挿入できます。
- integration test 用の TiDB cluster は自動起動しません。
- migration の自動実行には table を作成できる DB 権限が必要です。

## よくある起動エラー

- `DATABASE_URL is required`: `.env` がリポジトリ直下にあるか、`DATABASE_URL` が設定されているか確認します。
- `failed to connect to TiDB`: host、port、user、password、database 名、TLS mode、IP allowlist を確認します。
- TLS/CA の error: `ssl-mode=verify_identity` と、必要なら `ssl-ca` の絶対パスを確認します。
- `dependency release-age check failed closed`: crates.io への接続、公開から14日未満の crate、yank された crate、未知の registry のいずれかを確認します。
- HTTP 409 `insufficient_gold`: 新しいプレイヤーを作るか、戦闘結果を登録して gold を増やします。
