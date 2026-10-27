# 快捷创建达梦数据库表创建脚本、索引创建、注释添加

## 安装依赖

### Python
```pip install pypinyin```
### Java
```
<dependency>
    <groupId>com.belerweb</groupId>
    <artifactId>pinyin4j</artifactId>
    <version>2.5.0</version>
</dependency>
```

## 按需修改
自动根据库名、字段名取拼音首字母大写作为字段名
```
# 公有字段
common_columns = [
    ("DEL_FLAG", "INT", "是否删除", 0),
    ("CREATE_BY", "VARCHAR(100)", "创建人"),
    ("CREATE_TIME", "TIMESTAMP(6)", "创建时间"),
    ("UPDATE_BY", "VARCHAR(100)", "修改人"),
    ("UPDATE_TIME", "TIMESTAMP(6)", "修改时间")
]
# 库名
schema_name = "TEST"
# 表名公共前缀
table_name_prefix = "TS_"
# 表名
table_name_cn = "测试表"
# 表字段
columns_cn = [
    ("标题", "VARCHAR(100)"),
    ("时间", "TIMESTAMP(6)"),
    ("状态", "INT", 0)
]
# 常规索引字段
index_columns = ["标题", "状态"]
# 唯一索引字段 ["标题", "状态", "标题,状态"]
unique_index_columns = []
```

## 生成语句
```
CREATE TABLE "TEST"."TS_CSB"
(
    "ID" INT AUTO_INCREMENT NOT NULL,
    "BT" VARCHAR(100),
    "SJ" TIMESTAMP(6),
    "ZT" INT DEFAULT 0,
    "DEL_FLAG" INT DEFAULT 0,
    "CREATE_BY" VARCHAR(100),
    "CREATE_TIME" TIMESTAMP(6),
    "UPDATE_BY" VARCHAR(100),
    "UPDATE_TIME" TIMESTAMP(6),
    CONSTRAINT "CSB_PK" NOT CLUSTER PRIMARY KEY("ID")
) STORAGE(ON "MAIN", CLUSTERBTR) AUTO_INCREMENT = 1;

CREATE INDEX "CSB_ID_IDX" ON "TEST"."TS_CSB" ("ID");
CREATE INDEX "CSB_BT_IDX" ON "TEST"."TS_CSB" ("BT");
CREATE INDEX "CSB_ZT_IDX" ON "TEST"."TS_CSB" ("ZT");

COMMENT ON TABLE "TEST"."TS_CSB" IS '测试表';

COMMENT ON COLUMN "TEST"."TS_CSB"."ID" IS '主键';
COMMENT ON COLUMN "TEST"."TS_CSB"."BT" IS '标题';
COMMENT ON COLUMN "TEST"."TS_CSB"."SJ" IS '时间';
COMMENT ON COLUMN "TEST"."TS_CSB"."ZT" IS '状态';
COMMENT ON COLUMN "TEST"."TS_CSB"."DEL_FLAG" IS '是否删除';
COMMENT ON COLUMN "TEST"."TS_CSB"."CREATE_BY" IS '创建人';
COMMENT ON COLUMN "TEST"."TS_CSB"."CREATE_TIME" IS '创建时间';
COMMENT ON COLUMN "TEST"."TS_CSB"."UPDATE_BY" IS '修改人';
COMMENT ON COLUMN "TEST"."TS_CSB"."UPDATE_TIME" IS '修改时间';
```
