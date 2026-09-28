# Capability Space

> A learner-owned adaptive knowledge space.

把目标、学习材料和代码项目转化为可自由探索的能力空间，并严格区分学习活动、
可信证据和真实掌握。

```text
Activity != Evidence != Mastery
```

**Explore freely. Learn with evidence.**

## 最快开始（Windows）

将分发包完整解压到较短路径（推荐 `C:\Capability-Space`），然后双击
`打开 Capability Space.cmd`。首次启动会自动创建
独立的 `.runtime` 环境、安装必要 Python 组件、初始化本地数据库并导入基础
Probability 内容；前端已经预先构建，不要求安装 Node.js。日常启动不会再重复安装。

首次启动要求电脑已安装 Python 3.11 或更高版本，并且可以访问互联网。

分发包不包含开发者的数据库、API Key、虚拟环境、测试缓存或 `node_modules`。
AI 功能可以在产品右上角“设置”中配置 OpenAI 或 DeepSeek。

本项目采用 [MIT License](LICENSE)。

Capability Space is local-first and built on a thin Python + SQLite core. Raw
EvidenceEvent history is persisted; mastery remains a replaceable derived
estimate; InterviewEvidence remains a market signal rather than personal mastery.

## Requirements

- Python 3.11+
- SQLite (bundled with Python)
- `pytest` for tests
- Node.js 22+ and pnpm for the Chinese Beta web client

## Setup

```powershell
cd capability-space
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Initialize a local database

```powershell
python -m capos.cli init --db data/capos.sqlite3
```

The command applies all numbered migrations in order and enables SQLite foreign keys for the connection it opens.

## Import Probability Content V0

From the project directory, import the approved 45 capabilities and 75 external assessment references:

```powershell
python -m capos.cli import-probability --db data/capos.sqlite3
```

The importer reads the approved CSV files from the parent `outputs` directory by default. It validates all references and the prerequisite DAG before a single transactional, idempotent import. External source text is not copied into the database.

## Probability Initial Diagnostic

Start the fixed 15-reference diagnostic and display its first external assessment reference:

```powershell
python -m capos.cli diagnostic start probability --db data/capos.sqlite3 --subject local-user
python -m capos.cli diagnostic next --db data/capos.sqlite3
```

`diagnostic next` defaults to a readable assessment launch card. Use `--format json` when structured output is needed by scripts.

After completing the referenced assessment externally, record a result and continue:

```powershell
python -m capos.cli diagnostic answer --db data/capos.sqlite3 --result correct --independent --hints 0 --duration-seconds 300 --self-rating 4
python -m capos.cli diagnostic status --db data/capos.sqlite3
python -m capos.cli diagnostic next --db data/capos.sqlite3
```

Repeat `next` and `answer` through all 15 references, then derive replayable `heuristic_v0` estimates:

```powershell
python -m capos.cli diagnostic finish --db data/capos.sqlite3
```

Use `--assisted` instead of `--independent` when applicable, and add `--notes "..."` for a self-report. Every `answer` appends a new private EvidenceEvent; starting a later diagnostic never overwrites earlier attempts.

## Test

```powershell
pytest
```

## Chinese Beta product

完成一次安装和前端构建后，日常使用不需要再打开命令行。项目根目录提供
`双击启动 Capability Space.vbs`，它会在后台启动本地服务并打开浏览器；如果服务已经运行，则只打开产品页面。

如果双击后没有打开页面，运行项目根目录中的 `打开 Capability Space.cmd`。失败时窗口会保持打开并显示原因，详细服务日志位于 `data/launcher-server-error.log`。

Build the local React client once, then start the loopback-only Python product
server:

```powershell
cd web
pnpm install
pnpm build
cd ..
python -m capos.cli web --db data/capos.sqlite3 --port 8765
```

Open `http://127.0.0.1:8765`. The server binds only to `127.0.0.1`, validates
the exact Host and browser Origin on mutations, and uses a process-local session
token. It does not enable permissive CORS or cloud authentication.

For frontend development, run the backend with the single approved development
origin and start Vite in another terminal:

```powershell
python -m capos.cli web --db data/capos.sqlite3 --port 8765 `
  --development-origin http://127.0.0.1:5173
cd web
pnpm dev
```

The learner-facing surface is Chinese-native and includes 首页、学习、能力地图、
进展 and 数据源. Main/side quests, breakthroughs, milestones, weekly reviews and
share cards are derived projections; they are not new persisted domain truth.
The dedicated browser import route accepts bounded JSON/NDJSON/CSV files up to
10 MiB while ordinary JSON endpoints retain a 1 MiB body limit.

### AI teaching provider

The local teaching runtime supports either OpenAI or DeepSeek. Credentials are
read from the local process environment and are never stored in SQLite or the
browser.

OpenAI configuration:

```powershell
[Environment]::SetEnvironmentVariable("CAPOS_MODEL_PROVIDER", "openai", "User")
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_KEY", "User")
```

DeepSeek configuration:

```powershell
[Environment]::SetEnvironmentVariable("CAPOS_MODEL_PROVIDER", "deepseek", "User")
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "YOUR_KEY", "User")
```

DeepSeek defaults to `deepseek-v4-flash`. To override it:

```powershell
[Environment]::SetEnvironmentVariable("CAPOS_DEEPSEEK_MODEL", "deepseek-v4-flash", "User")
```

Fully exit and reopen the local application after changing provider settings.

Frontend verification:

```powershell
cd web
pnpm test
pnpm build
pnpm test:e2e
```

## Smoke example

`tests/test_smoke.py` creates a temporary database and verifies this chain:

```text
Domain -> Capability -> Assessment -> Mapping -> EvidenceEvent history
       -> heuristic_v0 EstimatorRun -> MasteryEstimate
```

`heuristic_v0` is only a transparent replayable baseline. It is not a scientific mastery algorithm.

## Passive external-source acquisition

External history is imported as provenance-first `SourceObservation` data. It
does **not** change mastery unless an existing reviewed Assessment resolution
and Capability mapping allow the evidence-qualification policy to create an
`EvidenceEvent`.

Connect a public Codeforces handle:

```powershell
python -m capos.cli connector connect codeforces `
  --db data/capos.sqlite3 `
  --subject local-user `
  --handle YOUR_HANDLE `
  --accept-consent-policy passive_acquisition_v0
```

The normal Chinese Beta UI supports selected public GitHub repositories only and
never asks a consumer for a token, secret reference, or environment-variable
name. The advanced CLI can still use a separately configured fine-grained
read-only token for private repositories; the token value is resolved only in
memory and is never stored in SQLite.

```powershell
$env:CAPOS_GITHUB_TOKEN = "..."
python -m capos.cli connector connect github `
  --db data/capos.sqlite3 `
  --subject local-user `
  --account YOUR_LOGIN `
  --repo owner/repository `
  --token-env CAPOS_GITHUB_TOKEN `
  --accept-consent-policy passive_acquisition_v0
```

Run one sync or the lightweight in-process worker:

```powershell
python -m capos.cli connector sync --all --once --db data/capos.sqlite3
python -m capos.cli connector worker --interval-seconds 900 --db data/capos.sqlite3
```

The worker is not installed as an operating-system service and only runs while
the process is active.
