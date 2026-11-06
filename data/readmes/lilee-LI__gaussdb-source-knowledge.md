# GaussDB 源码知识工程 2.1

同一仓库提供 Linux 产图端和 Windows 学习端。ECS 用随包 libclang 并发解析真实编译单元，输出带源码位置的调用图。Windows 读取交付目录、完整源码、设计和手册，生成全仓计划。成员选择特性后才创建研究任务。经审阅的知识保存在学习 SQLite，可导出 Wiki，或按开发、测试、评审、运维角色查询。

## 先在 ECS 生成调用图

解压发布 ZIP 或克隆本仓库，进入含 `ecs.sh` 的目录。在能正常编译产品的 Linux 环境中执行。ECS 需要 Git、64 位 Python 3.9+（含 venv、ensurepip）以及产品本身的编译环境。x86_64 和 aarch64 的 libclang 及内置头文件已经随包提供。

~~~bash
sh ecs.sh doctor
sh ecs.sh build --source /srv/GaussDB --compile-db /srv/build/compile_commands.json \
  --work /srv/kb-work --output /srv/export/build-01 --jobs 4
~~~

初次可追加一个或多个 `--tu 仓内相对路径.cpp` 先验证一个模块。省略 `--tu` 会处理编译库中的所有可用命令。如果使用项目自带 GCC，请加载与构建一致的环境，通过 `--cc` 和 `--cxx` 指定该工具链。分析进度写到终端，逐 TU 结果在工作目录的 `last-build.json`。

**还没有编译数据库时**，Make 项目可以用仓内采集器包住一次真实的重新编译，将下面的 `make -B -j4` 替换为项目的构建命令。CMake 项目也可以在原配置中开启 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`。

~~~bash
sh ecs.sh capture --source /srv/GaussDB --output /srv/export/compile_commands.json -- make -B -j4
~~~

把产图命令输出的**整个** `build-01/` 复制到 Windows，例如 `E:/ecs-export/build-01/`。其中 `knowledge.sqlite3` 是调用图，`run.json` 记录 run、编译覆盖和校验值，`blobs/` 保存回放所需的生成头或其他未跟踪材料。已有符合旧版合同的 ECS 索引可以直接接入。

## 在 Windows 第一次使用

准备 64 位 Python 3.12、Git 和已有的 Claude Code。解压内网包或克隆本仓库，在含 `kb.cmd` 的目录运行。首次调用从随包 wheel 离线安装依赖。

~~~powershell
New-Item -ItemType Directory -Force local | Out-Null
Copy-Item paths.example.json local/paths.json
notepad local/paths.json
~~~

填写 `source`（与上游匹配的完整源码）、`design`、`manual`、`index_db`（ECS 单文件一致性备份）、`home`（独立可写目录）。相对路径以 JSON 所在目录为准。缺少的文档可省略；CHM 先导出 HTML。一个可用 run 自动选择，有多个时从 `check` 的输出选择 `run_id`。没有 ECS 交付件时可省略 `index_db`，使用文本证据。Windows 使用配置的路径，无需提供 `compile_commands.json`。Linux 对应命令为 `sh kb.sh`。

~~~powershell
.\kb.cmd check
.\kb.cmd start
.\kb.cmd modules
.\kb.cmd features --limit 15
.\kb.cmd learn --candidate <上一步返回的候选ID>
~~~

打开 `start` 返回的 `plan`。每个模块分别列出文件数、ECS 清单内文件、编译记录和逐 TU 状态。`features` 可用 `--module`、`--state`、`--offset` 筛选或翻页。候选显示主责、相关模块、证据文件和行号、设计缺口、问题及任务状态。协调人可以在派单前用 `kb.cmd route --candidate <ID> --module <模块>` 确认或更正归属。临时问题仍可直接用 `learn --module <模块> --question "…" --symbol <符号>`。

执行 `learn` 返回的 `claude_command`，发送其 `prompt`。Claude 领取工作单、核对实际证据，提交研究。函数指针、宏分支或图外消费者需要单独取证。手册所写、源码所证、实际运行结果分别标注。

## 审阅和使用

~~~powershell
.\kb.cmd review --task <任务ID> --reviewer <审阅人>
.\kb.cmd review --task <任务ID> --reviewer <审阅人> --accept <研究digest> --notes "实际核对意见"
.\kb.cmd review --task <任务ID> --reviewer <审阅人> --accept <提案digest> --notes "实际核对意见"
.\kb.cmd wiki
.\kb.cmd ask --role test_generation --symbol <函数> --question "边界条件和预期依据是什么？"
~~~

研究证据和知识提案分别审阅。`wiki` 返回可整体分发的阅读目录，`ask` 从同一已审修订取结论、契约、测试预期和证据。可选角色为 `coding`、`test_generation`、`review`、`operations`。

## 不同服务器分别学习

协调端持有完整图，成员持有模块材料、一跳关系和候选条目的引用材料。每台机器的工作区独立。以下路径仅为示例。

~~~powershell
.\kb.cmd --home E:/kb/hub team assign --module <完整模块名> --worker opt-a --kit E:/share/optimizer.zip
.\kb.cmd --home E:/kb/member-a team open --kit E:/share/optimizer.zip
claude --mcp-config E:/kb/member-a/worker.mcp.json
~~~

在成员 Claude 中用 `feature_candidates` 查看本模块候选，用 `focus_module(candidate_id=…)` 生成一项任务，再领取、取证和提交。成员将一单结果回传，协调端收件后按同样的两步审阅。

~~~powershell
.\kb.cmd --home E:/kb/member-a team export --task <任务ID> --out E:/share/optimizer.result.gz
.\kb.cmd --home E:/kb/hub team receive --input E:/share/optimizer.result.gz
~~~

同一工作单支持重复投递同一结果。下一批使用新的工作单。请在完成现有审阅后替换分派。补包、旧队列迁移和归档见[操作手册](INTERNAL.md)。

## 实现、验收与打包

[完整技术设计](docs/DESIGN.md) · [验证范围与结果](docs/VALIDATION.md) · [ECS 交付与调用图查询](CALLGRAPH-REPLAY.md)

已实测公开 openGauss 的全部 2,412 个编译上下文：最终交付图 4.914 GiB，Windows `start` 用时 50.173 秒，生成 157 张模块盘点单和 3,370 条候选线索。818 个 TU 干净解析、1,594 个部分解析；当前仍有 GCC/Clang 兼容问题和产图写放大，详见[全仓实测报告](docs/benchmarks/opengauss-2412.md)。

~~~powershell
.\kb.cmd --help
.\.venv\Scripts\python -m unittest discover -s tests
.\.venv\Scripts\python scripts/verify_ecs_workflow.py --output E:/temp/new-kb-acceptance
python scripts/package_release.py
~~~

打包命令从当前 Git 暂存区生成 `dist/gaussdb-source-knowledge-2.1.1.zip` 和 SHA-256 清单。发布物包含两端代码、测试、研究方法和离线依赖。产品源码、构建依赖和用户已有的 Claude 使用各自环境。要从一次真实 Make 编译自测到协调端回放，可在同时具备 Python 3.12 和 Make/C++ 的 Linux 上运行 `python3.12 scripts/verify_ecs_producer.py --output /tmp/new-kb-acceptance`，输出目录须为新路径。
