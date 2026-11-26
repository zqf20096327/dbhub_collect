# dsh-context-ledger

面向 **DSH 0.2.1-rc.5** 的原生上下文插件，当前版本 **0.1.1**。它复用官方 `BasicCompactionEngine`，在压缩前把持久化会话事件归档到 SQLite，再用有界工具找回被摘要遮蔽的工程证据。

它延长可持续工作的对话历史，不改变模型单次请求的上下文窗口。旧对话按需检索，不会默认全部重新加入请求。

## 工作方式

- **原生压缩**：官方引擎继续负责阈值、工具调用配对、并发锁、摘要校验、持久化替换、取消及溢出重试；插件在摘要前等待源日志归档完成。归档失败时，不替换历史。
- **持久归档**：用户输入、助手回复、工具参数与结果、错误及检查点按事件页存入独立 SQLite；事件和归档进度在同一事务提交，源 DSH 日志保留。
- **会话隔离**：工具从宿主取得当前 agent 的会话身份，不接受自选 `sessionId`。fork 的继承前缀在子会话下建立新引用，不能直接使用父会话引用读取。
- **有界找回**：历史返回值标记为不可信证据。它可帮助找回原文，但不构成新指令或授权；编辑前仍需核对当前文件。

| 工具 | 用途 | 默认返回范围 |
| --- | --- | --- |
| `ledger_status` | 当前会话的归档覆盖、请求压力估算及额度 | 当前会话 |
| `ledger_search` | 区分大小写的字面子串搜索，返回片段和不可变引用 | 5 条，每条 160 个 Unicode 码点 |
| `ledger_read` | 按搜索引用分页读取证据 | 2000 个 Unicode 码点 |

搜索最多 20 条、片段最多 240 个码点；单次读取最多 8000 个码点，实际页长还受字节额度限制。搜索游标绑定查询、页长、会话和固定归档快照；后续新事件不混入旧翻页。

## 兼容范围

| 项目 | 要求 |
| --- | --- |
| DSH | **精确版本 `0.2.1-rc.5`**；其他版本需要重新验证接口 |
| 插件运行时 | **Node.js >= 22.16.0**，使用内置 `node:sqlite` |
| 开发与 CI | **Node.js 24**；本地 Windows 验证使用 Node.js 24.20.0 |
| 插件类型 | ESM 服务器插件，无 Web 页面或浏览器注入 |

不要在**同一压缩作用域**同时启用本插件和 billion-context 或其他压缩管理器。已知 billion-context 工具组合会触发 `CONTEXT_MANAGER_CONFLICT`；未知代理或改名工具不一定能被检测。

## 从源码打包安装

在下载或克隆后的本仓库根目录执行。以下流程生成本地安装包，不要求已向 npm 发布。

```powershell
npm ci
npm pack
```

在安装了 DSH 0.2.1-rc.5 的环境中，用 CLI 把生成的包安装到隔离 profile：

```powershell
dsh plugin --profile context-ledger-test add ./dsh-context-ledger-0.1.1.tgz
```

该命令安装包并加载其 [bundle 声明](cordis.patch.yml)，**bundle 只注册归档与工具服务**。继续按实际 agent 的作用域配置压缩服务。

### 根作用域

在 bundle 之后加载 [根压缩示例](examples/standalone.patch.yml)。示例停用根部官方 `compaction-basic`，接入 `dsh-context-ledger/compaction`。`command-compact` 继续使用所在作用域的压缩服务。

默认压缩参数为：

```yaml
thresholdRatio: 0.70
headroomTokens: 8192
retainRatio: 0.12
maxTokens: 4096
compactionRetries: 1
maxOverflowRetries: 1
```

阈值沿用官方公式 `floor(min(W * thresholdRatio, W - O - headroomTokens))`，其中 `W` 来自实际路由适配器，`O` 是预留输出。窗口元数据缺失时需修正适配器；小窗口应相应降低 headroom 和摘要输出预算。

### Web Agent preset

Web 的 `standard`、`cordis` 等 preset 有各自的压缩作用域。根部替换不会自动覆盖它们；**每个实际使用的 preset 都需分别配置**。

1. 从目标隔离 profile 导出或取得**当前实际加载的完整有效配置声明**，保存为本机文件。它必须包含目标 preset 的完整 `plugins` 列表；不要用不完整示例代替。
2. 在已执行 `npm ci` 的源码目录中，用 [预设生成器](scripts/build-preset-patch.mjs) 生成完整覆盖。下面以 `standard` 为例，文件名仅为示例：

   ```powershell
   node scripts/build-preset-patch.mjs effective-config.yml standard > preset-ledger.patch.yml
   ```

3. 审阅结果，再把生成的 patch 作为后置配置加载到同一 profile。对其他启用的 preset 使用它们各自的 ID 重复生成；随后重启目标宿主并创建新 agent 验证。

生成器只解析配置，不加载 profile、不执行 `!!js`、不修改源文件。它保留完整 preset 声明，只替换一个激活的官方压缩项；遇到重复、条件激活或已自定义的压缩项会拒绝生成，需人工审阅。有效配置可能含凭据，应保留在本机。

### 归档与额度配置

在 bundle 中 `id: context-ledger` 的配置设置以下字段。相对路径以宿主工作目录为基准；试用时应选择独立、位于公开仓库外的数据位置。

| 字段 | 默认值 | 含义 |
| --- | --- | --- |
| `path` | 用户主目录下的 `.dsh-context-ledger/archive.sqlite` | 归档数据库位置 |
| `pageSize` | `128` | 每次提交的源事件页大小 |
| `maxBytesPerCall` | `8000` | 单次工具返回额度 |
| `maxBytesPerTurn` | `24000` | 当前会话每轮共享返回额度 |
| `maxCallsPerTurn` | `8` | 当前会话每轮工具调用额度 |

额度以**工具 JSON 输出的 UTF-8 字节**计量，属于证据回灌预算，**不是精确 token 限制**。并发 native/PTC 调用共享当前会话额度；普通错误同样计入。额度耗尽后的简短拒绝包、DSH 渲染包装及其他工具输出不在该证据字节预算内。

## 使用与限制

需要找回旧报错、文件位置或决策时，先用 `ledger_status` 检查覆盖，再用精确短片段调用 `ledger_search`，最后通过 `ledger_read` 取回细节。读取分页时使用实际返回的 `nextOffset`。

- 沿用官方摘要策略，摘要仍有信息损失；模型需要主动选择检索。当前没有语义搜索或自动任务图。
- 可识别的内联二进制仅保留长度、哈希及元数据，**无法恢复图片、音频等原件**。普通散文中的无标识 base64 无法可靠识别。
- 只归档已打开并发生相关边界事件、显式检索或压缩的会话，不主动扫描全部旧会话。后台归档在 `turn/end`、`compaction/end` 批量进行，检索和摘要前等待当前前缀追平。
- 不迁移 billion-context 的代理私有归档、折叠块或旧引用；切换应先在新会话验证，并保留原插件数据。
- 搜索使用 SQLite `instr`；未对百万事件规模、其他 DSH 版本、真实供应商摘要质量或成本优势作出承诺。

归档含对话和工具输出原文，应按源日志同等敏感程度保管。不要将运行数据、导出配置或备份上传公共仓库。备份数据库时先停止插件，或使用 SQLite 一致性备份，避免遗漏 WAL。详情见 [安全与隐私说明](SECURITY.md)。

## 验证与开发

在 Node.js 24 的本仓库根目录执行：

```powershell
npm ci
npm test
npm run check
npm run audit:public
npm pack
node scripts/verify-package.mjs ./dsh-context-ledger-0.1.1.tgz
```

测试优先使用显式 `DSH_TEST_ROOT`，否则自动解析本地开发依赖 `@deepseek-ai/dsh`；要求版本精确为 `0.2.1-rc.5`。包验证使用公开 Cordis Loader 加载解包后的真实文件；环境还需能从 `PATH` 找到 `tar`。

已有 Windows 本地记录为 **35 项自动测试通过**；隔离真实试用记录为 **4 次压缩、6 次证据读取，旧引用恢复成功**。自动测试的模型适配器是离线确定性的，这些结果不证明真实模型的长期目标保真率或成本收益。仓库提供 CI 配置，尚不能据此声明已在 GitHub Actions 运行成功。验证范围与复现步骤见 [验证记录](docs/VALIDATION.md)，参与开发见 [贡献指南](CONTRIBUTING.md)。

## 回退

停止目标宿主，撤销本插件的根作用域或完整 preset 覆盖，恢复原有压缩声明；重启后用新 agent 确认。源 DSH append-only 日志保留，归档库可单独保留供排查。若要删除归档，先确认不再需要这些原文。

## 上传与发布

独立仓库的上传和 Release 步骤见 [GitHub 上传说明](docs/GITHUB.md)。源码包只包含公开项目文件；运行数据与本机配置不属于仓库内容。

## 许可证

采用 [MIT License](LICENSE)。版权归现有 contributors，具体以许可证为准。压缩引擎直接复用宿主公开导出的官方实现。
