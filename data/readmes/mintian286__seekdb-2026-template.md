# seekdb 赛题仓库

2026 第六届 OceanBase 数据库大赛 · **OceanBase seekdb 方向**参赛仓库。

- 参赛账号：**mintian286**
- 仓库地址：https://github.com/mintian286/seekdb-2026
- 当前阶段：仓库初始化，赛题作答待开展。

## 赛题方向

围绕 seekdb 的数据存储、处理、检索与智能应用开展实践。按具体赛题记录问题分析、实现方案、测试结果与复现步骤，题目要求和评测指标以赛事官方发布为准。

## 上游项目

- 官方源码：https://github.com/oceanbase/seekdb
- 上游许可：Apache-2.0

## 仓库结构

```text
seekdb-2026/
├── solutions/          # 赛题作答，一题一目录
│   └── _template/      # 单题作答模板
├── .gitignore
├── LICENSE
└── README.md
```

随着作答推进，按需增加以下目录：

```text
bench/                 # 压测、消融实验与基线数据
docs/                  # 设计说明、改动分析与复现步骤
scripts/               # 编译、部署和数据生成脚本
```

### 单题目录约定

```text
solutions/<题号>-<短名>/
├── README.md          # 题目要求、改动点、构建方式和实测数据
├── patches/           # 相对官方源码的补丁
├── sql/               # 建表、查询和测试 SQL
├── data/              # 小样本数据，大文件不入库
└── results/           # 性能对比、召回率与分析结果
```

## 构建与运行

本仓库用于管理参赛作答、补丁、实验和说明。seekdb 的构建与运行方法请参考[官方仓库](https://github.com/oceanbase/seekdb)，每道题的具体操作写在对应目录的 README 中。

## 进度

| 题号 | 题目 | 状态 | 负责人 |
| --- | --- | --- | --- |
| 待补充 | 待选题 | 待认领 | mintian286 |

状态取值：`待认领` / `进行中` / `已完成` / `已提测`。

## 提交规范

```text
<题号>: <一句话说明>

- 改了什么
- 验证方式与结果
- 复现步骤与环境
```

## 模板来源与许可

初始目录和作答模板导入自 [VeryPond/seekdb-2026](https://github.com/VeryPond/seekdb-2026)，保留原有提交历史及 Apache-2.0 许可证；本说明已针对 mintian286 的参赛仓库调整。后续作答在本仓库中维护。

本仓库内容遵循 [Apache-2.0](LICENSE)。
