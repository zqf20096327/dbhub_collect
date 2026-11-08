# -*- coding: utf-8 -*-
"""runner 机制自检（工作清单 G4-3 前置）：断点、超时重试、限流退避、额度等待。

不花钱：requests.post 全部打桩，不触网；sleep 打桩只记录不真等。

覆盖：
  A) 读超时 2 次后成功 → tries=3
  B) 额度 1113 两次 → 每次等 600s，第 3 次成功 → tries=3
  C) 普通 429 一次 → 短退避后成功 → tries=2
  D) 500 一次 → 重试成功 → tries=2
  E) ask()：模型输出违规 → 带原因重试一次 → tries 累加、最终通过
  F) 断点：state 记 done 后 pending 为空；sha 变化后重新入队

用法：python interpret/selftest_runner.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

os.environ.setdefault("AI_API_KEY", "selftest-key")     # AIClient 构造只需非空

import interpret as itp                      # noqa: E402
import vocab_control as vc                   # noqa: E402
import run_domain_tags as rd                 # noqa: E402
from interp_layer_store import LayerStore     # noqa: E402


class Resp:
    def __init__(self, code=200, body=None, text=""):
        self.status_code = code
        self._body = body or {"choices": [{"message": {"content": '{"ok":1}'},
                                          "finish_reason": "stop"}]}
        self.text = text or ("" if code == 200 else "err")

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class Sleep:
    def __init__(self):
        self.calls = []

    def __call__(self, secs):
        self.calls.append(secs)


def run_script(steps):
    """steps = [Resp | Exception, ...]；返回 (client, chat 结果, sleep 记录)。"""
    sleeps = Sleep()
    seq = list(steps)
    orig_post, orig_sleep = itp.requests.post, itp.time.sleep

    def fake_post(*a, **kw):
        step = seq.pop(0)
        if isinstance(step, Exception):
            raise step
        return step

    itp.requests.post = fake_post
    itp.time.sleep = sleeps
    try:
        c = itp.AIClient(deadline=None)
        out = c.chat("x")
    finally:
        itp.requests.post = orig_post
        itp.time.sleep = orig_sleep
    return out, sleeps.calls


def main() -> int:
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    # A) 读超时重试
    out, sl = run_script([itp.requests.exceptions.Timeout(),       # type: ignore[attr-defined]
                          itp.requests.exceptions.Timeout(),       # type: ignore[attr-defined]
                          Resp(200)])
    chk("超时 2 次后成功，tries=3", out["tries"] == 3)

    # B) 额度 1113 等待
    out, sl = run_script([Resp(429, text='{"code":"1113"}'),
                          Resp(429, text='{"code":"1113"}'),
                          Resp(200)])
    chk("额度 1113 两次后成功，tries=3", out["tries"] == 3)
    chk("额度等待每次 600s", sl == [600, 600])

    # C) 普通限流
    out, sl = run_script([Resp(429, text="rate limited"), Resp(200)])
    chk("普通 429 退避后成功，tries=2", out["tries"] == 2)
    chk("普通 429 退避非 600s", sl and sl[0] < 600)

    # D) 服务端 500
    out, sl = run_script([Resp(500, text="boom"), Resp(200)])
    chk("500 重试后成功，tries=2", out["tries"] == 2)

    # E) 校验失败带原因重试
    vocab = vc.load_vocab()
    allowed = vc.all_slugs(vocab)
    pack = {"desc": "", "topics": "", "headings": "", "install": "",
            "matched": "L1|cdc", "lines": {1}, "numbered": {1: "cdc"}}
    bad = '{"tags":[{"slug":"not-a-slug","line":1,"conf":"high"}],"abstain":null,"gap":null}'
    good = '{"tags":[{"slug":"cdc","line":1,"conf":"high"}],"abstain":null,"gap":null}'

    class FakeClient:
        model = "fake"

        def __init__(self):
            self.prompts = []

        def chat(self, prompt, timeout=300):
            self.prompts.append(prompt)
            content = bad if len(self.prompts) == 1 else good
            return {"content": content, "tries": 1}

    fc = FakeClient()
    res, errs, tries = rd.ask(fc, "base", allowed, pack)
    chk("校验失败后带原因重试并最终通过", res is not None and tries == 2)
    chk("重试提示包含拒收原因", "词表外" in fc.prompts[1] or "被拒" in fc.prompts[1])

    # F) 断点台账
    with tempfile.TemporaryDirectory() as td:
        st = LayerStore("domain_tags", Path(td))
        st.load()
        st.mark("a/x", "sha1", "done")
        chk("已 done 的条目不重复入队", st.pending([("a/x", "sha1")]) == [])
        chk("sha 变化后重新入队", st.pending([("a/x", "sha2")]) == [("a/x", "sha2")])
        st.mark("a/y", "sha1", "rejected")
        chk("拒收不进 done（除非 --retry-rejected）",
            st.pending([("a/y", "sha1")]) == [("a/y", "sha1")])

    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
