# -*- coding: utf-8 -*-
"""指纹×词表×topic 三规则匹配器（ATTRIBUTION T2b，2026-11-01）。

职责：把证据分片记录（evidence_collect 存 state/evidence_cache_shards 的
schema）+ 池记录（pool.ndjson 单条）翻译成 T2a 六型证据包——judge 的输入
生产者。纯函数、零网络零存储。

指纹 → 证据的翻译规则（票档 = evidence_model.DEFAULT_VOTES；弱路径降 0.5）：
  dep   files[](kind=dep).names/.dev → dep_match（普通 1 票；dev 0.5）
  image files[](kind=image).images   → 镜像段匹配（2 票；弱路径 0.5）
  ci    files[](kind=ci).images      → 同上但矩阵语境一律 0.5 票
  tree  clues.paths                  → 路径段匹配 dir_vocab（2 票；弱路径 0.5）
  topic pool_rec.topics              → 专有名才算（1 票）
  rel_notes 无数据源不产（T5b 前占位，见 T2a）

票的粒度 = 一个来源文件 × 一个库 = 1 条证据（pom 里 5 个 mysql 构件只算
一条依赖信号，命中词全部进 detail.words——票数反映证据不反映词数）。

topic 三规则（方案 §4.5）：
  1 专有名才算：topic 归一（去 -/_/空格、lower）命中库档案 name/aliases/topics
    通道词（sqlite3 这类只有 topic 语境成立的词从 topics 字段来）
  2 泛词不算：database/sql/rdbms/dbms（4,982 仓排除口径）
  3 矛盾=互补：topic 库在指纹里无同库命中 → detail.complementary=True +
    meta.topic_complement 列表——不判冲突不丢弃，复核归 T2c/人

防御（防坑落地）：只消费 status=ok 记录（方案 §7）；sha_mismatch/
parse_error/error 的文件跳过；分片键形态不一直接用 rec["fn"]。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.dep_match import match_dep
from attribution.evidence_model import DEFAULT_VOTES
from attribution.vocab import dir_vocab

# 泛词 topic 一律不算证据（方案 §4.5 规则 2；4,982 仓实测排除口径）
GENERIC_TOPICS = frozenset({"database", "sql", "rdbms", "dbms"})

# 弱路径（sqlc 先例：testdata 里的连接器路径不是核心支持）——命中降 0.5 票。
# 词边界：前后必须是段首/段尾或 - _ . 分隔，防 latest/attest 误中 test。
WEAK_PATH_RE = re.compile(
    r"(^|[/\-_])(testdata|tests?|examples?|fixtures?|benchmarks?|benches|bench"
    r"|demos?|samples?)([/\-_.]|$)", re.IGNORECASE)

_RE_REGEX_META = re.compile(r"[\\()\[\]{}*+?|^$]")


def _norm_topic(s: str) -> str:
    """topic 归一：lower + 去 -/_/空格（sql-server/sql_server/sqlserver 同一）。"""
    return re.sub(r"[-_ ]+", "", (s or "").strip().lower())


def _topic_view() -> dict[str, str]:
    """归一 topic 词 → 库名。词源 = 档案 name + 纯词 aliases + topics 通道词。"""
    from config.db_profiles import PROFILES
    view: dict[str, str] = {}
    for p in PROFILES:
        if not p.get("enabled", True):
            continue
        # topics 项两种形态：纯串 或 {"name","known_empty"} 声明性空档
        raw_topics = [t["name"] if isinstance(t, dict) else t
                      for t in (p.get("topics") or []) if isinstance(t, (str, dict))]
        words = [p["name"]] + list(p.get("aliases") or []) + [
            t for t in raw_topics if isinstance(t, str)]
        for w in words:
            if _RE_REGEX_META.search(w):          # 正则型 alias 不进纯词表
                continue
            n = _norm_topic(w)
            if n and n not in GENERIC_TOPICS and n not in view:
                view[n] = p["name"]
    return view


_TOPIC_VIEW = _topic_view()


def match_topic(topic: str) -> str | None:
    """单个 topic → 库名；泛词/未知名 → None。"""
    n = _norm_topic(topic)
    if not n or n in GENERIC_TOPICS:
        return None
    return _TOPIC_VIEW.get(n)


def _image_repo(image: str) -> list[str]:
    """镜像串 → repo 路径段：剥 tag/digest、lower。postgres:15→[postgres]；
    mcr.microsoft.com/mssql/server:2019→[mcr.microsoft.com,mssql,server]。"""
    repo = (image or "").strip().lower().split("@")[0].split(":")[0]
    return [seg for seg in repo.split("/") if seg]


def match_image(image: str) -> list[dict]:
    """镜像串 → [{db, word}]。段级匹配：词的段序列须在 repo 段中连续出现
    （postgres 不会撞 postgresml；mssql 命中 mcr.microsoft.com/mssql/server）。"""
    from config.db_profiles import PROFILES
    segs = _image_repo(image)
    if not segs:
        return []
    hits: list[dict] = []
    for p in PROFILES:
        if not p.get("enabled", True):
            continue
        for w in p.get("images") or []:
            wsegs = [s.lower() for s in w.split("/")]
            n = len(wsegs)
            if any(segs[i:i + n] == wsegs for i in range(len(segs) - n + 1)):
                hits.append({"db": p["name"], "word": w})
    return hits


def match_path(path: str) -> list[dict]:
    """路径 → [{db, token}]（dir_vocab 视图）。段级边界匹配：token=整段，
    或段前缀且下一字符为数字/-/_/.（psycopg 命中 psycopg2，oracle 不撞
    oraclelinux）。"""
    segs = [s.lower() for s in (path or "").replace("\\", "/").split("/")]
    hits: list[dict] = []
    for db, tokens in dir_vocab().items():
        for tok in tokens:
            t = tok.lower()
            for seg in segs:
                if seg == t or (seg.startswith(t) and len(seg) > len(t)
                                and seg[len(t)] in "0123456789-_."):
                    hits.append({"db": db, "token": tok})
                    break
    return hits


def is_weak_path(path: str) -> bool:
    return bool(WEAK_PATH_RE.search(path or ""))


def _floor_weak(votes: float, path: str) -> float:
    return 0.5 if is_weak_path(path) else votes


def build_pack(fn: str, evidence_rec: dict | None = None,
               pool_rec: dict | None = None, *, collected_at: str | None = None) -> dict:
    """证据分片记录 + 池记录 → T2a 证据包（normalize_pack 可过、judge 可吃）。

    evidence_rec 非 ok 状态/缺文件 → 只产 topic 证据；两者皆无 → 空包（fn 保留，
    结论 no_evidence——43 个 recheck 活案例中 42 个历史出池仓正是此路径）。
    collected_at 决策序：参数 > 分片记录；有证据条目但两者皆无 → ValueError。
    """
    fn = (fn or (evidence_rec or {}).get("fn") or "").strip()
    rec_ok = bool(evidence_rec) and evidence_rec.get("status") == "ok"
    ts = collected_at or (evidence_rec or {}).get("collected_at")

    evidences: list[dict] = []
    fp_dbs: set[str] = set()          # 指纹（dep/tree/image/ci）命中的库

    def _add(kind: str, db: str, votes: float, source: str, detail: dict) -> None:
        evidences.append({"kind": kind, "db": db, "votes": votes,
                          "source": source, "collected_at": ts, "detail": detail})
        fp_dbs.add(db)

    if rec_ok:
        for f in evidence_rec.get("files") or []:
            path = f.get("path") or ""
            if f.get("sha_mismatch") or f.get("parse_error") or f.get("error"):
                continue                       # 分支漂移/畸形清单/拉取失败：跳过
            kind = f.get("kind")
            if kind == "dep":
                per_db: dict[str, dict] = {}   # db → {main/dev 命中词}（一文件一库一条）
                for names, bucket in ((f.get("names") or [], "main"),
                                      (f.get("dev") or [], "dev")):
                    for n in names:
                        for h in match_dep(n, dev=(bucket == "dev")):
                            e = per_db.setdefault(h["db"], {"main": [], "dev": []})
                            if h["word"] not in e[bucket]:
                                e[bucket].append(h["word"])
                for db, e in sorted(per_db.items()):
                    weak = is_weak_path(path)
                    dev_only = not e["main"]            # 只有 devDeps 命中才算降档
                    votes = 0.5 if (weak or dev_only) else DEFAULT_VOTES["dep"]
                    det = {"words": (e["main"] or e["dev"])[:3]}
                    if weak:
                        det["weak_path"] = True
                    if dev_only:
                        det["dev"] = True
                    _add("dep", db, votes, path, det)
            elif kind in ("image", "ci"):
                per_db = {}
                for img in f.get("images") or []:
                    for h in match_image(img):
                        if h["word"] not in per_db.setdefault(h["db"], []):
                            per_db[h["db"]].append(h["word"])
                for db, words in sorted(per_db.items()):
                    if kind == "ci":
                        votes = DEFAULT_VOTES["ci"]     # 矩阵语境一律弱档
                        det = {"words": words[:3]}
                    else:
                        votes = _floor_weak(DEFAULT_VOTES["image"], path)
                        det = {"words": words[:3]}
                        if votes != DEFAULT_VOTES["image"]:
                            det["weak_path"] = True
                    _add(kind, db, votes, path, det)
        for p in (evidence_rec.get("clues") or {}).get("paths") or []:
            per_db = {}
            for h in match_path(p):
                if h["token"] not in per_db.setdefault(h["db"], []):
                    per_db[h["db"]].append(h["token"])
            for db, tokens in sorted(per_db.items()):
                weak = is_weak_path(p)
                det = {"words": tokens[:3]}
                if weak:
                    det["weak_path"] = True
                _add("tree", db, 0.5 if weak else DEFAULT_VOTES["tree"], p, det)

    complement: list[str] = []
    for t in ((pool_rec or {}).get("topics") or []):
        db = match_topic(t)
        if not db:
            continue
        det: dict = {}
        if db not in fp_dbs:                   # 规则 3：矛盾=互补，不判冲突
            det["complementary"] = True
            if db not in complement:
                complement.append(db)
        evidences.append({"kind": "topic", "db": db, "votes": DEFAULT_VOTES["topic"],
                          "source": f"topic:{t}", "collected_at": ts, "detail": det})

    if evidences and not ts:
        raise ValueError(f"{fn}: 有证据条目但无采集时间（collected_at 缺失）")

    meta: dict = {}
    stars = (pool_rec or {}).get("stars", (evidence_rec or {}).get("stars"))
    if stars is not None:
        meta["stars"] = stars
    if evidence_rec:
        meta["evidence_status"] = evidence_rec.get("status")
    if complement:
        meta["topic_complement"] = complement
    return {"fn": fn, "evidences": evidences, "meta": meta}
