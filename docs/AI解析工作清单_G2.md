# AI 解析新代（G2）工作清单

> 建立：2026-11-07
> 目标：按最新 v4 判定卷 / v4t 文本卷 / vc1.0 词控三层 + desc 降级通道，生成一份可追溯的新语料；验收后删除旧解析。
> 用法：**一次只做一项**，做完打勾；上一项的验收不过，不进下一项。
> **验收纪律：每项必须先跑测试，测试通过才打勾**；通用闸门 `python interpret/selftest_ai.py`（8 套全绿）+ 该项专项测试，结果记入文末「测试记录」。

> **当前进度（2026-11-08 11:15）**：✅ 36 · ⏸ 0 · ☐ 0。**G2 全部完成。**
> Phase 0–7 全部收口：四层新代（judge/text/domain_tags/desc）为**唯一**生产数据；旧单目录已删（备份目录 + tar.gz + `pre-g2` 标签三层可回）。
> 剩余为另册后备（非本清单）：desc 0.9% 技术栈越界可选重跑 · domain_tags 398 拒收补跑 · T5a 绿门 3 晚 CI 验证。

## 固定决策

| 项 | 决定 |
|---|---|
| 方案 | A：保留最新 v4/v4t，只补 domain_tags 全量，不重烧两层 |
| 模型 | **全四层统一 `glm-5.3-flash`**（base `open.bigmodel.cn/api/coding/paas/v4`）：judge / text / domain_tags / desc 一律用它，**不使用其他模型**；历史 463 条 deepseek 由 G2-2 归一 |
| 空描述仓（1,057） | 新代不生成介绍，页面显示“暂无简介”；进 dead-letter |
| domain_tags 非空率 | **全量实测 51.51%**（head 67.50% / mid 59.99% / tail 49.20%，n=30,936）；500 条影子曾估 63/45/36。**验收一律按分层口径判**，不用字母序前 N 条 |
| 缓存 | 不物理复制 158MB；用 manifest 记代际，删旧后缓存自然变小 |
| 页面 | `dbhub_page/build/sources.py` **完全不动**，由用户重做；本清单只交付数据与读取契约 |
| 删除 | 最后一步；新页面能读新键或用户确认旧页面可停之前，旧数据保留 |
| 存储布局 | **四层各自独立目录**：`state/interp/{judge,text,domain_tags,desc}/`，各 256 分片 + 自己的 state.json + runlog；文件内键=裸 sha（层由目录表达）。存量 v4/v4t 在 v4t 跑完后一次性搬（pre-g2 tag 可回滚） |
| 分片解耦 | **每层只存自己的字段**（payload 白名单，跨层字段写入即丢并计数）；`fn` 不进条目（内容 sha 镜像时一条服务多仓，fn→sha 归台账）；不在条目里冗余别的层内容 |
| 程序拼接 | 读时 `join(sha, stores)` 按 sha 取四层拼成一条；**不做字段复制**，页面/查询只读拼接结果 |
| 断点机制 | 每层有自己的 `state.json`（fn→sha+status）与 runlog；`pending` 只返回缺失/内容变化的项；重启零重复。超时/429/额度 1113 等待共用同一 runner 骨架 |

## 改动边界（红线）

| 范围 | 文件 | 动作 |
|---|---|---|
| ✅ AI 解析 | `interpret/interpret.py`、`selftest_v4.py`、`vocab_control.py`、`selftest_vocab_control.py`、`run_domain_tags.py`、`vc_stats.py`、`selftest_runner.py`、`gen_manifest.py`、`dead_letter.py`、`g2_model_normalize.py`、`desc_control.py`、`run_desc.py`、影子脚本 | 可改 |
| ✅ AI 读层 | `lib/interp_read.py`（仅 AI 影子脚本引用） | 可改 |
| ✅ AI 新增 | `lib/interp_keys.py`、`lib/interp_layer_store.py`、`tools/check_layer_keys.py`、`tools/split_layers.py`、`tools/prog_field_migrate.py`、`tools/rebuild_interp_state.py`、`tools/dual_read_check.py`、`config/domain_vocab_v0.11.json`、`docs/AI解析读取契约_G2.md` | 可加 |
| ✅ AI 数据 | `state/interp/<layer>/`（四层，唯一生产数据；`state/interp_cache_shards` 已于 G7-2 删除）、`state/interp_state.json`、`state/logs`、`state/shadow` | 可动 |
| ❌ 采集 | `collect.yml`、`data/readmes`、`data/live/pool*` | 不碰 |
| ❌ 富集 | `enrich/*`、`state/enrich_cache_shards` | 不碰 |
| ❌ 证据 | `evidence/*`、`state/evidence_cache_shards` | 不碰 |
| ❌ 适配 | `attribution/*`、`tools/push_via_api_chunked.py`、`tools/t4a_bucket.py` | 不碰 |
| ❌ 共享库 | `lib/gh.py` | 不碰 |
| ❌ 清洗层 | `state/clean_delta_shards` | 不碰 |
| ❌ 页面 | `dbhub_page/**` | 不碰 |
| 🗑 不提交 | `.env.bak_20261104`、`pilot_v4_sample.json` | 不 stage |

## 序约束

1. **v4t 已于 00:18 真正跑完**：原跑 `1107_1144_v4t_p4.0` 最终 done 24,699 / rejected 22 / failed 29；复跑 112 条又补回 98。守夜脚本有 bug（grep `解读完成`，v4t 实际输出 `文本卷完成` → 无限重启），已停，不再抢额度。`interpret.py` 冻结解除。
2. 改 `interpret.py` 前确认没有 interpret 进程在跑（当前零进程，v4t/v4 均已收尾）；G1-6b 与 G2 数据已无冲突。
3. Phase 7 删除必须在 Phase 6 验收之后；页面重做完成前不删。
4. G1-5 闸门只差 desc：v4t 已补齐，**身份 100.00%**；分类 97.00% 的缺口全是 desc-only 仓（989 条），等 G3-3 补 desc 后再复跑。它是 Phase 5/6 的前置，不阻塞 Phase 3/4。
5. **写入切换顺序**：G1-6a 搬迁 → G1-6b 改写入 → G1-6c 改 CI；三步都完成前旧目录仍是活文件，不能删。
6. **验收采样必须分层**（head≥1000★ / mid 100–999★ / tail<100★ 各 100）。字母序前 N 条会集中在 `0*` 仓、几乎全落 tail，测出的非空率不可用于闸门。

---

## Phase 0 准备（不动数据）

| 状态 | ID | 事项 | 产出 | 验收 | 耗时 |
|---|---|---|---|---|---|
| ✅ | G0-1 | 分批提交源码：只提交 AI 解析文件 | 干净 AI 基线 | `git status` 里非 AI 改动原样未动 | 30 分 |
| ✅ | G0-2 | 写 `state/gen_manifest.json` | gen_id、三层版本、词表 v0.11、模型、键前缀、开始时间 | 脚本可读 | 20 分 |
| ✅ | G0-3 | 建 `state/dead_letter.json` | 四类：no_desc/rejected/failed/out_of_pool | 空表 + schema | 20 分 |

**G0-1 只 stage 这些**：`interpret/interpret.py`、`interpret/selftest_v4.py`、`interpret/vocab_control.py`、`interpret/selftest_vocab_control.py`、`interpret/_shadow_vocab.py`、`interpret/_run_domain_tags_shadow.py`、`interpret/_vocab_control_ab.py`、`interpret/_domain_tags_calib.py`、`interpret/_ab_app_lite.py`、`lib/interp_read.py`、`config/domain_vocab_v0.11-draft.json`。

## Phase 1 读层基础（可与 v4t 并行）

| 状态 | ID | 事项 | 产出 | 验收 | 耗时 |
|---|---|---|---|---|---|
| ✅ | G1-1 | 层键规则 + 只读体检 | `lib/interp_keys.py`、`tools/check_layer_keys.py` | 分类可读 ≥35,800；身份 ≥35,200；失效键 0 | 40 分 |
| ✅ | G1-2 | 读层多卷合并 | `interp_read.py` 的 judge/text/legacy 合并 | 100 仓三卷字段齐全率 100% | 3–4h |
| ✅ | G1-3 | `ai_flag`/`dbs()` 修正 | 先 `ai_kind` 后 `ai.kind`；dbs 只认程序源 | AI 检出 2,561（v4 ai_kind 口径）；dbs engine 30→1,749 | 1–2h |
| ✅ | G1-4 | 三卷自检 | 缺卷/双卷/desc 用例 | 新断言全绿（41/41） | 1h |
| ✅ | G1-5 | 阶段闸门 | `interp_read.py --gate` | **PASS（desc 层补齐后复跑）**：200 仓分类 **100.00%** · 身份 **100.00%** · 双可读 100.00%（各 ≥99%） | 30 分 |
| ✅ | G1-6a | 分层存储 + 搬迁工具 | `lib/interp_layer_store.py` + `tools/split_layers.py`；备份 `D:\dbhub_interp_backup_20261108\`（167MB/256 桶） | **已搬迁**：judge 32,090 / text 32,018 / domain_tags 保留 / desc 0；`--verify` **0 差异**；旧目录原样保留待 G7-2 删 | 3–4h |
| ✅ | G1-6b | 生产写入切到新布局 | `interpret.py`：v4/v4t 写入与查重改 `state/interp/{judge,text}`（裸 sha 键 + 层台账 mark/断点）；v4 模式停走旧 desc 降级通道（`desc_defer_g3` 计数，等 G3-3）；`AIClient` 缺省 glm-5.3-flash + bigmodel；`LayerStore` 补 `__contains__` | 沙箱 16/16：双卷 done 写入只落新目录、旧缓存 106,994 零新增、缺省值不落 deepseek | 2h |
| ✅ | G1-6c | CI 提交路径 | `interpret.yml` 的 `git add` 加 `state/interp`（runlog/轮转副本由 gitignore 挡住不入库） | yaml 校验过 · `git add --dry-run` 模拟只带层状态与分片；14:23 夜窗实测首推 | 30 分 |

### G1-6 分层存储细则

| 层 | 目录 | 键 | 载荷 | 台账 |
|---|---|---|---|---|
| judge | `state/interp/judge/` | 裸 sha | v4 判定（cat/persona/eco/ai_kind/signals/audit） | state.json：fn→{sha,status} |
| text | `state/interp/text/` | 裸 sha | identity 四件套 | 同上 |
| domain_tags | `state/interp/domain_tags/` | 裸 sha | tags[{slug,line,conf}]/abstain/gap | 同上 |
| desc | `state/interp/desc/` | `desc::<12位摘要>` | 轻判定+轻介绍，source=desc | 同上 |

- **解耦规则**：每层 payload 白名单（judge=classification/signals/audit；text=identity；domain_tags=tags/abstain/gap；desc=identity+轻 classification）；跨层字段写入即丢并计数；`fn` 不落条目；一个内容 sha 可服务多个镜像仓。
- **拼接规则**：`join(sha, stores)` 按 sha 取四层，不复制字段；读层（`interp_read`）只做这个拼接，消费方不各自拼装。
- **断点规则**：每层独立 `state.json`（fn→sha+status）与 runlog；`pending` 只返回缺失/变化项；重启零重复；每层可单独重跑、单独换提示词，互不作废。
- **共用机制**：256 分片（桶=sha256(key)[:2]）、脏桶增量落盘、超时重试、429 退避、额度 1113 等待、墙钟预算，全部走同一套 runner 骨架，四层不各写一份。
- 搬迁：v4t 收尾 → 打 `pre-g2` → `tools/split_layers.py` 一次性重排 → 复跑读层对拍（搬迁前后逐仓 0 差异）。
- **写入切换（G1-6b）**：搬完必须把 `interpret.py` 的 v4/v4t 写入改到新目录，否则夜间 CI 会继续往旧目录写，形成双写分叉；`run_domain_tags.py` 已直接写新目录。
- **CI 路径（G1-6c）**：`interpret.yml` 的 `git add` 目前只加旧目录与 `interp_state.json`，不加新目录则新数据不进仓。
- 旧单目录已于 G7-2 删除（2026-11-08）；读层 legacy/desc_legacy 优先级自然失效（查不到即返回 None）。

## Phase 2 补齐 v4/v4t（等 v4t 跑完）

| 状态 | ID | 事项 | 量 | 验收 | 调用 |
|---|---|---|---|---|---|
| ✅ | G2-1 | v4t 收尾 + 复跑拒收/失败 | 原跑 done 24,699 / 拒收 22 / 失败 29；复跑 112 → ok 98 / 拒收 10 / 失败 4 | 在池身份可读 99.93%（文本 32,017） | 112 |
| ✅ | G2-2 | 模型归一 | 453 键（v4 398 / v4t 55）备份后删除重烧 | left=0、current_missing=0；26 条因 README sha 变更自然作废 | 453 |
| ✅ | G2-3 | v4 补跑 rejected | 433 待办（398 deepseek + 35 rejected）→ ok 429 / 拒收 4 | 在池分类可读 99.94% | 433 |
| ✅ | G2-4 | 覆盖率报告 | `state/shadow/g2_coverage_20261108.json` | v4 **99.997%**（32,691/32,692 有 README 口径）· 身份 99.93% · desc-only 989 条等 G3 · gap 清单已落盘 | — |
| ✅ | G2-5 | 提交数据 + 打 `tag pre-g2` | 提交 `1aaf74d53` + 标签 `pre-g2` | tag 存在，可回滚 | — |

## Phase 3 desc 路径（989 条 desc-only + 20 条无 README）

| 状态 | ID | 事项 | 产出 | 验收 | 调用 |
|---|---|---|---|---|---|
| ✅ | G3-1 | desc 键去碰撞 | `desc::<sha1(fn+desc)[:12]>`（interp_keys.desc_key，G1-1 已备）；旧键退役（台账改指新键，旧条目 G7 删） | 全量 1,009 fn → **1,009 键零碰撞**（runner 内置断言 + 事后核验）；97 仓共用一条归零 | — |
| ✅ | G3-2 | desc prompt/schema/validator | `interpret/desc_control.py`：轻判定（cat_primary 必填/persona 可 null/eco unclear 免 why/ai_kind 归一）+ 轻介绍（one_liner）；`source=desc`、`confidence=low` 层常量 | selftest 15/15；不要求 evidence_lines；prompt ~1.4-1.9KB | — |
| ✅ | G3-3 | desc runner | `interpret/run_desc.py` 全量 1,009 条（12 分钟 c=4，2.8s/条，glm）；912 空描述进 dead-letter；台账双写（desc 层 state + interp_state 指新键） | ok 1,009 / 拒收 0（13 条超长按 v4t 先例放宽 80→96 后全捞回）/ 失败 0；每条 `source=desc` ✓ | 1,022 |
| ✅ | G3-4 | 抽检 + 闸门 | 30 条随机样例（seed 20261108，落盘 shadow）+ 全量 1,009 条程序化反编造筛查（ASCII 实体词对拍 desc+fn+topics） | 30 条**明显编造 0 条**（≤3 ✓）；全量疑点 32 条中真越界（技术栈描述没提）约 9 条 = 0.9%，记后备（可收紧提示词重跑 desc 层） | — |

## Phase 4 domain_tags 全量

| 状态 | ID | 事项 | 产出 | 验收 | 调用 |
|---|---|---|---|---|---|
| ✅ | G4-1 | 冻结 v0.11 | abstain 只留 `insufficient`；桌面文档补 4 词；config 定版 | config `domain_vocab_v0.11.json`（75 词/15 域，vocab_ver=0.11）；桌面文档待用户侧同步 | — |
| ✅ | G4-2 | vc 生产 runner | `interpret/run_domain_tags.py`：并发/断点/校验/重试/dead-letter/墙钟预算 | 断点重启零重复；3 条冒烟 ok=3、读层可见 | — |
| ✅ | G4-3a | runner 加 `--stratum` | head/mid/tail 各 100 抽样（seed=20261107） | 抽样可复现、三层各 100；单测通过 | 30 分 |
| ✅ | G4-3 | vc 试点 300 条（分层） | head/mid/tail 各 100 | **四闸全过**：拒收 2.00% ✓ · 词表外 0.00% ✓ · 证据 100% ✓ · 非空 61.51% ✓；分层 head 73.20% / mid 57.14% / tail 54.17% | 300 |
| ✅ | G4-4 | vc 全量（**并发 4**） | 00:34–07:51 跑完：ok 30,936（非空 15,934）/ 拒收 398 / 失败 7；累计库存 31,598；提交 `b1f40548a` | 31,341 条全部处理，3.3s/条 | 31,341 |
| ✅ | G4-5 | vc 验收 | 分层覆盖/OOV/证据率 | **四闸全过**：拒收 1.27% ✓ · OOV 0% ✓ · 证据 100% ✓ · 非空 51.51% ✓；分层 head 67.50% / mid 59.99% / tail 49.20% | — |

## Phase 5 迁移与重建

| 状态 | ID | 事项 | 量 | 验收 |
|---|---|---|---|---|
| ✅ | G5-1 | 程序字段迁移 | `tools/prog_field_migrate.py`：按读链（fn→当前 sha）把 engine 型三件套物化进 judge 条目；AI 旧 verdicts fallback 不迁（v1.5 裁定，G7 闸门再裁） | 迁移 **1,763** 条（另 1,781 条 judge 已带）；删旧前对账 legacy engine 1,929 条 **丢失 0**（166 条差异全是被后续裁决推翻的旧弱路径值，judge 层带更新结论） | — |
| ✅ | G5-2 | 重建 `interp_state` | `tools/rebuild_interp_state.py`（备份 shadow）；只收在池 + sha 对齐 readme_state | 35,926 → **33,701**（删出池 2,225 · 修 sha 漂移 1 · 15 条 failed 全在出池集自然清除）；对账 **0 差异**；键体检闸门阈值改在池口径（33,600/33,500）后 PASS | — |
| ✅ | G5-3 | manifest 定稿 + lineage | `gen_manifest.py --finalize`：status→ready + lineage（条目级 source/prompt_ver/generated_at + runlog 模型证据 + 深浅注记） | 抽 **100 条出身 100%**（missing 0）；`g2_model_normalize --verify` 复核 PASS（库存全 glm）；selftest PASS | — |

## Phase 6 契约与本地验收（不碰页面）

| 状态 | ID | 事项 | 产出 | 验收 |
|---|---|---|---|---|
| ✅ | G6-1 | 导出新代读取契约 | `docs/AI解析读取契约_G2.md`：布局/键规则/四层字段表（真实条目口径）/读取优先级/空值与死信语义/manifest 指针/已知边界 | 新消费者只看这一份 + `lib/interp_keys.py` 即可读，含代码示例 | — |
| ✅ | G6-2 | 本地双读 200 条 | `tools/dual_read_check.py`（在池抽样，字段名感知：legacy 条目 cat vs v4 cat_primary） | **PASS**：分类一致 149 / 复判变更 37（v4 重烧）/ 新读独有 14（desc 层）；一句话重写 180（v4t 复烧）；引擎一致 184 / 新结论 10（G5-1）/ 裁决清零 5；**异常 0** | — |
| ✅ | G6-3 | 本地验收报告 | `state/shadow/g6_acceptance_20261108.json` | **全部达标**：层内直读覆盖 分类 99.988% / 身份 99.982%（全口径 100%/99.99%）；text 四件套 99.8%；judge confidence 100%；domain_tags 非空 54.4%（抽样）；desc persona null 52.8%/eco unclear 40%（薄描述保守判定，设计内） | — |

## Phase 7 归档与删除

| 状态 | ID | 事项 | 产出 | 验收 |
|---|---|---|---|---|
| ✅ | G7-1 | 归档旧代 | 备份目录 `D:\dbhub_interp_backup_20261108\interp_cache_shards`（256/256 分片 sha256 与删除前一致）+ `interp_cache_shards.tar.gz`（45MB，回环 sha256 校验一致；zstd 无二进制改 gzip，python 3.14 zstd 回环丢 52KB 弃用）+ 逐片清单 `state/shadow/g7_archive_manifest.json` + `pre-g2` 标签 | 恢复演练：随机 100 键备份直读 **100/100 可用** |
| ✅ | G7-2 | 删除旧数据 | `git rm` 下线 `state/interp_cache_shards` 256 片 167MB（提交 `0ecd28b43`）：v3 裸 sha 40,913 + desc_legacy 1,973 唯一数据入备份；双存副本 64,108 与新层重复 | **闸门满足：用户 2026-11-08 确认「删除」**；删前体检仅旧代可读 分类 3/身份 4（删后变空，量级 0.01%）；legacy db_verdicts fallback 读数清零（约 2 万仓，用户裁定接受；程序引擎结论 3,542 条物化在 judge 层不受影响） |
| ✅ | G7-3 | 删后复验 | selftest_ai **8/8** · 键体检闸门 PASS（在池 33,701：分类 33,697=99.99%/身份 33,695=99.98%，仅旧代可读归 0，失效键 0）· 读链闸门 200/200 双 100% · manifest `--phase G7-2` 重定稿（96,715 条/storage_dup 0/legacy 0）· 引擎结论 1,763 仓活读 OK · dual_read 200 全「新读独有」= 旧读归零证据 | `state/interp` 117MB <120MB ✅ · 无缺失 |
| ✅ | G7-4 | 更新文档/记忆 | 本清单 Phase 7 收口 + 读取契约 §4/§7/§8 删后口径 + `gen_manifest.py`（`--phase` 参数）+ auto-memory 落档 | README/COLLECTION_MAP 无旧路径引用（各 0 处）✅ |

---

## 提示词评审记录（vc1.0 / domain_tags）

| 轮次 | 规模 | 结论 |
|---|---|---|
| 影子跑 | 500 条分层（head 148 / mid 199 / tail 147） | OOV 0；双跑一致 exact 76% / Jaccard 0.873；收 40 个缺口词建议；空标签 head 37% / mid 55% / tail 64% |
| 校准 | 共现 + 混淆对 | 沉淀 10 组近邻规则（orm≠query-builder、cdc≠data-sync…），按词表命中动态注入 |
| app-lite A/B | 一批 | **否决**：应用类短提示把 orm 误标 59 倍 |
| 四配置 A/B | 300 条 × G1/G2/G3/G4 | 选 G4（全词表+证据纪律）：空标签 50.2%、平均 0.92 标签、OOV 0、prompt 10,860B、6.3s |
| 自检 | 36 条 | 体积/确定性/校验器/键分层全绿 |

**评审缺口（必须写明）**：
- 没有人工标注的 domain_tags 金标集；A/B 只证明配置间一致（exact 67–75%），不证明标得对。
- 与旧 patch 提示词 exact 60.5%，同样只是一致率。
- 唯一正确性锚是「行号必须在证据包内」（实测 in_pack 100%），但「这个词是否真适用于这行」无人核过。
- 无第二专家独立评审。→ 已列入另册 P2-7 人工复核。

## 测试记录

| 项 | 测试命令 | 结果 |
|---|---|---|
| G0-1 | `python interpret/selftest_ai.py` | PASS 5/5（v4 判定/文本、vc1.0、读层、manifest、死信表）；`git show --stat` 三提交仅动 AI 文件 |
| G0-2 | `python interpret/gen_manifest.py --selftest` | PASS 14/14（三层键与代码函数对拍、计数自洽、词表指纹、dirty 标记） |
| G0-3 | `python interpret/dead_letter.py --selftest` | PASS 9/9（空表/分层/同键覆盖/计数聚合/非法输入） |
| G1-1 | `python tools/check_layer_keys.py --selftest` + 全量体检 | 单测 PASS 31/31；体检：分类 35,861≥35,800 · 身份 35,329≥35,200 · 失效键 0 · 形态不符 0 · 契约一致 → PASS |
| G1-2 | `python lib/interp_read.py --selftest` + `--audit` | 单测 PASS 27/27（三卷齐全/仅旧代/旧代+文本卷/desc/形态不符/台账权威/镜像共享/无层）；真实抽样 100 仓三卷字段齐全 bad=0，文本卷不遮蔽判定卷；audit：分类 35,861 / 身份 35,329 / judge 32,766 / text 25,853 |
| G1-3 | `python lib/interp_read.py --selftest` + `--audit` | 单测 PASS 32/32（新增 ai_kind other 不算 AI、判定卷程序 dbs 优先、显式空结论不被旧代覆盖）；audit：engine 30→1,749 · fallback 20,839 · ai_flag 2,561 · ai_flag_mismatch 0 |
| G1-4 | `python lib/interp_read.py --selftest` | PASS 41/41：缺判定卷/缺文本卷/双卷冲突/文本键装 v4/只有词控/desc 新旧并存/不串用 desc/legacy 装 v4/两次构建一致 |
| G4-1 | `python interpret/selftest_vocab_control.py` | PASS 36/36（abstain 单码；app/not-db 旧码拒收；prompt 11036B，G4 实测量级内） |
| G4-3 | `run_domain_tags.py --limit 100 --concurrency 1` + `vc_stats.py --gate` | 100 条：ok 100 · 拒收 0 · 失败 0 · 4.6s/条 · 均 glm-5.3-flash；拒收 0% ✓ / 词表外 0% ✓ / 证据 100% ✓ / 非空 41.75% ✗（**字母序样本，tail 偏置，不作闸门依据**）；触发命中 95.15%；tries>1 共 7 条（均重试成功）；断点复跑 3 条 → 库存 103→106，零重复 |
| G4-3 机制 | `python interpret/selftest_runner.py` | PASS 12/12：超时 2 次上限 · 1113 等待 600s×2 · 普通 429 退避 · 500 重试 · 校验纠正重试 · pending 断点语义 |
| G4-3a | `run_domain_tags.py --stratum 100 --dry-run` + 抽样复现对拍 | 300 条 = head 100 / mid 100 / tail 100；同种子两次逐条一致、换种子不同；prompt 均值 11.2KB |
| G4-3 分层 | `run_domain_tags.py --stratum 100 --concurrency 3 --max-minutes 90` + `vc_stats.py --since 2026-11-07T14:30 --gate` | 300 条：ok 291 · 拒收 6 · 失败 3 · 7.9s/条（与 v4t 抢额度）；拒收 2.00% ✓ · 词表外 0.00% ✓ · 证据 100% ✓ · 非空 61.51% ✓ → **PASS**；分层 head 73.20%(n=97) / mid 57.14%(n=98) / tail 54.17%(n=96)。6 条拒收全是「空标签未给合法 abstain 码」，可 `--retry-rejected` 补跑 |
| G4-4 | `run_domain_tags.py --concurrency 4 --max-minutes 600` | 00:34–07:51 跑完 31,341 条：ok 30,936（非空 15,934）· 拒收 398 · 失败 7 · 3.3s/条；累计库存 31,598 条 / state 32,021 仓；tries 1次×30,010 / 2次×2,000 / ≥3次×26 |
| G4-5 | `vc_stats.py --since 2026-11-07T16:33 --gate` | **PASS**：拒收 1.27% · 词表外 0.00% · 证据 100.00% · 非空 51.51%；分层 head 67.50%(n=1,194) / mid 59.99%(n=4,579) / tail 49.20%(n=25,163)。398 拒收中 397 条是同一原因（空标签未给 abstain 码），可补跑 |
| G4-2 | `python interpret/run_domain_tags.py --limit 3 --concurrency 2` | 3/3 ok、0 拒收、0 失败、均 11.9s/条；写入 `state/interp/domain_tags/`（3 分片、state 3 仓、runlog）；读层 `InterpReader.domain_tags()` 可读，含证据行（orm@L52） |
| G1-6 | `lib/interp_layer_store.py --selftest` + `tools/split_layers.py --dry-run` + 读层新布局用例 | 存储 19/19（解耦/分片/脏桶/断点/拼接/键规则/日志）；读层 44/44（含新布局三卷可读、旧目录同 sha 新布局优先、desc 层可读）；搬迁预演（08:00）：judge **32,090** / text **32,018** / 不搬 legacy 40,913 + desc_legacy 1,973。v4t 已收尾、`pre-g2` 已打，等 `--apply` |
| G1-5 | `python lib/interp_read.py --gate` | **FAIL（只差 desc）**：200 仓身份 **100.00%** ✓ · 分类 97.00%。缺卷全是 desc-only（desc_legacy 有身份、无 cat_primary），等 G3-3；代码侧无缺陷 |
| G2 | `g2_model_normalize.py --selftest/--apply/--verify` + v4/v4t 重跑 | 归一工具 4/4；453 键备份后删除重烧；`--verify` → **PASS**（left=0 · current_missing=0 · 过期 26）；v4t 复跑 112 → 98 ok；v4 复跑 433 → 429 ok；覆盖率 `state/shadow/g2_coverage_20261108.json`（v4 99.997% / 身份 99.93%） |
| 模型口径 | `python interpret/gen_manifest.py --selftest` + 重生成 manifest | PASS 14/14；`model.target=glm-5.3-flash`、`mixed.action` 指向 glm-5.3-flash；CI（interpret.yml / retro_audit.yml）与 `.env` 的 `AI_MODEL` 均已为 glm-5.3-flash |
| G1-6a | `split_layers.py --apply/--verify` + `check_layer_keys.py` + `interp_read.py --selftest` + `gen_manifest.py --selftest` | **搬迁完成 0 差异**：judge 32,090 / text 32,018 / domain_tags 保留（跳过） / desc 0；键形态体检 PASS（失效键 0 · 闸门 PASS 分类 35,863≥35,800 · 身份 35,848≥35,200）；读层 selftest PASS（真实 100 仓三卷齐全 bad=0，judge+text 候选 32,778）；manifest 修双存重复计数（逻辑口径 138,592 + storage_dup 64,108）后 selftest 14/14 PASS |
| G1-6b | `selftest_ai.py` 8 套 + 沙箱端到端 16 断言 + 真机冒烟 | 8/8 套绿；沙箱（层目录/runlog/ISTATE 全重定向临时目录，桩客户端回放真实条目）：v4 done 写入=层内裸 sha + fn 被 sanitize 丢 + 台账/ISTATE 落账 ✓、v4t 同 ✓、旧缓存 106,994 条与文件数**零新增** ✓、缺省 base/model=bigmodel/glm-5.3-flash ✓；真机 `--mode v4 --retry-rejected --max-items 2`：拒收路径落层台账、`desc_defer_g3` 1,921 正确延后、判定层 32,090 不受污染 |
| G3 | `desc_control.py --selftest` + `run_desc.py --dry-run/全量/--retry-rejected` + 抽检/筛查 + `check_layer_keys.py` + `interp_read.py --gate` + `gen_manifest.py --selftest` | desc_control 15/15；dry-run 键零碰撞（1,009）；全量 1,009 ok / 0 拒 / 0 败（13 条 one_liner 81-96 字按 v4t 先例放宽带宽 80→96 后 `--retry-rejected` 全捞回，死信同步清理）；G3-4 抽检 30 条编造 0 条 + 全量程序筛查真越界 ~9 条（0.9%）；键体检 desc 分支修复后 **PASS**（分类 35,883 / 身份 35,868 / 在池分类 100.00%）；**G1-5 闸门 PASS：分类 100.00% · 身份 100.00%**；manifest desc 口径修正（新旧键不相交→相加，总 139,601）selftest PASS |

## 另册（不阻塞本清单）

- P1-2 缓存键契约、P1-3 长度口径、P1-4 ai_kind 条件输出
- P2-2 cat/domain 分工、P2-4 回归集、P2-5 字段台账、P2-6 仪表盘、P2-7 人工复核、P2-8 素材扩展、P2-9 外部证明
- 后备：T5a 绿门确认、15 条 failed 清理、Actions 记录清理、**domain_tags 398 条拒收补跑**（397 条是空标签未给 abstain 原因码）

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-08 | **Phase 7 清档完成，G2 全清（✅36/☐0）**：G7-1 归档三保险（备份目录 256/256 sha256 一致 + tar.gz 45MB 回环校验 + `pre-g2` 标签；恢复演练 100/100）；G7-2 用户确认「删除」后 `git rm` 旧目录 256 片 167MB（v3 40,913 + desc_legacy 1,973 + 双存副本 64,108，提交 `0ecd28b43`；MSYS 路径转换坑：`/`→`\`、`D:`→`D;`，提交信息须走 `-F` 文件）；G7-3 删后全量复验 6 项全绿（selftest 8/8 · 键体检 33,697/33,695 双 PASS · 读链 200/200 · manifest 96,715/storage_dup 0 · 引擎 1,763 仓活读 · dual_read 200 旧读归零）；G7-4 文档/契约/记忆收口。**新代四层自此为唯一数据源；tidb 等 override 型 legacy verdicts 随删清零（属用户裁定范围）** |
| 2026-11-08 | **Phase 6 契约与本地验收完成**：G6-1 读取契约落 `docs/AI解析读取契约_G2.md`（四层字段表按真实条目核对）；G6-2 双读 200 仓 `tools/dual_read_check.py`——两处口径修正后 PASS（样本限在池，分类比较字段名感知：legacy 条目本就返回 cat），差异全落可解释类目（复判变更/新读独有/引擎裁决），**异常 0**；G6-3 验收报告 `state/shadow/g6_acceptance_20261108.json` 全达标（层内直读覆盖 99.99%，空值率均为设计内）。**只剩 Phase 7 清档；G7-2 删除旧数据挂用户确认闸门** |
| 2026-11-08 | **Phase 5 迁移与重建完成**：G5-1 程序字段按读链物化进 judge 层（1,763 迁移 + 1,781 已带，删旧前对账 engine 1,929 条丢失 0；166 条"不一致"分诊为被裁决推翻的旧弱路径值，非丢失）；G5-2 台账重建 35,926→33,701（删出池 2,225，对账 0 差异，15 条 failed 全在出池集自然清除——后备项销账），键体检闸门阈值改在池口径（33,600/33,500）；G5-3 manifest 定稿（status=ready + lineage 块 + 100 条出身抽样 100%，g2 归一复核 PASS）。新增 `tools/prog_field_migrate.py`、`tools/rebuild_interp_state.py` |
| 2026-11-08 | **Phase 3 desc 层全链完成 + G1-5 闸门 PASS**：新落 `desc_control.py`（dc1.0 轻判定+轻介绍）与 `run_desc.py`（同 run_domain_tags 骨架）；全量 1,009 条 12 分钟跑完（glm，c=4），912 空描述进死信；13 条超长拒收按 v4t 先例放宽 one_liner 80→96 后全捞回，终态零拒收零失败。`check_layer_keys` 补新层目录查找链 + desc 键族分支（修完 PASS：在池分类 100.00%）；manifest 修 desc 计数口径（新旧键不相交）。**G1-5 复跑：分类/身份双 100.00% PASS**。G3-4 抽检 30 条编造 0 条；全量程序筛查约 9 条（0.9%）技术栈越界记后备。**Phase 0-4 全部完成（✅26/☐10），下一步 Phase 5** |
| 2026-11-08 | **G1-6c CI 提交路径完成**：`interpret.yml` git add 纳入 `state/interp`；gitignore 补 `state/interp/*/runlog/` 与层目录轮转副本规则。G1-6 三步全收口（搬迁→写入→CI），夜间窗起新数据只落新目录进仓 |
| 2026-11-08 | **G1-6b 生产写入切换完成**：`interpret.py` v4/v4t 写入/查重全部走 `LayerStore`（裸 sha + 层台账断点），旧缓存只读不写；v4 模式 no_readme 项不再走旧 desc 通道（1,921 条 `desc_defer_g3` 等 G3-3，防旧键碰撞+旧目录新增）；`AIClient` 缺省改 glm-5.3-flash/bigmodel；`LayerStore` 补 `__contains__`。验收=8 套自检 + 沙箱端到端 16 断言（旧缓存零新增）+ 真机冒烟 |
| 2026-11-08 | **G1-6a 物理搬迁完成**：备份 `D:\dbhub_interp_backup_20261108\`（167MB/256 桶）→ `--apply`（judge 32,090 / text 32,018，domain_tags 已有全量数据保留，desc 0）→ `--verify` **0 差异**；旧目录原样保留（G7-2 删）。顺带修 manifest 过渡期双存重复计数：total 改逻辑口径（138,592），重叠记 `storage_dup`（64,108，G7-2 后归零）。用户定执行序：G1-6a/b/c → G3-1/2/3 → G1-5 复跑 → Phase 5/6，每项完成即全量测试并更新本清单 |
| 2026-11-08 | **工作清单更新**：加「当前进度」快照（✅18/⏸2/☐16）；非空率改全量实测 51.51%；G1-5 复跑（身份 100.00% / 分类 97.00%，只差 desc）；G1-6 搬迁预演数字刷新（judge 32,090 / text 32,018）；补 G2 测试记录与提交号 |
| 2026-11-07 | 初版；方案 A；页面不动，删除挂起至新页面可读 |
| 2026-11-07 | 提示词评审入档：500 影子 + 校准 + app-lite 否决 + 300×四配置 A/B + 36 自检；**无人工金标、无第二专家**，正确性锚仅为行号可回查。输入链路确认为「原文 → clean_readme v2 → 证据包」，evidence_line 是清理后非空行坐标 |
| 2026-11-07 | 发现试点采样偏差：100 条按仓库名排序取前 100，全是 `0*` 仓（tail 偏置），41.75% 不能用于闸门。分层实测 head 非空 63% / mid 45% / tail 36%；G4-3 改为先加 `--stratum` 再跑 300 |
| 2026-11-07 | Phase 0 完成：G0-1 提交 11 文件（be52f85d0）；G0-2 manifest（05e4aa6d3）；G0-3 死信表（7a90bc528）。新增 `interpret/gen_manifest.py`（常量 import 取真值，G5-3 重跑定稿）、`interpret/dead_letter.py`（fn\|layer 分层记账） |
| 2026-11-07 | G4-3 首轮 100 条：机制全绿（断点/重试 7 条自愈/无拒收），三道闸门过，**非空 41.75% 差 3.25pp 未过**。n=100 不可判定（95% 区间 32–52%），建议补到 300 再定；空标签全部是 evidence-backed abstain，不是解析失败 |
| 2026-11-07 | G4-1/G4-2 完成：词表 v0.11 定版（abstain 单码，75 词），`run_domain_tags.py` 独立 runner 冒烟 3/3 —— **domain_tags 已可独立执行**，只写自己的目录，与 v4/v4t 并行不冲突 |
| 2026-11-07 | G1-6 代码就绪：`interp_layer_store` 四层解耦存储（payload 白名单、fn 不进条目、脏桶落盘、断点台账、runlog）+ `split_layers` 搬迁工具（dry-run 已验）+ 读层兼容新旧布局。物理搬迁等 v4t 收尾后 `--apply` |
| 2026-11-07 | 用户裁定存储架构：四层各自独立目录、分片保存、断点/超时机制同一套；存量 v4/v4t 在 v4t 跑完后一次性搬。新增 G1-6 |
| 2026-11-07 | 拆出 G1-6b/G1-6c：搬迁只搬存量，生产写入与 CI 提交路径必须同步切到新目录，否则夜间 CI 双写旧目录、新数据不进仓。三步顺序写入序约束第 5 条 |
| 2026-11-07 | 用户补充两条口径并写入固定决策与 G1-6 细则：①分片内容尽量解耦（每层只存自己字段、fn 不进条目）②后面通过程序拼接（join 按 sha 取四层，不做冗余复制）。断点/超时/额度等待明确为四层共用同一 runner 骨架 |
| 2026-11-08 | **G4-4/G4-5 完成（domain_tags 全量）**：00:34–07:51 跑完 31,341 条，ok 30,936（非空 15,934）/ 拒收 398 / 失败 7，3.3s/条；累计库存 31,598 条。验收四闸全过：拒收 1.27% / OOV 0% / 证据 100% / 非空 51.51%；分层 head 67.50% / mid 59.99% / tail 49.20%。398 拒收里 397 条同一原因（空标签未给 abstain 码），列入补跑后备 |
| 2026-11-08 | **Phase 2 收尾**：G2-4 覆盖率报告落盘（v4 99.997%、身份 99.93%、desc-only 989→G3）；G2-5 提交 AI 数据并打 `tag pre-g2`。G4-4 同时在跑（并发 4） |
| 2026-11-08 | **G2-1/G2-2/G2-3 收口**：v4t 原跑最终 done 24,699 / 拒收 22 / 失败 29；复跑 112 → 98 ok / 10 拒收 / 4 失败。v4 复跑 433 → 429 ok / 4 拒收。模型归一 453 键（v4 398 / v4t 55）备份后重烧，核对 **left=0、current_missing=0**；26 条因 README sha 变更自然作废（不计缺失）。在池覆盖：分类 99.94% / 身份 99.93%。**发现并停掉守夜脚本 bug**：grep `解读完成` 但 v4t 输出 `文本卷完成`，导致无限重启抢额度。G4-4 00:34 开跑（并发 4，待办 31,341） |
| 2026-11-08 | G2-2 首轮清理误判说明：22:56 删除 453 键后，运行中的 v4t 用内存缓存回写了 63 条（脏桶落盘覆盖），属并发写冲突非数据损坏；v4t 退出后重跑 `--apply` 全部收口。教训：**删缓存必须在无 interpret 进程时做** |
| 2026-11-07 | G4-4 开跑：**并发 4**（用户定，与 v4t 一致），待办 31,618 条；起跑前先跑的一轮 c=6 已停止，已落盘 120 条不浪费。v4t 进程已退出（run `1107_1144_v4t_p4.0`：done 21,461 / rejected 18 / failed 26），G1-6a/G2 解锁。**该“已退出”判断后被更正：当时并未退出，最终 done 24,699** |
| 2026-11-07 | **G4-3a + G4-3 完成（分层试点过闸）**：`--stratum` 按 head≥1000★/mid 100–999★/tail<100★ 各抽 100（seed 20261107，可复现）；300 条实跑 13 分钟，拒收 2.00% / 词表外 0.00% / 证据 100% / 非空 61.51%，四闸全过；分层 73.20% / 57.14% / 54.17%，明显高于 500 影子估算（63/45/36）。拒收 6 条同一原因（空标签未给 abstain 码），失败 3 条，均可补跑。`vc_stats` 增 `--since` 与分层报表（注意 state 的 `at` 是 UTC） |
| 2026-11-07 | 模型统一口径入档：四层（judge/text/domain_tags/desc）一律 `glm-5.3-flash`，不使用其他模型；G2-2 归一目标写明、manifest `mixed.action` 同步；G1-6b 顺带把 `AIClient` 缺省模型/base 从 deepseek 改为 glm-5.3-flash + bigmodel |
| 2026-11-07 | G1-5 闸门首跑 FAIL：分类 97.00% / 身份 94.50%。**这是数据未齐而非代码缺陷**——v4t 还差约 6,800 条、desc-only 1,009 仓要等 G3。闸门保留，待 G2-1+G3-3 后复跑；Phase 2/3 属于产出数据本身，不受此闸门阻塞 |
| 2026-11-07 | G1-4 完成：读层自检补齐缺卷/双卷/desc 新旧并存/形态不符/构建稳定性，41 条断言全绿 |
| 2026-11-07 | G1-3 完成：`ai_flag` 判定卷读 `ai_kind`（other 不算 AI，四类才真）、`dbs()` 六层来源优先级。**口径修正**：engine 恢复 1,749 而非 1,955——差值 214 是 v4 程序回写的「应用类不采纳」显式空结论（writeback v2 质量门，dbs_raw 留痕），新代以它为准；AI 检出 2,561 与旧估 1,449 的差同理（v4 ai_kind 四类口径） |
| 2026-11-07 | G1-2 完成：`interp_read` 改台账 fn→sha 权威连接 + 六层合并，旧单槽遮蔽与镜像共享两事故有回归用例。**已知过渡回退：dbs engine 1,963→30**（判定卷无 dbs_src，程序字段还在旧代条目里），G1-3 修 |
| 2026-11-07 | G1-1 完成：`lib/interp_keys.py` 层键契约（含「形态 vs 出处」分离——962 条 desc 旧键是 v3 结构）；`tools/check_layer_keys.py` 只读体检，闸门 PASS。**删旧代风险量化：在池仅旧代可读 分类 1,022 / 身份 7,432**，G2 收齐 v4t 后复查 |
