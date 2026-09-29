# TiDB権限付きRAG + Mem9権限検証デモ

このリポジトリには、TiDBを権限の正本として扱うPythonデモがあります。

1. TiDBだけで権限付きベクトル検索
2. Mem9の期間限定イベントによる検索順位の一時的な変更
3. Mem9の記憶に対する追加・論理削除権限

TiDBを文書・chunk・citation・権限の正本として使い、Mem9にはイベント名、
有効期間、ブースト対象chunk ID、強度だけを保存します。最終的な権限判定は
必ずTiDBで行い、Mem9が権限外のchunkを検索結果へ追加することはありません。

## セットアップ

`.env.example`を参考に、既存の`.env`へ設定します。

```env
TIDB_DATABASE_URL="mysql+pymysql://USER:PASSWORD@HOST:4000/DATABASE"
MEM9_API_URL="https://api.mem9.ai"
MEM9_API_KEY="your-mem9-api-key"
```

CA証明書はプロジェクト直下の`isrgrootx1.pem`を使います。

Mem9 APIキーをまだ持っていない場合は、公式のprovisioning endpointで
新しいspaceとキーを発行できます。返された`id`を`MEM9_API_KEY`へ設定します。

```bash
curl -sX POST https://api.mem9.ai/v1alpha1/mem9s
```

## デモ1: 権限付き検索

```bash
uv run python rag_mvp.py demo-permissions
```

同じ質問でも、public、follower、team、ownerで取得できるchunkが変わります。
デモ専用の`rag_demo_*`テーブルだけを初期化します。

## デモ2: Mem9期間限定イベント

最初にイベントをMem9へ登録します。サンプルイベントは
2026年6月1日から2026年6月26日まで有効です。

```bash
uv run python rag_mvp.py seed-event
uv run python rag_mvp.py demo-event
```

イベント期間中は、通常検索では2位以下の特設ガイドが一時的に1位へ上がります。
期限後はイベントが無視され、通常順位へ自動的に戻ります。

Mem9 APIキーをまだ用意していない場合は、同じ形式の固定イベントを使って
期間判定と再順位付けだけ確認できます。このモードはMem9 APIへ接続しません。

```bash
uv run python rag_mvp.py demo-event --offline
```

期限後の挙動を再現する場合:

```bash
uv run python rag_mvp.py demo-event \
  --offline \
  --at 2026-06-27T00:00:00+09:00
```

2つを続けて実行する場合:

```bash
uv run python rag_mvp.py demo-all --offline
```

## 注意

`rag_mvp.py`の`toy_embedding()`は、外部の埋め込みAPIなしで挙動を説明する
ための4次元ベクトルです。本番用途では利用する埋め込みモデルへ置き換えます。

Mem9のイベント分類は`metadata.kind=temporary_event_boost`に保存し、
`active_from`と`active_until`をアプリ側で必ず検証します。公式APIの
`memory_type`には`pinned`を使用しています。

イベントの適用順序は次の通りです。

1. TiDBでユーザーが閲覧できるchunkだけを検索する
2. Mem9から質問に関連するイベントを検索する
3. 有効期間内のイベントだけを採用する
4. 権限確認済みの結果にだけブーストを適用する

## テスト

```bash
uv run python -m unittest discover -s tests -v
```

## Mem9の記憶に対する操作権限の検証

`mem9_permissions_demo.py`は、次のポリシーをMem9実APIで比較します。

- A、B: 記憶の追加のみ
- C: 記憶の追加と論理削除

```bash
uv run python mem9_permissions_demo.py
```

Mem9のSpace API key自体は作成・更新・削除で共通です。
`X-Mnemo-Agent-Id`は実行者の記録には使われますが、A/B/Cの認可境界では
ありません。そのため、このデモではMem9 API keyを利用者へ渡さず、信頼済みの
`Mem9PermissionGateway`が先に操作権限を確認します。

デモは、ゲート経由ではAの削除が拒否されCの削除が成功することに加え、同じ
API keyでゲートを迂回するとBの直接DELETEもMem9には受理されることを示します。
DELETE後は`state=deleted`で再取得し、物理削除ではなく論理削除であることを
確認します。

### TiDBを権限の正本にする統合検証

`mem9_tidb_permissions_demo.py`では、Pythonへ直書きした権限ではなく、TiDBの
次のデモ用テーブルを使ってMem9操作を認可します。

- `mem9_demo_actor_permissions`: A/B/Cの操作権限
- `mem9_demo_memory_registry`: Mem9記憶IDと状態の対応表
- `mem9_demo_audit_log`: 許可・拒否・論理削除の監査証跡

```bash
uv run python mem9_tidb_permissions_demo.py
```

AとBの追加はMem9へ転送されますが、削除はTiDBで拒否されるためMem9 APIを
呼びません。Cの削除だけがMem9へ転送され、Mem9の`state=deleted`確認後に
TiDB側の対応表と監査ログも更新されます。

2026年6月20日の実TiDB Cloud・実Mem9 API検証結果は
`verification/mem9_tidb_permissions_20260620.json`に保存しています。

## TiDB権限付きRAGの専用検証（期間限定処理なし）

`rag_tidb_permissions_demo.py`はMem9や期間限定イベントを一切呼ばず、TiDBの
認可条件とベクトル距離を1つのSQLで評価します。既存テーブルと衝突しない
`rag_acl_demo_*`テーブルだけを初期化します。

```bash
uv run python rag_tidb_permissions_demo.py
```

全体では質問に最も近い`private/draft`文書を用意し、public、follower、teamの
利用者には返らず、ownerにだけ返ることを検証します。埋め込みは外部APIなしで
再現できる説明用4次元ベクトルで、本番用モデルではありません。

実TiDB Cloudでの検証結果は`verification/rag_tidb_permissions_20260620.json`、
Zenn本文用の抜粋は`docs/zenn_rag_tidb_permission_excerpt.md`に保存しています。

Mem9権限検証の本文用抜粋は
`docs/zenn_mem9_tidb_permission_excerpt.md`に保存しています。

## 公開物について

このリポジトリに認証情報は含めていません。`.env`やMem9 APIキーを保存した
`key`ファイルはコミットしないでください。`isrgrootx1.pem`はTiDB Cloudへの
TLS接続で使う公開CA証明書です。
