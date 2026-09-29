# rag-tidb

TiDB Cloud のベクトル検索機能を使って、**ベクトルDBを別に立てずにRAGっぽい検索アプリを作る**ためのサンプルプロジェクトです。

記事の内容に合わせて、Node.js + TypeScript + OpenAI + TiDB Cloud で構成しています。

## できること

- Markdown 文書をチャンクに分割
- OpenAI Embeddings API で embedding を生成
- TiDB Cloud に本文・メタデータ・embedding を保存
- 質問文を embedding 化して類似チャンクを検索
- 検索結果を LLM に渡して回答を生成

## 必要なもの

- Node.js v20 系
- TiDB Cloud アカウント
- OpenAI API キー

## セットアップ

### 1. 依存関係を入れる

```bash
npm install
```

### 2. `.env` を設定する

プロジェクト直下の `.env` に TiDB Cloud と OpenAI の情報を入れます。

```env
TIDB_HOST=your-tidb-host
TIDB_PORT=4000
TIDB_USER=your-tidb-user
TIDB_PASSWORD=your-tidb-password
TIDB_DATABASE=rag_demo
OPENAI_API_KEY=sk-xxxxxxxx
```

### 3. TiDB Cloud でテーブルを作る

`schema.sql` を TiDB Cloud の SQL Editor で実行します。

`CREATE DATABASE` → `USE` → `documents` / `document_chunks` / `search_logs` の順で作成してください。

### 4. 文書を投入する

```bash
npm run ingest
```

### 5. 検索する

```bash
npm run search -- "TiDB Cloudを使うメリットは？"
```

## スクリプト

- `npm run ingest` — `data/docs/` の文書を TiDB Cloud に投入
- `npm run search -- "..."` — 質問を投げて回答を取得

## ファイル構成

```text
rag-tidb/
├── src/
│   ├── db.ts
│   ├── embed.ts
│   ├── chunk.ts
│   ├── ingest.ts
│   └── search.ts
├── data/
│   └── docs/
├── schema.sql
├── TIDB_SETUP_GUIDE.md
└── .env
```

## 注意点

- `CREATE VECTOR INDEX` はプランや構成によって使えないことがあります
- その場合は、まずテーブル作成まで進めて検索ロジックを確認してください
- `.env` は Git にコミットしないでください

## 記事

このリポジトリは、次の記事の内容をもとにしています。

- ベクトルDBを別に立てずにRAGを作れる？TiDB Cloudで小さなAI検索アプリを作って検証した

## ライセンス

特に指定がなければ、必要に応じて追記してください。
