# -*- coding: utf-8 -*-
"""interp_cache 分片存取层（10-06 切片方案：sha 前 2 位 → 256 桶）。

单文件 interp_cache.json 已 62MB：每改一条整文件重写（还滚三份轮转副本），
git 每次提交一个整 blob 重传，推拉双堵。分片后写盘只动脏桶（~250KB/桶），
git 只传变化的桶，sync_remote_api.py 逐文件拉分片也不再需要 Range 分段。

规则：
- 桶名 = sha256(key) 前 2 位（10-06 加固：曾用 key 前 2 位，desc:: 前缀的
  299 条全挤进 de 桶 3 倍均值；哈希后任何 key 形态均匀落 00-ff）；
  文件 state/interp_cache_shards/<xx>.json。
- 读：分片 ∪ 旧单文件（并集；同 sha 同内容无真冲突，键冲突以分片为准）——
  切换期旧代码进程仍可能写单文件，并集保证不丢单。代价：过渡期"删除"不粘滞
  （单文件里的旧键会被并集读回来）；唯一删条目的 purge 工具已做双写收口。
- 写：只写分片；旧单文件由 tools/split_interp_cache.py --cutover 收口删除。
- 值必须整体替换（cache[k] = obj），不要原地改值的字段——脏桶按 key 追踪，
  原地改动感知不到，flush 时会丢。
- 分片写入不带轮转副本：单桶 250KB 级，轮转只会重演 332MB 副本漏进 git 的旧事。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
SHARD_DIR = STATE / "interp_cache_shards"
LEGACY = STATE / "interp_cache.json"


def _bucket(key: str) -> str:
    # 对 key 整体做 sha 再取前 2 位，而不是取 key 自身前缀：10-06 实测 desc:: 前缀
    # 的 299 条全部挤进 de 桶（3 倍均值）。任何 key 形态（sha、desc::、未来新
    # 前缀）经哈希后前 2 位都均匀取 00-ff。改此函数后必须重跑
    # tools/split_interp_cache.py（save_cache_all 会按新规则重分组并清废桶）。
    return hashlib.sha256(key.encode()).hexdigest()[:2]


def _write_shard(bucket: str, entries: dict) -> None:
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    p = SHARD_DIR / f"{bucket}.json"
    tmp = SHARD_DIR / f"{bucket}.tmp"
    tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def load_cache() -> dict:
    """全量加载：分片 ∪ 旧单文件，键冲突以分片为准。两边都没有返回空 dict。"""
    data: dict = {}
    if LEGACY.is_file():
        data.update(json.loads(LEGACY.read_text(encoding="utf-8")))
    if SHARD_DIR.is_dir():
        for p in sorted(SHARD_DIR.glob("*.json")):
            shard = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(shard, dict):
                raise RuntimeError(f"分片格式损坏（非 dict）：{p}")
            data.update(shard)
    return data


def save_cache_all(cache: dict) -> int:
    """全量落盘（拆分/合并/清理类工具用）：重写全部桶，清掉已无键的桶文件。"""
    buckets: dict[str, dict] = {}
    for k, v in cache.items():
        buckets.setdefault(_bucket(k), {})[k] = v
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    for p in SHARD_DIR.glob("*.json"):
        if p.stem not in buckets:
            p.unlink()
    for b, entries in buckets.items():
        _write_shard(b, entries)
    return len(buckets)


class InterpCacheStore(dict):
    """dict 兼容的分片缓存：改哪个桶，flush() 只重写哪个桶（checkpoint 用）。"""

    def __init__(self):
        super().__init__(load_cache())
        self._dirty: set[str] = set()

    def __setitem__(self, key, value):
        self._dirty.add(_bucket(key))
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self._dirty.add(_bucket(key))
        super().__delitem__(key)

    def update(self, *args, **kwargs):     # dict 原生 update 绕过 __setitem__，手动补
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def pop(self, key, *default):
        if key in self:
            self._dirty.add(_bucket(key))
        return super().pop(key, *default)

    def flush(self) -> int:
        """脏桶落盘；桶被清空则删该桶文件。返回本次写入的桶数。"""
        if not self._dirty:
            return 0
        grouped: dict[str, dict] = {}
        for k, v in self.items():           # 单趟全扫分组，避免逐桶重复扫
            b = _bucket(k)
            if b in self._dirty:
                grouped.setdefault(b, {})[k] = v
        for b in sorted(self._dirty):
            entries = grouped.get(b)
            if entries:
                _write_shard(b, entries)
            else:
                p = SHARD_DIR / f"{b}.json"
                if p.is_file():
                    p.unlink()
        n = len(self._dirty)
        self._dirty.clear()
        return n
