# LotteryStudio · 开奖研究所

> 双色球 & 大乐透 —— 历史数据分析、技术指标、策略回测与模拟投注的一体化平台。
> **纯本地运行**：后端 Python + 前端 Vue3，数据落在本机 SQLite，不上传任何数据。

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white)
![Release](https://img.shields.io/github/v/release/INDEXxiaoxia/LotteryStudio?display_name=tag)
![License](https://img.shields.io/badge/License-AGPL_v3-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows&logoColor=white)

---

## 直接下载使用（免安装）

不想装 Python / Node？直接下载打包好的单文件程序：

| 版本 | 文件 | 说明 |
| --- | --- | --- |
| v1.0 | [`LotteryStudio.exe`](https://github.com/INDEXxiaoxia/LotteryStudio/releases/latest) | 约 25 MB，双击即启动独立窗口，无需任何环境 |

- 数据库自动创建在 **exe 同目录的 `data/lottery.db`** —— 把 exe 拷到 U 盘/别的机器，数据一起带走。
- 依赖 **Microsoft Edge WebView2 Runtime**（Win10/11 一般已预装，缺失时系统会提示安装）。
- 首次启动稍慢（需自解压），之后正常。
- exe 未做代码签名，Windows SmartScreen 可能提示「未知发布者」，选择「更多信息 → 仍要运行」即可。

> 想从源码运行或自己改代码 → 见下方[快速开始](#快速开始)。

---

## 功能

| 模块 | 说明 |
| --- | --- |
| **历史数据** | 稳定抓取双色球（中彩网官方）与大乐透（体彩官方）历史开奖，首次全量、之后仅增量追加；号码走势绘制为「号码星图」与频率/遗漏图表 |
| **最新推荐** | 结合热号 / 冷号 / 均衡 / 随机，生成下一期 5 注参考号码 |
| **技术指标分析** | 频率、遗漏、和值、跨度、奇偶比、大小比、三区分布、连号、重号、AC 值、质合、尾数等 |
| **策略回测** | 热号 / 冷号 / 守号 / 随机 / 条件组合 / 胆拖 六类策略，逐期生成并回测（**不使用未来信息**），输出中奖次数、各等奖注数、投入与回报 |
| **号码测试** | 自定义最多 5 注（支持复式），回测全部历史数据 |
| **模拟投注小游戏** | 设置初始余额、随机起始开奖日，沿真实开奖日历一期一买；支持复式与 双色球 / 大乐透 / 混合 三种模式，开奖日历严格贴合真实日期 |

---

## 技术栈与端口

| 端 | 技术 | 端口 |
| --- | --- | --- |
| 后端 | FastAPI + SQLAlchemy + SQLite + APScheduler | **26001** |
| 前端 | Vue 3 + Vite + Element Plus + ECharts + Pinia | **26002** |

后端内置定时任务：每日 **21:45** 在双色球（21:15）/ 大乐透（21:25）开奖后自动增量刷新。

---

## 快速开始

> **所有命令都在项目根目录执行，无需 `cd` 到 `backend/` 或 `frontend/`。**

前置要求：**Python 3.11+**、**Node 18+** 与 **pnpm**。

### 方式一：一键启动（推荐）

```powershell
# 项目根目录：自动创建虚拟环境、装依赖，并同时拉起前后端
.\scripts\start.ps1
```

### 方式二：分步启动（两个终端）

**终端 1 —— 后端（:26001）**

```powershell
# 首次需装依赖（只需一次）
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt

# 启动后端
.\venv\Scripts\python.exe backend\run.py
```

**终端 2 —— 前端（:26002）**

```powershell
# 首次需装依赖（只需一次）
pnpm install --dir frontend

# 启动前端
pnpm --dir frontend dev
```

打开 **<http://127.0.0.1:26002>** ，先在「数据」页点击**更新数据**抓取历史开奖，再使用其它功能。

<details>
<summary>习惯先 <code>cd</code> 进子目录？等价写法</summary>

```powershell
# 终端 1：后端
cd backend
..\venv\Scripts\python.exe -m pip install -r requirements.txt   # 首次
..\venv\Scripts\python.exe run.py

# 终端 2：前端
cd frontend
pnpm install      # 首次
pnpm dev
```

</details>

---

## 桌面版（打包为 exe）

无需安装 Python / Node，双击即以**独立窗口**运行。

### 一键打包

> **改了前端（Vue）或后端（Python）代码后，只需重跑下面的打包命令**：脚本会自动重新编译前端 `dist` 并重新打包后端，无需其它手工步骤。exe 在打包时已把前后端一起打入，改代码后必须重新打包才会生效。

```powershell
.\packaging\build.ps1            # onedir 文件夹（exe + 依赖，启动轻快）
.\packaging\build.ps1 -OneFile   # 单文件 exe（推荐，拷走即用）
.\packaging\build.ps1 -Console   # 带控制台窗口（排查问题用）
```

也可用 `packaging\build.bat`（适合 cmd 或直接双击，参数同 `.ps1`，例如 `build.bat -OneFile`）。

产物在 `packaging/dist/`：单文件为 `LotteryStudio.exe`，onedir 为 `LotteryStudio/` 文件夹（内含同名 exe）。

### 运行与数据

- 数据目录为 **exe 同目录 `data/`**；端口冲突会弹窗提示，可用环境变量换端口：

  ```powershell
  $env:LOTTERY_BACKEND_PORT=26100
  .\LotteryStudio.exe
  ```

- 依赖 Microsoft Edge WebView2 Runtime（Win10/11 一般已预装）。

### 打包原理（对原程序的最小改造）

核心业务与前端页面**零改动**，仅三处向后兼容的小改：

- `backend/app/config.py` —— 数据/静态资源目录在打包后正确解析
- `backend/app/main.py` —— 托管前端静态文件 + SPA 回退
- `backend/app/schedulers.py` —— 直接实例化 `CronTrigger`，规避打包后 `entry_points` 失效

其余为新增文件（`backend/desktop.py`、`backend/requirements-desktop.txt`、`packaging/`），原开发流程（`start.ps1` / `pnpm dev` / `pytest`）不受影响。

---

## 目录结构

```
backend/
  run.py                 # 后端启动（:26001）
  desktop.py             # 桌面版入口（pywebview 窗口）
  app/
    main.py              # FastAPI 应用与路由
    config.py            # 配置（路径/端口/抓取参数/假设奖金）
    db.py / models.py    # SQLite ORM
    datalayer.py         # 统一数据读取
    fetcher/             # 双色球/大乐透数据源 + 增量抓取
    lottery/             # 玩法规则 / 组合数学 / 中奖判定
    engines/             # 分析 / 推荐 / 策略 / 回测 / 小游戏引擎
    api/                 # REST 路由
    schedulers.py        # 每日开奖后增量刷新
  tests/                 # pytest 单元测试（数据目录自动隔离）
frontend/
  src/views/             # 数据 / 推荐 / 分析 / 策略回测 / 号码测试 / 模拟投注
  src/components/        # 号码球 / 号码矩阵 / 图表封装
packaging/               # PyInstaller 打包脚本与 spec
scripts/start.ps1        # 一键启动
```

---

## 测试

```powershell
# 项目根目录执行（41 个用例）
.\venv\Scripts\python.exe -m pytest backend\tests -q
```

测试会把数据目录隔离到临时目录，因此**不受本机已抓取的历史数据影响**，可重复运行。

---

## 常见问题

- **端口被占用**：后端端口在 `backend/app/config.py`（`BACKEND_PORT`），前端端口在 `frontend/vite.config.js`（`port`），改完需同步 `frontend/vite.config.js` 里 `/api` 的反代目标。桌面版可用 `LOTTERY_BACKEND_PORT` 环境变量覆盖。
- **「更新数据」失败**：需本机能访问中彩网 / 体彩网；若网络受限会提示「抓取失败」，网络恢复后重试即可（已抓取的数据不会丢，支持断点续抓）。
- **`ImportError: No module named ...`**：说明依赖未装好，回到[快速开始](#快速开始)执行安装命令。
- **图表为空 / 无数据提示**：先到「数据」页确认历史期数 > 0，否则先点「更新数据」。
- **改了代码但 exe 没变化**：exe 内已固化前后端资源，必须重新执行 `packaging\build.ps1`。

---

## 说明与免责声明

- 数据来源为**中彩网**（双色球）与**体彩官网**（大乐透）公开开奖接口，仅用于研究与学习；若接口策略变化只需调整 `fetcher` 中各 Provider。
- 单注统一按 **2 元**计（大乐透「追加投注」默认关闭）。
- **一等奖 / 二等奖为浮动奖**，历史回测中默认只统计中奖注数；启用「按假设金额」时使用可配置的占位金额（双色球 500 万 / 150 万，大乐透 1000 万 / 20 万），仅供 ROI 曲线与游戏余额结算参考。
- 所有推荐与分析结果均为统计参考，**不构成任何投注建议**。彩票为概率游戏，请理性对待。

---

## 许可证

本项目采用 **AGPL-3.0（或更高版本）+ 商业授权** 的双许可模式，版权归 © 2026 INDEXxiaoxia 所有。

| 使用场景 | 是否需要商业授权 |
| --- | --- |
| 个人学习、研究、自用 | ❌ 不需要 |
| 公司内部自用（遵守 AGPL-3.0） | ❌ 不需要 |
| 二次开发后同样以 AGPL-3.0 开源 | ❌ 不需要 |
| **闭源**用于商业产品分发 | ✅ 需要 |
| 部署为**对外网络服务**且不愿公开源码 | ✅ 需要 |

- **愿意开源** → 直接按 AGPL-3.0 使用即可，**包括商业用途**。代价是：分发时必须提供源码，且若把修改版作为网络服务对外提供，须向使用者提供完整对应源码（AGPL 第 13 条）。
- **不想开源** → 请联系作者获取[商业授权](COMMERCIAL.md)。

完整条款见 [LICENSE](LICENSE)，授权细节见 [COMMERCIAL.md](COMMERCIAL.md)。