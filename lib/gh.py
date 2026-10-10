# -*- coding: utf-8 -*-
"""GitHub 客户端：动态限流 + ETag + 重试 + 预算停止（调度容错设计的实现层）。

铁律（来自事故教训）：
  - 顺序请求，不并发；礼貌间隔对齐现网实测（默认 0.5s，可调）
  - 睡等上限 SLEEP_CAP_SEC=900：403/429 需等超过上限时抛 QuotaPatienceOut，
    由调用方优雅收尾（本次运行结束、断点已落盘、下窗口再来）
  - 外部预算（max_calls / stop_when_remaining / deadline）先到先停
密钥：dbhub_v2/.env 的 GITHUB_TOKEN 或环境变量（不复制、不打印）。
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests

log = logging.getLogger("gh")

REQUEST_TIMEOUT = (5, 20)   # (连接, 读取)
SLEEP_CAP_SEC = 900          # 睡等上限 15 分钟
MAX_RETRY = 2                # 5xx/网络错误重试次数


class QuotaPatienceOut(Exception):
    """需睡等超过上限——调用方应立即收尾。reset=配额恢复时间戳（若有）。"""

    def __init__(self, msg: str, reset: int | None = None):
        super().__init__(msg)
        self.reset = reset


class BudgetOut(Exception):
    """外部预算（调用数/墙钟/配额保底）先到——优雅收尾。"""


class CoreReserveOut(BudgetOut):
    """Core 剩余配额触保底线。reset=失败响应的 X-RateLimit-Reset（跨窗续跑睡到那）。

    注意：Actions GITHUB_TOKEN 上 /rate_limit 探测与真实调用分属不同桶
    （09-30 实测探测 5000 / 调用头 800），等待决策必须以本异常携带的
    响应头 reset 为准，不能信探测。
    """

    def __init__(self, msg: str, reset: int | None = None):
        super().__init__(msg)
        self.reset = reset


def load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    p = next((c for c in (root / "config" / ".env", root / ".env") if c.is_file()), None)
    if p is None:
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


@dataclass
class Budget:
    max_calls: int = 4000          # 单次运行调用上限
    max_minutes: float = 90.0      # 单次运行墙钟上限
    reserve_remaining: int = 800   # 剩余配额保底线，触线即停
    min_interval: float = 0.5      # 礼貌间隔（现网实测节奏）
    calls: int = field(default=0)
    started: float = field(default_factory=time.time)

    def check(self):
        if self.calls >= self.max_calls:
            raise BudgetOut(f"调用数达上限 {self.max_calls}")
        if (time.time() - self.started) / 60 >= self.max_minutes:
            raise BudgetOut(f"墙钟达上限 {self.max_minutes} 分钟")


class GitHubClient:
    API = "https://api.github.com"

    def __init__(self, budget: Budget | None = None):
        load_env()
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise SystemExit("GITHUB_TOKEN 未配置：写入 dbhub_v2/.env 或设环境变量")
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dbhub-v2-collector",
        })
        self.budget = budget or Budget()
        self.etag_store: dict[str, str] = {}   # url -> etag（进程内；持久化由调用方管）

    # ---------------- 底层请求 ----------------
    def _request(self, method: str, url: str, *, params=None, etag=None,
                 accept=None, _retry=0) -> requests.Response:
        self.budget.check()
        # Search API 主限流 30/分钟（约 2.1s/次）；Core 走礼貌间隔
        interval = 2.1 if "/search/" in url else self.budget.min_interval
        time.sleep(interval)
        headers = {}
        if etag:
            headers["If-None-Match"] = etag
        if accept:
            headers["Accept"] = accept
        try:
            resp = self.s.request(method, url, params=params,
                                  headers=headers, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as e:
            if _retry < MAX_RETRY:
                time.sleep(2 ** (_retry + 1))
                return self._request(method, url, params=params, etag=etag,
                                     accept=accept, _retry=_retry + 1)
            raise
        self.budget.calls += 1
        # 区分资源域：保底线只对 Core 生效（Search 是 30/分钟小窗口，
        # 由 2.1s 间隔 + 403 睡等处理，不能拿它的剩余数对 Core 保底线）
        resource = resp.headers.get("X-RateLimit-Resource", "core")
        rem = resp.headers.get("X-RateLimit-Remaining")
        if resource == "core" and rem is not None and int(rem) <= self.budget.reserve_remaining:
            reset = resp.headers.get("X-RateLimit-Reset")
            raise CoreReserveOut(f"Core 剩余配额触保底线（remaining={rem}）",
                                 int(reset) if reset and reset.isdigit() else None)
        if resp.status_code == 304:
            return resp
        if resp.status_code in (403, 429):
            self._respect_retry_after(resp)
        if resp.status_code >= 500 and _retry < MAX_RETRY:
            time.sleep(2 ** (_retry + 1))
            return self._request(method, url, params=params, etag=etag,
                                 accept=accept, _retry=_retry + 1)
        resp.raise_for_status()
        return resp

    def _respect_retry_after(self, resp):
        """403/429：优先 Retry-After，否则睡到 Reset；超过睡等上限抛 QuotaPatienceOut。"""
        ra = resp.headers.get("Retry-After")
        wait = int(ra) if ra and ra.isdigit() else 0
        reset_ts = None
        if not wait:
            reset = resp.headers.get("X-RateLimit-Reset")
            if reset and reset.isdigit():
                reset_ts = int(reset)
                wait = max(0, reset_ts - int(time.time()) + 2)
        if wait > SLEEP_CAP_SEC:
            raise QuotaPatienceOut(f"需睡等 {wait}s > 上限 {SLEEP_CAP_SEC}s，本次收尾", reset_ts)
        if wait > 0:
            log.warning("限流：睡 %ss（上限内）", wait)
            time.sleep(wait)

    # ---------------- 业务方法 ----------------
    def search_total(self, q: str) -> int:
        r = self._request("GET", f"{self.API}/search/repositories",
                          params={"q": q, "per_page": 1})
        return int(r.json().get("total_count") or 0)

    def search_all(self, q: str, cap: int = 1000) -> list[dict]:
        """分页拉全（≤cap；超过需调用方用限定词拆分）。"""
        items, page = [], 1
        while len(items) < cap:
            r = self._request("GET", f"{self.API}/search/repositories",
                              params={"q": q, "per_page": 100, "page": page})
            batch = r.json().get("items") or []
            items += batch
            if len(batch) < 100:
                break
            page += 1
        return items[:cap]

    def org_repos(self, org: str) -> list[dict]:
        items, page = [], 1
        while True:
            r = self._request("GET", f"{self.API}/orgs/{org}/repos",
                              params={"per_page": 100, "page": page, "type": "public"})
            batch = r.json()
            items += batch
            if len(batch) < 100:
                break
            page += 1
        return items

    def repo(self, full_name: str) -> dict:
        return self._request("GET", f"{self.API}/repos/{full_name}").json()

    def readme_conditional(self, full_name: str, etag: str | None):
        """ETag 条件请求 README。返回 (status, text, etag)。304 不计配额。

        Accept: raw 直拿 Markdown 原文；超 100KB 截断（头部 4KB + 目录段 4KB）。
        """
        r = self._request("GET", f"{self.API}/repos/{full_name}/readme",
                          etag=etag, accept="application/vnd.github.raw")
        if r.status_code == 304:
            return 304, None, etag
        text = r.text or ""
        truncated = False
        if len(text.encode("utf-8", "ignore")) > 100_000:
            text = text[:4000] + "\n\n[...截断...]\n\n" + text[4000:8000]
            truncated = True
        return 200, text, r.headers.get("ETag"), truncated  # type: ignore[return-value]

    # ---------------- 富集端点（Link header 计数：per_page=1 读 rel="last"） ----------------
    @staticmethod
    def _link_last_count(resp: requests.Response) -> int | None:
        """解析 Link header 的 rel="last" 页码作为总数；无 Link（单页）返回条数。"""
        link = resp.headers.get("Link", "")
        for part in link.split(","):
            if 'rel="last"' in part:
                for seg in part.split(";"):
                    if "page=" in seg:
                        try:
                            return int(seg.strip().split("page=")[-1].strip(" >&\"'"))
                        except ValueError:
                            break
        try:
            body = resp.json()
        except ValueError:
            return None
        return len(body) if isinstance(body, list) else None

    def commits_count(self, full_name: str, since_iso: str) -> int | None:
        """since 之后的 commit 数（Link 计数）。空结果返回 0；空仓库 409 视为 0
        （国产无星通道会捞到空仓，409 未处理曾炸掉整个富集 step）。"""
        try:
            r = self._request("GET", f"{self.API}/repos/{full_name}/commits",
                              params={"per_page": 1, "since": since_iso})
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 409:   # Git Repository is empty
                return 0
            raise
        return self._link_last_count(r) or 0

    def releases(self, full_name: str, per_page: int = 12) -> list[dict]:
        r = self._request("GET", f"{self.API}/repos/{full_name}/releases",
                          params={"per_page": per_page})
        return [x for x in r.json() if not x.get("draft")]

    def advisories(self, full_name: str, per_page: int = 30) -> list[dict]:
        r = self._request("GET", f"{self.API}/repos/{full_name}/security-advisories",
                          params={"per_page": per_page})
        return r.json()

    def contributors_count(self, full_name: str) -> int | None:
        """非匿名 contributor 总数（Link 计数）。"""
        r = self._request("GET", f"{self.API}/repos/{full_name}/contributors",
                          params={"per_page": 1, "anon": "false"})
        return self._link_last_count(r)

    def languages(self, full_name: str) -> dict[str, int]:
        """语言构成（字节数）。几乎不变，一次性采集。"""
        r = self._request("GET", f"{self.API}/repos/{full_name}/languages")
        return r.json()

    def participation(self, full_name: str, polls: int = 3) -> list[int] | None:
        """52 周每周 commit 数（含所有者提交）。慢端点：202=计算中，轮询几次。"""
        for i in range(polls):
            r = self._request("GET", f"{self.API}/repos/{full_name}/stats/participation")
            if r.status_code == 200:
                return (r.json() or {}).get("all")
            if r.status_code == 202 and i < polls - 1:
                time.sleep(5)
        return None

    def core_rate_limit(self) -> dict | None:
        """GET /rate_limit：官方明确不计入配额。返回 core 域 {remaining, reset}。

        ⚠ Actions GITHUB_TOKEN 上此端点与真实调用分属不同配额桶
        （09-30 实测：探测 remaining=5000 的同一秒，调用响应头 remaining=800），
        只能作本地 PAT 场景的预检参考；CI 的跨窗等待决策走 CoreReserveOut.reset。
        探测失败返回 None（按不限流处理，fail-open）。
        """
        try:
            r = self.s.get(f"{self.API}/rate_limit", timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            core = ((r.json() or {}).get("resources") or {}).get("core") or {}
            return {"remaining": core.get("remaining"), "reset": core.get("reset")}
        except (requests.RequestException, ValueError) as e:
            log.warning("/rate_limit 探测失败（按不限流处理）：%s", e)
            return None

    def stats_summary(self) -> dict:
        return {"calls": self.budget.calls,
                "elapsed_min": round((time.time() - self.budget.started) / 60, 1)}


def atomic_write_json(path: Path, obj) -> None:
    """原子写 + 三份轮转（照搬 history.json 模式）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    for i in (3, 2, 1):
        src, dst = path.with_suffix(path.suffix + f".{i}"), \
            path.with_suffix(path.suffix + f".{i+1}")
        if src.is_file():
            src.replace(dst)
    if path.is_file():
        path.replace(path.with_suffix(path.suffix + ".1"))
    tmp = path.with_suffix(path.suffix + ".tmp")
    # newline='\n'：本地 Windows 写出必须与 CI(Linux) 同为 LF，否则整文件
    # CRLF 翻转 → 全文件假 diff（10-10 回填 interp_state 实测 135K 行全变）
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    tmp.replace(path)
