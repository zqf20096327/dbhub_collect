# t3-rust-accel

[T3 Code](https://github.com/pingdotgg/t3code) サーバを個人環境で動かすための、Rust 加速コンポーネントとテレメトリ無効化のセットです。
Linux・macOS・Windows のビルド済みサーバで、テレメトリを止めてメモリ使用量を抑えたいときに組み込みます。
上流の配布バイナリをパッチなしでそのまま使いたいときには使いません。

## 上流の T3 Code との違い

上流の T3 Code は使用状況を T3 運営のサーバに自動送信しますが、このキットは次の 2 点が異なります。

- 製品テレメトリと relay tracing を環境変数とソースパッチで既定で無効にします。上流ではイベント名・匿名 ID・OS・モデル名やキャッシュヒット量 (`cachedInputTokens` / `cacheCreationTokens`) を含むトークン数が `ingest.t3.codes` に送られますが、本文・プロンプト・コード・プロバイダの鍵は上流でも送られません。モデルとの通信には各プロバイダの CLI や API を使います。
- SQLite ドライバをネイティブアドオンと Rust bridge に置き換え、メモリ使用量を抑えます。Linux の systemd 設定では jemalloc と V8 の調整に加え、`code_index`・`code_slice`・`code_grep`・`code_diff`・`code_exec` の maki tools も利用可能です。

エージェントの動作やクライアント、セッションの扱いは上流と同じです。
セッションや鍵は `T3CODE_HOME` にそのまま残るため、このキットを外せば元の T3 Code をそのまま起動できます。

## リポジトリの構成

このリポジトリには 3 つの Rust クレートと、systemd 設定・パッチ・スクリプトが入っています。

| パス | 役割 |
| --- | --- |
| `crates/t3-rust-bridge/` | サーバから使う Rust bridge バイナリ (`T3_RUST_BRIDGE_BIN`) |
| `crates/t3-native-sqlite/` | `index.mjs` 経由で使うネイティブ SQLite バインディング (`T3_NATIVE_SQLITE_PATH`) |
| `crates/t3-maki-tools/` | `code_index` / `code_slice` / `code_grep` / `code_diff` / `code_exec` の CLI (`T3_MAKI_TOOLS_BIN`) |
| `systemd/` | `t3code.service` の user unit drop-in テンプレート (`%h` はホームディレクトリ) |
| `patches/` | Rust 統合・テレメトリ無効化・Antigravity 連携・T3 Connect E2EE のパッチ (`0000`〜`0003`) |
| `scripts/` | 共通のビルド・起動ランチャー (`t3-accel.mjs`) と systemd 設定スクリプト |

## サーバのビルドと起動

ビルドには Node.js 26、Rust stable (GitHub Actions は 1.100) を使います。
Windows では Rust の MSVC ツールチェーンと Visual Studio Build Tools の C++ ビルドツール・Windows SDK、`diff` には Git、`exec` には Python 3 が必要です。
[上流の T3 Code](https://github.com/pingdotgg/t3code) を対象コミットに切り替え、このリポジトリのルートからパッチを順に適用します。

```sh
git -C /path/to/t3code switch --detach 4e6b1fa7710515cee652370b534e041a372648ea
for patch in patches/000*.patch; do
  git -C /path/to/t3code apply "$PWD/$patch"
done
```

T3 Code のソースで `pnpm install --frozen-lockfile` と `pnpm exec vp run --filter t3 build` を実行すると、Web クライアント入りの `apps/server/dist/bin.mjs` が生成されます。
その後、このリポジトリのルートで Rust コンポーネントのビルドとテストを実行してください。

```sh
node scripts/t3-accel.mjs build
node --test crates/t3-native-sqlite/test.mjs scripts/t3-accel.test.mjs
```

### GitHub Release の配布アーカイブでの起動

バージョンタグ (例 `v1.2.3`) の GitHub Release には、Linux・macOS (x64・arm64) と Windows (x64) の配布アーカイブと `SHA256SUMS` が並びます。
Linux 用アーカイブは Debian 12 コンテナでビルドし、Debian 12・13 と macOS・Windows の各ランナーで展開と起動を確認済みです。
展開前に SHA-256 (または `gh attestation verify <archive> --repo sahenjp/t3-rust-accel`) を照合すれば、同梱のバイナリと SQLite アドオンで `build` なしに `node scripts/t3-accel.mjs serve <server/bin.mjs>` を実行できます。

### macOS でのビルドと起動

Xcode Command Line Tools を入れ、Node.js と Rust のアーキテクチャをそろえてビルドしたうえで、Linux と同じ `serve` コマンドで起動します。

### Windows での PowerShell からの起動

PowerShell から `t3-accel.mjs serve` にサーバの `bin.mjs` を渡して起動します。

```powershell
node scripts/t3-accel.mjs serve 'C:\src\t3code\apps\server\dist\bin.mjs'
```

このコマンドは `.exe` 2 本と SQLite アドオンのパスを渡し、既存の `T3CODE_HOME` を使って既定でループバック (`127.0.0.1`) に待ち受けます。
Python の場所を明示するときは、`T3_MAKI_PYTHON` に実行ファイルの絶対パスを指定してください。

### Linux の systemd サービスへの組み込み

フォアグラウンドでは `serve` コマンドを使用できますが、既存の `t3code.service` に組み込む場合は CLI 2 本を `~/.local/bin` に配置して drop-in を適用します。

```sh
install -d ~/.local/bin
install -m 755 target/release/t3-rust-bridge target/release/t3-maki-tools ~/.local/bin/
scripts/apply-phase2.sh
systemctl --user daemon-reload
systemctl --user restart t3code.service
```

この drop-in は既定で `~/Projects/t3code` のサーバと `~/Projects/t3-rust-accel` のアドオンを指すため、別の場所でビルドした場合は `ExecStart` と `T3_NATIVE_SQLITE_PATH` を編集します。
サービスを再起動するときは、実行中の T3 Code セッションを先に閉じてください。

## テレメトリ送信の無効化

drop-in と `t3-accel.mjs` には、テレメトリを止める次の設定が入っています。

```ini
Environment=T3CODE_TELEMETRY_ENABLED=false
Environment=T3CODE_OTEL_SDK_DISABLED=true
```

この設定で製品テレメトリ (`ingest.t3.codes`) と relay の OTLP tracing が止まり、環境変数を引き継ぐバンドルエージェントの analytics connect-RPC も停止します。
サーバに `patches/0001-telemetry-opt-in-by-default.patch` を適用してあれば、環境変数の指定がないときもテレメトリは無効です。

## 公式 Antigravity CLI での接続

`patches/0002-use-installed-antigravity-cli.patch` を適用したサーバでは別途導入した Google 公式の `agy` CLI をプロバイダ設定のパスか `PATH` から呼び出します。
T3 Code は公式 CLI を介して認証とセッションを扱い、利用履歴をローカルファイルから読み取りますが、CLI を自動ダウンロードせず残りクォータも表示しません。

## T3 Connect の TLS 1.3 エンドツーエンド暗号化

`patches/0003-t3-connect-e2ee.patch` は T3 Connect の管理トンネルに TLS 1.3 の相互認証を通し、Cloudflare のリレーには暗号化済みの WebSocket フレームだけを流します。

1. ホストの証明書ディレクトリに `host-key.pem`・`host-cert.pem` (`serverAuth`)・`client-ca.pem` を置き、各クライアントにはその機器で生成した `client-key.pem`・CA 発行の `client-cert.pem` (`clientAuth`)・別経路で受け取った `host-cert.pem` を配置してください。
2. ホストで `T3CODE_CONNECT_E2EE_CERT_DIR` に証明書ディレクトリ、`T3CODE_CONNECT_E2EE_PORT` に未使用のループバックポートを指定してサーバを起動します (このポートが通常の HTTP で応答するのはホスト情報と署名付きヘルスチェックだけです)。
3. ホストで `t3 auth pairing create --base-url http://127.0.0.1:3774` を実行して一度限りのペアリングリンクを発行し、接続する PC で次のコマンドを実行して表示されたローカル URL をブラウザで開きます。

```sh
t3 connect e2ee --endpoint https://your-connect-hostname --credentials /path/to/client-certs
```

`--endpoint` には T3 Connect の環境 URL を指定し、ローカルポート (既定 `3774`) を変えるときは `--port` とペアリングリンクの `--base-url` に同じ値を指定します (証明書を更新したらホスト証明書を再配布してください)。
このモードを有効にした環境はパッチ適用済み CLI 経由のブラウザだけで利用でき、公式アプリからの接続を拒否して管理トンネル経由の公開 Webhook も停止します (プッシュ通知を有効にした場合の通知データも別経路を通ります)。

## T3CODE_HOME のセッションと設定の引き継ぎ

ログ・スレッド・セッション・プロバイダの鍵は `T3CODE_HOME` (既定 `~/.t3`) の下に保存されるため、サーバのバイナリを差し替えたり drop-in を付けて再起動したりしてもそのまま引き継がれます。

## systemd drop-in の解除

Linux で drop-in を外して元の `t3code.service` に戻すには、次のコマンドを実行します。

```sh
sh scripts/rollback-phase2.sh
systemctl --user daemon-reload
systemctl --user restart t3code.service
```

## Python 実行と待ち受けアドレスの制限

- `exec` は全 OS で実行時間、Linux と Windows でメモリを制限し、API キーなどの環境変数を除外して参照範囲を作業ディレクトリ内に絞ります。ただし Python は実行ユーザーの権限で動くため、信頼できるスクリプトだけを渡してください。
- ランチャー (`t3-accel.mjs`) と systemd drop-in は、既定でループバック (`127.0.0.1`) に待ち受けます。
- drop-in の `T3CODE_RELAY_URL` と `T3CODE_CLERK_*` は上流のリリースバイナリが埋め込む公開値であり、T3 Connect を使わない環境では削除可能です。
