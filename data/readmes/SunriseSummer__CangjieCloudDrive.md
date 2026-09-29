# CDrive · 仓颉云盘

基于 **仓颉 (Cangjie)** 编程语言开发的云盘 Web 应用，使用 **MinIO S3** 对象存储存放文件，**OpenGauss** 数据库存储文件元数据。

## 架构

```
┌──────────────────────────────────────────────┐
│              CDrive Web App                  │
│         (Cangjie HTTP Server)                │
├──────────────────────────────────────────────┤
│  Route Layer    │  前端页面 (HTML/CSS/JS)      │
│  Service Layer  │  文件管理、搜索、预览         │
│  DAO Layer      │  数据库连接、JSON 转换        │
├─────────────────┼────────────────────────────┤
│  MinIO S3       │  OpenGauss DB              │
│  (文件存储)      │  (元数据存储)               │
└─────────────────┴────────────────────────────┘
```

## 功能特性

- 📁 文件上传 / 下载 / 预览
- 📂 文件夹创建 / 管理
- 🔍 文件搜索
- ✏️ 文件重命名
- 🗑️ 文件删除
- 📊 存储统计
- 💻 项目源码自动预置
- 🎨 专业优雅的前端界面
- 📱 网格视图 / 列表视图切换
- 🖱️ 右键上下文菜单

## 快速开始

### 前提条件

- Docker & Docker Compose
- Cangjie SDK 1.1.0
- Cangjie STDX 1.1.0

### 一键启动

```bash
chmod +x start.sh
./start.sh
```

说明：OpenGauss 元数据默认持久化到 `./data/opengauss`，MinIO 对象数据持久化到 `./data`。

### 手动启动

1. 启动 Docker 服务（MinIO + OpenGauss）：
```bash
docker-compose up -d
```

2. 设置环境变量：
```bash
source ../cangjie/envsetup.sh
export CANGJIE_STDX_PATH=/path/to/cangjie-stdx/linux_x86_64_cjnative/dynamic/stdx
export LD_LIBRARY_PATH=$CANGJIE_STDX_PATH:$PWD/target/release/s3client:$PWD/target/release/opengauss@cangjie_tpc:$LD_LIBRARY_PATH
```

3. 编译运行：
```bash
cjpm build
./target/release/bin/main
```

4. 访问 http://localhost:8080

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CDRIVE_DB_URL` | `opengauss://gaussdb:Root%40123456@127.0.0.1:15433/omm?sslmode=disable` | 数据库连接 URL |
| `CDRIVE_S3_ENDPOINT` | `http://127.0.0.1:9000` | MinIO S3 端点 |
| `CDRIVE_S3_ACCESS_KEY` | `sunrise2026` | S3 访问密钥 |
| `CDRIVE_S3_SECRET_KEY` | `sunrise2026` | S3 秘密密钥 |
| `CDRIVE_S3_BUCKET` | `cdrive` | S3 存储桶名称 |
| `CDRIVE_HOST` | `0.0.0.0` | 服务监听地址 |
| `CDRIVE_PORT` | `8080` | 服务监听端口 |
| `CDRIVE_SKIP_SEED` | `false` | 是否跳过预置文件 |

## 项目结构

```
cdrive/
├── cjpm.toml              # 项目配置
├── docker-compose.yml     # Docker 服务定义
├── start.sh               # 一键启动脚本
├── sql/
│   └── init.sql           # 数据库初始化 SQL
├── static/
│   └── index.html         # 前端页面
├── opengauss-driver/      # OpenGauss 数据库驱动
└── src/
    ├── main.cj            # 入口
    ├── dao/               # 数据访问层
    │   ├── DbConnector.cj
    │   └── JsonHelper.cj
    ├── service/           # 业务逻辑层
    │   ├── StorageService.cj  # S3 存储服务
    │   ├── FileService.cj     # 文件管理服务
    │   └── SeedService.cj     # 预置文件服务
    ├── route/             # 路由层
    │   └── FileRoute.cj
    ├── util/              # 工具类
    │   └── HttpHelper.cj
    └── web/               # Web 相关
        └── PageLoader.cj
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 前端页面 |
| GET | `/api/files?path=/` | 列出目录文件 |
| POST | `/api/upload?path=/&name=file.txt` | 上传文件 |
| POST | `/api/mkdir` | 创建文件夹 |
| POST | `/api/delete` | 删除文件 |
| GET | `/api/download?id=1` | 下载文件 |
| GET | `/api/preview?id=1` | 预览文件 |
| POST | `/api/rename` | 重命名 |
| GET | `/api/search?q=keyword` | 搜索文件 |
| GET | `/api/stats` | 存储统计 |
| GET | `/api/file?id=1` | 文件详情 |

## 技术栈

- **语言**: 仓颉 (Cangjie) 1.1.0
- **Web 框架**: 仓颉标准扩展库 `stdx.net.http`
- **对象存储**: MinIO S3
- **数据库**: OpenGauss 3.0.0
- **S3 客户端**: CangjieS3Client
- **数据库驱动**: CangjieGaussDB opengauss-driver
