# t3-rust-accel

[T3 Code](https://github.com/pingdotgg/t3code) サーバを個人環境で動かすための、Rust 加速コンポーネントとテレメトリ無効化のセットです。インストール、テレメトリの止め方、セッションの扱いまで、このリポジトリ 1 つで完結します。

## 普通の T3 Code との違い

普通の T3 Code は、サーバの動作は上流のままで、使用状況を T3 運営のサーバに自動送信します。このキットは次の 2 点が違います。

- テレメトリを既定で送りません。上流では起動状況や使用統計 (イベント名、匿名 ID、OS やモデル名などのメタデータ) が `ingest.t3.codes` に送られます。使用統計にはトークン数が含まれ、キャッシュヒットの量 (`cachedInputTokens` / `cacheCreationTokens`) もこの中です。本文、プロンプト、コード、プロバイダの鍵は上流でも送られません。このキットでは環境変数とソースパッチの 2 重で送信を止めるので、匿名 ID による機器の追跡も発生しません。モデルとの通常の通信 (各プロバイダの API) は上流と同じです。
- サーバの土台を Rust で置き換え、少ないメモリで動くようにします。上流は Node の SQLite ドライバと既定のメモリ設定で動きます。このキットはネイティブ sqlite バインディング、Rust bridge、jemalloc と V8 の省メモリ設定を組み合わせ、systemd 側でメモリ上限を付けて動かします。あわせて `code_index` / `code_slice` / `code_grep` のコード読み替えツール (maki tools) を使えます。

そのほかの部分 (エージェントの動き、クライアント、セッションの仕組み) は上流と同じです。セッションや鍵は `T3CODE_HOME` のままなので、このキットを外せば元の T3 Code に戻せます。

## このリポジトリの中身

| パス | 役割 |
| --- | --- |
| `crates/t3-rust-bridge/` | サーバから使う Rust bridge バイナリ (`T3_RUST_BRIDGE_BIN`) |
| `crates/t3-native-sqlite/` | `index.mjs` 経由で使うネイティブ sqlite バインディング (`T3_NATIVE_SQLITE_PATH`) |
| `crates/t3-maki-tools/` | `code_index` / `code_slice` / `code_grep` の CLI (`T3_MAKI_TOOLS_BIN`) |
| `systemd/` | user unit の drop-in テンプレート (phase 2 サーバとメモリ調整)。`__HOME__` は staging 時に展開 |
| `patches/` | T3 Code サーバの製品テレメトリと relay tracing をオプトイン式にするソースパッチ |
| `scripts/` | `apply-phase2.sh` / `rollback-phase2.sh` / `apply-phase1.sh` の staging ヘルパー |

## 必要なもの

- Rust ツールチェーン (`cargo`)
- Node.js (T3 Code サーバ) と、動作している T3 Code のインストール
- T3 Code サーバのソース (サーバのビルドができる状態)

## インストール

```sh
cargo build --release --manifest-path crates/t3-rust-bridge/Cargo.toml
cargo build --release --manifest-path crates/t3-maki-tools/Cargo.toml
cargo build --release --manifest-path crates/t3-native-sqlite/Cargo.toml
install -m 755 target/release/t3-rust-bridge ~/.local/bin/
install -m 755 target/release/t3-maki-tools ~/.local/bin/
install -m 644 target/release/libt3_native_sqlite.so crates/t3-native-sqlite/t3_native_sqlite.node
```

ビルドしたバイナリを環境に向けて、systemd drop-in を反映し、サービスを再起動します。

```sh
sh scripts/apply-phase2.sh
systemctl --user daemon-reload
systemctl --user restart t3code.service
```

`apply-phase2.sh` は `systemd/phase2-server.conf` を `~/.config/systemd/user/t3code.service.d/` に置きます。このとき `__HOME__` はホームディレクトリに展開されます。チェックアウトの位置が違う場合は、`T3CODE_STATIC_DIR` / `T3_NATIVE_SQLITE_PATH` / バイナリのパスを書き換えてください。

## テレメトリは無効

drop-in には次の設定が入っています。

```ini
Environment=T3CODE_TELEMETRY_ENABLED=false
Environment=T3CODE_OTEL_SDK_DISABLED=true
```

この設定で、製品テレメトリ (`ingest.t3.codes`) と relay の OTLP tracing が止まり、環境変数を継承するバンドルエージェントの analytics connect-RPC も止まります。

ソース側でも止めたい場合は、T3 Code サーバのチェックアウトにパッチを適用します。環境変数がなくてもテレメトリがオプトイン式になります。

```sh
git -C <t3code-checkout> apply patches/0001-telemetry-opt-in-by-default.patch
```

パッチは 3 ファイルを変更します。テレメトリサービスの既定値を false にする、relay tracing を明示的な `T3CODE_TELEMETRY_ENABLED=true` があるときだけ起動する、契約テストを新しい挙動に合わせる、の 3 点です。

## セッションは置き換えても残る

セッション、スレッド、プロバイダ鍵、ログは `T3CODE_HOME` (既定 `~/.t3`) の下にあります。サーバのバイナリを差し替えても、drop-in を付けて再起動しても、これらはそのまま引き継がれます。

## ロールバック

```sh
sh scripts/rollback-phase2.sh
systemctl --user daemon-reload
systemctl --user restart t3code.service
```

## 注意

- `client-latest/` (`T3CODE_STATIC_DIR` が指す静的クライアントのビルド)、コンパイル済みの `t3_native_sqlite.node`、cargo の `target/` は git 管理外です。初回はクライアントを既存の T3 Code インストールからコピーし、インストール節のコマンドでアドオンをビルドしてください。
- サーバはループバックでのみ待ち受けます。drop-in 自体はネットワークから届くリスナーを開きません。
- drop-in の `T3CODE_RELAY_URL` と `T3CODE_CLERK_*` は、上流のリリースバイナリが埋め込む公開値です。T3 Connect を使わないなら削除してください。
