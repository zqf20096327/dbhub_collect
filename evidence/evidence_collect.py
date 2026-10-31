# -*- coding: utf-8 -*-
"""证据层采集：文件树 + 依赖清单 + docker/CI 镜像指纹 + 变更检测（五型证据的采集侧）。

定位（全景见 COLLECTION_MAP §2.7）：
  - 只存"指纹 + 指针"——依赖名/镜像名/候选路径/blob sha/ETag，不存文件原文；
    原文留给裁决时按需 raw 拉（raw 不计 Core 配额），git 日增量纪律不破
  - 提取 vocab-free：只抽名字，不做"名字→哪个库"的判定，词表匹配归适配引擎
  - 与 unattr_judge 的关系：本层全池打底；unattr_judge 是定向侦查（双轨并存，
    后续可让它改读本层证据省 API）
  - 完整性自校验：raw 拉回的文件本地重算 git blob sha 与树中记录比对，
    分支漂移（采树与采文件之间 default branch 被推动）会留下 sha_mismatch 标记

成本模型（Core 计费；raw.githubusercontent 不计）：
  - 首采：树 1 调（main/master 命中率约 95%），都不中再 +1 调 repos 补 default_branch
  - 复采：池内 pushed_at（日粒度）未变 → 0 调；变了 → 树 1 调（ETag 304 再省）
  - raw：每仓 0~35 个文件（dep≤12 / image≤8 / ci≤15），0.1s 间隔顺序拉

断点续采（铁律，照抄 09-29 README 假振事故教训）：
  - 逐仓 except 顺序：HTTPError(404/409/410 就地特判) →
    (BudgetOut, QuotaPatienceOut) 必须原样 raise → Exception 三振隔离（fail_count≥3 弃采）
  - 预算触线在仓边界收尾、exit 0（CI 绿），断点随每 20 仓落盘
  - done 判定看证据分片本身（epoch 相符 + 终态），state 只记运行摘要——丢了也能重推

错误分类台账（"没证据"≠"采失败"）：
  - empty_repo（树 409）/ gone（repos 404/410）：终态，pushed_at 不变不再重试
  - error（403 DMCA、5xx、网络）：fail_count 累计，<3 次时 pushed_at 变化可重试

记录 schema（v1，存 state/evidence_cache_shards/<xx>.json，键 = fn）：
  {"fn","v":1,"epoch","status": ok|partial|empty_repo|gone|error,
   "collected_at","default_branch","pushed_at","stars",
   "tree":  {"sha","etag","truncated","path_count","matched":[选中路径]},
   "files": [{"path","kind": dep|image|ci,"ecosystem","blob_sha","bytes",
              "names":[依赖名],"dev":[开发依赖],"images":[镜像名],
              "sha_mismatch?","error?"}],
   "clues": {"changelog":[路径],"readme_i18n":[路径],"docs_matrix":[路径],
             "paths":[connector/driver 类路径指纹],"matrix_urls":[README 内的官网矩阵 URL]},
   "fail_count","last_error?"}

用法：
  python evidence/evidence_collect.py plan [--priority-file fns.txt]   # 离线分档出清单
  python evidence/evidence_collect.py sweep [--limit N]               # 按清单采集，断点续采
  python evidence/evidence_collect.py incremental [--limit N]         # 新仓 + pushed_at 变化仓
  python evidence/evidence_collect.py auto                            # CI 入口（下述三态自动选）
  python evidence/evidence_collect.py status | verify                 # 离线体检

auto 逻辑：清单不存在 → plan + sweep；清单有未完成 → sweep；清单扫完 → incremental。
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))

import requests  # noqa: E402

from gh import (  # noqa: E402
    Budget, BudgetOut, GitHubClient, QuotaPatienceOut, atomic_write_json,
)
from evidence_store import EvidenceCacheStore, load_cache as load_store  # noqa: E402

log = logging.getLogger("evidence")

# ---------------- 路径与常量 ----------------
STATE_P = ROOT / "state" / "evidence_state.json"
TASKS_P = ROOT / "state" / "evidence_tasks.json"
POOL_P = ROOT / "data" / "live" / "pool.ndjson"
POOL_CN_P = ROOT / "data" / "live" / "pool_cn.ndjson"
READMES_DIR = ROOT / "data" / "readmes"
INTERP_CACHE_MOD = "interp_store"          # plan 借道解读缓存判"已适配"，动态导入

EPOCH = "sweep-1"        # 全量纪元：记录结构不兼容变更时递增（旧记录视为未采）
REC_V = 1
RAW_BASE = "https://raw.githubusercontent.com"
RAW_INTERVAL = 0.1       # raw 域礼貌间隔（不计 Core 配额，但也不能打太快）
RAW_MAX_BYTES = 262_144  # 256KB：依赖/配置文件足够；超出截断并标记
FLUSH_EVERY = 20         # 每 N 仓落盘一次（分片 + state）
TERMINAL_OK = {"ok", "partial", "empty_repo", "gone"}
MAX_FAILS = 3            # 三振出局：连续失败 3 次的仓本次全量内不再重试

# ---------------- 文件选择表（改行为=改这里） ----------------
DEP_BY_BASENAME = {          # 根名精确匹配 → 生态
    "package.json": "npm", "go.mod": "go", "pom.xml": "maven",
    "build.gradle": "gradle", "build.gradle.kts": "gradle",
    "requirements.txt": "pypi", "pyproject.toml": "pyproject",
    "setup.py": "setup_py", "Cargo.toml": "cargo", "Gemfile": "gem",
    "composer.json": "composer", "mix.exs": "mix",
}
DEP_OTHER_RE = [             # 路径正则匹配 → 生态（csproj 任意层）
    (re.compile(r"[^/]+\.csproj$"), "csproj"),
]
IMAGE_PATH_RE = [            # 镜像/服务配置（compose、Dockerfile、helm values）
    re.compile(r"^docker-compose[^/]*\.ya?ml$"),
    re.compile(r"^compose(\.override)?\.ya?ml$"),
    re.compile(r"(^|/)Dockerfile[^/]*$"),
    re.compile(r"(^|/)values\.ya?ml$"),        # helm chart 的 image: 常在 values.yaml
]
CI_PATH_RE = re.compile(r"^\.github/workflows/[^/]+\.ya?ml$")
CAPS = {"dep": 12, "image": 8, "ci": 15}

# 线索（只记路径，不抓原文——裁决时按需 raw）
CHANGELOG_RE = re.compile(r"(?i)^changelog(\.[^/]*)?$")
README_I18N_RE = re.compile(r"(?i)^readme[-_.].+\.(md|rst|txt)$")   # 排除裸 README.md
DOCS_DIR_RE = re.compile(r"(?i)^(docs?|doc)/")
DOCS_MATRIX_RE = re.compile(r"(?i)(support|matrix|compat|driver|database)[^/]*\.(md|rst|txt)$")
# 路径指纹：connector/mysql、driver/postgres 这类目录结构是路径证据的本体
# （unattr_judge E1 同款信号）。纯结构词、不含库名——库名留在路径里由引擎匹配。
PATH_CLUE_RE = re.compile(r"(?i)(connector|driver|dialect|adapter|plugin)")
PATH_CLUE_CAP = 40


def _dedupe(items) -> list[str]:
    seen, out = set(), []
    for x in items:
        x = str(x).strip()
        if x and x.lower() not in seen:
            seen.add(x.lower())
            out.append(x)
    return out


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------- 解析器（纯函数，全部离线可测；vocab-free 只抽名字） ----------------
def _npm(text: str) -> dict:
    try:
        d = json.loads(text)
    except ValueError:
        return {"names": [], "dev": []}
    names = (list(d.get("dependencies") or {})
             + list(d.get("optionalDependencies") or {})
             + list(d.get("peerDependencies") or {}))
    return {"names": _dedupe(names), "dev": _dedupe(list(d.get("devDependencies") or {}))}


def _composer(text: str) -> dict:
    try:
        d = json.loads(text)
    except ValueError:
        return {"names": [], "dev": []}
    return {"names": _dedupe(list(d.get("require") or {})),
            "dev": _dedupe(list(d.get("require-dev") or {}))}


def _go_mod(text: str) -> dict:
    names, dev, section = [], [], None
    for raw in text.splitlines():
        code = raw.split("//")[0].strip()
        if not code:
            continue
        m = re.match(r"^(\w+)\s*\($", code)
        if m:
            section = m.group(1)
            continue
        if code == ")":
            section = None
            continue
        m2 = re.match(r"^(\w+)\s+(.*)$", code)
        if m2 and m2.group(1) in ("require", "exclude", "replace", "module", "go", "toolchain"):
            if m2.group(1) == "require":        # 单行 require
                (dev if "indirect" in raw else names).append(m2.group(2).split()[0])
            section = None if m2.group(1) != "require" else section
            continue
        if section == "require":                # 块内行（replace/exclude 块不走这里）
            (dev if "indirect" in raw else names).append(code.split()[0])
    return {"names": _dedupe(names), "dev": _dedupe(dev)}


def _pom(text: str) -> dict:
    names = []
    for blk in re.finditer(r"<dependency>(.*?)</dependency>", text, re.S):
        g = re.search(r"<groupId>(.*?)</groupId>", blk.group(1), re.S)
        a = re.search(r"<artifactId>(.*?)</artifactId>", blk.group(1), re.S)
        if g and a:
            names.append(f"{g.group(1).strip()}:{a.group(1).strip()}")
    return {"names": _dedupe(names), "dev": []}


_GRADLE_CONF = re.compile(
    r"(?m)^\s*(implementation|api|compileOnly|runtimeOnly|testImplementation|"
    r"testRuntimeOnly|testCompileOnly|annotationProcessor|developmentOnly)"
    r"(?:\s*\([^)]*\))?\s+['\"]([^'\"]+)['\"]")


def _gradle(text: str) -> dict:
    names, dev = [], []
    for m in _GRADLE_CONF.finditer(text):
        coord = m.group(2).split(":")
        if len(coord) >= 2:
            (dev if m.group(1).startswith("test") else names).append(
                f"{coord[0]}:{coord[1]}")
    return {"names": _dedupe(names), "dev": _dedupe(dev)}


def _requirements(text: str) -> dict:
    names = []
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line or line.startswith("-"):
            continue
        token = re.split(r"[\s\[<>=!~;,]", line, 1)[0].strip()
        if token:
            names.append(token.lower())
    return {"names": _dedupe(names), "dev": []}


def _pyproject(text: str) -> dict:
    names, section, in_deps = [], None, False
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"^\[([^\]]+)\]", line)
        if m:
            section, in_deps = m.group(1), False
            continue
        if section == "project" and re.match(r"^dependencies\s*=\s*\[", line):
            in_deps = True
            names += re.findall(r"[\"']([^\"']+)[\"']", line)
            continue
        if in_deps:
            if line.startswith("]"):
                in_deps = False
            else:
                names += re.findall(r"[\"']([^\"']+)[\"']", line)
            continue
        if section and section.startswith("tool.poetry.dependencies") and "=" in line:
            key = line.split("=")[0].strip()
            if key and key != "python" and not key.startswith("#"):
                names.append(key)
    out = []
    for n in names:
        token = re.split(r"[\s\[<>=!~;]", n, 1)[0].strip()
        if token:
            out.append(token)
    return {"names": _dedupe(out), "dev": []}


def _setup_py(text: str) -> dict:
    names = []
    m = re.search(r"install_requires\s*=\s*\[(.*?)\]", text, re.S)
    if m:
        for q in re.findall(r"[\"']([^\"']+)[\"']", m.group(1)):
            token = re.split(r"[\s\[<>=!~;]", q, 1)[0]
            if token:
                names.append(token)
    return {"names": _dedupe(names), "dev": []}


def _cargo(text: str) -> dict:
    names, dev, section = [], [], None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"^\[([^\]]+)\]", line)
        if m:
            section = m.group(1)
            continue
        if "=" in line:
            key = line.split("=")[0].strip()
            if not key or key.startswith("#"):
                continue
            if section == "dependencies":
                names.append(key)
            elif section in ("dev-dependencies", "build-dependencies"):
                dev.append(key)
    return {"names": _dedupe(names), "dev": _dedupe(dev)}


def _gem(text: str) -> dict:
    return {"names": _dedupe(re.findall(r"(?im)^\s*gem\s+['\"]([^'\"]+)", text)), "dev": []}


def _csproj(text: str) -> dict:
    return {"names": _dedupe(re.findall(r'(?i)PackageReference\s+Include="([^"]+)"', text)),
            "dev": []}


def _mix(text: str) -> dict:
    m = re.search(r"(?:def|defp)\s+deps\s+do(.*?)\bend\b", text, re.S)
    names = re.findall(r"\{\s*:([A-Za-z0-9_]+)\s*,", m.group(1)) if m else []
    return {"names": _dedupe(names), "dev": []}


PARSERS = {
    "npm": _npm, "composer": _composer, "go": _go_mod, "maven": _pom,
    "gradle": _gradle, "pypi": _requirements, "pyproject": _pyproject,
    "setup_py": _setup_py, "cargo": _cargo, "gem": _gem, "csproj": _csproj,
    "mix": _mix,
}


def extract_images(text: str) -> list[str]:
    """compose/workflows 的 image: 行 + Dockerfile 的 FROM 行。scratch 排除。"""
    out = []
    for m in re.finditer(r"(?im)^\s*image:\s*['\"]?([^\s'\"#]+)", text):
        out.append(m.group(1))
    for m in re.finditer(r"(?im)^FROM\s+(?:--platform=\S+\s+)?(\S+)", text):
        t = m.group(1)
        if t.lower() != "scratch":
            out.append(t)
    return _dedupe(out)


def git_blob_sha(data: bytes) -> str:
    """本地重算 git blob sha（与树接口返回的 blob sha 同算法），用于完整性校验。"""
    h = __import__("hashlib").sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


# ---------------- 树路径 → 抓取清单 + 线索（纯函数） ----------------
def select_targets(paths: list[str]) -> dict:
    dep, image, ci = [], [], []
    clues: dict[str, list] = {"changelog": [], "readme_i18n": [],
                              "docs_matrix": [], "paths": []}
    path_clues: list[str] = []
    for p in sorted(paths):
        base = p.rsplit("/", 1)[-1]
        if base in DEP_BY_BASENAME:
            dep.append((p, "dep", DEP_BY_BASENAME[base]))
        else:
            for rx, eco in DEP_OTHER_RE:
                if rx.search(p):
                    dep.append((p, "dep", eco))
                    break
        for rx in IMAGE_PATH_RE:
            if rx.search(p):
                image.append((p, "image", None))
                break
        if CI_PATH_RE.match(p):
            ci.append((p, "ci", None))
        if PATH_CLUE_RE.search(p):
            path_clues.append(p)
        if CHANGELOG_RE.match(base) and len(clues["changelog"]) < 2:
            clues["changelog"].append(p)
        elif README_I18N_RE.match(base) and len(clues["readme_i18n"]) < 5:
            clues["readme_i18n"].append(p)
        elif (DOCS_DIR_RE.match(p) and DOCS_MATRIX_RE.search(p)
              and len(clues["docs_matrix"]) < 5):
            clues["docs_matrix"].append(p)
    # 路径指纹：浅层优先（根附近的结构信号 > 深层），上限 PATH_CLUE_CAP
    clues["paths"] = sorted(path_clues, key=lambda x: (x.count("/"), x))[:PATH_CLUE_CAP]
    # 根级优先（路径深度升序），monorepo 子包按字典序取前 N
    dep.sort(key=lambda t: (t[0].count("/"), t[0]))
    image.sort(key=lambda t: (t[0].count("/"), t[0]))
    fetch = dep[:CAPS["dep"]] + image[:CAPS["image"]] + ci[:CAPS["ci"]]
    return {"fetch": fetch, "clues": clues}


def scan_matrix_urls(fn: str) -> list[str]:
    """本地 README 离线扫官网支持矩阵 URL（零 API；readme_sweep 已有正文）。"""
    p = READMES_DIR / (fn.replace("/", "__") + ".md")
    if not p.is_file():
        return []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")[:200_000]
    except OSError:
        return []
    urls = []
    for line in text.splitlines():
        if re.search(r"(?i)support|matrix|compat", line):
            urls += [u.rstrip(".,;") for u in
                     re.findall(r"https?://[^\s\)\]\"'<>]+", line)]
    return _dedupe(urls)[:5]


# ---------------- raw 抓取（独立域：不计 Core 配额） ----------------
class RawFetcher:
    """raw.githubusercontent 拉取：超限截断、404=None、网络错重试一次。

    单文件 get() 串行（0.1s 间隔）；单仓批量 get_many() 用 4 线程——
    raw 是 CDN 域无配额无礼貌间隔约束（gh.py 的"顺序不并发"铁律只针对
    api.github.com），10-30 实测串行 raw 是吞吐瓶颈（37s/仓 → 并发后大幅下降）。
    """

    def __init__(self, workers: int = 4) -> None:
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "dbhub-v2-collector"})
        self.count = 0
        self.errors = 0
        self._pool = ThreadPoolExecutor(max_workers=workers) \
            if workers > 1 else None

    def get(self, fn: str, ref: str, path: str) -> tuple[bytes | None, str | None]:
        url = f"{RAW_BASE}/{fn}/{ref}/{path}"
        for attempt in (1, 2):
            try:
                time.sleep(RAW_INTERVAL)
                r = self.s.get(url, timeout=(5, 20))
                self.count += 1
                if r.status_code == 404:
                    return None, "404"
                r.raise_for_status()
                if len(r.content) > RAW_MAX_BYTES:
                    return r.content[:RAW_MAX_BYTES], "truncated"
                return r.content, None
            except requests.RequestException:
                if attempt == 2:
                    self.errors += 1
                    return None, "network"
        return None, "network"

    def get_many(self, fn: str, ref: str, paths: list[str]) -> list[tuple]:
        """批量并发（保序返回 [(path, content, err), ...]）。"""
        if not self._pool or len(paths) <= 1:
            return [(p, *self.get(fn, ref, p)) for p in paths]
        futs = [(p, self._pool.submit(self.get, fn, ref, p)) for p in paths]
        return [(p, *fut.result()) for p, fut in futs]


# ---------------- 单仓采集 ----------------
def collect_repo(client: GitHubClient, raw: RawFetcher, fn: str,
                 pool_rec: dict, prev: dict | None) -> dict:
    """采单仓 → 证据记录。预算异常原样上抛；HTTP 404/409/410 就地分类为终态。"""
    rec = {
        "fn": fn, "v": REC_V, "epoch": EPOCH, "status": "ok",
        "collected_at": _iso_now(),
        "default_branch": (prev or {}).get("default_branch"),
        "pushed_at": (pool_rec.get("pushed_at") or "")[:10],
        "stars": pool_rec.get("stars"),
        "tree": {}, "files": [], "clues": {},
        "fail_count": (prev or {}).get("fail_count", 0),
    }
    prev_tree = (prev or {}).get("tree") or {}
    prev_branch = (prev or {}).get("default_branch")

    # --- 树：先验分支 → main → master；全 404 再花 1 调查 default_branch ---
    data = branch = new_etag = None
    seen: set[str] = set()
    for cand in [b for b in (prev_branch, "main", "master") if b]:
        if cand in seen:
            continue
        seen.add(cand)
        etag = prev_tree.get("etag") if (cand == prev_branch and prev_tree.get("sha")) else None
        try:
            status, tdata, new_etag = client.tree_conditional(fn, cand, etag)
        except requests.HTTPError as e:
            code = getattr(e.response, "status_code", None)
            if code == 404:
                continue
            if code == 409:            # Git Repository is empty（空仓 409 坑）
                rec["status"] = "empty_repo"
                return rec
            raise                      # 403(DMCA)/5xx 等由外层记振
        if status == 304:              # 树未变：续用旧记录，只刷新时间戳
            merged = dict(prev or {})
            merged.update({"pushed_at": rec["pushed_at"],
                           "collected_at": rec["collected_at"], "epoch": EPOCH})
            return merged
        data, branch = tdata, cand
        break
    if data is None:
        try:
            info = client.repo(fn)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) in (404, 410):
                rec["status"] = "gone"
                return rec
            raise
        db = info.get("default_branch")
        if not db:
            rec["status"] = "empty_repo"
            return rec
        root_only = False
        try:
            status, data, new_etag = client.tree_conditional(fn, db, None)
        except requests.HTTPError as e:
            code = getattr(e.response, "status_code", None)
            if code == 409:            # 报了 default_branch 的空仓（409 变体）
                rec["status"] = "empty_repo"
                return rec
            if code == 404:
                # 消歧（1 调）：非递归根树在 → 超大树 recursive 拿不动 → 根级降级；
                # 也 404 → 空壳仓（报了 default_branch 但无任何提交）→ 终态
                try:
                    status, data, new_etag = client.tree_conditional(
                        fn, db, None, recursive="0")
                except requests.HTTPError as e2:
                    code2 = getattr(e2.response, "status_code", None)
                    if code2 in (404, 409):
                        rec["status"] = "empty_repo"
                        return rec
                    raise
                root_only = True
            else:
                raise                  # 403(DMCA)/5xx 等由外层记振
        if status == 304:              # 理论上到不了（无 etag），防御性处理
            rec["default_branch"] = db
            return rec
        branch = db
        api_pushed = (info.get("pushed_at") or "")[:10]
        if api_pushed > rec["pushed_at"]:
            rec["pushed_at"] = api_pushed
    else:
        root_only = False
    rec["default_branch"] = branch

    # --- 树 → 路径/指纹/线索 ---
    entries = data.get("tree") or []
    blobs = {e["path"]: e.get("sha") for e in entries if e.get("type") == "blob"}
    sel = select_targets(list(blobs))
    rec["tree"] = {
        "sha": data.get("sha"), "etag": new_etag,
        "truncated": bool(data.get("truncated")) or root_only,
        "path_count": len(blobs),
        "matched": [p for p, _, _ in sel["fetch"]],
    }
    if root_only:                       # 超大树降级：仅根级条目，无深层路径
        rec["tree"]["fallback"] = "root_only"
    rec["clues"] = sel["clues"]

    # --- raw 抓取 + 解析 + blob sha 完整性校验 ---
    file_errs: list[str] = []
    results = raw.get_many(fn, branch, [p for p, _, _ in sel["fetch"]])
    for (path, kind, eco), (p, content, err) in zip(sel["fetch"], results):
        frec: dict = {"path": path, "kind": kind, "blob_sha": blobs.get(path)}
        if eco:
            frec["ecosystem"] = eco
        if content is None:
            frec["error"] = err or "unknown"
            file_errs.append(f"{path}:{err}")
            rec["files"].append(frec)
            continue
        frec["bytes"] = len(content)
        if err == "truncated":
            frec["truncated"] = True
        if blobs.get(path) and git_blob_sha(content) != blobs[path]:
            frec["sha_mismatch"] = True      # 采树与采文件之间分支漂移
        if kind == "dep" and eco in PARSERS:
            try:
                parsed = PARSERS[eco](content.decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001  畸形清单不炸仓：如顶层是数组的 package.json（10-31 pdxjie 实测）
                parsed = {}
                frec["parse_error"] = True
            if parsed.get("names"):
                frec["names"] = parsed["names"][:80]
            if parsed.get("dev"):
                frec["dev"] = parsed["dev"][:80]
        elif kind in ("image", "ci"):
            imgs = extract_images(content.decode("utf-8", "replace"))
            if imgs:
                frec["images"] = imgs[:40]
        rec["files"].append(frec)

    urls = scan_matrix_urls(fn)
    if urls:
        rec["clues"]["matrix_urls"] = urls
    if file_errs or rec["tree"]["truncated"]:
        rec["status"] = "partial"
        if file_errs:
            rec["errors"] = {"files": file_errs[:10]}
    return rec


# ---------------- 池与分档（plan 用，全部离线） ----------------
def load_pool() -> tuple[dict[str, dict], set[str]]:
    # 逐行迭代而非 read_text().splitlines()：后者会把描述里的 Unicode 行分隔符
    # （\u2028/\x85 等）也当换行切开，把合法 JSON 劈成两半（10-30 实测踩中）
    pool: dict[str, dict] = {}
    with POOL_P.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                pool[r["full_name"]] = r
    cn: set[str] = set()
    if POOL_CN_P.is_file():
        with POOL_CN_P.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    cn.add(json.loads(line)["full_name"])
    return pool, cn


def load_support_fns() -> set[str]:
    """已适配仓集合（解读缓存 classification.db_verdicts 含 support）。尽力而为：
    结构变化时降级为空集（plan 退化为不分空白档），绝不阻断。"""
    try:
        interp_store = __import__(INTERP_CACHE_MOD)
        cache = interp_store.load_cache()
        out = set()
        for v in cache.values():
            if not isinstance(v, dict):
                continue
            verdicts = (v.get("classification") or {}).get("db_verdicts") or []
            if v.get("fn") and any(isinstance(d, dict) and d.get("rel") == "support"
                                   for d in verdicts):
                out.add(v["fn"])
        log.info("解读缓存加载成功：%d 仓已适配", len(out))
        return out
    except Exception as e:  # noqa: BLE001
        log.warning("解读缓存加载失败，plan 降级为不分空白档：%s", e)
        return set()


def load_no_readme() -> set[str]:
    try:
        d = json.loads((ROOT / "state" / "readme_state.json").read_text(encoding="utf-8"))
        items = d.get("items", d) if isinstance(d, dict) else {}
        return {fn for fn, v in items.items()
                if isinstance(v, dict) and v.get("status") == "no_readme"}
    except Exception as e:  # noqa: BLE001
        log.warning("readme_state 读取失败（忽略）：%s", e)
        return set()


TIER_ORDER = ["P0", "cn_blank", "intl_blank", "cn_rest", "intl_high", "intl_rest"]


def cmd_plan(args) -> int:
    pool, cn = load_pool()
    support = load_support_fns()
    no_readme = load_no_readme()
    prio: list[str] = []
    if args.priority_file:
        pp = Path(args.priority_file)
        if pp.is_file():
            prio = [l.strip() for l in pp.read_text(encoding="utf-8").splitlines()
                    if l.strip() and "/" in l]
    buckets: dict[str, list[tuple[int, str]]] = {t: [] for t in TIER_ORDER}
    prio_set = set(prio)
    for fn, r in pool.items():
        stars = -(r.get("stars") or 0)
        blank = fn not in support
        if fn in prio_set:
            buckets["P0"].append((stars, fn))
        elif fn in cn:
            buckets["cn_blank" if blank else "cn_rest"].append((stars, fn))
        elif blank:
            buckets["intl_blank"].append((stars, fn))
        elif -(stars) >= 1000:
            buckets["intl_high"].append((stars, fn))
        else:
            buckets["intl_rest"].append((stars, fn))
    tasks: list[dict] = []
    for tier in TIER_ORDER:
        buckets[tier].sort()
        tasks += [{"fn": fn, "tier": tier} for _, fn in buckets[tier]]
    atomic_write_json(TASKS_P, {"epoch": EPOCH, "created_at": _iso_now(),
                                "total": len(tasks), "tasks": tasks})
    log.info("plan 完成：共 %d 仓 %s", len(tasks),
             {t: len(buckets[t]) for t in TIER_ORDER if buckets[t]})
    if no_readme:
        log.info("（参考：no_readme 仓 %d 个，证据是其唯一识别素材）", len(no_readme))
    return len(tasks)


# ---------------- 采集主循环（sweep / incremental 共用） ----------------
def run_collect_loop(client: GitHubClient, raw: RawFetcher, store: EvidenceCacheStore,
                     pool: dict[str, dict], todo: list[tuple], mode: str,
                     state: dict, limit: int | None) -> None:
    """todo = [(fn, pool_rec), ...] 按既定优先级。断点=分片里的终态记录。"""
    cnt = {"done": 0, "skip": 0, "fail": 0}
    run = {"date": _iso_now(), "mode": mode, "done": 0, "fail": 0}
    total = len(todo)
    # 逐仓日志：CI 日志要能看出"这一窗采了哪些仓"——静默 5 分钟等于黑箱
    try:
        for idx, (fn, pool_rec) in enumerate(todo, 1):
            prev = store.get(fn)
            if prev and prev.get("epoch") == EPOCH and prev.get("status") in TERMINAL_OK:
                cnt["skip"] += 1
                log.debug("[%d/%d] %s 跳过（已采）", idx, total, fn)
                continue
            if prev and prev.get("fail_count", 0) >= MAX_FAILS:
                cnt["skip"] += 1
                log.debug("[%d/%d] %s 跳过（失败 %d 次已出局）", idx, total, fn,
                          prev.get("fail_count"))
                continue
            t0 = time.time()
            try:
                rec = collect_repo(client, raw, fn, pool_rec or {"full_name": fn}, prev)
                store[fn] = rec
                cnt["done"] += 1
                log.info("[%d/%d] %s → %s · 树 %s 路径 · 指纹文件 %d · %.1fs · Core %d",
                         idx, total, fn, rec.get("status"),
                         (rec.get("tree") or {}).get("path_count", "-"),
                         len(rec.get("files") or []), time.time() - t0,
                         client.budget.calls)
            except (BudgetOut, QuotaPatienceOut):
                raise                       # 全局事件：绝不记成单仓失败（09-29 教训）
            except requests.HTTPError as e:
                code = getattr(e.response, "status_code", None)
                _mark_fail(store, fn, prev, f"http_{code}")
                cnt["fail"] += 1
                log.warning("[%d/%d] %s 失败 http_%s（%.1fs）", idx, total, fn, code,
                            time.time() - t0)
            except Exception as e:  # noqa: BLE001
                _mark_fail(store, fn, prev, str(e)[:120])
                cnt["fail"] += 1
                log.warning("[%d/%d] %s 失败 %s（%.1fs）", idx, total, fn,
                            str(e)[:120], time.time() - t0)
            if cnt["done"] and cnt["done"] % FLUSH_EVERY == 0:
                store.flush()
                _save_state(state, run | {"done": cnt["done"], "fail": cnt["fail"]})
            if limit and cnt["done"] >= limit:
                log.info("达到 --limit %d，收尾", limit)
                break
    except (BudgetOut, QuotaPatienceOut) as e:
        log.warning("预算先到，仓边界收尾（断点已落盘）：%s", e)
    finally:
        store.flush()
        run.update({"done": cnt["done"], "skip": cnt["skip"], "fail": cnt["fail"],
                    "calls": client.budget.calls, "raw": raw.count,
                    "raw_errors": raw.errors,
                    "elapsed_min": round((time.time() - client.budget.started) / 60, 1)})
        _save_state(state, run)
    log.info("==== %s 完成：新采 %d / 跳过 %d / 失败 %d · Core %d 调 · raw %d 次 ====",
             mode, cnt["done"], cnt["skip"], cnt["fail"],
             client.budget.calls, raw.count)


def _mark_fail(store: EvidenceCacheStore, fn: str, prev: dict | None, err: str) -> None:
    rec = prev or {"fn": fn, "v": REC_V, "epoch": EPOCH, "pushed_at": "", "stars": None}
    rec["status"] = "error"
    rec["fail_count"] = rec.get("fail_count", 0) + 1
    rec["last_error"] = err
    rec["collected_at"] = _iso_now()
    store[fn] = rec


def _load_state() -> dict:
    if STATE_P.is_file():
        try:
            return json.loads(STATE_P.read_text(encoding="utf-8"))
        except ValueError:
            log.warning("evidence_state 损坏，重建")
    return {"epoch": EPOCH, "runs": [], "totals": {}}


def _save_state(state: dict, run: dict) -> None:
    state["updated_at"] = _iso_now()
    state["runs"] = (state.get("runs") or [])[-29:] + [run]
    tot = state.setdefault("totals", {})
    for k in ("done", "fail"):
        tot[k] = tot.get(k, 0) + (run.get(k) or 0)
    atomic_write_json(STATE_P, state)


def _tasks_remaining(tasks: list[dict], store: dict) -> int:
    n = 0
    for t in tasks:
        rec = store.get(t["fn"])
        if not (rec and rec.get("epoch") == EPOCH and rec.get("status") in TERMINAL_OK):
            if not (rec and rec.get("fail_count", 0) >= MAX_FAILS):
                n += 1
    return n


def cmd_sweep(client, raw, store, pool, state, args) -> None:
    if not TASKS_P.is_file():
        raise SystemExit("任务清单不存在：先跑 plan（auto 会自动先 plan）")
    tasks = json.loads(TASKS_P.read_text(encoding="utf-8"))["tasks"]
    todo = [(t["fn"], pool.get(t["fn"])) for t in tasks]
    log.info("sweep：清单 %d 仓，剩余 %d", len(todo), _tasks_remaining(tasks, store))
    run_collect_loop(client, raw, store, pool, todo, "sweep", state, args.limit)


def plan_incremental(pool: dict[str, dict], cn: set[str], store: dict) -> list[tuple]:
    """纯函数：池 × 证据分片 → (新仓 ∪ pushed_at 变化仓)，新仓优先、国产优先、高星优先。"""
    todo = []
    for fn, r in pool.items():
        prev = store.get(fn)
        if prev is None:
            todo.append((0 if fn in cn else 1, -(r.get("stars") or 0), fn, r))
        elif (r.get("pushed_at") or "")[:10] != prev.get("pushed_at"):
            todo.append((2, -(r.get("stars") or 0), fn, r))
    todo.sort()
    return [(fn, r) for _, _, fn, r in todo]


def cmd_incremental(client, raw, store, pool, cn, state, args) -> None:
    todo = plan_incremental(pool, cn, store)
    log.info("incremental：候选 %d 仓（新仓 + pushed_at 变化）", len(todo))
    run_collect_loop(client, raw, store, pool, todo[:20000], "incremental", state, args.limit)


def cmd_auto(client, raw, store, pool, cn, state, args) -> None:
    if not TASKS_P.is_file():
        log.info("auto：无清单，先 plan")
        cmd_plan(args)
    tasks = json.loads(TASKS_P.read_text(encoding="utf-8"))["tasks"]
    if _tasks_remaining(tasks, store) > 0:
        cmd_sweep(client, raw, store, pool, state, args)
    else:
        log.info("auto：全量清单已扫完，转 incremental")
        cmd_incremental(client, raw, store, pool, cn, state, args)


# ---------------- 离线体检 ----------------
def cmd_status(recent: int = 10) -> None:
    from evidence_store import SHARD_DIR
    store = load_store()
    n = len(store)
    hist = Counter(r.get("status") for r in store.values())
    done_now = sum(1 for r in store.values()
                   if r.get("epoch") == EPOCH and r.get("status") in TERMINAL_OK)
    tasks: list[dict] = []
    if TASKS_P.is_file():
        try:
            tasks = json.loads(TASKS_P.read_text(encoding="utf-8")).get("tasks") or []
        except ValueError:
            log.warning("evidence_tasks 损坏，清单进度不可用")

    print(f"== 证据层 · 纪元 {EPOCH} ==")
    if tasks:
        print(f"清单 {len(tasks)} 仓：已采 {done_now}（{done_now / len(tasks) * 100:.1f}%），"
              f"剩余 {max(0, len(tasks) - done_now)}")
        for tier in TIER_ORDER:
            tier_fns = [t["fn"] for t in tasks if t.get("tier") == tier]
            if not tier_fns:
                continue
            d = sum(1 for fn in tier_fns
                    if (r := store.get(fn)) and r.get("epoch") == EPOCH
                    and r.get("status") in TERMINAL_OK)
            print(f"  {tier:<11} {d:>6} / {len(tier_fns):<6} {d / len(tier_fns) * 100:5.1f}%")
    else:
        print(f"清单未生成（已采 {done_now} 仓）")
    print(f"记录 {n} 条 · 状态 {dict(hist)} · 有指纹文件 {sum(1 for r in store.values() if r.get('files'))} 条"
          f" · 分片 {len(list(SHARD_DIR.glob('*.json'))) if SHARD_DIR.is_dir() else 0} 个")

    seen: set[str] = set()
    wins: list[dict] = []
    for r in reversed(_load_state().get("runs") or []):
        if r.get("date") in seen:
            continue
        seen.add(r.get("date"))
        wins.append(r)
        if len(wins) >= 3:
            break
    for r in wins:
        print(f"  窗口 {str(r.get('date'))[:16]} {r.get('mode', ''):<11}：采 {r.get('done', 0)}"
              f" / 跳过 {r.get('skip', 0)} / 失败 {r.get('fail', 0)} · Core {r.get('calls', 0)} 调"
              f" · raw {r.get('raw', 0)} 次 · {r.get('elapsed_min', '-')} 分钟")

    if recent:
        rows = sorted((r for r in store.values() if r.get("collected_at")),
                      key=lambda r: r["collected_at"], reverse=True)[:recent]
        print(f"最近 {len(rows)} 仓：")
        for r in rows:
            print(f"  {r['collected_at'][:16]} {str(r.get('status')):<10} {r.get('fn')}"
                  f" · 路径 {(r.get('tree') or {}).get('path_count', '-')}"
                  f" · 指纹文件 {len(r.get('files') or [])}")


def cmd_verify() -> None:
    from evidence_store import SHARD_DIR, _bucket
    errs: list[str] = []
    n = 0
    if SHARD_DIR.is_dir():
        for p in sorted(SHARD_DIR.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except ValueError as e:
                errs.append(f"{p.name}: JSON 损坏 {e}")
                continue
            if not isinstance(d, dict):
                errs.append(f"{p.name}: 非 dict")
                continue
            for fn, rec in d.items():
                if _bucket(fn) != p.stem:
                    errs.append(f"{fn}: 桶错位 {p.stem}≠{_bucket(fn)}")
                if not (isinstance(rec, dict) and rec.get("v") == REC_V
                        and rec.get("status") and rec.get("collected_at")):
                    errs.append(f"{fn}: schema 缺字段")
                n += 1
    print(f"[{'PASS' if not errs else 'FAIL'}] 分片校验：{n} 条记录，{len(errs)} 个问题")
    for e in errs[:20]:
        print("  -", e)
    if errs:
        sys.exit(1)


# ---------------- 入口 ----------------
def main() -> None:
    ap = argparse.ArgumentParser(description="证据层采集（树/依赖/镜像指纹）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "sweep", "incremental", "auto", "status", "verify"):
        sp = sub.add_parser(name)
        if name in ("sweep", "incremental", "auto"):
            sp.add_argument("--max-calls", type=int, default=4500)
            sp.add_argument("--max-minutes", type=float, default=110.0)
            sp.add_argument("--limit", type=int, default=None,
                            help="本次最多新采 N 仓（冒烟用）")
        if name == "plan":
            sp.add_argument("--priority-file", default=None,
                            help="fn 列表文件（每行 owner/repo），置顶为 P0 档")
        if name == "status":
            sp.add_argument("--recent", type=int, default=10,
                            help="列出最近 N 个已采仓（0=不列）")
        if name == "auto":      # auto 首跑会转 plan，参数保持一致
            sp.add_argument("--priority-file", default=None)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")

    if args.cmd == "status":
        cmd_status(args.recent)
        return
    if args.cmd == "verify":
        cmd_verify()
        return
    if args.cmd == "plan":
        cmd_plan(args)
        return

    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    raw = RawFetcher()
    store = EvidenceCacheStore(load_store())
    state = _load_state()
    if args.cmd == "sweep":
        pool, cn = load_pool()
        cmd_sweep(client, raw, store, pool, state, args)
    elif args.cmd == "incremental":
        pool, cn = load_pool()
        cmd_incremental(client, raw, store, pool, cn, state, args)
    else:
        pool, cn = load_pool()
        cmd_auto(client, raw, store, pool, cn, state, args)


if __name__ == "__main__":
    main()
