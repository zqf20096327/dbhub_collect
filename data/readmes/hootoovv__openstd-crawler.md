# 中国标准爬虫工具集

国家标准（GB）与行业标准（HB）全量数据爬取、PDF 下载及 Markdown 转换工具。支持断点续爬、增量爬取、验证码自动识别、多标准类型分类采集，数据存储于 SQLite 数据库。可使用 MinerU 将已下载的 PDF 自动转换为 Markdown 格式，内嵌图片提取到独立子目录。

---

## 项目结构

```
standards-crawler/
├── pyproject.toml          # 项目配置与依赖声明（uv/pip 兼容）
├── uv.lock                 # uv 锁定文件（精确版本锁定）
├── .python-version         # Python 版本声明
├── .gitignore              # Git 忽略规则
├── run_crawler.py          # 统一入口脚本
├── scripts/
│   ├── gb_crawler.py       # 国家标准爬虫
│   ├── hb_crawler.py       # 行业标准爬虫
│   └── pdf_to_md.py        # PDF → Markdown 转换工具
├── standards.db            # SQLite 数据库（运行后自动生成）
├── download/
│   ├── gb_standards/       # 国家标准 PDF 存放目录
│   └── hb_standards/       # 行业标准 PDF 存放目录
├── md/
│   ├── gb/                 # 国标 Markdown 输出目录
│   │   └── <文件名>/        # 每个标准一个目录
│   │       ├── <文件名>.md # Markdown 文件
│   │       └── images/     # 内嵌图片
│   └── hb/                 # 行标 Markdown 输出目录
├── logs/
│   ├── gb_crawler.log      # 国家标准爬虫日志
│   ├── hb_crawler.log      # 行业标准爬虫日志
│   └── pdf_to_md.log       # PDF 转换日志
└── README.md
```

---

## 功能特性

### 国家标准爬虫（gb_crawler）

- **数据来源**：[国家标准全文公开系统](https://openstd.samr.gov.cn)
- **三种标准类型**：
  - 强制性国家标准（p1=1）
  - 推荐性国家标准（p1=2）
  - 指导性技术文件（p1=3）
- **列表爬取**：解析服务端渲染的 HTML 分页页面，提取标准号、标准名称、状态、发布日期、实施日期等字段
- **PDF 下载**：支持两种下载方式，自动判断标准可用方式
  - **直接下载**：通过 `openstd.samr.gov.cn/bzgk/std/viewGb` 接口直接获取 PDF 文件流（标准允许下载时优先使用）
  - **预览方式下载**：通过 `openstd.samr.gov.cn/bzgk/std/showGb?type=online` 获取预览页面结构，下载图块资源并重组为 PDF（标准仅允许预览时使用，需加 `--include-preview` 参数）
- **下载选项**：默认仅下载可直接下载的国标（`allow_download=1`），使用 `--include-preview` 可包含仅可预览的国标
- **验证码识别**（仅当下载页 `isValid` 标志为 `false` 时触发）：
  1. 访问下载页 `showGb?type=download`，读取服务端 `var isValid` 标志
  2. 获取验证码图片：`openstd.samr.gov.cn/bzgk/std/gc`
  3. cv2 图像预处理：灰度化 → 二值化（阈值190）→ 反色
  4. ddddocr OCR 识别验证码文字
  5. 提交验证：`openstd.samr.gov.cn/bzgk/std/verifyCode`
  6. 最多重试 10 次，验证通过后在同一会话中下载 PDF
- **详情页检测**：自动检测标准是否允许下载/预览，不可下载的标准不会重复尝试
- **断点续爬**：通过 `gb_crawl_progress` 表记录已爬取的页码，中断后自动跳过已完成的页面
- **增量爬取**：全量爬取完成后再次运行时自动切换为增量模式，从第 1 页重新扫描，连续 N 页（默认 3，可配置）无新增条目则提前结束，避免重复爬取数千页已入库数据（详见 [增量爬取机制](#增量爬取机制)）
- **下载前自动检测**：下载时若发现存在未完成可用性检测的标准（`allow_checked=0`），会自动先执行检测，避免因 `allow_download`/`allow_preview` 仍为初始值 0 而遗漏实际可下载的标准
- **下载进度跟踪**：`gb_download_progress` 表记录每个标准的下载状态和重试次数

### 行业标准爬虫（hb_crawler）

- **数据来源**：[行业标准信息服务平台](https://hbba.sacinfo.org.cn)
- **列表爬取**：调用 REST API 接口 `/stdQueryList`，返回 JSON 格式数据
- **PDF 下载流程**（网站改版后已移除验证码机制）：
  1. 访问标准详情页（stdDetail），建立会话状态
  2. 访问在线查看页面（portal/online）判断是否公开
  3. 直接调用下载接口（portal/download/{pk}）获取 PDF
- **三种下载状态**：
  - `success` — 下载成功
  - `not_public` — 标准尚未公开，页面显示"尚未公开"
  - `no_file` — 标准无 PDF 文件可供下载（如部分 SH/T 类标准重定向到首页）
- **断点续爬**：通过 `hb_crawl_progress` 表记录已爬取页码
- **增量爬取**：全量爬取完成后再次运行时自动切换为增量模式，从第 1 页重新扫描，连续 N 页（默认 3，可配置）无新增条目则提前结束
- **下载进度跟踪**：`hb_download_progress` 表记录下载状态，已标记为 `not_public`、`no_file`、`success` 的标准不会重复下载

### PDF 转 Markdown 工具（pdf_to_md）

- **转换引擎**：使用 [MinerU](https://github.com/opendatalab/MinerU)（pipeline 后端）进行 PDF 解析
- **输出结构**：每个 PDF 在 `md/gb/` 或 `md/hb/` 下以文件名为目录名，内含同名 `.md` 文件和 `images/` 子目录
- **断点续转**：通过 `pdf_convert_progress` 表记录转换状态，已成功转换的文件不会重复处理
- **优雅中断**：支持 Ctrl+C 中断，自动保存当前转换进度，下次运行从断点继续
- **强制重转**：使用 `--force` 参数可忽略已完成记录，重新转换所有文件
- **中文优化**：默认使用 `ch` 语言参数，优化中文 OCR 和解析效果

### 通用特性

- **断点续爬/续转**：所有爬虫和转换工具均支持中断后从上次位置继续，无需重新开始
- **增量爬取**：国标和行标爬虫均支持，全量爬取完成后再次运行自动进入增量模式，仅扫描包含新增标准的页面，发现连续 N 页无新增即提前结束
- **优雅中断**：支持 Ctrl+C 中断，自动保存当前进度，下次运行从断点继续
- **请求延迟**：内置随机请求间隔，避免对目标服务器造成过大压力
- **重试机制**：网络请求失败时自动重试，最大重试次数可配置
- **文件命名**：PDF 文件以 `<标准号>-<标准名称>.pdf` 格式保存，特殊字符自动替换
- **日志记录**：同时输出到控制台和日志文件，便于排查问题

---

## 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) （推荐）或 pip
- （可选）MinerU：用于 PDF → Markdown 转换功能

---

## 安装

### 使用 uv（推荐）

```bash
# 克隆项目
cd standards-crawler

# 安装基础依赖
uv sync

# 如需 PDF → Markdown 转换功能，安装 MinerU
uv pip install -U mineru[all]
```

### 使用 pip

```bash
# 克隆项目
cd standards-crawler

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安装基础依赖
pip install -e .

# 如需 PDF → Markdown 转换功能，安装 MinerU
pip install mineru[all]
# 或使用可选依赖组
pip install -e ".[convert]"
```

---

## 使用方法

### 统一入口（推荐）

`run_crawler.py` 提供了统一的命令行入口，支持灵活的参数组合：

```bash
# 使用 uv run（自动激活虚拟环境）
uv run python run_crawler.py stats

# ===== 国家标准 =====
uv run python run_crawler.py gb --crawl              # 爬取全部类型国家标准列表（全量未完成则全量，已完成则增量）
uv run python run_crawler.py gb --crawl --type 1     # 只爬取强制性国家标准
uv run python run_crawler.py gb --crawl --type 2     # 只爬取推荐性国家标准
uv run python run_crawler.py gb --crawl --type 3     # 只爬取指导性技术文件
uv run python run_crawler.py gb --crawl --full       # 强制全量爬取（忽略已完成标记，用于定期校准数据）
uv run python run_crawler.py gb --crawl --early-stop-pages 0   # 增量模式但不提前结束（扫完全部页）
uv run python run_crawler.py gb --check              # 检测标准可用性（下载/预览权限）
uv run python run_crawler.py gb --download           # 下载国家标准 PDF（默认仅可下载标准）
uv run python run_crawler.py gb --download --include-preview  # 下载国家标准 PDF（含仅可预览标准）
uv run python run_crawler.py gb --all                # 爬取+下载国家标准

# ===== 行业标准 =====
uv run python run_crawler.py hb --crawl              # 爬取行业标准列表
uv run python run_crawler.py hb --download           # 下载行业标准 PDF
uv run python run_crawler.py hb --download --industry 农业  # 只下载农业相关的行业标准 PDF
uv run python run_crawler.py hb --all                # 爬取+下载行业标准
uv run python run_crawler.py hb --all --industry 农业    # 爬取+只下载农业相关的行业标准

# ===== 全部标准 =====
uv run python run_crawler.py all --crawl             # 爬取所有标准列表
uv run python run_crawler.py all --download          # 下载所有标准 PDF
uv run python run_crawler.py all --all               # 爬取+下载所有标准

# ===== PDF → Markdown 转换 =====
uv run python run_crawler.py gb --convert            # 将国标 PDF 转换为 Markdown
uv run python run_crawler.py hb --convert            # 将行标 PDF 转换为 Markdown
uv run python run_crawler.py all --convert           # 将所有标准 PDF 转换为 Markdown
uv run python run_crawler.py gb --convert --force    # 强制重新转换（忽略已完成记录）

# 查看统计信息
uv run python run_crawler.py stats
```

#### 增量爬取参数

以下参数仅作用于 `--crawl`（爬取列表），对下载和转换无效：

| 参数 | 说明 |
|------|------|
| `--full` | 强制全量爬取，忽略"已完成全量"标记与提前结束，从头爬到末页。用于定期彻底校准数据 |
| `--early-stop-pages N` | 增量爬取时连续 N 页无新增条目则提前结束。默认 3；设为 0 则禁用提前结束（增量模式但扫完全部页） |

爬虫会自动根据数据库中 `fully_crawled` 标记判断模式，**无需手动指定**：
- 从未爬取 / 上次被中断 → **全量模式**（断点续爬，跳过已 done 页）
- 已完成全量爬取 → **增量模式**（从第 1 页重扫，连续 N 页无新增即提前结束）

### 单独运行爬虫

也可以直接运行各个脚本：

```bash
# 国家标准爬虫
uv run python scripts/gb_crawler.py --crawl          # 爬取列表（自动判断全量/增量）
uv run python scripts/gb_crawler.py --crawl --full   # 强制全量爬取
uv run python scripts/gb_crawler.py --download       # 下载 PDF（默认仅可下载标准）
uv run python scripts/gb_crawler.py --download --include-preview  # 下载 PDF（含仅可预览标准）
uv run python scripts/gb_crawler.py --type 2         # 只爬取推荐性
uv run python scripts/gb_crawler.py --all            # 全部操作
uv run python scripts/gb_crawler.py --stats          # 统计信息

# 行业标准爬虫
uv run python scripts/hb_crawler.py --crawl          # 爬取列表
uv run python scripts/hb_crawler.py --download       # 下载 PDF
uv run python scripts/hb_crawler.py --download --industry 农业  # 只下载农业相关的 PDF
uv run python scripts/hb_crawler.py --all            # 全部操作
uv run python scripts/hb_crawler.py --all --industry 农业      # 全部操作(仅农业)
uv run python scripts/hb_crawler.py --stats          # 统计信息

# PDF → Markdown 转换
uv run python scripts/pdf_to_md.py gb               # 转换国标
uv run python scripts/pdf_to_md.py hb               # 转换行标
uv run python scripts/pdf_to_md.py all              # 转换所有
uv run python scripts/pdf_to_md.py gb --force       # 强制重新转换
uv run python scripts/pdf_to_md.py stats            # 转换统计
```

---

## 数据库结构

所有数据存储在项目根目录的 `standards.db`（SQLite）中，包含以下数据表：

### gb_standards（国家标准）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键自增 |
| std_type | TEXT | 标准类型（强制性国家标准/推荐性国家标准/指导性技术文件） |
| standard_no | TEXT | 标准号（唯一） |
| is_adopted | TEXT | 是否采标 |
| standard_name | TEXT | 标准名称 |
| status | TEXT | 标准状态 |
| publish_date | TEXT | 发布日期 |
| implement_date | TEXT | 实施日期 |
| detail_url | TEXT | 详情页 URL |
| hcno | TEXT | 标准编号哈希（用于下载） |
| allow_download | INTEGER | 是否允许直接下载（0/1）。注意：未检测前为初始值 0，仅当 `allow_checked=1` 时才代表真实权限 |
| allow_preview | INTEGER | 是否允许预览下载（0/1）。注意：未检测前为初始值 0，仅当 `allow_checked=1` 时才代表真实权限 |
| allow_checked | INTEGER | 是否已完成可用性检测（0/1）。1 表示 allow_download/allow_preview 已反映真实权限 |
| local_file | TEXT | 本地文件名 |
| created_at | TIMESTAMP | 记录创建时间 |

### hb_standards（行业标准）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键自增 |
| standard_no | TEXT | 标准号（唯一） |
| standard_name | TEXT | 标准名称 |
| industry | TEXT | 行业分类 |
| status | TEXT | 标准状态 |
| approve_date | TEXT | 批准日期 |
| implement_date | TEXT | 实施日期 |
| detail_url | TEXT | 详情页 URL |
| pk | TEXT | 主键标识（用于下载） |
| local_file | TEXT | 本地文件名 |
| charge_dept | TEXT | 主管部门 |
| revise_std_codes | TEXT | 替代标准号 |
| created_at | TIMESTAMP | 记录创建时间 |

### pdf_convert_progress（PDF 转换进度）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键自增 |
| std_type | TEXT | 标准类型（gb/hb） |
| pdf_filename | TEXT | PDF 文件名 |
| status | TEXT | 转换状态（pending/success/failed） |
| output_dir | TEXT | 输出目录路径 |
| error_msg | TEXT | 错误信息 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### gb_crawl_meta / hb_crawl_meta（全量爬取状态标记）

记录是否已完成过一次全量爬取，用于区分全量/增量模式。国标按类型分行，行标为单行表（`id=1`）。

| 字段 | 类型 | 说明 |
|------|------|------|
| std_type_code / id | INTEGER | 主键。国标为标准类型代码（1/2/3），行标固定为 1 |
| fully_crawled | INTEGER | 是否已完成全量爬取（0/1）。1 = 下次运行进入增量模式 |
| last_total_pages | INTEGER | 上次记录到的总页数（参考） |
| updated_at | TIMESTAMP | 更新时间 |

### 进度跟踪表

- `gb_crawl_progress` — 国家标准爬取进度（按类型+页码）
- `hb_crawl_progress` — 行业标准爬取进度（按页码）
- `gb_download_progress` — 国家标准下载进度
- `hb_download_progress` — 行业标准下载进度
- `pdf_convert_progress` — PDF → Markdown 转换进度

---

## 配置参数

可在各脚本顶部修改以下配置：

### 国家标准爬虫配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| PAGE_SIZE | 50 | 每页记录数 |
| REQUEST_DELAY | (1, 3) | 请求间隔范围（秒） |
| MAX_RETRIES | 3 | 列表请求最大重试次数 |
| CAPTCHA_MAX_RETRIES | 10 | 验证码识别最大重试次数 |
| DOWNLOAD_MAX_RETRIES | 5 | PDF 下载最大重试次数 |
| CONSECUTIVE_FAIL_LIMIT | 20 | 连续失败早停阈值 |
| EARLY_STOP_CONSECUTIVE_PAGES | 3 | 增量爬取时连续 N 页无新增条目则提前结束（0=禁用） |

### 行业标准爬虫配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| PAGE_SIZE | 100 | 每页记录数 |
| REQUEST_DELAY | (0.5, 2) | 请求间隔范围（秒） |
| MAX_RETRIES | 5 | 列表请求最大重试次数 |
| CAPTCHA_MAX_RETRIES | 10 | 验证码识别最大重试次数 |
| DOWNLOAD_MAX_RETRIES | 5 | PDF 下载最大重试次数 |
| EARLY_STOP_CONSECUTIVE_PAGES | 3 | 增量爬取时连续 N 页无新增条目则提前结束（0=禁用） |

### 行业过滤参数

| 参数 | 说明 |
|------|------|
| --industry | 按行业分类过滤行业标准下载，例如 `--industry 农业` 只下载农业相关的行业标准。不指定则下载全部行业标准 |

---

## 已知限制

1. **国家标准 PDF 下载**：国家标准 PDF 下载接口现已由独立的 `c.gb688.cn`（HTTP）迁移至主站 `openstd.samr.gov.cn/bzgk/std`（HTTPS），与列表/详情页同站。下载端点（`showGb`/`viewGb`/`viewGbImg`）必须携带正确的 `Referer` 头（指向详情页或下载页），否则服务器会 302 重定向回详情页导致下载失败。如遇下载失败，请确认网络环境能正常访问 `openstd.samr.gov.cn`。

2. **行业标准"尚未公开"**：大量行业标准标记为"尚未公开"，无法下载其 PDF 文件。爬虫会自动检测并标记为 `not_public` 状态，不会反复重试。

3. **行业标准"无文件"**：部分行业标准（如部分 SH/T 类标准）虽然页面可访问，但实际上没有 PDF 文件可供下载，点击下载会重定向回首页。爬虫会检测此情况并标记为 `no_file` 状态。

4. **验证码识别率**：`ddddocr` 对验证码的识别率并非 100%，但通过多次重试机制（默认最多 10 次）和 cv2 图像预处理（灰度化+二值化+反色），可以覆盖绝大多数情况。

5. **国标预览方式**：部分国家标准仅允许在线预览，不允许直接下载。默认下载时仅下载可直接下载的标准；使用 `--include-preview` 参数后，爬虫会尝试以预览方式下载仅可预览的标准。预览方式当前可能存在不稳定的情况。

6. **PDF 转 Markdown**：MinerU 需要额外安装（`pip install mineru`），首次使用时会自动下载模型文件。转换过程对 CPU/内存有一定要求，大文件转换可能耗时较长。建议在内存 ≥ 4GB 的环境下运行。

---

## 增量爬取机制

当源网站发布新标准后再次运行爬虫时，全量重爬数千页效率极低（实际只有前几页含新增内容）。本项目通过"全量/增量"双模式解决此问题。

### 模式自动判断

爬虫根据 `fully_crawled` 标记自动选择模式，**无需手动干预**：

| 数据库状态 | 运行模式 | 行为 |
|------------|----------|------|
| 从未爬取过（`fully_crawled=0`） | 全量模式 | 断点续爬：跳过已 done 页，从断点继续，爬到末页后标记 `fully_crawled=1` |
| 上次全量被中断（未到末页） | 全量模式 | 同上，继续未完成的页面 |
| 已完成全量爬取（`fully_crawled=1`） | 增量模式 | 从第 1 页重新扫描，连续 N 页（默认 3）无新增条目则提前结束 |
| `--full` 强制全量 | 全量模式 | 忽略标记，从头爬到末页，结束后重新标记 `fully_crawled=1` |

### 为什么能安全提前结束

标准列表按发布日期倒序（最新在前）排列：

- 有新标准发布 → 必出现在**最前几页**，这些页"新增数 > 0" → 连续计数被清零 → 不会误停；
- 越往后越旧 → 一旦进入"全是已入库老标准"的区域，后面只会更旧 → 连续 N 页命中即可安全停止。

### 关键设计：为何不直接跳过已 done 的页

全量模式下"跳过已 done 页"是断点续爬所必需的（否则中断重跑会从头开始）。但同一个 `done` 标志若在增量模式下也跳过，将**永远发现不了新标准**（因为所有页都已 done）。因此用独立的 `fully_crawled` 标记区分两种模式：全量模式跳过 done 页（续爬），增量模式忽略 done 标志、从第 1 页重新评估（发现新增）。

### 各场景行为

| 场景 | 预期结果 |
|------|----------|
| 空库首次运行 | 全量爬取全部页 → 标记 `fully_crawled=1` |
| 首次全量被 Ctrl+C 中断 | 断点续爬跳过已 done 页 → 到末页后标记 `fully_crawled=1` |
| 全量完成后、无新标准重跑 | 增量模式：第 1~3 页全已存在 → 第 3 页即停止（仅抓 3 页） |
| 网站新增 2 条标准重跑 | 增量模式：第 1 页有新增(计数清零) → 第 2/3/4 页全老 → 第 4 页停止 |
| 增量过程中 Ctrl+C | 下次重跑从第 1 页重新评估（仅多扫几页，代价小） |
| 怀疑数据漂移需彻底校准 | `--full` 强制全量重爬 |

---

## 运行示例

```bash
# 第一步：爬取国家标准列表
uv run python run_crawler.py gb --crawl

# 输出示例：
# 2025-05-15 10:00:00 [INFO] ===== 开始爬取 强制性国家标准 =====
# 2025-05-15 10:00:02 [INFO] 强制性国家标准 共 12 页
# 2025-05-15 10:00:03 [INFO] 第 1/12 页: 爬取 50 条记录
# 2025-05-15 10:00:05 [INFO] 第 2/12 页: 爬取 50 条记录
# ...

# 第二步：下载国家标准 PDF
uv run python run_crawler.py gb --download

# 输出示例：
# 2025-05-15 10:05:00 [INFO] 待下载标准: 44700 个 (仅可下载: 35000, 仅可预览: 8000, 下载+预览: 1700)
# 2025-05-15 10:05:00 [INFO] 下载模式: 仅可下载标准 (使用 --include-preview 可包含仅可预览标准)
# 2025-05-15 10:05:00 [INFO] 正在测试下载服务器 openstd.samr.gov.cn/bzgk/std 连通性...
# 2025-05-15 10:05:01 [INFO] 下载服务器响应: status=200, content_length=12345
# 2025-05-15 10:05:01 [INFO] 下载进度: 1/44700 - GB/T 1.1 标准化工作导则
# 2025-05-15 10:05:02 [INFO] ddddocr OCR引擎初始化完成
# 2025-05-15 10:05:03 [INFO] 验证码验证成功 (attempt 1)
# 2025-05-15 10:05:05 [INFO] 下载成功(直接): GB_T 1.1-标准化工作导则.pdf

# 第三步：将国标 PDF 转换为 Markdown
uv run python run_crawler.py gb --convert

# 输出示例：
# 2025-05-15 10:10:00 [INFO] ===== 开始转换 国家标准 PDF → Markdown =====
# 2025-05-15 10:10:00 [INFO] PDF 文件: 44700 个, 已转换: 0, 待转换: 44700
# 2025-05-15 10:10:01 [INFO] 转换进度: 1/44700 - GB_T 1.1-标准化工作导则
# 2025-05-15 10:10:15 [INFO] 转换完成: 成功 1, 失败 0, 已跳过(之前完成) 0

# 第四步：爬取+下载行业标准
uv run python run_crawler.py hb --all

# 第五步：查看统计
uv run python run_crawler.py stats
```

### 增量爬取示例（全量已完成后的后续运行）

```bash
# 网站发布了少量新标准，再次运行 —— 自动进入增量模式
uv run python run_crawler.py gb --crawl

# 输出示例（无新增时，仅抓前几页即停止）：
# 2025-06-01 09:00:00 [INFO] ===== 开始爬取 强制性国家标准 [模式: 增量] =====
# 2025-06-01 09:00:00 [INFO] 强制性国家标准 共 123 页
# 2025-06-01 09:00:00 [INFO] 强制性国家标准 已完成全量爬取，进入增量模式，连续 3 页无新增则提前结束
# 2025-06-01 09:00:01 [INFO] 第 1/123 页: 爬取 50 条记录, 新增 0 条
# 2025-06-01 09:00:03 [INFO] 第 2/123 页: 爬取 50 条记录, 新增 0 条
# 2025-06-01 09:00:05 [INFO] 第 3/123 页: 爬取 50 条记录, 新增 0 条
# 2025-06-01 09:00:05 [INFO] 连续 3 页无新增条目，提前结束 强制性国家标准 增量爬取

# 若有新增（如第 1 页出现新标准，计数清零，继续扫描）：
# 2025-06-01 09:00:01 [INFO] 第 1/123 页: 爬取 50 条记录, 新增 2 条
# 2025-06-01 09:00:03 [INFO] 第 2/123 页: 爬取 50 条记录, 新增 0 条
# ...
# 2025-06-01 09:00:05 [INFO] 第 4/123 页: 爬取 50 条记录, 新增 0 条
# 2025-06-01 09:00:05 [INFO] 连续 3 页无新增条目，提前结束 强制性国家标准 增量爬取

# 怀疑数据漂移需要彻底校准时，强制全量重爬
uv run python run_crawler.py gb --crawl --full
```

---

## 技术实现细节

### 国家标准爬虫

- 采用 `requests.Session` 维持会话，首次访问首页初始化 Cookie
- 列表页为服务端渲染 HTML，使用 `BeautifulSoup` + `lxml` 解析 `table.result_list` 表格
- 从 `onclick` 事件中提取 `hcno`（标准的唯一标识哈希值），用于拼接详情页 URL 和下载 URL
- 分页信息通过正则匹配页码元素获取
- **PDF 下载流程**（端点已迁移至主站 `openstd.samr.gov.cn/bzgk/std`）：
  1. 检查详情页，判断标准是否允许下载/预览（检测 `button.xz_btn` 和 `button.ck_btn`）
  2. 访问下载页 `showGb?type=download`（Referer 指向详情页），读取服务端 `var isValid` 标志
  3. 若 `isValid='false'`：获取验证码 `gc` → cv2 预处理 + ddddocr 识别 → 提交验证 `verifyCode`（同一会话）
  4. 直接下载：`GET viewGb?hcno={hcno}`（Referer 指向 showGb 下载页，优先）
  5. 预览下载：获取预览页面结构（`showGb?type=online`）→ 下载图块（`viewGbImg`，需 Referer）→ 重组页面 → 生成 PDF（备选）
- 验证码和下载必须在同一 HTTP 会话中完成，使用独立的 `requests.Session` 维护
- **关键**：`showGb`/`viewGb`/`viewGbImg` 等端点对 `Referer` 敏感，缺失或不正确时服务器会 302 重定向回详情页

### 行业标准爬虫

- 列表接口为 POST 请求的 REST API，返回 JSON 格式数据，包含分页信息
- 日期字段为毫秒级时间戳，自动转换为 `YYYY-MM-DD` 格式
- PDF 下载流程（网站改版后已移除验证码）：
  1. 先访问详情页 `stdDetail/{pk}` 建立会话状态（设置 Cookie）
  2. 访问在线查看页 `portal/online/{pk}` 检测是否公开（必须先访问详情页，否则一律被判为未公开）
  3. 直接 GET `portal/download/{pk}` 获取 PDF（无需验证码）
- 下载时检测重定向到首页的情况，标记为 `no_file`；检测页面含"尚未公开"文字，标记为 `not_public`

### PDF → Markdown 转换

- 使用 MinerU 的 Python API (`from mineru.cli.common import do_parse, read_fn`) 进行 PDF 解析
- 采用 `pipeline` 后端（无需 GPU），`auto` 解析方法（自动选择文本提取或 OCR）
- 中文语言参数 (`p_lang_list=["ch"]`)，启用公式和表格解析
- 转换流程：读取 PDF → MinerU 解析到临时目录 → 重组到目标目录结构 → 清理临时文件
- 目标目录结构：`md/<gb|hb>/<PDF文件名>/<文件名>.md` + `images/` 子目录
- 转换进度通过 `pdf_convert_progress` 表跟踪，支持断点续转
- 同时检测目标文件是否存在（双重保障），即使数据库记录丢失也不会重复转换

---

## 许可证

本项目仅供学习和研究使用，请遵守相关网站的使用条款和 robots.txt 规则。爬取数据时请注意控制请求频率，避免对目标服务器造成过大压力。

提示及测试： hootoovv  
设计及实现：GLM5.1 Agent @ https://chat.z.ai/ 