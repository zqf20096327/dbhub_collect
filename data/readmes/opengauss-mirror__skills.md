# skills

面向openGauss社区的 Agent Skills 合集，覆盖设计、开发、测试等研发环节。

## 目录结构

```
skills/
├── skills/                  # 所有 skill 平铺，一个 skill 一个目录
│   └── <skill-name>/
│       ├── SKILL.md         # 必须
│       ├── scripts/         # 可选：可执行脚本
│       └── references/      # 可选：参考文档
├── template/
│   └── SKILL.md             # 新 skill 模板
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Skill 索引

### 设计（design）

暂无

### 开发（development）

| Skill | 说明 |
| --- | --- |
| [commit-message](skills/commit-message/SKILL.md) | 根据暂存区改动生成 Conventional Commits 提交信息 |

### 测试（testing）

暂无

### 发布运维（release）

暂无

### 协作文档（collaboration）

暂无

## 使用方法

把需要的 skill 目录复制到 Agent 的 skill 目录下即可。

## 贡献

欢迎提交新的 skill，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

本项目采用 [木兰宽松许可证第2版（Mulan PSL v2）](LICENSE)。
