# Steam Vector Calculator

Steamのゲームを埋め込み（embedding）ベクトルにして、足したり引いたりしながら「傾向の近い次の一本」を探すツールです。`Hades − Slay the Spire`（アクションローグライク から デッキ構築 を引く）のような演算が、そのまま動きます。

**動くデモ: https://subara3.com/tool/steam-vector-calc/**

ベクトル検索・名前ベクトル・完全一致・埋め込み生成・記憶の自動失効を、**TiDB Cloud の単一エンジン**だけで組んでいます。アプリサーバーも専用ベクトルDBも立てていません（フロントは静的、APIはPHP1ファイル、共有レンタルサーバーで動きます）。

## できること

- **ベクトル演算**: 2本のゲームを足し引きして、近いゲームを探す
- **検索**: 英語名・日本語名の両対応。固有名詞には名前専用の2本目のベクトル、完全一致には LIKE、両者を RRF で融合
- **おきにいり**: 好きを覚えて、その平均ベクトルから「思い出す」（LLMは使わない。埋め込み＋SQL＋TTLだけ）

## 仕組みのあらまし

| 要素 | 使っているもの |
|---|---|
| 意味の検索 | `embedding`（説明文＋ジャンル）を Auto Embedding で自動生成 |
| 固有名詞・多言語 | `name_embedding`（名前だけの2本目のベクトル） |
| 完全一致 | SQL の `LIKE` |
| 融合 | Reciprocal Rank Fusion（順位から `1/(k+rank)` を足す） |
| 記憶 | `taste_memory` テーブル＋TTL（30日で自動失効） |
| 負荷対策 | 結果をファイルキャッシュしてRUを節約。混雑/休止はバナーで告知 |

埋め込みモデルは TiDB 内蔵の Auto Embedding（`tidbcloud_free/cohere/embed-multilingual-v3`、1024次元）。

## 構成

```
web/        フロント（HTML/CSS/JS）＋ PHP API（1ファイル）。フラット配置でそのまま置ける
python/     データ投入・埋め込み補完・recall計測のスクリプト
sql/        スキーマ
```

## セットアップ

1. **TiDB Cloud Starter** を作成（無料枠でOK・クレカ不要）。
2. `sql/schema.sql` でテーブルを作成。
3. `web/config.local.example.php` を `config.local.php` にコピーして接続情報を記入（このファイルは公開しないこと。`.gitignore` 済み）。Python側は `.env` に `TIDB_HOST` などを置く。
4. `python/load_data.py` でデータ投入（[FronkonGames/steam-games-dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset) を使用）。`embedding` はINSERT時に自動生成、`name_embedding` は `fill_name_embedding.py` で補完。
5. `web/` 一式をサーバーに置く（PHP 8.x）。

## recall の測り直し

記事で出している recall@k は、自分のTiDBで再現できます。

```bash
python python/benchmark_hybrid.py   # 説明文ベクトル / LIKE / 名前ベクトル / RRF
python python/benchmark_bm25.py     # BM25 vs LIKE（全文検索対応リージョンが必要）
```

## クレジット・ライセンス

- データ: [FronkonGames / steam-games-dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)（CC-BY-4.0）
- ゲーム画像・情報: Steam (Valve)
- 非営利のファン制作物です。
