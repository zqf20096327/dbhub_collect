# OceanBase 智能巡检系统（oceanbase-monitor）

面向银行内部 OceanBase 国产数据库的 AIOps 智能巡检平台（两地三中心演示背景）：

**定时/手动采集关键指标 → 规则引擎阈值判定 → 告警（收敛/确认/通知/自动恢复）→ 多 Agent AI 根因诊断 → 自治处置（守卫链 + 审批）→ 健康评分与巡检报告**

## 主项目：`ob-inspection/`

完整文档见 **[ob-inspection/README.md](ob-inspection/README.md)**（功能特性、系统架构、接口清单、安全说明）。

### 核心能力一览

- **巡检主链路**：8+3 类指标 JDBC 直连 OB 4.4 系统视图采集，14 条规则引擎（阈值热调整），告警全生命周期（同一事件只保留一条、恢复自动关闭）
- **多 Agent AI 诊断**：4 个专用 Agent（慢 SQL/容量/事务/兜底）确定性路由 + function calling 只读取证（SQL 防火墙）+ grounding 反幻觉校验 + per-agent 熔断降级
- **自治处置（Guarded Action）**：模型只能提议预定义动作（kill_session / major_freeze / restore_param_baseline），守卫链裁决（白名单→前置→限频熔断→审批门→dry-run→复测），L2 动作双审批入口（钉钉群 + 操作台）
- **两个前端**：赛博朋克 HUD 运维大屏（Vue3，:5173 纯展示）+ 运维操作台（:8080/admin.html，表单登录，两级角色 SYS_ADMIN/ADMIN）
- **平台能力**：多实例纳管、AES-256-GCM 凭据加密、钉钉通知（HmacSHA256 加签）、操作审计、263 个单元测试

### 快速开始

```bash
# 1. OceanBase（社区版 Docker）
docker start obce

# 2. 后端（必带加密密钥；钉钉/AI 走环境变量，缺省自动降级）
cd ob-inspection
export OB_ENCRYPT_KEY=zhongyuan-bank-ob-inspection-2026
JAVA_HOME=../tools/jdk-17.0.2 ../tools/apache-maven-3.9.9/bin/mvn -s ../tools/settings.xml spring-boot:run

# 3. 前端大屏
cd frontend && npm install && npm run dev   # :5173
```

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| 运维大屏 | http://localhost:5173 | 纯展示，无需登录 |
| 运维操作台 | http://localhost:8080/admin.html | 跳登录页；`admin`/`ob-admin-2026`（系统管理员）、`operator`/`ob-operator-2026`（普通管理员，**演示专用**） |
| Swagger UI | http://localhost:8080/swagger-ui.html | 接口文档 |

## 仓库结构

```
oceanbase-monitor/
├── ob-inspection/   # 主项目（后端 Spring Boot 3 + 前端 Vue3 + 全部文档）
├── src/, pom.xml    # 早期 DDD 骨架 Demo（历史保留，已被 ob-inspection 取代）
└── hello.txt        # git 连通性测试遗留
```

## 测试

```bash
cd ob-inspection
JAVA_HOME=../tools/jdk-17.0.2 ../tools/apache-maven-3.9.9/bin/mvn -s ../tools/settings.xml test   # 263 个单测
```
