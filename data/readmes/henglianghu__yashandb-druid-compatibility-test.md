# yashandb-druid-compatibility-test

用于验证 **Druid(已补丁支持 `jdbc:yasdb:` 推断)** + **YashanDB JDBC** 的最小 Spring Boot 3 联调应用。

## 1) 依赖说明
- **Druid（Boot3 Starter）**：`com.alibaba:druid-spring-boot-3-starter:${druid.version}`（默认 `1.2.28`）
  - 如果你在 Druid 源码仓库里改了 Druid（例如增加 `jdbc:yasdb:` 识别），请先在 Druid 仓库根目录执行安装到本地仓库：
    - `mvn -DskipTests install`
  - 然后本项目会使用本地仓库中的 `1.2.28` 构建产物。
- **YashanDB JDBC**：`com.yashandb:yashandb-jdbc:${yashandb.jdbc.version}`（默认 `1.9.24`）

## 2) 配置（通过环境变量）
默认端口：`18080`（可用 `SERVER_PORT` 覆盖）

至少需要：
- `YASDB_URL`：例如 `jdbc:yasdb://127.0.0.1:1688/REGRESS?productName=Oracle`
- `YASDB_USER`
- `YASDB_PASS`

可选：
- `DRUID_LOGIN_USERNAME` / `DRUID_LOGIN_PASSWORD`：访问 `/druid/*` 监控页的账号密码

## 3) 运行
在本目录执行：

```bash
mvn spring-boot:run
```

或在 IDEA 里运行 `com.yashandb.tool.compat.YashanDruidCompatibilityTestApplication`。

## 4) 验证点
- **Druid 监控页面**：`http://localhost:18080/druid/index.html`
- **连通性/元数据**：
  - `GET http://localhost:18080/api/db/meta`
  - `GET http://localhost:18080/api/db/select1`
- **Druid 推断结果（driver/dbType）**：
  - `GET http://localhost:18080/api/druid/infer`

