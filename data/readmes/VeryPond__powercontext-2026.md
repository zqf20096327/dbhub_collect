# PowerContext 赛题仓库

2026 第六届 OceanBase 数据库大赛 · **PowerContext 方向**（11 道赛题）参赛仓库。

> CCF 数据库专委指导，OceanBase 主办
> 主题：AI × 数据库 —— 从 0 到 1，打造你的 AI 数据库

---

## 赛题方向

PowerContext 聚焦大模型与 AI Agent 的**上下文工程**，围绕上下文的采集、解析、组织、检索、压缩、记忆更新与运行时注入设置赛题。

从官方赛题说明可归纳的动手方向：

| 方向 | 说明 |
| --- | --- |
| 多源上下文接入与结构化 | CSV 原始记录采集、Pi 会话历史接入 |
| 相关性检索与排序 | 财报 PDF 证据页检索、检索重排 |
| 长短期记忆管理 | 记忆停用与恢复 |
| 冗余与冲突处理 | 重复/矛盾上下文归并 |
| 上下文压缩与预算控制 | 上下文增量传输、Embedding 请求合并与缓存 |
| Agent 场景动态上下文编排 | 运行时按任务注入最相关上下文 |

考察维度：功能正确性、上下文相关性、任务效果、推理成本、工程质量、可解释性（证据可追溯）。

## 上游项目

- 仓库：<https://github.com/oceanbase/powercontext>
- 官网：<https://powercontext.oceanbase.io>
- 许可：Apache-2.0

## 仓库结构

```
powercontext-2026/
├── solutions/          # 赛题作答，一题一目录
│   └── _template/      # 新赛题目录模板
├── docs/               # 设计说明、实验记录、复现步骤
├── scripts/            # 环境安装、数据准备、评测脚本
└── README.md
```

### 单题目录约定

```
solutions/<题号>-<短名>/
├── README.md      # 题目要求、思路、运行方式、结果数据
├── src/           # 实现代码
├── data/          # 小样本数据（大文件不入库，见 .gitignore）
└── results/       # 评测输出、指标对比
```

## 环境

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 进度

| 题号 | 题目 | 状态 | 负责人 |
| --- | --- | --- | --- |
| - | - | - | - |

状态取值：`待认领` / `进行中` / `已完成` / `已提测`

## 提交规范

```
<题号>: <一句话说明>

- 改了什么
- 验证方式与结果
```

## 许可

本仓库内容遵循 [Apache-2.0](LICENSE)。
