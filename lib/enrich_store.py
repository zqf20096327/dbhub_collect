# -*- coding: utf-8 -*-
"""enrich_cache 分片存取层（三期，10-09：sha256(fn) 前 2 位 → 256 桶）。

单文件 enrich_cache.json 已 11.8MB：enrich 每晚 checkpoint/收尾整文件重写
（还滚轮转副本），git 每次提交一个整 blob 重传；head 层 security 30 天轮转
10 月底开闸后 cache 每晚必变，届时每晚一个 11.8MB blob。分片后写盘只动脏桶
（~46KB/桶），git 只传变化的桶。规则与 lib/interp_store.py 同源（10-06
interp_cache 切片方案），两处差异：

- 值是"原地合并"语义：enrich.collect_dims 用 sig.update 原地改字段
  （security-only 刷新保留旧 commit_7d/rel_ver 等），dict 子类的脏桶追踪
  看不见原地改——采集每个目标前必须显式 store.touch(fn)，忘掉即静默丢数据。
- state_dir 可选参数：purge_outpool --root 沙箱需要重定向读取位置。

规则：
- 桶名 = sha256(key) 前 2 位，文件 state/enrich_cache_shards/<xx>.json。
- 读：分片 ∪ 旧单文件（并集；键冲突以分片为准）——切换期旧代码进程仍可能写
  单文件，并集保证不丢单。旧单文件由 tools/split_enrich_cache.py --cutover
  收口删除（同一提交里同步删 enrich.py 的过渡期双写）。
- 写：只写分片；不带轮转副本（46KB 级，轮转重演副本漏进 git 旧事）。
- save_cache_all 会按桶规则重分组并清废桶——改 _bucket 后必须重跑
  tools/split_enrich_cache.py。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
SHARD_DIR = STATE / "enrich_cache_shards"
LEGACY = STATE / "enrich_cache.json"


def _bucket(key: str) -> str:
    # 对 key 整体做 sha 再取前 2 位（与 interp_store 同规则）：fn 形态虽本身
    # 均匀，统一走哈希防未来 key 形态漂移（前缀类 key 挤爆个别桶）。
    return hashlib.sha256(key.encode()).hexdigest()[:2]


def _shard_dir(state_dir: Path | None) -> Path:
    return (Path(state_dir) if state_dir else STATE) / "enrich_cache_shards"


def _legacy_path(state_dir: Path | None) -> Path:
    return (Path(state_dir) if state_dir else STATE) / "enrich_cache.json"


def _write_shard(bucket: str, entries: dict, state_dir: Path | None = None) -> None:
    d = _shard_dir(state_dir)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{bucket}.json"
    tmp = d / f"{bucket}.tmp"
    tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def load_cache(state_dir: Path | None = None) -> dict:
    """全量加载：分片 ∪ 旧单文件，键冲突以分片为准。两边都没有返回空 dict。"""
    data: dict = {}
    legacy = _legacy_path(state_dir)
    if legacy.is_file():
        data.update(json.loads(legacy.read_text(encoding="utf-8")))
    sdir = _shard_dir(state_dir)
    if sdir.is_dir():
        for p in sorted(sdir.glob("*.json")):
            shard = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(shard, dict):
                raise RuntimeError(f"分片格式损坏（非 dict）：{p}")
            data.update(shard)
    return data


def save_cache_all(cache: dict, state_dir: Path | None = None) -> int:
    """全量落盘（拆分/合并/清理类工具用）：重写全部桶，清掉已无键的桶文件。"""
    buckets: dict[str, dict] = {}
    for k, v in cache.items():
        buckets.setdefault(_bucket(k), {})[k] = v
    sdir = _shard_dir(state_dir)
    sdir.mkdir(parents=True, exist_ok=True)
    for p in sdir.glob("*.json"):
        if p.stem not in buckets:
            p.unlink()
    for b, entries in buckets.items():
        _write_shard(b, entries, state_dir)
    return len(buckets)


class EnrichCacheStore(dict):
    """dict 兼容的分片缓存：改哪个桶，flush() 只重写哪个桶（checkpoint 用）。

    值字段是原地 update 语义（collect_dims 的 sig.update），__setitem__
    追踪不到——采集前必须显式 touch(fn)。
    """

    def __init__(self, state_dir: Path | None = None):
        super().__init__(load_cache(state_dir))
        self._state_dir = state_dir
        self._dirty: set[str] = set()

    def touch(self, key) -> None:
        """显式标脏（原地改值字段前调用；值整体替换走 __setitem__ 自动标脏）。"""
        self._dirty.add(_bucket(key))

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
                _write_shard(b, entries, self._state_dir)
            else:
                p = _shard_dir(self._state_dir) / f"{b}.json"
                if p.is_file():
                    p.unlink()
        n = len(self._dirty)
        self._dirty.clear()
        return n
