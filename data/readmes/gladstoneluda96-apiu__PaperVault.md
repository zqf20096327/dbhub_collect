# PaperVault

PaperVault 是一款本地优先的学术论文管理工作台。导入 PDF 后，它会将论文转换为结构化 Markdown，并生成中文摘要、问答、术语表与全文翻译，帮助研究者按项目、标签和引用关系整理阅读材料。

> 论文原文、数据库和分析结果默认保存在本地，不会上传到 PaperVault 的服务器。

## 测试图片

以下图片用于检查 GitHub 的图片渲染效果，同时展示 PaperVault 的主要界面方向。

![论文库概览](assets/test-images/library-overview.svg)

![双语阅读与智能分析](assets/test-images/reading-workbench.svg)

![论文引用关系图](assets/test-images/citation-map.svg)

## 功能

- 导入本地 PDF，或通过 arXiv ID / Semantic Scholar 链接获取论文
- PDF 转 Markdown，保留章节与正文结构
- 生成中文摘要、研究问答和专业术语表
- 英文论文全文翻译，优先使用所配置的 LLM 或 DeepL
- 自动检索 CrossRef / Semantic Scholar 元数据
- 按项目、标签和关键词管理论文
- 基于 SQLite FTS5 的本地全文搜索
- 跟踪论文之间的双向引用关系
- 在应用内预览英文原文与中文译文

## 技术栈

- Tauri 2
- Vite 6
- Vanilla JavaScript / CSS
- Rust 2021
- SQLite + FTS5

## 本地运行

### 环境要求

- Node.js 18+
- Rust stable
- Tauri 2 对应的系统依赖

### 启动

```bash
npm install
npm run tauri -- dev
```

首次启动后，应用会在项目目录中创建 `paper_data/`，用于保存本地数据库、PDF 与生成的 Markdown。

### 构建

```bash
npm run tauri -- build
```

## API 配置

在应用右上角的设置面板中配置所需服务：

- LLM API Key 与接口地址
- DeepL Auth Key（可选）

API Key 只保存在当前设备的应用本地存储中。请勿将个人密钥、论文原文或本地数据库提交到版本库。

## 数据与隐私

- `paper_data/` 与 `.env*` 已被 Git 忽略
- 论文处理过程中，只会将所需文本发送到用户主动配置的 LLM、翻译或元数据服务
- 元数据查询可使用无需密钥的 CrossRef 与 Semantic Scholar 服务

## 项目文档

功能范围、处理管线、数据库结构和版本记录见 [PROJECT_PLAN.md](./PROJECT_PLAN.md)。

## 状态

PaperVault 目前处于早期开发阶段，核心阅读、整理与论文分析流程已可用，安装包与跨平台适配仍在持续完善。
