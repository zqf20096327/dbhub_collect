# 数据服务平台（Enterprise Data Service Platform）

企业级数据服务平台：把 **GBase 8a / Oracle / OceanBase(Oracle·MySQL 双模式) / MySQL / Redis / H2** 里的数据能力，通过**向导式**或 **SQL 代码式**快速发布为带鉴权、脱敏、订阅审批、监控计量的 HTTP API。开箱即用（内置 H2 元数据库 + 内置 H2 演示数据源），内网离线环境友好。

## 功能总览

### 数据服务（核心网关）
| 模块 | 能力 |
|---|---|
| 数据源管理 | MySQL / OceanBase / Oracle / GBase 8a / Redis / H2(内置演示)，HikariCP/Jedis 连接池，驱动 jar 动态加载，密码 AES 加密，连接测试，只读开关 |
| API 发布·向导式 | 6 步向导：基本信息 → 选表 → 选字段 → 查询条件（=、!=、>、>=、<、<=、LIKE、IN、BETWEEN、IS NULL，必填/默认值）→ 排序分组 → 参数与发布 |
| API 发布·SQL 式 | SELECT/WITH 语句，`#{param}` 占位参数自动解析，执行预览 |
| API 发布·Redis | GET/HGET/HGETALL/LRANGE/SMEMBERS/ZREVRANGE/SCAN/TTL/EXISTS，Key 支持 `{参数}` 模板 |
| 网关执行 | 统一入口 `/dsapi/{path}`，自动分页（`_pageNo`/`_pageSize`），方言分页（LIMIT / ROWNUM），响应缓存，滑动窗口限流，熔断降级，灰度路由，Mock 模式，trace_id 链路追踪 |
| 应用与鉴权 | AppKey/AppSecret，MD5 签名防重放（5 分钟窗口），令牌模式（X-App-Token），IP 白名单 |
| 版本管理 | 发布自动版本快照，支持历史版本回滚；发布/下线走审批流 |

### 数据资产
| 模块 | 能力 |
|---|---|
| 元数据管理 | 数据源全量/增量采集（表/字段/索引/注释），8 类敏感字段自动识别打标（手机号/身份证/姓名/银行卡/邮箱等），敏感级人工调整 |
| 资产目录 | 业务域目录树编目，资产全文检索（表+字段），API 血缘反查 |
| 动态脱敏 | 8 类规则 × 6 种脱敏方式（遮蔽/替换/截断/哈希/区间/置空），命中输出字段后网关级动态脱敏，效果实时预览 |

### 订阅与治理
| 模块 | 能力 |
|---|---|
| 订阅授权 | 应用订阅 API（字段范围/日月配额/有效期），紧急停用，续期，敏感字段明文查看申请 |
| 审批中心 | 服务发布/订阅/明文申请三类审批，OWNER/SEC/DEV/ADMIN 多角色会签 |
| 配额计量 | 日/月调用配额拦截 + 按应用/API/月计量汇总报表 |
| 批量导出 | SQL 导出任务（CSV/JSON、定时、加密、水印），执行记录，文件下载，对账 |

### 监控运维
| 模块 | 能力 |
|---|---|
| 服务器监控 | CPU/进程 CPU/物理内存/JVM 堆/线程/GC/磁盘分区实时指标，10 秒采样、60 分钟趋势（纯 JDK 实现，零第三方依赖） |
| 服务指标 | 窗口化调用统计（调用量/错误率/拒绝/平均·最大耗时），慢接口 TOP |
| 告警 | 阈值规则（错误率/耗时/拒绝数/调用量），告警抑制，告警确认（ACK），定时评估 |
| 健康检查 | 每 5 分钟对已发布服务探活，UP/DOWN 状态 |
| 安全事件 | SQL 拦截、熔断、告警等事件统一记录；操作审计日志 |

### 门户与系统
| 模块 | 能力 |
|---|---|
| 开发者门户 | 服务市场、自动生成接口文档（入参/出参/错误码）、在线调试、平台公告 |
| 系统管理 | 用户管理（ADMIN/DEV/OWNER/SEC/AUDIT 五角色 RBAC）、参数配置、操作日志 |
| 管理端 UI | 原生 HTML/JS 单页应用，**零 CDN 依赖**，内置 SVG 图表组件（折线/环形/仪表盘/条形），内网离线可用 |

## 技术栈

- Java 8 + Spring Boot 2.7.18（内网常用组合）
- 元数据库：H2（开箱即用）→ 生产可切 MySQL（改 `application.yml`）
- HikariCP（SQL 连接池）+ Jedis 4.3（Redis）
- 管理端：原生 HTML/JS + 纯 SVG 图表（零外部依赖）
- 服务器监控：com.sun.management.OperatingSystemMXBean（纯 JDK）

## 快速开始

```bash
mvn clean package -DskipTests
java -Dfile.encoding=UTF-8 -jar target/dsp-server.jar
```

启动后访问 `http://localhost:8086/`，初始账号 `admin / admin123`（登录后请修改）。

**离线体验路径**：数据源管理新建 `H2(内置演示)` 类型数据源 → 元数据管理采集 → API 服务管理向导式建 API → 发布审批 → 订阅审批 → 开发者门户调试调用。全程无需任何外部数据库。

### 推荐体验流程

1. **数据源管理** → 新建 H2 内置演示源，测试连接
2. **元数据管理** → 选择数据源采集，查看自动敏感打标
3. **API 服务管理** → 向导式 6 步创建 API（或 SQL 式），试运行，发布（触发审批）
4. **审批中心** → 通过发布/订阅申请
5. **订阅与授权** → 为应用申请订阅（字段范围/配额）
6. **开发者门户** → 在线调试调用，查看自动生成的接口文档
7. **监控与告警** → 服务器 CPU/内存/磁盘仪表盘 + 网关流量趋势 + 告警规则

### 端到端测试

仓库内置 79 项用例的可重复执行端到端测试（需平台已在本地 8086 运行，并至少一个 H2 演示数据源）：

```bash
bash e2e-test.sh
```

覆盖：鉴权矩阵（签名/令牌/开放/未授权/限流 429）、SQL 注入拦截（DELETE/DROP/多语句）、动态脱敏、订阅配额、熔断、缓存、分页、trace_id、批量导出文件落盘、告警引擎等。

## API 调用示例

### 签名模式（推荐）

```bash
TS=$(date +%s%3N)
KEY="dsp-xxxxxx"
SECRET="your-app-secret"
SIGN=$(echo -n "${KEY}${SECRET}${TS}" | md5sum | cut -d' ' -f1)

curl -X POST "http://localhost:8086/dsapi/order/list" \
  -H "Content-Type: application/json" \
  -H "X-App-Key: $KEY" -H "X-Timestamp: $TS" -H "X-Sign: $SIGN" \
  -d '{"status":"1","beginDate":"2026-01-01","_pageNo":1,"_pageSize":20}'
```

### 令牌模式

```bash
# 先换 token
curl -X POST http://localhost:8086/dsapi/token \
  -H "Content-Type: application/json" \
  -d '{"appKey":"dsp-xxxxxx","appSecret":"your-app-secret"}'
# 再携带 X-App-Token 调用
```

### 简单模式 / 开放 API

- Header 直接带 `X-App-Secret: xxx`（免签名，内网低敏场景）
- API 鉴权方式选"开放"后无需任何 Header

## SQL 模式示例

```sql
SELECT order_id, cust_name, amount, create_time
FROM orders
WHERE status = #{status}
  AND create_time >= #{beginDate}
```

点"解析参数"自动生成参数表；调用方传 `{"status":"1","beginDate":"2026-01-01"}`。

## 驱动安装

将以下驱动 jar 放入运行目录的 `./drivers` 文件夹（平台启动时自动加载注册）：

| 数据源 | 驱动 jar | 驱动类 |
|---|---|---|
| MySQL | mysql-connector-java-8.x | com.mysql.cj.jdbc.Driver |
| OceanBase | oceanbase-client-*.jar | com.alipay.oceanbase.jdbc.Driver |
| Oracle | ojdbc8.jar | oracle.jdbc.OracleDriver |
| GBase 8a | gbase-connector-java-*.jar | com.gbase.jdbc.Driver |

目录配置在 `application.yml` 的 `dsp.drivers-dir`。

## 生产部署建议

1. **元数据库切 MySQL**：`application.yml` 中替换 spring.datasource（schema.sql 兼容）。
2. **修改 AES 密钥**：`dsp.aes-key` 必须更换，否则数据源密码可被熟悉默认密钥的人解出。
3. **修改管理员密码**：登录后修改 `sys_user`（密码列为 `sha256(密码+盐)`）。
4. **HTTPS**：前置 Nginx 做 TLS 终结。
5. **限流/缓存**：默认单机内存实现，多实例部署时扩展为 Redis 版本。
6. **只读**：业务数据源保持 `read_only=1`，网关只提供查询能力。

## 项目结构

```
src/main/java/com/enterprise/dsp/
├── DspApplication.java            启动类
├── common/                        Result / CryptoUtil / SqlSecurityUtil / AuthInterceptor / 全局异常
├── dao/                           BaseDao 通用 CRUD + Repos 实体 DAO 汇总
├── datasource/                    DataSourceManager 动态数据源池 + 驱动动态加载
├── entity/                        DsInfo / ApiInfo / AppInfo
├── service/
│   ├── GatewayService.java        网关执行引擎（构建/解析/脱敏/分页/缓存/限流/熔断/灰度/Mock）
│   ├── MetaService.java           元数据采集 + 敏感打标
│   ├── MaskingEngine.java         动态脱敏引擎
│   ├── AccessService.java         订阅/授权/配额
│   ├── MonitorService.java        指标聚合/告警/熔断/健康检查
│   ├── SysMetricsService.java     服务器系统监控（CPU/内存/磁盘/JVM + 趋势采样）
│   ├── BatchService.java          批量导出
│   └── AdminService.java          管理端服务
└── controller/
    ├── AdminController.java       /dsp/api/**  基础管理接口
    ├── ManageController.java      /dsp/api/**  扩展模块接口（元数据/资产/脱敏/订阅/审批/监控/批量/门户）
    ├── GatewayController.java     /dsapi/**    网关入口（鉴权/白名单/签名/令牌）
    └── WebConfig.java             拦截器配置
src/main/resources/
├── application.yml
├── schema.sql                     元数据库结构（H2/MySQL 兼容）
└── static/index.html              管理端单页应用（含 SVG 图表组件库）
```

## 已知边界

- Oracle 分页用 ROWNUM 包装，兼容 11g；限流/缓存/趋势采样为单机内存实现，多实例需扩展为 Redis 版。
- GBase 8a 走 MySQL 协议；如驱动行为有差异，按报错调整即可。
- 批量定时调度与灰度路由为基础实现，可按需扩展。
- 元数据库升级跨版本时如遇列变更，需重置本地 `data/` 目录（H2 `CREATE TABLE IF NOT EXISTS` 不补列）。

## License

MIT License —— 详见 [LICENSE](LICENSE)。
