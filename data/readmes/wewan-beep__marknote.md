# MarkNote

**Markdown 笔记系统：左边写 Markdown，右边出公众号排版，写完一键复制，粘到公众号后台不掉格式。**

> **📖 项目介绍主页：https://wewan-beep.github.io/marknote/**
---
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)[![JDK](https://img.shields.io/badge/JDK-17-orange.svg)](https://adoptium.net/)[![Vue](https://img.shields.io/badge/Vue-3.x-42b883.svg)](https://vuejs.org/)[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2-brightgreen.svg)](https://spring.io/projects/spring-boot)[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)[![MinIO](https://img.shields.io/badge/MinIO-S3%20API-C7202C.svg)](https://min.io/)

前后端分离的完整工程，不是 demo：Vue3 + Vite + Element Plus 前端，Spring Boot 3 + MyBatis-Plus + MySQL 8 + MinIO 后端，JWT 鉴权，`docker compose` 一键起依赖，Windows 有双击启动脚本。

---
## 请关注公众号，有更多精彩内容分享
![公众号](docs/images/gzh_ewm.jpg)


## 界面预览

![工作台](docs/images/02-workspace.png)

左栏笔记列表，中间 Markdown 源码，右侧公众号预览——三段式布局，写和排版同时进行。

---

## 为什么不用现成的

| 对比项 | mdnice（在线） | Typora（本地） | MarkNote（本项目） |
| --- | --- | --- | --- |
| 数据在哪 | 别人的服务器 | 本地 md 文件 | 自己的 MySQL，可备份可迁移 |
| 账号体系 | 无 / 第三方登录 | 无 | 自建 user 表 + JWT |
| 导入已有 md | 每次粘贴 | 打开文件 | 顶栏多选导入、拖进列表 |
| 图片托管 | 平台图床，可能限流 | 本地相对路径，公众号粘贴易失效 | 自建 MinIO，可降级到本地磁盘 |
| 主题 | 平台内置，不能改代码 | 主题包 | 10 套，改一份 css 就能加 |
| 排版可控性 | 黑盒 | 需手动调 | 内联样式可见、可改（`Editor.vue` 里 `buildWechatHtml`） |

---

## 功能特性

| 模块 | 能力 | 细节 |
| --- | --- | --- |
| 账号 | 登录 / 注册 | JWT 签发，密码 bcrypt；401 自动跳登录页 |
| 笔记管理 | 新建、改名、搜索、回收站、恢复、彻底删除 | 三个改标题入口：顶栏输入 / 列表悬停 ✏️ / 标题双击 |
| 写作 | 左写右预览、同步滚动开关、代码高亮、KaTeX、字数行数统计 | markdown-it + highlight.js + katex |
| 自动保存 | 内容停笔 1.2s 落库，标题 0.9s 防抖，回车立即保存 | 切笔记、切标签、导入前先 flush |
| 导入 Markdown | 顶栏「导入 MD」多选，或文件直接拖进左侧列表 | 标题取首个 `# 一级标题`，否则取文件名（截 80 字）；单文件 ≤ 5MB |
| 图片上传 | 工具栏选图、拖进编辑区、粘贴截图、外链地址 | ≤ 10MB，白名单 png/jpg/jpeg/gif/webp/bmp/svg，多图按光标顺序插入 |
| 排版主题 | 10 套公众号主题一键切换，预览与复制同源 | 蓝调 / 青野 / 暖橙 / 紫罗兰 / 墨印 / 极简 / 科技 / 暖纸 / 夜色 / 糖果 |
| 公众号输出 | 「复制公众号 HTML」写入**富文本**剪贴板 | 计算样式全量内联、去 class、`<pre>`→`<section>`、KaTeX 降级 |
| 历史版本 | 每次保存写快照（`note_history`），可预览并回滚 | 默认保留最近 50 条 |
| 其他 | 导出 `.md`、编辑器暗色模式、统一返回体、全局异常处理 | 暗色只作用于 UI，不影响文章主题 |

---

## 界面截图

| 登录 | 导入 Markdown |
| --- | --- |
| ![登录](docs/images/01-login.png) | ![导入](docs/images/03-import.png) |

| 图片上传 | 主题切换 |
| --- | --- |
| ![图片上传](docs/images/04-image.png) | ![主题](docs/images/05-theme.png) |

**复制到公众号**：左侧是编辑器，右侧是公众号后台粘贴后的效果对照。

![复制](docs/images/06-copy.png)

---

## 技术栈

| 层 | 选型 | 备注 |
| --- | --- | --- |
| 前端 | Vue 3 + Vite 5 + Element Plus | 组合式 API，单文件组件，`npm run dev` 热更新 |
| 后端 | Spring Boot 3.2（JDK 17） | 内嵌 Tomcat，统一 `Result<T>` 返回 |
| ORM | MyBatis-Plus 3.5.5 | 表结构由 `sql/init.sql` 建，实体用注解映射 |
| 数据库 | MySQL 8 | 库名 `marknote`，4 张表 |
| 对象存储 | MinIO 8.5.7（S3 协议） | 首次上传自动建桶并设公开读 |
| 鉴权 | jjwt 0.11.5 | `JwtInterceptor` 拦 `/api/**`，放行 `login/register/files` |
| 图片兜底 | 本地磁盘 `uploads/` | MinIO 挂了自动落盘，`/files/**` 静态映射 |

**请求链路**

```
浏览器(3000) → Vite proxy /api → Spring Boot(8080) → MySQL
                                    ├─ MinIO(9000) 图片
                                    └─ uploads/    图片兜底
```

---

## 快速开始

### 环境要求

| 依赖 | 版本 |
| --- | --- |
| JDK | 17+ |
| Maven | 3.8+ |
| Node.js | 18+ |
| Docker（可选） | 任意（非 Docker 需自备 MySQL 8 + MinIO） |

### 1. 起依赖

```bash
cd marknote
docker compose up -d
```

- MySQL：`localhost:3306`，库 `marknote`，首次启动自动执行 `sql/init.sql`
- MinIO：API `9000`，控制台 `9001`（minioadmin / minioadmin）

不用 Docker 就自己装 MySQL 8 与 MinIO，然后手工执行 `sql/init.sql`。

### 2. 起后端

```bash
cd marknote-server
mvn spring-boot:run
```

Windows 也可以直接双击根目录 `start-backend.bat`。

启动前按需修改 `src/main/resources/application.yml`：

| 配置 | 默认值 | 说明 |
| --- | --- | --- |
| `spring.datasource.url` | `jdbc:mysql://localhost:3306/marknote` | 数据库地址 |
| `spring.datasource.username/password` | root / root | MySQL 账号密码 |
| `minio.endpoint` | `http://127.0.0.1:9000` | MinIO 服务地址 |
| `minio.access-key/secret-key` | minioadmin / minioadmin | MinIO 密钥 |
| `minio.bucket-name` | marknote | 首次上传自动建桶并设公开读 |
| `app.upload-dir` | `./uploads` | MinIO 不可用时的本地目录 |
| `app.file-base-url` | `http://localhost:8080` | 本地图片对外访问前缀 |
| `jwt.secret` | 内置长串 | 生产环境务必换掉 |

### 3. 起前端

```bash
cd marknote-web
npm install
npm run dev
```

打开 <http://localhost:3000>，演示账号 **admin / 123456**（`sql/init.sql` 已置入）。

> 微信/公众号相关功能请用 `localhost` 或 `https` 访问，`http://192.168.x.x` 下浏览器会禁用剪贴板 API。

---

## 目录结构

```
marknote/
├── sql/init.sql                    # 建库建表 + 演示账号 + 示例笔记
├── docker-compose.yml              # MySQL 8 + MinIO 一键起
├── start-backend.bat               # Windows 后端启动脚本
├── start-frontend.bat              # Windows 前端启动脚本
├── docs/                           # 图文手册与界面图
│   ├── 功能介绍与操作指南.md
│   └── images/
├── marknote-server/                # Spring Boot 3 后端（8080）
│   └── src/main/
│       ├── java/com/marknote/
│       │   ├── controller/         # User / Note / NoteHistory / Image
│       │   ├── service/            # 业务层（保存时写历史快照）
│       │   ├── mapper/             # MyBatis-Plus Mapper
│       │   ├── entity/ dto/        # 表实体与出入参
│       │   ├── config/             # CORS / JWT 拦截器 / 静态资源映射
│       │   └── util/               # JwtUtil、统一返回
│       └── resources/application.yml
└── marknote-web/                   # Vue3 前端（3000，/api 代理 8080）
    └── src/
        ├── views/                  # Login.vue、Editor.vue（主工作台）
        ├── components/             # MarkEditor.vue（编辑 + 预览 + 上传）
        ├── api/                    # note / user / image
        ├── theme/themes.js         # 10 套主题清单
        ├── styles/                 # editor.css、themes.css
        └── utils/request.js        # axios 封装，401 跳登录
```

---

## 数据模型

库 `marknote`，4 张表：

| 表 | 作用 | 关键字段 |
| --- | --- | --- |
| `user` | 账号 | `username`、`password`（bcrypt/明文兼容）、`nickname` |
| `note` | 笔记正文 | `title`、`content`、`version`、`is_deleted`、`update_time` |
| `note_history` | 保存快照 | `note_id`、`content`、`version`、`create_time` |
| `image` | 上传记录 | `file_name`、`url`、`size`、`user_id` |

保存链路：`updateNoteWithHistory` 先写一条 `note_history` 快照，再 `version + 1` 更新正文，避免并发保存互相覆盖。

---

## 接口一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/user/login` | 登录，返回 token |
| POST | `/user/register` | 注册（bcrypt） |
| GET | `/user/info` | 当前用户 |
| GET | `/note/list?isDeleted=0&keyword=` | 笔记列表 / 回收站 |
| POST | `/note/add` | 新建 |
| POST | `/note/update` | 保存（写快照、version+1） |
| POST | `/note/del` | 移入回收站 |
| POST | `/note/restore` | 从回收站恢复 |
| POST | `/note/remove` | 彻底删除 |
| GET | `/note/get?id=` | 笔记详情 |
| GET | `/noteHistory/list?noteId=` | 历史版本（最近 50 条） |
| POST | `/image/upload` | 上传图片（MinIO 优先，本地兜底） |

除 `login` / `register` 外，均需请求头 `Authorization: <token>`。

---

## 「复制到公众号」是怎么做到的

公众号编辑器会过滤 `class`、`<style>`、`<pre>`，只认元素上的内联样式。所以复制流程不是「把 HTML 字符串塞进剪贴板」，而是：

1. 克隆预览节点到屏幕外容器（`position:fixed; left:-9999px; width:760px`），保证样式计算与预览一致；
2. 对每个节点 `getComputedStyle`，拼成 `style` 属性（颜色、背景、字号、字重、行高、字距、对齐、内外边距、边框、圆角、列表符号、图片 `max-width`、表格 `border-collapse`）；
3. `pre` 转 `section`（公众号不支持 `pre`），换行替换为 `<br>`，高亮 token 的颜色单独保留；
4. KaTeX 节点降级成等宽 TeX 文本，并统计数量给出提示；
5. 两趟处理：先采集全部待处理节点，再统一删 `class`、写 `style`，否则边删边采集会让 `.markdown-body h1` 这类后代选择器失效；
6. 用 `ClipboardItem({'text/html', 'text/plain'})` 写剪贴板，失败时回落到隐藏容器 + `execCommand('copy')`。

主题的底色、内边距、圆角也从预览根节点读取，所以「暖纸」「夜色」这类整页底色的主题能一起带进公众号。

---

## 常见问题

**1. 登录后接口 401** — token 过期（默认 24h）或请求未带 `Authorization`，重新登录。

**2. 图片不显示** — 看 URL 是 MinIO 还是 `/files/`：前者确认桶 `marknote` 已建且公开读、`minio.endpoint` 可达；后者确认 `app.file-base-url` 与浏览器访问的后端地址一致。

**3. 复制到公众号没排版** — 大概率是用了 `http://` 局域网 IP 打开页面（剪贴板 API 被禁用），换 `localhost`；粘贴时用 Ctrl+V，别用「粘贴为纯文本」。

**4. 公式粘过去变一串 TeX** — 公众号不支持 KaTeX，这是平台限制。公式建议截图当图片插入。

**5. 后端启动报连不上数据库** — `application.yml` 数据源与实际 MySQL 地址不一致；Docker 版默认 `localhost:3306`。

**6. 历史表涨得快** — `note_history` 每次保存写一条，生产环境按 `note_id` 只保留最近 N 条或按时间归档（`NoteServiceImpl` 里加清理即可）。

---

## 生产部署

```bash
# 后端
cd marknote-server && mvn clean package
java -jar target/marknote-server-1.0.0.jar

# 前端
cd marknote-web && npm run build      # 产物在 dist/
```

- `dist/` 交给 Nginx，`/api` 反向代理到 `8080`，`/files/` 直连后端静态映射
- MySQL、MinIO 不要暴露公网端口；`jwt.secret` 换成随机长串
- 备份：MySQL 定时 `mysqldump` + MinIO 数据目录挂到独立磁盘

---

## Roadmap

- [ ] 一键 Docker 部署（前后端也进 compose）
- [ ] Markdown 目录（TOC）生成与锚点
- [ ] 主题自定义编辑器（可视化调色，导出 css）
- [ ] 团队协作：共享笔记本、评论
- [ ] 移动端适配（H5 阅读 + 轻编辑）
- [ ] 导出 PDF / 图片长图

---

## 参与贡献

1. Fork 本仓库
2. 新建分支 `feature/xxx`
3. 提交改动（前端请先 `npm run build` 验证通过）
4. 提 PR，说明改动点与影响范围

新增一套排版主题只需两处：`marknote-web/src/styles/themes.css` 加一组 CSS 变量，`src/theme/themes.js` 加一条主题描述。

---
界面截图见 [`docs/images/`](docs/images/)，图文操作手册见 [`docs/功能介绍与操作指南.md`](docs/功能介绍与操作指南.md)。

## 请作者喝杯奶茶吧！
<img width="300" src='docs/images/pay-wx.jpg'>  <img width="300" src='docs/images/pay-zfb.jpg'>

## 更多开源项目分享请关注：夜入烟雨（微信公众号）
---
<img width="500" src='docs/images/gzh_ss.png'> 

--- 

## 开源协议

[MIT](LICENSE) © MarkNote
