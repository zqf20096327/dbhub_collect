# DMViewer - 达梦数据库管理工具

一个基于 Web 的达梦数据库管理和终端调试工具，提供数据库管理、WebShell 终端、文件传输等核心功能。

## 功能特性

- 🗄️ **数据库管理**
  - 数据库连接与断开
  - Schema 和表结构浏览
  - SQL 查询执行（支持 Monaco Editor 编辑器）
  - 表数据查看与导出
  - 列注释展示

- 💻 **WebShell 终端**
  - 基于 WebSocket 的交互式终端
  - 支持 xterm.js 终端仿真
  - 实时命令执行与输出

- 📁 **文件传输**
  - 服务器文件浏览
  - 文件上传/下载
  - 在线文件编辑（Monaco Editor）
  - 文件重命名、删除、创建目录
  - 导入服务器 SQL 文件

## 技术栈

### 后端
- **Go** 1.25+
- **GORM** - ORM 框架
- **达梦数据库驱动** - `gitee.com/chunanyong/dm`
- **gorilla/websocket** - WebSocket 支持
- **creack/pty** - 伪终端支持

### 前端
- **Monaco Editor** - 代码编辑器
- **xterm.js** - 终端仿真
- **原生 JavaScript** - 无框架依赖

## 快速开始

### 编译构建

```powershell
# 使用构建脚本（Windows/Linux 交叉编译）
.\build.ps1

# 或手动构建
go build -o dmviewer.exe .
```

构建产物将输出到 `dist/` 目录。

### 运行程序

```bash
# 默认配置（端口 8088，监听所有地址）
./dmviewer

# 指定端口
./dmviewer -port 9090

# 仅限本机访问
./dmviewer -host 127.0.0.1 -port 9090

# 禁用空闲超时
./dmviewer -t 0

# 使用环境变量设置端口
PORT=8080 ./dmviewer
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-port` | 服务监听端口（也可通过 `PORT` 环境变量设置） | `8088` |
| `-host` | 服务绑定地址（默认监听所有网卡） | `0.0.0.0` |
| `-t` | 空闲超时自动关闭，单位分钟（0=不启用） | `30` |

### 访问服务

启动后访问：`http://localhost:8088`

## 项目结构

```
dmviewer/
├── main.go              # 程序入口，HTTP 服务配置
├── database/            # 数据库连接层
│   └── db.go
├── handlers/            # HTTP 请求处理器
│   ├── handlers.go      # 数据库相关 API
│   └── shell.go         # WebShell WebSocket 处理
├── models/              # 数据模型
│   └── models.go
├── templates/           # 前端静态资源
│   ├── index.html       # 主页面
│   └── vendor/          # 第三方前端库（离线）
├── dist/                # 构建输出目录
├── build.ps1            # 构建脚本
├── go.mod               # Go 模块依赖
└── go.sum
```

## API 接口

### 数据库管理
- `POST /api/connect` - 连接数据库
- `POST /api/disconnect` - 断开连接
- `GET /api/status` - 连接状态
- `GET /api/schemas` - 获取 Schema 列表
- `GET /api/tables` - 获取表列表
- `GET /api/table/info` - 获取表结构信息
- `GET /api/table/data` - 获取表数据
- `POST /api/query` - 执行 SQL 查询

### 文件管理
- `GET /api/server-files` - 浏览服务器文件
- `POST /api/import-server-file` - 导入服务器文件
- `GET /api/file/browse` - 文件浏览
- `POST /api/file/upload` - 文件上传
- `GET /api/file/download` - 文件下载
- `POST /api/file/delete` - 删除文件
- `POST /api/file/mkdir` - 创建目录
- `POST /api/file/rename` - 重命名
- `GET /api/file/read` - 读取文件
- `POST /api/file/write` - 写入文件

### WebShell
- `WS /api/shell/ws` - WebSocket 终端连接

## 环境要求

- **Go** 1.25+
- **达梦数据库** 客户端驱动
- **浏览器** 现代浏览器（Chrome、Edge、Firefox 等）

## 内网离线运行

项目前端依赖已本地化（`templates/vendor/` 目录），支持完全离线运行，无需访问外部 CDN。

## 注意事项

1. **数据库驱动**：需要安装达梦数据库客户端驱动
2. **安全性**：建议在生产环境中配置 `-host 127.0.0.1` 限制访问
3. **空闲超时**：默认 30 分钟无操作自动关闭，可使用 `-t 0` 禁用
4. **端口占用**：如遇端口冲突，可通过 `-port` 或 `PORT` 环境变量修改

## 开发

```bash
# 安装依赖
go mod tidy

# 运行开发服务器
go run main.go

# 构建特定平台
GOOS=linux GOARCH=amd64 go build -o dmviewer-linux-amd64 .
GOOS=windows GOARCH=amd64 go build -o dmviewer-windows-amd64.exe .
```

## 许可证

本项目仅供学习和内部使用。

## 版本历史

- **v1.0** - 初始版本
  - 数据库管理功能
  - WebShell 终端
  - 文件传输与在线编辑
  - SQL 编辑器增强
