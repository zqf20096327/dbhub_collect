# AI 解析新代（G2）读取契约

> 定稿：2026-11-08（工作清单 G6-1）· gen_id `g2-20261107` · manifest `state/gen_manifest.json`（status=ready）
> 读者：新页面 / 查询 / 任何消费 AI 解析结果的程序。**只看这一份 + `lib/interp_keys.py` 就能读，不靠猜缓存字符串。**
> 页面构建（dbhub_page）不在本契约范围；本仓只交付数据与读取方式。

## 1. 一句话总览

**fn →（`state/interp_state.json` 台账）→ sha →（`lib/interp_keys.py` 键规则）→ 四层分片目录 →（`lib/interp_read.py` 拼接）→ 一条记录。**

不做字段复制：每层只存自己的载荷，读时按 sha 拼接（`interp_layer_store.join`）。推荐直接用 `lib/interp_read.py` 的 `InterpReader`，不要各拼各的。

## 2. 存储布局与键规则

| 层 | 目录 | 键（层内文件里就是这个字符串） | 载荷字段（白名单，其余写入即丢） |
|---|---|---|---|
| judge 判定卷 | `state/interp/judge/shards/<xx>.json` | 裸 sha（12 位内容摘要） | `classification` `signals` `audit` |
| text 文本卷 | `state/interp/text/shards/<xx>.json` | 裸 sha | `identity` |
| domain_tags 词控 | `state/interp/domain_tags/shards/<xx>.json` | 裸 sha | `tags` `abstain` `gap` |
| desc 降级卷 | `state/interp/desc/shards/<xx>.json` | `desc::<sha1(fn+desc)[:12]>` | `classification`（轻）`identity`（轻） |

- 分片：256 桶，桶名 = `sha256(key)[:2]`；每层另有 `state.json`（fn→{sha,status} 断点台账）与 `runlog/`（gitignored）。
- **内容 sha 镜像**：README 相同的仓共用同一条 judge/text/domain_tags 条目（键是内容摘要）；fn→sha 归台账管。
- desc 键含 fn：同描述不同仓不共用（G3-1 去碰撞）；描述变 → 键变 → 自然重烧。
- 条目级元信息（四层通用）：`sha` `source`（readme/desc）`generated_at` `prompt_ver` `model`（仅词控/desc）`ver` `clean_ver` `confidence`（仅 desc，恒 low）。

## 3. 各层字段表（真实条目口径）

### judge（v4 判定卷，prompt_ver 4.0，模型 glm-5.3-flash）
```
classification:
  cat_primary   str    14 类之一：备份/监控/高可用/迁移/连接/代理/管理/平台/开发库/安全/审计/测试/质量/建模/设计/内核/引擎/应用/其他
  cat_tags      list?  0-3 个补充类（同 14 类；单一类别仓省略）
  persona       list   1-2 个：use=用库 / ops=管库 / build=造库
  eco           str    tool=生态工具 / app=用库的应用 / unclear
  eco_why       str?   仅 eco=unclear 时存在
  ai_kind       str    mcp/rag/text2sql/dba-agent/other（非 AI=other；缺省已归一）
  dbs           list?  程序适配结论（引擎判定，T4b/G5-1 物化；AI 不写 db——R6）
  dbs_src       dict?  {kind: "engine", ...} 程序结论出身
  dbs_empty_reason any? 程序判"不涉及"时的解释
signals:
  install       list   npm/pypi/docker/binary/source/helm 子集（可空数组）
  status        str?   experimental/deprecated/discontinued 或 null（活跃度不在此）
  license_note  str?   仅结构特殊许可证（双许可/open-core/BSL 类）
audit:
  confidence    str    high/mid/low
  evidence_lines list  支撑判定的 README 行号（清理文坐标）
  evidence_preview str 行号原文的程序切片（≤80 字）
```

### text（v4t 文本卷，prompt_ver 4.0）
```
identity:
  one_liner   str   1-96 字一句话
  review      str   30-360 字点评
  highlights  list  2-4 条亮点
  use_cases   list  2-4 条适用场景
  softened    list? 软放行时被程序中性化的禁词轨迹（罕见）
```

### domain_tags（vc1.0，词表 v0.11：15 域 75 词）
```
tags    list  [{slug: 受控词, line: 证据行号, ...}]；空数组=证据不足（配合 abstain）
abstain str?  insufficient=证据不足（唯一保留码）
gap     str?  词表缺口线索（供词表升级）
```

### desc（dc1.0，无 README 仓降级；仅 1,009 条，confidence 恒 low）
```
classification: cat_primary（14 类）· persona（可 null）· eco（可 unclear）· ai_kind
identity:       one_liner（1-96 字）
```

## 4. 读取优先级（InterpReader 已内置，勿自行实现）

| 语义 | 优先级 | 说明 |
|---|---|---|
| 分类 entry() | judge > desc | legacy/desc_legacy 已删（G7-2），查不到即无 |
| 身份 identity() | text > desc | 同上 |
| 词控标签 domain_tags() | domain_tags 层 | 拒收/未跑返回 None |
| 引擎归属 dbs() | judge.dbs（程序结论） | legacy fallback 已删（G7-2 用户裁定）：engine 型 3,542 条目物化 judge 层、1,763 仓可读；override 型旧 verdicts 清零 |
| AI 标记 ai_flag() | judge.ai_kind（> desc 层 ai_kind） | other=非 AI；legacy 已删 |
| 活跃度 activity() | pool pushed_at + enrich 提交数 | 程序合成，非 AI 字段 |

## 5. 怎么读（代码）

```python
import sys; sys.path.insert(0, "lib")
from interp_read import InterpReader
r = InterpReader()
rec = r.entry(fn)        # 分类来源条目（judge 优先）
one = r.identity(fn)     # 身份来源条目（text 优先）
tags = r.domain_tags(fn) # 词控标签
dbs = r.dbs(fn)          # {"dbs": [...], "src": "engine|fallback|None", "reason": ...}
```

- 批量读：`InterpReader` 内部已做索引缓存，逐 fn 调用即可；不要自己开 300MB 缓存文件。
- 键规则对拍：`import interp_keys`（judge_key/text_key/vocab_key/desc_key/parse_key）——写新消费者时用它，别拼字符串。
- 形态安全阀：`interp_keys.entry_shape()` 判载荷形态（v4/v3/text/vocab），`accepts()` 判该层是否可采信——取到键 ≠ 层里有货。

## 6. 空值与死信语义

- **无 README 且描述为空（912 仓）**：四层皆无数据，页面显示"暂无简介"；清单在 `state/dead_letter.json`（layer=desc, reason=empty_desc）。
- **拒收条目**：层台账 status=rejected（detail 有原因），条目不存在；死信表同镜像。
- **词控空标签**：tags=[] + abstain=insufficient 是合法值（全量 48.5%），不要当错误。
- **desc 层 confidence=low**：只有一行描述的保守判定，展示端可降权。

## 7. 出身与版本（manifest）

一切版本事实在 `state/gen_manifest.json`（status=ready，phase=G7-2，2026-11-08 删后重定稿）：
- 各层 prompt_ver / 键模板 / 词表指纹（sha256）/ 代码文件 sha256 / git_commit；
- `lineage`：条目级出身字段（source/prompt_ver/generated_at）+ runlog 模型证据；
- 模型统一 glm-5.3-flash（`g2_model_normalize --verify` PASS，left=0）；
- 计数口径：逻辑条目 **96,715**（judge 32,090 / text 32,018 / domain_tags 31,598 / desc 1,009；legacy 42,886 已随 G7-2 删除，storage_dup=0）。

## 8. 已知边界（消费端必读）

1. **旧单目录已删除（G7-2，2026-11-08）**：`state/interp_cache_shards` 下线，四层目录为唯一生产数据（G1-6b 起写入即在此）。恢复通道：`D:\dbhub_interp_backup_20261108`（目录副本 + `interp_cache_shards.tar.gz`）与 `pre-g2` 标签。
2. **旧 AI 的 db_verdicts 已清零**（用户裁定）：dbs 读数只剩程序结论（judge.dbs，engine 型 3,542 条目 / 1,763 仓在台账内可读）；override 型旧 verdicts（如 pingcap/tidb 曾有 `['TiDB']`）随删除清零，需要时从备份重放。
3. **台账只收在池**（G5-2）：33,701 仓；出池仓的解读数据随旧目录一并下线（例：facebook/rocksdb），回池需重烧。
4. **池外/台账外 fn 读 None**：读层原"旧缓存扩展索引"随删除消失——设计内行为，消费者按空值处理（见 §6）。
5. cat 枚举里的斜线是字面量（"连接/代理"是一个值），拼接展示时勿按斜线拆分。
