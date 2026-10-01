#!/usr/bin/env bash
# run_overnight.sh —— 过夜量产守护：循环跑到指定时刻或待解读清零。
# 用法：bash deploy/run_overnight.sh [结束时刻，默认 08:00]
#      tmux new -s interp 'bash deploy/run_overnight.sh 08:00'
# 停止：touch state/STOP（下一轮退出）；或 tmux kill-session -t interp
set -u
cd "$(dirname "$0")/.."
END_AT="${1:-08:00}"
END=$(date -d "$END_AT" +%s)
# 过夜场景：此刻已过 END_AT（如 23 点启动跑到 08:00）→ 目标是明早，加一天
[ "$END" -le "$(date +%s)" ] && END=$((END + 86400))
PY="${PY:-python3}"          # CentOS7 等 python3 过旧时：PY=/opt/miniconda3/bin/python3 bash ...
mkdir -p state/logs
"$PY" -c "import requests" 2>/dev/null || { echo "缺少 requests：先执行 $PY -m pip install requests"; exit 1; }
"$PY" -c "import sys; assert sys.version_info >= (3,8), '需要 Python 3.8+'; print('PY OK', sys.version.split()[0])"
echo "==== 过夜开始 $(date) · 计划跑到 $(date -d @$END '+%F %T') === PY=$PY ==="

while [ "$(date +%s)" -lt "$END" ]; do
  [ -f state/STOP ] && { echo "收到 STOP，退出"; break; }
  "$PY" interpret/interpret.py \
      --concurrency "${CONC:-6}" \
      --max-items 4000 \
      --max-minutes 200 \
      --retry-rejected \
      >> state/logs/overnight.log 2>&1
  rc=$?
  echo "[$(date +%H:%M)] 一轮结束 rc=$rc，日志尾部："
  tail -3 state/logs/overnight.log
  # 待解读清零 → 收工（再跑也只是空转）
  tail -50 state/logs/overnight.log | grep -q "待解读 0 项" && { echo "待解读清零，收工"; break; }
  # rc 异常（网络/额度断档）退避 2 分钟再战，别让一夜白等
  [ "$rc" -ne 0 ] && sleep 120 || sleep 20
done
echo "==== 过夜结束 $(date) ===="
"$PY" interpret/log_report.py
