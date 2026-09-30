# 基于web的数据库客户端
主要解决gauss数据库的mysql兼容模式，没有好用的跨平台的客户端。
- 支持的数据库类型
  - [x] opengauss/gaussdb mysql兼容模式
  - [ ] mysql

- 支持的功能
  - 多连接管理
  - 连接的数据库列表查看
  - 数据库的表列表查看
  - 执行SQL查询

# 目录说明

- 前端模块 db_client_gui_ui ，开发框架react
- 后端模块 db_client_gui_backend ，开发框架spring-boot

# 构建

执行build.bat

# 运行

运行文件目录 db_client_gui_backend/target/db-client-backend.jar

**创建application.yml配置文件**
```yaml
# application.yml
db:
  key: "加密数据库文件的密码"
```
**启动**
```shell
java -jar db-client-backend.jar
```