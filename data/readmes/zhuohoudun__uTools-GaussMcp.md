# uTools-GaussMcp

在 [uTools](https://u.tools/) 里连接 **华为 GaussDB**，像本地客户端一样写 SQL、看表结构；同时可作为 **MCP 工具**，给 Cursor 等 AI 助手调用。

> 复制 SQL → 呼出 uTools → Ctrl+Enter，在本机快速查高斯库；还能给 AI 当 MCP 连库工具。

驱动使用官方 [`gaussdb-node`](https://www.npmjs.com/package/gaussdb-node)。

## 核心优势

- **一键呼出，复制即查**：剪贴板里是 SQL（`SELECT` / `WITH` 等）时，呼出 uTools 即可匹配本插件，SQL 自动填入编辑器，少切换窗口、少一次粘贴
- **Ctrl+Enter 精准执行**：编辑器可写多条语句，只跑光标所在那一条（或选中片段），不必整段拆开、也不必反复删改
- **多 Tab + 本地脚本**：多个查询页并行编辑；可保存 / 打开 / 拖入 `.sql`，常用脚本随时复用
- **元数据随手看**：模式 → 表 / 视图 → 字段，表详情含列、索引、约束；一键预览 `LIMIT 100`，结构摸清再写 SQL
- **布局可拖、状态记得住**：查询区 / 结果区、左侧模式树 / 字段区可调大小；连接与偏好本机加密保存，下次打开接着用
- **给人也给 AI**：人用控制台查数/写数；同时提供 MCP 工具，Cursor 等智能体可连同一套 GaussDB
- **写库可回溯**：写操作二次确认，本机审计日志尽力快照并可生成回滚 SQL
- **安全默认**：只读查询护栏、无 WHERE 拒绝、默认禁 DDL；密码进 uTools 加密存储，不进安装包

## 能做什么

- **多连接管理**：默认连接、只读、search_path、主备多节点、SSL
- **SQL 控制台**
  - 多 Tab 编辑，支持保存 / 打开 / 拖入 `.sql`
  - `Ctrl+Enter` 执行光标所在语句（可选中片段只跑选中内容）
  - 写 SQL / 单元格改库（单表+主键）经确认后执行，并记入写库日志
  - 结果表头悬浮显示字段注释
  - SQL 关键词 Tab 补全
  - 查询区与结果区、元数据上下区可拖拽调节大小
- **元数据浏览**：模式 → 表 / 视图 → 字段；表详情（列 / 索引 / 约束）；一键预览
- **智能体（MCP）**：只读元数据工具 + `insert_rows` / `update_rows` / `delete_rows` / `execute`（须 `confirm:true`）+ 审计日志工具

> 回滚 SQL 仅供复制/人工执行，插件不会自动回滚。密码仅保存在本机 uTools 加密存储中。
## 快速开始

### 安装

1. 在 uTools 应用市场安装本插件  
   **或** 用开发者工具加载本仓库构建产物 `dist/plugin.json`（选文件，不要选整个仓库根目录）
2. 确保本机能访问目标 GaussDB（内网或已放行的公网）

### 配置连接

1. 呼出 uTools，搜索 **高斯连接配置**
2. 新建连接：主机、端口（云实例常见 `8000`）、数据库、用户、密码
3. 可选：默认连接、只读、search_path、仅主节点、SSL
4. 保存后点「测试连接」

### 执行 SQL

1. 搜索 **高斯控制台**
2. 选择连接，编写 SQL
3. 点「执行」或按 **Ctrl+Enter**
4. 左侧可浏览模式 / 表；点 ⌖ 定位搜索结果；「预览」生成 `SELECT * FROM "表名" LIMIT 100`

更完整的说明见 [用户手册](docs/user-manual.md)。

## 给开发者

```bash
npm install
npm test
npm run build
```

构建完成后，用 **uTools 开发者工具** 选择：

```text
dist/plugin.json
```

该目录下应同时有 `index.html`、`logo.png`、`preload.js` 以及运行依赖。

本仓库通过根目录 `.npmrc` 使用国内镜像安装依赖（仅影响本项目，不改动你的全局 npm 配置）。

### 版本与文档

| 文档 | 说明 |
|------|------|
| [用户手册](docs/user-manual.md) | 安装、连接、控制台、MCP、安全 |
| [v1.0.3 发布说明](docs/release-notes-v1.0.3.md) | 写库审计与 MCP 读写 |
| [设计说明](docs/superpowers/specs/2026-08-26-gauss-mcp-design.md) | 架构与规范 |
| [写库审计设计](docs/superpowers/specs/2026-09-04-write-audit-mcp-design.md) | v1.0.3 增强设计 |

## License

[MIT](LICENSE) © zhuohd
