# TMP · TiDB 管理平台

[![CI](https://github.com/Win-Man/tmp-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Win-Man/tmp-platform/actions/workflows/ci.yml)

面向 DBA 的轻量级 TiDB 集群管理平台：接管 TiUP 部署的集群，三通道采集集群信息，提供拓扑/实例/用户/参数/会话视图、异步任务引擎、内置 28 项巡检与可下载报告。

- **单二进制交付**：Go + Gin + GORM + SQLite（纯 Go 驱动，无 CGO），前端构建产物 `//go:embed` 内嵌。
- **开箱即用**：首次启动自动建 19 张表、灌入内置巡检模板与默认配置，并创建管理员 `admin / admin123`（首次登录强制改密）。
- **演示模式**：`TMP_MOCK=true` 时使用内置 3 套假集群数据，无需真实集群即可走通全流程。

## 快速开始

```bash
# 1. 构建（前端 npm install + vite build，后端 go build）
make build

# 2. 以演示模式启动（默认 :8080）
TMP_MOCK=true ./bin/tmp

# 3. 浏览器访问 http://localhost:8080 ，使用 admin / admin123 登录
```

真实环境接管集群时，去掉 `TMP_MOCK=true` 直接运行 `./bin/tmp`：

```bash
./bin/tmp                       # 真实采集模式
TMP_ADDR=:9000 ./bin/tmp        # 自定义端口
```

## 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `TMP_ADDR` | `:8080` | HTTP 监听地址 |
| `TMP_DATA_DIR` | `./data` | 运行数据目录（存放 `secret.key`） |
| `TMP_DB` | `./tmp.db` | SQLite 元数据库路径 |
| `TMP_SECRET` | 空 | 主密钥；为空时自动生成 `data/secret.key`（0600） |
| `TMP_MOCK` | `false` | 强制演示模式（界面不可切换） |
| `TMP_GIN_MODE` | `release` | `debug` 可输出调试日志 |
| `TMP_LOG_LEVEL` | `info` | `debug` / `info` / `warn` / `error` |

> ⚠️ 请备份 `data/secret.key`：丢失后已加密的集群凭据无法解密，需要重新录入。

## 常用命令

```bash
make build            # 前端类型检查 + 构建 + 后端单二进制 -> bin/tmp
make typecheck        # 仅前端类型检查（vue-tsc --noEmit）
make backend-build    # 仅后端（需先构建前端）
make frontend-build   # 仅前端 -> backend/web/dist
make run              # 构建并以演示模式启动
make dev-backend      # go run（debug 模式，真实采集）
make dev-frontend     # vite dev server :5173，/api 代理到 :8080
make smoke            # 自动冒烟：启动→登录→总览→集群→拓扑→巡检→报告→任务→关停
make test / fmt / vet / clean
```

## 开发与协作

```bash
git clone git@github.com:Win-Man/tmp-platform.git && cd tmp-platform
make build      # 首次会自动 npm install（较慢），之后增量构建
```

- **环境要求**：Go ≥ 1.22、Node ≥ 20（`CGO_ENABLED=0`，无需 C 工具链）。
- **`backend/web/dist/` 不入库**（前端构建产物，见 `.gitignore`）。所以单独执行 `cd backend && go build ./...` 前需先 `make frontend-build`，否则 `//go:embed all:dist` 找不到文件；直接 `make build` 会自动按 typecheck → 前端 → 后端 顺序执行。
- **提交前自检**：`make typecheck && make test && make vet`（`make smoke` 会真实起服务跑端到端断言，耗时约 30s）。
- **分支约定**：`main` 保持可构建；功能开发走 `feat/xxx`、修复走 `fix/xxx`，PR 合入前跑一遍 `make smoke`。
- **CI（GitHub Actions）**：push / PR 触发 [`ci.yml`](.github/workflows/ci.yml) 三个 job —— 后端（gofmt / vet / 单测 / `-race`）、前端（typecheck / build）、集成（`make build` + `scripts/smoke.sh` 端到端断言），集成 job 会上传 `tmp-binary-<sha>` 二进制产物（保留 7 天）。
- **协作注意**：`tmp.db`、`data/secret.key`、`*.log` 均被忽略，不要提交；本地凭据与密钥不要写进代码或文档。

## 架构与目录

```
tmp-platform/
├─ Makefile / scripts/smoke.sh
├─ backend/
│  ├─ cmd/tmp/main.go          # 唯一入口：装配 → 迁移 → 恢复任务 → 起 HTTP → 优雅退出
│  ├─ web/embed.go             # //go:embed dist（内嵌前端）
│  └─ internal/
│     ├─ api/                  # router / response / middleware / *_handler
│     ├─ service/              # 领域服务：业务规则、事务边界、审计
│     ├─ repo/                 # GORM 数据访问（含 SQLite 写锁串行化 Tx）
│     ├─ collector/            # SSH / MySQL / PD 三通道 + mock + 归一化 + 能力矩阵
│     ├─ job/                  # 异步任务引擎（队列 200、4 worker、步骤+日志、启动恢复）
│     ├─ inspect/              # 巡检模板（yaml embed）、checker 注册表、MD/HTML 渲染
│     ├─ auth/ crypto/ db/ model/ config/ pkg/
├─ frontend/                   # Vue3 + TS + Element Plus + Pinia + ECharts
└─ docs/                       # PRD / ARCHITECTURE（设计输入）
```

关键设计：

1. **集群唯一性**：`clusters.name` + `name_lower` 双列联合唯一（大小写不敏感），移除纳管时把 `name_lower` 改写为 `name#removed#id` 释放唯一键，同名可重新接管。
2. **健康状态单一来源**：只由 `Snapshot.ChanErrors` + `collect_fail_streak` 推导；PD 通道单独失败不降级（对应字段显示 `—`）；快照落库在同一事务内全量替换，避免新旧数据混杂。
3. **任务恢复**：进程启动时 `running → interrupted`、`pending` 重新入队、`clusters.collecting` 全部归零。
4. **凭据安全**：AES-256-GCM 加密存储，接口只返回掩码；审计 detail 自动脱敏；JWT 吊销依赖 `platform_users.token_version`，改密/禁用后旧 token 立即失效。

## 角色权限

| 角色 | 能力 |
| --- | --- |
| `admin` | 全部功能（用户管理、凭据管理、采集配置、演示模式切换、审计日志） |
| `operator` | 只读 + 变更类（接管/采集/TiDB 用户/权限/Kill 会话/参数修改/巡检/任务重试取消） |
| `viewer` | 只读（写操作返回 40301） |

## 统一错误码

| code | HTTP | 含义 |
| --- | --- | --- |
| 40001 | 400 | 参数错误 |
| 40101 | 401 | 未认证 / token 失效 |
| 40301 | 403 | 无权限 / 不在白名单 |
| 40302 | 403 | 初始密码未修改（`must_change_password=1`，仅放行 `/auth/me`、`/auth/password`、`/auth/logout`） |
| 40401 | 404 | 资源不存在 |
| 40901 | 409 | 冲突（唯一键、能力不支持、状态不允许） |
| 42901 | 429 | 登录失败锁定 |
| 50001 | 500 | 服务内部错误 |
| 50201 | 502 | 采集 / 连通性失败 |

## 已知边界（MVP 范围）

- 监控趋势（`/clusters/:id/metrics`）与慢查询（`/slow-queries`）、告警（`/alerts`）当前返回空态或 40901，界面展示「未接入监控」。
- 定时巡检调度为接口占位（P2），立即巡检与报告全流程可用。
- 巡检模板只读（内置 6 类 28 项）；自定义模板编辑不在 MVP 范围。
