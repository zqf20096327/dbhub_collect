# M2b 切换运行手册：pool 三件套 → NDJSON 活文件

> 状态：代码已就位（lib/pool_store.py），本手册所列改动在**切换晚**一次性执行。
> 原因：collect/pool_core.py 当前有另一会话未提交修改，CI yaml 必须与落盘代码同 commit 生效。

## 一、前置条件（缺一不切）

1. M1 归档滚动已上线且跑通 ≥1 晚（CI 里 rotate 步骤绿）。
2. 当晚本地停跑 collect 类任务（本地只读不写 pool 即可，interpret/readme 不受影响）。
3. 工作树干净：pool_core.py 的未提交修改已由归属会话落掉。
4. 切换晚前已用当前快照做过一次演练（见"四、验收"第 1 条的历史演练记录）。

## 二、代码改动清单

### 2.1 collect/pool_core.py（写入方，唯一落盘改动点）

`_merge_step()` 末尾（原 `atomic_write_json(snap / "pool.json", ...)` 处）改为：

```python
# 三路写：①NDJSON 活文件（进 git，每日只传变化行）
#        ②snapshot_latest 桥文件（gitignored，旧 list 格式，CI 内下游用）
#        ③快照目录不再写 pool.json 全量（M2b 起停，meta 照旧）
import pool_store  # 文件头已有 sys.path 处理则复用
pool_store.write_live(union_list, "pool")
union_list_intl = ...   # 若 _union_pools 已分侧算出，此处分别 write_live(...)
atomic_write_json(HERE / "data" / "snapshot_latest" / "pool.json", union_list)
```

注意：pool_intl/pool_cn 同理分别 `write_live(..., "pool_intl")` / `("pool_cn")`，
桥文件只 pool 需要（yaml 只桥接 pool）。`pool_{section}.json` 完成标记**保留**（断点续采语义不变）。

### 2.2 .github/workflows/collect.yml（"衔接当日池"步骤）

```yaml
- name: 衔接当日池（准备 snapshot_latest）
  run: |
    mkdir -p data/snapshot_latest
    if [ -f data/live/pool.ndjson ]; then
      python -c "import sys; sys.path.insert(0,'lib'); import pool_store, json; \
        recs,_ = pool_store.load_latest('pool'); \
        json.dump(recs, open('data/snapshot_latest/pool.json','w',encoding='utf-8'), \
        ensure_ascii=False)"
    else
      POOL=$(ls -t data/snapshot_*/pool.json 2>/dev/null | head -1)
      [ -z "$POOL" ] && { echo "无可用 pool，跳过后续"; exit 0; }
      cp "$POOL" data/snapshot_latest/pool.json
    fi
```

readme-monthly.yml 的同步骤同样改法。

### 2.3 interpret 系 glob 脚本（5 处，同模板）

`interpret.py:72`、`unattr_judge.py:191`、`retro_audit.py:112`、`agent_batch.py:102`、
`db_scan.py:76` 的 `sorted(glob("snapshot_20*/pool.json"))` 模式改为：

```python
sys.path.insert(0, str(ROOT / "lib"))
import pool_store
recs, src = pool_store.load_latest("pool")   # 活文件优先，回退最新快照
```

enrich.py / readme_sweep.py 走 `--pool data/snapshot_latest/pool.json` 显式传参，
桥文件保持旧格式，**无需改动**。gc_states.py 的"最近 N 个 pool.json 并集"口径改为：
最新活文件 + 最近快照并集（切换 15 天后老快照归档完，只剩活文件，逻辑自然收敛）。

### 2.4 .gitignore 追加

```
data/live/*.ndjson.tmp
_archive_tmp/
```

> **时序提前警示（M1 即生效）**：`_archive_tmp/` 这行在 **M1 rotate 上线的同一个
> commit** 里就要加——rotate 失败/中断时归档包残留目录，CI 的 `git add -A` 会把
> 1.7~30MB 的包收进 git（332MB 轮转副本旧事重演）。等 M2b 才加就晚了。
> （.gitignore 当前有未提交修改，故本行随 M1 上线 commit 一并落，不提前改文件。）

## 三、切换时序（当晚）

1. 22:00 前：确认前置条件，本地 `git pull`，工作树干净。
2. 应用 2.1–2.4 改动，本地冒烟：
   `python -c "import sys; sys.path.insert(0,'lib'); import pool_store; print(len(pool_store.load_latest('pool')[0]))"`
   （应输出与最新快照一致条数）
3. 提交推送（一个 commit：代码 + yaml + gitignore，不带数据文件——活文件由当晚 CI 首产）。
4. 当晚 CI 正常跑：产出的 commit 里应出现 data/live/pool.ndjson（新增），
   data/snapshot_当日/ 不再有 pool.json（仅 meta 与 pool_{section}.json 标记）。
5. 次日早验收（下节）。

## 四、验收（次日）

1. **语义等价比对**（唯一口径，文件 sha 不适用）：

```bash
python - <<'EOF'
import sys, json, subprocess
sys.path.insert(0, 'lib')
import pool_store
# 昨日最后快照（切换前最后一份旧格式全量）
old = json.load(open('data/snapshot_<切换前一日>/pool.json', encoding='utf-8'))
new, src = pool_store.load_latest('pool')
d = pool_store.semantic_diff(old, new)
print(json.dumps(d, ensure_ascii=False, indent=1, default=str))
assert d['equal'], '语义比对未通过，禁止删任何旧路径'
EOF
```

2. 条数一致、only_a/only_b 为预期的当日增减（若有新采集，人工核对增减名单）。
3. **日变化行数落档**（M4 预算依据）：

```bash
# 前后两晚活文件 commit 的差异行数（跨两日比对时各取当日最后 commit）
git show HEAD:data/live/pool.ndjson  | sort > /tmp/a
git show HEAD~1:data/live/pool.ndjson | sort > /tmp/b
comm -3 /tmp/a /tmp/b | wc -l
```

>1.5 万行/天连续两天 → 启动慢字段后手（updated_at 等拆 pool_activity.ndjson），
> 决策规则见方案 M2b。

4. CI 连续两晚全绿 → M2b 完成，进入 M3。

## 五、回滚

- 切换当晚 CI 红或次日比对不过：revert 切换 commit，恢复 pool_core 旧版。
  旧格式数据仍在（切换前的快照目录在 15 天归档窗口内），无数据损失。
- 活文件数据本身永远可从最新快照重建：`pool_store.convert_snapshot(snapshot, live)`。

## 六、历史演练记录

- 2026-10-06 本地验证：snapshot_20261003/pool.json (34,290 条) → convert →
  load_latest 回读 → semantic_diff 零差异（见验证报告）。
