# M2b 切换运行手册（终版）：pool 三件套 → NDJSON 活文件

> 状态：代码全部落地并本地验证。切换晚按"三、时序"执行。
> 设计定案（行号背书见 pool_core.py:412-484）：`pool_{section}.json` 三重职责
> （完成标记 / union 输入 / CI 跨机续跑侧数据载体）拆解为**轻量标记 + 侧活文件**。

## 一、改动清单（已全部实施）

### 1. 写入方（collect/pool_core.py，唯一写点）
- `_merge_step`：parts 合并 → `write_live(merged, f"pool_{section}")` + 轻量标记
  `{"done","count","ts"}`（几百字节仍进 git）。空结果不覆盖活文件（09-29 防线）。
- union：`_union_pools_live()` 读两个侧活文件（load_latest 回退快照），黑名单
  过滤/all_sources 合并与旧 `_union_pools` 同款；union 为空不写 pool（次防线）。
- pool 活文件 + 桥文件（`data/snapshot_latest/pool.json`，gitignored，stars 降序
  旧格式）双写；快照目录不再产 pool*.json 全量。

### 2. 读取方（7 处 + gc_states，全部"取最新"语义，逐行确认过）
- interpret.py `latest_pool()` → load_latest；调用处 json.loads → `read_any`
- agent_batch.py（`--pool` 显式路径经 read_any 兼容两种格式）
- db_scan.py `latest_pool()` + 调用处
- golden_eval.py 两处（金标关的池读取，仅格式兼容、语义不变）
- _repro_do.py、retro_audit.py `pool_stars()`、unattr_judge.py 内联 glob
- gc_states.py `alive_fns()`：活文件 ∪ 最近旧快照（15 天后退化当前池判活，可接受）
- `pool_store.read_any(path)`：ndjson/旧 json 通吃的兼容读（唯一解析入口）

### 3. CI（2 个 yaml）
- collect.yml / readme-monthly.yml 的"衔接当日池"：活文件优先转桥，旧 `ls -t` 兜底。

### 4. 种子
- `data/live/pool.ndjson`(34,401) / `pool_intl.ndjson`(27,318) / `pool_cn.ndjson`(7,194)
  由 snapshot_20261006 convert，三件语义等价校验过。**切换晚用当晚最新完整快照重做**。

## 二、验证记录（本地）

- 三件 convert → 语义比对 equal=True、零大小写碰撞
- `_merge_step` 冒烟（真实 parts 沙盒）：见完整验证输出
- 回退语义：无活文件时 load_latest 回退最新快照 ✅
- read_any：两种格式 + `--pool` 显式路径 ✅

## 三、切换时序（执行段）

1. 【北京 22:00 前】确认：M1 滚动首跑绿；工作树干净（除管线产物）；本地已收敛。
2. 重做种子：用当晚最新完整快照 convert 三件，落档基线日期。
3. 冒烟：`python -c "import sys;sys.path.insert(0,'lib');import pool_store;print(len(pool_store.load_latest('pool')[0]))"`
4. 提交推送（单 commit：代码+yaml+种子+本手册）。撞 interpret 推送则重跑
   push_via_api（幂等）；**含 workflow 文件必须 --gh-token**。
5. 当晚 CI collect 即真实首验（不手动触发，省采集配额）。

## 四、次晨验收

1. collect workflow 绿。
2. commit 含 `data/live/*.ndjson` 更新；`snapshot_当日/` 只有 meta + 轻量标记。
3. 语义比对（差异应全部为业务增删；改名 repo=旧删新增对）：
   ```bash
   python - <<'EOF'
   import sys, json; sys.path.insert(0,'lib')
   import pool_store
   old = json.load(open('data/snapshot_<基线日>/pool.json', encoding='utf-8'))
   new, _ = pool_store.load_latest('pool')
   print(json.dumps(pool_store.semantic_diff(old, new), ensure_ascii=False, default=str))
   EOF
   ```
4. 日变化行数落档（M4 预算依据）：
   ```bash
   git show HEAD:data/live/pool.ndjson | sort > /tmp/a
   git show HEAD~1:data/live/pool.ndjson | sort > /tmp/b
   comm -3 /tmp/a /tmp/b | wc -l
   ```
   >1.5 万行连续两天 → 启动慢字段后手（updated_at/pushed_at 拆 pool_activity.ndjson，
   > 桥文件生成时 join 回完整记录，下游零改造）。

## 五、回滚

- revert 单一切换 commit：活文件随 revert 消失，读取方自动回退 glob 旧快照
  （15 天窗口内），断点续采/回退昨池语义全程无伤。
- 活文件永远可从最新快照重建：`pool_store.convert_snapshot(snapshot, live)`。
