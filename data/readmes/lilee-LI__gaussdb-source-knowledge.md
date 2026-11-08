# GaussDB 源码知识工程 2.3

从完整源码、设计文档、用户手册和可选的 ECS 编译调用图，建立版本绑定的学习计划、经审阅的结构化知识和 Wiki。支持模块持续学习、不同服务器离线协作、覆盖验收和开发／测试／review 上下文查询。

**操作手册：[迁移到 GaussDB](MIGRATE-GAUSSDB.md)。工程合同：[全仓持续学习](docs/WHOLE-REPOSITORY.md)。验证范围：[2.3 验证报告](docs/VALIDATION-2.3.md)。**

直接看 [openGauss实际输出](assets/examples/opengauss-2.3/README.md)：全仓计划、Wiki、结构化知识和三类使用上下文；试点未覆盖范围保留为未完成。

## 输入和输出

- 输入：本地已有源码；可选设计、手册；可选 ECS `knowledge.sqlite3` 调用图。不会自动下载产品源码。
- 全仓计划：`home/whole/PLAN.md`、`PLAN.json`、`COVERAGE.csv`、`index.html`。按领域和目录模块归属，每个资产可追踪。
- 权威知识：学习工作区 `knowledge.sqlite3` 中的版本、任务、证据、已审知识、知识关系与覆盖账。`wiki.git` 保存知识修订。
- Wiki：同一已审知识的 HTML／Markdown 阅读视图；不复制整个源码图。
- 使用：`ask`／MCP 返回证据上下文与未决项，供已有 Claude 或开发工具使用。

完整图只读挂接到协调端；学习库不复制图。成员材料包包含本模块、证据文件和一跳图，成员不需要共享协调端 SQLite，不需要每人搬完整图。大公共模块的包仍可能较大；按自然目录细分或调整归属后分派。

## 配置后启动

Windows 准备 Python 3.12、Git 和已登录的 Claude Code。发行 ZIP 包含基础依赖的离线 wheel；源码克隆需同时取得仓内 wheelhouse。Claude、认证和产品源码不打包。Linux 对应使用 `sh kb.sh`。

```powershell
New-Item -ItemType Directory -Force local | Out-Null
Copy-Item paths.example.json local/paths.json
notepad local/paths.json
.\kb.cmd check
.\kb.cmd start
.\kb.cmd plan
```

只需在 `local/paths.json` 填写真实路径。缺少设计、手册、ECS 图可删掉相应字段；没有图时仍能用冻结文本研究，调用和宏配置保持待核。CHM 先导出 HTML。

`start` 自动盘点完整检出目录、额外编译材料和文档；按自然目录细分宽模块，生成领域归属、模块调查及公共机制／集成工作包。默认 PostgreSQL 家族策略含 20 个领域、10 项公共机制、12 项跨域主题；目录未匹配会生成范围调查，不能默认为不适用。领域与主题是规划模板，正确性需要源码研究。

它不会把每个函数或每条调用边变成任务。原始注册／语法／测试线索留在候选账，模块盘点通过审阅后，才按机制归并产生有预算、有依赖的深度任务。

## 持续学习与审阅

```powershell
.\kb.cmd modules
.\kb.cmd next --worker learner-a --module '<完整模块名>'
.\kb.cmd run --worker learner-a --module '<完整模块名>' --steps 1 --budget 3
.\kb.cmd review --task '<任务ID>' --reviewer reviewer-a
.\kb.cmd review --task '<任务ID>' --reviewer reviewer-a --accept '<研究digest>' --notes '实际核对意见'
```

`run` 使用本机已有的原生 Claude CLI，每项任务一个独立会话。先做模块盘点、分批提交机制提案；盘点通过后，`advance` 生成下一批任务。也可用 `learn --candidate` 或 `learn --module ... --question ...` 获得手动 Claude 命令和提示词。

有知识正文的任务还需第二次知识审阅：上一条命令返回新的提案 digest 后，核对提案和源码，再执行同一 `review --accept <提案digest>`。纯盘点任务只经过研究审阅。程序不会替审阅人自动批准。

```powershell
.\kb.cmd advance --max-tasks 8
.\kb.cmd run --worker learner-a --module '<完整模块名>' --steps 2 --budget 3
.\kb.cmd progress --module '<完整模块名>'
.\kb.cmd coverage --module '<完整模块名>'
.\kb.cmd wiki
.\kb.cmd ask --role test_generation --question '这个机制的边界、预期依据和未覆盖分支是什么？'
```

每位成员默认最多保留 4 项待审；活动租约、待审上限、依赖未通过会明确阻止继续。超时或模型失败会保留会话日志与任务状态，使用 MCP 租约工具或 `--home ... task` 命令恢复。模型与版本来自本机配置，完整过程只保留在本地 `home/sessions/`。

## 多服务器按模块协作

协调端：

```powershell
.\kb.cmd --home 'E:/knowledge/gaussdb' team assign --module '<完整模块名>' --worker learner-a --kit 'E:/exchange/opt-a.zip'
```

成员解压同一版本工程，接收材料包，在独立本地目录执行：

```powershell
.\kb.cmd --home 'E:/member/opt-a' team open --kit 'E:/exchange/opt-a.zip'
.\kb.cmd --home 'E:/member/opt-a' whole next --worker learner-a
.\kb.cmd --home 'E:/member/opt-a' whole run --worker learner-a --steps 1 --budget 3
.\kb.cmd --home 'E:/member/opt-a' team export --task '<已提交任务ID>' --out 'E:/exchange/result-01.gz'
```

协调端导入后，通过自己的路径配置执行 `review`，再回传反馈：

```powershell
.\kb.cmd --home 'E:/knowledge/gaussdb' team receive --input 'E:/exchange/result-01.gz'
# 完成研究／知识审阅；从 workspace/order 文件获得协调端工作单路径
.\kb.cmd --home 'E:/knowledge/gaussdb' team feedback --order 'E:/exchange/opt-a.order.json' --out 'E:/exchange/feedback-01.gz'
```

成员执行 `team sync --input feedback-01.gz`、`whole advance`、`whole run`，继续下一任务；同一工作单可以多次提交。签名包校验源码版本、成员和知识基线；重复导入幂等，退回可以重做，已审结果不能被另一个包覆盖。不要手工合并 SQLite 文件。

研究发现包内缺少材料时，协调端在 `team feedback` 添加 `--include-asset '<全仓计划里的冻结资产ID>'`，成员再次sync即可补充同版文本。此操作扩展可读材料，不宣称补齐了对应调用图。中断会话可用 `run --resume-task '<仍有效的本人成员任务ID>'` 续作；任务提交后程序会停止该会话，防止继续消耗预算。

## 覆盖验收

`coverage` 明确列出未覆盖文件、未处置线索、未闭合模块、公共机制／跨域任务、单方契约、未决问题和使用回读缺口。`partial` 允许大文件分段研究，只有实际阅读、研究审阅、知识入库后，引用区间才累积为完整文件覆盖；知识变化使相关覆盖失效。

每个模块还需开发、测试、review 三类实际检索用例：

```powershell
.\kb.cmd verify-uses --input 'E:/acceptance/use-cases.json'
.\kb.cmd coverage --module '<完整模块名>'
.\kb.cmd accept-coverage --module '<完整模块名>' --digest '<报告digest>' --reviewer owner-a --notes '实际验收意见'
```

用例格式见 [迁移手册](MIGRATE-GAUSSDB.md)。不指定 `--module` 是全仓验收。回读检查证明必要知识进入上下文，不能替代专家判断或数据库运行测试。完整发布需要全仓覆盖签署；试点 Wiki 可直接导出，部分范围发布需明确 `--allow-partial`。

## ECS 生成编译调用图

在产品原有 Linux 构建环境中，使用匹配版本的 `compile_commands.json`：

```bash
sh ecs.sh doctor
sh ecs.sh build --source /srv/GaussDB --compile-db /srv/build/compile_commands.json \
  --work /srv/kb-work --output /srv/export/build-01 --jobs 8
```

工程提供 GCC／Clang 分析器与并发调度，需匹配的产品编译器、插件开发头／libclang 及生成头。现有编译数据库可直接使用；没有时可用 `ecs.sh capture ... -- <实际构建命令>` 采集。将完整输出目录（图、run.json、blobs）交给协调端；Windows 不解析 TU。

## 配置适配与验证边界

`product_adapter` 控制目录、注册和候选规则；`learning_policy` 控制领域、模块预算及公共机制课程，内置 `postgres-family` 与 `generic`，也可用自己的 JSON。`module_prefixes` 可固定责任边界；新增模块跟随下一次 `start --refresh` 形成新版本计划，已有知识不会被删除或自动认定适用。

2.3 在公开 openGauss 与合成协议场景验证；公司专有 GaussDB 的目录、宏和构建条件需要首次实际接入核验。全仓计划不是全仓语义已经学完。历史探索方案见 `docs/plans/`，当前默认路径以本 README 与迁移手册为准。可选平台／HTTP／RAGFlow 组件不属于本条离线使用路径的依赖。
