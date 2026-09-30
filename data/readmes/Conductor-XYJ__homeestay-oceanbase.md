# Homeestay Project (OceanBase + Docker Version)

这是一个基于 Spring Boot + OceanBase 的民宿管理系统后端项目。本项目已完成 Docker 化封装，支持一键部署运行。

## 🚀 快速开始 (Quick Start)

### 1. 环境要求
- Docker Desktop (Windows/Mac) 或 Docker Engine + Docker Compose (Linux)
- 建议 Docker 分配内存 > 6GB (OceanBase 运行需求)

### 2. 启动项目
在项目根目录下打开终端，执行以下命令：

```bash
docker-compose up -d
```

### 3. 等待初始化
**重要提示**：首次启动时，OceanBase 数据库启动和初始化需要较长时间（约 2-5 分钟）。

- 系统会自动启动一个 `db-init` 容器来创建数据库并导入数据。
- 你可以通过以下命令查看初始化进度：
  ```bash
  docker-compose logs -f db-init
  ```
- 当看到 `Data import finished` 字样时，表示数据库准备就绪。

### 4. 访问应用
- **API 根地址**: `http://localhost:8080`
- **测试图片访问**: [http://localhost:8080/uploaded/1.png](http://localhost:8080/uploaded/1.png)

---

## ⚠️ 注意事项 (Important Notes)

### 1. 本地图片服务 (Local Image Serving)
为了确保项目在任何环境下都能正常显示图片，本项目已配置为**使用本地文件系统**。
- 图片文件位于项目根目录的 `uploaded/` 文件夹中。
- 数据库数据已预设为指向 `http://localhost:8080/uploaded/...`。
- **请勿删除或重命名 `uploaded` 文件夹**，否则前端将无法加载图片。

### 2. 数据库自动初始化
`docker-compose.yml` 中包含了一个 `db-init` 服务，它负责：
1. 等待 OceanBase 数据库健康检查通过。
2. 自动执行 `homeestay_ustb.sql` 脚本。
3. 创建 `homeestay_ustb` 库并导入初始数据。

如果应用启动时报错 `Unknown database`，这是正常的，应用配置了 `restart: always`，会自动重试直到数据库初始化完成。

### 3. 敏感信息 (Secrets)
由于 GitHub 安全策略，代码中的阿里云 AccessKey (用于短信和 OSS) 已被移除（替换为 `YOUR_ACCESS_KEY`）。
- **图片功能**：已改为本地存储，**不需要** 配置 OSS Key 即可正常使用。
- **短信功能**：如果必须测试短信验证码，请在 `src/main/java/com/ustb/boot/util/SmsUtils.java` 中填入有效的阿里云 Key。

### 4. 端口占用
请确保本地以下端口未被占用：
- `8080`: Spring Boot 应用
- `2881`: OceanBase 数据库
- `6379`: Redis

## 🛠️ 常用命令

```bash
# 停止并删除所有容器和卷（重置环境）
docker-compose down -v

# 查看应用日志
docker-compose logs -f app

# 重启应用容器
docker-compose restart app
```
