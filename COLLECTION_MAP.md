# COLLECTION_MAP — 采集全景图

> 采集项 / 采集内容 / 采集策略 / 采集频率 的单一参考。
> 口径截至 2026-10-29（池 31,884 仓 · README 已抓 34,170 · 解读缓存 41,200+ 条）。
> 改动采集策略或工作流时同步更新本文档。

## 0. 一图流水

```
collect_intl / collect_cn   →   enrich   →   readme_sweep   →   interpret   →   unattr_judge
     发现入池(每晚)          元数据分层到期     正文周增量月校准     AI 判读(2h)      未归类周检(周一)
                                   ↘ evidence_collect 证据指纹打底（树/依赖/镜像，每天 06:35）
```

数据流向一条线；**真正分国产/国际的只有发现层与富集层，README/解读/判定三层全池共用一套。**

---

## 1. 定时工作流（GitHub Actions，共 4 条）

| 工作流 | 文件 | 时间（北京） | 职责 |
|---|---|---|---|
| nightly-collect | `collect.yml` | 每天 00:00 | 发现入池 + 富集 + README + 治理收尾（单窗 6h） |
| nightly-interpret | `interpret.yml` | 每 2 小时 :23 | db_scan 提名 + AI 解读（每窗 100 分钟 / 1200 条） |
| unattr-judge | `unattr_judge.yml` | 每周一 10:30 | 未归类仓判定（台账幂等，配额墙自动收尾接力） |
| evidence-collect | `evidence.yml` | 每天 5 班（06:35/10:35/14:35/18:35/22:35） | 证据指纹采集（树+依赖+镜像；断点续采，collect 窗外全天铺满） |

推送撞车由各流提交步骤的重试+变基（5 轮）兜底；不同工作流分属不同 concurrency 组，互不取消。

---

## 2. 定时采集项（7 项，全部真实调 API）

### 2.1 国际池发现 `collect/collect_intl.py`（Search API）

- **内容**：仓库元数据——star、描述、语言、topics、pushed_at、watchers
- **策略**：五通道
  1. topic 扫描：17 库 + 生态词，星 ≥10（信噪比线），大 topic 按星三档→年→月拆
  2. 发现桶：`topic:database` 泛库捞 17 库外新 DB，剔除已覆盖噪音 topic
  3. 关键词检索：星 ≥10
  4. org 扫描
  5. 新项目窗口：45 天内新建且星 ≥3，当晚最先跑（最易腐烂）
  - 外加 watch 保险名单每晚重扫（防漏兜底）
- **频率**：每晚，800 次调用，断点续采

### 2.2 国产池发现 `collect/collect_cn.py`（Search API）

- **内容**：同上
- **策略**：四通道（无新项目窗口——主通道无星线即覆盖新仓）
  - 国产 topics / 关键词，**无星线**（star_min=0，国产正经产品常只有几十星）
  - org 三级：dedicated（pingcap、tikv、oceanbase、polardb、opengauss-mirror、yashan-technologies 等产品 org 零门槛直收）／cloud（huaweicloud、tencentcloud、ApsaraDB ≥10 星当范围噪音闸）／standard
  - 单查询超 GitHub 1000 条硬上限按创建年→月拆（不套星档，防隐性加线）
- **频率**：每晚，1000 次调用

### 2.3 元数据富集 `enrich/enrich.py`（Core API）

- **内容**：五维——commit 7 天/90 天计数、release（版本/日期/90 天发版数 + **最近 3 条正文前 512B**：适配变更史素材，10-30 起，零新增调用）、安全漏洞（GHSA/CVE 明细+最重等级）、贡献者数、语言占比
- **策略**：按星分层到期，到期的维度才采

| 层 | 范围 | commit | release | 漏洞 | 贡献者 | 语言 |
|---|---|---|---|---|---|---|
| 头部 | ≥1000★ | 7 天 | 7 天 | 30 天 | 90 天 | 一次 |
| 中间 | 100–999★ | 30 天 | 30 天 | 90 天 | 一次 | 一次 |
| 尾部 | <100★（仅国际） | **不采** | 一次 | 180 天 | 一次 | 一次 |

  - **国产保底中间层**：<100★ 的国产仓也按中间层盯（识别 = topics / 国产通道发现 / 国产 org 三信号任一）
  - 死仓零调用：pushed_at 未变则 commit/release 不重采；漏洞是外部事件，到期必查不豁免
- **频率**：每晚跑，每仓按 7/30/90/180 天轮，5000 次调用 / 220 分钟

### 2.4 README 正文 `collect/readme_sweep.py`（Core API）

- **内容**：README 全文
- **策略**：周增量（有变化才抓）；每月 1 号自动转月度全量校准（calibrated 按日标记跨窗接力，不重烧）
- **频率**：每晚增量 4200 次调用 / 每月 1 号全量。**全池共用**

### 2.5 AI 解读 `interpret/interpret.py`（bigmodel API，glm-5.3-flash）

- **内容**：逐仓判读——12 类工具分类、库名候选逐条裁决（db_verdicts）、每库支持判定
- **策略**：程序提名（db_scan）+ 逐候选裁决；按 README 内容 sha 去重不重复花钱；并发 4 断点续跑；语料烧空每窗 1 分钟即收（设计内）
- **频率**：每 2 小时 :23（整点被 GitHub 丢弃，错峰），每窗 100 分钟 / 1200 条。**全池共用**

### 2.6 未归类判定侦查 `interpret/unattr_judge.py`（trees API + raw）

- **内容**：仓库文件树全量路径（E1）+ 依赖清单原文（E3：requirements / pyproject / package.json / go.mod / pom.xml / Cargo.toml / Gemfile / composer.json / csproj / CMakeLists 等，根级优先取前 6 个）
- **策略**：只查无 README 行号引证的仓；零网络信号层先筛（范围外词表/教程词表/已裁决）；联网结果台账幂等粘住不重扫；配额墙（连败 8 次）自动收尾下周接力；产出 draft 归属草案（签发权在人，进 `config/overrides.json`）
- **频率**：每周一 10:30。**全池共用，按 star 从高往低**

### 2.7 证据指纹 `evidence/evidence_collect.py`（trees API + raw）

- **内容**：文件树（路径/截断/ETag）+ 依赖清单指纹（12 种生态的依赖名，不含 lock 全文）+ 镜像指纹（compose/Dockerfile/helm values/workflows 的 image 行）+ 路径指纹（connector/driver/dialect/adapter/plugin 类路径，≤40 条）+ 线索（CHANGELOG/中文 README/docs 支持矩阵路径、README 内官网矩阵 URL）。**只存指纹+指针不存原文**；blob sha 本地重算校验防分支漂移
- **策略**：vocab-free（只抽名字不判库，匹配归适配引擎）；分档全量（P0 点名 → 国产空白 → 国际空白 → 国产余量 → 国际高星 → 国际余量）扫完转增量；断点=分片终态记录（empty_repo/gone 终态不重试，error 三振出局）；256 分片（`state/evidence_cache_shards/`，三胞胎之三）；pushed_at 未变 0 调、树 ETag 304 再省
- **频率**：每天 5 班（06:35/10:35/14:35/18:35/22:35，collect 窗外全天铺满）4500 调 / 110 分钟每班；本地实测 12.5s/仓、CI 待首跑校准。首采全量 31,884 仓预估 2~4 天收敛；收敛后头班干完增量、其余班空转退出。周一 10:35 班与未归类侦查同窗，配额墙互让

---

## 3. 手动备用入口（workflow_dispatch，无定时）

| 入口 | 用途 |
|---|---|
| `readme-monthly.yml` | 月度全量校准的非 1 号补跑（与采集同队列串行，不抢配额） |
| `retro_audit.yml` | 解读缓存质量重审（调 AI：基线→剪缓存→重跑→对账） |
| collect 手动档 | 勾 force_monthly 强制月校准（不受 1 号限制） |
| interpret 手动档 | 可开重试拒收（捞历史拒收项）/ 调批量，吃满单窗 6h |
| unattr_judge 手动档 | 可调 limit / 只补扫 api_error / dry-run 预演 |
| evidence 手动档 | 可调 mode（auto/sweep/incremental）与 max_calls（全量加跑期建议 4500） |

---

## 4. 本地派生与治理（零 API，产账不采新数据）

| 项 | 内容 | 频率 |
|---|---|---|
| `interpret/db_scan.py` | 本地扫 README 全文提名库名候选 + 行号，喂给解读 | 每 2 小时随解读窗 |
| `tools/purge_outpool.py --stamp` | 出池仓 absent_since 打戳（零侵入台账） | 每晚 |
| `tools/release_archive.py rotate` | ≥15 天快照打包上 Releases（按月归档），远端 digest 一致才删本地 | 每晚 |
| `tools/purge_outpool.py` | 出池仓清理 dry-run 清单（人过目后本地 --apply；宽限 30 天，屏蔽仓 7 天） | 每月 1 号 |

---

## 5. 一次性历史工具（已完工，纯遗留，可删）

- `m3_filter.yml` — 2026-10-08 历史瘦身（filter-repo 重写）
- `m3_upload_post.yml` — 瘦身后备份 bundle 上传
- 备份均在 Releases（`m3-backup-20261008`、`pre-m3-full-bundle`）

---

## 6. 国产 / 国际差异设计原因（速记）

1. **国产入池不设星线**：国产库生态星数整体偏低，按 ≥10 星线会把官方产品挡在门外；靠关键词与 org 分级控噪音，宁全收。
2. **国产富集保底中间层**：约 7 千国产仓若按星分层会几乎全掉尾部层（死活无人问）；托底到中间层保证每 30 天看活没活、每 90 天查漏洞。
3. **国际尾部长尾不采 commit**：国际尾部仓量最大、价值密度最低，死活只看 pushed_at，把配额让给头部。

## 7. 频率一页速查

```
每晚 00:00   发现（国际800 + 国产1000 调）→ 富集(5000调/220min) → README 增量(4200调)
             → absent_since 打戳 → 快照归档
每 2 小时    db_scan 提名 → AI 解读(100min/1200条)
每天 5 班    证据指纹（06:35/10:35/14:35/18:35/22:35，4500调/110min每班；全量收敛后头班干完增量）
每周一 10:30 未归类判定（树+依赖侦查）
每月 1 号    README 全量校准 + 清理 dry-run 清单
每 7/30/90/180 天  富集各维度按层到期轮换
```
