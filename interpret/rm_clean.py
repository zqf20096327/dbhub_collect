# -*- coding: utf-8 -*-
"""rm_clean —— README 垃圾清理（喂模型前的预处理）。

实测 2000 篇抽样：代码块占 20.2%、徽章 2.7%、许可/贡献节 1.6%、目录 0.5%
——清理后提示词省 ~25-30%，且 1 万字窗口能多装约三成真实内容（支持矩阵等）。

规则（保守，宁少删不误删证据）：
  ① HTML 注释整段删
  ② 徽章行（markdown badge / <a><img/>）删
  ③ 导航类章节（目录/赞助/贡献指南/行为准则/致谢/star history）标题保留、正文换「（略）」
  ④ 链接列表式目录（连续 ≥4 行 [文字](#锚点)）删
  ⑤ 超长代码块（>6 行）保留语言行+前 3 行，余者「…（N 行代码略）」
     ——保留前 3 行是刻意的：docker run / pip install 等安装证据通常在头部
  ⑥ 分隔线、连续空行压缩
"""
from __future__ import annotations
import re

RE_COMMENT = re.compile(r"<!--.*?-->", re.S)
RE_BADGE = re.compile(r"^\s*(?:\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)|"
                      r"<a\s[^>]*>\s*<img[^>]*>\s*</a>|!\[[^\]]*\]\((?:badge|shield)[^)]*\))\s*$",
                      re.I)
RE_TOC_ITEM = re.compile(r"^\s*[-*+]?\s*\[[^\]]+\]\s*\(#\S*\)\s*$")
RE_SEP = re.compile(r"^\s*[-=*_]{4,}\s*$")
RE_SKIP_SECTION = re.compile(
    r"^\s{0,3}#{1,6}\s*(table of contents|contents|目录|sponsors?|赞助|捐赠|donate|donation|"
    r"contributing|贡献指南|贡献者|contributors?|code of conduct|行为准则|"
    r"acknowledgm?ents?|致谢|star history|badges?)\s*$", re.I)
RE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+\S")
MAX_CODE_LINES = 6


def clean_readme(text: str) -> str:
    t = RE_COMMENT.sub(" ", text or "")
    out, i, n = [], 0, len(t)
    lines = t.split("\n")
    ln = 0
    while ln < len(lines):
        line = lines[ln]
        # 代码块处理
        if line.strip().startswith("```"):
            block = [line]
            ln += 1
            while ln < len(lines) and not lines[ln].strip().startswith("```"):
                block.append(lines[ln])
                ln += 1
            if ln < len(lines):
                block.append(lines[ln])  # 收尾 ```
                ln += 1
            if len(block) > MAX_CODE_LINES + 2:
                kept = block[:4] + [f"…（{len(block) - 5} 行代码略）"] + [block[-1]]
                out.extend(kept)
            else:
                out.extend(block)
            continue
        # 章节跳过：标题保留，正文换（略）
        if RE_SKIP_SECTION.match(line):
            out.append(line)
            ln += 1
            body = 0
            while ln < len(lines) and not RE_HEADING.match(lines[ln]):
                ln += 1
                body += 1
            if body:
                out.append("（略）")
            continue
        # 链接式目录：连续 ≥4 行
        if RE_TOC_ITEM.match(line):
            run = 0
            while ln + run < len(lines) and RE_TOC_ITEM.match(lines[ln + run]):
                run += 1
            if run >= 4:
                out.append(f"（目录 {run} 行略）")
                ln += run
                continue
        if RE_BADGE.match(line) or RE_SEP.match(line):
            ln += 1
            continue
        out.append(line)
        ln += 1
    # 空行压缩
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return cleaned.strip()


if __name__ == "__main__":   # 快速自测：python interpret/rm_clean.py 某文件.md
    import sys
    src = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    dst = clean_readme(src)
    print(f"{len(src)} -> {len(dst)} 字（压缩 {100 - len(dst) * 100 // max(len(src), 1)}%）")
