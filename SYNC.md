# 手工同步步骤（GitHub → 本地）

CI 在云端跑，解读/采集的结果都提交在 GitHub 上。要把这些拉到本地，按下面走。
前提：`.env` 里有 `GITHUB_TOKEN`（已配好）。

---

## 第 1 步：试 git 通不通

```bash
git fetch origin
```

- 成功 → 走 **A（正常 git 同步）**
- 卡住 / 超时（github.com 443 间歇阻断）→ 走 **B（API 兜底）**

---

## A. git 通了：正常同步

### 1. 看两边差多少

```bash
git log --oneline main..origin/main    # 远端比本地多的提交
git log --oneline origin/main..main    # 本地比远端多的提交
```

### 2. 按情况三选一

**情况 1：本地纯落后**（第二条命令输出为空）——最常见：

```bash
git pull --ff-only origin main
```

如果报 `local changes would be overwritten`（本地未提交修改挡路）：

```bash
git stash
git pull --ff-only origin main
git stash pop
```

stash pop 有冲突时，先想"本地领先"：本地 python 管线一直在写 data/，冲突文件多半是本地刚写的较新内容，保本地那份。

**情况 2：分叉了**（两条命令都有输出）——用 reset --mixed 合并法，别用 rebase（撞车会丢数据）：

```bash
git branch backup/local_0103        # 先备份本地 main，兜底
git reset --mixed origin/main       # 本地独有提交的全部改动回到工作区，不会丢
git add -A
git commit -m "合并本地管线改动"
git push origin main
```

**情况 3：本地领先**（第一条命令输出为空）——不用拉，该干嘛干嘛。

### 3. 收尾确认

```bash
git log --oneline -3        # 本地最新一条应和 origin/main 对上
```

---

## B. git 断了：API 兜底（tools/sync_remote_api.py）

git 拉不动但 api.github.com 通常还能通，用它把远端数据直接落盘：

```bash
python tools/sync_remote_api.py --dry-run     # 先看有多少差异，不落盘
python tools/sync_remote_api.py               # 落盘（只拉 data/ + state/）
```

差异上千就分批：`--limit 300`（Core API 小时帽 ~5000）。

特点 / 注意：

- 脚本已做 CRLF 归一化比对，不会把 3 万文件误判成差异。
- 只拉 data/ state/，不动代码文件；远端已删的本地文件不会被删。
- 落盘后 `git status` 会显示一堆"已修改"——**正常**（工作区=远端内容，HEAD 还在旧提交）。
- 这不是 git 合并！git 恢复后仍要补走一遍 A，历史才能真正对齐。

---

## 每次同步前扫一眼的坑

1. **data/ 单文件"已修改" ≠ 坏事**：本地管线持续写 data，多半是本地领先，别 `git checkout` 丢弃。
2. **CI 随时在推**：解读/采集每隔几小时提交一批。push 被拒（non-fast-forward）说明刚有新提交进来，重新 `git fetch` 走情况 2。
3. **push 前看一眼 Actions**：有 run 在排队就等它跑完再推，排队中的 run 拿的是冻结的旧 head_sha，推完必撞。
4. **untracked 不用管**：`state/golden_*.json`、`_remote_sync_*/`、`_purge_backup_*/`、`_tmp_*` 都是本地工作文件，远端没有，不参与同步。

---

## 当前实况（2026-10-03）

本地落后、无分叉，属情况 1，一条命令即可：

```bash
git pull --ff-only origin main
```
