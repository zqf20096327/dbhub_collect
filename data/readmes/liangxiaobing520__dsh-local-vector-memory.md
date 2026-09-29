# dsh-local-vector-memory

本地向量记忆插件 for DeepSeek Harness(DSH)。本地 embedding 向量化 + SQLite 单文件存储,对话自动召回注入;会话结束由 DeepSeek 云端 deepseek-v4-pro 自动提取。

*A local-first vector memory plugin for DeepSeek Harness: local embeddings, SQLite storage, automatic recall injection, and DeepSeek cloud v4-pro extraction at session flush.*

## 特性

- **写入三条路**:手动 `memory_add`;用户消息命中记忆线索(记住/以后/偏好/约定/不要…)时毫秒级自动捕获;DeepSeek 云端 deepseek-v4-pro 在会话结束时从整段对话提取记忆(`autoExtract`,默认开)
- **防矛盾记忆**:写入时检测与已有记忆的冲突/过时(相似度 ≥0.86 但未达完全重复),提示改用 `memory_update` 更新旧记忆而不是新增重复条目
- **回收站**:`memory_forget` 默认软删除,`memory_restore` 可恢复;`purge=true` 才永久删除
- **在线备份**:`memory_backup` 用 SQLite `VACUUM INTO` 生成一致性快照(安全于手工复制 WAL 库),默认保留 5 份
- **自动召回**:每次 agent 推理前检索 top-K 相关记忆注入上下文(`<local-memory>` 标签),会话内 LRU 去重
- **批量向量化**:提取/重建索引一次 HTTP 批量请求,失败自动逐条回退
- **关键词兜底**:embedding 服务不可用时退化为中英文关键词匹配,写入照常
- **本地存储**:向量库是单个 SQLite 文件(`node:sqlite`,Node ≥22.5);embedding 全本地,提取走 DeepSeek 云端

## 需求

- DSH(DeepSeek Harness),web profile
- Node.js ≥ 22.5(内置 `node:sqlite`)
- OpenAI 兼容的本地 embedding 服务(见下文,推荐 Qwen3-Embedding-0.6B + llama-server)
- DeepSeek 官方云端 API(`deepseek-v4-pro`)用于提取(可选;默认走线索自动捕获)
- ⚠️ **不要把 API key 写进任何会被提交的文件**。key 只放在本机,支持三种写法:
  ```yaml
  extractionApiKey: "${DEEPSEEK_API_KEY}"        # 1. 环境变量
  extractionApiKey: "dsh:DEEPSEEK_API_KEY"       # 2. DSH 凭据库(~/.dsh/.credentials.yaml)
  extractionApiKey: "local-no-auth"              # 3. 明文占位(仅限免认证的本地服务)
  ```
  仓库内的 `cordis.patch.yml` 只是 bundle 挂载声明,不含任何凭据;`profiles/<profile>/cordis.patch.yml` 用于覆盖配置,请勿在其中写明文 key(会留在磁盘上,也可能被 UI 回显)。

## 安装

```bash
dsh plugin --profile web add dsh-local-vector-memory
```

插件声明 `dsh.bundle.patch`,安装后 `dsh.profile.bundles` 自动追加,无需手改 package.json。重启 DSH Web 生效。

## 工具(12 个)

| 工具 | 作用 |
| --- | --- |
| `memory_add` | 写入一条长期记忆(用户说"记住…"时;自动去重 + 冲突检测) |
| `memory_search` | 向量检索(embedding 挂了自动关键词兜底;支持 tag 过滤) |
| `memory_list` | 浏览记忆,支持 tag/source 过滤;`includeDeleted=true` 看回收站 |
| `memory_update` | 按 id 更新文本/标签(自动重向量化),纠正过时/冲突记忆 |
| `memory_forget` | 按 id 删除,默认软删除(可恢复);`purge=true` 永久删除 |
| `memory_restore` | 恢复被软删除的记忆(回收站) |
| `memory_backup` | SQLite 在线备份到 `~/.dsh/backups/memory`,自动保留最近 5 份 |
| `memory_stats` | 库状态 + 软删除数 + 服务地址 |
| `memory_reindex` | 给未向量化条目补向量(批量) |
| `memory_extract` | 调用提取模型从一段文本提炼记忆入库(仅短文本,建议 ≤2000 字) |
| `memory_merge` | 合并重复/同主题记忆:保留一条,其余软删除并标记"已被取代" |
| `memory_health` | 健康报告:条数/软删/未向量化/置顶分布 + 重复对检测与合并建议 |

## 默认配置

全部默认值在 `lib/config.mjs`。覆盖方式:在 `~/.dsh/profiles/web/cordis.patch.yml` 写:

```yaml
- id: local-vector-memory
  config:
    autoRecall: true
    recallTopK: 6
    recallMinScore: 0.55
    autoExtract: false   # 可选实验项:若提取模型是长思考链模型,长文本会耗尽 max_tokens,谨慎开启
    autoCapture: true    # 用户消息命中"记住/以后/偏好/约定/不要"等线索时自动入库
    skipDuplicates: true # 相同/高度相似记忆跳过
    softDelete: true     # memory_forget 默认软删除(回收站)
    backupDir: ~/.dsh/backups/memory
    backupKeep: 5
    conflictScore: 0.86  # 相似度 >= 此值(未达完全重复)提示冲突、建议 memory_update
    recallDedupeLru: 16  # 会话内召回去重 LRU 上限
    embeddingEndpoint: auto      # auto = WSL 网关 + embeddingPort
    embeddingPort: 8081
    extractionEndpoint: auto     # auto = WSL 网关 + extractionPort
    extractionPort: 8080
```

注意 DSH patch 是整段替换,不是深合并;上例只写了要改的字段,其余回到默认值。

## 配套 embedding 服务(独立于插件)

模型下载(一次):

```bash
modelscope download --model Qwen/Qwen3-Embedding-0.6B-GGUF \
  Qwen3-Embedding-0.6B-Q8_0.gguf --local-dir /path/to/models
```

Windows 启动脚本(路径按你的实际安装位置替换):
```powershell
# <LLAMA_DIR> = llama.cpp 可执行文件目录;<MODEL_DIR> = GGUF 模型目录
Start-Process -FilePath '<LLAMA_DIR>\llama-server.exe' -ArgumentList @(
  '-m','<MODEL_DIR>\Qwen3-Embedding-0.6B-Q8_0.gguf',
  '--embeddings','--pooling','mean','-c','8192',
  '--host','0.0.0.0','--port','8081','-ngl','0'
) -WindowStyle Hidden -RedirectStandardOutput '<LLAMA_DIR>\embedding-server.log' -RedirectStandardError '<LLAMA_DIR>\embedding-server.err.log' -PassThru
```

验证:

```bash
# <GATEWAY> = embedding 服务所在主机地址(同机用 127.0.0.1;WSL 访问 Windows 宿主用默认网关)
curl http://<GATEWAY>:8081/v1/embeddings \
  -H 'Content-Type: application/json' \
  -d '{"model":"local-embedding","input":"测试"}'
```

## 数据流

```
用户消息 ──记忆线索命中?──▶ embedding(8081) ──▶ SQLite 向量库
memory_add ─────────────────────────────▶ embedding(8081) ──▶ SQLite 向量库
memory_extract ──▶ 本地 9B(8080,仅短文本) ──▶ 批量 embedding ──▶ SQLite 向量库
                                                       │
                 agent/pre-step 自动召回 ◀──────────────┘
```

## 故障排查

- `memory_stats` 显示未向量化很多:检查 8081 服务,然后 `memory_reindex`。
- 自动提取没发生:`autoExtract` 默认关闭。若 `extractionModel` 指向长思考链模型,长文本提取会耗尽 max_tokens(实测),故默认改为线索自动捕获;短文本可手动 `memory_extract`。
- DSH 日志过滤:`[dsh-local-vector-memory]`。
- WSL 重启后网关变化:插件自动探测默认网关;若 8081/8080 不通,先确认 Windows 侧服务在跑。

## License

MIT

## 落库前低价值过滤（v0.3.4+）

auto-extract / auto-capture 会把「瞬时状态、纯进度、一次性参数」当成长期记忆写入，
稀释检索质量。v0.3.4 起在**落库前**自动拦截（`lib/filter.mjs`）：

| 拦截类型 | 例子 | 原因码 |
|---|---|---|
| 一次性参数/规模快照 | 「训练参数为每个角色约291张图像、800步，耗时约23分钟」 | `effort-snapshot` |
| 运行状态快照 | 「4.10版本回放训练任务目前持续正常运行，客户端为Base75689」 | `state-snapshot` |
| 进度/计数快照 | 「剩余44个角色预计还需1-1.5小时完成采集」 | `state-snapshot` |
| 无信息碎片 | 「当前 GPU 处于空闲状态」 | `too-short` |

判据是**双条件**：像过程性内容 **且** 不含任何知识信号。命中任一即放行：
规则/约定/红线、因果与根因、结论与教训、决策与要求、机制与原理、
操作说明（`可使用/入口/步骤`）、环境约束、具体技术实体（路径/命令/标识符/参数）。

```yaml
- id: local-vector-memory
  config:
    filterLowValue: true   # 总开关（默认开）
    filterMinChars: 24     # 短碎片长度阈值
```

实测（2026-09-21，本机 2146 条活跃记忆）：
- 活跃库抽样 500 条 → **误伤 0 条**
- 用户点名的典型状态句（3 类）→ **100% 拦截**
- 单元测试 `node --test tests/filter.test.mjs` → 5/5 通过
