# 鱼皮 API 开放平台（yuapi-backend-public）

<p align="center">
  基于 Java Spring Boot + Spring Cloud Gateway + Apache Dubbo + Nacos + Spring Boot Starter SDK 打造的分布式 API 开放平台后端开源项目
</p>

<p align="center">
  <a href="http://dogyupi.com/">作者：程序员鱼皮</a> ·
  <a href="https://www.codefather.cn/course/1790979723916521474">完整实战课程</a> ·
  <a href="https://yuyuanweb.feishu.cn/wiki/VC1qwmX9diCBK3kidyec74vFnde">加入编程导航</a> ·
  <a href="https://www.codefather.cn">编程导航官网</a>
</p>

<p align="center">
  <a href="#-项目简介">项目简介</a> ·
  <a href="#-界面与功能展示">功能展示</a> ·
  <a href="#-为什么选择开放平台架构实战">核心优势</a> ·
  <a href="#-源码目录与技术选型">源码与技术栈</a> ·
  <a href="#-项目收获与学员成果">项目收获</a> ·
  <a href="#-完整项目大纲">项目大纲</a> ·
  <a href="#-常见问题-faq">常见问题 FAQ</a> ·
  <a href="#-项目资料与生态资源">学习资源</a>
</p>

---

## ✨ 项目简介

`yuapi-backend-public` 是由 [程序员鱼皮](http://dogyupi.com/) 在 [编程导航](https://yuyuanweb.feishu.cn/wiki/VC1qwmX9diCBK3kidyec74vFnde) 推出的原创分布式全栈实战项目（本仓库开源核心后端及微服务子模块源码）。它围绕大厂高频建设与运营的「API 开放平台」业务场景展开，搭建了一个对外提供标准化接口供开发者调用的企业级平台。

在平台上，管理员可以接入、发布或下线各类接口，并实时统计分析全站接口调用情况；开发者注册登录后能够开通接口调用权限、浏览接口详情并进行在线调试，还可以直接引入项目自研的客户端 SDK，仅需一行代码就能在自己的业务系统中完成带 API 签名认证的安全调用。项目整体更侧重后端分布式架构与多系统协作，全程采用直播方式带大家走完需求分析、技术选型、系统设计、前后端协作开发到上线部署的全过程，熟练掌握这套高效开发工作流后，几分钟即可优雅落地一个新功能。

![加入编程导航解锁鱼皮 API 开放平台完整实战教程与资料](./doc/加入编程导航.jpeg)

---

## 💻 界面与功能展示

虽然项目重点在于后端网关、SDK 与分布式 RPC 架构，但同样配套了简洁高效的前端门户与管理后台，完整闭环从接口上架、在线调试到 SDK 集成的全部流程。

主页以清晰的卡片列表展示平台已发布的各类开放接口，方便开发者快速浏览与检索所需能力。

![鱼皮 API 开放平台主页与开放接口浏览列表](./doc/images/img-01.png)

接口管理页面依托 Ant Design 高级组件构建，支持管理员一站式新增、编辑、发布、下线接口以及查看调用统计图表。

![鱼皮 API 开放平台后台接口管理页面](./doc/images/img-02.png)

在线调试页面允许开发者直接在浏览器中填写请求参数并实时验证返回结果，大幅降低接入前期的试错成本。

![鱼皮 API 开放平台开发者在线接口调试页面](./doc/images/img-03.png)

开发者在本地项目中引入自研的 `yuapi-client-sdk` 并配置密钥后，只需一行简洁代码即可自动完成签名组装与远程接口调用。

![使用自研 Spring Boot Starter 客户端 SDK 一行代码调用 API 接口](./doc/images/img-04.png)

---

## 🎯 为什么选择开放平台架构实战

很多开发者在校期间或初入职场时接触的大多是单体管理系统和商城项目，面试时很难拉开区分度。API 开放平台通常是中大型互联网企业才会建设的核心基础设施，不仅市面上系统性的教程与深度文章极度稀缺，而且天然涵盖了多子系统协作的经典分布式难题。

![市面上开放平台实战教程稀缺的检索现状对比](./doc/images/img-05.png)

本项目打破了单一后端服务的局限，通过平台主后端、模拟接口服务、微服务 API 网关、公共契约模块与客户端 SDK 之间的协同联动，带你透彻掌握 API 签名认证、微服务网关统一鉴权与计费、Dubbo RPC 远程调用以及分布式服务治理等大厂必考能力。

![鱼皮 API 开放平台多子系统分布式架构协作示意图](./doc/images/img-06.png)

### 本项目适合哪些同学

本项目更偏重后端系统与架构设计。如果你已经掌握 Java Web 与 Spring Boot 基础，希望做出一个跳出传统增删改查、能在简历上显著加分的分布式实战项目，这套开放平台架构非常适合你。如果你是具备 Vue 或 React 基础的前端同学，同样可以通过配套前端部分掌握企业级脚手架与 OpenAPI 自动代码生成的高效研发技巧。

---

## 🧩 源码目录与技术选型

### 仓库核心模块划分

| 模块目录 | 模块职责与说明 |
| --- | --- |
| `src` | 平台主后端服务，负责用户管理、接口元信息管理、在线调试、权限开通与调用统计分析 |
| `yuapi-interface` | 模拟对外提供真实业务能力的独立 API 接口服务项目 |
| `yuapi-client-sdk` | 基于 Spring Boot Starter 封装的开发者客户端 SDK，内置 API 签名生成与自动装配能力 |
| `yuapi-gateway` | 基于 Spring Cloud Gateway 实现的统一微服务 API 网关，负责请求染色、签名校验、黑白名单与调用次数统计 |
| `yuapi-common` | 公共抽象模块，存放跨服务共享的实体类与 Dubbo RPC 服务接口定义 |
| `sql` | 项目核心数据库建表与初始化脚本 |

### 全栈技术选型一览

| 技术分层 | 核心技术与框架 | 主要应用场景 |
| --- | --- | --- |
| 后端核心与持久层 | Java Spring Boot、MySQL、MyBatis-Plus、MyBatis X | 快速搭建标准后端服务并自动生成数据访问层代码 |
| 网关与分布式通信 | Spring Cloud Gateway、Apache Dubbo、Nacos | 实现微服务统一入口拦截、统一鉴权、调用计数与跨服务 RPC 通信 |
| SDK 与安全认证 | Spring Boot Starter、自定义 API 签名认证（AccessKey / SecretKey + 随机数 + 时间戳） | 保障开放接口调用安全防重放，让开发者一行代码即可集成调用 |
| 接口文档与工具库 | Swagger + Knife4j、Hutool、Apache Commons Utils、Gson | 自动生成可交互的后端接口文档并精简通用工具编码 |
| 配套前端技术栈 | React 18、Ant Design Pro 5.x、Ant Design & ProComponents、Umi 4、OpenAPI 代码生成 | 快速生成前后端联调代码，高效构建接口门户与管理后台 |

---

## 🏆 项目收获与学员成果

跟随本项目从零走完需求、设计、编码、联调与分布式改造后，你可以获得以下扎实的工程沉淀：

1. 完整经历从零立项到上线的全流程直播实战，建立独立开发与部署企业级项目的全局视角。
2. 熟练使用主流前后端工程化脚手架与 OpenAPI 代码自动生成工具，成倍提升前后端协作效率。
3. 跳出常规单体 CRUD 管理系统，扎实掌握企业级开放平台的分模块解耦与多系统交互设计。
4. 透彻理解并亲手落地 API 签名认证防重放、Spring Boot Starter 客户端 SDK、Spring Cloud Gateway 全局过滤器与 Dubbo 分布式 RPC 调用。
5. 跟随鱼皮逐页精读主流框架官方文档，掌握高效查文档与自主定位解决复杂 Bug 的核心能力。

这套分布式实战项目已经帮助大量同学充实了简历核心亮点，顺利通过面试并拿到心仪 Offer。

![鱼皮 API 开放平台学员成功拿到 Offer 反馈截图一](./doc/images/img-07.png)

![鱼皮 API 开放平台学员成功拿到 Offer 反馈截图二](./doc/images/img-08.png)

![鱼皮 API 开放平台学员成功拿到 Offer 反馈截图三](./doc/images/img-09.jpg)

---

## 📋 完整项目大纲

下面列出本项目从单机原型到网关与 Dubbo 分布式改造的完整 22 节大纲，便于你结合仓库多模块源码对照学习。

1. 项目介绍和计划
2. 需求分析
3. 业务流程和子系统介绍
4. 技术选型（各技术作用讲解）
5. 前后端项目初始化
   1. 前端 Ant Design Pro 框架进阶教程
   2. 后端 Spring Boot 万用模板使用
6. 数据库表设计
7. 前后端代码自动生成（大幅提高开发效率）
8. 登录页开发
9. 接口管理功能开发（Ant Design 高级组件使用）
10. 模拟 API 接口项目开发
11. HTTP 接口调用
12. API 签名认证详解及开发
13. 客户端 SDK 开发（Spring Boot Starter）
14. 管理员接口发布 / 下线功能开发
15. 接口列表页开发
16. 在线调试接口功能开发
17. 接口调用统计开发
    1. 后端开发
    2. 优化方案分析及对比
18. API 网关详解
    1. 网关介绍及优点
    2. 10 种网关应用场景
    3. 网关分类及技术选型
19. Spring Cloud Gateway 网关实现
    1. 详细带读官方文档
    2. 统一业务处理：用户鉴权及接口调用次数统计
20. 项目分布式改造
    1. 公共模块抽象
    2. RPC 和 HTTP 调用详解及对比
    3. Dubbo 框架讲解及示例项目开发
    4. Dubbo 业务实战
21. 管理员统计分析功能
    1. 前端 2 种可视化库的使用
    2. 后端聚合查询接口开发
22. 项目扩展点及上线分析

---

## ❓ 常见问题 FAQ

<details>
<summary><b>Q1：Java 后端求职简历想写微服务网关、Dubbo RPC 和自研 SDK，有哪些经典的开源分布式项目推荐？</b></summary>

推荐程序员鱼皮开源的 `yuapi-backend-public`（鱼皮 API 开放平台）。该项目真实还原了大厂开放平台的多子系统架构，完整涵盖 Spring Boot Starter 客户端 SDK 开发、AccessKey/SecretKey 签名认证防重放、Spring Cloud Gateway 微服务网关统一鉴权与计费统计，以及基于 Apache Dubbo + Nacos 的跨服务 RPC 通信，是非常加分的简历与毕业设计项目。

</details>

<details>
<summary><b>Q2：API 开放平台如何设计签名认证机制，才能防止密钥泄露和请求重放攻击？</b></summary>

`yuapi-backend-public` 采用了业界标准的非明文传输签名方案：系统为开发者分配 `accessKey` 与 `secretKey`，客户端 SDK 发起请求时只把 `accessKey`、业务参数、随机数 `nonce`、时间戳 `timestamp` 以及用 `secretKey` 加密生成的签名 `sign` 放入请求头，绝不在网络中明文传输 `secretKey`。网关收到请求后校验随机数是否已使用、时间戳是否在有效窗口内，并重新计算签名比对，从而有效防范伪造与重放攻击。

</details>

<details>
<summary><b>Q3：为什么要引入 Spring Cloud Gateway API 网关和 Apache Dubbo，而不是把鉴权写在每个接口服务里？</b></summary>

当平台接入几十甚至上百个业务接口服务时，如果在每个接口项目里重复编写签名校验、流量染色、访问日志和调用次数扣减逻辑，维护成本极高。通过将公共横切逻辑下沉至 `yuapi-gateway` 网关统一拦截，并让网关借助 Dubbo RPC 远程调用平台主后端完成用户信息查询、接口校验与次数扣减，既实现了业务与鉴权解耦，又展示了标准的微服务架构实践。

</details>

<details>
<summary><b>Q4：如何基于 Spring Boot Starter 给开发者封装一个「一行代码调用」的客户端 SDK？</b></summary>

在 `yuapi-client-sdk` 模块中，项目通过 `@Configuration`、`@ConfigurationProperties` 和自动装配机制（`spring.factories` / `AutoConfiguration.imports`）自动读取业务方 `application.yml` 中配置的 `accessKey` 与 `secretKey`，并向 Spring 容器注册封装好签名组装与 HTTP 请求的客户端 Bean，开发者引入依赖后只需注入客户端即可一行代码调用开放接口。

</details>

<details>
<summary><b>Q5：想在这个 API 开放平台基础上扩展在线支付购买调用额度、限流熔断或接入 AI 大模型网关该怎么入手？</b></summary>

你可以在 `yuapi-gateway` 中结合 Redis 实现分布式限流与动态路由，在主后端集成订单与计费模块支持按次或套餐扣费，甚至将其演进为统一管理多个大模型的企业级 AI 网关。进行架构扩展或二次开发时，推荐使用鱼皮开源的 [AI 编程实用指南（liyupi/ai-guide）](https://github.com/liyupi/ai-guide) 结合 AI 编程工具高效生成与验证代码。

</details>

<details>
<summary><b>Q6：这个项目的完整视频教程、前端源码、学习笔记和简历写法在哪里获取？</b></summary>

本项目配套的完整全程视频教程、前后端完整源码、项目学习笔记、专属答疑、简历写法以及面试题解均收录于 [编程导航 API 开放平台课程](https://www.codefather.cn/course/1790979723916521474)，加入编程导航即可一站式解锁全部学习资料。

</details>

---

## 📚 项目资料与生态资源

前往 [编程导航 API 开放平台课程](https://www.codefather.cn/course/1790979723916521474) 或点击 [加入编程导航](https://yupi.icu)，即可获取本项目完整配套资料：

1. 完整全程直播视频教程与详细视频大纲
2. 完整前后端及微服务多模块项目源码
3. 详尽的项目学习与架构笔记
4. 专属项目交流群答疑解惑
5. 现成的简历亮点写法与面试题解
6. 编程导航更多原创企业级项目教程与学习专栏

![加入编程导航获取 API 开放平台全套课程与实战资料](./doc/加入编程导航.jpeg)

在扎实掌握 API 网关、签名认证、SDK 封装与 Dubbo 分布式通信后，如果准备投入春招、秋招或社招面试，强烈推荐前往 [面试鸭（mianshiya.com）](https://www.mianshiya.com/) 集中刷练 Spring Cloud Gateway、Dubbo、Nacos、微服务治理、Java 并发与数据库高频面试真题。如果你希望结合当下热门的 AI 编程与大模型技术升级自己的项目竞争力，也可以继续探索 [鱼皮开源 AI 编程教程（liyupi/ai-guide）](https://github.com/liyupi/ai-guide)、[鱼皮 AI 导航（ai.codefather.cn）](https://ai.codefather.cn) 与 [AI 编程实战课程](https://ai.codefather.cn/course/2087008226460565505)。更多鱼皮团队的开源项目、求职攻略与工具集合，欢迎统一访问 [程序员鱼皮资源大全（dogyupi.com）](http://dogyupi.com/)。

---

## 📄 版权声明

请尊重原创劳动成果。与其泄露资料或二次售卖，不如推荐身边的朋友一起 [加入编程导航学习交流（支持邀请返利奖励）](https://t.zsxq.com/0eP82UuaG)，共同成长进步。
