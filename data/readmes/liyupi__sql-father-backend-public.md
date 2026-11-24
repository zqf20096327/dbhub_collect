<div align="center">

# SQL Father - 模拟数据与 SQL 生成平台（Java 后端）

**SQL 之父全栈项目后端服务：一键生成建表 SQL、模拟测试数据、JSON 与前后端代码，大幅提升开发与测试效率**

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.7.x-6db33f.svg)](https://spring.io/projects/spring-boot)
[![MyBatis-Plus](https://img.shields.io/badge/MyBatis--Plus-3.5.x-blue.svg)](https://baomidou.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-4479a1.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)

作者：[程序员鱼皮](http://dogyupi.com/) · [在线体验](http://sqlfather.yupi.icu) · [视频演示教程](https://www.bilibili.com/video/BV1eP411N7B7/) · [前端代码仓库](https://github.com/liyupi/sql-father-frontend-public)

[项目简介](#-项目简介) · [核心场景与功能](#-核心场景与功能) · [技术栈](#-技术栈) · [系统架构设计](#-系统架构设计) · [快速启动](#-快速启动) · [常见问题](#-常见问题-faq) · [延伸学习](#-延伸学习与生态资源)

</div>

> **版权声明**：本项目为 [程序员鱼皮](http://dogyupi.com/) 原创开源学习项目，制作不易，请勿用于商业用途或二次售卖。如果你觉得本项目对日常开发或技术学习有帮助，欢迎点亮 Star 并给 UP 主一键三连支持！

---

## ✨ 项目简介

SQL Father（SQL 之父）是一套达到线上生产标准的前后端分离全栈工具平台，本仓库为其核心 Java 后端代码，配套的 React 前端仓库位于 [liyupi/sql-father-frontend-public](https://github.com/liyupi/sql-father-frontend-public)。你可以直接访问 [http://sqlfather.yupi.icu](http://sqlfather.yupi.icu) 在线体验完整功能，也可以通过 [B 站视频演示与使用教程](https://www.bilibili.com/video/BV1eP411N7B7/) 快速了解上手流程。

![SQL Father 模拟数据与建表 SQL 生成平台主界面截图](./doc/images/img-01.png)

项目的创作初衷源于非常真实的开发痛点：每次启动新项目或者编写接口联调测试时，开发者都要反复敲写建表 SQL 语句并手动构造假数据。如果只需几秒钟就能自动生成结构规范的建表语句、批量插入测试数据以及对应的实体代码，开发和测试效率将会提升一大截。至于有同学好奇为什么项目叫 SQL Father 而不叫 SQL Mother，其实思路很像面向对象编程里的概念——就像继承中的基类被称为「父类」一样，它希望成为各类业务数据表的统一源头。

除了作为高效率的提效工具之外，本项目同时包含完整的用户前台与管理后台，目录结构清晰规范。后端深度实践了策略模式、工厂模式、单例模式、建造者模式、门面模式以及 Spring AOP 切面鉴权，前端则涉及复杂动态嵌套可折叠表单与 Monaco 代码编辑器，非常适合全栈与 Java 后端同学深入研究。如果你希望系统学习本项目的创作思路、技术选型、源码拆解与简历写法，可以前往 [鱼皮的编程导航 - SQL 数据生成平台实战课程](https://www.codefather.cn/course/1966416608870055938) 或访问 [编程导航](https://yupi.icu) 查看完整讲解。

## 🌟 核心场景与功能

无论你是后端开发、前端工程师、测试人员、数据开发还是高校科研方向的同学，只要日常工作中会接触数据库表设计与测试数据构造，都能在以下典型场景中直接受益。

### 五大高频应用场景

当你从零设计一张新业务表时，可以直接填写可视化表单配置表名、字段类型和生成规则，系统会一次性输出建表 SQL、插入语句、模拟测试数据以及 Java 和前端代码，彻底告别重复劳动。

![SQL Father 可视化表单一键生成建表 SQL 与模拟数据截图](./doc/images/img-02.png)

如果手中已经有现成的数据库表结构或业务文档，系统提供了丰富的快捷导入能力。你可以直接粘贴现有的建表 SQL 语句解析出字段结构并生成模拟数据，也可以上传 Excel 表格自动识别表头完成建表，甚至可以使用智能导入功能，只输入几个字段关键词就能自动推导出完整的表结构与测试数据。

![SQL Father 支持智能导入、SQL 导入与 Excel 导入建表截图](./doc/images/img-03.png)

针对不同业务字段的数据特征，后端内置了多种灵活的模拟数据生成规则，涵盖固定值、随机值（人名、城市、手机号、邮箱等）、正则表达式匹配生成、规则递增，以及关联自定义词库在指定枚举范围内随机抽样。

![SQL Father 固定值、随机值、正则、递增与词库模拟规则配置截图](./doc/images/img-04.png)

为了降低团队与社区成员之间的重复造轮子成本，平台设计了完善的资源共享体系，支持词库、表设计和单个字段信息的公开共享。你可以直接参考其他开发者沉淀的优秀库表设计，一键导入复用或在其基础上二次修改。

![SQL Father 表结构与字段信息社区共享广场截图](./doc/images/img-05.png)

对于词库资源，你既可以直接利用现成词库一键生成系统字典表，也可以将其导出作为实验和数据分析用的基础数据集，并支持继承已有词库进行二次扩充与完善。

![SQL Father 词库管理、继承与一键生成字典表功能截图](./doc/images/img-06.png)

### 完整功能清单

系统整体划分为用户前台与管理后台两大模块，核心功能覆盖如下：

| 模块归属 | 功能分组 | 具体支持能力 |
| --- | --- | --- |
| 用户前台 | 可视化与快捷导入建表 | 支持可视化表单建表、智能导入、导入已有表、导入 JSON 配置、导入建表 SQL 与导入 Excel |
| 用户前台 | 一键多端代码与数据生成 | 支持生成建表 SQL 与插入语句、模拟数据、JSON 数据、Java 实体与对象代码、前端 TypeScript 代码 |
| 用户前台 | 模拟数据生成规则 | 支持固定值、随机值、正则表达式、递增序列与定制词库五种核心规则 |
| 用户前台 | 词库共享 | 支持创建词库、词库继承、一键创建字典表，以及根据词库随机生成数据（甚至可以用来决定午饭吃什么） |
| 用户前台 | 表信息与字段共享 | 支持创建公开表与字段信息、一键复制建表或字段语句、一键导入复用及违规内容举报 |
| 管理后台 | 平台运维与审核管理 | 包含用户管理、词库管理、表信息管理、字段信息管理与举报管理五大后台模块 |

## 🔧 技术栈

为了让前后端开发者都能快速理清整个全栈项目的技术选型，下面完整列出了后端服务与配套前端所使用的主要框架及核心依赖库。

### 后端技术选型（本仓库）

| 分类 | 技术或依赖库 | 核心作用 |
| --- | --- | --- |
| 基础框架 | Spring Boot 2.7.x + Spring AOP | 负责核心 Web 服务搭建与切面权限校验 |
| 数据持久层 | MyBatis-Plus 3.5.x + MySQL 8.x | 提供高效的数据持久化操作与关系型数据存储 |
| 模板与 SQL 解析 | FreeMarker + Druid SQL Parser | 分别负责动态代码模板渲染与现成建表 SQL 语法树解析 |
| 模拟数据引擎 | Datafaker + Generex | 分别支持逼真的多类型随机数据与基于正则表达式的数据生成 |
| 文档与工具库 | EasyExcel + Knife4j + Hutool + Gson + Apache Commons Lang3 | 负责 Excel 导入导出、在线接口文档、JSON 序列化及常用工具封装 |

### 前端技术选型（配套仓库）

配套前端仓库 [sql-father-frontend-public](https://github.com/liyupi/sql-father-frontend-public) 采用 React 18、Umi 4.x、TypeScript、Ant Design 4.x 与 Ant Design Pro Components 搭建，借助 ESLint 与 Prettier 保障代码风格一致，并集成了 `monaco-editor` 实现代码高亮预览以及 `copy-to-clipboard` 实现一键剪贴板复制。

## 📐 系统架构设计

传统 Web 项目的增删改查逻辑较为常规，这里重点拆解本仓库 `core` 目录下的核心架构设计与设计模式落地实践，帮助你从全局视角理解代码组织方式。

### 整体架构：任意输入收敛为统一 Schema

整个后端生成引擎最核心的设计理念可以概括为一句话：**任意输入 => 统一 Schema => 任意输出**。无论前端传来的是可视化表单、建表 SQL 还是 Excel 文件，系统都会先将其转换为结构一致的 `TableSchema` 模型，再交给下游各类生成器并行产出 SQL、数据与代码，从而彻底解耦输入源与输出目标，后续扩展新的输入方式或输出语言都无需改动原有核心流程。

![SQL Father 任意输入转统一 Schema 再生成任意输出的系统架构图](./doc/images/img-07.png)

基于这一思想，后端核心能力被清晰划分为四个职责分明的模块。首先由 **Schema 构造器** 将智能输入、SQL 语句、Excel 文件等不同格式的输入源统一解析为标准的表结构模型；接着交由 **统一 Schema 定义**（本质上是一个可序列化为 JSON 配置的 Java 模型类）集中保存库名、表名、表注释、模拟条数及字段列表；随后由 **生成器引擎** 读取这份 Schema 并协调数据生成规则和各类 Builder 输出 SQL、模拟数据及多语言代码；最后由 **共享服务** 承载词库、表信息、字段信息及举报记录的存储与增删改查 Web 接口。

### Schema 构造器与 Druid SQL 解析

核心类 `TableSchemaBuilder` 承担了将多样化入参收敛为 `TableSchema` 对象的职责，包含针对不同输入源的构建方法：

![TableSchemaBuilder 核心构造方法类图](./doc/images/img-08.png)

其中最值得借鉴的是 `buildFromSql` 方法（根据建表 SQL 反向推导 Schema）。它直接复用了阿里巴巴 Druid 数据库连接池内置的 SQL 语法解析器，解析能力非常完备且稳定。在实际工程开发中，面对 SQL 解析器这类复杂度极高的底层基础设施，合理复用成熟开源组件远比从零手写更高效可靠。

### 统一 Schema 数据结构

用于描述数据表与字段元信息的 `TableSchema` JSON 结构示例如下：

```json
{
  "dbName": "库名",
  "tableName": "test_table",
  "tableComment": "表注释",
  "mockNum": 20,
  "fieldList": [{
    "fieldName": "username",
    "comment": "用户名",
    "fieldType": "varchar(256)",
    "mockType": "随机",
    "mockParams": "人名",
    "notNull": true,
    "primaryKey": false,
    "autoIncrement": false
  }]
}
```

### 生成器与经典设计模式实践

后端在 `core/builder` 与模拟数据生成链路中综合运用了多种经典设计模式，使代码兼具高内聚与良好的扩展性。

#### 多种输出类型的 Builder 设计

系统将每一种生成目标抽象为独立的 Builder 类，存放在 `core/builder` 目录下。对于 SQL 生成器（`SqlBuilder`），项目引入了数据库方言（Dialect）抽象并结合**策略模式**支持不同数据库类型的语法差异，同时配合**单例模式与工厂模式**统一创建和管理方言实例。对于 Java 代码与前端代码生成器（`JavaCodeBuilder`、`FrontendCodeBuilder`），则借助 FreeMarker 模板引擎将 Schema 数据渲染为目标代码。

![SQL Father core/builder 目录下多种生成器类结构图](./doc/images/img-09.png)

![FreeMarker 代码生成模板示例截图](./doc/images/img-10.png)

#### 多种模拟数据规则的工厂设计

每一种造数规则都被封装为独立的 `DataGenerator` 实现类，由 `DataGeneratorFactory` 通过**工厂模式**统一完成实例注册、获取与生命周期管理。其中 `RandomDataGenerator` 底层集成 Datafaker 库生成多样化随机数据，`RuleDataGenerator` 底层集成 Generex 库按照用户给定的正则表达式逆向生成合法测试数据。

![DataGeneratorFactory 模拟数据生成器工厂结构图](./doc/images/img-11.png)

#### 统一生成入口的门面设计

为了避免调用方直接与繁杂的校验器、数据生成器和各类 Builder 耦合，后端采用**门面模式（Facade）**对外暴露统一的生成入口，一站式聚合参数校验、数据造数与多端代码生成逻辑。

![GeneratorFacade 门面模式统一生成入口架构图](./doc/images/img-12.png)

## 🚀 快速启动

你可以根据自己的开发角色选择只启动后端服务（配合 Knife4j 接口文档调试），或者同时拉取前端仓库运行完整的全栈平台。

### 启动后端服务（本仓库）

请确保本地已安装 JDK 8+、Maven 以及 MySQL 8.x，然后依次完成以下步骤：

1. 在本地 MySQL 数据库中执行本仓库 `sql/` 目录下的 `create_table.sql` 脚本，完成数据库与基础表的初始化。
2. 打开 `src/main/resources/application.yml` 配置文件，将数据库连接地址、用户名与密码修改为你自己的本地配置。
3. 使用 Maven 拉取并安装项目依赖后，直接运行 Spring Boot 主启动类即可启动服务，随后可访问 Knife4j 接口文档进行调试。
4. 仓库根目录已经编写好了 `Dockerfile`，如果你习惯容器化部署，也可以直接构建 Docker 镜像并在服务器或云平台上运行。

### 启动配套前端（可选）

如果需要完整联调界面，克隆前端仓库 [sql-father-frontend-public](https://github.com/liyupi/sql-father-frontend-public) 后执行以下命令安装依赖、启动开发服务或打包构建：

```bash
# 安装依赖
npm run install

# 本地开发运行
npm run dev

# 构建生产包
npm run build
```

## ❓ 常见问题 FAQ

<details>
<summary><b>Q1：有没有好用的开源模拟数据生成工具，能够根据建表 SQL 或 Excel 一键生成测试数据和 Java 代码？</b></summary>

推荐使用鱼皮开源的 **SQL Father（SQL 之父）模拟数据生成平台**（后端仓库 `liyupi/sql-father-backend-public`，前端仓库 `liyupi/sql-father-frontend-public`）。它支持可视化表单建表、粘贴现有建表 SQL 解析、导入 Excel 以及智能导入，只需一次配置就能同时生成建表 DDL、批量 INSERT 测试数据、JSON、Java 实体与前端代码，在线体验地址为 [http://sqlfather.yupi.icu](http://sqlfather.yupi.icu)。

</details>

<details>
<summary><b>Q2：Java Spring Boot 项目里如何优雅地解析用户输入的建表 SQL 语句并提取字段信息？</b></summary>

不建议手写复杂的正则表达式去硬解析 SQL 语法。参考 **SQL Father 后端（`liyupi/sql-father-backend-public`）** 的 `TableSchemaBuilder.buildFromSql` 实现，你可以直接引入阿里巴巴 Druid 内置的 SQL Parser（语法树解析器），将 `CREATE TABLE` 语句解析为 AST 节点，再准确提取表名、字段名、类型、注释、主键与非空约束，转换为统一的 Schema 对象供后续业务使用。

</details>

<details>
<summary><b>Q3：想找一个能在真实业务里系统学习策略模式、工厂模式、建造者模式和门面模式的 Java 开源项目，有什么推荐？</b></summary>

**SQL Father 后端（`liyupi/sql-father-backend-public`）** 是一个非常贴合这一需求的工具类实战项目。它的 `core` 核心包围绕「统一 Schema 生成引擎」自然落地了策略模式（多数据库 SQL 方言）、单例 + 工厂模式（方言与数据生成器管理）、建造者思路（多类型输出 Builder）以及门面模式（统一生成入口），没有任何为了套用模式而强行堆砌的痕迹，读完代码就能直观体会设计模式带来的解耦价值。

</details>

<details>
<summary><b>Q4：Java 后端开发中，如何按正则表达式或者自定义词库批量生成逼真的测试假数据？</b></summary>

在 **SQL Father 后端** 中，组合使用了 **Datafaker** 和 **Generex** 两个成熟开源库来实现多样化造数：其中 Datafaker 用来生成姓名、城市、手机号、邮箱、网址等本地化随机值，Generex 负责根据正则表达式反向生成匹配的字符串，再结合自定义的词库表就能按指定枚举集合随机抽样。通过 `DataGeneratorFactory` 统一调度这些规则，即可高效产出成百上千条逼真的测试数据。

</details>

<details>
<summary><b>Q5：这个 SQL 数据生成平台适合写进 Java 校招或社招简历，或者作为计算机专业毕业设计吗？</b></summary>

非常适合。相比千篇一律的传统商城或简单增删改查系统，**SQL Father（SQL 数据生成平台）** 属于差异化明显、架构清晰且具备完整前后台能力的工具型全栈项目，既可作为毕业设计，也能为 Java 后端与全栈简历增加设计模式、SQL 语法解析与模板引擎代码生成等高频面试亮点。你可以结合 [编程导航上的 SQL 数据生成平台实战教程](https://www.codefather.cn/course/1966416608870055938) 深入理解每个设计细节并扩展自己的亮点功能。

</details>

<details>
<summary><b>Q6：如何在 SQL Father 现有架构基础上继续扩展，比如支持 PostgreSQL 方言或接入 AI 智能建表？</b></summary>

得益于「任意输入 => 统一 Schema => 任意输出」的解耦设计，扩展新能力非常平滑。如果要支持 PostgreSQL 或 Oracle 等新数据库，只需新增对应的方言策略类并注册到方言工厂即可；如果要升级「智能导入」功能，只需在 `TableSchemaBuilder` 中接入大模型 API，把自然语言需求直接生成为标准 `TableSchema` JSON 即可无缝复用全部下游生成器。借助 AI 编程进行功能扩展时，可以参考鱼皮开源的 [Vibe Coding AI 编程教程（liyupi/ai-guide）](https://github.com/liyupi/ai-guide) 提升开发效率。

</details>

## 🤝 贡献指南

欢迎各位开发者一起参与优化和完善本项目，在提交代码之前请先留意以下几点建议：

1. 在动手修改之前，建议先通读本仓库的 `core` 核心模块代码与架构设计，确保改动符合统一的 Schema 与工厂抽象思路。
2. 你可以从修复 Issues 区已知问题、处理社区反馈建议（[反馈入口](https://support.qq.com/product/440825)）、新增数据库方言或扩展新的代码生成模板等方向切入贡献。
3. 提交 Pull Request 前请保持与原项目一致的代码格式与命名风格，做到最小化精准改动，避免引入无关文件变更。

## 🙏 致谢

感谢以下优秀开源项目与开放数据平台为本项目提供的词库与表结构示例灵感：

- 部分公共词库数据参考自 [fighting41love/funNLP](https://github.com/fighting41love/funNLP)
- 部分示例表结构信息参考自 [YesApi 开放表结构列表](https://open.yesapi.cn/list1.html)

## 📚 延伸学习与生态资源

如果你想系统掌握本项目从 0 到 1 的设计思路、源码拆解与简历亮点写法，欢迎加入 [鱼皮的编程导航](https://www.codefather.cn) 并学习对应的 [SQL 数据生成平台实战课程](https://www.codefather.cn/course/1966416608870055938)，编程导航还提供 20 余套全栈与 AI 应用开发项目教程、1 对 1 答疑交流以及完整的项目学习路线。

如果你想紧跟 AI 编程浪潮，学习如何用 AI 辅助二次开发、自动生成建表 Schema 或构建自己的 AI 工具，推荐阅读免费开源的 [AI 编程教程（liyupi/ai-guide）](https://github.com/liyupi/ai-guide)，同时也可以访问 [鱼皮 AI 导航](https://ai.codefather.cn) 与 [AI 编程实战课程](https://ai.codefather.cn/course/2087008226460565505) 系统提升 AI 工程能力。

学完本项目准备投递简历与冲刺面试时，欢迎前往 [面试鸭](https://www.mianshiya.com/) 专项刷题巩固 Java 基础、Spring Boot、MyBatis-Plus、MySQL 索引优化与设计模式等高频面试考点。更多由鱼皮团队整理的开源项目与免费资源，欢迎访问 [鱼皮团队资源大全](http://dogyupi.com/) 一站式查看。
