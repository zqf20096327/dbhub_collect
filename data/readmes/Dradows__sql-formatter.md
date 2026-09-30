# GaussDB SQL Formatter

面向 GaussDB（兼容 PostgreSQL 语法）的 VSCode 离线 SQL 格式化插件。
单文件 `.vsix` 导入即用，无需联网、无需任何运行时依赖。

## 核心特性

- **平台特色内容不修改**
  - 以 `@` 开头的整行（如 `@set ...`、`@hint ...`、`@{...}`）**原样保留**，并作为语句级分隔符，前后语句独立格式化；
  - `${...}` 参数（如 `${bizdate}`、`${min_amount:100}`）整体视为一个原子 token，**内部内容绝不被拆改**，也不受大小写转换影响；`$1`、`$2` 等位置参数同理；
  - 字符串、注释、美元引号（`$$...$$`、`$tag$...$tag$`）内容一律原样保留，内部的逗号、分号、括号不会干扰格式化。
- **逗号前导的多字段列表**（默认 block 风格）
  - 多行多字段语句拆行后，**逗号放在下一行句首**；
  - 列表项与首字段行对齐（首行相对逗号行多出“逗号 + 空格”的对齐量）。
- **关键字统一大写**（表名、字段名、字符串、参数保持原样），可配置为小写或保留。
- **智能拆行**：输入本身跨多行，或单行超过 `maxLineLength`（默认 120）时拆行；单行短语句保持单行。
- 支持 SELECT / INSERT / UPDATE / DELETE / CREATE TABLE / MERGE / WITH(CTE) / 子查询 / JOIN / UNION / CASE WHEN / 窗口函数(OVER) / CONNECT BY / GRANT 等常见 GaussDB 语法。

## 安装（内网/离线）

1. 将 `gaussdb-sql-formatter-1.0.1.vsix` 拷贝到内网机器；
2. VSCode 中：`扩展` 视图 → 右上角 `...` → `从 VSIX 安装...`，选择该文件；
3. 重启（或自动生效）后即可使用。

> 命令行安装：`code --install-extension gaussdb-sql-formatter-1.0.1.vsix`

## 使用

- 打开 `.sql` 文件（内置 `sql` 语言）或语言 ID 为 `gaussdb` 的文件；
- **格式化文档**：`Shift+Alt+F`（或右键 → 格式化文档）；
- **格式化选中语句**：选中一段 SQL 后 `Ctrl+K Ctrl+F`（选区会自动扩展到其所在完整语句，保证分号/`@` 行不被破坏）；
- **保存时自动格式化**：在 `settings.json` 中配置：

```json
{
  "[sql]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "gaussdb-tools.gaussdb-sql-formatter"
  },
  "[gaussdb]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "gaussdb-tools.gaussdb-sql-formatter"
  }
}
```

如果文件关联到了其他语言，可添加：

```json
{
  "files.associations": { "*.gaussdb.sql": "gaussdb" }
}
```

## 格式风格

### block（默认）：关键字独占一行

```sql
SELECT
    a.col1
  , a.col2
  , a.col3
FROM
    table_a a
WHERE
    a.col1 = 1
    AND a.col2 = 2
```

- 列表项缩进 = `2 × indentSize`（默认 4 空格），逗号行缩进 = `indentSize`（默认 2 空格）；
- `AND`/`OR` 条件行缩进 = `2 × indentSize`，与 `ON` 同级且条件列对齐；
- 带对象的关键字（`INSERT INTO t (...)`、`UPDATE t`、`CREATE TABLE t (`）与对象同行；
- **`JOIN` 家族（`JOIN`/`LEFT JOIN`/...）与表名同行**，`ON` 缩进 `2 × indentSize` 且与条件同行：

```sql
FROM
    table_a a
LEFT JOIN table_b b
    ON  b.id = a.id
    AND b.name = 'x'
LEFT JOIN (
    SELECT
        id
    FROM
        table_c
) c
    ON  c.id = b.cid
```

- 子查询、IN 列表、函数参数等括号组按所在行的条目列继续缩进。

### aligned：关键字与首字段同行，逗号列对齐

```sql
SELECT a.col1
     , a.col2
     , a.col3
  FROM table_a a
 WHERE a.col1 = 1
   AND a.col2 = 2
```

## 设置项

| 设置 | 默认 | 说明 |
| --- | --- | --- |
| `gaussdbSqlFormatter.keywordCase` | `upper` | 关键字大小写：`upper` / `lower` / `preserve` |
| `gaussdbSqlFormatter.clauseStyle` | `block` | 子句排版：`block`（关键字独占一行）/ `aligned`（行内对齐） |
| `gaussdbSqlFormatter.indentSize` | `2` | 基础缩进宽度 |
| `gaussdbSqlFormatter.maxLineLength` | `120` | 超过该长度拆行；短字段列表的行尾 `--` 注释会在此范围内对齐；`0` 表示不限制行宽 |
| `gaussdbSqlFormatter.breakMode` | `auto` | `auto`（跨行或超长）/ `input`（仅跨行）/ `length`（仅超长）/ `never`（不拆行） |

`SELECT` 字段的行尾 `--` 注释按整个字段列表对齐，支持跨多行的 `CASE … END` 等表达式；子查询中的字段列表单独对齐。注释前至少保留两个空格，如果对齐后任一注释行超过 `maxLineLength`，该组保持原有间距。

## 样例

- `samples/complex_gaussdb.sql` —— 未格式化的复杂 SQL（覆盖 `@` 语句、`${}` 参数、CTE、子查询、CASE、窗口函数、CONNECT BY、多行 VALUES、建表、注释等）；
- `samples/complex_gaussdb.formatted.sql` —— 对应格式化结果（与默认设置完全一致，由测试保证）。

## 内容守恒保证

插件保证**格式化绝不改变 SQL 的内容**：除关键字大小写（由 `keywordCase` 控制）外，所有标识符、字符串、数字、参数、运算符、括号、逗号、分号、注释、`@` 语句行均逐字符原样保留；不丢失、不重复、不新增、不改变顺序。

该保证由自动化验证守护：

```bash
npm test                          # 格式化用例 + 样例一致性 + 每个用例的内容守恒校验
node test/verify-conservation.js  # 全量守恒验证（所有用例×4 种设置 + 样例×8 种设置 + 80 个边界输入×3 种设置 + 600 次随机变异）
node test/fuzz-heavy.js           # 高强度模糊变异（3000 次随机变异下的内容守恒）
```

任何输入（包括语法错误、未闭合字符串/注释/参数、括号不匹配、极端字符组合）都不会导致内容变化。

## 已知限制

- 超长表达式内部不做二次折行（只在“列表/子句”粒度拆行）；
- `SELECT ... INTO`、PL/pgSQL 过程体等特殊语法按通用规则处理，关键字仍会识别，但不会为其设计专门布局；
- 嵌套的 `${...}`（如 `${a:${b}}`）按第一个 `}` 结束。

## 开发与测试

每次修改后递增 `package.json` 中的补丁版本号（例如 `1.0.1` → `1.0.2`），同步更新安装示例并重新打包。打包脚本从 `package.json` 读取版本号，自动写入 VSIX 清单及安装包文件名。

```bash
npm test                  # 运行全部单元测试与样例一致性校验
node test/run-tests.js --update-sample   # 重新生成样例格式化结果
powershell -File build.ps1               # 按 package.json 版本号打包 VSIX（无需网络）
```

目录结构：

```
extension.js                  VSCode 扩展入口（文档/选区格式化提供器）
formatter/tokenizer.js        词法分析（@行、${}参数、字符串、注释、美元引号、运算符）
formatter/core.js             布局引擎（block/aligned 两种风格）
test/cases.js                 测试用例
test/run-tests.js             测试运行器
samples/                      复杂样例 SQL（输入 + 格式化结果）
build.ps1                     离线打包脚本（手工构造 vsix 结构，不依赖 npm/vsce）
```

## License

MIT
