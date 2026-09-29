# PowerRAG 社区版文档仓库

欢迎访问 PowerRAG 社区版文档仓库。本仓库用于维护和发布与 PowerRAG 社区版相关的产品文档，包括 PowerRAG 社区版与其衍生项目 Langfuse 的文档内容。

## 仓库说明

本仓库包含以下两部分文档：

### 1. PowerRAG 社区版

PowerRAG 社区版是基于 [RAGFlow](https://github.com/infiniflow/ragflow) 二次开发的开源项目，采用 **Apache 2.0** 协议。该项目在 RAGFlow 的基础上，扩展了文档服务、结构化信息提取、多模搜索及效果评估与反馈等功能，为大模型（LLM）应用提供一体化的数据服务能力。  

PowerRAG 社区版文档仅介绍 PowerRAG 社区版新增的独立能力。其他与 Ragflow 通用的功能和使用方法，请参考 [RAGFlow 官方文档](https://ragflow.io/docs/v0.22.0/)。

### 2. Langfuse

Langfuse 是 PowerRAG 社区版生态下的独立子项目，用于实现效果评估与反馈模块。该项目拥有独立的 [GitHub 仓库](https://github.com/oceanbase/langfuse)，但文档统一收录在本仓库中，以便开发者集中查阅。  

Langfuse 提供模型可观测性、提示词管理与评估能力，帮助用户构建可监控、可调优的 LLM 应用体系。

## 文档结构

```plain
zh-CN/
├── 00.PowerRAG 社区版用户指南/    # PowerRAG 社区版文档
│   ├── 00.PowerRAG 社区版概述.md
│   ├── 10.新增分片方式.md
│   └── 20.结构化信息提取.md
└── 10.Langfuse 用户指南/          # Langfuse 项目文档
    ├── 00.Langfuse 概述.md
    ├── 10.部署与初始化/
    │   ├── 00.概述.md
    │   ├── 10.部署 Langfuse 服务.md
    │   ├── 20.访问 Langfuse 并创建 API 密钥.md
    │   └── 30.部署 Bridge 服务.md
    ├── 20.应用观测/
    │   ├── 00.概述.md
    │   ├── 10.快速开始.md
    │   ├── 20.可观测性数据模型.md
    │   └── 30.核心功能/
    │       ├── 00.会话（Sessions）.md
    │       ├── 10.用户跟踪（User Tracking）.md
    │       ├── 20.运行环境（Environments）.md
    │       ├── 30.标签（Tags）.md
    │       ├── 40.元数据（Metadata）.md
    │       └── 50.Trace ID 和分布式追踪（Distributed Tracing）.md
    ├── 30.提示词管理/
    │   ├── 00.概述.md
    │   ├── 10.快速开始.md
    │   ├── 20.提示词数据模型.md
    │   └── 30.核心功能/
    │       ├── 00.版本控制.md
    │       ├── 10.可组合性（Composability）.md
    │       ├── 20.消息占位符.md
    │       └── 30.Playground.md
    └── 40.应用评估/
        ├── 00.概述.md
        ├── 10.评估方法/
        │   ├── 00.LLM 作为评判（LLM-as-a-Judge）.md
        │   └── 10.评分数据模型.md
        ├── 20.跑测/
        │   ├── 00.跑测概述.md
        │   ├── 10.数据集.md
        │   ├── 20.通过 SDK 跑测.md
        │   ├── 30.通过控制台跑测.md
        │   └── 40.跑测数据模型.md
        └── 30.配置 LLM 连接.md
```

## 如何使用文档

您可以直接在 GitHub 上浏览文档，或将本仓库克隆到本地后查看：

```bash
git clone https://github.com/<your-org>/powerrag-docs.git
cd powerrag-docs
```

## 贡献指南

欢迎通过 Pull Request 或 Issue 提交文档修改、勘误或新增章节。

* 对于 PowerRAG 社区版相关内容，请在 `00.PowerRAG 社区版用户指南/` 下更新
* 对于 Langfuse 相关内容，请在 `10.Langfuse 用户指南/` 下更新

## 开源许可

本仓库的文档内容遵循 **Apache License 2.0** 协议。
