# OpenGaussWeb 学生管理系统

一个用于演示学生、课程与成绩管理的轻量级 Web 应用。

- 运行方式：
	- 可自定义：`docker-compose.yml`（需 `.env` 提供变量）
	- 已配置：`docker-compose-release.yml`（内置默认参数，直接构建运行）

提示：数据库及应用凭据需通过环境变量注入。

## 最低要求
- Docker 24+、Docker Compose v2+

## 目录简述
- `src/` 应用源代码
- `db/init.sql` 初始化数据库脚本
- `Dockerfile` 应用镜像构建文件
- `docker-compose.yml` 部署编排（可自定义）
- `docker-compose-release.yml` 部署编排（已配置）

如需自行构建 Jar，请在本地执行 `mvn -DskipTests package`，结果位于 `target/`。
