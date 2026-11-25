# tidbshard

TiDB 拆批 / 跑批引擎，Go 库形态。

> module path 为 `github.com/PanfengChen/tidbshard`。

## 当前状态

**M0 骨架 + M1 解析器已完成**：

```
$ go vet ./...     # 通过
$ go test ./...    # 14 个测试全部通过
ok  github.com/PanfengChen/tidbshard  0.002s
```

### 已实现（API 契约层）

| 类型 | 说明 |
|---|---|
| `Spec` | 纯数据作业规格，可序列化、可存库、可由上层调度生成 |
| `BatchSplit` / `BatchRun` | 拆批与跑批步骤 |
| `SQL` / `If` / `For` / `Try` | 控制流步骤 |
| `Engine` / `Config` | 无全局状态，可并发多实例 |
| `Secret` / `SecretFromEnv` | 凭据不落源码 |
| `Diagnostic` | 带行号列号的校验问题 |
| `Event` / `Summary` | 进度回调与结果聚合 |
| `lexer` / `parser` | `.tsk` 脚本 → `Spec`，错误带行号列号 |

### 待实现（M2~M4）

`Check` / `Run` 目前返回 `ErrNotImplemented`，签名和 godoc 已定稿。
`ParseFile` / `Parse` 已可用。

## 设计上的几条硬约束

这些不是风格偏好，是「能不能当库用」的门槛：

1. **不直接写 stdout** —— 日志走 `*slog.Logger`
2. **不调用 `os.Exit`** —— 返回 `error`，退出码是调用方的事
3. **无包级可变状态** —— 每个 `Engine` 独立
4. **`context.Context` 贯穿** —— 可优雅取消；取消时不派发新分片，在跑的分片保留可续跑状态
5. **不共享调用方的切片** —— `New` 会复制 `Config.Targets`（有测试覆盖）

## 测试

```
spec_test.go
  TestStepMarker                      所有 Step 类型满足接口
  TestNewValidatesConfig              New 拒绝不完整配置
  TestNewDoesNotMutateCallerConfig    New 不共享调用方切片
  TestSecretFromEnv                   环境变量读取，含缺失分支
  TestDiagnosticString                带/不带位置的诊断格式

parser_test.go
  TestLexBasics                       命令/地址/块/引号/注释/运算符
  TestLexReportsPositions             词法错误带 1-based 行列号
  TestLexUnterminated                 {{ / 引号 / 注释未闭合
  TestParseRealScript                 原版文档示例脚本 → 结构断言
  TestParseBatchRun                   .sql run batch 的 .with 与 .begin 体
  TestParseForSeq                     for seq 及步长方向校验
  TestParseIfAllSuccess               all success / not all success
  TestParseReportsUnknownCommand      未知命令给出诊断而非静默成功
  TestParseDiagnosticHasPosition      语法错误带位置
```

其中 `TestParseRealScript` 是核心回归：它解析原版工具文档里那个完整的
拆批跑批脚本，并逐项断言解析结果（实例、拆批列、group by、where、
procid、异常分支的退出码）。

## 目录规划

```
.                      # 包本体：Engine / Spec / Config
  engine/              # 拆批 / 调度 / 状态机（待建）
  store/               # 任务表接口 + TiDB 实现（待建）
  tidb/                # 连接 / 探测 / 拆批 SQL（待建）
  examples/cli/        # 演示 CLI（待建）
  testdata/*.tsk       # 回归脚本（待建）
```

按 v0.2 方案，CLI 放 `examples/`，不单独开仓库。
