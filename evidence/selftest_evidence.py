# -*- coding: utf-8 -*-
"""evidence_collect 离线自检：解析器夹具 + FakeClient 端到端 + 分片存储 + 增量分档。

不调任何网络。CI 在采集前先跑本文件（绿了才采集）；本地：
  python evidence/selftest_evidence.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "evidence"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))

import evidence_collect as ec  # noqa: E402
import evidence_store as es  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def _http_error(code: int) -> requests.HTTPError:
    resp = requests.Response()
    resp.status_code = code
    return requests.HTTPError(f"{code}", response=resp)


class FakeClient:
    def __init__(self, tree_by_ref: dict, repo_info: dict | None = None):
        self.tree_by_ref = tree_by_ref
        self.repo_info = repo_info or {}
        self.calls: list[tuple] = []

    def tree_conditional(self, fn, ref, etag=None):
        self.calls.append(("tree", ref, etag))
        if etag and ref in self.tree_by_ref:
            return 304, None, etag
        if ref in self.tree_by_ref:
            return 200, self.tree_by_ref[ref], f'etag-{ref}'
        raise _http_error(404)

    def repo(self, fn):
        self.calls.append(("repo", fn))
        if fn in self.repo_info:
            return self.repo_info[fn]
        raise _http_error(404)


class FakeRaw:
    def __init__(self, files: dict[str, bytes]):
        self.files = files
        self.count = 0

    def get(self, fn, ref, path):
        self.count += 1
        if path in self.files:
            return self.files[path], None
        return None, "404"

    def get_many(self, fn, ref, paths):
        return [(p, *self.get(fn, ref, p)) for p in paths]


# ---------------- 1. 解析器 ----------------
def test_parsers() -> None:
    r = ec._go_mod("""module example.com/app
go 1.21
require (
\tgithub.com/go-sql-driver/mysql v1.7.1
\tgithub.com/jackc/pgx/v5 v5.5.0
\tgithub.com/stretchr/testify v1.8.4 // indirect
)
require github.com/lib/pq v1.10.9
replace github.com/x/y => github.com/z/w v1.0.0
""")
    check("go.mod 直接依赖", r["names"] == ["github.com/go-sql-driver/mysql",
          "github.com/jackc/pgx/v5", "github.com/lib/pq"], str(r))
    check("go.mod indirect 入 dev", r["dev"] == ["github.com/stretchr/testify"], str(r))
    check("go.mod replace 目标不算依赖", all("z/w" not in x for x in r["names"] + r["dev"]))

    r = ec._npm('{"dependencies":{"mysql2":"^3","pg":"8"},'
                '"devDependencies":{"jest":"^29"},"peerDependencies":{"knex":">=2"}}')
    check("npm 三类依赖", r["names"] == ["mysql2", "pg", "knex"] and r["dev"] == ["jest"], str(r))

    r = ec._pom("""<project><dependencies>
<dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId></dependency>
<dependency><groupId>mysql</groupId><artifactId>mysql-connector-java</artifactId></dependency>
</dependencies></project>""")
    check("pom 依赖", r["names"] == ["org.postgresql:postgresql", "mysql:mysql-connector-java"], str(r))

    r = ec._gradle("""
dependencies {
    implementation 'org.postgresql:postgresql:42.7.1'
    testImplementation 'com.h2database:h2:2.2.224'
}""")
    check("gradle 依赖", r["names"] == ["org.postgresql:postgresql"]
          and r["dev"] == ["com.h2database:h2"], str(r))

    r = ec._requirements("SQLAlchemy>=2.0  # ORM\npsycopg2-binary==2.9\n-r other.txt\n# 注释\nPyMySQL[rsa]\n")
    check("requirements", r["names"] == ["sqlalchemy", "psycopg2-binary", "pymysql"], str(r))

    r = ec._pyproject("""[project]
name = "x"
dependencies = [
  "sqlalchemy>=2",
  "psycopg[binary]",
]
[tool.poetry.dependencies]
python = "^3.11"
redis = "^5"
""")
    check("pyproject PEP621+poetry", r["names"] == ["sqlalchemy", "psycopg", "redis"], str(r))

    r = ec._setup_py("setup(\n    install_requires=['Django>=4.2', 'psycopg2'],\n)")
    check("setup.py", r["names"] == ["Django", "psycopg2"], str(r))

    r = ec._cargo("[dependencies]\nmysql = \"25\"\n\n[dev-dependencies]\ntokio-test = \"0.4\"")
    check("Cargo.toml", r["names"] == ["mysql"] and r["dev"] == ["tokio-test"], str(r))

    r = ec._gem("source 'https://rubygems.org'\ngem 'sqlite3'\ngem \"mysql2\"")
    check("Gemfile", r["names"] == ["sqlite3", "mysql2"], str(r))

    r = ec._composer('{"require":{"php":"^8","ext-pdo":"*","illuminate/support":"^10"},'
                      '"require-dev":{"phpunit":"^10"}}')
    check("composer.json", r["names"] == ["php", "ext-pdo", "illuminate/support"]
          and r["dev"] == ["phpunit"], str(r))

    r = ec._csproj('<Project><ItemGroup>'
                   '<PackageReference Include="Npgsql" Version="8.0" />'
                   '<PackageReference Include="MySqlConnector" />'
                   '</ItemGroup></Project>')
    check("csproj", r["names"] == ["Npgsql", "MySqlConnector"], str(r))

    r = ec._mix("defp deps do\n  [\n    {:postgrex, \">= 0.0.0\"},\n    {:ecto_sql, \"~> 3.10\"},\n    {:jason, \"1.4\"}\n  ]\nend")
    check("mix.exs", r["names"] == ["postgrex", "ecto_sql", "jason"], str(r))


# ---------------- 2. 镜像提取 / blob sha / 选择表 ----------------
def test_extract() -> None:
    imgs = ec.extract_images("""services:
  db:
    image: mysql:8.0
  cache:
    image: "redis:7"
  pg:
    image: postgres:16-alpine
""")
    check("compose 镜像", imgs == ["mysql:8.0", "redis:7", "postgres:16-alpine"], str(imgs))

    imgs = ec.extract_images("FROM --platform=$BUILDPLATFORM golang:1.22 AS builder\nFROM alpine:3.19\nFROM scratch\n")
    check("Dockerfile FROM（scratch 排除）", imgs == ["golang:1.22", "alpine:3.19"], str(imgs))

    check("git blob sha 算法对齐 git", ec.git_blob_sha(b"hello\n")
          == "ce013625030ba8dba906f756967f9e9ca394464a")

    sel = ec.select_targets([
        "README.md", "README.zh-CN.md", "CHANGELOG.md", "docs/supported-databases.md",
        "package.json", "services/api/package.json", "go.mod", "docker-compose.yml",
        ".github/workflows/ci.yml", "src/main.go",
        "src/connector/mysql/conn.go", "internal/dialect/postgres/dialect.go",
    ] + [f"svc{i}/package.json" for i in range(20)])
    kinds = [k for _, k, _ in sel["fetch"]]
    check("选择表：dep 上限 12", kinds.count("dep") == 12, str(kinds))
    check("选择表：根级 package.json 优先", ("package.json", "dep", "npm") in sel["fetch"])
    check("选择表：image/ci", ("docker-compose.yml", "image", None) in sel["fetch"]
          and (".github/workflows/ci.yml", "ci", None) in sel["fetch"])
    check("线索：changelog/i18n/docs", sel["clues"]["changelog"] == ["CHANGELOG.md"]
          and sel["clues"]["readme_i18n"] == ["README.zh-CN.md"]
          and sel["clues"]["docs_matrix"] == ["docs/supported-databases.md"], str(sel["clues"]))
    check("路径指纹：connector/dialect 捕获",
          "src/connector/mysql/conn.go" in sel["clues"]["paths"]
          and "internal/dialect/postgres/dialect.go" in sel["clues"]["paths"],
          str(sel["clues"]["paths"]))


# ---------------- 3. 端到端（FakeClient） ----------------
GO_MOD = "module example.com/app\n\nrequire github.com/go-sql-driver/mysql v1.7.1\n"
COMPOSE = "services:\n  db:\n    image: mysql:8.0\n"
CI = "jobs:\n  t:\n    services:\n      pg:\n        image: postgres:16\n"


def _fake_env():
    blobs = {"go.mod": GO_MOD.encode(), "docker-compose.yml": COMPOSE.encode(),
             ".github/workflows/ci.yml": CI.encode()}
    tree = {"sha": "t-sha", "truncated": False, "tree": [
        {"path": p, "type": "blob", "sha": ec.git_blob_sha(b)} for p, b in blobs.items()
    ] + [{"path": "README.zh-CN.md", "type": "blob", "sha": "r1"},
         {"path": "src/main.go", "type": "blob", "sha": "r2"}]}
    return FakeClient({"main": tree}), FakeRaw(blobs)


def test_collect_repo() -> None:
    client, raw = _fake_env()
    rec = ec.collect_repo(client, raw, "o/r", {"full_name": "o/r", "pushed_at": "2026-10-28", "stars": 10}, None)
    check("端到端：状态 ok", rec["status"] == "ok", rec.get("errors", ""))
    check("端到端：分支解析 main", rec["default_branch"] == "main")
    check("端到端：树元数据", rec["tree"]["sha"] == "t-sha" and rec["tree"]["path_count"] == 5)
    files = {f["path"]: f for f in rec["files"]}
    check("端到端：go.mod 指纹", files["go.mod"]["names"] == ["github.com/go-sql-driver/mysql"])
    check("端到端：compose 镜像", files["docker-compose.yml"]["images"] == ["mysql:8.0"])
    check("端到端：CI 镜像", files[".github/workflows/ci.yml"]["images"] == ["postgres:16"])
    check("端到端：blob sha 全对（无漂移）",
          not any(f.get("sha_mismatch") for f in rec["files"]))
    check("端到端：线索", rec["clues"]["readme_i18n"] == ["README.zh-CN.md"])

    # 树 304：续用旧记录只刷时间戳，不再抓文件
    client2, raw2 = _fake_env()
    rec["default_branch"] = "main"
    merged = ec.collect_repo(client2, raw2, "o/r",
                             {"pushed_at": "2026-10-29", "stars": 10}, rec)
    check("304 合并：保旧值刷新戳", merged["pushed_at"] == "2026-10-29"
          and merged["files"] == rec["files"] and merged["epoch"] == ec.EPOCH)

    # 空仓 409 → 终态
    c3 = FakeClient({})
    orig = c3.tree_conditional
    c3.tree_conditional = lambda fn, ref, etag=None: (_ for _ in ()).throw(_http_error(409))
    rec3 = ec.collect_repo(c3, FakeRaw({}), "o/r", {"pushed_at": "2026-10-28"}, None)
    check("空仓 409 → empty_repo", rec3["status"] == "empty_repo")

    # main/master 全 404 + repos 404 → gone
    c4 = FakeClient({}, repo_info={})
    rec4 = ec.collect_repo(c4, FakeRaw({}), "o/r", {"pushed_at": "2026-10-28"}, None)
    check("全 404 → gone", rec4["status"] == "gone")
    check("gone 只花 3 调（main+master+repos）", len(c4.calls) == 3, str(c4.calls))

    # raw 404 → partial
    c5, _ = _fake_env()
    rec5 = ec.collect_repo(c5, FakeRaw({}), "o/r", {"pushed_at": "2026-10-28"}, None)
    check("raw 全 404 → partial + errors", rec5["status"] == "partial"
          and "files" in rec5.get("errors", {}), str(rec5.get("errors")))

    # blob sha 漂移检测：树里给错 sha
    c6, raw6 = _fake_env()
    c6.tree_by_ref["main"]["tree"][0]["sha"] = "bad"
    rec6 = ec.collect_repo(c6, raw6, "o/r", {"pushed_at": "2026-10-28"}, None)
    check("sha_mismatch 标记", any(f.get("sha_mismatch") for f in rec6["files"]))


def test_matrix_urls() -> None:
    with tempfile.TemporaryDirectory() as td:
        old = ec.READMES_DIR
        d = Path(td)
        (d / "o__r.md").write_text(
            "see the [support matrix](https://example.com/docs/matrix) for details\n"
            "other [link](https://github.com/x)\n", encoding="utf-8")
        ec.READMES_DIR = d
        try:
            urls = ec.scan_matrix_urls("o/r")
        finally:
            ec.READMES_DIR = old
    check("README 离线扫矩阵 URL", urls == ["https://example.com/docs/matrix"], str(urls))


# ---------------- 4. 分片存储 ----------------
def test_store() -> None:
    with tempfile.TemporaryDirectory() as td:
        old = es.SHARD_DIR
        es.SHARD_DIR = Path(td)
        try:
            store = es.EvidenceCacheStore({"a/b": {"fn": "a/b", "status": "ok"}})
            store["c/d"] = {"fn": "c/d", "status": "ok"}
            n = store.flush()
            check("分片：写脏桶", n >= 1 and len(list(es.SHARD_DIR.glob("*.json"))) >= 1)
            store["a/b"] = {"fn": "a/b", "status": "partial"}
            store.flush()
            reloaded = es.load_cache()
            check("分片：upsert 覆盖", reloaded["a/b"]["status"] == "partial"
                  and reloaded["c/d"]["status"] == "ok")
            check("分片：桶定位与三胞胎一致",
                  all(es._bucket(fn) == __import__("interp_store")._bucket(fn)
                      for fn in ("a/b", "c/d", "pingcap/tidb", "o/r")))
        finally:
            es.SHARD_DIR = old


# ---------------- 5. 增量分档（纯函数） ----------------
def test_plan_incremental() -> None:
    pool = {"A/new": {"pushed_at": "2026-10-28", "stars": 100},
            "B/old": {"pushed_at": "2026-10-01", "stars": 50},
            "C/chg": {"pushed_at": "2026-10-28", "stars": 10},
            "D/stable": {"pushed_at": "2026-10-01", "stars": 5}}
    store = {"B/old": {"pushed_at": "2026-10-01"},          # 未变 → 跳过
             "C/chg": {"pushed_at": "2026-10-27"},          # 变了 → 复采
             "D/stable": {"pushed_at": "2026-10-01"}}       # 未变 → 跳过
    todo = ec.plan_incremental(pool, {"A/new"}, store)
    fns = [fn for fn, _ in todo]
    check("增量：新仓+变化仓、新仓优先", fns == ["A/new", "C/chg"], str(fns))


def test_release_notes() -> None:
    """enrich._release_notes：适配变更史素材（字节截断 + 命中行优先，零新增调用）。"""
    sys.path.insert(0, str(ROOT / "enrich"))
    import enrich  # noqa: E402  顶部只有路径 bootstrap，无副作用
    rels = [
        {"tag_name": "v3.0", "published_at": "2026-10-20T00:00:00Z", "body": "removed MySQL support\nadded PostgreSQL"},
        {"tag_name": "v2.1", "published_at": "2026-09-01T00:00:00Z", "body": ""},
        {"tag_name": "v2.0", "published_at": "2026-08-01T00:00:00Z", "body": "x" * 900},
        {"tag_name": "v1.0", "published_at": "2026-01-01T00:00:00Z", "body": "first"},
    ]
    notes = enrich._release_notes(rels)
    check("rel_notes：取前 3、跳过空正文", notes is not None
          and [n["t"] for n in notes] == ["v3.0", "v2.0"], str(notes))
    check("rel_notes：512 字节截断 + 日期日粒度",
          len(notes[1]["n"].encode()) == 512 and notes[0]["d"] == "2026-10-20")
    check("rel_notes：全空正文返回 None", enrich._release_notes(
        [{"tag_name": "v1", "published_at": "2026-01-01", "body": ""}]) is None)

    # 超长 changelog：DB 变更行在 512 字节之外，命中行优先应把它捞回来
    boiler = "What's Changed\n" + "\n".join(f"* Fix bug {i} by @user{i}" for i in range(40))
    body = boiler + "\n* Dropped MySQL 5.7 support\n* Added PostgreSQL 16 support"
    n = enrich._release_notes([{"tag_name": "v9", "published_at": "2026-10-01", "body": body}])
    txt = n[0]["n"]
    check("rel_notes：命中行优先（超长正文末尾的 DB 变更）",
          "MySQL 5.7" in txt and "PostgreSQL 16" in txt
          and "What's Changed" in txt and len(txt.encode()) <= 512, txt)

    # 中文按字节截断：字符截会超预算（1 字 3 字节），且不能劈开半个字
    n = enrich._release_notes([{"tag_name": "v1", "published_at": "2026-10-01",
                                "body": "新增功能说明" * 200}])
    check("rel_notes：中文按字节截断不劈字",
          len(n[0]["n"].encode("utf-8")) <= 512 and "新增" in n[0]["n"])


def main() -> int:
    test_parsers()
    test_extract()
    test_collect_repo()
    test_matrix_urls()
    test_store()
    test_plan_incremental()
    test_release_notes()
    print()
    if FAILS:
        print(f"==== 自检失败 {len(FAILS)} 项 ====")
        return 1
    print("==== 自检全绿 ====")
    return 0


if __name__ == "__main__":
    sys.exit(main())
