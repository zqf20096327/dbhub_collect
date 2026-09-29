# TiDB Issue Monitor

GitHub の [`pingcap/tidb`](https://github.com/pingcap/tidb) リポジトリを定期的に監視し、**指定バージョンに関連するバグ Issue の新規登録・ステータス変化** を Slack に通知するシステムです。

**GitHub Actions** を使って動作するため、サーバーの用意は不要です。このリポジトリを Fork するだけで、誰でも同じ監視システムを即座に構築できます。

---

## 主な機能

- 監視対象バージョン・Slack URL・通知設定をすべて **GitHub Secrets** で管理（ソースコードへの直書き不要）
- Issue の状態を **TiDB** に保存し、前回との差分で変化を検知（重複通知防止）
- **6種類のイベント**を検知・通知（`NOTIFY_EVENTS` Secret でカスタマイズ可能）
- 毎日 JST 9:00 に自動実行（スケジュール変更可能）・手動実行にも対応

---

## 通知イベント仕様

`NOTIFY_EVENTS` Secret にカンマ区切りで指定します。

| イベント名 | トリガー | 通知例 |
|---|---|---|
| `OPEN` | バージョン関連バグ Issue が**新規作成**された | 初回検出時に通知 |
| `CLOSE` | 監視中の Issue が**クローズ**された | 修正済み・wontfix 等 |
| `REOPEN` | 一度クローズされた Issue が**再オープン**された | 修正が不完全だった等 |
| `LABEL_ADDED` | 監視中の Issue に**ラベルが追加**された | `severity/critical` が付いた等 |
| `LABEL_REMOVED` | 監視中の Issue から**ラベルが削除**された | バグラベルが外れた等 |
| `TITLE_CHANGED` | 監視中の Issue の**タイトルが変更**された | 内容が修正・明確化された等 |

**設定例:**

```
NOTIFY_EVENTS = OPEN,CLOSE,REOPEN,LABEL_ADDED
```

---

## システム構成

```
あなたの GitHub リポジトリ（このリポジトリ）
  ├── .github/workflows/monitor.yml   ← GitHub Actions ワークフロー
  └── scripts/monitor_issues.py       ← Issue 取得・フィルタリング・通知スクリプト

TiDB（外部）
  ├── issue_snapshots テーブル   ← Issue の最新状態を保存（変化検知・重複防止に使用）
  └── notification_log テーブル  ← 通知履歴ログ（デバッグ・監査用）
```

```
[GitHub Actions スケジューラー]
        ↓ 毎日 JST 9:00（または手動実行）
[monitor_issues.py]
  1. GitHub REST API で pingcap/tidb の新規・更新 Issue を取得（open/closed 両方）
  2. バグ関連ラベル（type/bug, bug, regression 等）でフィルタ
  3. タイトル・本文に TARGET_VERSION のキーワードが含まれるか確認
  4. TiDB の issue_snapshots と比較して変化を検知
     （OPEN / CLOSE / REOPEN / LABEL_ADDED / LABEL_REMOVED / TITLE_CHANGED）
  5. NOTIFY_EVENTS に含まれるイベントのみ Slack に通知
  6. TiDB の issue_snapshots を最新状態に更新
  7. 通知履歴を TiDB の notification_log に記録
```

---

## TiDB のテーブル設計

### `issue_snapshots` テーブル

Issue の「最後に確認した状態」を保存します。前回との差分で変化を検知します。

| カラム | 型 | 説明 |
|---|---|---|
| `issue_number` | INT | Issue 番号（PK） |
| `repo` | VARCHAR(128) | リポジトリ名（PK） |
| `title` | TEXT | Issue タイトル |
| `state` | VARCHAR(16) | `open` または `closed` |
| `labels` | TEXT | ラベル名の JSON 配列 |
| `html_url` | VARCHAR(512) | Issue の URL |
| `first_seen_at` | DATETIME | 初回検出日時（UTC） |
| `last_checked_at` | DATETIME | 最終確認日時（UTC） |

### `notification_log` テーブル

通知した履歴を記録します。デバッグ・監査に使用します。

| カラム | 型 | 説明 |
|---|---|---|
| `id` | BIGINT | 自動採番（PK） |
| `issue_number` | INT | Issue 番号 |
| `repo` | VARCHAR(128) | リポジトリ名 |
| `event_type` | VARCHAR(32) | イベント種別 |
| `detail` | TEXT | 変化の詳細 |
| `notified_at` | DATETIME | 通知日時（UTC） |

---

## セットアップ手順

### ステップ 1: このリポジトリを Fork する

1. GitHub でこのリポジトリを開き、右上の **Fork** ボタンをクリックします。
2. 自分のアカウントに Fork されたリポジトリが作成されます。

> **ポイント:** Fork することで、設定（Secrets）は自分のリポジトリに独立して管理されます。他の人と共有する場合も、それぞれが Fork して自分の設定・通知先を持てます。

---

### ステップ 2: TiDB を用意する

Issue の状態管理に TiDB が必要です。以下のいずれかを選択してください。

**オプション A: TiDB Cloud Zero（無料・すぐ使える）**

```bash
curl -X POST https://zero.tidbapi.com/v1alpha1/instances \
  -H "Content-Type: application/json" \
  -d '{"tag": "tidb-issue-monitor"}'
```

レスポンスの `connection.host`, `port`, `username`, `password` を使って DSN を組み立てます。

**オプション B: TiDB Cloud Serverless（永続利用）**

[TiDB Cloud](https://tidbcloud.com) でアカウントを作成し、Serverless クラスターを作成します。

**DSN の形式:**

```
mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/test?ssl_verify_cert=false&ssl_verify_identity=false
```

**テーブルの初期作成は不要です。**

`monitor_issues.py` は初回実行時に接続先 TiDB へ必要なテーブルを自動作成します（`CREATE TABLE IF NOT EXISTS`）。DSN を Secrets に登録するだけで動作します。

---

### ステップ 3: Slack Incoming Webhook を取得する

1. [Slack API: Your Apps](https://api.slack.com/apps) を開き、**Create New App** をクリックします。
2. **From scratch** を選択し、アプリ名（例: `TiDB Issue Monitor`）とワークスペースを設定します。
3. 左メニューの **Incoming Webhooks** を開き、**Activate Incoming Webhooks** をオンにします。
4. **Add New Webhook to Workspace** をクリックし、通知を送りたいチャンネルを選択します。
5. 表示された Webhook URL（`https://hooks.slack.com/services/...`）をコピーします。

---

### ステップ 4: GitHub Secrets を設定する

Fork したリポジトリの **Settings → Secrets and variables → Actions** で以下を登録します。

| Secret 名 | 値の例 | 説明 |
|---|---|---|
| `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/services/...` | Slack Webhook URL |
| `TARGET_VERSION` | `v8.5.5` | 監視対象の TiDB バージョン |
| `TIDB_DSN` | `mysql+pymysql://user:pass@host:4000/test?...` | TiDB 接続文字列 |
| `NOTIFY_EVENTS` | `OPEN,CLOSE,REOPEN,LABEL_ADDED` | 通知するイベント（カンマ区切り）。省略時は `OPEN` のみ |
| `MIN_SEVERITY` | `critical` | 通知する最低 severity。省略時は `critical` のみ |

> **補足:** `GITHUB_TOKEN` は GitHub Actions が自動で提供するため、手動での登録は不要です。

---

### ステップ 5: ワークフローを有効化して動作確認する

1. Fork したリポジトリの **Actions** タブを開きます。
2. 「I understand my workflows, go ahead and enable them」ボタンが表示されていればクリックします。
3. **TiDB Issue Monitor** を選択し、**Run workflow** で手動実行します。
4. `lookback_hours` に `720`（30日分）などを入力して実行すると、過去の Issue が一括検出されます。

---

## カスタマイズ

### 監視バージョンを変更する

GitHub Secrets の `TARGET_VERSION` を更新するだけです。ソースコードの変更は不要です。

### 通知イベントを変更する

GitHub Secrets の `NOTIFY_EVENTS` を更新します。例えばクローズ通知だけ受け取りたい場合:

```
NOTIFY_EVENTS = CLOSE
```

### 実行スケジュールを変更する

`.github/workflows/monitor.yml` の cron 式を変更します。

| cron 式 | 実行タイミング |
|---|---|
| `0 0 * * *` | 毎日 JST 9:00 |
| `0 0 * * 1` | 毎週月曜 JST 9:00 |
| `0 */6 * * *` | 6時間ごと |

### バグラベルを追加・変更する

`scripts/monitor_issues.py` の `BUG_LABELS` リストを編集します。

---

## よくある質問

**Q: TiDB Cloud Zero は無料ですか？**

A: はい。TiDB Cloud Zero はサインアップ不要・無料で使えます。インスタンスは30日で自動削除されますが、表示される Claim URL からアカウントに紐づけることで永続利用できます。

**Q: GitHub Actions の無料枠はどれくらいですか？**

A: パブリックリポジトリでは無制限、プライベートリポジトリでは月 2,000 分まで無料です。本ワークフローは 1 回あたり 1 分未満で完了します。

**Q: 他のリポジトリも監視できますか？**

A: `.github/workflows/monitor.yml` の `REPO` 環境変数を変更することで、任意のリポジトリを監視できます。

---

## ライセンス

MIT License
