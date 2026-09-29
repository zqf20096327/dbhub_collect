# Drizzle ORM × TiDB（NestJS）

TypeScript / NestJSからDrizzle ORM（1.0 rc）でTiDBに接続するサンプルアプリケーションです。テナント別データベースのマルチテナント構成で、TiDB固有機能（AUTO_RANDOM、TTL、JSON生成列）を含みます。

起動すると <http://localhost:3000> に実行可能なチュートリアル（`TUTORIAL.md`）が表示されます。このファイルはチュートリアルではなく、**このプロジェクトをDrizzle + TiDBアプリケーションとして開発するときの手順**をまとめています。

## 必要環境

- Node.js 22以上（`process.loadEnvFile()` を使用）
- TiDB（TiDB Cloud Zero / Starter / Dedicated / セルフホスト）。接続ユーザーに `CREATE DATABASE` 権限が必要（テナントDBを作るため）

## セットアップ

```bash
npm install
npm run provision      # TiDB Cloud Zero を作成し .env を生成、テナント DB (tenant_acme, tenant_globex) を作成
npm run migrate        # 全テナント DB にマイグレーションを適用
npm run start:dev      # http://localhost:3000
```

既存のTiDBを使う場合は、`.env.example` を `.env` にコピーして接続情報を書きます。そのうえで `npm run provision` を実行すると、テナントDBだけが作成されます（`.env` があればインスタンスは作りません）。

`.env` の内容：

| 変数 | 用途 |
| --- | --- |
| `DATABASE_URL` | 接続先。**開発用テナント（`tenant_acme`）のDBを指す**。TLSは `mysql2` のオプションで有効にするためURLにパラメータは不要 |
| `TENANTS` | テナント名のカンマ区切り。DB名は `tenant_<name>` |
| `TIDB_EXPIRES_AT` / `TIDB_CLAIM_URL` | TiDB Cloud Zeroの失効日時とclaim URL（UI表示用） |

ランタイム（NestJS）は `DATABASE_URL` のホスト・認証情報だけを使い、DB名はリクエストの `x-tenant-id` から決めます。

## フォルダ構成

```text
.
├── src/
│   ├── main.ts                # NestJS 起動。ValidationPipe を登録
│   ├── app.module.ts          # モジュール構成、テナントミドルウェアの適用範囲
│   ├── env.ts                 # .env の読み込み、DATABASE_URL の分解、テナント名 → DB 名
│   ├── provision.ts           # TiDB Cloud Zero の作成と .env 生成、テナント DB 作成（npm run provision）
│   ├── migrate.ts             # 全テナント DB への migrate()（npm run migrate）
│   ├── db/
│   │   ├── schema.ts          # テーブル定義と defineRelations（唯一の定義元）
│   │   ├── client.ts          # mysql2 プール（TLS、プール設定）+ drizzle()。生 SQL 用の rows<T>()
│   │   ├── db.service.ts      # テナント DB ごとの Drizzle インスタンスを生成・キャッシュ・破棄
│   │   └── db.module.ts
│   ├── tenant/                # x-tenant-id ヘッダ → AsyncLocalStorage（currentTenant()）
│   ├── common/                # BigInt → 文字列の interceptor、ParseBigIntPipe
│   ├── users/  posts/         # NestJS 標準のリソース構成（module / controller / service / dto）
│   ├── steps/                 # チュートリアルの各ステップ（表示されるコード = 実行されるコード）
│   └── tutorial/              # TUTORIAL.md の描画とステップ実行 API
├── migrations/                # drizzle-kit generate の出力（SQL + snapshot.json）。TiDB 固有 DDL は手編集
├── drizzle.config.ts          # drizzle-kit の設定（スキーマの場所、出力先、任意で接続先）
├── TUTORIAL.md                # チュートリアル本文
├── Dockerfile  .dockerignore  # Lambda 用コンテナ（Lambda Web Adapter 入り。他のコンテナ環境でもそのまま動く）
├── template.yaml  samconfig.toml  # AWS SAM（Lambda コンテナイメージ + Function URL）
├── .env.example
├── nest-cli.json  tsconfig.json  tsconfig.build.json
└── package.json
```

## 開発作業のコマンド

### npm scripts

| コマンド | 内容 |
| --- | --- |
| `npm run start:dev` | 開発サーバ（ファイル変更で再起動） |
| `npm run build` / `npm start` | tscビルド / ビルド済みを起動 |
| `npm run provision` | TiDB Cloud Zeroの作成と `.env` 生成、テナントDBの作成 |
| `npm run migrate` | `TENANTS` の全DBに `migrations/` を適用（アプリ内のmigratorを使う。CLI不要） |
| `npm run generate` | `drizzle-kit generate` と同じ |

### drizzle-kit

drizzle-kitは `drizzle.config.ts` を読みます。`generate` はスキーマとスナップショットだけを見るのでDB接続は不要です。DBに繋ぐコマンドは `.env` の `DATABASE_URL`（開発用テナント `tenant_acme`）に接続します。

| コマンド | 用途 | 備考 |
| --- | --- | --- |
| `npx drizzle-kit generate --name <name>` | スナップショットとの差分からマイグレーションSQLを生成 | DB接続不要。リネームは対話で判定する |
| `npx drizzle-kit check` | スナップショットの整合性を検査 | DB接続不要。CIに組み込める |
| `npx drizzle-kit migrate` | 未適用のマイグレーションを適用 | 1テナントのみ。全テナントは `npm run migrate` |
| `npx drizzle-kit studio` | ブラウザでデータを閲覧・編集 | `DATABASE_URL` のテナントが対象 |
| `npx drizzle-kit pull` | 実DBから `schema.ts` を逆生成 | 既存DBの取り込み用 |
| `npx drizzle-kit push` | スキーマを直接DBに反映 | **使わない**。手編集したDDL（AUTO_RANDOM / TTL）を上書きしようとする |

### スキーマを変更する手順

1. `src/db/schema.ts` を編集する。参照箇所の型エラーはこの時点で出る（生成ステップは無い）
2. `npx drizzle-kit generate --name <name>` でマイグレーションSQLを生成する
3. `migrations/<timestamp>_<name>/migration.sql` を確認する
   - カラムのリネームは `generate` の対話で「rename」を選ぶと `RENAME COLUMN` になる
   - AUTO_RANDOM、TTLなどのTiDB固有DDLはこの段階に手編集で付与する（`[手編集]` コメントを付ける）。手編集はスナップショットに影響しないため、次回の `generate` で差分にならない
4. `npm run migrate` で全テナントに適用する

### TiDB固有DDLとスキーマ宣言の対応

| 機能 | `schema.ts` | マイグレーションSQL | 例 |
| --- | --- | --- | --- |
| 生成列 | `.generatedAlwaysAs(sql\`...\`, { mode: 'virtual' })` | drizzle-kitが生成する（手編集不要） | `users.plan` |
| AUTO_RANDOM主キー | `.autoincrement()` | `AUTO_RANDOM` に手編集 | `events.id` |
| TTL | 宣言しない | `TTL = \`created_at\` + INTERVAL 7 DAY TTL_ENABLE = 'ON'` を手編集 | `events` |

AUTO_RANDOM列を `.autoincrement()` と宣言しておくと、insertの型で `id` が省略可能になります。ただし実際のinsertでは `id: autoRandomId()` を明示し、`$returningId()` は使いません。

初回マイグレーション：`migrations/20260828022858_init/migration.sql`

## 接続と設定

- Drizzleは `mysql2` のプールをそのまま使う。設定は `src/db/client.ts`
  - `ssl: { minVersion: 'TLSv1.2', rejectUnauthorized: true }`: TiDB Cloudの公開エンドポイントは公的CAなのでCAファイルは不要
  - `connectionLimit: 5`, `idleTimeout: 300_000`: テナントごとのプール
  - プールはコールバック版 `mysql2` の `createPool` で作る。Drizzle 1.0 rcのmysql2ドライバは `client.config` を参照するため、`mysql2/promise` のプールや `connection` オプション指定では起動時に落ちる
- BIGINT列はスキーマで `{ mode: 'bigint' }` にし、JavaScriptの `bigint` で扱う（AUTO_RANDOMの値は2^53を超える）
- `createPool` に `supportBigNumbers: true, bigNumberStrings: false` を明示する。無いとmysql2が2^53超のBIGINTを丸めた `number` で返し、Drizzleがそれを `BigInt` にするため、型は正しいのに値が壊れる。`bigNumberStrings: true` にすると `insertId` が文字列になり、AUTO_RANDOM行の `$returningId()` がメモリ枯渇で落ちる
- Relational Queriesの `with`（ネスト取得）は `LEFT JOIN LATERAL` を生成するためTiDBでは使えない。ネスト取得はselectビルダーと複数クエリ、または相関サブクエリ + `JSON_ARRAYAGG` で組む
- 生SQLの `db.execute()` は戻り型が `ResultSetHeader` 固定なので、SELECTには `rows<T>()`（`src/db/client.ts`）で型を付ける

## REST API

`x-tenant-id` ヘッダでテナントを指定します。

```bash
curl -H 'x-tenant-id: acme' -H 'content-type: application/json' \\
  -d '{"name":"山田","email":"yamada@example.com","attributes":{"plan":"pro"}}' localhost:3000/api/users
curl -H 'x-tenant-id: acme' 'localhost:3000/api/posts?published=true&take=20'
```

| メソッドとパス | 内容 |
| --- | --- |
| `GET /api/users`, `GET /api/users/:id`, `POST /api/users` | ユーザー |
| `GET /api/posts`, `GET /api/posts/:id`, `POST /api/posts`, `DELETE /api/posts/:id` | 投稿（`published` / `take` / `cursor` で絞り込み） |
| `POST /api/posts/:id/comments` | コメント追加 |
| `GET /api/status`, `POST /api/steps/:id` | チュートリアル用 |

## デプロイ（AWS Lambda + SAM）

Lambda Web Adapterを使い、NestJSをHTTPサーバのままLambda（コンテナイメージ）で動かします。IaCは `template.yaml` と `samconfig.toml` の2ファイルだけです。接続先の `DATABASE_URL` はSAMのパラメータで渡します（Lambdaのファイルシステムは `/tmp` 以外読み取り専用のため、コンテナ内でZeroを作る方式は使いません）。

### 前提

- AWS CLIの認証（管理者相当。初回にECR、S3、IAMロールを作る）
- SAM CLI（1.165で確認）
- Docker。ソケットが `/var/run/docker.sock` に無い環境（Rancher Desktopなど）では `DOCKER_HOST` を指定する。例：`unix://$HOME/.rd/docker.sock`

### 手順

```bash
npm run migrate          # マイグレーションは手元から適用しておく
sam build                # Dockerfile から arm64 イメージをビルド
sam deploy --parameter-overrides "DatabaseUrl=$(grep '^DATABASE_URL' .env | cut -d'"' -f2)"
# 出力の TutorialUrl を開く
```

更新も同じ `sam build && sam deploy` です。イメージのビルドに数分かかります。

### 構成と注意点

- 初回はSAMがS3バケット、ECRリポジトリ、実行ロールを作る（`samconfig.toml` の `resolve_s3` / `resolve_image_repos`）
- Function URLは認証なし（`AuthType: NONE`）の公開URL。ホスト名はランダムで、データは使い捨てのZeroインスタンス。不要になったら削除する
- `ReservedConcurrentExecutions: 1` で同時実行を1に絞り、コネクションプールと状態を1インスタンスに閉じている。数十分アイドルするとインスタンスは破棄されるが、`DATABASE_URL` は環境変数なので再起動後も同じDBに接続する
- `02-migrate` はアプリ内のmigratorなのでLambda上でもそのまま動く（Prisma版のようなCLI起動の工夫は不要）
- `Architectures: [arm64]`。Intel Macで `sam build` する場合は `template.yaml` を `x86_64` に変える
- `.env` はイメージに含めない（`.dockerignore`）

### 削除

```bash
sam delete
```

TiDB Cloud Zeroのインスタンスは30日で自動失効するため、削除操作は不要です。

## トラブルシューティング

| 症状 | 対処 |
| --- | --- |
| 起動時に `Cannot set properties of undefined (setting 'supportBigNumbers')` | `drizzle()` に `mysql2/promise` のプールか `connection` オプションを渡している。コールバック版 `mysql2` の `createPool` で作ったプールを `client` に渡す |
| `You have an error in your SQL syntax ... near "(select ..."` | Relational Queriesの `with` が生成する `LEFT JOIN LATERAL` をTiDBが解釈できない。selectビルダーで組む（`src/posts/posts.service.ts` を参照） |
| `Field 'id' doesn't have a default value` | AUTO_RANDOM列に `DEFAULT` を渡している。`values()` で `id: autoRandomId()` を明示する |
| idが `bigint` なのに値が丸められている（末尾が `000` や重複） | `createPool` に `supportBigNumbers: true` が無い。`src/db/client.ts` を参照 |
| `$returningId()` でメモリ枯渇 | AUTO_RANDOM列のinsertで呼んでいる（`insertId` が文字列になる）。AUTO_RANDOMテーブルでは `$returningId()` を使わない |
| `drizzle-kit generate` が「No schema changes」なのにDBと合わない | 手編集したSQLが未適用か、`push` で上書きされた。`__drizzle_migrations` と `SHOW CREATE TABLE` を確認する |
| TiDB Cloud Zeroに接続できなくなった | 30日で失効している。`rm .env && npm run provision && npm run migrate`。Lambdaにデプロイしている場合は `sam deploy` で新しい `DatabaseUrl` を渡す |
