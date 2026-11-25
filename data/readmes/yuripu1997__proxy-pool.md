<div align="center">

# ProxyPool

### 免费代理池：定时抓取 · 严格测活 · 自动留存 · Web 面板 · 通用 API

**A self-hosted free proxy pool — scrape, verify, persist, serve.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yuripu1997/proxy-pool?style=social)](https://github.com/yuripu1997/proxy-pool)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](#contributing)

<p>
  <a href="#quick-start">Quick Start</a> ·
  <a href="#why">为什么做</a> ·
  <a href="#sources">IP 来源</a> ·
  <a href="#api">API</a> ·
  <a href="#architecture">架构</a> ·
  <a href="#deployment">部署</a>
</p>

</div>

---

> **中文**：一个零依赖的代理池服务。它从公开源定时抓取免费代理，用**真实目标实测**（不是只看状态码），
> 把能用的存进 SQLite，持续复检淘汰，最后通过 Web 面板和标准 HTTP 接口输出。
> 专门解决了「免费代理列表 95% 是死号」和「看起来活着其实连不上 OpenAI」两个痛点。
>
> **EN**: A zero-dependency proxy pool daemon. It scrapes public free-proxy lists on a schedule,
> verifies them against **real upstream targets**, keeps the survivors in SQLite, continuously
> re-checks and evicts dead ones, then serves them through a Web UI and plain HTTP endpoints.
> It fixes two problems with public proxy lists: **~95% are dead**, and many "alive" ones
> still can't reach real APIs.

---

## Why / 为什么做

<p align="center">
<img src="https://img.shields.io/badge/free%20proxy%20lists-95%25%20dead-red" alt="95% dead">
<img src="https://img.shields.io/badge/httpbin%20check-false%20positive-orange" alt="false positive">
<img src="https://img.shields.io/badge/our%20approach-real%20target%20probe-green" alt="real target probe">
</p>

公开代理列表有两个坑：

1. **列表里绝大部分是死号** —— 抓 16,000 条，真正能用的常常不到 10%。
2. **通用检测站会误杀** —— 用 `httpbin.org` 测，socks5 代理 `usable=0`；
   换成真实目标 `api.openai.com`，同样的代理有 **18.5% 能用**。

The public lists have two traps: most entries are dead, and generic echo endpoints
(httpbin) produce **false negatives** for SOCKS proxies. Verifying against the actual
upstream you care about changes the yield from **0% to ~18%** in our tests.

**所以这个项目做的是：不猜，直接打真实目标。** / **So we probe the real target. Don't guess.**

---

## Features / 特性

| 中文 | English |
|---|---|
| 🔄 定时抓取 15 个公开源，自动去重 | Scheduled scraping of 15 public sources with dedup |
| 🔬 严格测活：回显校验 + 随机 nonce 防缓存 + 透明代理识别 | Strict verification: echo check + nonce + transparent-proxy detection |
| 🎯 **真实目标探测**：直接打 `api.openai.com`，401/200 才算可用 | **Real-target probe**: 401/200 from `api.openai.com` means usable |
| 🏠 住宅 / 机房自动分类（ip-api ASN） | Residential / datacenter auto-classification via ASN |
| 🧹 连续失败自动淘汰，池子自我新陈代谢 | Automatic eviction after consecutive failures |
| 📊 Web 面板：筛选、搜索、统计、日志、在线改配置 | Web UI: filtering, search, stats, logs, live settings |
| 🔌 通用 API：`/proxy` 一行一个，直接 curl 就能用 | Plain HTTP API: one proxy per line, curl-friendly |
| 🤖 专用 feed：给 codex2api 等只认 GET 的软件对接 | Dedicated feed for clients that only send plain GET |
| 🔐 UI 登录密钥 + API Token + 限流 + 防爆破 | UI login key + API token + rate limiting + brute-force protection |
| 📦 零第三方依赖，Python 3.8+ 直接跑 | Zero pip dependencies, runs on Python 3.8+ |

---

## Sources / IP 来源

> **重要说明**：本项目**不生产、不购买、不转售**任何 IP。所有代理均来自下列公开渠道，
> 项目只是抓取 + 验证 + 管理。使用者需自行评估来源合法性与合规性。
>
> **Important**: This project **does not produce, buy, or resell** any IP addresses.
> All proxies come from the public sources listed below. The tool only scrapes, verifies,
> and manages them. Users should evaluate legality and compliance themselves.

### 公开列表源 / Public list sources（GitHub raw，定时更新）

| 源 Source | 协议 | 地址 URL | 更新频率 |
|---|---|---|---|
| **proxifly** | http / socks5 | `raw.githubusercontent.com/proxifly/free-proxy-list` | 每 5 分钟 |
| **TheSpeedX** | http / socks4 / socks5 | `raw.githubusercontent.com/TheSpeedX/PROXY-List` | 每天 |
| **monosans** | http / socks4 / socks5 | `raw.githubusercontent.com/monosans/proxy-list` | 每小时复检 |
| **vakhov** | http | `raw.githubusercontent.com/vakhov/fresh-proxy-list` | 每小时 |
| **hideip.me** | http | `raw.githubusercontent.com/zloi-user/hideip.me` | 每 10 分钟 |
| **roosterkid** | https | `raw.githubusercontent.com/roosterkid/openproxylist` | 每小时 |

### API 源 / API sources

| 源 Source | 协议 | 说明 |
|---|---|---|
| **ProxyScrape** | socks5 / http / socks4 | `api.proxyscrape.com/v4`，免费公开 API |
| **Webshare** | http | `proxy.webshare.io/api/v2`，免费套餐 10 个带认证的代理（需填 API Key） |

### 固定出口 / Static (optional)

| 类型 | 说明 |
|---|---|
| 自建 Clash / 自己的代理 | 通过 `static_proxies` 配置，永久保留、不参与淘汰 |

### 不同来源的实测命中率 / Measured yield by source

> 抽样 100~400 个候选，直接用 `api.openai.com` 探测的结果。
> Sampled 100–400 candidates, probed directly against `api.openai.com`.

| 源 Source | 池大小 | 可用率 Yield |
|---|---:|---:|
| **ProxyScrape SOCKS5** | 2,000 | **26–29%** 🏆 |
| **monosans SOCKS5** | 63 | **27%** |
| hideip.me | 210 | 23% |
| monosans HTTP | 453 | 15% |
| roosterkid | 150 | 12% |
| ProxyScrape HTTP | 753 | 12% |
| proxifly HTTP | 5,088 | 5% |
| proxifly SOCKS5 | 5,183 | 2.5% |
| speedx SOCKS5 | 1,621 | 2.5% |

**结论**：小源比大源干净 10 倍。项目默认优先从高命中率源直连入库。
**Takeaway**: small, frequently-refreshed lists beat huge stale ones by 10x.

---

## Screenshots / 界面预览

<details>
<summary><b>📊 面板主页 — 池子概览与代理列表 / Dashboard overview</b></summary>

![ProxyPool Dashboard](docs/dashboard.jpg)

实时统计：可用数、住宅/机房分布、OpenAI 可用数、平均延迟。支持按国家/协议/类型筛选、搜索、一键复制。
Live stats, filters by country/protocol/type, search, and one-click copy.

</details>

<details>
<summary><b>🔌 数据源管理 — 每个源可单独开关 / Source manager</b></summary>

![Proxy Sources](docs/sources.jpg)

每个源显示上次抓取时间、本次数量、累计抓取量、健康状态，可以单独启用/关闭。
Per-source status, fetch count, cumulative total, health, and enable/disable toggles.

</details>

---

## Quick Start

```bash
git clone https://github.com/yuripu1997/proxy-pool.git
cd proxy-pool

# 启动（默认 127.0.0.1:8787）
python3 server.py

# 打开面板
open http://127.0.0.1:8787
```

点 **「立即跑一轮 / Run now」**，一分钟后池子里就有数据了。

Zero dependencies — no `pip install` needed. Python 3.8+ only.

```bash
# 验证 / verify
curl http://127.0.0.1:8787/health
curl http://127.0.0.1:8787/proxy | head
```

---

## API

### 通用接口 / Generic endpoints

| 请求 | 返回 / Returns |
|---|---|
| `GET /proxy` | 纯文本，`scheme://host:port` 一行一个 |
| `GET /proxy?format=plain` | 只要 `host:port` |
| `GET /proxy?format=json` | JSON，含延迟 / ISP / 成功次数 |
| `GET /proxy/one` | 随机一个（从最快的那批里抽） |
| `GET /api/stats` | 统计、国家分布、上轮结果 |
| `GET /api/rounds` / `/api/logs` | 运行记录 / 日志 |

### 过滤参数 / Filters

| 参数 | 说明 | 示例 |
|---|---|---|
| `country` | ISO2 国家码 | `?country=US` |
| `scheme` | http / https / socks4 / socks5 | `?scheme=socks5` |
| `type` | `residential` / `datacenter` / `openai` | `?type=openai` |
| `limit` | 条数，**硬上限 100** | `?limit=20` |

```bash
# 20 个美国 SOCKS5 / 20 US SOCKS5
curl "http://HOST:8787/proxy?country=US&scheme=socks5&limit=20"

# 随机一个，直接用 / grab one and use it
P=$(curl -s http://HOST:8787/proxy/one)
curl -x "$P" https://httpbin.org/ip
```

### 专用 feed / Client feed

给只发 GET、不带认证头的客户端（如 codex2api）设计的只读接口：

```
GET /feed/<feed_key>
```

- 密钥在**路径**里，无需请求头 / key in path, no headers needed
- 只输出客户端支持的协议 / only supported schemes
- 默认只给 **OpenAI 实测可用** 的 / only verified-working proxies
- 单次最多 100 条 / max 100 per call

```bash
# 用坏了一个就回报，达到阈值立即下线
curl -X POST http://HOST:8787/api/report \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://1.2.3.4:8080","ok":0}'
```

---

## Architecture / 架构

```
   ┌──────────────────────────────────────────────────────┐
   │  Scheduler (every 30 min)                            │
   │        ↓                                             │
   │  15 sources ──→ dedup ──→ 2 paths:                   │
   │                    ├─ A: strict check (httpbin+TLS)  │
   │                    └─ B: direct OpenAI probe  🎯     │
   │        ↓                                             │
   │  SQLite pool (alive / history / stats / geo)          │
   │        ↓                  ↓                           │
   │   Web UI             Generic API + feed               │
   └──────────────────────────────────────────────────────┘
```

```
proxy-pool/
├── server.py          # HTTP server + scheduler + UI + API
├── core.py            # scrape / verify / SQLite / eviction
├── proxy-check.py     # strict verification engine
├── static/index.html  # single-file Web UI (no build step)
├── deploy/            # systemd + one-click installer
└── data/pool.db       # SQLite (auto-created)
```

**Why two verification paths?** / **为什么两条测活路径？**

Strict checking (echo + TLS) is accurate for HTTP proxies but produces **false negatives**
for SOCKS proxies. Direct probing against the real target has a higher yield for those.
Both paths run, and results are merged into one pool.

---

## Deployment / 部署

### systemd (Linux)

```bash
sudo bash deploy/install.sh          # installs to /opt/proxy-pool, port 8787
systemctl status proxypool
journalctl -u proxypool -f
```

### Docker

```bash
docker build -t proxy-pool .
docker run -d --name proxypool -p 8787:8787 \
  -v $(pwd)/data:/app/data --restart unless-stopped proxy-pool
```

### Security / 安全

> 绑公网务必加 token：`python3 server.py --bind 0.0.0.0 --token YOUR_KEY`
>
> Always set a token when binding to a public interface.

- UI 登录密钥 + HMAC 签名 Cookie（HttpOnly / SameSite）
- API 三种鉴权：`?token=` / `X-API-Token` / Cookie
- 登录失败限流（8 次/分钟）、API 限流（180 次/分钟）、IPv6 /64 归并防绕过
- 独立系统用户 + `NoNewPrivileges` + `ProtectSystem`

---

## Real-world data / 实测数据

Running continuously for 13 days on a 2-core VPS:

```
635 rounds · 57,145 candidates fetched · 12 countries
peak: 764 alive / 557 OpenAI-verified
current: 120 alive / 48 OpenAI-verified
```

Free proxies are **ephemeral** — the value of this tool is continuous refresh, not one-time scraping.

> ⚠️ 免费代理寿命以小时计。本项目价值在于**持续跑**，不是跑一次。
> 要稳定大量，建议接付费住宅代理（面板已预留 Webshare API Key 位置）。

---

## Contributing / 贡献

PRs welcome! Especially for:

- 新增代理源 / new proxy sources
- 更准的测活策略 / better verification heuristics
- 面板改进 / UI improvements

```bash
python3 -m unittest discover  # (tests welcome too)
```

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**如果对你有用，点个 ⭐ Star 吧！**
**If this helped, give it a ⭐ — it motivates more open-source work.**

[![Star History Chart](https://api.star-history.com/svg?repos=yuripu1997/proxy-pool&type=Date)](https://star-history.com/#yuripu1997/proxy-pool&Date)

</div>

---

<div align="center">

本项目在 [LINUX DO](https://linux.do) 社区首发分享，感谢社区佬友的反馈与支持。

<sub>This project was first shared on [LINUX DO](https://linux.do) — thanks to the community for the feedback and support.</sub>

</div>
