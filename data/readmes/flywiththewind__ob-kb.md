# ob-kb

OceanBase 数据库知识库离线镜像（本地 HTML）。

内容来自 [OceanBase 官方知识库 · OceanBase 数据库](https://www.oceanbase.com/knowledge-base/oceanbase-database-1000000000324072)，整理为可本地浏览的静态站点，**仅供个人学习查阅**。

- 文章约 1999 篇
- 含本地图片与目录导航、标题搜索

---

## 快速开始（离线使用）

> 不要直接双击用 `file://` 打开。侧边栏目录依赖 `fetch` 加载 `catalog.json`，需要本地 HTTP 服务。

### 1. 克隆仓库

```bash
git clone https://github.com/flywiththewind/ob-kb.git
cd ob-kb
```

仓库约 **580MB**（图片较多），克隆会稍慢。

### 2. 启动本地预览服务

在仓库根目录执行：

```bash
./serve.sh
```

或手动：

```bash
cd site
python3 -m http.server 8765 --bind 127.0.0.1
```

### 3. 浏览器打开

[http://127.0.0.1:8765/index.html](http://127.0.0.1:8765/index.html)

常用入口：

| 页面 | 地址 |
|------|------|
| 首页 | http://127.0.0.1:8765/index.html |
| 知识导图 | http://127.0.0.1:8765/articles/1000000000324072.html |

停止服务：终端里按 `Ctrl+C`。

### 换端口

```bash
cd site
python3 -m http.server 9000 --bind 127.0.0.1
# 然后打开 http://127.0.0.1:9000/index.html
```

其他静态服务器也可以，例如：

```bash
npx --yes serve site -l 8765
```

---

## 目录结构

```text
ob-kb/
├── README.md
├── serve.sh              # 一键启动本地预览
├── download_kb.py        # 可选：重新拉取/更新文章
├── site/                 # 静态站点（真正打开的是这里）
│   ├── index.html
│   ├── articles/         # 文章 HTML
│   ├── images/           # 本地图片
│   └── assets/           # 样式、导航、目录数据
└── data/                 # 目录树等元数据（下载脚本用）
```

---

## 可选：重新下载 / 断点续传

若要更新内容或补下失败文章：

```bash
# 需要本机 Python 3，并安装证书包（macOS 常见）
pip3 install certifi

# 16 并行（已存在的文章会跳过）
python3 download_kb.py --workers 16

# 只重建首页/目录壳子，不重新拉文章
python3 download_kb.py --assets-only
```

---

## 说明

- 原始站点：https://www.oceanbase.com/knowledge-base
- 本仓库为非官方镜像，内容版权归 OceanBase / 原作者所有
- 请勿用于商业传播；官网有更新时以官方为准
