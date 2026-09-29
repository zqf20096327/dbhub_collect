# 我的时间管家 · Schedule AI Butler

> 一个人就能自托管的三端日程管理工具：**电脑网页版 + 桌面挂件 + 手机离线 PWA**，本地 SQLite 存储，数据完全归你。

一个轻量、自托管、**几乎零依赖**的个人日程 / 积分管理应用。不依赖任何云账号，数据存在你自己的电脑上（`timekeeper.db` 单文件），电脑和手机访问同一份数据，可跨网同步。

---

## ✨ 功能

- 📅 **日程管理**：日视图、月历、看板、周报、待办、专注番茄钟六种视图
- ⭐ **积分体系**：按分类（学习/健身/运动/工作/会议/休息/其他）+ 时长 + 优先级自动算分，逾期扣分
- 🤖 **AI 日程助手**（`agent.py`）：对话即可添加/查看/完成/修改/删除任务、生成学习计划、汇总积分；内置规则模式未配 Key 也能用，配了 OpenAI 兼容接口（默认 DeepSeek）即可自由对话
- 🪟 **桌面挂件**（`widget_app.py`，pywebview）：常驻桌面的可折叠小窗，收拢成一条精致胶囊，实时显示时钟/下一项/今日进度
- 📱 **手机版**（`mobile/`，PWA）：扫码配对后可「添加到主屏幕」安装成手机 App，增删实时同步回电脑
- 🔄 **多端跨网同步**：`sync_hub` + `sync_client` + `boot_all` 守护进程，手机/电脑数据一致
- 🎙️ **语音/文字解析**（`ai_helper.py`）：手机端说话自动转成日程（本地 Whisper 兜底，离线可用）
- 🗂 **周报留档**：一键把周报快照存档到本地，并清理过期日程

---

## 📦 目录结构（分类打包）

```
.
├── pc/                      # 电脑版（网页 + 后端 + 桌面挂件，保持平级便于直接运行）
│   ├── app.html             # 前端单文件（电脑完整界面）
│   ├── server.py            # 后端（标准库，零依赖）
│   ├── widget_app.py        # 桌面挂件外壳（pywebview）
│   ├── agent.py             # AI 日程助手（对话 + 工具调用）
│   ├── ai_helper.py         # 手机端语音/文字→日程 解析
│   ├── sync_*.py / boot_all.py  # 多端同步与守护
│   ├── *.bat                # 启动 / 打包脚本
│   └── ...                  # 其余业务模块
├── mobile/                  # 手机版（离线 PWA，可安装到手机桌面）
│   ├── index.html
│   ├── manifest.webmanifest
│   ├── sw.js
│   └── icons/
└── docs/                    # 文档（安装/使用/架构）
```

> **运行时布局**：把 `mobile/` 里的 `手机站` 放到 `pc/` 目录下（或直接使用网页版），`server.py` 会自动托管它。

---

## 🚀 快速开始（电脑端）

1. 安装 Python 3.8+（勾选 *Add to PATH*）。
2. 双击 `pc/run_server.bat`（或 `一键启动.bat`），浏览器打开 **http://localhost:8000**。
3. 想常驻桌面：双击 `pc/启动挂件.bat`（需 `pip install pywebview`）。
4. 手机端：电脑端「📱 手机同步」→ 扫码配对 → 手机浏览器「添加到主屏幕」安装为 App。

### 可选依赖

程序核心用 **Python 标准库**、零依赖即可运行；以下为可选增强：

```bash
pip install pywebview qrcode        # 桌面挂件 + 配对二维码
pip install faster-whisper av numpy # 手机语音本地转写（离线可用）
pip install matplotlib              # 周报图表
```

---

## ⚙️ 配置说明

- AI 助手：电脑端 ⚙️ 面板填 `api_key` / `base_url` / `model`（默认 DeepSeek），存本机 `ai_config.json`，密钥不出服务器。
- 端口：默认 8000，可用环境变量 `PORT` 覆盖。
- 数据备份：直接复制 `timekeeper.db` 即可。

## 🔒 隐私

本仓库为**代码/模板**仓库，不含任何个人数据。默认生成的 `timekeeper.db`、密钥、日志、备份均在 `.gitignore` 中排除，请勿提交。

---

## 📄 License

[MIT](./LICENSE)
