# loop_bigdata_demo

大数据平台 ETL 接入模块 Demo

## 技术栈

| 层 | 技术 |
|---|---|
| 数据库 | TiDB (MySQL compatible) |
| 后端 | Spring Boot 3 + MyBatis-Plus |
| 前端 | Vue 3 + TypeScript + Ant Design Vue |
| 部署 | Docker Compose |

## 项目结构

```
loop_bigdata_demo/
├── backend/          # Spring Boot ETL服务
├── frontend/         # Vue 3 管理界面
├── docs/             # 接口文档与设计文档
└── docker-compose.yml
```

## 核心功能

1. 数据源管理（MySQL/PG/Oracle/SQL Server → TiDB）
2. ETL任务配置（全量/增量同步，字段映射）
3. 任务调度执行（手动/Cron）
4. 运行监控与日志查看
5. 管理端登录入口与会话鉴权
6. API 网关、数据治理演示页面

## API 文档

启动后访问：`http://localhost:8080/swagger-ui.html`

## 登录与前端鉴权

管理端默认访问 `/dashboard`，未登录时会跳转到 `/login`。

- 默认用户：`admin`
- 默认密码：`admin`
- 会话策略：登录状态保存在当前浏览器标签页的 `sessionStorage` 中，刷新页面不需要重新登录；关闭标签页或点击退出后需要重新登录。
- 业务接口认证：登录成功后前端会在当前会话中写入 demo API Key，并由 Axios 自动注入 `X-API-Key`。
- 网关密钥管理：访问 `/api/gateway/keys` 时前端会自动注入 `X-Admin-Key`。

更多说明见 [docs/login-auth.md](docs/login-auth.md)。
