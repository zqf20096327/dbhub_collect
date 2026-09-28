# GitHub 仓库 AI 文档翻译平台

> 作者：[程序员鱼皮](https://yuyuanweb.feishu.cn/wiki/Abldw5WkjidySxkKxU2cQdAtnah)
>
> 本项目为教学项目，提供完整视频教程 + 文字教程 + 简历写法 + 面试题解 + 答疑服务，帮你提升项目能力，给简历增加亮点！
>
> ⭐️ 加入项目系列学习：[加入编程导航](https://www.codefather.cn/vip)



## 一、项目介绍

这是一套以 **AI 编程实战** 为核心的项目教程，基于 Next.js + GitHub App + OpenRouter，用 AI 编程的方式从 0 到 1 开发一个《GitHub 仓库 AI 文档翻译 SaaS 平台》，带你亲身体验 AI Vibe Coding 的完整工作流，学会用 AI 做出真正能用、能部署、能赚钱的产品！

📺 项目介绍视频，快速查看成品效果：https://bilibili.com/video/BV1mAAmzqEfP

![](https://pic.yupi.icu/1/1769079083162-aa879560-6044-4ef7-a3a2-718b03070978-20260225143424199.png)

输入任意一个 GitHub 仓库地址，AI 自动将文档翻译成多种语言，并在基准语言内容发生变更时，**自动增量同步翻译**，生成 PR 等待仓库负责人合并，全程无需人工干预。



### 为什么做这个项目？

鱼皮开源了一套 AI 编程教程仓库 [ai-guide](https://github.com/liyupi/ai-guide)，包含了上百个中文教程文档。为了让海外用户也能看到，希望把仓库翻译成多语言版本，但人工翻译成本太高，GitHub Actions 又要自己折腾配置……

既然如此，**不如做一个更通用的工具**。

这就是 GitHub Global 项目的起点：输入任意一个 GitHub 仓库地址，AI 自动将文档翻译成多种语言，并在基准语言内容发生变更时，**自动增量同步翻译**，生成 PR 等待仓库负责人合并，全程无需人工干预。

零配置，一键翻译，让你的 GitHub 项目走向全球！

![](https://pic.yupi.icu/1/GitHub%2520Global%2520%25E4%25B8%25BB%25E9%25A1%25B5.png)



### 6 大核心能力

1）用 GitHub 账号一键登录，基于 GitHub App 实现安全登录与授权。

![](https://pic.yupi.icu/1/image-20260225142930323.png)



2）导入 GitHub 仓库，输入地址即可自动拉取仓库信息。

![](https://pic.yupi.icu/1/1769079897565-92698844-bfcc-4f6d-b226-d18352ea2244-20260225144921746-20260225144924730.png)



3）配置翻译，可视化选择翻译范围和目标语言（支持 20 种主流语言）。

![](https://pic.yupi.icu/1/1769079897565-92698844-bfcc-4f6d-b226-d18352ea2244-20260225144921746-20260225144924730.png)



4）一键执行翻译，实时展示进度，翻译完成后自动创建 PR。

![](https://pic.yupi.icu/1/1769079926879-90640105-2d23-418c-b4b5-e962eab31299-20260225144931498.png)

![](https://pic.yupi.icu/1/1769080074375-806fa172-c440-47e3-93fd-07ad33c271ea-20260225144935674.png)

仓库负责人可以自己选择是否合并本次翻译，既方便又安全：

![](https://pic.yupi.icu/1/1769080059408-f3e3d44f-df55-4872-8bdc-c781b71cfc81.png)



5）自动触发增量翻译，开启后每次 Push 都会自动翻译变更的文档。

![](https://pic.yupi.icu/1/1770201178863-f4e450bd-b92f-4f56-9b43-82aed36a73b0-20260225142203617.png)

![](https://pic.yupi.icu/1/1770201323050-d991c61a-2ffa-40c1-b1c8-4334ff05c248-20260225141729741.png)



6）自定义大模型和 API Key，支持 GPT、Claude、Gemini、DeepSeek 等主流模型。

![](https://pic.yupi.icu/1/1770194573295-9e7552ca-b0c1-4612-a590-6060b5717d79-20260225144945946.png)



## 二、项目优势

本项目选题新颖，紧跟 AI 编程时代，以 **真实 SaaS 产品开发** 为导向，区别于增删改查的烂大街项目。项目内容精炼，**不到一周就能学完**，带你掌握 AI 编程的完整工作流，给你的简历和求职大幅增加竞争力！

技术丰富，覆盖 AI 编程全链路：

![](https://pic.yupi.icu/1/image-20260225140224582.png)

从这个项目中你可以学到：

- 如何用 AI 进行需求调研，生成专业的《需求规格文档》？
- 如何用多 AI 并行的方式，同时开发前端和后端？
- 如何与 GitHub App 对接，实现安全的 OAuth 授权和仓库操作？
- 如何接入 OpenRouter，统一对接数百种 AI 大模型？
- 如何使用 GitHub API 获取仓库文件树、提交文件、创建 PR？
- 如何通过 GitHub Webhook 实现事件驱动的自动化翻译？
- 如何使用内网穿透工具，在本地调试 Webhook 回调？
- 如何用 Vercel 部署 Next.js 全栈项目，快速上线？
- 如何在 AI 开发流程中进行代码审查、版本控制和问题修复？
- 如何识别竞品差异化机会，设计真正有竞争力的产品？




### 鱼皮系列项目优势

鱼皮的原创项目以 **实战** 为主，用 **全程直播** 的方式 **从 0 到 1** 带做，从需求分析、技术选型、项目设计、项目初始化、Demo 编写、前后端开发实现、项目优化、部署上线等，每个环节我都 **从理论到实践** 给大家讲的明明白白、每个细节都不放过！

比起看网上的教程学习，鱼皮项目系列的优势：从学知识 => 实践项目 => 复习笔记 => 项目答疑 => 简历写法 => 面试题解的一条龙服务

![](https://pic.yupi.icu/1/image-20260225142355401.png)

编程导航已有 **20+ 套项目教程！** 每个项目的学习重点不同，几乎全都是前端 + 后端的 **全栈项目**，也有大量 AI 应用开发项目。

详细请见：[https://codefather.cn/course](https://www.codefather.cn/course)（在该页面右侧有教程推荐和学习建议）

往期项目介绍视频：[https://bilibili.com/video/BV1YvmbYbEgS](https://www.bilibili.com/video/BV1YvmbYbEgS/)

鱼皮的项目帮很多同学拿到了大厂高薪 Offer：

![](https://pic.yupi.icu/1/%E7%BC%96%E7%A8%8B%E5%AF%BC%E8%88%AA2026%20offer%E6%8A%A5%E5%96%9C.png)



## 三、更多介绍

功能模块：

![](https://pic.yupi.icu/1/image-20260225140201706.png)

架构设计：

![](https://pic.yupi.icu/1/image-20260225141302579.png)



## 四、快速运行

> 详细的保姆级教程请参考 [本地运行指南](./docs/本地运行指南.md)

### 前置条件

- Node.js >= 20
- MySQL >= 8.0
- 一个 [GitHub App](https://github.com/settings/apps/new)（用于登录和仓库操作）
- 一个 [OpenRouter API Key](https://openrouter.ai/keys)（用于 AI 翻译）

### 1. 克隆并安装依赖

```bash
git clone https://github.com/liyupi/github-global.git
cd github-global
npm install
```

### 2. 配置环境变量

```bash
# 创建环境变量文件（两个文件内容保持一致）
cp .env.example .env
cp .env.example .env.local
```

编辑 `.env` 和 `.env.local`，填入你的配置：

```bash
DATABASE_URL=mysql://root:你的密码@localhost:3306/github_global
NEXTAUTH_URL=http://localhost:3123
AUTH_SECRET=随机字符串至少32位
GITHUB_APP_ID=你的AppID
GITHUB_APP_CLIENT_ID=你的ClientID
GITHUB_APP_CLIENT_SECRET=你的ClientSecret
GITHUB_APP_PRIVATE_KEY_PATH=./private-key.pem
PLATFORM_OPENROUTER_API_KEY=sk-or-v1-你的key
```

将 GitHub App 的私钥文件保存为项目根目录下的 `private-key.pem`。

### 3. 初始化数据库并启动

```bash
# 创建数据库（MySQL 命令行）
mysql -u root -p -e "CREATE DATABASE github_global CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 生成 Prisma 客户端 + 建表
npx prisma generate
npx prisma db push

# 启动开发服务器
npm run dev
```

访问 **http://localhost:3123** 即可使用。

### Docker 部署

```bash
docker-compose up -d
docker-compose exec app npx prisma db push
```

更多细节请查看 [本地运行指南](./docs/本地运行指南.md) 和 [人工配置文档](./docs/人工配置文档.md)。



## 加入项目学习

编程导航已有 **20+ 套项目教程**！每个项目的学习重点不同，几乎全都是前端 + 后端的 **全栈** 项目，也有大量 AI 应用开发项目。

![](https://pic.yupi.icu/1/%25E9%25A1%25B9%25E7%259B%25AE%25E6%2595%2599%25E7%25A8%258B.png)

欢迎加入 [编程导航](https://www.codefather.cn/vip)，加入后不仅可以全程跟学本项目，往期 **20+ 套原创项目教程** 也都可以无限回看。还能享受更多原创技术资料、学习和求职指导、上百场面试回放视频，开启你的编程起飞之旅~

🧧 助力新项目学习，给大家发放 **限时编程导航优惠券**，扫码即可领券加入。加入三天内不满意可全额退款，欢迎加入体验，名额有限，速来学习！

<img width="404" alt="image" src="https://github.com/user-attachments/assets/56411098-b60e-4267-8ba2-4ebc5d416afc" />

1 天不到 1 块钱，绝对是对自己最值的投资！成为编程导航会员后，可以解锁 20 多套项目的教程和资料，PC 网站和 APP 都可以学习，如图：

![](https://pic.yupi.icu/1/image-20250120113756426-20250422160856746.png)
