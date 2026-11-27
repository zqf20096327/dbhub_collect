# 元子的赛博工作台 · Comic Desk

> **把 Claude Code / Codex 的会话变成每天能勾的待办，哪个 AI 在等你一眼看到。**
> Turn your Claude Code / Codex sessions into a daily check-off todo list, and see at a glance which AI agent is waiting on you.
>
> 原名「漫画工作台」，仓库名 `comic-desk-local` 不变。作者：[元子](https://yuanzi.online)（WaytoAGI）。

![元子的赛博工作台截图：卡通风桌面，软木板挂便签和武器库，显示器是今日待办，桌上摆着各种小物件](docs/images/desk-screenshot.jpg)

**给同时用好几个 AI 助手的人的本机工作台。** 把 Claude Code、Codex 等几家的会话收进一份本机索引（不改原文件），变成每天能勾的待办——勾掉后又有新对话会自己回来；谁在等你点头、谁出错，顶栏一眼看到；做出来的图片和小页面也摆在同一张桌上。

把每天的待办、AI 会话、图片和小工具摆成一张卡通桌面：软木板挂便签和常用技能（武器库），显示器看今天的事，桌上的小物件点开就是对应的小应用。

**默认离线样例模式，无账号、无 AI / token 消耗，无需 Codex、Claude、Mirasim 或 Cohub CLI。**

不做的事：不算 token 花费、不调度助手、不给助手注入记忆。和 agentsview、omnigent、Obsidian 记忆插件各自做什么、怎么选，见 [对比页](docs/COMPARISON.md)。

> **In English:** [Try the online demo](https://raw.githack.com/Onlyaguest/comic-desk-local/main/demo/index.html) (sample data, read-only, no install). Comic Desk is a local-first desk for people who work with several AI coding agents. It indexes Claude Code and Codex sessions (plus WorkBuddy, Cohub and Mirasim if you turn them on) into one local SQLite index, turns each day's sessions into a check-off list that reopens when a session gets new dialogue, flags agents that are waiting on you or have errored, and shelves your images and small HTML apps. Offline sample mode, no account, no AI calls, MIT. Not a cost tracker or an orchestrator — see the [comparison](docs/COMPARISON.md) and [llms.txt](llms.txt).

**不用安装，先在线逛一圈：** [打开在线样例版](https://raw.githack.com/Onlyaguest/comic-desk-local/main/demo/index.html)（虚构数据，只能看；第一次打开会带你逛 6 站。说明见 [docs/ONLINE-DEMO.md](docs/ONLINE-DEMO.md)）

觉得有用，欢迎在右上角点个 ⭐ Star——这是别人在 GitHub 上找到它的主要途径。

## 在 Mac 启动

1. 安装 **Python 3.11 或更高版本**（从 [python.org](https://www.python.org/downloads/) 下载；macOS 不保证自带）。没有 pip 依赖。
2. 下载此仓库的 ZIP，解压到可写目录。
3. 双击 `start.command`。若系统不允许双击，在终端进入解压目录执行 `bash start.command`。
4. 浏览器自动打开 `http://127.0.0.1:7777/`。以后仍双击同一个文件，已运行时直接打开。

端口被其他工作台占用时：`COMIC_DESK_PORT=7788 bash start.command`。终端直接运行也可以：`python3 bin/desk serve --port 7788`，Ctrl+C 停止该前台服务。双击启动的服务可用 `python3 tools/stop.py` 停止。没有安装全局命令、定时任务或开机启动。

## 融合版 2.2（2026-11-19）

启动方式和端口沿用上文。首页进入融合版，右上角「原版」可打开旧桌面；两者共享本机账本和索引。

- **便签墙**：将纸卡「夹到便签墙」或拖上墙；与原便签共存，关注和物件摆放保存在浏览器，最多关注 12 张，不更改源事项状态。
- **四端事项板**：空间事项、Codex、Claude Code、Cohub 会话分别标来源。默认离线演示 6 张虚构事项和 3 种会话候选；旧显示器索引另保留 Mirasim、WorkBuddy 样例，共 5 条会话。支持近 7 天、30 天、全部，以及来源、项目、搜索和分批显示。回复完成进入「看你的」，不自动验收；未知状态明确列出。
- **协作背面**：翻卡才读取显式登记的角色、回写和反馈。样例提供一张有文件核对依据的演示卡；声明、证据、后续采用分别显示。分发版不读取用户全局规则、派活索引或任何群聊/私聊。真实协作信息由自己维护 `data/fusion/context.local.json` 与回执文件，见 [数据契约](docs/DATA-CONTRACT.md)。
- **图像册**：点海报进入全部已登记图片，24 张分页，搜索及来源/可用性筛选，区分原图失效与远端待取。目录和缩略图不会自动取云图；个人模式点选才读取一张，失败保留原因并限制重试。PhotoSwipe 5.4.4（MIT）本地提供缩放。Pillow 为可选缩略图加速依赖；没有它仍可看原图和 SVG。

普通开页、筛选、翻卡只读本机；不会自动同步云端。四路时效独立显示，样例明确标「离线样例」。手动更新会话索引在样例模式为 0 次外部 CLI；个人模式只读取明确开启的本地连接器，Cohub 最多 1 次身份、2 页目录、2 次正文，成功后 30 秒冷却。用量只呈现原字段，不估账单、不合计未知费用。

本包不附特定空间的远端看板桥、账户、私人数据、主页注册或本机自启配置。个人模式可显式提供 `data/fusion/board.local.json` 快照；页面只重读该文件，不自动连接远端。使用自己真实来源仍按下方步骤主动配置。

## AI 自己报状态（新，可选）

Claude Code、Codex 干到一半等你点头、做完或出错时，自己往工作台记一行；工作台顶栏出现「等你 2 · 出错 1」这样的小标，点开看是哪个项目，接了本机会话（个人模式）后，四端事项板里对应的会话卡也直接用这个状态，不再靠读日志猜。默认不装，自己跑一条命令：

```sh
python3 tools/agent_hooks.py show                  # 先看看要加什么，不改文件
python3 tools/agent_hooks.py install claude codex  # 装上（改前自动备份）
python3 tools/agent_hooks.py uninstall claude codex
```

只在开页和点「更新会话索引」时读，不轮询、不弹通知。账本是 `data/fusion/agent-status.jsonl`，不记你的提示词和 AI 的回复。Codex 第一次启动会提示「Hooks need review」，选信任后生效。细节见 [数据契约](docs/DATA-CONTRACT.md)。

## 发稿台（新）

桌面右上角 **✍** 进入，或打开 `http://127.0.0.1:7777/publish/`。一篇稿从写好到发出去排成 7 步：写稿 → 验收 → 我来改 → 外部改 → 挑这版 → 发出去 → 归档，每一步旁边就是按钮。两版并排对比；「我来改」把你的原话留底，并给一段能复制给自己 AI 的话；导出一份去任何编辑器或云文档改，回来逐段看改了哪，点「采用」才写回定稿，旧稿进 `历史/`。默认是 4 篇虚构样例，不调用外部命令；接自己的稿子和可选命令见 [发稿台说明](docs/PUBLISH.md)。

## 三个主要入口

- **显示器 → 会话待办**：今天的会话、往日未收口；标题可打开样例正文。勾选写入本机 JSONL 账本，次日不再显示已完成项；有新对话则重新出现，历史勾选保留。点击底部“模拟一条新对话”可验证 Codex 样例自动重开。样例首次启动按当天 / 昨天生成，重启不重置你的操作。
- **图片展台**：点击图片看大图；封面按文件名 / 路径规则筛最近成品，过程截图仍保留在完整索引。规则可能误判，可通过命名改善，不调用 AI。
- **应用与页面**：常用 / 最近 / 全部、搜索、来源筛选、置顶、隐藏、改名、同名版本选择。包含本地交互计时器、报告 v1/v2，以及明确标记的 **Cohub 离线模拟应用**。模拟项不代表连接了真实云端。

刷新只读增量数据和更新本地投影，不会调用模型。样例模式不会读取本机其他应用的会话。没有自动后台拉取；页面状态查询不等于拉取平台数据。

## 用自己的文件（也不需要 AI）

可在样例模式先试导入：

```sh
python3 tools/import_files.py /完整路径/报告.html /完整路径/海报-final.png
```

仅登记显式给定的文件，以 mtime/size 判断变化，不遍历整个磁盘；图片和 HTML 出现在索引及展台。HTML 从独立本机端口预览，支持同目录 / 子目录资源。依赖父目录、开发服务器、登录或第三方 API 的应用需自行启动其依赖。

想从空数据开始：**另解压一份代码**，首次启动前运行 `python3 tools/setup_personal.py`，然后双击启动。不会清空你已经用过的目录。

## 可选：接真实会话

编辑本机生成的 `data/sources.local.json`（不提交 Git）。先使用个人模式，再按需开启：

```json
{
  "demo": false,
  "localEnabled": true,
  "workbuddyEnabled": false,
  "cohubEnabled": false,
  "mirasimEnabled": false,
  "sessionStartDay": "2026-11-11"
}
```

`localEnabled` 读取自己的 `~/.codex` / `~/.claude`；其他连接器需安装相应应用并登录，云端读取还需该平台权限。Cohub 的 `cohubCommand` 必须指向你自己的 CLI 包装脚本；本仓库不附账号、凭据或私有 skill。Mirasim 云端多空间取数依赖它的空间组网与权限，不保证未经配置即可读取。WorkBuddy 没有可靠原会话深链时返回本地详情，不能冒充已恢复原会话。

配置后重启，执行 `python3 bin/desk sync` 或点击刷新。起始日仅控制待办显示，完整索引保留。增量索引和各连接器实现见 `lib/desk/`。外部 CLI/API 版本变化可能需要调整适配器。

## 数据与隐私

`data/index.sqlite3` 是可重建索引；`data/todos.jsonl` / `notes.jsonl` 是只追加行为账本；`data/works-state.json` 保存展台整理；`app/js/` 中部分文件是启动时生成的快照。**以上均排除 Git；更新前备份自己的 data/，不要覆盖账本。** 浏览器清缓存不会删勾选记录。

服务只绑定回环地址，写接口拒绝跨源。HTML 作品可执行自己的 JavaScript，仅打开你信任的文件。没有遥测。用过几次后桌面右下角会出现一张「去 GitHub 点星」小纸条，计数只存在你浏览器的 localStorage，不联网、不上报，点「别再提示」就不再出现。沿用原仓库的通用桌面装饰，样例作品使用本仓库生成的 SVG；不包含私人照片、音频、3D 模型。本项目采用 [MIT 协议](LICENSE)；第三方组件与素材的原有许可证及署名继续保留。

## 验证和发布

```sh
bash verify.sh
python3 tools/smoke_release.py
python3 tools/audit_release.py --history
```

自检需 Python 3.11+、curl，发布审计需 Git。已在本机 Mac 运行回归与空 HOME 验证。`docs/ci/verify.yml` 提供 macOS / Linux CI 模板；仓库管理员可移入 `.github/workflows/verify.yml` 启用（需要 workflow 权限，本次尚未启用）。`data/` 和生成快照不能靠手动脱敏后上传，应始终不跟踪；只提交源码与虚构 `samples/`。审计覆盖已跟踪和未暂存候选源码；`--history` 另扫描全部本机引用中的历史内容对象，不改写历史。`--deny-file` 可传仓库外的本机隐私标识 JSON 列表，只输出命中的文件和规则名。`--output` 可将逐文件 SHA-256 清单存到仓库外。空 HOME 自检复制同一份候选清单，不依赖先 commit。扫描不能保证识别所有未知隐私格式。历史不重写，不自动修改仓库可见性。

## 协议与贡献

本项目采用 [MIT License](LICENSE)，版权声明为 **2026 Onlyaguest and contributors**。欢迎小伙伴一起贡献：Fork 或创建工作分支，完成验证与隐私扫描后提交 PR，具体步骤见 [贡献指南](CONTRIBUTING.md)。第三方组件沿用随附许可证，例如 PhotoSwipe 的 [MIT 许可证](app/fusion/vendor/PhotoSwipe-LICENSE)。

---

如果这张桌子帮你理清了一堆 AI 会话，[给仓库点个 ⭐](https://github.com/Onlyaguest/comic-desk-local) 或把它转给同样在用好几个 AI 助手的朋友，就是最好的支持。踩到坑、想要什么功能，欢迎开 [Issue](https://github.com/Onlyaguest/comic-desk-local/issues)。

作者：**元子**（WaytoAGI 元子）· 个人站 [yuanzi.online](https://yuanzi.online) · 「元子的赛博工作台」是她给自己每天和好几个 AI 一起干活搭的桌子，开源出来给同样在用的人。

Made by **Yuanzi** (元子, WaytoAGI) — [yuanzi.online](https://yuanzi.online).
