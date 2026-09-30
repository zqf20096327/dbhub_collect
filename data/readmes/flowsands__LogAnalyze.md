# LogAnalyze - GaussDB日志分析工具

📋 一个功能强大的GaussDB集群日志分析工具，支持压缩文件解压、多节点日志分析、时间轴追踪等功能。

## ✨ 主要特性

### 🔍 日志分析功能
- **Action时间轴追踪** - 自动追踪action的enter/leave状态，标记未完成的action（红色显示）
- **Process Failed检测** - 自动检测并展示包含"process failed"的日志
- **Agent ERROR日志** - 过滤并展示Roach Agent中的ERROR日志（大写匹配）
- **GaussDB FATAL/PANIC** - 分析GaussDB日志中的FATAL和PANIC错误，自动去重

### 📦 文件处理
- **嵌套压缩包解压** - 自动递归解压ZIP/TAR.GZ嵌套压缩包
- **多节点支持** - 支持分析多IP节点的GaussDB集群日志
- **智能解压** - 解压到源文件同级目录，自动创建同名子目录

### 🎯 过滤与展示
- **时间区间过滤** - 精准的时间范围过滤功能
- **行数限制** - 可配置最大显示行数，避免数据过载
- **文件路径展示** - 每条日志显示完整的文件绝对路径

### 💻 用户体验
- **HTML5文件上传** - 完美支持Windows 11，无需依赖Swing
- **UTF-8编码** - 全面支持中文，无乱码问题
- **清理重置** - 一键清理临时文件和重置状态
- **响应式界面** - 美观的Web界面，支持标签页切换

## 🚀 快速开始

### 环境要求
- JDK 1.8+
- Maven 3.6+

### 启动方式

#### 方式1：使用启动脚本（推荐）
```bash
# Windows
start.bat

# 或使用Maven
mvn spring-boot:run
```

#### 方式2：打包运行
```bash
# 打包
mvn clean package

# 运行
java -jar target/log-analyze-1.0.0.jar
```

访问：**http://localhost:8080**

## 📖 使用指南

### 1. 上传文件
- 点击虚线框选择压缩文件（.zip/.tar.gz）
- 或拖拽文件到上传区域
- 显示文件名和大小信息

### 2. 解压文件
- **可选**：选择解压目录（默认为源文件同级目录）
- 点击"🔓 上传并解压文件"
- 自动处理所有嵌套压缩包

### 3. 分析日志
- 设置时间过滤范围（可选）
- 设置最大显示行数（默认100）
- 点击"🔍 开始分析"
- 在4个标签页查看结果

### 4. 清理与重置
- 点击"🔄 重置状态" - 清空所有输入和结果
- 点击"🗑️ 清理临时文件" - 删除解压产生的临时目录

## 📁 日志文件结构

工具支持以下目录结构：

```
xxxxx.zip
├── 192.168.1.100.zip/          # 数据库节点IP
│   └── logfiles/
│       └── log.zip              # 嵌套压缩包
│           ├── gs_log/
│           │   ├── dn_6001/     # DN节点
│           │   │   └── gaussdb-*.log
│           │   └── cn_5001/     # CN节点
│           │       └── gaussdb-*.log
│           └── roach/
│               ├── agent/
│               │   └── roach_agent-*.log
│               └── controller/
│                   └── roach_controller-*.log
├── 192.168.1.101.zip/           # 第二个节点
└── 192.168.1.102.zip/           # 第三个节点
```

## 🛠️ 技术栈

### 后端
- **Spring Boot 2.7.18** - Web框架
- **Apache Commons Compress** - 压缩文件处理
- **Lombok** - 简化代码

### 前端
- **HTML5** - 文件上传
- **CSS3** - 响应式样式
- **JavaScript** - 交互逻辑

### 构建
- **Maven** - 项目构建和依赖管理

## 📊 功能详解

### Action时间轴
- 自动识别日志中的`action is [xxx]`格式
- 追踪enter和leave状态
- **红色标记**未完成的action（只有enter没有leave）

### 时间过滤
- 支持datetime-local格式（HTML5）
- 精准的时间范围过滤
- 兼容多种日期格式

### 去重功能
- GaussDB FATAL/PANIC日志自动去重
- 基于日志内容（去除时间戳）进行去重

## 🔧 配置说明

### 日志配置
编辑 `src/main/resources/application.properties`：

```properties
# 日志级别
logging.level.com.loganalyze=INFO

# 日志文件路径
logging.file.name=./logs/log-analyze.log

# 日志文件大小限制
logging.logback.rollingpolicy.max-file-size=10MB

# 保留天数
logging.logback.rollingpolicy.max-history=30
```

### 端口配置
```properties
server.port=8080
```

## 📝 测试数据生成

项目包含多个测试数据生成脚本：

```bash
# 生成多节点多天测试数据
powershell -ExecutionPolicy Bypass -File generate_test_multiday.ps1

# 生成多节点测试数据
powershell -ExecutionPolicy Bypass -File generate_test_multinode.ps1

# 生成嵌套压缩包测试数据
powershell -ExecutionPolicy Bypass -File generate_test_nested.ps1
```

## 🐛 故障排查

### 中文乱码
使用 `start.bat` 启动，自动设置UTF-8编码。

### 端口占用
```bash
# 查找占用8080端口的进程
netstat -ano | findstr :8080

# 关闭进程
taskkill /PID <PID> /F
```

### 解压失败
检查压缩包格式是否为.zip或.tar.gz，确保文件未损坏。

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题或建议，请提交Issue。
