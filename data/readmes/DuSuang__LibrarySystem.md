# 图书管理系统

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![openGauss](https://img.shields.io/badge/database-openGauss-orange.svg)
![Flask](https://img.shields.io/badge/framework-Flask%203.0-green.svg)
![License](https://img.shields.io/badge/license-学习参考-lightgrey.svg)

基于 openGauss 的数据库驱动图书管理系统，采用"重数据库、瘦应用"设计理念，核心业务逻辑通过存储过程实现。

## 技术栈

- **数据库**：openGauss
- **后端**：Python 3.8+ / Flask 3.0
- **前端**：HTML5 / CSS3 / Jinja2

## ✨ 项目特点

- 📚 **完整的开发流程**：涵盖从 E-R 建模、逻辑设计到物理实现的完整数据库开发周期
- 🎯 **数据库中心化设计**：借阅、归还、预约等核心逻辑通过存储过程实现
- 🔧 **生产级实践**：全表满足 BCNF、并发控制（行级锁 + SKIP LOCKED）、事务处理、安全防护
- 📖 **清晰的代码结构**：数据库层、应用层、表现层职责分明，易于理解和扩展
- 💡 **实用的技术选型**：openGauss + Python + Flask，主流且易于上手

## 📸 项目展示

### 数据库设计

<details>
<summary>点击查看 E-R 模型与关系模式</summary>

**全局 E-R 图**

![全局E-R图](assets/全局E-R图.png)

**全局关系模式图**

![全局模式图](assets/全局模式图.png)

**系统架构图**

![系统架构图](assets/系统架构图.png)

</details>

### 核心功能

**图书检索与借阅**

![图书检索](assets/book_search.png)

![图书详情](assets/book_detail.png)

**预约排队机制**

![预约记录管理](assets/admin_reservation_record.png)

**管理员功能**

![图书管理](assets/book_manage.png)

## 快速开始

### 1. 启动数据库

```bash
docker run --name opengauss \
  -e GS_PASSWORD=<your-password> \
  -p 8888:5432 \
  -d opengauss/opengauss-server:latest
```

### 2. 配置连接

创建 `.env` 文件：

```bash
DB_HOST=127.0.0.1
DB_PORT=8888
DB_NAME=library
DB_USER=gaussdb
DB_PASSWORD=<your-password>
SECRET_KEY=<your-random-secret-key>
```

> **注意**：请将 `<your-password>` 和 `<your-random-secret-key>` 替换为实际的密码和密钥。

### 3. 初始化并启动

```bash
pip install -r requirements.txt
python init_db.py
python app.py
```

访问 `http://localhost:5000`

## 数据库设计

### 核心表结构

```sql
users(user_id, username, password_hash, role, ...)
books(book_id, title, isbn, publisher_id, category_id)
book_copies(copy_id, book_id, status, reserved_for_user_id, location)
borrow_records(borrow_id, user_id, copy_id, borrow_date, return_date)
reservations(reservation_id, user_id, book_id, reservation_date, status, ...)
```

### 存储过程

| 名称 | 功能 |
|------|------|
| `borrow_book` | 借阅图书（行级锁 + 业务校验） |
| `return_book` | 归还图书 + 自动触发预约匹配 |
| `reserve_book` | 图书预约（无可借副本时） |
| `match_reservation_for_book` | 预约匹配（SKIP LOCKED） |
| `borrow_with_reservation` | 预约取书 |
| `create_book` | 创建图书（自动处理分类/出版社/作者） |

### 关键约束

- `uq_books_isbn`：ISBN 条件唯一
- `uq_borrow_records_copy_active`：同一副本至多一条未归还记录
- `uq_reservations_user_book_active`：同一用户对同一图书至多一条活跃预约
- `ck_reserved_logic`：副本状态与预约用户一致性

## 功能特性

**读者端**：图书检索、借阅、归还、预约、预约领取、个人信息管理、热门排行

**管理员端**：统计看板、用户管理、图书管理、副本管理、借阅记录管理、预约管理

## 项目结构

```
LibraySystem/
├── app.py              # Flask 应用主文件
├── db.py               # 数据库连接封装
├── init_db.py          # 数据库初始化脚本
├── schema.sql          # 数据库 schema
├── requirements.txt    # Python 依赖
├── .env                # 环境配置（需自行创建）
├── templates/          # HTML 模板
└── static/             # 静态文件
```

## 许可证

本项目仅供学习参考使用。