# RAG-TIDB #
该项目整合springAI、ollama和tidb实现了一个简易的RAG，包括对文档分块后embedding保存数据库，然后在聊天接口中，自动根据用户问题语义搜索关联文档，作为上下文进行辅助回答。

该项目主要侧重简单rag的实现和tidb向量库的实际应用。

## java版本
 jdk17

## 技术栈
- [x] 微服务架构：springboot
- [x] AI框架：[springAI](https://docs.spring.io/spring-ai/reference/index.html)
- [x] ORM框架：mybatis
- [x] 模型部署工具：[ollama](https://ollama.com/)
- [x] 大语言模型：[qwen3:14b](https://ollama.com/library/qwen3:14b)
- [x] embedding模型：[bge-large-zh-v1.5:f32](https://ollama.com/quentinz/bge-large-zh-v1.5)
- [x] 文档分块服务：[unstructured-api](https://github.com/Unstructured-IO/unstructured-api)
- [x] 关系数据存储和向量存储：[tidb](https://docs.pingcap.com/zh/)
