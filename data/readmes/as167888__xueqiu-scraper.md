# 雪球数据采集与浏览系统

基于 mitmproxy 中间人代理的雪球（xueqiu.com）数据采集工具，配套 SQLite 数据库存储与交互式浏览。

## 项目定位

本程序专用于采集以下三个板块的雪球数据：

| 板块 | 对象 | 归属ID |
|---|---|---|
| 博主发帖 | 雪球大V「逸修1」的 timeline | 用户ID: 1936609590 |
| 专栏文章 | 雪球大V「逸修1」的专栏 | 用户ID: 1936609590 |
| 个股帖子 | 「心动公司(2400.HK)」个股卡页讨论区 | 股票代码: 02400 |

## 架构概览

```
main.py                         # 交互主入口
  ├── scraper_v1.py             # 启动 mitmproxy + 浏览器 → 用户 timeline
  │     └── xueqiu_addon.py     #   拦截 API 响应，解析帖子，写入 DB
  ├── column_scraper_v1.py      # 启动 mitmproxy + 浏览器 → 专栏页面
  │     └── column_addon_v1.py  #   解析 SNOWMAN_STATUS，提取文章，写入 DB
  ├── stock_scraper_v1.py       # 启动 mitmproxy + 浏览器 → 个股卡页
  │     └── stock_addon_v1.py   #   拦截讨论区 API，解析帖子，写入 DB
  └── view_db.py                # 数据库统计/浏览/搜索/导入
        └── stock_db.py         #   SQLite 三表 CRUD + 自动去重
```

**核心链路**：`scraper` 启动 mitmdump 代理进程并打开 Chrome → 用户在浏览器正常访问雪球 → mitmdump 拦截 HTTPS 响应 → `addon` 解析 JSON/HTML 提取数据 → 按 ID 去重后写入 SQLite 数据库。

## 快速开始

### 环境要求

- Python 3.11+
- mitmproxy（`pip install mitmproxy`）
- Chrome 或 Edge 浏览器

### 启动

```bash
python main.py
```

进入交互菜单，选择功能序号即可。

### 抓取流程

1. 选择抓取类型（发帖 / 专栏 / 个股）
2. 自动打开浏览器并启动代理
3. 在浏览器中登录雪球，滚动加载数据
4. 完成后在控制台输入 `q` + 回车退出
5. 数据自动存入数据库，同时保留 JSON 文件

## 数据库

### 三表结构

| 表名 | 存储内容 | 主键/区分字段 | 来源 addon |
|---|---|---|---|
| `user_posts` | 博主 timeline 发帖 | `id`（帖子ID） | `xueqiu_addon.py` |
| `column_articles` | 博主专栏文章 | `id`（文章ID） | `column_addon_v1.py` |
| `stock_posts` | 个股讨论区帖子 | `id`（帖子ID） | `stock_addon_v1.py` |

每条记录包含完整的帖子/文章内容、互动数据（点赞/评论/转发）、用户信息等。

### 去重机制

每次插入时按 `id` + `归属(source_id)` 联合去重，同一帖子多次抓取不会产生重复记录。

### 浏览与搜索

```bash
# 总览统计
python view_db.py stats

# 分页浏览（支持 -t 类型 -s 归属ID -k 关键词 -p 页码）
python view_db.py list -t stock -s 02400 -p 1
python view_db.py list -t user -s 1936609590
python view_db.py list -k 心动 -p 1

# 导入历史 JSON（自动识别类型和归属）
python view_db.py import 20260510_091931_stock_posts.json
```

## 文件说明

```
main.py                 交互主程序（菜单、子程序调度）
scraper_v1.py           博主发帖爬虫启动器
xueqiu_addon.py         mitmproxy 插件：拦截用户 timeline API
column_scraper_v1.py    专栏文章爬虫启动器
column_addon_v1.py      mitmproxy 插件：解析专栏页面 HTML
stock_scraper_v1.py     个股帖子爬虫启动器
stock_addon_v1.py       mitmproxy 插件：拦截个股讨论区 API
stock_db.py             数据库模块（三表建表、插入去重、查询、自动导入）
view_db.py              数据库浏览工具（统计/列表/搜索/导入）
scraper_utils.py        公共工具（q 键退出监控）
```

## 技术细节

### 代理方案

- 使用 mitmproxy 的 `mitmdump` 模式，通过 `-s` 参数加载 Python 插件
- 代理端口 8899，开启 `--ssl-insecure` 以解密 HTTPS
- 浏览器通过 `--proxy-server` 指向代理，使用独立 `--user-data-dir` 保持登录态

### 数据提取

- **用户 timeline**：拦截 `user_timeline.json` API 响应，直接解析 JSON
- **个股讨论区**：拦截 `statuses/search.json`、`stock_timeline.json` 等多个 API 端点，兼容裸数组和包装对象两种响应格式
- **专栏文章**：解析页面 HTML 中的 `window.SNOWMAN_STATUS` 嵌入 JSON，过滤 `type=3` 的专栏文章

## License

MIT
