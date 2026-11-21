<div align="center">

# Sheet Studio

**在 VS Code 里看表格、改数据、写 SQL。**

Excel · CSV · SQLite · PostgreSQL · MySQL · MariaDB · SQL Server

[![版本](https://img.shields.io/github/v/release/didongji91/sheet-studio?color=2b7654&label=version)](https://github.com/didongji91/sheet-studio/releases/latest)
[![检查](https://github.com/didongji91/sheet-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/didongji91/sheet-studio/actions/workflows/ci.yml)
[![VS Code](https://img.shields.io/badge/VS%20Code-1.96%2B-2878b5)](https://code.visualstudio.com/)
[![MIT](https://img.shields.io/badge/license-MIT-777777)](LICENSE)

[下载安装包](https://github.com/didongji91/sheet-studio/releases/latest) · [使用手册](docs/guide.zh-CN.md) · [更新记录](CHANGELOG.md) · [反馈问题](https://github.com/didongji91/sheet-studio/issues)

</div>

Sheet Studio 把表格编辑器和数据库工作台放进 VS Code。打开工作区里的 Excel、CSV 或 SQLite 文件就能查看、编辑和搜索，也可以连接数据库服务器执行 SQL。

文件在本地处理，服务器连接直接访问你配置的数据库，不需要注册 Sheet Studio 账号。

![表格编辑器：多工作表、公式栏和可调整的行列](docs/images/spreadsheet.png)

## 能做什么

| 功能 | 支持内容 |
| --- | --- |
| **表格编辑** | 多工作表、常用公式、格式、合并单元格、水平与垂直对齐、冻结首行首列、排序筛选、查找替换、工作区内容检索。 |
| **数据库工作台** | 表与视图导航、分页、筛选排序、记录增删改，查看字段、索引、外键和 DDL。 |
| **SQL 编辑器** | 语法高亮、表名和字段补全、格式化、执行选区、多个结果页签、执行历史和事务。 |
| **导入导出** | 表格导出 XLSX / CSV / TSV；数据库导入 CSV / TSV，当前页或查询结果导出 CSV / JSON / XLSX。 |
| **外观调整** | 拖动或输入行高、列宽；浅色、深色、暖色、浅绿预设，也能自己选背景色。背景不跟随系统主题。 |
| **保存与恢复** | 撤销重做、另存为、热退出恢复、外部文件修改检查；SQLite 覆盖保存前保留备份。 |

## 安装

需要 **VS Code 1.96 或更新版本**。目前通过 VSIX 安装，尚未上架扩展市场。

1. 到 [Releases](https://github.com/didongji91/sheet-studio/releases/latest) 下载 `.vsix` 安装包。
2. 打开 VS Code 扩展面板，点右上角 **… → 从 VSIX 安装…**。
3. 打开表格或 SQLite 文件。如果已有其他扩展接管，右键文件标签页，选择 **重新打开编辑器的方式… → Sheet Studio**。

也可以在下载目录执行：

```sh
code --install-extension sheet-studio-0.2.1.vsix
```

按 `Ctrl+Shift+P`（macOS 为 `Cmd+Shift+P`），输入 `Sheet Studio`，可以新建工作簿、检索工作区表格、打开 SQLite 文件或进入数据库连接管理。

## 支持的文件和数据库

| 类型 | 支持情况 |
| --- | --- |
| `.xlsx` | 查看、编辑、原格式保存。含复杂 Excel 对象时进入兼容模式，改为导出副本。 |
| `.csv` / `.tsv` | 查看、编辑、原格式保存；识别常见编码、分隔符和换行方式，保留前导零和长编号。 |
| `.xls` / `.xlsm` / `.xlsb` / `.ods` | 兼容导入，编辑后导出为 XLSX；不执行宏。 |
| `.db` / `.sqlite` / `.sqlite3` / `.db3` / `.s3db` / `.sqllite` | 直接打开 SQLite 3 文件，无需额外安装驱动。扩展名可以不同，文件内容必须是 SQLite。 |
| PostgreSQL / MySQL / MariaDB / SQL Server | 使用连接管理配置服务器，支持用户名密码认证、TLS、数据编辑和 SQL。 |

## 数据库怎么用

打开 SQLite 文件，或运行 **Sheet Studio: 数据库连接管理** 新建服务器连接。左边选表，右边切换 **数据 / 结构 / SQL 编辑器**。

![数据库工作台：表和视图导航、分页筛选与数据网格](docs/images/database.png)

双击或按 `F2` 编辑单元格，修改会先暂存在网格里，点 **应用修改** 后再提交。SQL 编辑器按 `Ctrl+Enter` 执行选中的语句，没有选区时执行全文。

**SQLite 文件还需要按 `Ctrl+S` 保存到磁盘。** 覆盖前会留下 `<文件名>.sheet-studio.bak` 备份。服务器连接默认自动提交，也可以手动开启事务、提交或回滚；密码单独存入 VS Code SecretStorage。

<details>
<summary><strong>看看 SQL 编辑器和自定义深色背景</strong></summary>

![SQL 编辑器：深色背景、语法高亮与查询结果](docs/images/sql-dark.png)

语法高亮、补全、格式化、执行历史和多个结果页签已包含。数据库网格右上角的 **外观设置** 可以调整背景和行高，列宽直接拖动列标题边缘。

</details>

## 行高、列宽和背景

- **拖动调整**：拖行号下边缘或列标题右边缘，双击列边缘自动适配。选中多行或多列后可以一起改。
- **输入尺寸**：表格的 **视图 → 行高… / 列宽…** 支持精确像素值，也可以从右键菜单打开。XLSX 保存后保留尺寸。
- **手动选色**：表格的 **视图 → 背景颜色** 或数据库的 **外观设置** 中选择预设、使用取色器或输入 `#RRGGBB`。颜色保存为个人偏好，不会修改文件内容。

CSV / TSV 本身不保存行列尺寸和样式；需要保留这些内容时，导出成 XLSX。

合并标题或高行里的文字，可以在 **开始** 工具栏选择 **顶端对齐 / 垂直居中 / 底端对齐**。打开 XLSX 会读取原有设置，编辑、复制和保存后继续保留。

## 使用前了解一下

这版主要用于日常表格处理和数据库浏览、编辑、查询。完整的兼容范围和操作限制见 [使用手册](docs/guide.zh-CN.md)。

- Excel 的图表、透视表、复杂条件格式、宏和部分新公式尚未完整支持。复杂工作簿会提示导出副本，副本可能丢失不支持的对象。
- `.db` 不代表任意数据库格式。目前文件模式支持 SQLite，不支持 DuckDB、Access 或加密 SQLite；也没有通用 JDBC、SSH 隧道、ER 图和跨库同步。
- SQLite 默认文件上限 128 MB，使用内存中的副本编辑。文件被其他程序修改，或存在未完成的 WAL / journal 时，会阻止覆盖保存。
- 数据库导出 CSV / JSON / XLSX 针对**当前页或当前结果**。完整 SQLite 数据库请使用数据库副本或 SQL 脚本导出。
- SQLite 读写和 VS Code 文件生命周期已经过实际测试。服务器驱动已验证加载、模拟客户端和连接失败处理，**尚未完成真实 PostgreSQL / MySQL / MariaDB / SQL Server 实例的端到端联调**。PostgreSQL / SQL Server 的 DDL 视图是参考重建，不能当完整备份使用。

## 本地开发

开发环境使用 **Node.js 24** 和 npm。

```sh
git clone https://github.com/didongji91/sheet-studio.git
cd sheet-studio
npm ci
npm run check
```

用 VS Code 打开项目，按 **F5** 启动扩展开发宿主。

| 命令 | 用途 |
| --- | --- |
| `npm run check` | 类型检查、自动测试、构建 |
| `npm run test:extension` | 在独立 VS Code 测试环境中检查保存、撤销重做、数据库等流程 |
| `npm run package` | 检查并打包为 VSIX |
| `npm run dev` | 构建后启动浏览器预览，地址为 `http://127.0.0.1:5173` |

项目代码、界面和测试分别位于 `src/`、`webview/`、`test/`。测试环境配置和浏览器预览说明见 [开发说明](docs/guide.zh-CN.md#开发)。

## 许可

[MIT](LICENSE)。第三方依赖与许可证见 [THIRD_PARTY_NOTICES.txt](THIRD_PARTY_NOTICES.txt)。
