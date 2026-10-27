# 一页 · 个人记录

一个前后端分离的个人记录项目：包含登录 / 注册、日记、账本与随笔四个模块，支持日记图片上传与账本月度收支统计。

## 项目结构

```
onePage/
├── pom.xml                           # 聚合 POM（IDEA 导入根目录即可识别 Maven 多模块）
│
├── backend/                          # 后端服务（Spring Boot）
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/onepage/
│       │   ├── OnePageApplication.java      启动入口
│       │   ├── controller/               【控制层】REST 接口
│       │   ├── service/                  【服务层】业务接口
│       │   ├── service/impl/             【服务层】业务实现
│       │   ├── mapper/                   【数据访问层】MyBatis-Plus Mapper
│       │   ├── po/                       持久化对象（PO，对应数据库表）
│       │   ├── dto/                      请求 / 响应对象
│       │   ├── config/                   登录拦截器、CORS / MVC 配置
│       │   ├── common/                   统一响应、业务异常、全局异常处理
│       │   └── util/                     密码摘要、Token、用户上下文
│       └── resources/
│           ├── application.yml           端口、数据源、MyBatis-Plus 配置
│           └── db/
│               ├── README.md             数据库说明（连接、初始化、配置）
│               ├── init-dm.sql           创建 ONEPAGE 模式
│               └── schema.sql            建表脚本
│
├── frontend/                         # 前端（Vue 3 + Vite）
│   ├── package.json                      依赖与脚本
│   ├── vite.config.js                    Vite 配置、/api 代理
│   ├── index.html                        Vite 入口
│   └── src/
│       ├── main.js                       应用入口
│       ├── App.vue                       根组件（全局 Toast）
│       ├── router/index.js               路由与登录守卫
│       ├── api/request.js                统一请求封装
│       ├── api/auth.js                   认证接口
│       ├── api/diary.js                  日记与上传接口
│       ├── api/bill.js                   账本接口
│       ├── api/essay.js                  随笔接口
│       ├── composables/useToast.js       Toast 单例
│       ├── views/LoginView.vue           登录 / 注册页
│       ├── views/HomeView.vue            个人空间
│       ├── views/DiaryView.vue           日记列表与编辑
│       ├── views/BillView.vue            账本统计与记账
│       ├── views/EssayView.vue           随笔列表与编辑
│       └── assets/styles/                基础、登录、主页、日记、账本、随笔样式
│
└── README.md
```

## 三层架构

```
Controller（控制层）
    ↓ 接收请求、参数校验、返回统一响应
Service（服务层，接口 + 实现）
    ↓ 业务规则：注册查重、密码校验、Token 签发
Mapper（数据访问层）
    ↓ MyBatis-Plus BaseMapper，访问达梦数据库
Database（ONEPAGE.sys_user 表）
```

| 层 | 代码位置 | 职责 |
|----|----------|------|
| 控制层 | `controller/AuthController` | 路由、`@Valid` 校验、响应封装 |
| 服务层 | `service/AuthService` + `service/impl/AuthServiceImpl` | 认证业务逻辑 |
| 数据访问层 | `mapper/UserMapper` | 继承 `BaseMapper<User>`，由框架生成 CRUD |

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | JDK 8、Spring Boot 2.7.17、Spring MVC、Bean Validation、Lombok |
| 持久层 | MyBatis-Plus 3.5.4 + 达梦 DM8（DmJdbcDriver18） |
| 认证 | PBKDF2WithHmacSHA256 密码摘要 + HMAC-SHA256 无状态 Token |
| 前端 | Vue 3.5 + Vue Router 4 + Vite 6 |

## 启动方式

### 1. 启动后端

```bash
cd backend
mvn spring-boot:run
```

服务默认监听 `http://localhost:8080`。

首次部署需先创建达梦 `ONEPAGE` 模式，数据库连接、初始化与配置详见
[`backend/src/main/resources/db/README.md`](backend/src/main/resources/db/README.md)。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 `http://localhost:5173`。

Vite 已配置 `/api` 代理到 `http://localhost:8080`，开发时无需额外处理跨域。

生产构建：

```bash
npm run build
```

产物输出到 `frontend/dist`。

### 常见问题

**端口被环境变量覆盖**

若系统存在 `SERVER__PORT` / `SERVER_PORT` 环境变量，会覆盖 `application.yml` 中的 `server.port`。可显式指定端口启动：

```bash
mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=8080
```

**IntelliJ IDEA 导入**

根目录已提供聚合 `pom.xml`。用 IDEA 打开项目根目录，等待 Maven 自动导入；若未自动触发，点击 Maven 面板的 **Reload All Maven Projects** 即可。

**Lombok 注解未生效**

项目使用 Lombok 的 `@Data` / `@Getter` 等注解生成 getter、setter。IDEA 需要安装 **Lombok** 插件，并开启注解处理：

`Settings → Build, Execution, Deployment → Compiler → Annotation Processors → 勾选 Enable annotation processing`

**端口不一致**

后端默认 `8080`，前端 Vite 默认 `5173`。若修改后端端口，请同步修改 `frontend/vite.config.js` 中 `/api` 代理的 `target`。

## 接口说明

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/api/auth/register` | 注册 | 否 |
| POST | `/api/auth/login` | 登录 | 否 |
| GET | `/api/auth/me` | 获取当前用户 | 是 |
| POST | `/api/auth/logout` | 退出登录 | 是 |
| GET | `/api/auth/check-username` | 校验用户名是否可用 | 否 |
| GET | `/api/diaries` | 日记列表 | 是 |
| GET | `/api/diaries/{id}` | 日记详情 | 是 |
| POST | `/api/diaries` | 新建日记 | 是 |
| PUT | `/api/diaries/{id}` | 更新日记 | 是 |
| DELETE | `/api/diaries/{id}` | 删除日记 | 是 |
| POST | `/api/upload/image` | 上传日记图片 | 是 |
| GET | `/api/bills` | 账单列表 | 是 |
| POST | `/api/bills` | 新建账单 | 是 |
| PUT | `/api/bills/{id}` | 更新账单 | 是 |
| DELETE | `/api/bills/{id}` | 删除账单 | 是 |
| GET | `/api/essays` | 随笔列表 | 是 |
| POST | `/api/essays` | 新建随笔 | 是 |
| PUT | `/api/essays/{id}` | 更新随笔 | 是 |
| DELETE | `/api/essays/{id}` | 删除随笔 | 是 |

### 请求示例

```bash
# 注册
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"heart01","password":"123456","nickname":"小鹿"}'

# 登录
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"heart01","password":"123456","remember":true}'

# 获取当前用户
curl http://localhost:8080/api/auth/me \
  -H "Authorization: Bearer <token>"
```

统一响应结构：

```json
{ "code": 0, "message": "success", "data": { } }
```

`code` 为 `0` 表示成功；非 `0` 时 `message` 为可直接展示的错误提示。
