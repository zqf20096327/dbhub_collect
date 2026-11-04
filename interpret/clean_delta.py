# -*- coding: utf-8 -*-
"""clean_delta —— 清理文行级 delta 分片（B1，工作包清单 v4）。

问题：interp 缓存只存清理后的判定输入，原文→清理文的映射不留档；回查引句时
"当时看到的是什么"无法逐字节复现。全量存清理文每篇 ~5.3KB，四万条 = 200MB+，
不可行；行级 delta 均 2.09KB/篇（《v1存档》§3.6 实测），日增 ~0.6MB，可承受。

规则（B1 工作包）：
- 落点 state/clean_delta_shards/（256 分片，桶名=sha256(key) 前 2 位，仿
  interp_cache_shards 模式，不带轮转副本）；
- 键 = "<sha>+<clean_ver>"，值 = 原文行 → 清理文行的 SequenceMatcher opcodes；
- 只增量积累：键已存在直接跳过，**存量 4 万条不回填**（A1 读库 clean_ver 缺省
  = 常态非异常）；
- 判定调用构造 prompt 时顺手算 delta（build_prompt 内，零额外 IO），
  done 落缓存时写分片，元数据 clean_ver 随解读条目落盘；
- 清理器升级 = clean_ver 升版，新旧 delta 并存键控，互不覆盖。

验收：python interpret/clean_delta.py --selftest
  1) delta 重建清理文 == 直接 clean_readme 输出（逐字节，抽 500 篇）；
  2) 体积画像（均 KB/篇 → 推算日增，红线 ≤2MB）。
"""
from __future__ import annotations

import hashlib
import json
import random
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARD_DIR = ROOT / "state" / "clean_delta_shards"

# 从 rm_clean 导入须能被 golden_eval 等同目录脚本复用；作 lib 导入时保底
try:
    from rm_clean import CLEAN_VER          # noqa: F401
except ImportError:                          # 以包名/它目录运行时
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from rm_clean import CLEAN_VER          # noqa: F401


def _bucket(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()[:2]


def compute_delta(raw_text: str, clean_text: str) -> list:
    """原文→清理文的行级 opcodes：[[tag, i1, i2, j1, j2, ins_lines?], ...]。

    行切分用 splitlines()。'equal' 段只存区间（体积大头已被行级压缩）；
    'insert'/'replace' 段的清理侧是**新文本**（如噪音章节→「（略）」、
    行内变换改写的行），原文里没有——必须内嵌清理侧行文本，否则重建不出来
    （首版只存 opcode 占位空串，500 篇对拍当场推翻，教训）。
    """
    a = raw_text.splitlines()
    b = clean_text.splitlines()
    sm = SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        ent = [t, i1, i2, j1, j2]
        if t in ("insert", "replace"):
            ent.append(b[j1:j2])
        out.append(ent)
    return out


def apply_delta(raw_text: str, delta: list) -> str:
    """按 delta 重建清理文（验收 1 的对拍对象）。"""
    a = raw_text.splitlines()
    b: list[str] = []
    for ent in delta:
        t, i1, i2, j1, j2 = ent[:5]
        if t == "equal":
            b.extend(a[i1:i2])
        elif t in ("insert", "replace"):
            b.extend(ent[5])
        # delete：清理文侧无对应行，跳过
    return "\n".join(b)


def shard_path(bucket: str) -> Path:
    return SHARD_DIR / f"{bucket}.json"


def save(key: str, delta: list, fn: str = "") -> bool:
    """增量写一个条目：键已存在跳过（返回 False）。失败不抛——B1 是旁路，
    任何异常只损失留档，不许影响判定主流程。"""
    try:
        SHARD_DIR.mkdir(parents=True, exist_ok=True)   # 1104 修：漏建目录导致
        # save 全程静默失败（CI 首验 30 条 delta 全丢，真因=照抄 interp_store
        # _write_shard 时漏了 mkdir 这一行）
        p = shard_path(_bucket(key))
        shard = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        if key in shard:
            return False
        shard[key] = {"fn": fn, "clean_ver": key.split("+", 1)[1],
                      "raw_lines": delta[0][2] if delta else 0,
                      "ops": delta, "at": date.today().isoformat()}
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(shard, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        tmp.replace(p)
        return True
    except Exception:                         # noqa: BLE001
        return False


def load(key: str) -> dict | None:
    p = shard_path(_bucket(key))
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8")).get(key)


def total_bytes() -> int:
    return sum(p.stat().st_size for p in SHARD_DIR.glob("*.json")) if SHARD_DIR.is_dir() else 0


# ---- selftest（B1 验收） ----

def _selftest(sample_n: int = 500) -> int:
    from rm_clean import clean_readme
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    # 1) 合成往返
    raw = "# Title\n[![badge](url)\n\ntext here\n```\ncode\n```\ntail"
    clean = clean_readme(raw)
    d = compute_delta(raw, clean)
    chk("合成往返：apply_delta == clean_readme", apply_delta(raw, d) == clean)
    chk("空文往返", apply_delta("", compute_delta("", "")) == "")

    # 2) 真实 500 篇逐字节对拍（验收 1）
    rdir = ROOT / "data" / "readmes"
    files = [p for p in rdir.glob("*.md")]
    sample = random.Random(42).sample(files, min(sample_n, len(files)))
    bad, total_kb, n = 0, 0.0, 0
    for p in sample:
        raw_text = p.read_text(encoding="utf-8", errors="ignore")
        clean_text = clean_readme(raw_text)
        delta = compute_delta(raw_text, clean_text)
        if apply_delta(raw_text, delta) != clean_text:
            bad += 1
            if bad <= 3:
                print("  MISMATCH:", p.name)
        total_kb += len(json.dumps(delta, ensure_ascii=False)) / 1024
        n += 1
    chk(f"真实 {n} 篇逐字节重建一致（bad={bad}）", bad == 0)
    avg_kb = total_kb / n if n else 0
    print(f"[INFO] delta 均 {avg_kb:.2f}KB/篇；按日均新增解读 ~300 条推算日增 "
          f"{avg_kb * 300 / 1024:.2f}MB（红线 ≤2MB）")
    chk("体积画像在红线内（推算口径）", avg_kb * 300 / 1024 <= 2.0)

    # 3) 分片写读往返 + 键控跳过（临时目录，不碰真分片）
    import tempfile
    global SHARD_DIR
    with tempfile.TemporaryDirectory() as td:
        orig = SHARD_DIR
        SHARD_DIR = Path(td)
        try:
            key = "deadbeef+" + CLEAN_VER
            chk("save 新键", save(key, d, "a/b") is True)
            chk("save 重复键跳过", save(key, d, "a/b") is False)
            ent = load(key)
            chk("load 读回", ent is not None and ent["fn"] == "a/b"
                and ent["clean_ver"] == CLEAN_VER)
        finally:
            SHARD_DIR = orig
    print(f"selftest {'FAIL' if fails else 'PASS'}（{fails} 处失败）")
    return fails


def main() -> int:
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return 1 if _selftest() else 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
