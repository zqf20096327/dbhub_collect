# Stock Technical Analysis Skill

一个用于 A 股个股和自定义板块技术分析的 Codex Skill。它直接通过 Python `eltdx` 获取行情数据，维护独立 SQLite 缓存，并输出多周期技术指标分析。

> 技术分析结果仅用于研究和决策辅助，不构成投资建议。

## Demo

![Demo](images/demo.png)

## Features

- 直接使用 `eltdx` 拉取 A 股 K 线数据
- 独立 SQLite 数据库缓存，不依赖外部项目数据库
- 每次运行自动更新最新行情数据
- 支持个股和自定义板块分析
- 支持 `1d`、`5m`、`15m`、`30m`、`60m`、`120m`
- `120m` 优先尝试原生 eltdx 数据，失败后自动 fallback 到 `60m` 重采样
- 输出 Markdown 或 JSON
- 覆盖常用技术指标：MA、KDJ、SKDJ、RSI、ENE、DMA、MACD、BIAS、BOLL、LON

## Project Structure

```text
stock-tech-analysis/
+-- SKILL.md
+-- README.md
+-- agents/
|   +-- openai.yaml
+-- references/
|   +-- eltdx-data.md
+-- scripts/
    +-- analyze.py
```

运行时会自动创建缓存数据库：

```text
data/stock-tech-analysis.db
```

建议在 GitHub 仓库中忽略 `data/*.db`，因为它是本地行情缓存。

## Requirements

- Python 3.10+
- `eltdx`
- `pandas`
- `numpy`

安装依赖：

```bash
pip install eltdx pandas numpy
```

## Quick Start

分析个股并自动更新缓存：

```bash
python scripts/analyze.py --symbol 000001.SZ --kind stock --periods all --format markdown
```

分析指定周期：

```bash
python scripts/analyze.py --symbol 600519.SH --kind stock --periods 1d,60m,120m --limit 500 --format markdown
```

只使用已有缓存，不请求 eltdx：

```bash
python scripts/analyze.py --symbol 000001.SZ --kind stock --periods 1d --no-fetch --format json
```

## Sector Analysis

`eltdx` 本身不提供可靠的概念/行业板块成分查询，所以板块由用户显式提供成分股。第一次运行时传入 `--members`，脚本会把板块成分保存到自己的 SQLite 数据库。

```bash
python scripts/analyze.py \
  --symbol 白酒 \
  --kind sector \
  --members 600519.SH,000858.SZ,000568.SZ,600809.SH \
  --periods 1d,60m,120m \
  --format markdown
```

之后可以直接复用该板块：

```bash
python scripts/analyze.py --symbol 白酒 --kind sector --periods 1d,60m --format markdown
```

板块 K 线由成员股 K 线等权合成。

## Supported Indicators

| Category | Indicators |
| --- | --- |
| Moving Average | `ma5`, `ma10`, `ma20`, `ma30`, `ma60`, `ma120`, `ma180`, `ma250`, `ma360` |
| KDJ | `kdj_k`, `kdj_d`, `kdj_j` |
| SKDJ | `skdj_k`, `skdj_d`, `skdj_j` |
| RSI | `rsi6`, `rsi12`, `rsi24` |
| ENE | `ene_upper`, `ene_mid`, `ene_lower` |
| DMA | `dma_dif`, `dma_ama` |
| MACD | `macd_dif`, `macd_dea`, `macd_hist` |
| BIAS | `bias5`, `bias10`, `bias20`, `bias30`, `bias60`, `bias120`, `bias180`, `bias250`, `bias360` |
| BOLL | `boll_upper`, `boll_mid`, `boll_lower` |
| LON | `lon`, `lon_ma` |

## 120m Data Strategy

`120m` 周期采用原生优先策略：

1. 先尝试 `client.get_kline_all("120m", symbol)`
2. 如果成功，将数据写入 SQLite，周期标记为 `120m`
3. 如果 eltdx 版本或服务器不支持，或返回空数据，则刷新/读取 `60m`
4. 使用 `60m` 数据本地重采样生成 `120m` 分析结果

fallback 生成的 `120m` 不会写成伪原生缓存，避免混淆数据来源。

## CLI Options

```bash
python scripts/analyze.py --help
```

常用参数：

| Option | Description |
| --- | --- |
| `--symbol` | 个股代码或板块名称，例如 `000001.SZ`、`600519.SH`、`白酒` |
| `--kind` | `stock` 或 `sector` |
| `--periods` | `all` 或逗号分隔周期，例如 `1d,60m,120m` |
| `--start` | 起始日期或时间 |
| `--end` | 结束日期或时间 |
| `--limit` | 指标计算使用的最大 K 线数量 |
| `--db-path` | 自定义 SQLite 数据库路径 |
| `--members` | 板块成分股列表 |
| `--sector-member-limit` | 板块最多使用的成分股数量 |
| `--hosts` | 自定义 eltdx 服务器列表 |
| `--timeout` | eltdx 请求超时时间 |
| `--no-fetch` | 仅分析缓存，不请求 eltdx |
| `--format` | `markdown` 或 `json` |

## As A Codex Skill

该目录本身也是一个 Codex Skill。将 `stock-tech-analysis` 放入 Codex skills 目录后，可通过 `$stock-tech-analysis` 触发。

技能说明在：

```text
SKILL.md
```

OpenAI/Codex UI 元数据在：

```text
agents/openai.yaml
```

## Notes

- 数据源为 `eltdx`，实际可用周期取决于安装版本和可连接的行情服务器。
- 长周期均线如 `ma250`、`ma360` 需要足够多的历史 K 线，否则会输出数据不足提示。
- 自定义板块依赖用户维护成分股列表。
- 本项目不会读取其他项目的数据库。

## License

本项目基于 GNU General Public License v3.0 开源。

详细条款请查看 `LICENSE` 文件。

## Acknowledgements

感谢 [electkismet/eltdx](https://github.com/electkismet/eltdx) 提供 Python `eltdx` 行情数据接口，本技能的数据获取能力基于该项目实现。
