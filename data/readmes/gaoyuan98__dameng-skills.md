# dameng-skills

可复用技能包集合，用于沉淀数据库分析、内容创作与可视化等场景的工作流、脚本、参考资料和离线资源。这里的技能包面向能够读取 `SKILL.md` 的 AI 助手、自动化流程和人工使用者，不绑定某个特定平台。

## 当前技能包

| 技能包 | 用途 |
| --- | --- |
| `content-infographic` | 将文章、技术内容、优化案例或问题解决过程整理为蓝白卡片式流程信息图，交付可编辑 HTML，并在具备 Node.js 与 Chrome、Edge 或 Chromium 时导出 2 倍分辨率 PNG。 |
| `dm-log-visualizer` | 解析、汇总和可视化达梦/DM 数据库实例日志，生成中文离线 HTML 报告以及 CSV/JSON 证据文件。 |

## 目录结构

仓库根目录只放集合级文档和各个技能包目录。每个技能包目录必须自包含，目录名应与 `SKILL.md` 中的 `name` 保持一致。

```text
dameng-skills/
├── README.md
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

目录用途：

- `SKILL.md`：必需。技能包入口，描述何时使用、如何执行、如何分析结果、何时停止。
- `scripts/`：可选。放可执行脚本，适合需要稳定、可重复执行的解析、转换、报告生成等任务。
- `references/`：可选。放按需读取的参考资料，例如数据库机制说明、错误码、诊断手册、字段说明。
- `assets/`：可选。放输出需要携带或复制的静态资源，例如离线 JS/CSS、模板、示例素材。

不要在单个技能包目录中添加额外的 `README.md`、安装指南、快速参考、变更日志等冗余文档。集合级说明放在根目录 `README.md`，技能执行说明放在对应 `SKILL.md`。

## SKILL.md 规范

每个技能包必须包含一个 `SKILL.md`，并使用以下 frontmatter：

```yaml
---
name: skill-name
description: One clear sentence that explains what the skill does and when to use it.
---
```

规范要求：

- `name` 使用小写字母、数字和连字符，长度保持简短清晰。
- `description` 同时写清楚能力和触发场景，避免只写功能名。
- frontmatter 只放 `name` 和 `description`，不要添加无关字段。
- 正文只保留核心流程、关键命令、分析方法、停止条件和交付要求。
- 大段背景知识、字段解释和案例材料放入 `references/`，并在 `SKILL.md` 中说明何时读取。
- 脚本或资源路径必须使用相对技能目录可定位的路径，避免依赖个人机器路径。

## 使用方式

将需要使用的技能包目录导入到支持技能、工具或知识包的平台中。导入粒度应是完整技能目录，例如 `dm-log-visualizer/`，不要只复制 `SKILL.md`。

导入时保持目录结构不变，确保平台可以读取 `SKILL.md`，并能按相对路径访问同级的 `scripts/`、`references/`、`assets/`。平台应根据 `SKILL.md` frontmatter 中的 `description` 判断适用场景，再按正文中的流程调用脚本、读取资料或使用离线资源。

具体执行命令、输入要求、输出位置、分析顺序和交付内容以各技能包的 `SKILL.md` 为准。
