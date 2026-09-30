# 📚 基于 B/S 架构的图书管理系统

本项目是《数据库应用实践》课程实验项目，采用 Python Flask 框架连接部署在华为云 ECS 上的 openGauss 数据库。

## 🛠️ 技术栈
- **后端**: Python 3.x, Flask
- [cite_start]**数据库**: openGauss 5.0.1 (部署于华为云 ECS)
- **驱动**: psycopg2

## 🚀 核心实践：云数据库排错记录

本项目最大的技术价值在于解决了复杂的云端环境配置问题：

### 1. 解决云服务器网络连通性
- [cite_start]**问题**: 本地程序连接华为云数据库频繁超时 (`Connection timed out`) 。
- [cite_start]**解决**: 意识到华为云具有“双重防火墙”。除了关闭 Linux 内部防火墙，还需在华为云控制台**安全组**中添加入方向规则，放行 TCP 26000 端口 。

### 2. 解决 openGauss 认证加密兼容性
- [cite_start]**问题**: 报错 `fe_sendauth: invalid authentication request` 。
- [cite_start]**分析**: openGauss 默认使用 SHA256 加密，而 Python 驱动默认使用 MD5 。
- **解决**:
    - [cite_start]修改服务器 `postgresql.conf`，设置 `password_encryption_type = 1` (MD5 模式) 。
    - 修改 `pg_hba.conf` 允许远程连接。
    - [cite_start]重置用户密码以更新哈希值 。

## 📝 功能实现
- [x] [cite_start]图书信息的 CRUD（增删改查）操作
- [x] [cite_start]使用 SQL 聚集函数 `COUNT(*)` 实现库存统计
- [x] [cite_start]基于 Bootstrap 的响应式前端界面