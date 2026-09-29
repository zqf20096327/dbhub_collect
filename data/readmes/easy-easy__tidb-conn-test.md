# TiDB接続アプリケーション

PythonでTiDBに接続するアプリケーションです。構成管理は`uv`を使用しています。

## セットアップ

### 1. 依存関係のインストール

```bash
# uvで依存関係をインストール
uv sync
```

### 2. 環境変数の設定

`.env`ファイルを作成して編集：

```env
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=your_password
```

## 使い方

### アプリケーションの実行

```bash
# uvで実行
uv run main.py

# または、仮想環境をアクティベートして実行
source .venv/bin/activate
python main.py
```
