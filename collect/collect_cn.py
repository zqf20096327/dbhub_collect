# -*- coding: utf-8 -*-
"""国产 10 库候选池采集入口（策略：db_profiles.GLOBAL["sections"]["cn"]）。

  国产不设星：topic/keyword 查询无星限定（生态总量小、星分布低，自标签与专属
  org 即信号）；查询超 1000 结果纯按创建年→月拆（不套星档，防拆档路径隐性加星线）。
  无新项目窗口：主通道无星线，新仓从第 0 天起即被覆盖。
  org 分级：dedicated（pingcap/tikv/tidb-samples/tidb-incubator/oceanbase/polardb/
  opengauss-mirror/yashan-technologies）无星线；cloud（huaweicloud/tencentcloud/
  ApsaraDB，云厂商超集 org 含大量非数据库 SDK）>=10 当范围噪音闸。
用法：
  python collect_cn.py                   # 全流程（断点续采）
  python collect_cn.py --dry-run
共享实现见 pool_core.py。
"""
import sys as _sys
from pathlib import Path

_sys.path.insert(0, str(Path(__file__).resolve().parent))
from pool_core import run_main  # noqa: E402

if __name__ == "__main__":
    run_main("cn")
