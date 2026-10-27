# miniob-env-traps

MiniOB / OceanBase 数据库大赛的**环境坑速查**（Agent Skill）。

只收「会复发、且不报错只骗人」的坑：改了代码不生效、日志找不到、脚本挂住、构建产物损坏、git 状态骗人、提测几秒失败且无信息。

## 结构

```
miniob-env-traps/
  SKILL.md      # 技能本体（Anthropic Agent Skills 协议：frontmatter + 正文）
  _meta.json    # 元信息（名称/描述/版本/标签）
```

## 使用

把整个目录放进你的 skills 目录（如 `./skills/miniob-env-traps/`），Agent 会按 `description` 里的触发场景自动加载。

## 内容

- 20 条坑：现象 → 对策（每条都带「怎么认出你踩上了」）
- 4 条识别原则：先怀疑环境再怀疑代码 / 间接信号不可信 / 卡住两轮就停 / 带排除清单求助
- 边界与触发条件

## 许可

Apache-2.0
