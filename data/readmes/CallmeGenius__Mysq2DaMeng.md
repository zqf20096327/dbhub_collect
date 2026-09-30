# MySQL到DM数据库转换工具

## 项目简介

这是一个用于将MySQL数据库SQL脚本转换为达梦数据库(DM)SQL脚本的Python工具。该工具支持批量转换，能够处理表结构创建、数据插入、索引定义等SQL语句。

## 功能特性

- ✅ 支持MySQL到DM数据类型的自动映射
- ✅ 自动转换表名、字段名为大写
- ✅ 将auto_increment转换为IDENTITY(1,1)
- ✅ 转换注释语法为DM格式
- ✅ 支持批量文件转换
- ✅ 自动生成转换报告
- ✅ 详细的日志记录
- ✅ 转换结果验证

## 项目结构

```
mysql_to_dm_converter/
├── mysql_to_dm_converter.py    # 主转换脚本
├── config/
│   ├── data_type_mapping.json  # 数据类型映射配置
│   └── conversion_rules.json   # 转换规则配置
├── utils/
│   ├── sql_parser.py           # SQL解析工具
│   ├── sql_converter.py        # SQL转换工具
│   └── file_processor.py       # 文件处理工具
├── logs/                       # 日志目录
├── requirements.txt            # 依赖包
└── README.md                   # 使用说明
```

## 安装和使用

### 1. 环境要求

- Python 3.7+
- 无需安装额外的第三方库（使用Python标准库）

### 2. 使用方法

#### 转换整个项目
```bash
python mysql_to_dm_converter.py --project /path/to/project
```

#### 转换单个文件
```bash
python mysql_to_dm_converter.py --source /path/to/mysql/file.sql --target /path/to/dm/file.sql
```

#### 转换目录
```bash
python mysql_to_dm_converter.py --source /path/to/mysql/dir --target /path/to/dm/dir
```

#### 验证转换结果
```bash
python mysql_to_dm_converter.py --source file.sql --target file.sql --validate
```

#### 详细输出
```bash
python mysql_to_dm_converter.py --project /path/to/project --verbose
```

### 3. 命令行参数

- `--source, -s`: 源文件或目录路径
- `--target, -t`: 目标文件或目录路径
- `--project, -p`: 项目根目录路径
- `--validate, -v`: 验证转换结果
- `--verbose`: 详细输出

## 配置说明

### 数据类型映射配置 (config/data_type_mapping.json)

```json
{
  "data_types": {
    "bigint": "BIGINT",
    "int": "INT",
    "tinyint": "SMALLINT",
    "varchar": "VARCHAR",
    "text": "TEXT",
    "datetime": "DATETIME",
    "timestamp": "TIMESTAMP",
    "decimal": "DECIMAL",
    "float": "FLOAT",
    "double": "DOUBLE",
    "char": "CHAR",
    "blob": "BLOB",
    "longtext": "TEXT",
    "mediumtext": "TEXT",
    "json": "TEXT"
  }
}
```

### 转换规则配置 (config/conversion_rules.json)

```json
{
  "case_conversion": {
    "table_names": "UPPER",
    "column_names": "UPPER",
    "keywords": "UPPER"
  },
  "syntax_conversion": {
    "auto_increment": "IDENTITY(1,1)",
    "comment_syntax": "COMMENT_ON"
  }
}
```

## 转换规则

### 1. 数据类型转换

| MySQL数据类型 | DM数据类型 | 说明 |
|--------------|-----------|------|
| `bigint` | `BIGINT` | 大整数类型，保持原样 |
| `int` | `INT` | 整数类型，保持原样 |
| `tinyint` | `SMALLINT` | 小整数类型，转换为SMALLINT |
| `varchar(n)` | `VARCHAR(n)` | 可变长度字符串，保持原样 |
| `text` | `TEXT` | 长文本类型，保持原样 |
| `datetime` | `DATETIME` | 日期时间类型，保持原样 |
| `timestamp` | `TIMESTAMP` | 时间戳类型，保持原样 |
| `decimal(m,d)` | `DECIMAL(m,d)` | 精确小数类型，保持原样 |

### 2. 语法转换

#### CREATE TABLE语句
**MySQL格式**:
```sql
create table table_name
(
    id bigint auto_increment primary key,
    name varchar(50) null comment '字段注释'
)
comment '表注释';
```

**DM格式**:
```sql
CREATE TABLE TABLE_NAME (
    ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    NAME VARCHAR(50) NULL
);

-- 添加表注释
COMMENT ON TABLE TABLE_NAME IS '表注释';

-- 添加字段注释
COMMENT ON COLUMN TABLE_NAME.NAME IS '字段注释';
```

#### INSERT语句
**MySQL格式**:
```sql
INSERT INTO emergency_basedam.sel_dict (id, code, caption) VALUES (1, 'test', '测试');
```

**DM格式**:
```sql
INSERT INTO EMERGENCY_BASEDAM.SEL_DICT (ID, CODE, CAPTION) VALUES (1, 'test', '测试');
```

### 3. 大小写规范

- 表名: 全部大写，如 `EMERGENCY_DICTIONARY`
- 字段名: 全部大写，如 `DICT_ID`
- 关键字: 全部大写，如 `CREATE`, `TABLE`, `PRIMARY KEY`

## 输出文件

### 1. 转换后的SQL文件

转换后的文件保存在对应的`dmsql`目录中，文件名保持不变。

### 2. 日志文件

- `logs/conversion.log`: 详细的转换日志
- `logs/conversion_report.txt`: 转换完成报告

### 3. 报告内容

转换报告包含以下信息：
- 转换时间
- 总文件数
- 成功转换数
- 转换失败数
- 成功率
- 错误详情

## 注意事项

1. **备份**: 转换前务必备份源文件
2. **测试**: 建议在测试环境中先进行转换测试
3. **验证**: 转换完成后请验证转换结果的正确性
4. **字符集**: 确保DM数据库使用UTF-8字符集

## 常见问题

### Q: 转换失败怎么办？
A: 查看日志文件`logs/conversion.log`获取详细错误信息，根据错误提示进行修复。

### Q: 如何自定义数据类型映射？
A: 修改`config/data_type_mapping.json`文件中的映射关系。

### Q: 如何修改转换规则？
A: 修改`config/conversion_rules.json`文件中的转换规则。

### Q: 支持哪些SQL语句？
A: 目前支持CREATE TABLE、INSERT INTO、CREATE INDEX等基本语句。

## 版本信息

- 版本: v1.0
- 创建时间: 2025-08-20
- 维护人员: chenyejian

## 许可证

本项目仅供内部使用。
