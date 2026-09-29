# tidb-data-analyze

TiDB の**ベクトル検索**、**全文検索**、**自動 Embedding** 機能を活用し、生成された日本語のキャラクターレビューデータを分析・検索するデモプロジェクトです。

- [TiDB Zero](https://zero.tidbcloud.com/): ログイン不要で試せるクラウドデータベース
- ベクトル検索 & 全文検索: セマンティック検索の定番手法

## アーキテクチャ概要

```
┌─────────────────┐        ┌─────────────────────────┐
│  Browser (SPA)  │ <────> │  Express Server :4001   │
│  public/*.html  │  HTTP  │  src/server.ts          │
└─────────────────┘        └───────────┬─────────────┘
                                       │ mysql2
                                       ▼
                           ┌─────────────────────────┐
                           │   TiDB Zero Cluster     │
                           │  ┌───────────────────┐  │
                           │  │ characters        │  │
                           │  │ reviews           │  │
                           │  │  ├─ FULLTEXT idx  │  │
                           │  │  └─ VECTOR  idx   │  │
                           │  └───────────────────┘  │
                           │  TiDB Cloud Inference   │
                           │  (auto text embedding)  │
                           └─────────────────────────┘
```

- **データ層**：API 経由で TiDB Zero の一時クラスタをワンクリックで発行し、接続情報を `.env` に書き出します。
- **データ準備**：`src/prepare.ts` がテーブルを作成し、10 体のキャラクターと約 1000 件の日本語レビューを一括投入します。`reviews.content_vector` は `GENERATED` カラムで、TiDB が挿入時に `EMBED_TEXT` を呼び出して自動生成します。
- **サーバーサイド**：Express が以下 3 種類の API を公開します。
  - キャラクター / 属性ランキング（`fts_match_word` による言及数集計）
  - レビュー検索（`fts` / `vector` / `hybrid` の 3 モード）
  - キャラクター詳細と集計統計
- **フロントエンド**：静的な SPA（`public/index.html` + Chart.js）。タブ切り替えでランキング、レーダーチャート、検索結果を表示します。

## 実行方法

### 前提条件

- Node.js 20+ と `pnpm`
- `zero.tidbapi.com` へアクセス可能であること（TiDB Zero クラスタ発行に使用）

### 手順

```bash
# 1. 依存関係をインストール
pnpm install

# 2. データ準備：TiDB Zero クラスタの作成、テーブル作成、キャラクターとレビューの投入
#    初回は各レビュー挿入時に自動 Embedding が走るため時間がかかります
pnpm prepare

# 3. Web サーバーを起動
pnpm web
# → http://localhost:4001
```

### 補助スクリプト

```bash
# 現在のクラスタに mysql クライアントで直接接続
pnpm tidb
```

接続情報は `.env` に保存されます（`prepare` が生成）。`web` と `tidb` はいずれもこのファイルから読み込みます。`pnpm prepare` を再実行すると新しいクラスタを発行し、このファイルを上書きします。

## Web 画面の説明

### キャラクター

キャラクター画面では全てのキャラクターを一覧表示します。

![](./assets/characters.png)

### ランキング

ランキング画面では、各キャラクターおよび属性ごとのレビュー件数ランキングを表示します。

![](./assets/ranking.png)

### 検索

検索画面では、FTS 検索とベクトル検索を手動で実行できます。

![](./assets/search.png)
