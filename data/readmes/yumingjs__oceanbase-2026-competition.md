# 2026 OceanBase 数据库大赛复现归档

**雏草姬万岁** · **Liangyu Kong** · **东北大学计算机科学与工程学院**

这是单独的公开复现仓库，收录初赛 11 题和加赛 MiniVectorDB 的复现入口，初赛正式总分为 **620/620**。生态项目可从各自目录运行，内核项目使用固定上游提交和源码补丁还原。 [赛事主页](https://open.oceanbase.com/train/detail/21)

## 初赛

| 题号 | 题目与入口 | 运行方式 | 验证结果 |
| --- | --- | --- | --- |
| 600069 | [seekdb SQL 扩展](preliminary/600069-seekdb-sql/) | 应用补丁，构建 seekdb，逐组运行 AI 函数、文件 SQL 和 AI 列用例 | 赛时 160/160，归档补丁校验通过 |
| 600070 | [PowerContext](preliminary/600070-powercontext/) | 应用补丁，运行 10 组公开代码自测 | 赛时 240/240，复测 95 项通过 |
| 600071 | [seekdb 基础实践](preliminary/600071-seekdb-practice/) | 启动独立 seekdb 实例，运行 SQL 并查看公开协作流程 | 赛时 30/30，原生实例 SQL 和版本读取通过 |
| 600072 | [AMD 向量索引](preliminary/600072-amd/) | 应用补丁，运行 CPU 契约测试。GPU 构建使用 ROCm 与 hipVS | 赛时 20/20，桥接层 CPU 测试通过 |
| 600073 | [阶跃星辰](preliminary/600073-stepfun/) | 安装依赖，下载固定模型，启动浏览器和 seekdb 服务 | 赛时 20/20，复测 6 项和 Vite 构建通过 |
| 600074 | [高德地图](preliminary/600074-gaode/) | 在有高德地图工具的环境加载 Skill | 赛时 20/20 |
| 600075 | [ModelScope](preliminary/600075-modelscope/) | 启动课程资料服务，导入样例后运行 Skill 客户端 | 赛时 20/20，复测真实 seekdb 与 HTTP 原文回查通过 |
| 600076 | [Dify · 异界档案馆](preliminary/600076-dify/) | 启动 Dify、档案服务和本地 CPU 模型，运行端到端验证器 | 赛时 20/20，主 DSL 与后端复测 10 项通过 |
| 600077 | [MiniMax](preliminary/600077-minimax/) | 运行 seekdb 与 PowerContext 的上下文重启验证，按需接入 MiniMax API | 赛时 20/20，复测 35 项通过 |
| 600078 | [Qoder](preliminary/600078-qoder/) | 创建数据库并启动资料检索与复习卡网页 | 赛时 20/20，复测 25 项通过 |
| 600080 | [seekdb 全文索引优化](preliminary/600080-seekdb-fts/) | 应用补丁，运行批写回归和全文索引用例 | 赛时 50/50，归档补丁校验通过 |

## 加赛

| 题目与入口 | 运行方式 | 验证结果 |
| --- | --- | --- |
| [MiniVectorDB · 600081](playoff/minivectordb.md) | 在仓库根目录使用 CMake 或 Docker 构建，通过 JSON Lines 执行 SQL 和向量检索 | CMake、PGO、官方公开用例 20/20 和崩溃恢复通过 |
| [MiniVectorDB · 性能与 Prompt 实验](playoff/minivectordb.md#prompt-专项实验) | 使用固定随机种子的合成负载和公开用例复核查询正确性、性能及持久化 | 精确检索与 Python 暴力搜索抽查一致 |

各题页面注明构建要求、具体命令与验证范围。平台记分、账号配置和原始开发记录由队伍单独存档。贡献归属和上游许可见 [版权声明](COPYRIGHT.md)。
