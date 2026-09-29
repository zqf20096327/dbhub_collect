<p align="center">
  <img src="https://www.cloudflare.com/img/logo-web-badges/cf-logo-on-white-bg.svg" alt="Cloudflare Logo" width="400"/>
</p>

<h1 align="center">🚀 Cloudflare 免费服务完全指南</h1>

<p align="center">
  <strong>全面了解 Cloudflare 平台提供的所有免费服务、额度限制和最佳实践</strong>
</p>

<p align="center">
  <a href="#-服务概览">服务概览</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-文档目录">文档目录</a> •
  <a href="#-免费额度汇总">免费额度</a> •
  <a href="#-贡献指南">贡献</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Cloudflare"/>
  <img src="https://img.shields.io/badge/Workers-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Workers"/>
  <img src="https://img.shields.io/badge/Pages-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Pages"/>
  <img src="https://img.shields.io/badge/AI-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="AI"/>
</p>

## 📋 服务概览

Cloudflare 提供了丰富的免费服务，让开发者可以零成本构建和部署现代化应用。本仓库整理了所有免费服务的详细信息。

| 服务 | 描述 | 免费额度 |
|-----|------|---------|
| **Workers** | 无服务器边缘计算 | 10万请求/天 |
| **Pages** | 静态网站托管 | 500次构建/月 |
| **Workers AI** | AI 推理服务 | 10,000 Neurons/天 |
| **D1** | 无服务器 SQLite 数据库 | 500万行读取/天 |
| **KV** | 键值存储 | 10万次读取/天 |
| **R2** | 对象存储 | 10GB 存储 |
| **Queues** | 消息队列 | 100万条消息/月 |
| **Durable Objects** | 有状态边缘计算 | 包含在付费计划 |

## 🚀 快速开始

```bash
# 安装 Wrangler CLI
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 创建新项目
npm create cloudflare@latest my-app

# 本地开发
wrangler dev

# 部署
wrangler deploy
```

## 📚 文档目录

详细的服务文档请查看 `docs/` 目录：

| 文档 | 内容 |
|-----|------|
| [📦 Workers 指南](docs/workers.md) | 无服务器函数、路由、绑定 |
| [🌐 Pages 指南](docs/pages.md) | 静态网站部署、Functions |
| [🤖 Workers AI 指南](docs/workers-ai.md) | AI 模型、定价、使用示例 |
| [🗄️ D1 数据库指南](docs/d1.md) | SQLite 数据库、查询、限制 |
| [📝 KV 存储指南](docs/kv.md) | 键值存储、缓存策略 |
| [💾 R2 存储指南](docs/r2.md) | 对象存储、S3 兼容 API |
| [📨 Queues 指南](docs/queues.md) | 消息队列、异步处理 |
| [🔧 其他服务](docs/others.md) | Email、Images、Stream 等 |

## 💰 免费额度汇总

### 计算服务

| 服务 | 免费额度 | 超出费用 |
|-----|---------|---------|
| Workers 请求 | 100,000 次/天 | $0.30/百万请求 |
| Workers CPU | 10ms/请求 | 付费版最高5分钟 |
| Pages 构建 | 500 次/月 | Pro 计划无限制 |
| Pages Functions | 共享 Workers 配额 | - |

### AI 服务

| 服务 | 免费额度 | 超出费用 |
|-----|---------|---------|
| Workers AI | 10,000 Neurons/天 | $0.011/1,000 Neurons |
| AI Gateway | 无限制 | 免费 |

### 存储服务

| 服务 | 免费额度 | 超出费用 |
|-----|---------|---------|
| D1 读取 | 500万 行/天 | $0.001/百万行 |
| D1 写入 | 10万 行/天 | $1.00/百万行 |
| D1 存储 | 5 GB | $0.75/GB-月 |
| KV 读取 | 100,000 次/天 | $0.50/百万次 |
| KV 写入 | 1,000 次/天 | $5.00/百万次 |
| KV 存储 | 1 GB | $0.50/GB-月 |
| R2 存储 | 10 GB | $0.015/GB-月 |
| R2 A类操作 | 100万 次/月 | $4.50/百万次 |
| R2 B类操作 | 1000万 次/月 | $0.36/百万次 |

### 其他服务

| 服务 | 免费额度 |
|-----|---------|
| Queues | 100万 条消息/月 |
| Email Routing | 无限制 |
| DNS | 无限制 |
| CDN | 无限制带宽 |
| SSL/TLS | 免费通配符证书 |
| DDoS 防护 | 无限制 |

## 🛠️ 技术栈

- **运行时**: V8 Isolates
- **语言**: JavaScript, TypeScript, Rust, Python, Go (WASM)
- **框架**: Hono, Remix, Next.js, Astro, SvelteKit
- **存储**: D1 (SQLite), KV, R2, Durable Objects

## 📖 学习资源

- [Cloudflare Workers 官方文档](https://developers.cloudflare.com/workers/)
- [Cloudflare Pages 官方文档](https://developers.cloudflare.com/pages/)
- [Workers AI 官方文档](https://developers.cloudflare.com/workers-ai/)
- [D1 官方文档](https://developers.cloudflare.com/d1/)
- [Cloudflare 开发者 Discord](https://discord.cloudflare.com)

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## ⭐ Star History

如果这个项目对你有帮助，请给一个 Star ⭐

<p align="center">
  <sub>Made with ❤️ by <a href="https://github.com/chuankangkk">传康KK</a></sub>
</p>
