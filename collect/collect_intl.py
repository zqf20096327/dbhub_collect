# -*- coding: utf-8 -*-
"""国际 7 库候选池采集入口（策略：db_profiles.GLOBAL["sections"]["intl"]）。

  topic/keyword 带 stars:>=10；大 topic 星三档→年→月拆；新项目窗口 stars:>=3
  created:>=45天前（最易腐烂，当晚最先跑，结果并入同通道 parts）。
用法：
  python collect_intl.py                 # 全流程（预算内跑多少算多少，断点续采）
  python collect_intl.py --only new      # 只跑新项目窗口
  python collect_intl.py --dry-run
共享实现见 pool_core.py。
"""
import sys as _sys
from pathlib import Path

_sys.path.insert(0, str(Path(__file__).resolve().parent))
from pool_core import run_main  # noqa: E402

if __name__ == "__main__":
    run_main("intl")
