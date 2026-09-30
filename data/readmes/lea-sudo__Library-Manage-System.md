# 📚 图书馆管理系统

基于 openGauss 的分馆连锁图书馆管理系统，提供统一的图书信息检索、读者服务与管理后台。

## 项目简介

系统面向分馆连锁图书馆，强调“管理一体化”：
所有新增（注册）入口整合到对应管理页面，支持增删改查，查询与状态展示更直观。

## 主要功能

- **图书信息查询**：多条件检索，含图书在馆/借出状态与预计归还时间
- **读者服务**：借书、还书、续借、借阅记录查询
- **系统管理（管理员）**：读者/图书/类别/图书馆管理（新增/编辑/删除）
- **逾期记录管理**：逾期记录列表 + 可编辑借阅记录（修正应还/归还日期）

## 技术栈

- Python 3.8+ / Flask 3.1.2
- openGauss（PostgreSQL 兼容）
- pg8000（数据库驱动）

## 数据库设计

### 关系模型

```
Reader(rid, rname, gender, phone)
Category(cid, cname)
Library(lid, lname, location, tel)
Book(bid, cid, lid, bname, author, publisher)
  FK: cid -> Category, lid -> Library
BorrowRecord(brid, rid, bid, borrow_date, due_date, return_date)
  FK: rid -> Reader, bid -> Book
```

## 使用说明（界面入口）

- 首页“图书信息”入口即为统一检索入口（含状态展示）
- 管理员在“系统管理”中进入各管理页面（新增/编辑/删除）
- 逾期记录页面可直接编辑借阅记录日期，便于纠错与强制归还

> 删除限制：若存在外键关联（如类别下有图书、图书存在借阅记录），数据库会阻止删除并提示错误。

## 默认账号

- 管理员：`admin` / `admin123`
- 读者示例账号：
  - `reader1` / `123456`
  - `reader2` / `123456`
  - `reader3` / `123456`
  - `reader4` / `123456`
  - `reader5` / `123456`

## 快速开始（镜像部署）

### 1. 构建并启动服务

```bash
docker compose up -d --build
```

默认数据库端口映射为本机 5432（容器内仍为 5432）。如端口冲突，请改为 15432:5432。macOS 上已设置为 `linux/amd64` 以兼容官方镜像。

### 2. 初始化数据库（首次启动）

确保 db 与 web 服务已启动（db 需要通过健康检查）：

```bash
docker compose ps
```

```bash
docker compose exec web python init_database.py
```

### 3. 访问系统

浏览器打开：http://127.0.0.1:5001

## 项目结构

```
library_web/
├── app.py                # Flask 应用主文件
├── db.py                 # 数据访问层
├── config.py             # 数据库配置
├── init_database.py      # 数据库初始化脚本
├── requirements.txt      # 依赖列表
├── .gitignore           # Git 忽略规则
└── templates/           # HTML 模板
    ├── index.html
    ├── book/            # 图书相关页面
    ├── reader/          # 读者服务页面
    └── admin/           # 管理功能页面
```

## 配置说明

修改 `config.py` 中数据库连接信息：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'librarydb',
    'user': 'gaussdb',
    'password': 'Aa!123456'
}
```

## 测试数据

初始化脚本自动导入：
- 2 个图书馆
- 3 个类别
- 5 个读者
- 11 本图书
- 6 条借阅记录

## 常见问题

### Docker 容器无法启动

```bash
docker restart opengauss
```

### db 容器 unhealthy

确认 `docker-compose.yml` 中为 db 设置了 `shm_size: "1g"`，然后重启：

```bash
docker compose down
docker compose up -d --build
```

### 重置数据库

```bash
python init_database.py
```

### 修改端口

```bash
docker run -d --name opengauss -e GS_PASSWORD=Aa!123456 -p 15432:5432 opengauss/opengauss:latest
```

同时修改 `config.py` 中的 `port` 为 `15432`。

---

数据库大作业 - 2026 年 1 月
