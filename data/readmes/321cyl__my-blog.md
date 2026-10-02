# 我的技术博客系统

一个基于 Vue3 + Node.js + MongoDB 的全栈个人技术博客系统。

## 技术栈

| 部分 | 技术 | 说明 |
|---|---|---|
| 前端 | Vue 3 + Vite | 快速构建，组件化开发 |
| 路由 | Vue Router | 单页应用路由 |
| 状态 | Composition API | Vue3 组合式 API |
| HTTP | Axios | 前端请求后端 API |
| Markdown | marked + highlight.js | 渲染文章、代码高亮 |
| 后端 | Node.js + Express | RESTful API |
| 数据库 | MongoDB + Mongoose | 文档型数据库 |
| 鉴权 | JWT + bcryptjs | 登录鉴权、密码加密 |
| 版本控制 | Git + Gitee | 代码托管 |

## 项目结构

\`\`\`
my-blog/
├── backend/                  # 后端
│   ├── models/
│   │   ├── Post.js          # 文章数据模型
│   │   └── User.js          # 用户数据模型
│   ├── server.js            # Express 主入口
│   ├── createAdmin.js       # 创建管理员脚本
│   └── .env                 # 环境变量
│
└── frontend/                # 前端
    └── src/
        ├── views/
        │   ├── Home.vue         # 首页文章列表
        │   ├── PostDetail.vue   # 文章详情
        │   ├── Login.vue        # 登录页
        │   └── Admin.vue        # 后台管理
        ├── router/
        │   └── index.js         # 路由配置
        └── utils/
            └── api.js           # API 请求封装
\`\`\`

## 核心功能

- ✅ 文章列表展示（分类、标签、日期）
- ✅ 文章详情页（Markdown 渲染 + 代码高亮）
- ✅ 后台登录（JWT 鉴权）
- ✅ 文章发布（需登录）
- ✅ 文章删除（需登录）
- ✅ 退出登录

## 本地运行

### 后端

\`\`\`bash
cd backend
npm install
# 创建管理员（首次运行）
node createAdmin.js
# 启动服务
node server.js
\`\`\`

### 前端

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

## 默认账号

- 用户名：`admin`
- 密码：`admin123`