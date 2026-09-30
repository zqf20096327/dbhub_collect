#!/usr/bin/env bash
# interpret_loop.sh —— 服务器 24 小时解读循环（零 GitHub API 消耗）
#
# 每轮：git pull（取 Actions 夜间采集的新 README，git 协议不计配额）
#      → db_scan 刷新库名候选（纯本地）
#      → interpret 解读一批（断点续跑，sha 缓存自动跳过已解读）
#      → git push 回存状态（同样不计配额）
#
# 用法：
#   ./tools/interpret_loop.sh            # 常驻循环（nohup / systemd 用）
#   ./tools/interpret_loop.sh --once     # 只跑一轮（crontab 用）
#   BATCH=1000 ./tools/interpret_loop.sh # 自定义每轮条数
#
# 前置：.env 里配好 AI_API_KEY/AI_BASE_URL/AI_MODEL；git 远程已配好推送凭据
set -u
cd "$(dirname "$0")/.."

BATCH="${BATCH:-500}"          # 每轮最多解读条数
BUDGET="${BUDGET:-50}"         # 每轮解读墙钟预算（分钟）
SLEEP="${SLEEP:-300}"          # 轮间隔（秒）
ONCE="${1:-}"

log() { echo "[$(date '+%F %T')] $*"; }

while :; do
  log "== 轮开始 =="
  # 1) 取新数据（Actions 夜间采集的提交；冲突时以远端为准，本地状态稍后重生成）
  git pull --rebase --autostash 2>/dev/null || log "pull 失败（网络/冲突），用本地数据继续"

  # 2) 刷新库名候选（README 有更新才有必要，幂等全量约 30 秒）
  python interpret/db_scan.py || log "db_scan 失败，沿用旧候选"

  # 3) 解读一批（额度耗尽脚本会自动等窗口；墙钟到点收尾，断点已存）
  python interpret/interpret.py --concurrency 3 \
        --max-items "$BATCH" --max-minutes "$BUDGET" \
    && log "本轮解读完成" || log "interpret 异常退出（下轮自动续）"

  # 4) 回存状态（无变更则跳过）
  git add state/interp_cache.json state/interp_state.json \
          state/db_scan.json state/manual_review.json 2>/dev/null
  if git diff --cached --quiet; then
    log "无新结果（语料待采集补充或额度窗口未恢复）"
  else
    git -c user.name="interpret-bot" \
        -c user.email="interpret-bot@users.noreply.github.com" \
        commit -m "解读批次 $(date -u +%F\ %H:%M)" -q
    git push 2>/dev/null && log "状态已推送" || log "push 失败（下轮重试）"
  fi

  [ "$ONCE" = "--once" ] && { log "== 单轮模式结束 =="; break; }
  log "休眠 ${SLEEP}s 后进入下一轮"
  sleep "$SLEEP"
done
