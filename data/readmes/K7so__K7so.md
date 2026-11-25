# K7so

**Agent 自动化渗透测试平台**

给它一个域名，它自己抓页面、读前端脚本、理接口，按你勾选的能力逐项验证，最后交出带请求包和响应包的漏洞清单。整个过程用对话完成，不选模块、不配策略。

FastAPI + 原生 HTML/CSS/JS + SQLite。运行时只依赖 4 个 Python 包，前端没有第三方库，数据只落在本机 `data/`。

> **免责声明**：本工具仅供已获得授权的安全测试使用。使用者的全部行为及其后果由使用者本人承担，作者仅提供工具，不对任何使用后果负责。

## 截图

| 仪表盘 | 智能工作（运行中） |
| --- | --- |
| ![](docs/screenshots/01-dashboard.png) | ![](docs/screenshots/02-chat-running.png) |
| **自动继续** | **模型能力** |
| ![](docs/screenshots/03-chat-autocontinue.png) | ![](docs/screenshots/04-capabilities.png) |
| **漏洞结果** | **资产监管** |
| ![](docs/screenshots/05-findings.png) | ![](docs/screenshots/06-assets.png) |
| **API 中心** | **审计日志** |
| ![](docs/screenshots/07-connectors.png) | ![](docs/screenshots/08-audit.png) |

## 功能

- **智能工作**　一句「把 example.com 测一遍」就开始。模型自己决定发包顺序，能跑命令、跑脚本、发原始 HTTP 请求，每步留一条进展。
- **模型能力**　64 项能力分 7 组，可设 1–5 权重和用户提示。勾了就一定验完，台账没清空这一轮不算结束。
- **资产监管**　xlsx/docx/pdf/txt/md 直接解析出域名和 IP；子域收集走前缀枚举、DNS 记录、证书日志三条路；模块按月对比新增与消失。
- **漏洞结果**　按主机名归组，一个站点一行，点开看 URL、说明、请求包、响应包。归档那一刻就推到对话里。
- **K7so 工具**　自己的 py/exe/jar/bin 放进来，用同一套界面运行，输出实时滚动。
- **API 中心**　28 个连接器：15 家大模型、6 家测绘、2 家情报、2 家漏洞平台，外加 Nmap/Nuclei/HTTPX 本地检测。
- **批量作业**　不对话也能跑：可用性 → 测绘 → 存活与配置 → 端口 → 模板检测 → AI 研判，进度可取消。
- **审计日志**　操作人、时间、来源、动作、目标、结果全留痕，界面上删不掉。

## 快速开始

需要 Python 3.10+。nmap、nuclei、java 可选，不装也能用其余功能。

```bash
python -m venv .venv
.venv\Scripts\activate            # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
python run.py                     # http://127.0.0.1:8000
```

Windows 也可以直接双击 `start.bat`。改端口用 `python run.py --port 9000`。

账号 `admin`，口令是首次启动随机生成的。随机口令写在 `data/初始口令.txt`，启动日志也会打一行，仓库里没有固定口令。想固定口令启动：

```bash
K7so_ADMIN_PASSWORD='你的口令' python run.py
```

进去后三步：API 中心填模型 Key 并检测 → 模型能力里勾要测的类型 → 智能工作里输入目标。

## 内置工具

| 工具 | 说明 |
| --- | --- |
| `http_request` | 内置 HTTP 客户端，返回状态码、头、体，以及可归档的请求包与响应包 |
| `run_shell` | 跑外部命令，Windows 走 `cmd /d /c`，类 Unix 走 `/bin/sh -c` |
| `run_python` | 跑 Python 脚本，返回输出和 traceback |
| `record_finding` | 归档漏洞：标题、等级、URL、影响、修复建议、报文、分步过程 |
| `report_capability` | 登记能力结论：found / clean / blocked / weak |
| `list_capabilities` | 重读能力快照 |
| `ask_choice` | 需要拍板时给 2–4 个可点选项 |
| `platform_overview` | 一次拿全资产、作业、漏洞、能力、连接器状态 |
| `list_assets` / `create_asset` | 资产台账查询与登记 |
| `start_scan` / `list_scans` / `get_scan` / `cancel_scan` | 批量作业的发起、查询、终止 |
| `list_findings` / `update_finding_status` | 查漏洞、流转状态 |
| `list_connectors` / `test_connector` / `test_all_connectors` | 连接器查询与检测 |
| `list_dir` / `read_file` / `write_file` | 记忆目录只读、工作目录可写，其余路径拒绝 |
| `read_memory` / `search_memory` | 分页读记忆、按关键词检索 |

共 24 个。破坏性操作在工具层就拦下：格式化、删根目录、关机、改引导、写业务数据、上传可执行文件、压测、爆破、落地后门、内网横向一律拒绝；读凭据和删文件各有一个询问开关。

## 测试能力

64 项，7 组。同类漏洞合并，勾一项覆盖该类全部常规手法。

| 分组 | 项数 | 内容 |
| --- | --- | --- |
| 注入攻击 | 16 | XSS（反射/存储/DOM）、SQL、NoSQL、ORM/HQL、SSTI、表达式、命令注入、反序列化、SSRF、XXE、LDAP、XPath、CRLF、GraphQL |
| 执行与文件 | 10 | RCE、动态执行、文件上传/读取/写入、LFI/RFI、压缩包穿越、源码与备份泄露、目录爆破、目录索引 |
| 认证与访问控制 | 15 | 未授权、IDOR、越权提升、批量赋值、弱口令、默认凭据、登录防爆破、密码重置、任意用户接管、注册、JWT 弱密钥、会话固定、OAuth/SSO、CSRF、开放重定向 |
| 业务逻辑 | 5 | 逻辑缺陷、支付篡改、并发竞态、限流缺失、批量导出 |
| 云与组件 | 7 | 云配置与元数据、对象存储、组件已知漏洞、中间件管理端、容器 API、K8s API、CI/CD 泄露 |
| 客户端与传输 | 4 | 原型链污染、postMessage、点击劫持、缓存欺骗 |
| 信息泄露 | 7 | 敏感信息、接口文档、详细报错、个人数据、日志文件、版本库、调试端点 |

「自动渗透」开关默认关闭：关着只测勾选项，开着则勾选项变底线，还会按暴露面找清单外的类型。CORS 宽松、缺安全头、版本指纹、Source Map 这类只进报告附录，不占漏洞条目。

## 大模型接入

15 个连接器，Claude 与 Gemini 走原生协议，其余 OpenAI 兼容。

| 连接器 | 默认地址 | 默认模型 |
| --- | --- | --- |
| NCC 大模型 | `https://ai.nccsec.cn/v1` | `cyber-model-1` |
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| OpenAI 兼容 | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Anthropic Claude | `https://api.anthropic.com` | `claude-sonnet-4-5-20250929` |
| Google Gemini | `https://generativelanguage.googleapis.com` | `gemini-2.0-flash` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
| Moonshot Kimi | `https://api.moonshot.cn/v1` | `kimi-k2` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4` | `glm-4.5` |
| 豆包 / 火山方舟 | `https://ark.cn-beijing.volces.com/api/v3` | 填自己的 `ep-…` |
| 腾讯混元 | `https://api.hunyuan.cloud.tencent.com/v1` | `hunyuan-turbos-latest` |
| 百度文心 | `https://qianfan.baidubce.com/v2` | `ernie-4.0-turbo-8k` |
| MiniMax | `https://api.minimax.chat/v1` | `MiniMax-M2` |
| 硅基流动 | `https://api.siliconflow.cn/v1` | `deepseek-ai/DeepSeek-V3` |
| Ollama | `http://127.0.0.1:11434/v1` | `qwen2.5:7b` |
| 自定义模型 | 自己填 | 自己填 |

「保存并检测」会真发一次 `max_tokens=16` 的补全，拿到回包才算接入。密钥用 Fernet 加密存在服务端，页面只显示 `sk-abc…7890`。目录里没有的模型走「自定义模型」，内网网关可以免 Key。

## 配置

环境变量统一 `K7so_` 前缀，旧 `MONO_` 前缀仍兼容，都有默认值。

| 变量 | 默认 | 作用 |
| --- | --- | --- |
| `K7so_DATA_DIR` | `./data` | 数据目录 |
| `K7so_ADMIN_USER` / `K7so_ADMIN_PASSWORD` | `admin` / 空 | 初始账号；口令留空则随机生成 |
| `K7so_MAX_OUTPUT_TOKENS` | `16000` | 单次输出上限 |
| `K7so_TURN_MAX_SECONDS` | `900` | 单轮时限 |
| `K7so_LEDGER_HARD_STEPS` | `1200` | 单轮步数硬上限 |
| `K7so_CONTEXT_CHAR_BUDGET` | `80000` | 上下文预算 |
| `K7so_HISTORY_CHAR_BUDGET` | `24000` | 历史对话预算 |
| `K7so_CMD_TIMEOUT` | `300` | 命令默认超时 |
| `K7so_STEP_STALL_SECONDS` | `300` | 看门狗静默阈值 |
| `K7so_MEMORY_PRELOAD` / `K7so_MEMORY_CHUNK` | `12000` / `16000` | 记忆预载与翻页字数 |
| `K7so_SHELL` | 自动 | 覆盖 shell |

其余截断与账本类阈值见 `mono/config.py`。界面里还有安全模式、并发、超时、UA、记忆与工作目录。

## 目录结构

```text
mono/
├── api/            接口层：auth / chat / capabilities / assets / kits / findings /
│                   scans / connectors / reports / dashboard / settings
├── engine/         agent（工具循环、提示词、收尾自检）、capabilities、coverage、
│                   watchdog、shell、scanner、asset_registry、kits、workspace
├── connectors/     连接器适配：llm / recon / platforms / tools
├── static/         index.html + style.css + app.js
├── db.py           SQLite 持久层与审计
├── security.py     口令哈希、Fernet、会话签名
└── main.py         FastAPI 装配
data/               运行时数据，不进仓库
tests/              1062 项回归测试
```

## 测试

```bash
python tests/run_all.py     # 1062 项，用临时数据目录，不动 data/
```

覆盖 agent 主循环、接口边界、设置项是否真生效、文件解析、看门狗、首次启动口令等十个文件。

## 使用边界

只对你拥有或已获书面授权的目标使用。压测、拒绝服务、密码爆破不在能力清单里，也会被工具层拒绝。默认监听 `127.0.0.1`，给别人用请先改口令；单用户模型，不要暴露到公网。报告里的漏洞信息属于敏感数据。

## 许可

运行依赖 FastAPI、Uvicorn、HTTPX、cryptography，均为宽松许可。前端全部手写，不含第三方库与字体文件。文中提到的第三方名称与接口地址只用于说明可接入哪些服务，商标归各自权利人所有。

MIT，见 [LICENSE](LICENSE)。
