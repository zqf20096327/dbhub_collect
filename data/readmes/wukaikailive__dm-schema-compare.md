# 达梦数据库结构对比工具

达梦数据库(DM Database)结构对比工具，用于比较两个数据库的表结构差异，并生成同步SQL脚本。

## 功能特性

- 支持连接达梦数据库进行结构对比
- 支持上传SQL文件解析表结构
- 对比表结构差异（新增表、删除表、修改表）
- 对比字段差异（新增字段、删除字段、修改字段类型等）
- 对比索引差异
- 生成结构同步SQL脚本
- Web界面可视化操作

## 技术栈

- **后端**: Node.js + Express
- **数据库驱动**: dmdb (达梦数据库官方驱动)
- **前端**: 原生 HTML/CSS/JavaScript

## 安装

```bash
# 安装依赖
npm install

# 启动服务
npm start

# 开发模式（支持热重载）
npm run dev
```

## 使用方法

1. 启动服务后访问 `http://localhost:3000`
2. 配置源数据库和目标数据库连接信息
3. 点击"开始对比"进行结构对比
4. 查看对比结果并生成同步SQL

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/connect` | POST | 测试数据库连接 |
| `/api/compare` | POST | 对比两个数据库结构 |
| `/api/parse-sql` | POST | 解析SQL文件提取表结构 |
| `/api/generate-sync` | POST | 生成同步SQL脚本 |
| `/health` | GET | 健康检查 |

## 项目结构

```
dm-schema-compare/
├── server.js           # 服务入口
├── routes/
│   └── api.js          # API路由
├── services/
│   ├── db.js           # 数据库连接服务
│   ├── schema.js       # 表结构获取服务
│   ├── compare.js      # 结构对比服务
│   └── sql-parser.js   # SQL解析服务
├── utils/
│   └── sql-generator.js # SQL生成工具
├── public/             # 前端静态文件
│   ├── index.html
│   ├── css/
│   └── js/
└── package.json
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PORT` | 服务端口 | 3000 |

## 许可证

MIT
