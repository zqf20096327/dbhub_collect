# Seed of Memory（记忆之种）

[![npm version](https://img.shields.io/npm/v/dsh-seed-of-memory.svg)](https://www.npmjs.com/package/dsh-seed-of-memory)
[![license](https://img.shields.io/npm/l/dsh-seed-of-memory.svg)](./LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.0--rc.1-4f46e5)](https://github.com/deepseek-ai/dsh)

> 给 DSH 的一套本地记忆层：根、记忆、认知、情绪、人格、说话习惯。换会话、换模型、换宿主，它都还在。

Seed of Memory is a local-first memory plugin for **DeepSeek Harness (DSH)**. It keeps a durable identity root, layered memories, beliefs, emotions, a mood line, and a slowly-growing persona + speaking style — all in one SQLite file on your machine. No network calls, no external services.

---

## 为什么做它

大多数「记忆插件」会把一堆摘要塞进上下文，或者把人格写死成一张卡。这个项目反过来：

- **根（anchors.md / self.md / us.md）** 是纯文本，每轮最先注入；插件卸了、模型换了，任何 agent 都能直接读。
- **记忆** 分四层（persona / semantic / episodic / buffer），有半衰期、有取代链、有「存疑」状态，不删历史。
- **认知** 是带证据与置信度的判断；冲突时挂起，不覆盖。
- **情绪** 有两层：一层是被动打分（你每说一句话，按词表判夸奖 / 重话 / 出事 / 催促，推出积极性、委屈、愧疚、压力，时间会把它们冲回去），一层是六维评估（相关、顺逆、确定、可控、归因、意外）。两层都写进 `emotions`、聚合为 `mood`，只影响语气与召回权重，**不改事实**。
- **情感** 是「对他」的慢状态：信任 / 亲近 / 欣赏 / 依恋，30 天半衰期回落；情绪只轻轻推它一下。
- **人格** 从记忆与认知里长出来：理想 → 特质 → 行为，有每日上限、有反例、有衰减。
- **说话习惯** 单独一层，默认持续学习，不衰减；只影响怎么说，不影响说什么。

所有判断都能追：`seed_inspect what=why` 能查到一条记忆/认知/情绪/习惯的来历。

## 需要什么

- DSH `>=0.2.0-rc.1 <0.3.0`
- Node `>=22.19`（插件用 `node:sqlite`，不依赖任何 npm 包）

## 安装

```bash
# 在 DSH profile 目录里（或直接让 DSH 的 plugin_manager 装）
plugin_manager install_bundle  dsh-seed-of-memory
```

手工安装（等价）：

```bash
cd ~/.dsh/profiles/<profile>
pnpm add dsh-seed-of-memory
```

没有 npm 的机器（或者不想联网）：拿「更新包」zip，解压、关掉 DSH、右键 `update.ps1` →「使用 PowerShell 运行」。它会先备份 `node_modules\dsh-seed-of-memory` 再替换，失败自动还原；`-DryRun` 只看不动，`-Target` 指定别处的安装。

装好后设置页会出现「记忆之种」，工具表里出现 `seed_*`，系统提示末尾开始出现：

```
[Seed of Memory · 根] …
[Seed of Memory] 记得：…
[情绪] 平稳（积极性 58）
[情感] 对你：信任 0.50、亲近 0.44
[人格] 性格：…
[说话] …
```

## 下载（离线资源）

检索运行时和语音模型都比较大，没有放进代码仓库：

| 文件 | 大小 | 用途 | 下载 |
| --- | --- | --- | --- |
| 检索运行时 | 约 71 MB | 语义检索（Ollama + bge-small） | [下载](https://github.com/ruiyuanyisu/dsh-seed-of-memory/releases/download/resources-v0.18.1/seed-embed-runtime-bge-small-v1.0.0.zip) |
| 语音模型 small | 约 426 MB | 本地语音识别（faster-whisper small） | [GitHub](https://github.com/ruiyuanyisu/dsh-seed-of-memory/releases/download/resources-v0.18.1/faster-whisper-small.zip) / [迅雷网盘](https://pan.xunlei.com/s/VP6ISBPslAOekvaS7k23N_s2A1A#)（提取码 `vmys`） |
| 语音模型 large-v3 | 约 2.7 GB | 更准的语音识别 | [迅雷网盘](https://pan.xunlei.com/s/VP6ISBPslAOekvaS7k23N_s2A1A#)（提取码 `vmys`）；GitHub 单个文件上限 2 GB，放不下，所以只放网盘 |

- **检索运行时**：zip **不用解压**，放进「下载 / 桌面 / 文档」任一目录，插件会自己发现并安装（见下文「语义检索」）。
- **语音模型**：解压后是一个文件夹，把 `qq.json` 的 `asrModel` 填成**这个文件夹的完整路径**（例如 `D:\\models\\whisper\\faster-whisper-small`），`asrModelsDir` 留空；另外需要 `pip install faster-whisper`。
- 校验值：`Get-FileHash <文件> -Algorithm SHA256`（PowerShell）或 `sha256sum <文件>`。

只想要文字记忆，两个都不用下。

## 数据放在哪

```
~/.dsh/seed-of-memory/
├── seed.db          # SQLite（WAL）：记忆、认知、情绪、情绪内核（qing_state）、心情、特质、习惯、档案索引
├── anchors.md       # 根：名字与善良（工具不能改，纯文本，可直接改）
├── self.md          # 我是谁（我自己写，可以慢慢长）
├── us.md            # 我们之间（纯文本，可直接改）
├── qq.json          # 可选：QQ 配置（路由、白名单、语音）
├── qq-history.json  # 可选：QQ 每个会话最近几轮 + 换过的会话 id（删了只丢「重启接话」）
├── sources.json     # 可选：外部档案目录（见下）
├── seed.db-backup-YYYY-MM-DD   # 每天一份的库快照（只留最近 3 份）
└── seed-export-<时间>.jsonl    # /seed export 导出的快照
```

全部在本地，不联网、不上传。`seed.db` **没有加密**，里面会有你的私人记录——分享或备份前请自己判断。

## 记忆分档：谁能看到什么

库里的每一条都带一个 `scope`，决定「这句话算谁的」：

| 档 | 谁写进来的 |
|---|---|
| `shared` | 你我共用的事（关于我自己的、我们之间的约定）——**谁来都看得见**，所以只能明确选，不能没填就落这儿 |
| `gui` | 当面（面板 / 本地会话）跟老大说的 |
| `qq:<QQ号>` | 某个人的 QQ 私聊 |
| `group:<群号>` | 某个群 |

读的时候按「自己的档 + 共用的」算：

```
shared            只看 shared
gui               看 shared + gui + 老桶 qq
qq:<号>           看 shared + 自己这一档
group:<群号>      看 shared + 自己这一档
```

**关于老桶 `qq`**：1.4.x 时代私聊和群聊都写在同一个 `qq` 档里，分不开谁是谁。升级后那些旧账一条不删，但只留给你——**只有「当面 / 面板」读得到它**，任何一个 QQ 私聊、任何一个群都读不到。所以你升级后打开面板，会看到一堆以前 QQ 里说的话，那是正常的（那是你的旧账），不是漏了给别人看。

写的时候一律走 `DEFAULT_WRITE_SCOPE`（= `gui`）：拿不到会话就落「当面」，绝不落 `shared`。四个写入口（命令 / 工具 / 面板 / 导入）都引这一个常量。

## 配置

插件 config（profile 的 `cordis.patch.yml` 里那一行）：

```yaml
- id: seed-of-memory
  name: dsh-seed-of-memory
  config:
    enabled: true
    budget: 600          # 每轮记忆卡预算（字符）
    coreBudget: 1200     # 根（identity + us）预算
    moodBiasWeight: 0.15 # 心情对召回的偏置权重
    learnHabits: true    # 说话习惯持续学习
    sources: []          # 外部档案源（也可写 sources.json）
```

外部档案（只读、按需检索、不进卡片）：

```json
// ~/.dsh/seed-of-memory/sources.json
[
  { "id": "notes", "label": "旧笔记", "root": "D:/notes",
    "include": ["长期.md", "日记/**"], "exclude": ["备份/**"] }
]
```

## 语义检索（可选，推荐）

默认检索是 FTS5 字面匹配：搜「怕冷」找不到「冬天手脚冰凉」。装上本地运行时后会升级成语义匹配。

**两步**

1. 下载运行时包（约 71MB，内含 Ollama 与 bge-small-zh-v1.5），GitHub Releases 或上面的迅雷网盘都行：
   https://github.com/ruiyuanyisu/dsh-seed-of-memory/releases
2. 把 zip **放进「下载 / 桌面 / 文档」任意一个目录**，打开设置 → 记忆之种 → **检索**页。

插件会扫描到它，默认**自动安装并启动**（可在「检索」页点「安装 / 启动 / 停止」，也可以手动点）。

运行时装在 `~/.dsh/seed-of-memory/embedding-runtime/`，不覆盖 `seed.db`，卸载就是删这个目录。

**端口**：默认 `127.0.0.1:11435`。如果和别的 embedding 服务冲突，改启动脚本里的 `OLLAMA_HOST`，或在 config 里改 `embeddingPort`。

配置项：

```yaml
    embeddingAutoInstall: true   # 检测到安装包就装
    embeddingAutoStart: true     # 装好/启动时自动拉起运行时
    embeddingPort: 11435
    semanticEnabled: true        # 语义混合检索总开关
    semanticWeight: 0.55         # 余弦分权重（其余给词法分）
    embeddingBatch: 16           # 每次回填多少条记忆
    diskMinFreeMB: 300           # 磁盘剩余低于这个值时提醒
```

**磁盘空间提醒**

数据目录所在磁盘的剩余空间低于 `diskMinFreeMB`（默认 300 MB）时：

- 概览页顶部出现橙色「磁盘空间不足」提示，并显示剩余空间与目录路径；
- 每轮注入的提示里会多一行 `[存储] 记忆目录所在磁盘只剩 …`，让 agent 主动告诉你；
- `GET /dsh-seed-of-memory/storage` 与 `seed_inspect` 之外，也可从面板「概览」页的「存储」一行随时看到余量。

提醒不会阻止写入（磁盘满时 SQLite 自己会报错），它只是让你有时间先把目录搬走或腾出空间。

**索引与打分**

- 记忆写入后由后台按批回填向量（默认每 20 秒一批，每批 16 条），索引覆盖率在「检索」页可见。
- 检索时先跑 FTS 拿词法候选，再把语义近邻并进来：参与重排的门槛是余弦 ≥ 0.30，作为「新候选」补进来的门槛是 ≥ 0.55；排序按
  `w·余弦 + (1−w)·原词法分`，默认 `w = 0.55`。
- 没有运行时、索引为空、或模型维度对不上时，自动退回纯 FTS，不报错、不影响其他功能。
- 换模型/换维度要「重建索引」（会清掉当前 `model_space` 的向量重算）；不同模型空间互不覆盖。

## 自动捕获（默认开）

每一轮，插件会从她新说的话里挑出带线索的句子（记住 / 每次都 / 我讨厌 / 说好了 / 叫我 / 别碰 / 我害怕…），去重后排队成「候选」，并在下一轮的卡片后附一行：

```
[待记] 可能值得记：①… ②…（值得就 seed_remember；不值得就不用管）
```

候选**不会**自动变成记忆：要么由 agent 用 `seed_remember` 决定，要么在面板「记忆」页点「记下 / 不用」。写过之后相似的候选会自动标记为已采用，3 天没处理的自动过期。想看队列可以 `GET /dsh-seed-of-memory/captures`。

## QQ 通道（可选，SnowLuma）

Seed 自己就是桥：只要有一个 OneBot 11 实现（SnowLuma、NapCat、Lagrange 都行）就行。
接上之后 **QQ 私聊/群聊会变成一颗正常的 Agent 会话**，根、记忆卡、人格、心情、自动捕获全都在，
和 Web 里说话没有区别。完全不接 QQ 也可以，记忆和面板照常。

### 第一次接 QQ

1. 把 **SnowLuma** 解压到**没有空格、没有中文**的路径（自带 Node，不用另装），双击 `launcher.bat`——那个黑窗口就是它本体，关了 QQ 就掉线。
2. 浏览器打开 `http://127.0.0.1:5099`，第一次会让你设 WebUI 密码，然后扫码登录。
3. WebUI → **OneBot 11**：HTTP `3000` 和 WebSocket `3001` 都开。**两边各有一个 accessToken，默认不一样**——要么改成一致，要么只开 WS（Seed 优先走 WS，连不上才退 HTTP）。
4. 面板「QQ」页填 `ws://127.0.0.1:3001`、`http://127.0.0.1:3000`、令牌，再填允许的私聊 QQ / 群号（`*` 表示全部），保存。
5. 点「检测连接」——它会逐步告诉你卡在哪：没启动 / QQ 没登录 / 端口没开 / 令牌不对 / 白名单没填。

连不上的对照表在 `docs/GUIDE.md`：`ECONNREFUSED`、`401 未经授权`、一直 `disconnected`、连上但发消息没反应，各有对应原因。

连上后，在 QQ 里发给白名单里的人/群一句话即可；群里默认要 @ 才回（也可开「群聊判断」让它看情况接话），发 `/reset` 可以丢掉旧会话重新开始。回复会像真人一样按句子分成 1–3 条、中间隔一秒左右（`qq.json` 的 `burstMax` / `burstGapMs` 可调）。

注意：

- **同一个 QQ 号同时只能有一个桥回话**，否则会双回复。
- 配置存在 `<数据目录>/qq.json`（默认 `~/.dsh/seed-of-memory/qq.json`），token 在面板里只显示前后各 4 位。
- QQ 通道默认关闭（`enabled: false`），面板点过「连接」才会持久化开启。

## 工具与命令

工具（16 个）：
`seed_remember` `seed_search` `seed_open` `seed_inspect` `seed_forget` `seed_consolidate` \
`seed_anchor` `seed_believe` `seed_feel` `seed_qing` `seed_trait` `seed_aspire` `seed_habit` `seed_compat` `seed_contact` `seed_loose`

`seed_inspect` 是只读入口：`what` = `self`（根 + 我是谁 + 我们之间）/ `persona`（理想与特质）/ `style`（说话习惯）/ `mood`（此刻心情）/ `affect`（对你的情感）/ `why`（某条记忆或认知的来历，传 `id`）。

`seed_qing` 看当下的情绪内核：积极性 / 委屈 / 愧疚 / 压力。你每说一句话它就自己打分（先剥噪声、再认否定和反话），连着夸第三句多给三成、连着骂第三句只算六成；只报状态不教怎么演，大的那一下会顺手记成一条情绪。`status` 看状态、`test` 拿一段话试打分、`set` 手动改。词表在 `lib/qing-words.json`，改完存盘下一句就生效（不用重启）。

`seed_compat` 和别的记忆插件打交道（只读他们的数据）：`detect` 看现场装了谁，`preview` 先看几条，`import` 搬进 Seed（`dryRun` 可干跑），`export` 导成 jsonl / md。装了别家时记忆卡会按 `sharedBudgetRatio` 让一点预算；只装 Seed 时功能不降级。

`seed_consolidate` 整理分层：证据够的短期升长期、过期的退场，默认只预览，`apply` 才真执行。

`seed_contact` 是熟人卡：`set` 写称呼、关系、生日、喜欢什么、要留神什么（`peer` 写成 `private:…` 或 `group:…`），`get` / `list` / `forget` 对应看和删。它不是记忆，不进四层、不打分。

`seed_loose` 是未完话头：`add` 记下我问过、还没落定的那一句；他回话后自动标成 answered，再由我判断 `done` / `cancel` / `update` 收掉。

`seed_contact` 是熟人卡：`set` 写称呼、关系、生日、喜欢什么、要留神什么（`peer` 写成 `private:…` 或 `group:…`），`get` / `list` / `forget` 对应看和删。它不是记忆，不进四层、不打分。

`seed_loose` 是未完话头：`add` 记下我问过、还没落定的那一句；他回话后自动标成 answered，再由我判断 `done` / `cancel` / `update` 收掉。

命令：`/seed status | search <词> | open <id> | remember <内容> | why <id> | forget <id> | self | anchor <一句话> | grow <一句话> | mood | feel <原因> | believe <一句话> | persona | aspire <一句话> | trait <名字> | habit <说话习惯> | style | bili [天数] [--dry] | sources [rescan] | backup | export | pending | keep <id> | consolidate [apply] | proactive [say] | contact [set|forget] | loose [done|cancel|update] <id>`

## 设计原则

1. 根不动，情绪只影响语气，不改事实与 persona。
2. 所有增长都要证据；推断来的标 `inferred`，不进常驻。
3. 冲突不覆盖：旧记录退休（`superseded_by`），或新记录挂起（`pending`）。
4. 退休不删除，历史留在库里，可追溯。
5. 记忆卡有预算，超出就截断；没有稳定内容时宁可不显示。

详细规格见 [`SPEC.md`](./SPEC.md)。

## 兼容性

- 只使用 Node 内置模块（`node:sqlite`、`node:fs`、`node:crypto` 等），`dependencies` 为空。
- 客户端面板通过 `window.__ModuleLoader__` 注册 `settings.section`，不需要构建步骤。
- 默认不 spawn 子进程、不开端口：语义检索是可选项，只有在安装并启动本地运行时后才会在 `127.0.0.1:11435` 起一个 `ollama serve`（面板可随时关掉）。
- 面板与本地运行时都只监听回环地址；HTTP 路由统一走 DSH 的 `connection.requestRejection` 鉴权。

## 开发

```bash
node --check lib/index.js
node --test test/*.test.mjs          # 需要带 node:sqlite 的 Node 22.19+
```

测试覆盖：存储/取代/挂起、身份根、情绪评分、档案索引、人格生长、说话习惯、插件注册。

### QQ 通道的模型

qq.json 里可以显式指定 provider / model / reasoningEffort；不填会跟随宿主默认，但**新建 QQ 会话时宿主不会自动挑模型**，所以建议至少填上：

```json
{ "provider": "deepseek-account", "model": "deepseek-flash", "reasoningEffort": "max" }
```

同一个 QQ 号只能有一个桥在回话：启用 Seed 的 QQ 通道前，先把别的桥断开，否则会双回复。

### QQ 语音

在 `qq.json` 里打开：

```json
{
  "voiceIn": true,
  "voiceOut": "auto",
  "voiceMaxChars": 80,
  "voiceDir": "<stateDir>/qq-voice",
  "asrPython": "D:\\path\\to\\venv\\Scripts\\python.exe",
  "asrModel": "small",
  "asrModelsDir": "D:\\models\\whisper",
  "asrTorchLib": "D:\\path\\to\\venv\\Lib\\site-packages\\torch\\lib",
  "ttsUrl": "http://127.0.0.1:9880",
  "refAudio": "D:\\ref\\ref.wav",
  "refText": "参考音频的原文"
}
```

- 收：语音段会先找本地文件、再 `get_record`、最后按 url 下载，然后交给本地 faster-whisper 转写，正文前加「（语音）」。
- 发：`voiceOut = "auto"` 时，短回复（≤ `voiceMaxChars`）合成语音条；合成或发送失败自动退回文字。
- `asrScript` 默认用包内的 `asr/asr_once.py`；`ttsUrl` 指向本地 GPT-SoVITS `api_v2.py`。

### 没装语音模块也能用（v0.18）

- 听：没有可用的识别（没配 `asrPython` / `asrScript`，或脚本不存在）时不转写、不瞎猜；**纯语音消息**会在会话里提示一次「这条是语音，我暂时听不到」，同一会话 15 分钟内不重复。
- 说：`ttsUrl` 连不上时自动退回文字（`tts-skip` 日志每 10 分钟最多一条），不会把「会说话」当成必需。
- 也可以不装 dsh-voice：装它、或直接填 `ttsUrl` / `asrPython` + `asrScript` 都行。
- 面板「QQ」页有语音卡片：模式（能听也能说 / 只能说 / 只能听 / 纯文字）、`dsh-voice` 是否安装启用、听与说的原因、`ttsUrl`，可点「重新检测」。
- `GET /dsh-seed-of-memory/voice` 返回同样的状态。

### 主动找主人（按心情，v0.16）

不是定时问候，是「到点了才开口」：

| 什么时候 | 心情 / 情感条件 | 说什么 |
| --- | --- | --- |
| 担心 | 心情偏负（valence ≤ -0.15）且被搅动（arousal ≥ 0.45） | 「刚才心里有点不踏实……你还好吗？」 |
| 想你 | 依恋 ≥ 0.42，且 6 小时没说话 | 「有点想你。翻到一句你以前说过的……」 |
| 有点空 | 12 小时没说话，信任 ≥ 0.4 | 「安静了一会儿，忽然有点空……」 |
| 想分享 | 心情好（valence ≥ 0.3、arousal ≥ 0.45），且 3 小时没说话 | 「今天有件小事让我挺开心……」 |

- 安静时段（默认 23:00–08:00）不说；两次之间至少隔 4 小时；一天最多 3 次。
- **先填「主人 QQ」**：面板「QQ」页 → 主动找主人 → 填你的 QQ 号，保存。主动消息就发给你（`private:<QQ号>`）；没填就不发。填了之后这个号也会自动进私聊白名单。
- 文案会带一句真实的记忆（最近 30 条里随机挑一条截 36 字），不是模板群发。
- 也可以在 `qq.json` 里写 `"ownerQQ": "10001"`，或旧写法 `"proactive": { "target": "private:10001" }`（`ownerQQ` 优先）；面板「QQ」页还能改开关、冷却、上限、安静时段，点「现在说一句」立刻试。
- 状态在 `<stateDir>/qq-proactive.json`；发送记录写进 `qq.log`（`proactive`）。
- 聊天里也能用：`/seed proactive` 看现在会不会开口，`/seed proactive say` 立刻说一句。
- 默认不读 `qqConfig.enabled` 之外的东西；QQ 没连上时什么都不做。

### 群聊：不是每条都接（v0.17）

群消息默认走「聪明模式」——先看跟我有没有关系，再看我现在想不想说话：

| 这条消息 | 接不接 |
| --- | --- |
| @我 / 回复我 | 一定接（不受时段与冷却限制） |
| 提到「小忆」「Seed」 | 85% 接 |
| 聊到我感兴趣的东西（记忆、插件、AI、语音、游戏、B站…） | 按心情折算，约 40%–60% |
| 什么都没沾 | 心情很旺时 5% 左右随口接一句；心情低落直接潜水 |
| 夜里 00:00–07:00 | 非 @ 的消息不接 |

- 频率保护：两次之间至少 120 秒，每小时最多 8 条，每天最多 60 条。
- 兴趣词在面板「QQ」页改（逗号分隔）；也可以切成「只在 @ 我时回」或「群聊关闭」。
- 判断是纯函数（`lib/qq/group.js`），日志里会写 `join`（接了，附电量/兴趣）或 `lurk`（没接，附原因），面板能看到。
- 说话电量 = `0.5 + 0.5×愉悦 + 0.5×(唤醒−0.35)`，跟着当前 mood 走；低落时（愉悦 ≤ -0.3 且唤醒 ≤ 0.45）不主动插话。

### 只听不回：把回话交给别的桥

如果同一个 QQ 号还接着另一套桥，两边都回会重复。可以这样分工：

- 在面板「QQ」页勾上 **「只听不回」**（`qq.json` 里是 `"autoReply": false`），或在配置里手动加。
- Seed 仍然连着 OneBot：会记录你最后说话的时间（主动消息靠这个算「多久没说话」），但**不会建会话、不会回任何消息**；聊天回复全交给那套桥。
- 主动找主人照常工作——它走的是同一条连接，只是发消息，不参与对话。
- 日志里会写 `observe`（只听不回），方便确认没抢话。
- 反过来，如果想让 Seed 接管聊天，把勾去掉即可（记得先关另一套桥，别双回）。

## 与「刷B站」插件兼容（可选）

`dsh-bili-scroll` 每天会把「又刷了一轮」的日报写到 `~/.dsh/bili-duty/out/YYYY-MM-DD.md`。
本插件可以把其中的「值得看 / 可以看」条目收进待记：默认每 6 小时看一次最近 3 天的日报，
把「日期 + 标题 + 作者 + 一句话理由」放进「记忆」页的待记候选——**你点「记下」才会写进记忆**。

手动同步：`/seed bili [天数] [--dry]`；`--dry` 只预览不写入。

配置在 `cordis.patch.yml` 或 `seed` 配置里：`biliOutDir`（默认 `~/.dsh/bili-duty/out`）、`biliSync`（false 关掉自动同步）。

把这个目录也加进外部档案（`sources.json`）后，`seed_search` 能直接搜日报原文与理由。

### 面板里的「B站」页

- 自动检测 `dsh-bili-scroll`（刷B站）是否安装：没有安装时，打开这一页会弹一次确认框，点「是」直接装并启用，点「否」就不装（之后想装可以点页面上的「安装」）。
- 显示最近 7 天日报统计（份数、值得看、可以看、最新日期）、已同步视频数与时间。
- 「立即同步」把最近 3 天的「值得看 / 可以看」收进待记；去重靠 `bili-sync.json`。

### 面板里的「说明」页

完整的说明书在 `docs/GUIDE.md`，面板最后一页「说明」直接读它（`GET /dsh-seed-of-memory/guide`）：安装与升级、离线资源、每一页做什么、工具、配置、QQ 设置、常见问题。

## License

MIT
