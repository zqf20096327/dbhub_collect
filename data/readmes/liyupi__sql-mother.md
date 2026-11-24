<div align="center">

# SQL 之母（SQL Mother）— 闯关交互式 SQL 自学网

**Free Interactive SQL Learning Platform Built Purely on the Frontend**

由 [程序员鱼皮](http://dogyupi.com/) 一人全栈构思并以纯前端实现的免费闯关式 SQL 自学教程网站

<p>
  <a href="http://sqlmother.yupi.icu" target="_blank">
    <img src="https://img.shields.io/badge/🌐_在线体验-sqlmother.yupi.icu-00b894?style=for-the-badge" alt="SQL 之母在线体验" />
  </a>
  <a href="https://www.bilibili.com/video/BV1pV4y1i7LW" target="_blank">
    <img src="https://img.shields.io/badge/🎬_B站视频演示-BV1pV4y1i7LW-fb7299?style=for-the-badge&logo=bilibili&logoColor=white" alt="SQL 之母视频演示" />
  </a>
  <a href="https://www.codefather.cn/course/1966412848320004097" target="_blank">
    <img src="https://img.shields.io/badge/📘_项目实战教程-编程导航-4c8bf5?style=for-the-badge" alt="闯关式 SQL 自学网项目教程" />
  </a>
</p>

<p>
  <a href="https://github.com/liyupi/sql-mother/stargazers">
    <img src="https://img.shields.io/github/stars/liyupi/sql-mother?style=flat-square&logo=github&color=f59e0b" alt="GitHub Stars" />
  </a>
  <a href="https://github.com/liyupi/sql-mother/network/members">
    <img src="https://img.shields.io/github/forks/liyupi/sql-mother?style=flat-square&logo=github&color=3b82f6" alt="GitHub Forks" />
  </a>
  <img src="https://img.shields.io/badge/Vue-3.x-42b883?style=flat-square&logo=vue.js&logoColor=white" alt="Vue 3" />
  <img src="https://img.shields.io/badge/TypeScript-4.x-3178c6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Vite-3.x-646cff?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/WebAssembly-sql.js-654ff0?style=flat-square&logo=webassembly&logoColor=white" alt="sql.js WebAssembly" />
  <img src="https://img.shields.io/badge/Monaco-Editor-007acc?style=flat-square&logo=visualstudiocode&logoColor=white" alt="Monaco Editor" />
</p>

[项目介绍](#-项目介绍) · [20 秒学会使用](#-20-秒学会使用) · [本地启动](#-1-分钟本地启动) · [功能特性](#-功能与特性) · [技术选型](#-技术选型) · [核心设计](#-核心设计解析) · [目录结构](#-项目目录结构) · [常见问题](#-常见问题-faq) · [贡献指南](#-贡献指南)

</div>

---

你可以直接访问 [http://sqlmother.yupi.icu](http://sqlmother.yupi.icu) 在浏览器中免安装开始闯关，也可以先观看 [B 站项目演示视频](https://www.bilibili.com/video/BV1pV4y1i7LW) 快速了解网站的整体玩法。如果你希望系统学习这套纯前端 SQL 引擎与闯关系统的源码实现，欢迎查看 [鱼皮的编程导航配套项目教程](https://www.codefather.cn/course/1966412848320004097)。

## 📖 项目介绍

SQL 之母（SQL Mother）是由 [程序员鱼皮](http://dogyupi.com/) 开源的一款完全免费的闯关交互式 SQL 自学教程网站。网站结合了鱼皮多年的 SQL 学习与工程实践经验，内置了 **30 个循序渐进的主线关卡** 以及 **15 个贴近真实业务场景的自定义趣味关卡**（涵盖电商分析、游戏数据、金融交易、物流配送、票房统计等主题）。用户不需要在本地折腾 MySQL、SQLite 或 PostgreSQL 数据库环境，打开网页就能编写并提交 SQL 代码做题闯关，从零基础开始逐步掌握常用 SQL 查询与数据库操作语法。

除了循序渐进的闯关主线之外，网站还提供了自由选择关卡、自定义关卡扩展以及可自由运行的 SQL 在线练习广场等功能，兼顾新手系统入门与老手随手验证语句的需求。

![SQL 之母闯关式 SQL 自学网主界面：左侧教程文档、右上角 SQL 编辑器与右下角实时查询结果](./doc/index.png)

### 为什么做这样一个网站？

SQL 知识在实际工作中极其重要，几乎是后端程序员、前端全栈开发者、产品经理以及数据分析同学共同的必备技能。相比单纯阅读文档或观看视频，学习 SQL 更适合在真实的数据表上动手写语句、看结果、反复调试来入门。

此前网络上虽然也有一些类似的 SQL 自学网站，但它们要么需要付费解锁，要么关卡零散、不够体系化。因此鱼皮决定自己动手打造一个完全免费且开源的 SQL 自学网，一方面希望能帮助更多人更轻松地学好 SQL，另一方面也希望这份纯前端实现的项目源码能够给开发者带来架构启发，吸引更多同学参与共建，一起把开源项目打磨得更好。

## ⚡ 20 秒学会使用

整个学习流程非常直观，你只需要按照下面四个步骤操作，20 秒就能顺利上手第一关：

1. 直接打开网站主页，首先完整阅读左侧的教程知识点与本关题目要求。
2. 在右上角的 SQL 编辑器中编写你的 SQL 语句，写完之后点击运行按钮提交结果。
3. 如果遇到卡壳或者想核对表结构，可以随时打开右下角的题目助手区域来辅助思考。
4. 当系统判定你的 SQL 执行结果正确之后，即可点击进入下一关继续挑战。

![SQL 之母 20 秒上手操作指南：阅读题目、编写 SQL、查看助手并验证通关](./doc/tutorial.png)

如果你已经具备一定的 SQL 基础，或者想针对某个知识点专门刷题，也可以直接进入选关页面自由挑选挑战。网站内的所有主线关卡与自定义关卡都没有解锁门槛，你完全不必受顺序限制：

![SQL 之母选关页面：支持自由切换 30 个主线关卡与趣味自定义实战关卡](./doc/levels.png)

## 🚀 1 分钟本地启动

由于 SQL 之母完全采用纯前端方案实现，不依赖任何后端服务器和本地数据库，因此你在自己电脑上启动整套项目非常简单。如果在线站点访问人数较多导致偶发卡顿，非常推荐你直接把代码拉取到本地流畅使用。

执行下面几条命令即可在 1 分钟内完成本地运行：

```bash
# 下载本项目源码到本地
git clone https://github.com/liyupi/sql-mother.git
cd sql-mother

# 安装项目所需依赖
npm install

# 启动本地开发服务器
npm run dev
```

## 🧩 功能与特性

为了让零基础同学能够顺畅入门，同时也满足进阶用户的自由练习需求，网站围绕「学、练、查、扩」四个环节设计了完整的功能体系。

在教程与做题环节，网站以清晰的 Markdown 格式呈现每一关的语法讲解与题目说明，并在右侧提供专业的代码编辑体验。提交 SQL 后，系统会自动比对查询结果并实时反馈是否通关；配套的题目助手则支持随时查看执行结果、查阅思路提示、检查原始建表语句以及核对参考答案，帮你把卡点迅速打通。

在关卡与自由练习环节，系统既支持按主线关卡顺序点击上一关或下一关系统推进，也支持在选关页自由切换任意主线关卡与自定义关卡。此外，项目专门提供了「SQL 广场」页面，你可以在这里像使用在线数据库沙箱一样自由建表、写入测试数据并执行任意 SQL 查询语句。

![SQL 之母在线 SQL 广场界面：支持自由输入、格式化与实时运行 SQL 语句](./doc/sql-playground.png)

## 🔧 技术选型

整个项目采用纯前端架构实现，前端开发者完全不需要具备后端前置知识即可读懂源码并参与开发。之所以坚持纯前端方案，主要出于三个非常务实的考量：第一，SQL 语句全部在用户本地浏览器沙箱中执行，从根源上减少了服务端遭受 SQL 注入和恶意攻击的风险；第二，省去了云数据库和后端服务器的持续运维开销，让公益免费网站能够长久稳定运行；第三，这也是一次很有价值的纯前端解决复杂业务场景的技术尝试。

项目用到的主要前端框架与核心依赖如下表所示：

| 类别 | 使用的技术与依赖 | 主要作用 |
| :--- | :--- | :--- |
| 前端核心框架 | Vue 3、Vite 3、Vue Router 4 | 负责组件化界面开发、路由切换与极速构建 |
| 组件库与文档渲染 | `ant-design-vue`、`bytemd`、`github-markdown-css` | 提供清爽的交互组件以及 GitHub 风格的 Markdown 教程渲染 |
| 编辑器与格式化 | `monaco-editor`、`sql-formatter` | 提供媲美 VS Code 的语法高亮代码编辑器与 SQL 一键格式化能力 |
| 浏览器端 SQL 引擎 | `sql.js`（基于 WebAssembly） | 在浏览器本地直接创建内存数据库并实时执行 SQL 语句 |
| 状态管理与持久化 | `pinia`、`pinia-plugin-persistedstate` | 管理当前关卡进度等全局状态并自动持久化到本地浏览器 |
| 工程化与工具库 | TypeScript、ESLint、Prettier、`lodash` | 保障类型安全、统一代码规范并提供常用数据处理函数 |

## 📐 核心设计解析

如果你想借这个项目提升前端架构设计能力，下面这四个核心模块的设计思路非常值得重点阅读。

### 1. 界面模块化设计

项目采用模块化的组件拆分思想，将核心做题页面拆分为三个彼此独立的 Vue 组件，分别负责文档展示、代码编写与结果反馈。这种拆分方式不仅实现了各区域业务逻辑的清晰隔离，还让组件具备了良好的跨页面复用能力，例如 SQL 编码区组件在主线做题页和 SQL 练习广场页面中就得到了直接复用。

具体来说，题目浏览区组件（`QuestionBoard`）负责渲染每一关的 Markdown 教程与题目描述；SQL 编码区组件（`SqlEditor`）封装了 Monaco 代码编辑器以及运行、格式化和重置按钮；题目结果区组件（`SqlResult`）则负责展示 SQL 执行后的结果表格与提示状态。最终，主页文件 `IndexPage.vue` 只需要引入这三个组件，并统一管理与传递当前关卡信息和运行结果数据，就能优雅地组装出完整的交互页面。

### 2. 关卡数据管理设计

虽然项目没有引入后端数据库，但所有关卡内容依然需要做到结构清晰、易于维护和方便扩展。为此，项目专门设立了 `src/levels` 目录来统一管理全部关卡数据，并将关卡划分为主线教程关卡与自定义扩展关卡两类，分别通过 `mainLevels.ts` 和 `customLevels.ts` 进行集中注册。

在目录组织上，每一个关卡都拥有独立的子目录，从而实现了关卡与关卡之间的彻底隔离。

![SQL 之母关卡目录结构示意图：每个关卡拥有独立的目录与配置文件](./doc/customLevel.png)

考虑到每一关的教程文章通常篇幅较长，直接把大段文案写死在 TypeScript 文件中既不方便阅读也不利于协作维护，因此项目采用了资源分离的策略：将教程正文单独保存在 `README.md` 文件中，将初始化建表语句保存在 `createTable.sql` 文件中，再在关卡入口文件 `index.ts` 中通过 Vite 的 `?raw` 语法直接导入文本内容。下面是一个典型关卡的完整定义示例：

```ts
import md from "./README.md?raw";
import sql from "./createTable.sql?raw";

export default {
  key: "level1",
  title: "基础语法 - 查询 - 全表查询",
  initSQL: sql,
  content: md,
  defaultSQL: "select * from student",
  answer: "select * from student",
  hint: "请仔细查看本关给出的示例",
  type: "main",
} as LevelType;
```

### 3. 纯前端 SQL 执行引擎

很多同学第一次接触这个项目时都会感到好奇，在完全没有后端数据库的情况下，纯前端究竟是如何建表并执行 SQL 查询的。有前端工程经验的同学通常会很快联想到 WebAssembly 技术。借助 WebAssembly，浏览器可以高效运行 JavaScript 之外的语言（例如 C 与 C++）编译出的底层模块。

在具体落地时，我们完全不必重复造轮子去从头编写数据库内核，而是可以站在巨人的肩膀上，直接集成成熟的开源库 `sql.js`（基于 SQLite 编译的 WebAssembly 版本）来在前端执行各类 SQL 操作。

这部分核心逻辑都封装在 `src/core/sqlExecutor.ts` 中，仅用初始化数据库（`initDB`）和执行语句（`runSQL`）两个函数就完成了整套浏览器端数据库引擎的对接：

```ts
import initSqlJs, { Database, SqlJsStatic } from "sql.js";

/**
 * SQL 执行器
 *
 * @author coder_yupi https://github.com/liyupi
 */
let SQL: SqlJsStatic;

/**
 * 获取初始化 DB
 * @param initSql
 */
export const initDB = async (initSql?: string) => {
  if (!SQL) {
    SQL = await initSqlJs({
      // Required to load the wasm binary asynchronously
      locateFile: () =>
        "https://cdn.bootcdn.net/ajax/libs/sql.js/1.7.0/sql-wasm.wasm",
    });
  }
  // Create a database
  const db = new SQL.Database();
  if (initSql) {
    // Execute a single SQL string that contains multiple statements
    db.run(initSql); // Run the query without returning anything
  }
  return db;
};

/**
 * 执行 SQL
 * @param db
 * @param sql
 */
export const runSQL = (db: Database, sql: string) => {
  return db.exec(sql);
};
```

每当用户进入一个新关卡时，系统会先调用 `initDB` 执行该关卡对应的初始化建表和示例数据导入脚本，随后用户提交的任意查询语句都会通过 `runSQL` 在这个内存数据库实例中即时得出结果。

### 4. 智能判题机制

与判题相关的状态枚举和校验函数都集中定义在 `src/core/result.ts` 文件中。为了避免死板地要求用户写出与标准答案一字不差的 SQL 文本，系统并没有直接比对字符串，而是通过对比真实查询结果的方式来判定对错，整个过程依次包含三个步骤：

1. 将用户提交的 SQL 语句与本关预设的标准答案 SQL 分别提交给执行器，得到两份查询结果表。
2. 校验两份结果表输出的列名集合是否完全一致，这里要求列的名称与排列顺序均保持一致。
3. 校验两份结果表输出的每一行数据记录是否完全一致。

在比对两份结果集的数据内容时，项目采用了一个非常巧妙的工程技巧：直接将两份查询结果对象序列化为 JSON 字符串并进行比对，从而替代了繁琐且容易出错的多重 `for` 循环遍历，代码既简洁又稳定。

## 📂 项目目录结构

为了方便你快速定位核心代码并上手二次开发，下面整理了整个仓库的目录结构与关键文件说明：

```text
sql-mother
├── public/                        # 公共静态资源目录
├── doc/                           # 项目文档与界面截图资源
├── src/                           # 前端核心源码目录
│   ├── assets/                    # 图片与样式等静态资源
│   ├── components/                # 可复用业务与基础组件
│   │   ├── CodeEditor.vue         # 通用代码编辑器组件
│   │   ├── MdViewer.vue           # Markdown 教程渲染组件
│   │   ├── QuestionBoard.vue      # 题目面板组件（左侧教程区）
│   │   ├── SqlEditor.vue          # SQL 编辑器组件（右上练习区）
│   │   ├── SqlResult.vue          # SQL 执行结果组件（右下结果区）
│   │   └── SqlResultTable.vue     # 查询结果数据表格组件
│   ├── configs/                   # 路由等全局配置文件
│   ├── core/                      # 核心引擎与状态管理
│   │   ├── sqlExecutor.ts         # 基于 sql.js 的 SQL 执行引擎
│   │   ├── result.ts              # 判题状态与结果校验核心逻辑
│   │   └── globalStore.ts         # Pinia 全局状态管理
│   ├── levels/                    # 关卡数据与配置目录
│   │   ├── custom/                # 自定义趣味实战关卡目录
│   │   ├── main/                  # 30 个主线教程关卡目录
│   │   │   └── level1/            # 每个关卡独立成目录，互不干扰
│   │   │       ├── createTable.sql # 本关依赖的初始化建表与数据语句
│   │   │       ├── index.ts       # 本关元信息、默认 SQL、答案与提示配置
│   │   │       └── README.md      # 本关知识点与题目文档
│   │   ├── index.ts               # 关卡加载与查询辅助函数
│   │   ├── level.d.ts             # 关卡 TypeScript 类型定义
│   │   ├── mainLevels.ts          # 主线关卡注册列表
│   │   └── customLevels.ts        # 自定义关卡注册列表
│   ├── pages/                     # 页面级视图组件
│   │   ├── IndexPage.vue          # 闯关学习主页
│   │   ├── LevelsPage.vue         # 自由选关页面
│   │   └── PlaygroundPage.vue     # SQL 自由练习广场页面
│   ├── App.vue                    # 应用根组件
│   ├── main.ts                    # Vue 应用入口文件
│   ├── style.css                  # 全局样式文件
│   └── vite-env.d.ts              # Vite 环境类型定义
├── .eslintrc.js                   # ESLint 代码规范配置
├── .gitignore                     # Git 忽略文件清单
├── index.html                     # 静态入口页面
├── package.json                   # 项目依赖与脚本管理
├── tsconfig.json                  # TypeScript 编译配置
└── vite.config.ts                 # Vite 构建配置
```

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q1：零基础自学 SQL 有哪些免费、不用安装数据库就能在线练习的网站推荐？</b></summary>

SQL 之母（[在线体验](http://sqlmother.yupi.icu)）就是一个完全免费且免安装数据库的开源 SQL 自学网站。你只需要打开浏览器，就能在网页内一边阅读循序渐进的语法教程，一边在内置的 Monaco 代码编辑器里编写并运行 SQL 语句，系统会实时给出查询结果和自动判题反馈，非常适合零基础新手、产品经理和数据分析同学快速入门。

</details>

<details>
<summary><b>Q2：有没有像玩游戏闯关一样的 SQL 刷题网站，适合快速掌握 MySQL 常用语法？</b></summary>

SQL 之母内置了 30 个体系化的主线闯关教程以及 15 个模拟真实业务场景的趣味自定义关卡（涵盖电商分析、游戏数据、金融交易、物流配送等主题），并且所有关卡均免费开放、支持自由选关。它覆盖了条件查询、排序分页、聚合分组、多表关联（JOIN）、子查询和窗口函数等标准 SQL 核心语法，掌握之后可以平滑迁移到 MySQL、PostgreSQL 和 SQLite 等主流关系型数据库。

</details>

<details>
<summary><b>Q3：如何在纯前端浏览器里直接执行 SQL 语句并实现自动判题？</b></summary>

SQL 之母采用 WebAssembly 方案解决了纯前端运行数据库的难题。项目通过集成开源的 `sql.js` 库在浏览器内存中初始化 SQLite 实例，加载关卡的建表和示例数据脚本后实时执行用户输入的语句；判题时则分别执行用户 SQL 与标准答案 SQL，再比对两份结果表的列名顺序与 JSON 序列化后的行数据是否完全一致，既精准又避免了后端被注入攻击的风险。

</details>

<details>
<summary><b>Q4：学完 SQL 基础语法之后，准备后端或数据分析求职面试还需要重点刷什么？</b></summary>

通过 SQL 之母熟练掌握常用查询语法与多表关联之后，如果你正在准备后端开发、测试或数据分析岗位面试，建议进一步巩固 MySQL 索引底层原理（如 B+ 树与最左匹配）、慢 SQL 调优、事务隔离级别与锁机制等高频考点。你可以继续前往 [面试鸭](https://www.mianshiya.com/) 针对性地刷数据库与 SQL 高频面试真题，系统提升面试通过率。

</details>

<details>
<summary><b>Q5：有哪些高星且代码清晰的 Vue 3 + TypeScript 纯前端开源项目适合练手或当毕业设计？</b></summary>

SQL 之母拥有 4500+ GitHub Stars，基于 Vue 3、TypeScript、Vite、Pinia、Ant Design Vue、Monaco Editor、ByteMD 与 sql.js 构建，涵盖组件模块化拆分、关卡数据驱动架构、WebAssembly 引擎对接与自动判题逻辑。项目无需后端即可本地秒级启动，非常适合作为前端进阶练手项目或在其基础上扩展后端与排行榜作为毕业设计。配套的系统架构讲解与简历写法可以查看 [编程导航的闯关式 SQL 自学网项目教程](https://www.codefather.cn/course/1966412848320004097)。

</details>

<details>
<summary><b>Q6：在线访问偶尔加载较慢怎么办？如何在本地离线流畅刷题？</b></summary>

由于首次打开页面需要加载 `sql.js` 的 WebAssembly 运行文件，在访问高峰期可能会稍慢。你可以直接克隆本仓库到本地，依次执行 `npm install` 和 `npm run dev` 启动本地服务，所有关卡教程、SQL 练习广场和自动判题都会在本地浏览器中极速运行。

</details>

## 🤝 贡献指南

非常欢迎各路开发者参与项目共建，无论是新增趣味关卡、完善文档还是扩展系统功能，都是一件利人利己、很有成就感的事情。目前我们主要推荐下面三种贡献方式。

### 1. 贡献新关卡

在动手编写新关卡之前，请先确认你已经理解了上文介绍的关卡加载机制。为了保证主线教程的知识连贯性，我们更推荐大家优先贡献「自定义关卡」而不是修改主线关卡，这类提交也会更容易获得合并。你可以按照以下五个步骤完成一个自定义关卡的开发：

1. 复制 `src/levels/custom/自定义关卡模板` 目录，并将新目录重命名为你设计的关卡中文名称。
2. 编辑模板中的 `createTable.sql` 文件，编写本关所需的建表语句并插入清晰的示例测试数据。
3. 编辑模板中的 `index.ts` 文件，完整填写关卡的中英文标识、默认 SQL、标准答案 SQL 以及解题提示。
4. 编辑模板中的 `README.md` 文件，编写清晰的标题、背景故事与题目要求，务必给出完整的表结构说明，并明确写出输出顺序等判题细节要求。
5. 打开 `src/levels/customLevels.ts` 文件，导入并注册你刚刚新建的自定义关卡。

需要特别注意的是，由于底层引擎采用 `sql.js`，本项目仅支持 SQLite 语法（绝大多数标准通用 SQL 均支持），编写题目和答案时请尽量使用通用 SQL，避免依赖过于生僻的方言函数。

![SQL 之母自定义关卡模板目录示例](./doc/customLevel.png)

### 2. 完善现有内容

如果你在刷题过程中发现了某道关卡的错别字、表结构描述不清或答案边界问题，非常欢迎直接提交 Pull Request 来修复错误、优化文档表述、补充更多实用干货或者微调关卡难度曲线。

### 3. 项目功能扩展

由于本项目最初由鱼皮一人利用业余时间开发完成，很多细节和进阶想法还没有来得及全部实现，非常欢迎大家 Fork 仓库进行自由扩展，打造出属于你自己的「SQL 之子」「SQL 之孙」系列作品。下面列出了一些值得尝试的扩展方向：

1. 当用户点击提交题目之后，自动展开下方的执行结果区域，减少手动操作。
2. 当用户顺利通关之后，展示更加友好的过关反馈动画，并提供更顺手的跳转下一关入口。
3. 进一步增强 SQL 一键格式化与快捷键支持，提升编码体验。
4. 优化关卡资源的加载机制，按需动态加载关卡文档与初始化数据，降低首屏体积。
5. 为项目接入后端服务与数据库，支持用户在网页端直接在线投稿、审核和发布新关卡。
6. 增加用户登录体系与闯关进度排行榜，增强学习激励感。

值得一提的是，如今结合 AI 编程工具来扩展这类模块化项目效率极高，你可以让 AI 帮你批量生成趣味业务关卡、编写 SQL 错因解释助手，甚至快速补全后端接口。如果你想系统掌握如何用 AI 编程从 0 到 1 打造和迭代完整产品，可以参考鱼皮开源免费的 [AI 编程与 Vibe Coding 零基础入门教程（ai-guide）](https://github.com/liyupi/ai-guide)，也可以学习配套的 [AI 编程实战课](https://ai.codefather.cn/course/2087008226460565505) 或逛一逛 [鱼皮 AI 导航](https://ai.codefather.cn)。

感谢阅读与支持，也欢迎加入 [鱼皮的编程导航](https://yupi.icu) 学习更多从 0 到 1 的原创实战项目，或者前往 [鱼皮的资源大全](http://dogyupi.com/) 获取更多免费编程学习资料与实用工具。如果 SQL 之母帮到了你，欢迎点一个免费的 Star 收藏鼓励！

## 🙏 感谢赞助

本项目 CDN 加速及安全防护由 Tencent EdgeOne 赞助：

[亚洲最佳CDN、边缘和安全解决方案 - Tencent EdgeOne](https://edgeone.ai/zh?from=github)

![Tencent EdgeOne 赞助支持](https://github.com/user-attachments/assets/eeb52237-4520-4a97-8f3d-6cb901e2106a)
