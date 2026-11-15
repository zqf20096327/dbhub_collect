# 纸间 · Paper Club

[![Django checks](https://github.com/Top-1-Lj/paper-club/actions/workflows/tests.yml/badge.svg)](https://github.com/Top-1-Lj/paper-club/actions/workflows/tests.yml)
[MIT License](LICENSE)

面向学生和研究小组的论文共读应用。将论文资料、结构化阅读笔记和讨论集中在同一处，帮助读者记录理解、提出问题并交流观点。

基于 **Python、Django 和 SQLite** 构建，使用服务端模板和本地静态资源，运行应用无需模型 API 或 GPU。

## 功能

- **论文库**：手动录入标题、作者、年份、摘要、标签、DOI、原文和代码链接。
- **阅读卡片**：按研究问题、核心方法、主要结果、局限、个人理解、待讨论问题组织笔记；每位读者可为同一论文维护自己的卡片。
- **共读讨论**：浏览其他人的卡片并发表评论，作者可编辑和删除自己的内容。
- **个人阅读**：独立记录未读、在读、已读状态，按关键词和状态筛选自己的卡片。
- **检索与导出**：按标题、作者、标签搜索，支持分页、Markdown 笔记和 BibTeX 引用导出。
- **示例内容**：提供可重复初始化的样例，以及附来源定位的 XR 隐私与个性化联邦学习导读。

## 界面预览

![论文广场](docs/screenshots/curated-library.jpg)

[阅读卡片](docs/screenshots/curated-xr-multimodal.jpg) · [移动端](docs/screenshots/curated-mobile-source.jpg)

## 快速开始

需要 Git 和 Python **3.11–3.14**。SQLite 随 Python 提供；首次安装依赖需要网络。

### Windows PowerShell

```powershell
git clone https://github.com/Top-1-Lj/paper-club.git
cd paper-club
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py import_papers
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### Linux / macOS

```bash
git clone https://github.com/Top-1-Lj/paper-club.git
cd paper-club
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo
.venv/bin/python manage.py import_papers
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)。保持终端运行，按 `Ctrl+C` 停止服务；再次启动会继续使用已有数据库。

`seed_demo` 和 `import_papers` 用于加载示例内容。需要空白数据库时，可省略这两步并自行注册账号。

### 演示账号

执行 `seed_demo` 后可使用以下普通账号：

| 用户名 | 初始密码 |
| --- | --- |
| `lin` | `PaperClub2026!` |
| `chen` | `PaperClub2026!` |

初始化命令可重复执行，保留已有密码和编辑。演示账号用于开发体验，正式使用可注册自己的账号

## 使用流程

1. 在论文广场搜索或选择论文，也可登录后录入新条目。
2. 打开论文详情，设置个人阅读状态并创建阅读卡片。
3. 查看其他读者的理解，在卡片下提出问题或补充说明。
4. 在“我的阅读卡片”中管理笔记，或导出 Markdown 和 BibTeX。

完整体验流程见 [使用演示](docs/DEMO.md)。

论文、卡片、评论和导出内容对应用访问者公开；“我的阅读卡片”用于筛选个人内容，不提供私密存储。登录后才能写入，论文由录入者维护，卡片和评论由作者维护。已有阅读卡片关联的论文受删除保护。

## 示例数据与导读

示例通过命令生成，数据库文件不纳入版本管理。`seed_demo` 提供论文、笔记和评论样例；`import_papers` 从 [data/papers](data/papers) 导入三篇论文及其导读卡片。

导读区分原文结论和辅助理解，保留 PDF 页码、章节或图表定位，并标注“基于论文原文整理，AI辅助生成，待人工复核”。论文正文不包含在仓库中，可通过记录中的来源链接查阅。

数据格式、重复导入规则和来源说明见 [导读数据文档](docs/CURATED_IMPORT.md)。

## 配置

配置通过环境变量传入；[.env.example](.env.example) 是示例文件，应用不会自动加载它。

| 环境变量 | 默认值 / 用途 |
| --- | --- |
| `DJANGO_DEBUG` | `1`，开发模式；设为 `0` 关闭调试 |
| `DJANGO_SECRET_KEY` | 开发密钥；关闭调试时必须提供独立密钥 |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost,[::1]`，以逗号分隔 |
| `PAPERCLUB_DB_PATH` | 项目目录中的 `db.sqlite3`，可指定其他数据库路径 |

## 开发与测试

Windows：

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```

Linux / macOS 将 Python 路径替换为 `.venv/bin/python`。测试使用独立数据库，覆盖权限、数据保存、检索、导出和数据导入。GitHub Actions 在 Python 3.11 和 3.13 上执行检查，结果见 [CI](https://github.com/Top-1-Lj/paper-club/actions/workflows/tests.yml)。

## 项目结构

```text
paper-club/
├── club/          # 业务模型、表单、视图、导出、管理命令和测试
├── paperclub/     # Django 配置与入口
├── templates/     # 页面模板
├── static/        # 本地样式与界面资源
├── data/papers/   # 导读元数据、卡片和证据定位
├── docs/          # 使用、架构、测试和来源文档
├── manage.py
└── requirements.txt
```

## 适用范围

当前版本适合本地运行和小规模共读试用，使用 SQLite 与 Django 开发服务器。生产部署需要配置正式 WSGI / ASGI 服务、静态文件、密钥和数据库，并评估并发与备份方案。

论文信息采用手动录入；自动抓取、PDF 解析、在线 AI 问答、组内可见性和统一登录未实现。

## 文档与参与

- [使用演示](docs/DEMO.md)
- [架构与数据模型](docs/ARCHITECTURE.md)
- [导读数据与来源](docs/CURATED_IMPORT.md)
- [测试指南](docs/VERIFICATION.md)
- [贡献指南](CONTRIBUTING.md)

问题与建议请提交到 [Issues](https://github.com/Top-1-Lj/paper-club/issues)，功能改进可提交 Pull Request。维护者：[Top-1-Lj](https://github.com/Top-1-Lj)。

## 许可证

项目源码采用 [MIT License](LICENSE)。所引用论文及其他第三方材料的权利归各自权利人所有。
