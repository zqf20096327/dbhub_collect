# oGRAC-common-tools

oGRAC 定制适配工具管理仓库。

## 工具清单

### ograc-docs-review

oGRAC 中文文档低级错误检视与修复 skill。

- 作用：自动扫描 `docs/zh/` 下 Markdown（含 `_toc.yaml`），按规则修复错别字、产品命名不一致、中英文混排空格、行内代码缺失、SQL 关键字大小写、Markdown 格式、口语化表述、Shell 代码块可复制性、弯引号等。
- 触发：在 OpenCode 中处理「检视/审校/修复/规范化 docs/zh 文档」「文档低级错误」「文档格式检查」「清理口语化」「PR 文档自检」「同步官方文档前批量检查」或任何涉及 oGRAC 中文文档质量批处理的任务时，agent 会自动加载本 skill。
- 使用：将 `ograc-docs-review/` 目录复制到 `.opencode/skills/ograc-docs-review/` 或 `.agents/skills/ograc-docs-review/` 下即可生效。
- 规则文件：`ograc-docs-review/references/ograc_rules.json`

## 许可证

MulanPSL-2.0
