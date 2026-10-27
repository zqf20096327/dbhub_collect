# dsh-web-search-pro

增强型、可持久化的扩展网页搜索插件 for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）。

一个 DSH **bundle 插件**，把多引擎网页搜索、平台搜索、持久化缓存、受控按站增强和 Playwright 渲染打包成模型可调用的能力。常驻上下文只有 `web_index` / `web_call` 两个工具（原 11 个 `web_*` 工具已并入 20 个动作，见[工具面](#工具面索引--调用)）。路由控制面借鉴 Agent-Reach 的后端探测、顺序选择和失败冷却思路，核心逻辑为本项目原生 TypeScript 实现。

## 兼容与发布通道

| 插件发布通道 | DSH 基线 | 兼容承诺 |
|---|---|---|
| `0.1.11` 及更早的维护版本 | `dsh-v0.1.1-rc.2` | 旧基线；不再维护，不与新插件混装 |
| `0.1.15` | `dsh-v0.1.7-rc.2` + Browser `0.1.15` | 精确锁定该宿主版本；**仍停留在 DSH 0.1.x 宿主或 dsh-browser 0.1.x 的用户请使用这一版**（后续不再更新） |
| `0.1.17` | `dsh-v0.1.7-rc.2` ~ `dsh-v0.2.0-rc.2` + Browser `0.1.17` | 过渡版本，已不再演进；新功能不会回到这条线 |
| `0.2.0`（正式版） | **只支持 `dsh-v0.2.0-rc.2` 这一条线**（peer `>=0.2.0-rc.2 <0.2.1-0`）+ 可选 `@anweat/dsh-browser ^0.2.0` | 第一个 0.2.0 线版本，**破坏性变更**（见 [CHANGELOG.md](./CHANGELOG.md)）；711 项单元测试、94 项 bench 测试，`pnpm run test:peers` 两种解析模式检查，真实 Host（DSH 0.2.0-rc.2）验收 |
| `0.2.1` | 同 `0.2.0`（peer `>=0.2.0-rc.2 <0.2.1-0` + 可选 `@anweat/dsh-browser ^0.2.0`） | 独立 CLI 适配层与平台后端链，无破坏性变更（见 [CHANGELOG.md](./CHANGELOG.md)）；774 项单元测试、94 项 bench 测试，真实 Host（DSH 0.2.0-rc.2）验收 |
| `0.2.2` | **只支持 `dsh-v0.2.1-rc.2` / `dsh-v0.2.1-rc.3`（0.2.1 线）**（peer `>=0.2.1-rc.2 <0.2.2-0`）+ 可选 `@anweat/dsh-browser ^0.2.0`（配套 `0.2.2` 起，旧的 0.2.0 / 0.2.1 只适用于 0.2.0-rc.2 宿主） | 适配 DSH 0.2.1-rc.2 / rc.3 宿主（cordis 4.0.5、schemastery 3.18.5、cordis-plugin-group 1.0.5 / loader 1.0.6 / include 1.0.10、cosmokit 1.8.6），并修复 twitter 平台结果全错（[#38](https://github.com/anweat/dsh-web-search-pro/issues/38)）；无破坏性变更。npm 上的 0.2.1 在 0.2.1-rc.x 宿主上会被安装闸门拒绝，需要升级到本版。devDeps 里停更的 `dsh-invariants` 换成 `dsh-working-directory`，并显式补上 0.2.1 线改成 peer-only 的 `dsh-llm` / `dsh-session`（宿主 `autoInstallPeers: false` 不自动装 peer）；790 项单元测试、94 项 bench 测试、`pnpm run test:peers` 两种解析模式检查；真实宿主验收（rc.3）见 `docs/validation/dsh-0.2.1-rc.3.md`。twitter 的搜索输出契约来自 twitter-cli 0.8.5 源码与 issue 里的真实输出，我们自己没有用 Token 跑过搜索 |
| `0.2.3` | **两条宿主线同时支持**：`dsh-v0.2.0-rc.2`（0.2.0 线）与 `dsh-v0.2.1-rc.2` ~ `rc.4`（0.2.1 线）；peer `>=0.2.0-rc.2 <0.2.1-0 \|\| >=0.2.1-rc.2 <0.2.2-0`，cordis `~4.0.4`；可选 `@anweat/dsh-browser ^0.2.0`（0.2.0 线配 Browser `0.2.0` / `0.2.1` / `0.2.2`，0.2.1 线配 `0.2.2` 起） | 接入 **DeepSeek Search / Fetch API** 并标为“常用”（有 Key 时默认排第一；**按请求计费**，见下文“DeepSeek 搜索 / 抓取”）；设置面板同步调整。无破坏性变更，但**已有 `DEEPSEEK_API_KEY` 的用户升级后默认搜索会走这个付费接口**（`sources.disabled: [deepseek]` 关闭）。宿主适配没有改任何运行时代码：面板保存、私有 RPC、凭据、审批钩子在 0.2.0-rc.2 上与 rc.3 / rc.4 行为一致（见 `docs/validation/2026-10-28-host-lines-and-install.md`）；测试数见 [CHANGELOG.md](./CHANGELOG.md) |

**支持范围**：DSH `>=0.2.0-rc.2 <0.2.1-0 || >=0.2.1-rc.2 <0.2.2-0`，已在真实宿主上验证 `0.2.0-rc.2`、`0.2.1-rc.3`、`0.2.1-rc.4`（`0.2.1-rc.2` 与 rc.3 同源，由 `test:peers` 的范围检查覆盖）；`0.2.0-rc.1`、`0.2.1-alpha.x`、`0.2.1-rc.1`、`0.2.2` 及以上都被拒绝。可选配套浏览器插件 `@anweat/dsh-browser ^0.2.0`（即 0.2.x，不含 0.3）：0.2.0 线宿主上用 Browser `0.2.0` / `0.2.1` / `0.2.2`，0.2.1 线宿主上必须是 `0.2.2` 起（旧的 0.2.0 / 0.2.1 的 peer 只含 `<0.2.1-0`，会被 0.2.1 线宿主的安装闸门拒绝，并且**整次安装作废**，插件也不会装上）。

**不再支持 DSH 0.1.x 宿主线，也不再支持旧的 dsh-browser 0.1.x 线；仍在这两条线上的用户请停留在 dsh-web-search-pro 0.1.15。**

- DSH 0.1.x 宿主：peer 范围不再包含它，`dsh plugin add` 会因 peer 不满足而拒绝，或在组装期点名报 `incompatible`。本插件已去掉为旧宿主保留的兼容分支。
- 旧 dsh-browser 0.1.x：浏览器是可选依赖，本插件仍会**识别**它但不会驱动它。服务对象没有版本字段，所以以形状判定：不带任何 0.2 才有的方法（`observe` / `listTargets` / `sessionState`）即视为旧线。检测到旧线时：
  - `read.snapshot`、`read.fetch mode=playwright`、浏览器平台与 OpenCLI 平台返回 `CAPABILITY_UNAVAILABLE`：`dsh-browser 0.1.x is not supported by web-search-pro 0.2+; upgrade to @anweat/dsh-browser ^0.2.0`；
  - `read.fetch mode=auto` 不再尝试浏览器渲染，静默跳过（全部后端失败时，错误说明里会写明原因）；
  - `sources.status` 显示 `browser: legacy (unsupported)`；系统提示不加浏览器那一行；旧服务上的 `automationMode` 不参与写操作审批（按没有 Browser 处理，`standard` 下询问）；
  - 其他一切（网页搜索、证据管线、非浏览器平台、缓存、历史）照常工作。

**peer 范围的写法**与 `@anweat/dsh-browser 0.2.x` 完全一致：每个 `@deepseek-ai/dsh-*` peer 都是两段并联的范围 `>=0.2.0-rc.2 <0.2.1-0 || >=0.2.1-rc.2 <0.2.2-0`，cordis 为 `~4.0.4`。

- 宿主的组装期校验用的是 `semver.satisfies(host, range, { includePrerelease: true })`；真正决定装机成败的是 npm/pnpm 的**默认** semver：预发布版本只有在某个比较符自带同号（同 

[...截断...]

major.minor.patch）预发布时才被判为满足。两段各自的下界（`>=0.2.0-rc.2`、`>=0.2.1-rc.2`）自带同号预发布，是**承重**的，必须保留；写成 `>=0.2.0-rc.2 <0.2.2-0` 这类跨线的单段范围会过宿主校验、却让 `dsh plugin add` 报 ERESOLVE。与 `@anweat/dsh-browser` 必须声明同一套策略，否则两者互为 peer 时会出现 ERESOLVE。
- 两段之间留了缝：`0.2.1-alpha.1` ~ `0.2.1-rc.1` 没有验证过，两种解析模式都拒绝。上界是 `<0.2.2-0` 而不是 `<0.2.2`：后者放行 `0.2.2-alpha.1` 这类 0.2.2 的预发布。收口后，若 0.2.2 真出现破坏，会在**组装期**直接报 `is incompatible with dsh 0.2.2` 并点名，而不是拖到用户机器上变成运行期怪错（`0.1.5 → 0.1.7` 曾一次性打断所有按 `0.1.5-alpha.1` 构建的插件）。
- cordis：0.2.0-rc.2 宿主依赖 `~4.0.4`，0.2.1-rc.x 依赖 `~4.0.5`，干净安装时两者都解析到 4.0.5（有锁文件的 rc.2 宿主可能是 4.0.4）。peer 写 `~4.0.4`（`>=4.0.4 <4.1.0`）同时容纳两者，挡住 4.1.0。schemastery 的 peer `^3.18.5` 不变：两条线的宿主都解析到 3.18.5。
- 范围只表示「测过哪些」，不等于承诺不破坏；真正的防线是每换一个 DSH 版本重跑一遍这套验证。`pnpm run test:peers`（已并入 `pnpm verify`）用两种解析模式逐个断言受管 peer：`0.2.0-rc.2`、`0.2.1-rc.2` ~ `rc.4` 必须通过，`0.1.7-rc.2`、`0.2.0-rc.1`、`0.2.1-alpha.5`、`0.2.1-rc.1`、`0.2.2-alpha.1` 必须被拒绝，cordis `4.0.4` / `4.0.5` 通过、`4.1.0` 拒绝；并自带 `--selftest` 已知行为自校验（含两段范围的缝）。开发依赖固定在 `0.2.1-rc.3`（单元测试跑在这一套类型上）；0.2.0-rc.2 与 rc.4 靠真实宿主验证，不靠第二套 devDependencies。

## 安装

```bash
# 默认安装（面向 dsh-v0.2.0-rc.2 与 dsh-v0.2.1-rc.2 ~ rc.4 宿主；浏览器插件可选，需要读取渲染页 / 浏览器平台时一起装）：
dsh plugin --profile web add @anweat/dsh-browser@0.2.2 dsh-web-search-pro@0.2.3
# 不需要浏览器能力时，只装本插件即可：
dsh plugin --profile web add dsh-web-search-pro@0.2.3
# 或本地目录 / tarball：
dsh plugin --profile web add ../dsh-browser ./dsh-web-search-pro
# 重启（web profile 关闭了 HMR）：
dsh --profile web
```

> 两个插件都必须是 profile 的直接依赖：DSH 只激活直接依赖的 bundle layer，且标准 profile 可能设置 `autoInstallPeers: false`。不要只安装 Web Search Pro 后依赖 peer 自动补齐。
> **新用户第一次安装**：只装本插件时，`dsh plugin add` 在 pnpm 11 下退出码为 0、没有任何警告（本包没有安装脚本，也不依赖 OpenCLI 或 Playwright；约 20 个包、10 MB）。要一起装浏览器插件，用 `@anweat/dsh-browser` **0.2.2 起**：它不再把 `@jackwener/opencli` 作为依赖，所以不会再有 `ERR_PNPM_IGNORED_BUILDS`（`0.2.1` 及更早的 Browser 会让 pnpm 11 拦下 OpenCLI 的安装脚本，`dsh plugin add` 以失败退出，**包其实装上了、插件却没有被加入 profile 的 bundles，之后再 `add` 任何包也都会同样失败**，连带的本插件也不会被启用；用 0.2.1 线宿主的用户在这点上没有选择，只能升级到 0.2.2）。
> **第一次使用**：① 网页搜索、证据管线、CLI 平台不需要浏览器，装完即用。② `read.snapshot`、`read.fetch mode=playwright`、搜索页类平台需要浏览器插件，且**有 Google Chrome / Microsoft Edge 就直接用**（不用下载 Playwright 的 Chromium）；都没有时 `sources.status` 的 `browser:dsh-browser` 一行会写 `loaded, no browser to launch` 和 dsh-browser 给的可照做的步骤（装 Chrome / Edge，或 `runtime.install`，或终端命令）。③ 小红书 / 知乎 / Reddit / X 要用你日常 Chrome 的登录态：`npm i -g @jackwener/opencli` 并装它的 Browser Bridge 扩展（`opencli doctor` 全 OK），本插件优先用 PATH 上的独立 `opencli`；没有它这几个平台会往后落到独立 CLI 或 dsh-browser 的后端，`sources.status` 写明原因。OpenCLI 与浏览器的装法细节见 [dsh-browser 的 README](https://github.com/anweat/dsh-browser#readme)。
> 本版支持 `dsh-v0.2.0-rc.2` 与 `dsh-v0.2.1-rc.2` ~ `rc.4`，Browser 为 `^0.2.0`（0.2.1 线宿主上必须是 0.2.2 起的 0.2.x），宿主或浏览器插件仍在 0.1.x 线上的，请安装 `dsh-web-search-pro@0.1.15`。若你的 harness 是本地源码 checkout，版本号可能有出入——用
> `dsh plugin --profile web add ./<path>` 并在 profile 的 `pnpm-workspace.yaml`
> 里对齐版本后重装即可。

## 从旧版本升级

先确认宿主是 `dsh-v0.2.0-rc.2` 或 `dsh-v0.2.1-rc.2` ~ `rc.4`，浏览器插件（如果装了）是 `@anweat/dsh-browser@0.2.2`（或更新的 0.2.x；0.2.0-rc.2 宿主上 0.2.0 / 0.2.1 也可以）；两者都需要作为 profile 的直接依赖。

```bash
dsh plugin --profile web add @anweat/dsh-browser@0.2.2 dsh-web-search-pro@0.2.3
```

> **不再支持旧线**：宿主仍是 DSH 0.1.x，或浏览器插件仍是 `@anweat/dsh-browser` 0.1.x，请不要升级，停留在 `dsh-web-search-pro@0.1.15`。只升级本插件、保留旧浏览器插件时，本插件照常工作，但所有浏览器相关能力都会返回上面的 `CAPABILITY_UNAVAILABLE`，`sources.status` 显示 `browser: legacy (unsupported)`。

> **破坏性变更（工具面）**：旧的 `web_search_pro`、`web_fetch_pro` 等 11 个工具名不再注册，也没有兼容包装。旧会话里对它们的调用会失败；把调用改成对应动作即可，对照表见[旧工具到新动作](#旧工具到新动作)。模型在 `web_call` 里写旧工具名会得到新动作名和翻译后的参数，`web_index()` 根目录也列出同一张对照。已存储的数据（历史、页面、规则、证据、账本）与 `ctx.web` provider 不受影响。其他不兼容变化与新功能见 [CHANGELOG.md](./CHANGELOG.md)。

升级完成后需要**完整停止并重新启动 Web profile**；仅刷新网页不会重新扫描插件的 `client.js`。随后依次检查：

1. `browser_call({action:"runtime.status"})`：确认 OpenCLI、`playwright | patchright` 运行时、`automationMode` 与 `usagePolicy` 符合预期。
2. `web_call({action:"sources.status"})`：确认搜索、CLI、Agent Reach 与浏览器后端是否 ready（浏览器应显示 `ready`，不是 `legacy (unsupported)`）。
3. 打开 `插件 → 已安装` 中两个 bun