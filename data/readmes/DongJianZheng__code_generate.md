# Code Forge · 离线工作工具箱

一个断网可用的多数据库工具。SQL 工作台支持字段描述、多表 `CREATE TABLE` 脚本与 `.sql` 文件，选择一张表生成常用 SQL。独立 Java 生成器可生成 MyBatis-Plus 的 Entity、Mapper、XML、Service 和 Controller。支持 MySQL、Oracle、SQL Server、达梦和 PostgreSQL。

新增独立的**工作命令库**：Windows、CentOS/Linux、Docker 与 Git 常用操作速查，支持收藏、搜索和记录自己的实践笔记。**Skill 经验库**则记录可复用工作方法、个人实践和公众号素材。四个入口互相导航，离线页面无需账号或 AI 调用；把 Skill 模板交给 AI 执行仍会消耗模型额度。

## Skill 经验库

打开 `code_generate/skill-library.html`，查阅本机个人 Skill 整理卡：task-governor、frontend-quality、playwright 已在本项目使用；enterprise-sdlc 仅确认已安装，标为待实践，不冒充高频使用统计。

每张卡包含适用/不适用场景、提问模板、步骤、产物检查、踩坑与可人工照做的方法。内置卡保留相对来源与 SHA-256 指纹，不复制本机路径或完整技能源码，也不能编辑或覆盖。可新增最多 100 张自建摘要，保存后可编辑内容但 ID 锁定；它们只表示本人整理，没有安装或实践证据，也不生成源码指纹。删除自建卡需确认，会一并删除关联笔记、收藏与素材选择，可从此前备份恢复。

自建摘要、笔记与收藏统一存入当前浏览器的 `code-forge.skill-library.v2`（`cards` + `notebook`）。没有新版资料时只读迁移旧键 `code-forge.skill-notes.v1`，保留旧版原件。JSON 备份包含已保存的自建摘要、笔记和收藏，不含未保存草稿，兼容导入 v1 笔记备份；导入先预览，同 ID 内容冲突时可比较字段、逐条选择当前或导入版本，默认保留当前。采用导入版本需额外确认，并可先备份合并前资料；不会自动拼接字段。备份及内置、自建卡片组成的总目录分别限制为 1 MiB UTF-8。

素材篮可勾选卡片导出公众号 Markdown 草稿，自建摘要默认不选入文章，个人笔记默认不导出。加入自建摘要或个人笔记都需要人工脱敏确认，不会直接发布。使用和数据边界见 [Skill 经验库说明](docs/Skill经验库.md)，写作底稿见 [公众号素材](docs/公众号素材-Skill经验沉淀.md)，本轮验收见 [Skill 冲突合并验收记录](docs/Skill冲突合并验收记录.md)。这是资料摘要工具，不是完整 Skill 安装包，也不会后台自动扫描更新。

## 工作命令库

打开 `code_generate/command-library.html`：按系统、分类或关键词搜索，核对 Shell、版本、权限和风险后复制。可将内置条目“复制为我的命令”，补充自己的场景、注意事项与标签，也可直接新增、编辑或删除个人条目。内置条目保持只读。

个人命令和收藏保存在当前浏览器；JSON 导出仅包含个人资料与收藏，导入经预览确认后合并。相同 ID 内容不同会拒绝，不静默覆盖资料。存储被禁用、写入失败或其他标签页修改资料时，会提示导出备份，当前页仍可使用。最多 500 条个人命令，备份上限 1 MiB，不应存入密码或 Token。

这里只展示、复制文本，不会执行命令或自动填充 Shell 参数。修改类和高风险命令复制前需要确认，但这不代表运行安全；先替换占位符并核对实际环境。使用说明见 [工作命令库](docs/工作命令库.md)，官方资料与核验边界见 [命令来源](docs/工作命令库来源.md)，当前测试与交付见 [验收记录](docs/工作命令库验收记录.md)。

## 离线 SQL 工具

打开 `code_generate/sql-workbench.html`，选择目标数据库与操作：

| 操作 | 可配置内容 |
| --- | --- |
| 建表 | 从表结构生成目标数据库的 DDL |
| 插入数据 | 1–100 行参数模板，或 1–1000 行模拟测试数据；默认跳过自增列 |
| 查询数据 | 配置返回字段、条件操作符、AND/OR、多字段排序和结果条数上限 |
| 修改数据 | 分别选择修改字段和带操作符的 WHERE 条件 |
| 删除数据 | 配置带操作符的 WHERE 条件 |
| 添加字段 | 输入字段名、类型、可空性和受控默认值 |
| 修改字段类型 | 选择已有字段并填写新类型 |
| 查询表结构 | 生成目标数据库的系统目录查询 SQL |

插入默认生成参数模板，也可切换到“模拟数据（测试用）”：按字段类型生成带实际字面量的 INSERT，支持行数、随机种子、起始编号和基准日期，预览前 10 行并复制或下载。可给状态、测试部门 ID 等普通字段设候选值：单值固定，多值按种子抽取；不勾选插入的字段会暂停规则并保留草稿。纯本地计算，不调用 AI，不消耗 Token；详情见 [SQL 模拟数据](docs/SQL模拟数据.md)。

查询、修改、删除仍生成参数模板，不接收真实数据，界面列出绑定顺序。条件支持比较、LIKE、IN、BETWEEN 和空值判断；多个条件可用 AND 或 OR 统一连接，暂不支持嵌套分组。修改与删除未选择条件时不生成 SQL，条件未以 AND 等值覆盖完整主键时提示可能影响多行。

批量插入中，MySQL、PostgreSQL、SQL Server 使用多行 VALUES；Oracle、达梦输出多条单行 INSERT，参数在整份文件中连续编号，不自动添加事务。SQL 工具允许无主键与复合主键的表，Java 工程模板仍要求单一主键。两个页面均不连接数据库、不执行 SQL。

查询支持按页生成 SQL：设置页码、每页条数与排序，缺少排序时会拦截。左侧“保存与备份”可手动保存一份本机配置，也可导入 / 导出版本化 JSON；恢复前需确认，不会自动覆盖当前输入。配置文件包含表结构，请妥善保管。

支持 UTF-8 `.sql` 文件预览导入，最多 100 张表、1 MiB / 262144 字符。切表会重置操作设置，完整 SQL 保留；非建表语句不执行、不应用。配置 JSON 已升级到版本 4，保存当前选中表、模拟数据设置与候选规则，兼容版本 1、2、3 导入。

### 离线分发

开发者在仓库根目录执行：

```bash
npm run build:offline
```

将生成的 `dist/code-forge-offline.zip` 分发给使用者。完整解压后双击 `sql-workbench.html`、`command-library.html`、`skill-library.html` 或 `生成代码.html`。使用者不需要安装 Node、Python、数据库驱动或前端依赖；不要只复制一个 HTML 文件，需保留同目录脚本、样式及 `vendor` 文件夹。

操作说明与适用边界见 [离线 SQL 工具说明](docs/离线SQL工具.md)，本次验证结果见 [离线 SQL 验收记录](docs/离线SQL验收记录.md)。

> V2 源自 2025 年的公众号文章《[基于 Vue + Element UI 的智能代码生成器设计与实现](https://mp.weixin.qq.com/s/BiOdmjRETMCF5-J6BKAD1w)》。这次升级先用真实示例复现旧版问题，再以自动测试约束解析和生成结果。

## V2 更新

- 使用统一 `SchemaModel` 驱动预览和 ZIP，避免类名、表名和文件路径互相冲突。
- 顶层逗号解析感知括号与引号，正确处理 `DECIMAL(10,2)`、带逗号的注释和函数默认值。
- 支持单列表级主键、`IF NOT EXISTS`、实际默认值、字段长度和精度；核心可把复合主键转成单个表级约束，页面会明确停止不兼容的整套工程预览和导出。
- 数据库增加 PostgreSQL，现支持 MySQL、Oracle、SQL Server、达梦和 PostgreSQL。
- 增加实时错误/警告、错误时禁止导出、本地历史快照和响应式界面。
- 修复 `BigDecimal` import、Mapper XML 尾逗号、非自增主键策略和时间字段自动填充。
- Controller 模板升级为 OpenAPI 3，并增加分页查询接口。
- ZIP 一次包含 5 种 DDL、Java/XML 文件和生成说明。

## 运行

无需安装前端依赖：

```bash
git clone https://github.com/DongJianZheng/code_generate.git
cd code_generate
python3 -m http.server 4173 --directory code_generate
```

浏览器打开：

```text
http://localhost:4173/sql-workbench.html
```

Vue、Element UI、JSZip、样式和字体已固定版本并随仓库提供，不再从 CDN 加载。四页均在本机处理输入；参考文档仅主动点击时联网。第三方库的版本、来源、许可证和校验值记录在 `code_generate/vendor/README.md`。

本地 HTTP 服务仅用于开发调试。离线使用请完整保留目录结构，直接打开 HTML；若浏览器限制剪贴板，可手动选择复制或下载 `.sql` 文件。

## 测试

当前全量验收为 **192 项通过，0 失败**，模拟数据与字段候选规则的验证范围见 [模拟数据验收记录](docs/SQL模拟数据验收记录.md)。工具箱初版的 160 项历史结果见 [发布验收记录](docs/发布验收记录.md)；后续数量以 `npm test` 输出为准。

测试只使用 Node.js 内置测试框架，不安装生产依赖：

```bash
npm test
```

测试覆盖解析与代码生成、五种方言 SQL 操作、参数绑定、条件操作符与写入拦截、排序与分页、批量插入、模拟数据与容量边界、字段变更、配置往返与严格校验、命令目录和个人资料合并/搜索、离线资源完整性。

## 字段配置语法

```text
#表名: order_item 订单明细
#类名: OrderItem
主键:id bigint [主键,自增]
订单编号:order_no varchar(64) [非空]
订单金额:amount decimal(10,2) [非空,默认值=0]
状态:status varchar(20) [非空,默认值='pending']
创建时间:created_at datetime [非空,默认值=CURRENT_TIMESTAMP]
```

## 目录

```text
code_generate/
├── skill-library.html  # Skill 经验库入口
├── skill-library.js    # 实践笔记、本机保存与公众号素材交互
├── skill-library.css   # 复用已有风格的经验库局部样式
├── skill-library-core.js # 笔记校验/合并与安全 Markdown 素材
├── skill-catalog.js    # 四份个人 Skill 的整理快照与来源指纹
├── command-library.html # 工作命令库入口
├── command-library.js   # 收藏、编辑、本机保存与备份交互
├── command-library.css  # 复用工作台样式的局部布局
├── command-library-core.js # 资料校验、搜索与合并
├── command-catalog.js   # 随包提供的内置命令目录
├── sql-workbench.html  # 离线 SQL 工具入口
├── sql-workbench.js    # SQL 工具交互
├── sql-workbench.css   # 本地页面样式
├── sql-operations.js   # SQL 操作生成与校验
├── sql-mock-data.js    # 可复现的离线模拟数据与 INSERT 字面量
├── sql-script.js       # 多语句切分、表识别与注释归属
├── sql-workspace.js    # 配置格式、大小与字段引用校验
├── vendor/            # 固定版本本地依赖与许可证
├── generator-core.js   # 可测试的解析、校验、类型映射和 DDL 生成核心
├── templates.js        # MyBatis-Plus / Spring 代码模板与模板引擎
└── 生成代码.html        # Vue 2 + Element UI 单页界面
tests/
├── skill-library.test.js
├── skill-custom.test.js
├── skill-merge.test.js
├── skill-catalog.test.js
├── command-library.test.js
├── command-catalog.test.js
├── generator-core.test.js
├── sql-operations.test.js
├── sql-mock-data.test.js
├── sql-script.test.js
├── sql-workspace.test.js
└── offline-package.test.js
scripts/
├── browser-skills.js    # Skill 笔记、素材隐私边界与断网验收
├── browser-skill-custom.js # 自建摘要、旧资料迁移与备份验收
├── browser-skill-merge.js # 冲突对比、确认替换与恢复验收
├── browser-commands.js  # 命令库搜索、个人资料、风险确认与断网验收
├── build-offline.js      # 校验本地依赖并生成离线 ZIP
├── browser-smoke.js      # 浏览器操作路径与断网验证
├── browser-enhancements.js # 条件、排序、批量插入与默认值交互验收
├── browser-workspace.js  # 配置备份恢复、分页与存储故障验收
├── browser-sql-mock.js  # 模拟数据、配置迁移、下载与断网验收
├── browser-mock-rules.js # 字段候选值、规则备份与暂停/恢复验收
└── browser-multitable.js # SQL文件、多表切换、版本迁移验收
docs/
├── Skill经验库.md
├── 公众号素材-Skill经验沉淀.md
├── 工作命令库.md
├── 工作命令库来源.md
├── assets/              # 文章与验收截图
├── 离线SQL工具.md
├── SQL模拟数据.md
├── 离线SQL验收记录.md
├── V2-验收记录.md
└── 公众号文章-V2.md
```

## 边界

- SQL 工作台可以载入多表脚本，但每次只为选中表生成，不是完整 SQL 方言解析器。过程块与自定义分隔符不支持，忽略的 ALTER 等语句不会更新模型；分区表、复杂表达式等仍需人工复核。跨库 DDL 不是自动迁移方案。
- SQL 工具默认输出参数模板，参数应在数据库驱动中绑定；模拟插入模式输出合成测试值，不保证与已有数据不重复，也不保证满足外键、CHECK、唯一索引及业务规则。两种模式均不执行 SQL，批量提交与回滚由执行程序控制。新增非空字段需要规划存量数据填充；字段类型修改不能保证旧数据可转换，主键、自增列和无法完整恢复的 MySQL 列属性会被拦截。
- MyBatis-Plus `BaseMapper` 工程模板只支持单一主键；检测到复合主键时会停止整套工程预览和导出并提示处理。
- 生成的 Java 代码需要宿主工程提供 Spring Web、MyBatis-Plus、Lombok 和 springdoc-openapi 依赖。
- 自动测试验证解析和文本生成；尚未连接五种真实数据库执行全部 DDL，也未在完整 Spring Boot 示例工程中编译生成代码。

新版改造过程与前后对比见 [公众号文章草稿](docs/公众号文章-V2.md)，实测步骤与结果见 [V2 验收记录](docs/V2-验收记录.md)。
