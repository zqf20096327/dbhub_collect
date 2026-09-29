# Prisma 7 × TiDB（NestJS）

TypeScript / NestJSからPrisma 7でTiDBに接続するサンプルアプリケーションです。テナント別データベースのマルチテナント構成で、TiDB固有機能（AUTO_RANDOM、TTL、JSON生成列）を含みます。

起動すると <http://localhost:3000> に実行可能なチュートリアル（`TUTORIAL.md`）が表示されます。このファイルは、チュートリアルではなく**このプロジェクトをPrisma + TiDBアプリケーションとして開発するときの手順**をまとめています。

## 必要環境

- Node.js 22以上（`process.loadEnvFile()` を使用）
- TiDB（TiDB Cloud Zero / Starter / Dedicated / セルフホスト）。接続ユーザーに `CREATE DATABASE` 権限が必要（テナントDBとPrismaのshadow DBを作るため）

## セットアップ

```bash
npm install            # postinstall は無い。Prisma Client は下の provision / generate で生成する
npm run provision      # TiDB Cloud Zero を作成し .env を生成、テナント DB (tenant_acme, tenant_globex) を作成
npm run migrate        # 全テナント DB にマイグレーションを適用
npm run start:dev      # http://localhost:3000
```

既存のTiDBを使う場合は、`.env.example` を `.env` にコピーして接続情報を書きます。そのうえで `npm run provision` を実行すると、テナントDBだけが作成されます（`.env` があればインスタンスは作りません）。

`.env` の内容：

| 変数 | 用途 |
| --- | --- |
| `DATABASE_URL` | Prisma CLIが使う接続先。**開発用テナント（`tenant_acme`）のDBを指す**。TiDB Cloudでは `?sslaccept=strict` を付ける |
| `TENANTS` | テナント名のカンマ区切り。DB名は `tenant_<name>` |
| `TIDB_EXPIRES_AT` / `TIDB_CLAIM_URL` | TiDB Cloud Zeroの失効日時とclaim URL（UI表示用） |

ランタイム（NestJS）は `DATABASE_URL` のホスト・認証情報だけを使い、DB名はリクエストの `x-tenant-id` から決めます。

## フォルダ構成

```text
.
├── prisma/
│   ├── schema.prisma          # モデル定義（唯一の定義元）。DDL と Prisma Client の両方がここから生成される
│   └── migrations/            # prisma migrate dev が生成した SQL。TiDB 固有 DDL は手編集（[手編集] コメント付き）
├── prisma.config.ts           # Prisma 7 の CLI 設定（スキーマの場所、migrations の場所、CLI 用の接続先）
├── src/
│   ├── main.ts                # NestJS 起動。ValidationPipe を登録
│   ├── app.module.ts          # モジュール構成、テナントミドルウェアの適用範囲
│   ├── env.ts                 # .env の読み込み、DATABASE_URL の分解、テナント名 → DB 名
│   ├── provision.ts           # TiDB Cloud Zero の作成と .env 生成（npm run provision）
│   ├── migrate.ts             # 全テナント DB への prisma migrate deploy（npm run migrate）
│   ├── db/
│   │   ├── prisma-client.ts   # driver adapter (@prisma/adapter-mariadb) の設定: TLS、プール、タイムアウト
│   │   ├── db.service.ts      # テナント DB ごとの PrismaClient を生成・キャッシュ・破棄
│   │   └── db.module.ts
│   ├── tenant/                # x-tenant-id ヘッダ → AsyncLocalStorage（currentTenant()）
│   ├── common/                # BigInt → 文字列の interceptor、ParseBigIntPipe
│   ├── users/  posts/         # NestJS 標準のリソース構成（module / controller / service / dto）
│   ├── steps/                 # チュートリアルの各ステップ（表示されるコード = 実行されるコード）
│   ├── tutorial/              # TUTORIAL.md の描画とステップ実行 API
│   └── generated/prisma/      # prisma generate の出力（git 管理外）
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
| `npm run build` / `npm start` | `prisma generate` + tscビルド / ビルド済みを起動 |
| `npm run provision` | TiDB Cloud Zeroの作成と `.env` 生成、テナントDBの作成 |
| `npm run migrate` | `TENANTS` の全DBに `prisma migrate deploy` を実行 |
| `npm run prisma:generate` | Prisma Clientの再生成（`npx prisma generate` と同じ） |
| `npm run prisma:migrate:dev` | `npx prisma migrate dev --create-only` と同じ |

### Prisma CLI

Prisma CLIは `prisma.config.ts` を読み、`.env` の `DATABASE_URL`（開発用テナント `tenant_acme`）に接続します。別のテナントを対象にするときは環境変数で上書きします。

```bash
DATABASE_URL="mysql://USER:PASSWORD@HOST:4000/tenant_globex?sslaccept=strict" npx prisma migrate status
```

| コマンド | 用途 | 備考 |
| --- | --- | --- |
| `npx prisma validate` | `schema.prisma` の構文と整合性を検査 | DB接続不要 |
| `npx prisma format` | `schema.prisma` を整形 | DB接続不要 |
| `npx prisma generate` | Prisma Clientを `src/generated/prisma/` に生成 | DB接続不要。スキーマを変えたら必ず実行する。`.env` が無くても動く |
| `npx prisma migrate dev --create-only --name <name>` | スキーマの差分からマイグレーションSQLを生成（適用はしない） | shadow DBを自動作成する。生成後にSQLを確認・手編集する |
| `npx prisma migrate deploy` | 未適用のマイグレーションを適用 | 1テナントのみ。全テナントは `npm run migrate` |
| `npx prisma migrate status` | 適用状況を確認 | |
| `npx prisma migrate diff --from-config-datasource --to-schema prisma/schema.prisma --exit-code` | 実DBとスキーマの差分（drift）を検出 | 差分なしでexit 0、ありで2。CIに組み込める |
| `npx prisma migrate resolve --applied <name>` / `--rolled-back <name>` | 途中で失敗したマイグレーションの記録を修正 | |
| `npx prisma migrate reset` | DBを作り直して全マイグレーションを適用 | **データが消える**。開発用テナントでのみ使う |
| `npx prisma db pull` | 実DBから `schema.prisma` を逆生成 | 既存DBの取り込み用。AUTO_RANDOM / TTL / 生成列は反映されない |
| `npx prisma db execute --file <sql>` | SQLファイルを実行 | 手動のDDLやデータ投入に |
| `npx prisma studio` | ブラウザでデータを閲覧・編集 | `DATABASE_URL` のテナントが対象 |

### スキーマを変更する手順

1. `prisma/schema.prisma` を編集し、`npx prisma format && npx prisma validate` で確認する
2. `npx prisma migrate dev --create-only --name <name>` でマイグレーションSQLを生成する
3. `prisma/migrations/<timestamp>_<name>/migration.sql` を確認する
   - カラムのリネームは `DROP COLUMN` + `ADD COLUMN` として生成されるので、`RENAME COLUMN` に書き換える
   - AUTO_RANDOM、TTL、生成列などのTiDB固有DDLはこの段階に手編集で付与する（`[手編集]` コメントを付ける）
4. `npm run migrate` で全テナントに適用する
5. `npx prisma generate` でPrisma Clientを再生成し、`npm run build` でコンパイルエラー（変更漏れ）を確認する

### TiDB固有DDLとスキーマ宣言の対応

| 機能 | `schema.prisma` | マイグレーションSQL（手編集） | 例 |
| --- | --- | --- | --- |
| AUTO_RANDOM主キー | `BigInt @id @default(dbgenerated())` | `\`id\` BIGINT NOT NULL AUTO_RANDOM` | `events.id` |
| TTL | 宣言しない | `TTL = \`created_at\` + INTERVAL 7 DAY TTL_ENABLE = 'ON'` | `events` |
| 生成列 | `String? @default(dbgenerated())` | `\`plan\` VARCHAR(20) AS (\`attributes\`->>'$.plan') VIRTUAL` | `users.plan` |

いずれも `dbgenerated()` で宣言すると `migrate diff` のdrift判定に出ません。AUTO_RANDOMの主キーを `autoincrement()` と宣言すると、動作はしますが毎回driftとして報告されます。また `dbgenerated()` の主キーは `create()` の戻り値が `null` になるため、採番値が必要なテーブルには使えません（詳細は `TUTORIAL.md` の「スキーマ定義と型生成」）。

初回マイグレーション：`prisma/migrations/20260827225404_init/migration.sql`

## 接続とTLS

- ランタイムは `@prisma/adapter-mariadb`（Prisma 7でMySQL向けに提供される唯一のTCP用driver adapter）を使う。設定は `src/db/prisma-client.ts`
  - `ssl: { rejectUnauthorized: true }`: TiDB Cloudの公開エンドポイントは公的CAなのでCAファイルは不要
  - `connectTimeout: 10_000`: 既定の1秒では遠隔リージョンで `pool timeout` になる
  - `connectionLimit: 5`, `idleTimeout: 300`: テナントごとのプール
- Prisma CLIは `DATABASE_URL` の `?sslaccept=strict` でTLSを検証する

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
- `Timeout: 120`。`02-migrate` は2テナントで約15秒かかる
- `02-migrate` はLambda上でも動く。`src/migrate.ts` はnpxを経由せずPrisma CLIを直接起動し、`HOME=/tmp` にして読み取り専用のファイルシステムを避けている
- `Dockerfile` は `node:22-slim` に `openssl` と `ca-certificates` を追加してある。無いとPrisma CLIのTLS検証が `P1011` で失敗する（ランタイムのmariadbコネクタはNode内蔵のCAで接続できるため、アプリは動くのにマイグレーションだけ失敗する）
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
| `pool timeout: failed to retrieve a connection` | `src/db/prisma-client.ts` の `connectTimeout` を延ばす |
| `Cannot resolve environment variable: DATABASE_URL` | `.env` が無い。`npm run provision` か `.env.example` のコピー |
| `migrate dev` がshadow DBの作成で失敗する | 接続ユーザーに `CREATE DATABASE` 権限を付与するか、`prisma.config.ts` の `migrations.shadowDatabaseUrl` に別DBを指定する |
| TiDB Cloud Zeroに接続できなくなった | 30日で失効している。`rm .env && npm run provision && npm run migrate`。Lambdaにデプロイしている場合は `sam deploy` で新しい `DatabaseUrl` を渡す |
