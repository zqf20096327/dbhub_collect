# gaussdbdocs-mcp-server

> Local MCP server for **GaussDB documentation** semantic search + read-only metadata access.
> Apache-2.0 · Python 3.12 · Qdrant 1.12 · MCP 1.x

[English](#english) · [中文](#中文)

---

## English

### What is this?

A Model-Context-Protocol server that gives Claude Desktop / Cursor (and any other MCP client) **two** capabilities against a GaussDB instance:

1. **Hybrid semantic search over the GaussDB documentation corpus** — dense (BGE-large-zh-v1.5) + sparse (BM25) + Reciprocal Rank Fusion (k=60). Built for the database's high identifier density (GUC / WAL / XID / TOAST etc.).
2. **Read-only introspection of a live GaussDB instance** — metadata tools (`list_databases`, `list_schemas`, `list_tables`, etc.) and `EXPLAIN` for query plans. DML/DDL/DCL are rejected at the Python layer BEFORE any SQL leaves the process.

### One-command install

```bash
git clone https://github.com/songmenglin-dev/gaussdbdocs-mcp-server.git
cd gaussdbdocs-mcp-server
./setup.sh            # or: ./setup.sh v1   # pin a snapshot
docker compose ps     # confirm qdrant + mcp-server both healthy
```

`setup.sh` validates Docker availability, copies `.env.example` → `.env`, downloads the `index-v*.tar.gz` snapshot from GitHub Releases into the named `index_data` volume, and brings up the stack. Target: ≤ 10 minutes on a clean Linux box.

### Architecture

```
.chm → parse_chm → chunk → BGE + BM25 → Qdrant (named vectors: dense + sparse)
                                  ↓
                       export snapshot → GitHub Releases (BUILD)
                                  ↓
                  setup.sh downloads index-v*.tar.gz (RUN)
                                  ↓
                       import_snapshot → Qdrant storage
                                  ↓
              MCP server (stdio / SSE) — hybrid retrieval + DB tools
```

### MCP tools (11 total)

| Tool | Requires | Description |
|------|----------|-------------|
| `query_gaussdb_docs(query, top_k)` | — | Hybrid retrieval |
| `search_sql_reference(query, edition?, top_k)` | — | SQL syntax lookup (filtered to `doc_type=sql_reference`) |
| `search_admin_guide(query, edition?, top_k)` | — | Operational guidance lookup |
| `compare_gaussdb_editions(topic, top_k_per_side)` | — | Paired evidence across `distributed` / `centralized` |
| `list_databases` | `GAUSSDB_DSN` | Enumerate databases the role can see |
| `list_schemas(schema?)` | `GAUSSDB_DSN` | Schemas (default: all) |
| `list_tables(schema?)` | `GAUSSDB_DSN` | Tables (default: user schemas) |
| `list_indexes(table)` | `GAUSSDB_DSN` | Indexes on a table |
| `describe_table(table)` | `GAUSSDB_DSN` | Columns + types + nullability + defaults |
| `show_performance_views` | `GAUSSDB_DSN` | `pg_stat_*` performance views |
| `explain_query(sql)` | `GAUSSDB_DSN` | `EXPLAIN` only — `EXPLAIN ANALYZE` is rejected |

The DB tools are only registered when `GAUSSDB_DSN` is configured; without it, the docs surface (4 tools) is the entire tool list.

### Configuration

All config via env vars (see `.env.example`):

```env
QDRANT_HOST=qdrant               # service hostname
QDRANT_PORT=6333
QDRANT_GRPC_PORT=6334
INDEX_ARCHIVE=/data/index.tar.gz
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5
BM25_MODEL=Qdrant/bm25
RETRIEVAL_MODE=hybrid           # hybrid | dense | sparse
RRF_K=60
MCP_TRANSPORT=stdio             # stdio | sse
MCP_SSE_PORT=8080
GAUSSDB_DSN=postgresql://user:pass@host:5432/db  # optional
LOG_LEVEL=INFO
```

### Development

```bash
make test-unit     # fast unit tests
make test          # full suite (in-memory Qdrant)
make lint          # ruff
make build-index   # run the BUILD pipeline
make docker-build  # production image
```

### Project status

| Batch | What | Status |
|-------|------|--------|
| 1 | Scaffold + config + logging | ✅ |
| 2 | CHM parse + chunk | ✅ |
| 3 | Embedding + Qdrant index + snapshot export | ✅ |
| 4 | Snapshot import + hybrid RRF + `keyword_critical` regression + domain tools | ✅ |
| 5 | MCP server (stdio + SSE) | ✅ |
| 6 | GaussDB read-only connector + DB tools | ✅ |
| 7 | Docker / Compose / setup.sh / CI / Release | 🚧 |
| 8 | Eval harness | ⏳ |
| 9 | Coverage gate + community files | ⏳ |

### License

Apache-2.0 — see `LICENSE`.

---

## 中文

### 这是什么？

一个 **Model-Context-Protocol (MCP)** 服务器，给 Claude Desktop / Cursor（以及任何兼容 MCP 的客户端）提供两个能力对接 GaussDB：

1. **GaussDB 文档语料库的混合语义检索** — dense（BGE-large-zh-v1.5） + sparse（BM25） + Reciprocal Rank Fusion（k=60）。专为数据库文档的高专有名词密度（GUC / WAL / XID / TOAST 等）调优。
2. **活 GaussDB 实例的只读内省** — 元数据工具（`list_databases`、`list_schemas`、`list_tables` 等）和 `EXPLAIN` 看查询计划。DML/DDL/DCL 在 **Python 层 SQL 离开进程前** 就被拒绝。

### 一键安装

```bash
git clone https://github.com/songmenglin-dev/gaussdbdocs-mcp-server.git
cd gaussdbdocs-mcp-server
./setup.sh             # 或 ./setup.sh v1 钉特定版本
docker compose ps      # 确认 qdrant + mcp-server 都 healthy
```

`setup.sh` 校验 Docker 可用性、把 `.env.example` 拷成 `.env`、从 GitHub Releases 下载 `index-v*.tar.gz` 到命名卷 `index_data`、然后启动整套栈。目标：干净 Linux 机器 ≤ 10 分钟上线。

### 架构

```
.chm → parse_chm → chunk → BGE + BM25 → Qdrant（named vectors: dense + sparse）
                                  ↓
                  export snapshot → GitHub Releases（BUILD）
                                  ↓
            setup.sh 下载 index-v*.tar.gz（RUN）
                                  ↓
                 import_snapshot → Qdrant storage
                                  ↓
           MCP server（stdio / SSE）— 混合检索 + DB 工具
```

### 开发

```bash
make test-unit   # 快速单元测试
make test        # 全套（in-memory Qdrant）
make lint        # ruff
make build-index # 跑 BUILD pipeline
make docker-build
```

### 许可证

Apache-2.0 — 见 `LICENSE`。
