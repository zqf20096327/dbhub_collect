#  基于 OpenGauss 的校园二手书籍共享系统

> 一款面向高校的国产数据库驱动的二手书籍交易与共享平台，助力绿色校园建设与资源循环利用。

##  项目简介

本项目针对当前高校二手书籍流转中存在的“信息孤岛”、“资源错配”以及交易信任缺失等问题，设计并实现一个基于 **openGauss** 企业级数据库的校园专属二手书籍共享系统。系统充分利用 openGauss 的高性能并发控制、全密态计算、智能运维等特性，为在校学生提供安全、高效、可信的二手书籍发布、检索、交易与评价服务，同时为学校管理者提供可视化数据统计与内容审核功能。

##  技术栈

- **数据库**：openGauss（主备集群，读写分离）
- **后端框架**：Spring Boot + MyBatis
- **前端**：Vue.js（Web 端） + 微信小程序（移动端）
- **监控运维**：Prometheus + openGauss 监控插件
- **开发工具**：Maven / Gradle，JDBC（openGauss 官方驱动）
- **安全机制**：全密态计算、行级安全策略、动态数据脱敏、统一审计

## 主要功能

### 学生端
- 书籍浏览与多维度搜索（分类、价格、新旧程度等）
- 发布闲置二手书（上传图片、自主定价）
- 个人中心（资料维护、收货地址管理、登录注册）
- 交易完成后评价反馈

###  管理员端
- 用户注册审核与角色权限配置
- 二手书籍信息审核、违规下架
- 可视化数据统计（交易量、用户活跃度、书籍分类占比等）
- 用户反馈处理

##  系统架构

- **数据库层**：openGauss 一主两备集群，主节点处理写入事务，备节点承担查询与统计分析，实现读写分离。
- **应用层**：Spring Boot 提供 RESTful API，通过 JDBC 与 openGauss 交互，MyBatis 完成 ORM 映射。
- **前端层**：Vue.js 构建响应式 Web 界面，微信小程序提供移动端服务。
- **安全与运维**：全密态计算保障敏感信息（学号、手机号等）加密；AI 参数调优 + 慢 SQL 诊断 + 索引推荐实现智能运维；Cgroups 资源管控隔离交易与分析负载。

## 快速开始

### 环境要求
- JDK 11+
- Maven 3.6+
- openGauss 3.0+（或更高版本）
- Node.js 14+（前端构建）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-repo/campus-book-sharing.git
   cd campus-book-sharing
2.数据库初始化
• 在 openGauss 中创建数据库及用户
• 执行 docs/schema.sql 创建表结构
• 导入初始数据（可选 docs/data.sql）
3.后端配置
cd backend
cp application-example.yml application.yml
# 修改数据库连接、加密密钥等配置
mvn clean package
java -jar target/book-sharing-1.0.jar
4.前端运行
cd frontend-web
npm install
npm run serve
5.微信小程序
• 使用微信开发者工具打开 frontend-miniprogram 目录
• 配置小程序 AppID 和后端接口地址
项目结构
.
├── backend/               # Spring Boot 后端
│   ├── src/main/java     # 业务代码（Controller, Service, Mapper）
│   └── src/main/resources # 配置、SQL 映射文件
├── frontend-web/          # Vue.js Web 端
├── frontend-miniprogram/  # 微信小程序端
├── docs/                  # 数据库脚本、设计文档
└── README.md
关键设计亮点
• 高并发一致性：利用 openGauss 的 NUMA-Aware 原子操作、无锁化事务与 MVCC，解决热门教材“秒杀”场景下的超售问题。
• 全密态计算：学生手机号、学号等敏感信息在存储、传输、计算全链路加密，满足《个人信息保护法》合规要求。
• 多模数据融合：行存 (UStore) 支撑高频交易，列存 + 向量化引擎加速统计查询，向量存储实现书籍相似度推荐。
• 智能运维：AI 参数自调优、慢 SQL 诊断、索引推荐，结合 Prometheus 监控，无需专业 DBA 即可长期稳定运行。
应用前景
• 社会效益：降低学生购书成本，推动绿色低碳校园建设。
• 技术推广：为国产数据库 openGauss 在高校信息化中的落地提供示范案例。
• 商业潜力：支持广告、服务费、书籍消毒/配送等增值服务，可吸引校园创业团队运营。
贡献指南
欢迎提交 Issue 和 Pull Request。请确保代码符合项目编码规范，并补充相应的单元测试。
许可证
本项目采用 MIT License。
联系方式
• 项目作者：闫家辉（兰州理工大学 软件工程鲲鹏1班）
• 指导教师：许天鹏
• 高校：兰州理工大学 计算机与人工智能学院
若您在使用过程中遇到问题或有改进建议，请通过 GitHub Issues 与我们联系。

