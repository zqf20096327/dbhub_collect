# Rust TiDB CRUD Sample

TiDBを使用した簡単なCRUD操作のサンプルアプリケーションです。

## 機能

- User構造体のCRUD操作
- GET /users - 全ユーザー取得
- POST /users - ユーザー作成
- GET /users/:id - 特定ユーザー取得

## セットアップ

### 1. TiDBコンテナの起動

```bash
docker-compose up -d
```

### 2. アプリケーションの実行

```bash
cargo run
```

アプリケーションは `http://localhost:3000` で起動します。

## API エンドポイント

### ユーザー作成
```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com"
  }'
```

### 全ユーザー取得
```bash
curl http://localhost:3000/users
```

### 特定ユーザー取得
```bash
curl http://localhost:3000/users/1
```

## プロジェクト構造

```
src/
├── lib.rs          # モジュール管理
├── main.rs         # エントリーポイント
├── models.rs       # データモデル
├── handlers.rs     # HTTPハンドラー
├── database.rs     # データベース接続・マイグレーション
└── error.rs        # エラーハンドリング
```

## 技術スタック

- **Rust**: 2021 edition
- **Web Framework**: Axum
- **Database**: TiDB (MySQL互換)
- **ORM**: SQLx
- **Serialization**: Serde
- **Logging**: Tracing 