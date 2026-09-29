# PolarDB Supabase Skill

OpenClaw 的 PolarDB Supabase 数据库管理技能，基于 TypeScript + Supabase JS SDK + Commander 开发。

## 项目结构

```
polardb-supabase-skill/
├── skill/                    # 📦 部署产物（可直接复制到 OpenClaw）
│   ├── SKILL.md              # 技能描述文档
│   ├── .env.example          # 环境变量示例
│   ├── scripts/              # 构建后的零依赖 JS 脚本
│   └── references/           # Supabase AI Prompt 最佳实践文档
├── src/                      # 🔧 TypeScript 源码
│   ├── lib/
│   │   └── supabase-client.ts
│   └── scripts/
│       ├── database.ts
│       ├── storage.ts
│       ├── edge-functions.ts
│       ├── secrets.ts
│       ├── auth.ts
│       └── profile.ts
├── tests/                    # 🧪 集成测试
├── package.json
├── tsconfig.json
└── build.mjs                 # 构建脚本
```

## 开发

### 安装依赖

```bash
npm install
```

### 构建

```bash
npm run build          # 构建到 skill/scripts/
npm run build:watch    # 监听模式
```

### 测试

```bash
# 配置环境变量
cp skill/.env.example .env
# 编辑 .env 填入实际配置

# 运行所有测试
npm test

# 监听模式（开发时使用）
npm run test:watch
```

### 本地测试脚本

```bash
node skill/scripts/database.js --help
node skill/scripts/database.js list-tables

# 多环境支持
node skill/scripts/database.js list-tables --profile project-a
```

## 部署到 OpenClaw

```bash
cp -r skill/ ~/.openclaw/skills/polardb-supabase/
```

## 功能模块

| 脚本 | 功能 |
|------|------|
| `database.js` | SQL 查询、表结构查看 |
| `storage.js` | 存储桶管理、文件上传下载 |
| `edge-functions.js` | Edge Functions 部署管理 |
| `secrets.js` | Secrets 密钥管理 |
| `auth.js` | 用户管理、MFA、审计日志 |
| `profile.js` | 多环境配置管理 |

## 技术栈

- **开发**: TypeScript + Supabase JS SDK + Commander
- **构建**: esbuild (打包为零依赖 CJS)
- **运行**: Node.js 18+
