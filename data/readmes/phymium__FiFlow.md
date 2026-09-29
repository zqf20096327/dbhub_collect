# FiFlow

[中文](#中文) · [English](#english)

![FiFlow 仪表盘 / FiFlow dashboard](FiFlow.png)

## 中文

FiFlow 是一款本地优先、单用户的个人财务应用，使用 Python 3.12、Streamlit、
SQLAlchemy、Alembic 和 SQLite 构建。它用于记录现金流、物品日均使用成本、
周期计划和手动投资数据。

所有个人数据只保存在项目目录的 `./data/` 下。FiFlow 不提供云端服务、券商连接、
实时行情或遥测功能。

### 主要功能

- 中英文界面，可随时切换语言，默认显示中文。
- 仪表盘展示净资产、现金流、预算进度、近期付款、提醒、投资概览和交易记录。
- 支持支出、收入、退款、转账、拆分交易以及交易归档。
- 跟踪耐用品、消耗品和订阅，并计算对应的使用成本。
- 现金流与使用成本是两个独立的分析口径，不会相加混用。
- 管理周期规则、月度预算、现金日历和提醒。
- 按账户手动记录投资配置，不连接实时行情。
- 支持 CSV 导入、重复数据审核、CSV/JSON 导出、SQLite 备份与恢复。

### 快速开始

需要安装 [uv](https://docs.astral.sh/uv/)，无需 Conda。

```bash
brew install uv
uv python install 3.12
uv sync --python 3.12
uv run streamlit run streamlit_app.py
```

然后打开终端中显示的本地地址，通常是 `http://localhost:8501`。首次启动只会创建
`data/fiflow.db`、`data/backups/`、`data/imports/` 和 `data/logs/`。

### 文档

- [安装与启动](docs/installation.md)
- [计算说明](docs/calculations.md)
- [本地数据与备份](docs/local-data-and-backups.md)

### 开发

```bash
uv run pytest -v
uv run ruff check src pages streamlit_app.py tests alembic
uv run pytest --cov=fiflow --cov-report=term-missing
```

## English

FiFlow is a local-first, single-user personal finance app built with Python 3.12,
Streamlit, SQLAlchemy, Alembic, and SQLite. It tracks cash flow, daily cost of use,
recurring plans, and manually entered investment data.

All personal data stays under `./data/` in the project directory. FiFlow has no cloud
service, broker connection, live price feed, or telemetry.

### Features

- Chinese and English interface with an in-app language switch; Chinese is the default.
- Dashboard for net worth, cash flow, budget progress, upcoming payments, reminders,
  investments, and recent transactions.
- Expenses, income, refunds, transfers, split transactions, and transaction archiving.
- Durable, consumable, and subscription tracking with cost-of-use calculations.
- Separate Cash Flow and Cost of Use reporting modes that are never added together.
- Recurring rules, monthly budgets, a cash calendar, and reminders.
- Manual investment allocation records by account, without a live market feed.
- CSV import with duplicate review, CSV/JSON export, and SQLite backup and restore.

### Quick start

Install [uv](https://docs.astral.sh/uv/). Conda is not required.

```bash
brew install uv
uv python install 3.12
uv sync --python 3.12
uv run streamlit run streamlit_app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`. The first
launch creates only `data/fiflow.db`, `data/backups/`, `data/imports/`, and `data/logs/`.

### Documentation

- [Installation](docs/installation.md)
- [Calculations](docs/calculations.md)
- [Local data and backups](docs/local-data-and-backups.md)

### Development

```bash
uv run pytest -v
uv run ruff check src pages streamlit_app.py tests alembic
uv run pytest --cov=fiflow --cov-report=term-missing
```

## 许可 / License

FiFlow 自有代码采用 [MIT License](LICENSE)。仓库内置的第三方 SVG 图标保留其
原始许可，详情请参阅 [第三方声明](THIRD_PARTY_NOTICES.md)。

FiFlow's original code is licensed under the [MIT License](LICENSE). Vendored
third-party SVG icons retain their upstream licenses; see the
[third-party notices](THIRD_PARTY_NOTICES.md) for details.
