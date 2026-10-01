# -*- coding: utf-8 -*-
"""rm_clean —— README 垃圾清理（喂模型前的预处理）。

实测 2000 篇抽样（v1）：代码块 20.2%、徽章 2.7%、许可/贡献节 1.6%、目录 0.5%。
前 1 万篇实测（v2，2026-09）：整体压缩 17% → 31%，前 1 万字符窗口多装 ~14% 内容。

v2 新增规则（逐条消融实测省量，占总残余 17%）：
  ⑦ 修 v1 徽章正则 bug：原第三分支要求 URL 以 badge|shield 开头，真实 URL
     以 https: 开头 → 纯图片式徽章行从未被删过（1 万篇中 4294 篇命中）
  ⑧ 行内图片/徽章只留 alt 文本（![SQL Server](badge…/supported) → SQL Server：
     alt 本身可能是唯一适配证据，宁留短文本不整行删）
  ⑨ 链接丢 URL 保文字（[text](url) → text，实测最大单项 -7.3%）
  ⑩ HTML：<a href>解包保内文，结构标签（p/div/table/br…）删除保内文
  ⑪ 表格对齐空格压缩（| a   | b   | → |a|b|，单元格内容不动）
  ⑫ 引用定义行（[ref]: url）删
  ⑬ 噪音章节正文换「（略）」：changelog/roadmap/community/用户列表/评价；
     license 只留正文首行（license_note 的依据）
  ⑭ 三字符水平线 ---/***/___ 删（v1 要求 4+ 字符，漏掉标准写法）

证据安全（interpret/db_scan 共用本清理器，两侧自动一致）：
  - 图片保 alt、链接保文字、HTML 保内文——被删的只有 URL/标签/空格/装饰；
  - evidence 引句核对走 _norm_txt（本来就剥链接与标签），新旧口径兼容；
  - 旧缓存按内容 sha 键控，不受清理器升级影响。

用法：python interpret/rm_clean.py 某文件.md   # 自测压缩率
"""
from __future__ import annotations
import re

RE_COMMENT = re.compile(r"<!--.*?-->", re.S)
# v1 曾有整行徽章正则，但 URL 前缀条件写错（要求以 badge|shield 开头）从未命中过
# 真实 URL（https: 开头）——v2 改由 _inline 统一处理：徽章/图片行解包后只剩 alt 文本。
RE_TOC_ITEM = re.compile(r"^\s*[-*+]?\s*\[[^\]]+\]\s*\(#\S*\)\s*$")
RE_SEP = re.compile(r"^\s*[-=*_]{3,}\s*$")          # v2：3+ 即删（v1 为 4+）
RE_SKIP_SECTION = re.compile(
    r"^\s{0,3}#{1,6}\s*(table of contents|contents|目录|sponsors?|赞助|捐赠|donate|donation|"
    r"contributing|贡献指南|贡献者|contributors?|code of conduct|行为准则|"
    r"acknowledgm?ents?|致谢|star history|badges?|"
    r"changelogs?|change ?logs?|release ?notes?|更新日志|更新记录|版本历史|what'?s new|"
    r"roadmaps?|路线图|规划|"
    r"communit(y|ies)|discussions?|slack|discord|gitter|zulip|社区|交流群?|联系我们|"
    r"contact( us)?|supports?|getting help|"
    r"who uses.*|adopters|users of.*|production users.*|谁在用|落地案例|case studies?|"
    r"testimonials?|what people say|用户评价|口碑)\s*$", re.I)
RE_LICENSE_SECTION = re.compile(
    r"^\s{0,3}#{1,6}\s*(licen[cs]es?|licen[cs]e[ &\w]*|许可|开源许可|许可证?)\s*$", re.I)
RE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+\S")
MAX_CODE_LINES = 6

# ---- v2 行内变换 ----
RE_IMG_ALT = re.compile(r"!\[([^\]]*)\]\([^)]*\)")                   # markdown 图片 → alt
RE_IMG_TAG = re.compile(r"<img\b[^>]*>")                              # <img> → alt
_RE_IMG_ALT_ATTR = re.compile(r"alt=[\"']([^\"']*)[\"']", re.I)


def _img_tag_repl(m) -> str:
    a = _RE_IMG_ALT_ATTR.search(m.group(0))
    return a.group(1) if a and a.group(1) else " "
RE_A_WRAP = re.compile(r"<a\s[^>]*>(.*?)</a>", re.I)
RE_TAG = re.compile(r"</?(?:p|div|center|b|i|em|strong|span|details|summary|br|"
                    r"h[1-6]|table|thead|tbody|tr|td|th|ul|ol|li|picture|source|"
                    r"sub|sup|kbd|font)\b[^>]*>|<br\s*/?>", re.I)
RE_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")                        # [text](url) → text
RE_REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+\S")                # [ref]: url 定义行
RE_TABLE_LINE = re.compile(r"^\s*\|.*\|\s*$")
RE_TABLE_CELL_WS = re.compile(r"\s*\|\s*")


def _inline(text: str) -> str:
    """行内噪音变换（代码块外逐行调用）。顺序要紧：图片先于链接，
    否则 ![alt](url) 会被链接规则拆成 "!alt"。"""
    t = RE_IMG_ALT.sub(r"\1", text)       # ![alt](url) → alt
    t = RE_A_WRAP.sub(r"\1", t)           # <a href>解包
    t = RE_IMG_TAG.sub(_img_tag_repl, t)  # <img alt="X"> → X
    t = RE_TAG.sub(" ", t)                # 结构标签删
    for _ in range(3):                    # 嵌套徽章 [![a](u)](u) 需两轮解包
        u = RE_LINK.sub(r"\1", t)
        if u == t:
            break
        t = u
    return re.sub(r"\s{2,}", " ", t)


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
        # license 节：标题保留 + 正文首行保留（license_note 依据），其余略
        if RE_LICENSE_SECTION.match(line):
            out.append(line)
            ln += 1
            while ln < len(lines) and not RE_HEADING.match(lines[ln]):
                body_line = _inline(lines[ln]).strip()
                ln += 1
                if body_line:
                    out.append(body_line)
                    break
            while ln < len(lines) and not RE_HEADING.match(lines[ln]):
                ln += 1
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
        if RE_REFDEF.match(line) or RE_SEP.match(line):
            ln += 1
            continue
        # v2 行内变换 + 表格空格压缩
        line = _inline(line)
        if RE_TABLE_LINE.match(line):
            line = RE_TABLE_CELL_WS.sub("|", line.strip())
        if line.strip():
            out.append(line)
        elif out and out[-1].strip():
            out.append("")
        ln += 1
    # 空行压缩
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return cleaned.strip()


if __name__ == "__main__":   # 快速自测：python interpret/rm_clean.py 某文件.md
    import sys
    src = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    dst = clean_readme(src)
    print(f"{len(src)} -> {len(dst)} 字（压缩 {100 - len(dst) * 100 // max(len(src), 1)}%）")
