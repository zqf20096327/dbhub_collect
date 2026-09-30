# openGauss RAG Best Practices

## 项目简介

本项目是一个基于 **openGauss 的 RetrievalQA / RAG 工程实践项目**，围绕“文档切分 → embedding 生成 → 向量写库 → 相似度检索 → 上下文拼接 → 生成回答”的完整链路展开，重点不只是验证系统能否跑通，而是沉淀一套更适合工程复用的配置收敛过程与最佳实践。

当前主线采用：

- **openGauss**：向量存储与检索
- **HuggingFace DPR**：query / context embedding
- **自定义 RetrievalQA 管线**：参数化控制 chunk、operator、top-k、generator
- **生成模型**：以 `flan-t5-base` 为 baseline，以 `Phi-3.5-mini-instruct` 为当前主生成器路线

本仓库更偏向“项目阶段经验总结 + 工程验证结果沉淀”，适合用于：

- openGauss + RAG 方案验证
- 向量检索与生成模型解耦实验
- 边缘部署场景下的系统拆分参考
- 最佳实践与阶段性评测归档

---

## 项目亮点

- 基于 **openGauss** 完成向量写库与相似度检索，构建 RetrievalQA 主链路。
- 将 **chunk / similarity operator / top-k / generator** 进行解耦，便于独立实验与参数收敛。
- 明确区分 **retrieval evaluation** 与 **generation evaluation**，避免两层问题相互掩盖。
- 对 `flan-t5-base` 与 `Phi-3.5-mini-instruct` 进行了阶段性端到端对比。
- 面向 **AArch64 / RK3568** 的部署目标，形成了“开发机重处理、边缘端保留最小闭环”的工程判断。

---

## 系统架构

当前项目的主链路如下：

```text
Raw Text
  -> TextChunker
  -> HFEmbedder (DPR Context Encoder)
  -> openGauss (vector store)
  -> OPController Retrieval
  -> RagPipeline Context Assembly
  -> Generator
  -> Final Answer
```

工程角色划分上，当前更推荐：

- **开发机侧**：文档切分、embedding 生成、批量入库、生成模型实验
- **边缘端侧**：在线 query、向量检索、轻量响应组装

---

## 项目目录结构

```text
.
├── app/
│   ├── text_chunker.py          # 文本切分与 chunk 构造
│   ├── hf_embedder.py           # HuggingFace DPR embedding 生成
│   ├── op_controller.py         # openGauss 连接、写库与检索控制
│   └── rag_pipeline.py          # RetrievalQA 主流程封装
├── scripts/
│   ├── test_rag.py              # 端到端测试入口
│   ├── build_index_hf_opengauss.py # HuggingFace DPR embedding 生成与存储测试入口
│   ├── test_retrieval.py        # openGauss 检索测试入口
│   └── test_split_chunk.py      # Chunker 测试入口
├── docs/
│   ├── advice/                  # 生成模型推荐 / 总体/待测试内容
│   ├── eval/                    # 评测结果与阶段性记录
│   ├── filename_map/            # 文件名总览 / 新命名输出文件与原始输出文件对应表
│   ├── output/                  # 新命名输出文件
│   ├── query                    # 测试使用query
│   ├── review/                  # 最佳实践报告
│   └── raw_outputs/             # 原始终端输出与归档材料
├── app/                         # 过程输出数据：dataset-chunk / dataset-embeddings
├── requirements.txt             # Python 依赖
├── docker-compose.yml           # Docker Compose 配置（阶段性工程材料）[不适配于当前配置未归档在此]
├── bentofile.yaml               # BentoML 配置（阶段性工程材料）[不适配于当前配置未归档在此]
└── README.md
```

> 注：仓库中的 BentoML / Docker / Compose 相关文件主要用于说明工程实现路径，不等价于“已经验证完毕的最终最佳实践参数”。

---

## 环境要求

当前阶段主要实验环境如下：

- **OS**：Ubuntu 24.04.3 LTS
- **架构**：x86_64
- **CPU**：AMD Ryzen 7 H 255，8 核 16 线程
- **内存**：30 GiB
- **GPU**：未使用 GPU 加速，当前结果主要基于 CPU 推理
- **openGauss**：6.0.2
- **Python**：建议 3.10

核心依赖以 `requirements.txt` 为准。

> 说明：早期 FAISS 索引阶段与后期 RAG end-to-end 阶段的 Ubuntu 版本并不完全一致。当前 README 以“后期主线环境”为主。

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备 openGauss

你需要先准备好 openGauss 实例，并完成：

- 数据库创建
- 表结构初始化
- `vector` 字段准备
- 数据库连接参数配置

如果你使用容器方式，可以参考仓库中的 `docker-compose.yml` 和初始化脚本，但请注意这些内容属于阶段性工程材料，使用前需要结合你的环境自行确认。

### 3. 准备模型

当前主线涉及的模型包括：

- `facebook/dpr-question_encoder-single-nq-base`
- `facebook/dpr-ctx_encoder-single-nq-base`
- `google/flan-t5-base`（baseline）
- `microsoft/Phi-3.5-mini-instruct`（当前主生成器路线）

建议优先采用**本地模型路径**方式，避免因为网络、代理或 SSL 问题导致流程中断。

### 4. 配置知识库与参数

根据你的知识文本准备：

- 原始文档或知识文本
- chunk 参数（如 `mark_200_50`）
- retrieval operator（如 `<#>`）
- top-k
- generator model

### 5. 运行测试

```bash
python -m scripts.test_rag
```

运行前请确保：

- 数据库可连接
- 模型路径有效
- 配置文件中的表名、字段名、连接参数与你本地环境一致

---

## 当前最佳实践结论

基于当前阶段的实验结果，项目主收敛路线如下：

### 1. Chunk 配置

- **默认推荐**：`mark_200_50`
- **边界增强候选**：`mark_200_100`
- **对照组保留**：`mark_150_10`
- **不推荐主路线**：`length` 系列、`mark_100_10`

### 2. Retrieval operator

- **当前主算子**：`<#>`
- **对照算子**：`<=>`
- **当前不推荐主用**：`<->`

在当前 DPR embedding 路线下，`<#>` 与训练目标一致性更强，综合表现最优。

### 3. Embedding 路线

- **当前证据最充分的主路线**：DPR
- Cohere 路线仍保留在后续工作中，但尚未形成同等强度证据

### 4. Generator 路线

- **baseline**：`flan-t5-base`
- **当前主生成器路线**：`Phi-3.5-mini-instruct`

目前主要结论不是“检索层失效”，而是端到端质量瓶颈已经明显转向生成层。相比 `flan-t5-base`，`Phi-3.5-mini-instruct` 在答案正确性、groundedness 与完整性上有显著提升，但生成耗时也明显更高。

### 5. 部署策略

- **推荐**：开发机重处理 + 边缘端最小闭环
- **不推荐当前直接推进**：将重 embedding 与重生成全部塞入 RK3568 板端

---

## 评测说明

当前项目的评测思路强调分层：

### Retrieval Evaluation

- 检索 Top-1 命中率
- 检索 Top-3 命中率

### Generation Evaluation

- 答案正确性
- groundedness / faithfulness
- 答案完整性
- 幻觉

这样做的目的，是避免把生成器问题误判为检索问题，或者反过来把检索缺陷被生成器能力掩盖。

---

## 当前已知限制

- 当前结论主要基于现有知识库与题集，不保证可无条件推广到所有 RAG 任务。
- `<#>` 优于 `<=>` 与 `<->` 的结论，当前主要绑定于 DPR embedding 路线。
- Cohere 路线、BentoML 完整交付、AArch64 最小闭环结果仍待继续补齐。
- gold context 上限测试出现了异常现象，提示当前生成器对 context 的利用方式仍需进一步复测。
- 仓库中的部分 Docker / Compose / BentoML 文件是阶段性工程材料，不能直接视为最终最佳实践配置。

---

## 后续工作

当前更值得优先推进的方向包括：

1. **生成侧异常复测**

   - 重点检查 gold context 条件下的拒答与不完整问题
   - 控制 prompt、chat template、context 组织方式等变量
2. **检索侧收尾实验**

   - 补齐 top-k 收尾对比
   - 进一步细化不同题型在 retrieval 层的表现差异
3. **工程交付补齐**

   - 补全 Cohere 路线证据
   - 完善 BentoML 服务封装
   - 补充边缘端最小闭环验证
   - 进一步整理社区输出材料

---

## 文档与报告

建议在仓库中配套维护以下文档：

- 正式版最佳实践报告
- 面向简历 / 面试的工程总结
- 阶段性评测结果
- 原始输出归档说明
- 文件命名对应关系说明

如果你想快速了解项目结论，优先阅读最佳实践与工程总结；如果你希望复核证据链，再继续查看 `eval` 与 `raw_outputs` 目录中的材料。

---

## 适用场景

本项目更适合作为以下场景的参考：

- openGauss + RAG 的工程验证
- RetrievalQA 参数收敛实验
- 向量数据库与生成模型解耦设计
- CPU 条件下的生成器替换评测
- 面向边缘端的职责拆分与部署判断

---

## License

本项目的 License 可根据后续公开范围与使用方式进一步补充。
