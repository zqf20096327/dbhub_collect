# dbhub_collect — 数据库生态采集仓库

只包含**采集功能**和**采集数据**：候选池采集、README 扫描、信号富集、多机状态合并。
解读（interpret）/ 分类（classify）/ 渲染（render）等产品侧代码在主项目 dbhub_v2，不在本仓库。

## 目录结构

```
collect/   collect_intl.py（国际池采集：stars>=10 + 新项目窗口）★
           collect_cn.py（国产池采集：不设星，专属 org 无星线/云厂商 org>=10）★
           pool_core.py（两入口共享核心：拆档/截断修复/merge 并集）
           readme_sweep.py（README：init 全量 / weekly 周增 / monthly 月全量，ETag 304）
enrich/    enrich.py（富集：五维分层增量 + push/时间维度二分 + 国产 floor=mid）
config/    db_profiles.py（档案 + sections 分策策略） + strategy.py（通道派生+一致性校验）
lib/       gh.py（GitHub 客户端/预算/限流） + merge_states.py（多机键控并集合并）
data/      snapshot_YYYYMMDD/ 采集数据（见下）
state/     断点状态（任何机器克隆即可续采增量）
tools/     sync_from_main.py（从主项目同步采集代码） + gc_states.py（state 残渣 GC）
```

## 分策采集（国际 / 国产）

策略单一事实源：`db_profiles.GLOBAL["sections"]` + 档案 orgs 的 `class` 字段。

| 通道 | 国际 7 库 | 国产 10 库 |
|---|---|---|
| topic | `stars:>=10`；超1000 星三档→年→月拆 | **不设星**；超1000 纯按创建期拆（不套星档） |
| keyword | 仅 sqlite 词 `>=10` | 16 专有词（含中文）**不设星** |
| org | `>=10` | dedicated（org 即产品，含 tidb-samples 等）**无星线**；cloud（云厂商超集）`>=10` |
| 新项目 | `created>=45天前 stars>=3` 窗口，当晚最先跑 | 无需（主通道无星线，新仓天然覆盖） |
| 富集 | 按 star 分层 | **floor=mid**（识别：国产 topic ∪ 国产通道命中） |

任何检索查询 total>1000 一律拆分抓取（旧版 keyword 在 1000 处静默截断，已修复）。
富集维度按变化成因二分：push 依赖（commit/release/contrib/lang）仅在 pushed_at
变化时刷；security 到期即刷（死仓豁免已修复）。

## 采集数据布局

- `data/snapshot_YYYYMMDD/pool.json` —— 当日候选池（国际+国产并集）
- `data/snapshot_YYYYMMDD/pool_intl.json` / `pool_cn.json` —— 分 section 池
- `data/snapshot_YYYYMMDD/merged/all_projects.json` —— 历史快照（旧管道格式，
  2026-08-05 ～ 09-12，growth 计算双格式兼容）
- `data/snapshot_YYYYMMDD/meta/` —— probe_intl / probe_cn / run_summary_*
- `data/readmes/` —— README 正文（**入库**；平均 7KB/仓，超 100KB 截断）
- `data/snapshot_*/parts*/` —— 不入库的中间数据（分通道原始结果，仅断点续采需要）

## 常用命令

```bash
# 通道校验（改 config 后先跑这个）
python config/strategy.py

# 池采集（国际/国产分脚本，断点续采，预算内跑多少算多少）
python collect/collect_intl.py                # 国际：stars>=10 + 新项目窗口
python collect/collect_intl.py --only new     # 只跑新项目窗口
python collect/collect_cn.py                  # 国产：不设星
python collect/collect_intl.py --dry-run      # 只打印查询不联网

# README（先有 pool）
python collect/readme_sweep.py --mode init    --pool data/snapshot_YYYYMMDD/pool.json
python collect/readme_sweep.py --mode weekly  --pool data/snapshot_YYYYMMDD/pool.json

# 富集（分层增量：head=star≥1000 每周 / mid=star≥100 每月 / tail 仅安全通告；
#       国产仓 floor=mid；push 依赖维度仅 pushed_at 变化时刷）
python enrich/enrich.py --tier head
python enrich/enrich.py --tier all

# state 残渣 GC（出池仓的 state 条目清理，默认 dry-run）
python tools/gc_states.py --apply

# 多机采集结果合并（服务器与本地各自跑完后）
python lib/merge_states.py --help
```

## 自动采集（GitHub Actions，主采集器）

`.github/workflows/collect.yml`：每晚北京 00:00 自动跑 **池采集·国际（800 调用）→
池采集·国产（1000 调用）→ README 增量（每月 1 号自动转月度校准）→ 富集（分层增量）
→ 每月 1 号 state 残渣 GC**，数据直接 commit + push 回本仓库。
用内置 `GITHUB_TOKEN`（独立 1000 次/时配额桶，不占用个人 PAT 的 5000/时），
触线由 `--max-calls` 预算优雅收尾、次晚续采。也支持在 Actions 页面手动触发。

## 多机协作

- **本地/服务器**：以开发与数据消费为主（`git pull` 取数）。可以跑采集，但
  **不要与 Actions 同晚跑同一任务**（state 文件双写会 git 冲突）；跑前先 `git pull --rebase`。
- token 放各自机器的 `.env`（Actions 用 secrets，无需配置），永不入库。

## 代码同步

采集层代码以主项目 dbhub_v2 为开发主线，改动后运行：

```bash
python tools/sync_from_main.py            # 默认从 ../dbhub_v2 同步
python tools/sync_from_main.py --src D:/dbhub_v2 --with-snapshots
```
