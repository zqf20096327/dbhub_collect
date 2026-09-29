# Kysely × TiDB（NestJS）

TypeScript / NestJSからKysely（型付きクエリビルダ）でTiDBに接続するサンプルアプリケーションです。テナント別データベースのマルチテナント構成で、TiDB固有機能（AUTO_RANDOM、TTL、JSON生成列）を含みます。スキーマはマイグレーション（TypeScript）で定義し、型は `kysely-codegen` でDBから生成します。

起動すると <http://localhost:3000> に実行可能なチュートリアル（`TUTORIAL.md`）が表示されます。このファイルはチュートリアルではなく、**このプロジェクトをKysely + TiDBアプリケーションとして開発するときの手順**をまとめています。

## 必要環境

- Node.js 22.12以上（`process.loadEnvFile()` と、CommonJSからESM専用パッケージ（Kysely）を読み込む `require(esm)` を使用）
- TiDB（TiDB Cloud Zero / Starter / Dedicated / セルフホスト）。接続ユーザーに `CREATE DATABASE` 権限が必要（テナントDBを作るため）

## セットアップ

```bash
npm install
npm run provision      # TiDB Cloud Zero を作成し .env を生成、テナント DB (tenant_acme, tenant_globex) を作成
npm run migrate        # 全テナント DB にマイグレーションを適用
npm run codegen        # DB から src/db/types.ts を生成（コミット済みのものと同じになる）
npm run start:dev      # http://localhost:3000
```

既存のTiDBを使う場合は、`.env.example` を `.env` にコピーして接続情報を書きます。そのうえで `npm run provision` を実行すると、テナントDBだけが作成されます（`.env` があればインスタンスは作りません）。

`.env` の内容：

| 変数 | 用途 |
| --- | --- |
| `DATABASE_URL` | 接続先。**開発用テナント（`tenant_acme`）のDBを指す**。末尾の `?ssl=...` は `kysely-codegen` がTLSで接続するためのmysql2のURLパラメータ |
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
│   ├── migrate.ts             # 全テナント DB への Migrator.migrateToLatest()（npm run migrate）
│   ├── db/
│   │   ├── migrations/        # スキーマの定義元（TypeScript）。0001_init.ts から連番で追加する
│   │   ├── types.ts           # kysely-codegen が DB から生成した型（コミットする。手で編集しない）
│   │   ├── client.ts          # mysql2 プール（TLS、プール設定、typeCast）+ Kysely。生 SQL 用の rows()
│   │   ├── db.service.ts      # テナント DB ごとの Kysely インスタンスを生成・キャッシュ・破棄
│   │   └── db.module.ts
│   ├── tenant/                # x-tenant-id ヘッダ → AsyncLocalStorage（currentTenant()）
│   ├── common/                # BigInt → 文字列の interceptor、ParseBigIntPipe
│   ├── users/  posts/         # NestJS 標準のリソース構成（module / controller / service / dto）
│   ├── steps/                 # チュートリアルの各ステップ（表示されるコード = 実行されるコード）
│   └── tutorial/              # TUTORIAL.md の描画とステップ実行 API
├── .kysely-codegenrc.json     # kysely-codegen の設定（camelCase、型の上書き）
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
| `npm run migrate` | `TENANTS` の全DBに `src/db/migrations/` を適用（アプリ内のMigrator。CLI不要） |
| `npm run codegen` | `DATABASE_URL` のDBから `src/db/types.ts` を生成 |
| `npm run codegen:verify` | 生成し直した結果がコミット済みの `types.ts` と一致するか検査（CI向け） |

KyselyにはCLIがありません。マイグレーションの適用はアプリ内の `Migrator`、型の生成は `kysely-codegen` で行います。

### スキーマを変更する手順

1. `src/db/migrations/0002_<name>.ts` を追加する。`up` / `down` にKyselyのスキーマビルダーで書き、ビルダーに無いTiDB固有DDLは `sql` で書き足す
2. `npm run migrate` で全テナントに適用する（`down` は使わない。戻すときは次のマイグレーションで戻す）
3. `npm run codegen` で `types.ts` を再生成する
4. `npm run build` で、変更した列を参照している箇所のコンパイルエラー（変更漏れ）を確認する

DBを先に変えてから型を追従させる流れなので、2と3の間はDBと型がずれています。デプロイでは「マイグレーション適用 → 型を再生成したコードのビルド → デプロイ」の順を守ります。

### TiDB固有DDLとスキーマ定義の対応

| 機能 | マイグレーションでの書き方 | 型（`.kysely-codegenrc.json` の上書き） | 例 |
| --- | --- | --- | --- |
| 生成列 | `col.modifyEnd(sql\`GENERATED ALWAYS AS (...) VIRTUAL\`)` | `ColumnType<string \| null, never, never>`（insert / updateを型で禁止） | `users.plan` |
| AUTO_RANDOM主キー | `col.primaryKey().modifyEnd(sql\`AUTO_RANDOM\`)` | `Generated<bigint>` | `events.id` |
| TTL | `createTable(...).modifyEnd(sql\`TTL = ...\`)` | なし | `events` |

マイグレーションがコードなので、生成したSQLを手編集する工程はありません。AUTO_RANDOM列はinsertで省略するだけで採番されます（Kyselyは `values()` に書いた列だけをINSERT文に含める）。

### kysely-codegenの上書き設定

`kysely-codegen` はMySQLのBIGINTとBOOLEAN（TINYINT(1)）を `number` にし、生成列を検出しません。`.kysely-codegenrc.json` の `overrides.columns` で次を上書きしています。テーブルや列を増やしたら、ここにも追加します。

- id列は `Generated<bigint>`、外部キー列は `bigint`
- `posts.published` は `Generated<boolean>`
- `users.plan` は `ColumnType<string | null, never, never>`

初回マイグレーション：`src/db/migrations/0001_init.ts`

## 接続と設定

- Kyselyは `mysql2` のプールをそのまま使う。設定は `src/db/client.ts`
  - `ssl: { minVersion: 'TLSv1.2', rejectUnauthorized: true }`: TiDB Cloudの公開エンドポイントは公的CAなのでCAファイルは不要
  - `connectionLimit: 5`, `idleTimeout: 300_000`: テナントごとのプール
  - `typeCast`: BIGINTを `bigint`、TINYINT(1)を `boolean` に変換する。Kyselyは値を変換しないため、ドライバで行う。`field.string()` は1列につき1回しか呼べない（2回呼ぶとパケットの読み取り位置がずれ、後続の列が壊れる）
  - `CamelCasePlugin`: DBのsnake_case列名をコード上はcamelCaseで扱う
- `jsonArrayFrom` / `jsonObjectFrom` で受け取るJSON経由の値には `typeCast` が効かない。ネストの中のBIGINTは `CAST(... AS CHAR)` で文字列にし、BOOLEANは `= 1` で真偽値にする
- `kysely-codegen` はmysql2にURLで接続する。TLSは `DATABASE_URL` の `?ssl=%7B%22rejectUnauthorized%22%3Atrue%7D` で指定する（`npm run provision` が付ける）
- Kysely 0.29はESM専用パッケージ。CommonJSのNestJSから使うため `tsconfig.json` は `module: nodenext`（Node 22.12以降の `require(esm)`）にしている。`Migrator` は `kysely/migration` サブパスから読み込む

## REST API

`x-tenant-id` ヘッダでテナントを指定します。

```bash
curl -H 'x-tenant-id: acme' -H 'content-type: application/json' \
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
- `02-migrate` はアプリ内のMigratorなのでLambda上でもそのまま動く
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
| `kysely-codegen` が `Connections using insecure transport are prohibited` | `DATABASE_URL` に `?ssl=%7B%22rejectUnauthorized%22%3Atrue%7D` が無い。`.env.example` を参照 |
| `Cannot find module 'kysely/migration'` | `tsconfig.json` の `module` / `moduleResolution` が `nodenext` になっていない |
| `is not valid JSON` / `Cannot convert ... to a BigInt` で500 | `typeCast` の中で `field.string()` を2回呼んでいる。1回だけ呼ぶ |
| 生成列 `plan` にinsertしようとして型エラー | 意図どおり。`overrides` で生成列を `never` にしている |
| idが `number` で返り、大きな値が丸められる | `typeCast` が無い（`src/db/client.ts`）。JSON経由のネストなら `CAST(... AS CHAR)` にする |
| TiDB Cloud Zeroに接続できなくなった | 30日で失効している。`rm .env && npm run provision && npm run migrate`。Lambdaにデプロイしている場合は `sam deploy` で新しい `DatabaseUrl` を渡す |
