# -*- coding: utf-8 -*-
"""attribution 适配引擎包（ATTRIBUTION_PLAN v1.1）。纯离线：不碰网络、不碰存储。

分层（卡号即建设顺序，词表单一事实源 = config/db_profiles）：
  T1b  dep_match       依赖名匹配（exact/子串两档 + @types 排除 + 子串吸收）
  T1c  vocab           三视图词表派生（readme/dir/dep，消灭三套硬编码）
  T2a  evidence_model/api  六型证据 schema + judge 纯函数判定入口
  T2b  matcher         采集侧指纹 → 证据包（judge 的输入生产者）
  T2c  quorum/rules_ci ≥2 票立案 + 国产兼容协议消歧
"""
from attribution.api import ENGINE_VERSION, judge  # noqa: F401  包级入口：from attribution import judge

