# KLineRadar · A股技术形态选股与看盘终端

<p align="center">
  <a href="https://github.com/henryorpeter/baostock-visual-screener/stargazers">
    <img src="https://img.shields.io/github/stars/henryorpeter/baostock-visual-screener?style=for-the-badge&logo=star&logoColor=white&color=ffb703" alt="GitHub stars" />
  </a>
  <a href="https://github.com/henryorpeter/baostock-visual-screener/network/members">
    <img src="https://img.shields.io/github/forks/henryorpeter/baostock-visual-screener?style=for-the-badge&logo=git&logoColor=white&color=0284c7" alt="GitHub forks" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  </a>
  <a href="https://www.starlette.io/">
    <img src="https://img.shields.io/badge/Starlette%20%2B%20TradingView%20v5-Native%20Web-f6465d?style=for-the-badge" alt="Starlette + TradingView v5" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License" />
  </a>
</p>

> 🌟 **如果这个项目对你的日常复盘、技术形态选股或 Python 可视化有所启发，请动动手指在右上角点一个 Star ⭐️ 吧！**  
> 你的每一个 Star 都是作者持续优化代码、新增经典战法与维护数据接口的最大动力！欢迎点击上方按钮或仓库右上角加星关注更新 ↗️

---

基于 **Python（Starlette + Uvicorn）+ 离线 TradingView Lightweight Charts v5** 构建的本地 A 股技术形态选股与看盘终端。支持全市场历史日线本地 SQLite 缓存、20 套经典形态与指标策略极速扫描、多策略共振榜单、**暗色 / 亮色双主题一键切换**以及完整 **14 项 K 线技术指标**实时交互看盘。

> **免责声明**：本工具仅供技术形态研究与复盘学习参考，所有筛选信号与历史胜率统计均不构成任何投资建议。

<p align="center">
  <img src="./assets/demo.gif" alt="KLineRadar 原生 Web 看盘终端与全市场极速选股演示" width="100%" /><br />
  <sub><b>演示：秒开占位引导 → 流式实时选股进度条 → 暗黑交易所风格多副图 K 线（MA / BOLL / VOL / MACD / KDJ + 实时十字光标）→ 周线切换 → 亮色日间主题 → 20 套策略矩阵与本地缓存管理</b></sub>
</p>

---

## 核心特性

- **原生 Web 交易所级终端（零前端构建 + 暗/亮双主题）**：
  - 彻底脱离重型框架刷新闪烁，基于 `Starlette + Uvicorn` 与离线打包的 `TradingView Lightweight Charts v5.0.7` 打造；打开页面默认展示清爽选股占位页，**秒开不卡顿**，点击「开始选股」或按 `/` 搜索个股后即时进入看盘终端。
  - 右上角一键切换 **暗黑模式（OKX / TradingView 风格）** 与 **浅色日间模式**，K 线画布、网格与坐标轴实时同步换肤，并自适应桌面宽屏与手机移动端。
- **完整 14 项专业 K 线技术指标 + 实时十字光标读数**：
  - **周期切换**：日线 / 周线 / 月线无缝重采样，保留长周期前置均线与指标预热。
  - **6 项主图叠加**：`MA (5/10/20/30)`、`EMA (12/26/60)`、`BOLL (20, 2)`、`BBI`、`SAR`（抛物线转向点）、`KC`（肯特纳通道）。
  - **8 项同步副图**：`VOL (MA5/10)`、`MACD (12, 26, 9)`、`KDJ (9, 3, 3)`、`RSI (6/12/24)`、`WR (10/6)`、`CCI (14)`、`OBV (MA30)`、`ATR (14)`；支持多副图自由组合、鼠标拖拽调整高度，以及十字光标悬停实时 OHLCV 与副图角标数值联动。
- **纯 NumPy 极速离线选股 + 流式实时进度条**：
  - 全市场 5,200+ 只 A 股日线落盘至本地 `stock_cache.sqlite3` 并内置线程安全 LRU 数组缓存，**热缓存全市场扫描仅约 0.3 秒**，断网完全可用。
  - 选股接口采用 NDJSON 流式推送（`/api/screen/stream`），扫描期间界面居中展示实时进度弹窗与顶部进度线，同步跳动百分比、耗时、已扫描股数与命中信号数。
- **多策略共振信号榜 + 多格式导出 + 自选池**：
  - 支持 **「共振聚合 / 全部信号」** 一键切换，按多策略共振数、涨跌幅、换手率或成交额排序；内置 **20 日迷你走势折线图（Sparkline）**、排除 ST / 双创、最低涨幅与最低成交额过滤，支持键盘 `↑ / ↓` 快速翻股。
  - 支持一键导出 **选股明细（`.csv`）**、**通达信自定义板块（`.ebk`）**、**纯 6 位代码（`.txt`）** 或 **一键复制到剪贴板**。
  - 内置 SQLite 本地 `watchlist` 自选观察池，标题栏一键 `☆ / ★` 收藏与集中复盘。
- **历史胜率速验（复盘验证）**：
  - 在「区间与高级」中将截止日期调至历史某交易日并重新选股，自动统计各策略及 **★ 多策略共振（≥2 / ≥3）** 随后 **5 日 / 10 日胜率与平均涨幅**（*仅作历史统计研究，不代表未来收益*）。
- **收盘后自动增量同步**：
  - 后台守护调度器支持交易日收盘后自动增量补齐当日行情（可在「数据缓存」页自定义开关与触发时间），日常复盘完全本地离线运行。

---

## 项目目录结构

```text
baostock-visual-screener/
├── web_server.py            # 原生 Web 终端后端（Starlette + Uvicorn REST & 流式进度 API）
├── static/
│   ├── index.html           # 终端主页面（行情终端 / 策略矩阵 / 数据缓存）
│   ├── app.css              # 暗色 / 亮色双主题样式与移动端响应式布局
│   ├── app.js               # TradingView v5 多副图联动、十字光标与流式选股交互
│   └── lightweight-charts.standalone.production.js  # 离线 TradingView v5 图表库
├── engine.py                # 纯 NumPy 指标计算、20 套策略引擎、历史胜率速验与 .ebk 导出
├── sync.py                  # 收盘自动调度器与增量行情同步模块
├── db.py                    # SQLite 本地缓存、股票池、配置与自选观察池管理
├── charts.py                # 全套 14 项 K 线周期重采样与技术指标计算
├── tests/
│   └── test_core.py         # pytest 核心模块与 Web API 回归测试套件
├── assets/                  # README 演示动图与赞赏码素材
├── start.bat                # Windows 一键双击启动脚本（固定 8506 端口并自动清理残留进程）
├── requirements.txt         # Python 依赖清单
├── LICENSE                  # MIT 开源许可证
└── stock_cache.sqlite3      # 本地行情与自选池缓存库（首次同步后生成，已加入 .gitignore）
```

---

## 手动部署操作说明

### 环境要求

- **Python**：建议 `3.10` ~ `3.13`
- **网络**：首次同步行情需联网拉取公开市场历史日线；缓存建立后日常选股与看盘完全离线可用。

---

### 方式一：Windows 本地部署（推荐）

1. **克隆项目并进入目录**

   ```powershell
   git clone https://github.com/henryorpeter/baostock-visual-screener.git
   cd baostock-visual-screener
   ```

2. **创建并激活 Python 虚拟环境**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   > 若提示 PowerShell 执行策略禁止运行脚本，可先执行一次：
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

3. **安装依赖包**

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   > 如国内下载较慢，可临时指定清华源：
   > ```powershell
   > python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   > ```

4. **启动终端**

   直接双击根目录的 `start.bat`（自动清理旧进程、固定监听 `8506` 端口并打开浏览器），或在 PowerShell 运行：

   ```powershell
   python web_server.py --port 8506 --open
   ```

   打开浏览器访问 `http://localhost:8506`（同一局域网下的手机或平板可直接访问 `http://<电脑局域网IP>:8506`）。

---

### 方式二：macOS / Linux 本地部署

```bash
git clone https://github.com/henryorpeter/baostock-visual-screener.git
cd baostock-visual-screener
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python web_server.py --port 8506
```

在浏览器访问 `http://localhost:8506` 即可。

---

### 方式三：Linux 服务器长期后台部署（局域网 / 公网访问）

1. **准备环境与依赖**

   ```bash
   git clone https://github.com/henryorpeter/baostock-visual-screener.git /opt/baostock-visual-screener
   cd /opt/baostock-visual-screener
   python3 -m venv .venv
   ./.venv/bin/pip install --upgrade pip
   ./.venv/bin/pip install -r requirements.txt
   ```

2. **快速后台启动（`nohup`）**

   ```bash
   nohup ./.venv/bin/python web_server.py --host 0.0.0.0 --port 8506 > screener.log 2>&1 &
   tail -f screener.log
   ```

3. **生产推荐：`systemd` 守护进程托管**

   新建服务文件 `/etc/systemd/system/klineradar.service`：

   ```ini
   [Unit]
   Description=KLineRadar A-Share Stock Screener Web Terminal
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/opt/baostock-visual-screener
   ExecStart=/opt/baostock-visual-screener/.venv/bin/python web_server.py --host 0.0.0.0 --port 8506
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

   启用并启动服务：

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now klineradar
   sudo systemctl status klineradar
   ```

4. **Nginx 反向代理提示**

   若通过 Nginx 代理域名访问，建议关闭代理缓冲以确保 `/api/screen/stream` 实时进度条逐条推送：

   ```nginx
   location / {
       proxy_pass http://127.0.0.1:8506;
       proxy_http_version 1.1;
       proxy_set_header Host $http_host;
       proxy_buffering off;
       proxy_read_timeout 300;
   }
   ```

---

### 离线行情缓存跨机迁移

本地行情与自选池完整保存在项目根目录的 `stock_cache.sqlite3` 单文件中。已在某台机器完成同步后，直接复制该文件到另一台机器同目录并重启服务即可免等待使用。

---

## 日常使用指南

1. **同步本地行情缓存**
   - 点击顶部栏 **「同步行情」**（或进入 **「数据缓存」** 页点击 **「立即增量同步」**）。首次全量拉取约需数分钟；之后每个交易日收盘后可自动或一键秒级增量补齐。
2. **组合策略并执行选股**
   - 在顶部快捷条选择四大流派（`趋势突破` / `涨停战法` / `均线共振` / `形态反转`），或点 **「策略 ▾」** 自由勾选多套策略；按需调整 `排除ST`、`排除双创`、`涨幅≥`、`额≥` 与日期区间。
   - 点击红色 **「开始选股」**，弹出实时进度窗并迅速生成右侧共振信号榜。
3. **多指标看盘与导出**
   - 点击右侧榜单任意股票（或按 `/` 搜索任意代码/简称、按 `↑ / ↓` 键连续翻股）即可在主视口联动展示多周期 K 线；自由开关 6 主图与 8 副图指标。
   - 点击右侧 **「导出 ▾」** 支持导出 `.csv`、通达信 `.ebk`、纯 6 位代码 `.txt` 或一键复制。

---

## 内置 20 套选股策略一览

| 策略流派 | 包含策略 | 核心思路 |
| :--- | :--- | :--- |
| **趋势突破** | 海龟突破策略、阻力位突破策略、高旗形整理策略、趋势加速拐点、趋势起点策略、RPS强势突破 | 捕捉前高放量突破、高位收敛缩量蓄势、均线加速及 120 日相对强度前 10% 领涨股 |
| **涨停战法** | 涨停回马枪策略、涨停横盘策略、涨停洗盘策略、强势洗盘弱转强、上升趋势跌停反包 | 围绕近期涨停基因、缩量回踩支撑、窄幅横盘突破及强势洗盘反包机会（按板块区分 10%/20%/30% 阈值） |
| **均线共振** | 多金叉共振、2560战法、金三角策略、金叉不绿策略 | MA / 均量 / MACD / KDJ 多维度金叉共振与价托放量阳线确认 |
| **形态反转** | 底部趋势拐点、启明星策略、多方炮策略、仙人指路策略、W底策略 | 识别深跌超卖拐点、启明星、两阳夹一阴、长上影试盘与双底颈线突破 |

---

## 常见问题（FAQ）

- **Q：如何切换暗黑模式和亮色模式？**  
  A：点击右上角太阳 / 月亮图标即可一键切换，浏览器会自动记住偏好，K 线画布与网格同步换肤。
- **Q：双击 `start.bat` 启动后端口会变吗？**  
  A：不会。`start.bat` 已固定监听 `8506` 端口，并在启动前自动清理同端口残留进程，收藏 `http://localhost:8506` 即可长期直达。
- **Q：同步行情时偶发少量标的超时或缺失怎么办？**  
  A：再次点击「同步行情」即可，程序会自动跳过已完成项、仅增量补齐缺失的标的。
- **Q：想运行自动化回归测试怎么执行？**  
  A：在虚拟环境中运行 `pytest -v` 即可执行全部本地数据库、指标精度、策略引擎与 Web API 回归测试（测试使用隔离临时库，不会修改本地行情缓存）。

---

## ⭐️ 欢迎 Star 与交流共建

开源不易，如果这个小工具对您有所帮助或带来了启发：
- 请在右上角点击一下 **Star ⭐️** 支持我们，让更多技术分析与复盘爱好者看到这个项目！
- 如果您有新的技术战法、指标思路、改进建议或交流合作，非常欢迎发送邮件至 **[1561784670@qq.com](mailto:1561784670@qq.com)**，或在 GitHub 提交 [Issues](https://github.com/henryorpeter/baostock-visual-screener/issues) 共同交流共建！

---

## 打赏支持

如果这个项目帮到了你，可以请作者喝杯咖啡 ☕

<table>
  <tr>
    <td align="center">
      <img src="./assets/wechat_pay.jpg" alt="微信赞赏码" width="220" /><br />
      <sub><b>微信赞赏</b></sub>
    </td>
    <td align="center">
      <img src="./assets/alipay.jpg" alt="支付宝收款码" width="220" /><br />
      <sub><b>支付宝打赏</b></sub>
    </td>
  </tr>
</table>

---

## 免责声明

1. **非投资建议**：本项目及内置的所有选股策略、技术指标与可视化图表仅用于编程学习、行情数据分析与技术形态研究，**不构成任何证券买卖建议、投资指导或收益承诺**。
2. **历史与信号局限性**：所有筛选信号均基于历史日线 OHLCV 数据的规则化计算，历史形态与回测表现不代表未来走势；市场存在突发风险、流动性风险及跳空缺口等不可控因素。
3. **数据免责说明**：行情数据来源于公开市场行情接口，作者不对数据的实时性、完整性、准确性或接口长期可用性作任何担保。
4. **风险自担**：股市有风险，投资需谨慎。使用本工具所做出的一切分析判断与交易决策均由使用者自行负责，项目作者不承担因使用或无法使用本工具所导致的任何直接或间接经济损失。

---

## 📄 开源协议

本项目采用 [MIT License](./LICENSE) 开源协议。
