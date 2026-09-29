# データベース パフォーマンス テスト

Laravel と TypeScript API の TiDB Serverless vs PlanetScale パフォーマンス比較

## 構成

- **Laravel API** (`/src`) - PHP Laravel + Eloquent ORM
- **TypeScript API** (`/src-ts`) - Hono + Drizzle ORM  
- **負荷テスト** (`/locust`) - Locust パフォーマンステスト

## データベース

- **TiDB Serverless** - メインテスト用データベース
- **PlanetScale** - 比較用サーバーレスデータベース

## テスト実行

```bash
cd locust
./run_tests.sh [light|medium|heavy|spike|custom]
```

詳細な結果は `locust/` フォルダ内のレポートファイルを確認してください