# dbhub_collect — 数据库生态采集仓库

只包含**采集功能**和**采集数据**：候选池采集、README 扫描、信号富集、多机状态合并。
解读（interpret）/ 分类（classify）/ 渲染（render）等产品侧代码在主项目 dbhub_v2，不在本仓库。

## 目录结构

```
collect/   collect_pool.py（池采集：probe→topic→org→关键词→白名单）
           readme_sweep.py（README：init 全量 / weekly 周增 / monthly 月全量，ETag 304）
enrich/    enrich.py（富集：commit/release/security/contrib/lang 五维分层增量）
config/    db_profiles.py（档案） + strategy.py（通道派生+一致性校验）
lib/       gh.py（GitHub 客户端/预算/限流） + merge_states.py（多机键控并集合并）
data/      snapshot_YYYYMMDD/ 采集数据（见下）
state/     断点状态（任何机器克隆即可续采增量）
tools/     sync_from_main.py（从主项目同步采集代码，防两份漂移）
```

## 采集数据布局

- `data/snapshot_YYYYMMDD/pool.json` —— 当日候选池（新格式，2026-09-16 起）
- `data/snapshot_YYYYMMDD/merged/all_projects.json` —— 历史快照（旧管道格式，
  2026-08-05 ～ 09-12，growth 计算双格式兼容）
- `data/snapshot_YYYYMMDD/meta/` —— probe / run_summary
- `data/readmes/`、`data/snapshot_*/parts/` —— **不入库**的工作区数据（见 .gitignore）

## 常用命令

```bash
# 通道校验（改 config 后先跑这个）
python config/strategy.py

# 池采集（断点续采，预算内跑多少算多少）
python collect/collect_pool.py                    # 当晚全流程
python collect/collect_pool.py --only topic       # 只跑某阶段
python collect/collect_pool.py --dry-run          # 只打印查询不联网

# README（先有 pool）
python collect/readme_sweep.py --mode init    --pool data/snapshot_YYYYMMDD/pool.json
python collect/readme_sweep.py --mode weekly  --pool data/snapshot_YYYYMMDD/pool.json

# 富集（分层增量：head=star≥1000 每周 / mid=star≥100 每月 / tail 仅安全通告）
python enrich/enrich.py --tier head
python enrich/enrich.py --tier all

# 多机采集结果合并（服务器与本地各自跑完后）
python lib/merge_states.py --help
```

## 多机协作

各机克隆本仓库 → 跑采集 → commit + push（服务器网络通畅，数据推送从服务器发）。
token 放各自机器的 `.env`，永不入库。三机共用 token，注意配额抢占。

## 代码同步

采集层代码以主项目 dbhub_v2 为开发主线，改动后运行：

```bash
python tools/sync_from_main.py            # 默认从 ../dbhub_v2 同步
python tools/sync_from_main.py --src D:/dbhub_v2 --with-snapshots
```
