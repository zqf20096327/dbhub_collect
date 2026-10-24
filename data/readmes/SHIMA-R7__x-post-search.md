# x-post-search

**twiforkで公開ユーザーの投稿を収集し、SQLiteで日本語・キーワード・正規表現検索するPython CLI。**

自分のログインセッションを使い、他の公開ユーザーを取得対象にできます。X公式APIのキーや読み取り料金は不要です。取得・再開、IDによる重複更新、CSV出力、既存JSON/CSVの取り込みに対応します。

> 非公式のWebクライアント方式です。Xによる承認や規約順守を保証するものではありません。レート制限を守っても自動アクセスが許可されるとは限りません。利用前に[X利用規約](https://x.com/en/tos)と適用条件を確認してください。全履歴の取得・継続動作は保証しません。Xから拒否・ロック等を受けた場合は停止し、通常画面で確認してください。

## インストール

Python 3.11以上。Windows / macOS / Linux向けです。

```powershell
git clone https://github.com/SHIMA-R7/x-post-search.git
cd x-post-search
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\python.exe -m xpost --help
```

macOS/Linuxでは `.venv/bin/python` に読み替えてください。仮想環境を有効化すれば `xpost` コマンドも使えます。すでにtwiforkを使っている環境とは別の仮想環境を推奨します。依存は `twifork==2.4.0` に固定しています。`twikit` と `twifork` は同じimport名を使うため、両パッケージを同じ環境に入れないでください。

## 収集する

既存のtwiforkが読み込めるCookie JSONを、プロジェクト外の安全な場所に置きます。`auth_token` と `ct0` が必要です。ブラウザー拡張によって出力形式が異なるため、Netscape形式やCookie配列をそのまま読む機能はありません。既存のtwiforkの `save_cookies` で保存したJSONを使えます。

**Cookieはログイン権限そのものです。GitHub、Issue、チャットに貼り付けないでください。** このツールは既存ファイルをローカルで読むだけで、ログイン情報を収集・配布しません。対象ユーザーの認証情報は不要です。

```powershell
$env:X_COOKIES_FILE = 'C:\private\x-cookies.json'
.\.venv\Scripts\python.exe -m xpost collect --user XDevelopers --max-pages 3
```

または `--cookies 'C:\private\x-cookies.json'` で指定できます。Cookieの実値をコマンド引数に書かないでください。

既定は **searchモード**。ユーザーIDによる `from:` 条件でLatest検索をページ送りします。全期間検索の公式APIとは別の、Xの通常検索に依存する方式です。古い期間を調べる場合:

```powershell
.\.venv\Scripts\python.exe -m xpost collect --user XDevelopers --since 2020-01-01 --until 2021-01-01 --max-pages 10
```

日付はUTC、sinceは開始日、untilは終了日を含まない条件です。取得範囲はXが返す検索結果に限られます。期間を分割しても、存在する全投稿を網羅できたとは証明できません。

直近のプロフィールをたどる場合:

```powershell
.\.venv\Scripts\python.exe -m xpost collect --user XDevelopers --mode timeline --max-pages 5
```

timelineはtwiforkのRepliesフィードを使い、返信を含む本人の投稿を収集します。会話内の他人の投稿は著者IDで除外します。日付指定はsearchモード専用です。timelineでも全履歴に届く保証はありません。リポスト、引用、長文の表現はtwifork/Xの応答に依存し、本文は `Tweet.full_text` を保存します。画像・動画・引用先・リンク先は取得せず、本文だけを検索します。

## 保存済み投稿を検索する

```powershell
.\.venv\Scripts\python.exe -m xpost search --user XDevelopers --keyword Python
.\.venv\Scripts\python.exe -m xpost search --keyword 日本語 --keyword SQLite --mode any
.\.venv\Scripts\python.exe -m xpost search --regex 'Python|SQLite' --ignore-case --csv results.csv
.\.venv\Scripts\python.exe -m xpost status
```

- キーワードは本文全体への部分一致。複数指定は既定AND、`--mode any` はOR。正規表現を併用するとANDです。
- `--ignore-case` はキーワードにUnicode casefold、正規表現にIGNORECASEを使います。
- 日本語の単語分割に依存しない全件走査です。SQLite FTSのトークン検索ではありません。大量データでは時間がかかります。
- 正規表現は1投稿あたり0.1秒で打ち切り、タイムアウトなら停止します。`--limit 100` で結果件数を制限できます。
- コンソールはJSONL、CSVはUTF-8 BOM付き。改行・カンマを保持し、数式扱いされ得るセルにはアポストロフィを付けます。CSVは完全な再取り込み用バックアップではありません。
- CSV成功時に出力先を置き換えます。失敗時は既存CSVを保持します。ExcelでIDを開く際は文字列として扱ってください。

## 中断・再開と重複排除

同じDB・ユーザーID・mode・since/until・page-sizeで再実行すると確定済みページの次から再開します。Ctrl+Cでも確定済みページは残ります。本文とカーソルは同じSQLiteトランザクションで保存します。未確定ページは再取得し、投稿IDを主キーとして重複を更新します。

twiforkのページ内バッファをすべて読み出してからカーソルを保存するため、要求件数を超えて返された投稿も再開時に飛ばしません。この互換処理は2.4.0向けに固定・テストしています。`--page-size` は1〜20件の要求サイズであり、実際のページ件数の上限ではありません。

searchの初回には上限投稿IDと終了日を固定し、再開時も同じ検索範囲を使います。空ページ、次カーソルなしで走査終了とします。カーソルの循環は状態を保持してエラー停止します。「終了」は全履歴取得の証明ではありません。

新規投稿を調べる、またはカーソルが失効した場合は同じ条件に `--restart` を追加します。DBの投稿を消さず、走査だけ先頭からやり直します。条件を変えると別ジョブになります。同じDBを複数の収集プロセスから同時操作しないでください。

## 通信制限・エラー

通信間隔は既定5秒、最低5秒です。twifork内の初期通信も同じ待機処理を通します。応答のrate-limit残数が0ならresetまで待機し、429ではresetとRetry-Afterを尊重します。ヘッダーがない429は900秒待機します。通信失敗・5xxは指数バックオフとジッターで最大3回再試行します。既定960秒を超える待機なら停止し、後で手動再開します。

認証エラー、アクセス拒否、アカウントロック等は再試行せず停止します。アカウント切替、プロキシローテーション、自動解除、CAPTCHA解決、TLS偽装のオプションは提供しません。読み取り用機能のみを呼び、送信層でもGET以外を拒否します。Xへの投稿・いいね・フォロー操作はありません。

## 設定

```powershell
Copy-Item config.example.toml config.toml
.\.venv\Scripts\python.exe -m xpost --config config.toml --db data/posts.sqlite3 collect --user XDevelopers
```

設定は `--config` 指定時のみ読みます。`--config` / `--db` はサブコマンドの前に置きます。相対パスは現在の作業ディレクトリー基準です。CookieパスはCLIか環境変数で指定します。

## 手持ちファイルを取り込む（通信なし）

```powershell
.\.venv\Scripts\python.exe -m xpost import example-posts.json --user sample
.\.venv\Scripts\python.exe -m xpost search --user sample --keyword SQLite
```

サンプルは架空の2投稿です。JSON配列、APIのdata配列、JSONL、CSV、Xアーカイブのtweets.jsに対応します。1ファイルは1ユーザーに限定し、`--user` で所属を指定してください。

JSON/CSVの必須項目は `id,text`、任意項目は `created_at,author_id`。`id_str` / `full_text` / 長文フィールドにも対応します。IDは文字列にしてください。日時はタイムゾーン付きISO 8601またはXアーカイブ形式で受け付け、UTCに統一します。未指定は空欄です。

入力全体をメモリーへ読み込み検証してから保存するので、大きいファイルは分割してください。アーカイブJSは既知の代入接頭辞を除いてJSON解析し、実行しません。利用・保存する権限のあるデータのみ取り込んでください。

## 削除とデータ管理

```powershell
.\.venv\Scripts\python.exe -m xpost purge --id 1234567890123456789
.\.venv\Scripts\python.exe -m xpost purge --user targetname
```

DBの投稿だけを削除します。CSV・バックアップ・共有先も必要に応じて別途削除してください。X上の削除・編集・非公開化を自動監視する機能はありません。再収集だけでは削除済み投稿は消えません。必要な更新・削除を運用で実施し、削除対象を再取り込みしないでください。公開投稿も恒久保存・再配布が自由という意味ではありません。

`.gitignore` で一般的なCookie名・DB・config.toml・private/data/exportsを除外していますが、任意の名前の秘密ファイルまで自動検出できません。公開前には必ずGitの追跡対象を確認してください。実データをIssueへ添付しないでください。

## 任意の公式API

規約・契約に沿った公式経路が必要な場合には有料の `official-collect` も残しています。`--allow-paid-api` が必須です。twiforkの `collect` から公式APIへ自動フォールバックしません。[公式APIの範囲・料金・使い方](docs/official-api.md)を参照してください。

## 開発・テスト

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub ActionsでWindows/Linux、Python 3.11/3.13の通信なしテストを実行します。twifork本体のResultクラスを使ってバッファと再開処理を検証します。実アカウントでのX通信はCIで行いません。[検証記録](VALIDATION.md)も参照してください。

## ライセンス・謝辞

本プロジェクトは[MIT License](LICENSE)。[twifork](https://github.com/PawiX25/twifork)および元の[twikit](https://github.com/d60/twikit)に感謝します。本プロジェクトは依存ライブラリーとして利用し、そのコードを同梱しません。X、twifork、twikitの公式製品ではありません。
