# -*- coding: utf-8 -*-
"""domain_tags 影子运行：词表提取 + 影子 prompt 渲染（一次性工具，不入生产链）。
来源：《受控词表v0.10（A类修复版）.md》§0 格式规格。
只读文档、只产 state/shadow/ 下的报告；不写 interp_cache / interp_state。"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(d))

DOC = Path.home() / "OneDrive" / "桌面" / "受控词表v0.10（A类修复版）.md"
OUT = ROOT / "state" / "shadow"
OUT.mkdir(parents=True, exist_ok=True)

# v0.11 草案（1107 补 platform 域缺口）：500 抽样显示 cat=平台 的项目
# 无词可用（platform 域仅 operator/dbaas，命中 2），实际形态集中在
# 语义层 / 数据库分支 / BaaS / 本地多实例管理。待人工定稿后并入词表文档。
EXTRA_PLATFORM = [
    {"slug": "semantic-layer", "cn": "语义层",
     "def": "BI/指标的统一语义建模层，≠analytics"},
    {"slug": "db-branching", "cn": "数据库分支",
     "def": "秒级克隆/分支库用于开发测试"},
    {"slug": "baas", "cn": "后端即服务",
     "def": "托管后端与数据库一体化平台"},
    {"slug": "local-db-manager", "cn": "本地实例管理",
     "def": "本机多版本数据库实例启停管理"},
]
VOCAB_VER = "0.11-draft"

# 超短定义（人工按文档第 4 列语义重写：8-15 字、保留 ≠ 边界；机械截断会切出残句）
SHORT = {
    "cdc": "日志流实时捕获行级变更，≠data-sync",
    "binlog": "解析事务日志为事件的底层库，≠cdc",
    "etl": "跨源抽取-转换-加载，≠stream-processing",
    "data-sync": "库/端间批量或定时搬运，≠cdc",
    "data-pipeline": "多级处理流水线通称（兜底）",
    "replication": "库实例间保持副本一致，≠cdc",
    "stream-processing": "数据流实时计算（窗口/聚合）",
    "kafka-connect": "实现 Kafka Connect 框架的连接器",
    "backup": "物理或逻辑备份数据库，≠replication",
    "restore": "从备份重建数据库",
    "dump": "导出为 SQL/文本的工具形态",
    "snapshot": "基于存储/文件系统的时点副本",
    "pitr": "按 WAL/binlog 回放任意时点",
    "schema-migration": "schema 变更版本化管理执行",
    "data-migration": "跨库/跨版本一次性搬迁数据",
    "dialect-rewrite": "SQL 方言间语法转换工具",
    "pooler": "数据库连接池化管理，≠proxy",
    "proxy": "代理协议居中转发/改写请求",
    "router": "按规则路由到不同后端，含分库分表",
    "load-balancer": "对请求/节点做负载均衡",
    "jdbc": "实现 JDBC 接口的驱动",
    "odbc": "ODBC 协议驱动",
    "driver": "语言级连接驱动/客户端库，≠jdbc",
    "orm": "对象模型与关系表映射层",
    "query-builder": "链式 API 构造 SQL，≠orm",
    "mapper": "手写 SQL + 对象映射框架",
    "exporter": "按 Prometheus 格式暴露指标",
    "metrics": "采集/存储数据库运行指标",
    "slow-query": "慢查询日志采集与分析",
    "query-analytics": "查询负载统计与优化建议",
    "dashboard": "监控可视化面板",
    "alerting": "基于阈值的告警",
    "observability": "日志+指标+追踪合称（兜底）",
    "admin-cli": "数据库管理命令行工具",
    "gui-client": "图形界面数据库客户端",
    "web-console": "浏览器访问的管理控制台",
    "sql-editor": "以编写/执行 SQL 为主业的编辑器",
    "benchmark": "数据库性能基准测试",
    "test-data": "生成测试/伪造数据填充",
    "fuzzing": "对 DB/SQL 模糊测试找缺陷",
    "sql-linter": "SQL 风格规范检查/格式化",
    "chaos": "注入故障验证数据库韧性",
    "erd": "从库/模型生成或编辑 ER 图",
    "data-modeling": "设计期数据建模工具",
    "schema-design": "表结构可视化设计并输出 DDL",
    "audit-log": "数据库操作审计记录",
    "data-masking": "敏感数据脱敏/匿名化",
    "access-control": "数据库访问权限控制",
    "sql-firewall": "拦截危险 SQL",
    "encryption": "存储/传输层加密",
    "failover": "主库故障时自动切换从库",
    "orchestration": "实例部署编排自动化",
    "switchover": "计划内主从切换",
    "storage-engine": "可插拔/独立存储引擎实现",
    "columnar": "列式存储引擎/加速器",
    "distributed-sql": "分布式 SQL 引擎",
    "htap": "混合事务分析引擎",
    "time-series": "时序存储引擎/扩展",
    "embedded": "进程内嵌入式数据库",
    "parser": "SQL 词法语法解析库",
    "optimizer": "查询计划优化实现/研究",
    "operator": "K8s 上管理数据库的 Operator",
    "dbaas": "数据库即服务平台",
    "vector-search": "向量近邻检索引擎/扩展",
    "embedding-store": "面向 embedding 的存储，≠vector-search",
    "semantic-search": "基于语义理解的文本检索",
    "knowledge-graph": "图谱构建/图存储与检索",
    "agent-memory": "为 LLM agent 提供持久记忆",
    "data-export": "查询结果/表数据导出文件",
    "csv-tool": "CSV 与库互转工具",
    "analytics": "BI/报表/即席分析，≠query-analytics",
}


def strip_md(s: str) -> str:
    s = re.sub(r"\*\*", "", s or "")
    s = re.sub(r"\s*（候选档[^）]*）", "", s)
    s = s.replace("✓", "").replace("⟳", "")      # 词频背书/环增补图例不进 prompt
    return re.sub(r"\s+", " ", s).strip()


def short_def(slug: str, cell: str) -> str:
    """优先用人工超短定义；缺失时退回文档第 4 列机械压缩（并在输出里标记）。"""
    if slug in SHORT:
        return SHORT[slug]
    parts = [p.strip() for p in strip_md(cell).split("↔")]
    main = re.split(r"[；。，]", re.sub(r"（[^）]*）", "", parts[0]))[0].strip(" /、")
    return (main[:15].rstrip(" /、-") or parts[0][:15]) + "［机］"


def parse_vocab() -> dict:
    text = io.open(DOC, encoding="utf-8").read()
    lines = text.splitlines()
    domains, cur = [], None
    for ln in lines:
        m = re.match(r"^### 域[一二三四五六七八九十]+ ([a-z\-]+) ([^（]+)（(\d+) 词）", ln)
        if m:
            cur = {"domain": m.group(1), "cn": m.group(2).strip(), "words": []}
            domains.append(cur)
            continue
        if cur is None or not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.match(r"^[a-z][a-z0-9\-]+$", cells[0]):
            continue
        if cells[1] in ("中文", "slug"):        # 表格表头行
            continue
        cur["words"].append({"slug": cells[0], "cn": strip_md(cells[1]),
                             "syn": strip_md(cells[2]),
                             "def": short_def(cells[0], cells[3])})
    # v0.11 草案：把 4 个平台域补词并进 platform 域
    for d in domains:
        if d["domain"] == "platform":
            d["words"].extend([dict(w, draft=True) for w in EXTRA_PLATFORM])
    return {"vocab_ver": VOCAB_VER, "domains": domains,
            "n_words": sum(len(d["words"]) for d in domains)}


def vocab_block(v: dict) -> str:
    """§0 呈现格式：[域] slug 中文名 / 每词 slug: 中文名——超短定义。同义词环不进 prompt。"""
    out = []
    for d in v["domains"]:
        out.append(f"[域] {d['domain']} {d['cn']}")
        for w in d["words"]:
            out.append(f"{w['slug']}: {w['cn']}——{w['def']}")
        out.append("")
    return "\n".join(out).rstrip()


def shadow_schema(base_v4: str, vblock: str) -> str:
    """生产 SCHEMA_V4 原样 + domain_tags 字段（写进 classification）+ 词表区块。
    词表插在硬规则之前（规则贴尾部，遵守率最高）。"""
    ai_line = ('   "ai_kind": "mcp|rag|text2sql|dba-agent|other 之一'
               '（【必填，不许省略】——非 AI 项目也必须输出 other）"\n')
    assert ai_line in base_v4, "SCHEMA_V4 结构变了，影子脚本需同步"
    field = ai_line.rstrip("\n") + ",\n" + (
        '   "domain_tags": ["0-3 个词表 slug（只能取下方词表）；只标 README 有明确依据的，'
        '宁缺勿编；无依据时输出空数组 []"]\n')
    schema = base_v4.replace(ai_line, field)
    marker = "硬规则（违反即拒收）："
    assert marker in schema
    schema = schema.replace(marker, "可用词表（domain_tags 只能取下列 slug，词表外 slug 视为无依据）：\n"
                            + vblock + "\n\n" + marker)
    return schema


if __name__ == "__main__":
    v = parse_vocab()
    (OUT / "domain_vocab_v0.10.json").write_text(
        json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    blk = vocab_block(v)
    print(f"词条 {v['n_words']} / 域 {len(v['domains'])} / 区块 {len(blk.encode())} B")
    if "--block" in sys.argv:
        print(blk)
