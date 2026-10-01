# -*- coding: utf-8 -*-
"""数据库采集策略 · 声明式档案（单一事实源）。

每个库一份档案 → 四通道全部自动推导，清单间一致性由构造保证。
加一个新库 = 写一份档案；改口径 = 改开关字段。

通道字段说明：
  topics        GitHub topic 通道（含变体命名空间，如 postgres/sql-server）
  orgs          org 扫描通道；dict 形式可带 cadence
  search        关键词全文检索通道：None=关（词泛）/"auto"(纯词别名)/显式词列表
  watch         白名单兜底（内核/官方仓库/曾误杀项目）
  orgs.class    dedicated=org 即产品（无星线）/ cloud=云厂商超集 org（>=10 当范围噪音闸）；
                国产 org 必须 dict+class，国际 org 默认 star_min
  brand_infer   品牌词→库推断（canon 层：percona→MySQL+PostgreSQL）
  collisions    撞名词 → 排除规则（tdsql 撞 Teradata）
  known_empty   声明性空列（GitHub 无公开生态，不算采集故障）
  enabled=False 整库移出口径（矩阵列/canon/通道全撤）
"""

GLOBAL = {
    "star_min": 10,                 # 国际侧宇宙边界：信噪比线，不是编辑性排除
    "star_min_new": 3,
    "new_project_days": 30,
    # 分 section 采集策略（collect_intl.py / collect_cn.py 消费）：
    #   intl：topic/keyword 带 stars:>=10；新项目窗口 stars:>=3（主通道星线挡住的 3-9 星新仓）
    #   cn  ：国产不设星（生态总量小、星分布低；自标签 topic 与专属 org 即信号），
    #         故无需新项目窗口——新仓从第 0 天起即被主通道覆盖
    "sections": {
        "intl": {"star_min": 10, "new_star_min": 3, "new_days": 45},
        "cn":   {"star_min": 0,  "new_star_min": 0, "new_days": 45},
    },
    "search_qualifiers": "stars:>={star} fork:false",
    "per_page": 100,
    "max_pages": 10,                # GitHub Search 单查询 1000 条硬上限
    # 泛库发现桶：不挂任何库，用于多库/新工具发现；与四大库互斥（防重复抓大头）
    "discovery_topics": ["database"],
    "big_four": ["database", "mysql", "postgresql", "oracle"],
    "watch_insurance": ["OtterMind/Chat2DB"],
    # 仓库黑名单（人工拉黑）：与 DB 生态无关的误捞仓。全通道生效，双保险接线——
    # strategy 把它拼进全部搜索查询的 -repo:（keyword/topic 检索不再捞）
    # + pool_core 合并/并集时过滤兜底（org 列表 API 与历史池残留靠这层挡）
    # 加一条 = 往此列表加一项 "owner/repo"；与 watch 白名单互斥（validate ⑦ 检查）
    "exclude_repos": [],             # 当前为空；误捞仓优先加 config/exclude_users.txt（按整用户屏蔽）
    "tier_rules": {"empty": 0, "micro": 100, "small": 1000},
    # 范围外库（与任何库别名冲突时 strategy.validate 直接 FAIL）
    "out_of_scope_dbs": [
        "mongodb", "mongo", "redis", "valkey", "dragonfly", "kvrocks", "etcd",
        "cassandra", "scylla", "dynamodb", "couchdb", "couchbase",
        "hbase", "firebase", "firestore", "realmdb",
        "neo4j", "falkordb", "memgraph", "arangodb", "nebula",
        "qdrant", "milvus", "weaviate", "pinecone", "faiss", "lancedb", "chromadb",
        "vector database", "vector-database", "vector search", "vector-search",
        "vector store", "vector-store", "embedding database", "embeddings database",
        "elasticsearch", "opensearch", "meilisearch", "typesense", "solr",
        "manticore", "seekdb",
        "duckdb", "doris", "starrocks", "greenplum", "vertica",
        "trino", "prestodb", "bigquery", "redshift", "databricks",
        "influxdb", "timescaledb", "tdengine", "iotdb",
        "cockroach", "yugabyte", "singlestore", "memsql", "surrealdb",
        "libsql", "turso",
        "json database", "json file storage",
    ],
    # AI 信号词（板块 AI 判定用，规则版；正式判定走 README 结构化解读）
    "ai_keywords": ["ai", "llm", "gpt", "text2sql", "text-to-sql", "nl2sql",
                    "chat2db", "mcp server", "mcp-server", "agent", "copilot",
                    "rag", "embedding", "vector search", "ai-powered",
                    "ai agent", "openai", "claude", "deepseek"],
}

PROFILES = [
    # ============ 国际 7 库 ============
    {"name": "PostgreSQL", "section": "intl", "enabled": True,
     "aliases": ["postgres"],
     "topics": ["postgresql", "postgres"],          # +变体命名空间
     "orgs": ["postgres", "percona"],
     "search": None,
     "brand_infer": {"percona": ["MySQL", "PostgreSQL"]},
     "watch": ["postgres/postgres"],
     "notes": "postgres topic 为变体补扫；percona org+品牌词双修"},
    {"name": "MySQL", "section": "intl", "enabled": True,
     "aliases": ["mysql"],
     "topics": ["mysql", "mysql-database"],
     "orgs": ["mysql", "percona"],
     "search": None,
     "watch": ["mysql/mysql-server"],
     "notes": ""},
    {"name": "Oracle", "section": "intl", "enabled": True,
     "aliases": ["oracle"],
     "topics": ["oracle", "oracle-database"],
     "orgs": ["oracle"],
     "search": None,
     "watch": [],
     "notes": "oracle org 噪音（graal/oci）由范围层过滤"},
    {"name": "SQLite", "section": "intl", "enabled": True,
     "aliases": ["sqlite"],
     "topics": ["sqlite", "sqlite3"],
     "orgs": [],
     "search": "auto",
     "watch": ["sqlite/sqlite"],
     "notes": "★口径修复：移出范围外清单；topic 变体 sqlite/sqlite3 补齐"},
    {"name": "SQL Server", "section": "intl", "enabled": True,
     "aliases": [r"sql\s*server", "sqlserver", "mssql"],
     "topics": ["sqlserver", "sql-server"],         # +kebab 变体
     "orgs": [],
     "search": None,
     "watch": ["microsoft/go-mssqldb", "microsoft/mssql-jdbc"],
     "notes": "官方驱动不打 topic，白名单兜底"},
    {"name": "ClickHouse", "section": "intl", "enabled": True,
     "aliases": ["clickhouse"],
     "topics": ["clickhouse"],
     "orgs": ["ClickHouse"],
     "search": None,
     "watch": [],
     "notes": ""},
    {"name": "MariaDB", "section": "intl", "enabled": True,
     "aliases": ["mariadb"],
     "topics": ["mariadb"],
     "orgs": ["MariaDB"],
     "search": None,
     "watch": ["MariaDB/server"],
     "notes": ""},
    # ============ 国产 10 库 ============
    {"name": "TiDB", "section": "cn", "enabled": True,
     "aliases": ["tidb", "tikv"],
     "topics": ["tidb"],
     "orgs": [{"name": "pingcap", "class": "dedicated"},
              {"name": "tikv", "class": "dedicated"},
              {"name": "tidb-samples", "class": "dedicated"},
              {"name": "tidb-incubator", "class": "dedicated"}],
     "search": "auto",
     "watch": ["pingcap/tidb", "tikv/tikv"],
     "notes": "tikv 并入 TiDB；tidb-samples/incubator 为官方低星子 org（org 审计首轮补录）"},
    {"name": "OceanBase", "section": "cn", "enabled": True,
     "aliases": ["oceanbase"],
     "topics": ["oceanbase"],
     "orgs": [{"name": "oceanbase", "class": "dedicated"},
              {"name": "ApsaraDB", "class": "cloud"}],
     "search": "auto",
     "watch": ["oceanbase/oceanbase"],
     "notes": ""},
    {"name": "PolarDB", "section": "cn", "enabled": True,
     "aliases": ["polardb"],
     "topics": ["polardb", "polardb-x"],
     "orgs": [{"name": "polardb", "class": "dedicated"},
              {"name": "ApsaraDB", "class": "cloud"}],
     "search": "auto",
     "watch": ["polardb/PolarDB-for-PostgreSQL", "polardb/polardbx-engine"],
     "notes": "polardb 子串覆盖 polardb-x/polardbx"},
    {"name": "Dameng", "section": "cn", "enabled": True,
     "aliases": ["dm8", "dameng", "达梦", r"dm[- ]database"],
     "topics": ["dameng", "dm8"],
     "orgs": [],
     "search": "auto",                              # auto 展开纯词别名：dm8/dameng/达梦
     "watch": ["gaoyuan98/dameng_exporter", "Jackfinal/laravel-dm8",
               "nfjBill/gorm-driver-dm", "sjm1327605995/dm-xorm"],
     "notes": "中文词『达梦』进检索；裸 dm 歧义由词边界规则处理"},
    {"name": "openGauss", "section": "cn", "enabled": True,
     "aliases": ["opengauss"],
     "topics": ["opengauss"],
     "orgs": [{"name": "opengauss-mirror", "class": "dedicated"}],
     "search": "auto",
     "exclude_repos": ["math-inc/OpenGauss"],
     "watch": ["opengauss-mirror/openGauss-server"],
     "notes": "GitHub 为 mirror，org 是主通道"},
    {"name": "GaussDB", "section": "cn", "enabled": True,
     "aliases": ["gaussdb"],
     "topics": ["gaussdb"],
     "orgs": [{"name": "huaweicloud", "class": "cloud", "cadence": "weekly"}],
     "search": "auto",
     "watch": [],
     "notes": "云 SDK 噪音大，org 降频每周"},
    {"name": "GBase", "section": "cn", "enabled": True,
     "aliases": ["gbase"],
     "topics": ["gbase"],
     "orgs": [],
     "search": ['"gbase 8s"', '"gbase 8a"', '"gbase 8c"'],
     "watch": [],
     "notes": "三产品线短语检索防撞名"},
    {"name": "TDSQL", "section": "cn", "enabled": True,
     "aliases": ["tdsql"],
     "topics": ["tdsql"],
     "orgs": [{"name": "tencentcloud", "class": "cloud", "cadence": "weekly"}],
     "search": "auto",
     "collisions": {"teradata": "tdsql=Teradata SQL 缩写，命中 teradata 即排除"},
     "watch": [],
     "notes": ""},
    {"name": "YashanDB", "section": "cn", "enabled": True,
     "aliases": ["yashandb"],
     "topics": [{"name": "yashandb", "known_empty": True}],
     "orgs": [{"name": "yashan-technologies", "class": "dedicated"}],
     "search": "auto",
     "watch": [],
     "notes": "topic 实测 0，org 唯一路径"},
    {"name": "GoldenDB", "section": "cn", "enabled": True,
     "aliases": ["goldendb"],
     "topics": [{"name": "goldendb", "known_empty": True}],
     "orgs": [],
     "search": "auto",
     "watch": [],
     "known_empty": True,
     "notes": "GitHub 无公开生态（Gitee/内部），空列如实声明"},
]

# 口径遗留：建议移出白名单（不属于任何档案）
LEGACY_WATCH = {
    "cockroachdb/cockroach": "CockroachDB 不在 17 库口径",
    "duckdb/duckdb": "DuckDB 在范围外清单",
}
