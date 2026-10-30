# -*- coding: utf-8 -*-
"""证据层缓存：fn → 证据记录，256 分片（interp_store / enrich_store 三胞胎之三）。

与两个兄长同规：
  - 分片 = sha256(key)[:2] → state/evidence_cache_shards/<xx>.json（00-ff 共 256 片）
  - 单分片 = 一个 JSON dict，ensure_ascii=False + indent=1，tmp+replace 原子写
  - 值整体替换（无原地 merge 需求，InterpStore 模式），flush() 只回写脏桶

差异（有意为之）：
  - 分片写出带 newline="\n"——Windows 本地跑也必须与 CI(Linux) 同为 LF，
    否则整片 CRLF 翻转产生全文件假 diff（atomic_write_json 的 10-10 教训）
  - 无旧单文件遗留，不需要 LEGACY 合并逻辑

改动 _bucket 必须与 interp_store 同步改并重跑迁移工具（见其注释）。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARD_DIR = ROOT / "state" / "evidence_cache_shards"


def _bucket(key: str) -> str:
    # 与 interp_store._bucket 同款：整体 sha 取前 2 位，任何 key 形态都均匀落 00-ff
    return hashlib.sha256(key.encode()).hexdigest()[:2]


def _write_shard(bucket: str, entries: dict) -> None:
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    p = SHARD_DIR / f"{bucket}.json"
    tmp = SHARD_DIR / f"{bucket}.tmp"
    tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    tmp.replace(p)


def load_cache() -> dict:
    """全量加载所有分片为一个 dict。无分片目录返回空 dict。"""
    data: dict = {}
    if SHARD_DIR.is_dir():
        for p in sorted(SHARD_DIR.glob("*.json")):
            shard = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(shard, dict):
                raise RuntimeError(f"分片格式损坏（非 dict）：{p}")
            data.update(shard)
    return data


class EvidenceCacheStore(dict):
    """dict 子类：写路径标脏桶；flush() 只回写脏桶。值必须整体替换。

    初始数据经 C 层 dict 构造灌入，不触发 __setitem__（初始即干净）。
    """

    def __init__(self, data: dict | None = None):
        self._dirty: set[str] = set()
        super().__init__(data or {})

    def _touch(self, key: str) -> None:
        self._dirty.add(_bucket(key))

    def __setitem__(self, key: str, value) -> None:
        super().__setitem__(key, value)
        self._touch(key)

    def __delitem__(self, key) -> None:
        super().__delitem__(key)
        self._touch(key)

    def update(self, *args, **kwargs) -> None:  # type: ignore[override]
        super().update(*args, **kwargs)
        for k in dict(*args, **kwargs):
            self._touch(k)

    def setdefault(self, key, default=None):  # type: ignore[override]
        if key not in self:
            self._touch(key)
        return super().setdefault(key, default)

    def pop(self, key, *args):  # type: ignore[override]
        if key in self:
            self._touch(key)
        return super().pop(key, *args)

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
