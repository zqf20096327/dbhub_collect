# OceanBase 多模态沙发咨询助手

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OceanBase](https://img.shields.io/badge/OceanBase-Vector%20Database-green.svg)](https://www.oceanbase.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-AI%20Workflow-purple.svg)](https://langchain-ai.github.io/langgraph/)

🚀 **基于 OceanBase 向量数据库的智能沙发咨询系统**

这是一个展示 OceanBase 向量数据库与多模态混合检索能力的完整Demo，通过智能对话为用户提供个性化的沙发产品推荐服务。

## ✨ 主要功能

- **🗄️ 向量存储**: OceanBase 多模态向量数据存储和高效索引
- **🔍 混合检索**: 支持文本、图像及文图混合的跨模态相似度搜索
- **🤖 智能对话**: 基于 LangGraph 的多轮对话AI工作流
- **🎯 意图识别**: 自动识别用户意图（产品推荐、详情咨询、普通聊天）
- **💡 智能推荐**: 条件提取 + 个性化产品推荐
- **�️ 图片搜索**: 上传图片找相似产品
- **⚡ 流式回复**: 实时流式AI响应提升用户体验
- **🌐 双界面**: Web UI (Streamlit) + 命令行界面

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/pingcy/oceanbase-multimodal-demo.git
cd oceanbase-multimodal-demo

# 安装依赖
uv venv
source .venv/bin/activate  
uv pip install -e .
```

### 2. 配置环境

复制并编辑环境配置：

```bash
cp .env.example .env
```

配置 OceanBase 和 API 信息：

```bash
# OceanBase 向量数据库配置
OB_URL="your-oceanbase-url"
OB_USER="your-username"  
OB_DB_NAME="your-database-name"
OB_PWD="your-password"

# 通义千问 API 配置
DASHSCOPE_API_KEY="your-dashscope-api-key"
```

### 3. 验证环境

```bash
# 验证配置是否正确
python test_environment.py
```

### 4. 初始化数据库

```bash
# 创建表结构并插入测试数据
python init_database.py
```

⚠️ **注意**: 初始化脚本包含演示用的测试数据，请根据实际需求修改 `init_database.py` 中的数据内容。

### 5. 启动系统

#### 🚀 快速启动（推荐）

```bash
# 启动 Web 界面（Streamlit UI）
./startui.sh

# 启动命令行界面
./startcli.sh
```

启动脚本会自动：

- ✅ 检查并激活虚拟环境
- 📦 安装必要的依赖包
- 🚀 启动对应的应用程序

#### 📱 手动启动

```bash
# Web 界面方式（推荐）
streamlit run chat_ui.py

# 命令行方式
python chat_cli.py
```

## 🏗️ 系统架构

### AI 工作流程图

系统基于 **LangGraph** 构建的智能对话工作流：

1. **意图分析** → 自动识别用户意图类型
2. **条件提取** → 从用户输入提取产品筛选条件
3. **智能检索** → 多模态向量搜索匹配产品
4. **个性化推荐** → 生成专业的产品推荐回复

### 核心技术栈

- **数据库**: OceanBase 向量数据库
- **AI框架**: LangGraph + LangChain
- **LLM**: 通义千问 (Qwen-Plus)
- **Web框架**: Streamlit
- **向量化**: 通义千问多模态embedding
- **工作流**: 异步流式处理

## 📊 数据说明

系统包含两个主要数据表：

- **sofa_demo_v2**: 产品主表，存储沙发产品信息和多模态向量数据
- **sofa_product_docs**: 产品文档表，支持产品详细信息的语义检索

测试数据包含 5 个精选沙发产品样本，涵盖不同风格、材质和价位，可根据实际业务需求扩展为其他类型产品。

详细的数据库初始化说明请参考：[数据库初始化文档](DATABASE_INIT.md)

## 📁 项目结构

```
oceanbase-demo/
├── chat_ui.py              # Streamlit Web 界面
├── chat_cli.py             # 命令行界面  
├── startui.sh              # Web UI 启动脚本
├── startcli.sh             # CLI 启动脚本
├── init_database.py        # 数据库初始化脚本
├── conversation_agent_flow.md  # AI工作流程图
├── srd/                    # 核心源码目录
│   ├── agents/            # AI智能体
│   │   └── conversation_agent.py  # 对话智能体
│   ├── llm/               # LLM接口
│   ├── tools/             # 工具类
│   │   └── retrieval_tool.py  # 检索工具
│   └── prompt/            # 提示词模板
└── temp_images/           # 临时图片存储
```

## 🎯 使用场景

- **产品推荐**: "我想要一个北欧风格的三人沙发，预算5000左右"
- **图片搜索**: 上传喜欢的沙发图片，找相似产品
- **产品详情**: "这个沙发的材质怎么样？保修政策是什么？"
- **对比咨询**: "能帮我对比一下这几款沙发的优缺点吗？"

## 🔧 系统要求

- Python 3.10+
- OceanBase 数据库（支持向量功能）
- 通义千问 API 访问权限

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

## � 关注我们

如果这个项目对您有帮助，欢迎关注我的微信公众号获取更多技术分享：

<div align="center">
  <img src="images/qrcode_1m.jpg" alt="微信公众号" width="200">
  <p><em>扫码关注微信公众号，获取最新技术文章和项目更新</em></p>
</div>

## �📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

💡 **这是一个 OceanBase 向量数据库能力的完整演示项目，展示了多模态AI应用在电商推荐场景的技术实现。**

🔗 **相关链接**:

- [OceanBase 向量数据库文档](https://www.oceanbase.com/docs)
- [通义千问 API 文档](https://help.aliyun.com/zh/dashscope/)
- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
