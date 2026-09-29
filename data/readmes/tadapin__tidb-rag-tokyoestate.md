# TiDB RAG Sample - 東京都不動産取引検索

TiDB Serverless のベクトル検索機能を使った RAG (Retrieval-Augmented Generation) のサンプルプロジェクトです。

東京都の不動産取引データ（108,028件）を自然言語で検索し、AIが回答を生成するチャットボットを構築します。

## 動作イメージ

```
ユーザー: 渋谷区の駅近マンション
    ↓
[Gemini] クエリパース → {"city": "渋谷区", "search_text": "渋谷区の駅近マンション"}
    ↓
[TiDB] フィルタ(city=渋谷区) + ベクトル検索 → 上位10件取得
    ↓
[Gemini] 検索結果を要約して日本語で回答
    ↓
チャット回答 + データテーブル表示
```

## セットアップ

### 1. 前提条件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (パッケージマネージャ)
- [TiDB Serverless](https://tidbcloud.com/) アカウント (無料枠あり)
- [Google AI API Key](https://aistudio.google.com/apikey) (Gemini 用)

### 2. インストール

```bash
git clone <this-repo>
cd tidb-re
uv sync
```

### 3. 環境変数

`.env` ファイルを作成:

```env
TIDB_HOST=gateway01.ap-northeast-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME=<cluster_id>.root
TIDB_PASSWORD=<password>
TIDB_DATABASE=test
GEMINI_KEY=<your_google_ai_api_key>
```

TiDB の接続情報は [TiDB Cloud Console](https://tidbcloud.com/) の Cluster > Connect から取得できます。

### 4. データ準備

[国土交通省 不動産取引価格情報](https://www.land.mlit.go.jp/webland/download.html) から東京都のCSVをダウンロードし、`data/` に配置します。

ダウンロードしたCSVは Shift_JIS エンコーディングのため、UTF-8 に変換が必要です:

```bash
cd data
iconv -f Shift_JISX0213 -t UTF8 Tokyo_20203_20253.csv > Tokyo_20203_20253.utf8.csv
```

### 5. データインポート

```bash
uv run python import_data.py
```

108,028行を TiDB にインポートします（Gemini Embedding API 経由で自動ベクトル化）。
Free tier では約17 rows/s で、フルインポートに約1.5時間かかります。
途中で中断しても、再実行で自動的に続きから再開します。

### 6. アプリ起動

```bash
uv run streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

## 使い方

チャット入力欄に自然言語で質問を入力:

| 質問例 | 動作 |
|--------|------|
| 渋谷区の駅近マンション | city=渋谷区 フィルタ + ベクトル検索 |
| 港区の商業地で事務所 | city=港区, area_type=商業地 + ベクトル検索 |
| 新宿駅周辺の土地 | ベクトル検索のみ (駅名はフィルタ対象外) |
| 木造の住宅地物件 | structure=木造, area_type=住宅地 + ベクトル検索 |

CLI での検索も可能:

```bash
uv run python search.py "千代田区の商業地"
```

## プロジェクト構成

```
tidb-re/
├── app.py              # Streamlit チャットUI
├── import_data.py      # CSV → TiDB インポーター
├── search.py           # ベクトル検索 CLI
├── test_app.py         # ユニットテスト
├── pyproject.toml      # 依存定義 (uv)
├── .env                # 環境変数 (git管理外)
├── data/               # CSVデータ (git管理外)
│   └── Tokyo_20203_20253.utf8.csv
├── design/             # 設計ドキュメント
│   ├── architecture.md # アーキテクチャ詳細
│   ├── pytidb.md       # PyTiDB の使い方
│   └── llm-integration.md # LLM連携パターン
├── CLAUDE.md           # Claude Code 向け指示
└── README.md           # このファイル
```

## テスト

```bash
uv run pytest test_app.py -v
```

外部API (Gemini, TiDB) は全て `unittest.mock` でモック化されており、ネットワーク不要で実行できます。

## 技術スタック

| カテゴリ | 技術 | 用途 |
|----------|------|------|
| DB | TiDB Serverless | MySQL互換 + ベクトル検索 |
| ORM/Vector | PyTiDB (`pytidb`) | スキーマ定義、CRUD、ベクトル検索 |
| Embedding | Gemini Embedding (`gemini-embedding-001`) | テキスト→ベクトル変換 |
| LLM | Gemini 2.5 Flash / Flash-Lite (`google-genai`) | クエリパース (Flash-Lite)、回答生成 (Flash) |
| UI | Streamlit | チャットボットUI |
| パッケージ管理 | uv | 高速な依存管理 |
| テスト | pytest | ユニットテスト |

設計の詳細は [`design/`](design/) ディレクトリを参照してください。

## ライセンス

MIT
