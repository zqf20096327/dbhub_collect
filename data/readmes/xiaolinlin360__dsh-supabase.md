# dsh-supabase
![image](img/image.png)
让 DeepSeek Harness 里的 Agent 直接操作你的 Supabase 项目 —— 数据库增删改查、建表/外键/RLS 策略、Storage 桶与文件上传、RPC，全部通过自然语言完成。

> Give your DSH agent full Supabase superpowers: CRUD, DDL/policies via SQL, Storage buckets and binary uploads, and RPC — no middleware required.

[English summary](#english) · [安装](#安装) · [快速开始](#快速开始) · [工具](#工具) · [密钥对照](#密钥对照) · [架构与安全](#架构与安全) · [路线图](#路线图)

<!-- 顶部 GIF 演示占位：
![demo](docs/demo.gif) -->

## 特性

- 🔌 **10 个模型工具**：配置、连通性测试、任意 SQL、RPC、CRUD、Storage 建桶/上传
- 🖼️ **头像级文件流程**：本地文件 → 二进制直传 Storage 桶 → 公开 URL → 写回数据表，全自动
- 🗄️ **SQL 全能力**：建表、外键、索引、RLS 策略、Storage 桶策略（Management API，需 PAT）
- 🔐 **密钥安全**：API Key 通过环境变量传给子进程，**不进命令行、不进日志、不回显**；写入凭据服务后仅存于 Host 侧，跨插件重启仍可读取
- 🛡️ **防误操作**：update / delete 强制要求非空过滤条件
- 🌍 **跨平台**：优先 Node 24 自带 fetch（OpenSSL TLS），curl 降级为后备方案；自动探测 pwsh / bash 执行器
- 📦 **纯 JS、零依赖**：一个 `apply(ctx)` 函数就是整个插件，不需要构建工具

## 安装

在 DSH 会话中使用 Cordis 动态插件工具安装：

1. 调用 `cordis_define`：
   - `plugin.kind = "new"`，`idPrefix` 随意（如 `supab`）
   - `code.host` 填 [`src/host.js`](src/host.js) 的完整内容（`return { ... }` 函数体）
2. 用返回的 `pluginId` / `packageId` 调用 `cordis_run`（mode = `run`）
3. 用 `cordis_inspect_self` 查看运行状态；升级用 `cordis_define`(existing) + `cordis_run`(update)

> 注意：DSH 动态插件是会话级、进程内的，进程重启后需重新安装（凭据服务中的配置不受影响）。持久化打包（agent preset）见[路线图](#路线图)。

## 快速开始

1. 在 Supabase Dashboard 拿齐配置（对应关系见[密钥对照](#密钥对照)）：
   - **Project URL + publishable key**：Settings → API Keys
   - **secret key**：Settings → API Keys（写操作 / Storage 必需）
   - **PAT 个人访问令牌**：Account → Access Tokens（`supabase_sql` 必需，勾选"数据库 读写"即可）
2. 对话中说：`用 supabase_configure 配置 https://xxx.supabase.co`（或让 Agent 帮你调用）。
3. 然后你可以这样使唤 Agent：
   - 「查一下 todos 表里所有未完成的任务」
   - 「建一张 products 表，id 自增，category_id 外键关联 categories」
   - 「把这张图片上传到 avatars 桶，然后把 URL 写进 user 表的 avatar 字段」——把图片文件放进工作区即可，Agent 全自动完成

## 工具

| 工具 | 说明 | 关键参数 |
|---|---|---|
| `supabase_configure` | 配置项目（含 managementToken，写入凭据服务） | `projectUrl`、`anonKey?`、`serviceKey?`、`managementToken?` |
| `supabase_test` | 连通性验证（401/403 仅说明根 OpenAPI 需要 secret key） | — |
| `supabase_sql` | 任意 SQL：建表/外键/索引/策略/迁移（Management API，需 PAT） | `query` |
| `supabase_rpc` | 调用 Postgres 函数（PostgREST /rpc） | `fn`、`args?` |
| `supabase_select` | 查询（PostgREST GET） | `table`、`select?`、`limit?`、`order?`、`filters?` |
| `supabase_insert` | 插入一行或多行 | `table`、`rows` |
| `supabase_update` | 按条件更新（**filters 必填**） | `table`、`values`、`filters` |
| `supabase_delete` | 按条件删除（**filters 必填**） | `table`、`filters` |
| `supabase_storage_create_bucket` | 建 Storage 桶（可公开） | `name`、`isPublic?` |
| `supabase_storage_upload` | 本地文件二进制直传，返回公开 URL | `bucket`、`filePath`、`objectPath?`、`contentType?` |

过滤条件采用 PostgREST 语法：`{"done": "eq.false", "score": "gt.10"}` → `?done=eq.false&score=gt.10`。

## 密钥对照

| 插件参数 | 值 | 用途 |
|---|---|---|
| `projectUrl` | `https://<ref>.supabase.co` | 项目地址 |
| `anonKey` | publishable key（`sb_publishable_...`）或旧版 anon key | 读操作，受行级安全（RLS）约束 |
| `serviceKey` | secret key（`sb_secret_...`）或旧版 service_role key | 写操作、Storage 建桶/上传，服务端全权限，**请勿泄露** |
| `managementToken` | PAT（`sbp_...`，Account → Access Tokens，勾选"数据库 读写"） | `supabase_sql` 的 Management API 调用 |

## 架构与安全

```
模型工具调用
        │
        ▼
   Host 插件（本仓库）
        │  ① 配置：内存 > 凭据服务(环境变量)，跨重启持久
        │  ② 传输：Node 24 fetch(OpenSSL TLS) 为主，curl 后备
        │  ③ 通道：PostgREST / Management API / Storage API
        ▼
  ctx.shell 子进程（node -e）
        │  密钥/URL/请求体 → 环境变量；上传文件 → 子进程直接读盘
        │  响应附加 XHTTPSTATUS 标记 → 真实 HTTP 状态码
        ▼
   Supabase：rest/v1 · api.supabase.com · storage/v1
```

- 读操作优先 `anonKey`（受 RLS 约束）；写操作优先 `serviceKey`；`supabase_sql` 使用 `managementToken`。
- 二进制文件由 Node 子进程直接读取后作为请求体，**不经过对话文本**。
- 工具结果必须是纯无损 JSON：可选字段条件化构造，绝不带 `undefined`。

详细设计与踩坑记录见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 路线图

- [ ] Client 端数据表格卡片与上传进度 UI（React）
- [ ] 多项目配置切换（profiles）
- [ ] Storage 文件下载/删除/列表工具
- [ ] 打包为 agent preset / 官方收录渠道的持久化安装
- [ ] schema 自省：Agent 自动发现表结构与 RLS 策略（PAT/secret key 读 OpenAPI）
- [ ] 请求体走临时文件而非环境变量，解除 16 KiB 上限
- [ ] Auth 用户管理与认证流程工具

## English

`dsh-supabase` gives your DeepSeek Harness agent ten tools: `supabase_configure` / `supabase_test`, arbitrary SQL via the Management API (`supabase_sql`), PostgREST CRUD (`select` / `insert` / `update` / `delete`), `supabase_rpc`, and Storage operations (`supabase_storage_create_bucket`, `supabase_storage_upload`) with binary file upload and public URLs. Keys travel via environment variables — never on argv, never in results. Transport prefers Node 24's built-in fetch (OpenSSL TLS) with curl fallback. Pure JavaScript, no build step.

## License

[MIT](LICENSE) © 2026
