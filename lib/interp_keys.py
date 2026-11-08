# -*- coding: utf-8 -*-
"""层键规则（工作清单 G1-1）：一代解析的键契约，读写两侧唯一口径。

为什么单独一个模块：缓存里同时躺着 v3 裸 sha、v4 判定、v4t 文本、vc1.0 词控、
desc 降级五种键，读层各自拼字符串就会重演"单槽读取互相遮蔽"的事故（v4/v4t
同 fn 只有一条能活到今天）。这里把拼键、解键、认形态集中成一张表。

键契约（冻结，改动即作废存量，必须走 prompt_ver 升级）：

| 层       | 键                          | 载荷形态 | 说明 |
|----------|-----------------------------|----------|------|
| judge    | <sha>#v4                    | v4       | 后缀是字面量 v4，**不等于** prompt_ver 4.0；见下方注释 |
| text     | <sha>#txt4.0                | text     | 后缀随 PROMPT_VER_TEXT 升级 |
| vocab    | <sha>#vc1.0                 | vocab    | 独立词表版本 |
| legacy   | <sha>                       | v3       | 旧代，G7 删除 |
| desc     | desc::<sha1(fn+desc)[:12]>  | desc     | 新方案（G3）；旧键 desc::<description> 数字更少 |
| desc旧   | desc::<description>[#v4]    | v3       | 会碰撞（最多 97 仓共用一条），G3 退役 |

判定后缀为什么是 `#v4` 而不是 `#v4.0`：interpret.cache_key 从落地起就写死
`#v4`，与 PROMPT_VER_V4="4.0" 解耦。要改必须同时迁 32k 条存量（见另册 P1-2），
本模块只如实描述现状，并由检查器对拍代码产出。

形态识别是必需的安全阀：实测 962 条 `desc::…#v4` 里装的是 v3 内容（带 identity
+ 旧 classification，无 cat_primary）。按键取到不等于层里有货，读层必须校验
形态后再采信。

用法：
  from interp_keys import judge_key, text_key, vocab_key, desc_key, parse_key, entry_shape
  parse_key("abc123#v4")      -> ("judge", "abc123")
  entry_shape(obj)            -> "v4" | "v3" | "text" | "vocab" | "desc" | "other" | "bad"
"""
from __future__ import annotations

import hashlib
import re

# ---- 版本常量（与 interpret/vocab_control 同值；由 check_layer_keys 对拍，勿单改）----
JUDGE_KEY_SUFFIX = "#v4"         # interpret.cache_key 写死字面量，随代码而非 prompt_ver
PROMPT_VER_TEXT = "4.0"          # interpret.PROMPT_VER_TEXT
VOCAB_PROMPT_VER = "vc1.0"       # vocab_control.VOCAB_PROMPT_VER
TEXT_KEY_SUFFIX = "#txt" + PROMPT_VER_TEXT
VOCAB_KEY_SUFFIX = "#" + VOCAB_PROMPT_VER

DESC_PREFIX = "desc::"
DESC_DIGEST_LEN = 12             # desc::{sha1(fn+desc)[:12]}
_SHA_RE = re.compile(r"^[0-9a-f]{6,64}$")
_DIGEST_RE = re.compile(r"^[0-9a-f]{%d}$" % DESC_DIGEST_LEN)

LAYERS = ("judge", "text", "vocab", "legacy", "desc", "desc_legacy")
# 每层接受的载荷形态（"desc" 层是 G3 新方案，轻判定+轻介绍的载荷按 v3/v4 子集放行）
ACCEPTS = {
    "judge": ("v4",),
    "text": ("text",),
    "vocab": ("vocab",),
    "legacy": ("v3",),
    "desc": ("v3", "v4", "text"),
    "desc_legacy": ("v3", "other"),
}


def judge_key(sha: str) -> str:
    return f"{sha}{JUDGE_KEY_SUFFIX}"


def text_key(sha: str) -> str:
    return f"{sha}{TEXT_KEY_SUFFIX}"


def vocab_key(sha: str) -> str:
    return f"{sha}{VOCAB_KEY_SUFFIX}"


def legacy_key(sha: str) -> str:
    return sha


def desc_digest(fn: str, desc: str) -> str:
    """新 desc 键摘要：fn+描述一起哈希，同描述不同仓不再共用一条（G3-1）。"""
    return hashlib.sha1(f"{fn}\x00{desc or ''}".encode("utf-8")).hexdigest()[:DESC_DIGEST_LEN]


def desc_key(fn: str, desc: str) -> str:
    return DESC_PREFIX + desc_digest(fn, desc)


def parse_key(key: str) -> tuple[str, str]:
    """解键 → (layer, sha)。sha 与条目 entry["sha"] 同口径（desc 键含 desc:: 前缀）。

    layer ∈ judge/text/vocab/legacy/desc/desc_legacy/unknown。
    未知后缀一律 unknown，不猜——猜错会把旧条目当新层用。
    """
    if not isinstance(key, str) or not key:
        return ("unknown", "")
    if key.startswith(DESC_PREFIX):
        core = key[len(DESC_PREFIX):]
        if core.endswith(JUDGE_KEY_SUFFIX):      # 旧键 desc::<描述>#v4（载荷是 v3）
            core = core[:-len(JUDGE_KEY_SUFFIX)]
        elif core.endswith(TEXT_KEY_SUFFIX) or core.endswith(VOCAB_KEY_SUFFIX):
            return ("unknown", key)              # 未出现的组合，防未来误写
        if _DIGEST_RE.match(core):
            return ("desc", DESC_PREFIX + core)
        return ("desc_legacy", DESC_PREFIX + core)
    if key.endswith(JUDGE_KEY_SUFFIX):
        return ("judge", key[:-len(JUDGE_KEY_SUFFIX)])
    if key.endswith(TEXT_KEY_SUFFIX):
        return ("text", key[:-len(TEXT_KEY_SUFFIX)])
    if key.endswith(VOCAB_KEY_SUFFIX):
        return ("vocab", key[:-len(VOCAB_KEY_SUFFIX)])
    if _SHA_RE.match(key):
        return ("legacy", key)
    return ("unknown", key)


def entry_shape(obj) -> str:
    """载荷形态（只看结构，不看出处）。v4 与 v3 的关键差别是 classification.cat_primary。

    出处（如 source=desc）用 entry_source 取，别混进形态：desc 旧条目是 v3 结构，
    按 v3 对待才不会被误判成"形态不符"。
    """
    if not isinstance(obj, dict):
        return "bad"
    cls = obj.get("classification")
    if not isinstance(cls, dict):
        cls = {}
    if "cat_primary" in cls:
        return "v4"
    if "tags" in obj or "abstain" in obj:
        return "vocab"
    if "identity" in obj and cls:
        return "v3"
    if "identity" in obj:
        return "text"
    return "other"


def entry_source(obj) -> str | None:
    """出处标记：desc=描述降级生成；None=README 正常路径。"""
    return obj.get("source") if isinstance(obj, dict) else None


def accepts(layer: str, shape: str) -> bool:
    """该层的载荷形态是否可采信。取到键但形态不符 = 当作缺层。"""
    return shape in ACCEPTS.get(layer, ())


def probe(sha: str, get) -> dict:
    """探查一个 sha 的三层（+旧代）可用性。

    get(key) -> obj | None；返回 {layer: {"key", "shape", "ok"}}。
    只回可采信的层；形态不符的层仍列出但 ok=False，便于体检统计。
    """
    out = {}
    for layer, key in (("judge", judge_key(sha)), ("text", text_key(sha)),
                       ("vocab", vocab_key(sha)), ("legacy", legacy_key(sha))):
        obj = get(key)
        shape = entry_shape(obj) if obj is not None else None
        out[layer] = {"key": key, "shape": shape,
                      "ok": bool(obj is not None and accepts(layer, shape))}
    return out


def best(sha: str, get, want: tuple[str, ...] = ("judge", "legacy")) -> dict | None:
    """按优先级返回第一个可采信层：{"layer","key","shape","obj"}。"""
    for layer in want:
        key = {"judge": judge_key, "text": text_key, "vocab": vocab_key,
               "legacy": legacy_key}[layer](sha)
        obj = get(key)
        if obj is not None and accepts(layer, entry_shape(obj)):
            return {"layer": layer, "key": key, "shape": entry_shape(obj), "obj": obj}
    return None
