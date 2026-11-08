# -*- coding: utf-8 -*-
"""分层存储（工作清单 G1-6）：四层各自一个目录，分片、断点、超时机制同一套。

用户裁定（1107）：
  ① 分片内容尽量解耦——每层只存自己的字段；
  ② 后面通过程序拼接——读时用 sha 把四层拼起来，不做冗余拷贝。

目录（root 默认 state/interp/<layer>/）：
  <root>/shards/<xx>.json   256 桶，桶名 = sha256(key)[:2]，与旧缓存同规则
  <root>/state.json         本层断点台账：fn → {sha, status, at}
  <root>/runlog/            本层条目级日志（gitignored）

层规格（payload 之外的字段一律视为元信息；`fn` 不进条目——fn→sha 由台账负责，
内容 sha 镜像时一个条目服务多个仓，条目本身不该属于某个 fn）：

| layer        | payload                                  | 键            |
|--------------|------------------------------------------|---------------|
| judge        | classification, signals, audit           | 裸 sha        |
| text         | identity                                 | 裸 sha        |
| domain_tags  | tags, abstain, gap                       | 裸 sha        |
| desc         | identity, classification（轻）           | desc::<12位>  |

共性机制（各层共用本模块，不各写一套）：
  - 脏桶增量落盘：改哪个桶只重写哪个桶（同 interp_store 的 checkpoint 语义）
  - 断点续跑：state.json 记 fn→sha+status，pending() 只返回缺的/内容变了的
  - 超时/重试/额度等待：由 runner 骨架统一处理，本模块只负责存取

用法：
  from interp_layer_store import LayerStore, join, LAYERS
  st = LayerStore("judge")
  st.items[sha] = obj; st.flush()
  st.mark(fn, sha, "done"); st.save_state()
  rec = join(sha, {l: LayerStore(l) for l in LAYERS})
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from gh import atomic_write_json   # noqa: E402

LAYER_ROOT = ROOT / "state" / "interp"

# 每层只允许这些载荷字段（解耦红线）；其余只保留 META
SPECS = {
    "judge": {"payload": ("classification", "signals", "audit"), "key": "sha"},
    "text": {"payload": ("identity",), "key": "sha"},
    "domain_tags": {"payload": ("tags", "abstain", "gap"), "key": "sha"},
    "desc": {"payload": ("identity", "classification"), "key": "desc"},
}
LAYERS = tuple(SPECS)
# 条目级元信息：出身/时间/来源，四层共用的最小集合
# （confidence 供 desc 层标层常量 low；判定卷的 confidence 在 audit 里，不冲突）
META = ("sha", "source", "generated_at", "prompt_ver", "model", "ver",
        "clean_ver", "layer", "confidence")
STATUSES = ("done", "rejected", "failed", "skipped")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bucket(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()[:2]


def validate_key(layer: str, key: str) -> str:
    """层内键校验：judge/text/domain_tags 是裸 sha，desc 是 desc::<12位摘要>。"""
    if layer not in SPECS:
        raise ValueError(f"未知层 {layer}；允许 {LAYERS}")
    if not isinstance(key, str) or not key:
        raise ValueError("空键")
    if layer == "desc":
        if not key.startswith("desc::") or len(key) != len("desc::") + 12:
            raise ValueError(f"desc 键须 desc::<12位摘要>：{key[:40]}")
        if any(c not in "0123456789abcdef" for c in key[6:]):
            raise ValueError(f"desc 摘要须十六进制：{key[:40]}")
        return key
    if key.startswith("desc::") or "#" in key:
        raise ValueError(f"{layer} 键须裸 sha（层由目录表达）：{key[:40]}")
    return key


def sanitize(layer: str, obj: dict) -> tuple[dict, list[str]]:
    """解耦：只留本层 payload + META，其余字段丢弃并上报字段名。

    `fn` 刻意不在 META：条目按内容 sha 存，镜像仓共用一个条目；fn→sha 在台账。
    classification 里若混入别的层字段（如文本卷带了 classification），整块丢弃。
    """
    if not isinstance(obj, dict):
        raise ValueError("条目必须是 dict")
    payload = set(SPECS[layer]["payload"])
    out, dropped = {}, []
    for k, v in obj.items():
        if k in payload or k in META:
            out[k] = v
        else:
            dropped.append(k)
    return out, dropped


class LayerStore:
    """一层一个 store。dict 式读写 + 脏桶落盘 + 断点台账。"""

    def __init__(self, layer: str, base: Path | None = None):
        """base 是父目录，实际根 = base/<layer>；默认 state/interp/<layer>。

        必须按层再套一层子目录：若直接共用 base，四层会读同一个 shards/，
        拼接时会把判定卷条目当成 desc 条目（自检第一版就是这么抓到的）。
        """
        if layer not in SPECS:
            raise ValueError(f"未知层 {layer}；允许 {LAYERS}")
        self.layer = layer
        self.root = ((Path(base) if base else LAYER_ROOT) / layer)
        self.shard_dir = self.root / "shards"
        self.state_path = self.root / "state.json"
        self.runlog_dir = self.root / "runlog"
        self.items: dict[str, dict] = {}
        self._dirty: set[str] = set()
        self._state: dict[str, dict] | None = None
        self.dropped: dict[str, int] = {}       # 字段解耦丢弃计数（体检用）

    # ---- 分片 ----

    def load(self) -> dict[str, dict]:
        self.items = {}
        if self.shard_dir.is_dir():
            for p in sorted(self.shard_dir.glob("*.json")):
                shard = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(shard, dict):
                    raise RuntimeError(f"分片格式损坏（非 dict）：{p}")
                self.items.update(shard)
        self._dirty.clear()
        return self.items

    def put(self, key: str, obj: dict) -> dict:
        """写入并自动解耦（丢 fn/跨层字段）。返回实际落盘的条目。"""
        validate_key(self.layer, key)
        clean, dropped = sanitize(self.layer, obj)
        for f in dropped:
            self.dropped[f] = self.dropped.get(f, 0) + 1
        clean.setdefault("sha", key)
        self.items[key] = clean
        self._dirty.add(bucket(key))
        return clean

    def get(self, key: str) -> dict | None:
        return self.items.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self.items

    def flush(self) -> int:
        """脏桶落盘（只重写脏桶；桶空则删文件）。返回写入桶数。"""
        if not self._dirty:
            return 0
        grouped: dict[str, dict] = {}
        for k, v in self.items.items():
            b = bucket(k)
            if b in self._dirty:
                grouped.setdefault(b, {})[k] = v
        self.shard_dir.mkdir(parents=True, exist_ok=True)
        for b in sorted(self._dirty):
            entries = grouped.get(b)
            p = self.shard_dir / f"{b}.json"
            if entries:
                tmp = p.with_suffix(".tmp")
                tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1),
                               encoding="utf-8")
                tmp.replace(p)
            elif p.is_file():
                p.unlink()
        n = len(self._dirty)
        self._dirty.clear()
        return n

    # ---- 断点台账 ----

    def state(self) -> dict[str, dict]:
        if self._state is None:
            if self.state_path.is_file():
                d = json.loads(self.state_path.read_text(encoding="utf-8"))
                self._state = d.get("items") or {}
            else:
                self._state = {}
        return self._state

    def mark(self, fn: str, sha: str, status: str = "done", **extra) -> None:
        if status not in STATUSES:
            raise ValueError(f"未知状态 {status}；允许 {STATUSES}")
        self.state()[fn] = {"sha": sha, "status": status, "at": _now(), **extra}

    def save_state(self, extra: dict | None = None) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        atomic_write_json(self.state_path, {
            "schema": 1, "layer": self.layer, "updated_at": _now(),
            "counts": self._counts(), "items": self.state(), **(extra or {}),
        })

    def _counts(self) -> dict:
        c: dict[str, int] = {}
        for v in self.state().values():
            s = v.get("status") or "unknown"
            c[s] = c.get(s, 0) + 1
        return c

    def pending(self, pairs) -> list[tuple[str, str]]:
        """断点续跑：返回还没做/内容变了的 (fn, sha)。pairs=[(fn, sha), ...]"""
        st = self.state()
        out = []
        for fn, sha in pairs:
            rec = st.get(fn)
            if not rec or rec.get("sha") != sha or rec.get("status") != "done":
                out.append((fn, sha))
        return out

    # ---- 条目级日志 ----

    def log(self, rec: dict) -> None:
        self.runlog_dir.mkdir(parents=True, exist_ok=True)
        p = self.runlog_dir / f"{self.layer}-{datetime.now(timezone.utc):%Y%m%d}.jsonl"
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def join(sha: str, stores: dict[str, LayerStore]) -> dict:
    """程序拼接：按 sha 把各层载荷拼成一条记录（不做字段复制）。"""
    rec = {"sha": sha}
    for layer in LAYERS:
        st = stores.get(layer)
        if st is None:
            continue
        obj = st.get(sha)
        if obj is not None:
            rec[layer] = obj
    return rec


def _selftest() -> int:
    import tempfile
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        st = LayerStore("judge", root)
        st.load()
        # 1) 分片轮转
        for i in range(1000):
            st.put(f"{i:064x}", {"classification": {"cat_primary": "开发库"},
                                 "signals": {}, "audit": {}, "fn": f"a/r{i}"})
        nb = st.flush()
        nf = len(list(st.shard_dir.glob("*.json")))
        chk(f"1000 条写入后桶数合理（{nb} 桶 / {nf} 文件）", 240 <= nb == nf <= 256)
        chk("解耦丢弃 fn", "fn" not in st.get(f"{0:064x}"))
        chk("丢弃计数可见", st.dropped.get("fn") == 1000)
        chk("重载内容一致", LayerStore("judge", root).load() == st.items)
        # 2) 脏桶增量
        before = {p.name: p.stat().st_mtime_ns for p in st.shard_dir.glob("*.json")}
        st.put(f"{0:064x}", {"classification": {"cat_primary": "监控"}})
        chk("单条改动只落 1 桶", st.flush() == 1)
        after = {p.name: p.stat().st_mtime_ns for p in st.shard_dir.glob("*.json")}
        changed = [k for k in after if after[k] != before.get(k)]
        chk("未触碰的桶文件未重写", len(changed) == 1)
        # 3) 断点台账
        st.mark("a/x", "s1", "done")
        st.mark("a/y", "s2", "rejected", detail="schema")
        chk("pending 只返回缺的/变了的",
            st.pending([("a/x", "s1"), ("a/y", "s2"), ("a/z", "s3"),
                        ("a/x", "s9")]) == [("a/y", "s2"), ("a/z", "s3"), ("a/x", "s9")])
        st.save_state({"prompt_ver": "4.0"})
        re = LayerStore("judge", root)
        chk("台账重载保留状态与计数",
            re.state()["a/y"]["status"] == "rejected"
            and re.state()["a/x"]["status"] == "done")
        # 4) 解耦红线：跨层字段被丢
        t = LayerStore("text", root)
        t.load()
        got = t.put(f"{1:064x}", {"identity": {"one_liner": "x"},
                                  "classification": {"cat_primary": "开发库"},
                                  "fn": "a/r1"})
        chk("文本层只留 identity", set(got) == {"sha", "identity"})
        chk("文本层丢弃 classification", t.dropped.get("classification") == 1)
        # 5) 键规则
        for bad_layer, bad_key in (("judge", "abc#v4"), ("text", "desc::abcdef123456"),
                                   ("desc", f"{0:064x}"), ("desc", "desc::XYZ")):
            try:
                validate_key(bad_layer, bad_key)
                chk(f"非法键被拒 {bad_layer}/{bad_key[:12]}", False)
            except ValueError:
                chk(f"非法键被拒 {bad_layer}/{bad_key[:12]}", True)
        chk("desc 合法键通过",
            validate_key("desc", "desc::abcdef123456") == "desc::abcdef123456")
        try:
            LayerStore("bogus", root)
            chk("未知层被拒", False)
        except ValueError:
            chk("未知层被拒", True)
        # 6) 程序拼接
        stores = {l: LayerStore(l, root) for l in LAYERS}
        sha = f"{2:064x}"
        stores["judge"].load(); stores["text"].load()
        stores["domain_tags"].load(); stores["desc"].load()
        stores["judge"].put(sha, {"classification": {"cat_primary": "开发库"}})
        stores["text"].put(sha, {"identity": {"one_liner": "一句话"}})
        stores["domain_tags"].put(sha, {"tags": [{"slug": "cdc", "line": 3}],
                                        "abstain": None})
        rec = join(sha, stores)
        chk("四层按 sha 拼成一条", set(rec) == {"sha", "judge", "text", "domain_tags"})
        chk("拼接不复制字段", rec["judge"]["classification"]["cat_primary"] == "开发库"
            and rec["text"]["identity"]["one_liner"] == "一句话")
        # 7) 条目日志
        stores["judge"].log({"fn": "a/r0", "sha": sha, "ok": True})
        logs = list(stores["judge"].runlog_dir.glob("*.jsonl"))
        chk("条目日志可写", len(logs) == 1 and "a/r0" in logs[0].read_text(encoding="utf-8"))

    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    print(__doc__)
