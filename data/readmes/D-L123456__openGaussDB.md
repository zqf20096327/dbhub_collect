# OpenGauss 知识智能体

基于openGauss官方教程文档构建的知识智能体，支持RAG问答、SQL练习判题和知识树浏览。

## 架构

- **后端**: FastAPI + Chroma + 华为云ModelArts
- **前端**: Vue 3 + TypeScript + Pinia
- **向量数据库**: Chroma (嵌入式)
- **大模型**: 华为云ModelArts

## 快速启动

### 1. 配置环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填写以下配置：

- `DATABASE_URL`: PostgreSQL连接字符串
- `MODELARTS_API_KEY`: 华为云ModelArts API密钥
- `MODELARTS_BASE_URL`: ModelArts API地址
- `MODELARTS_MODEL`: 模型名称
- `DOCX_DIR`: openGauss教程docx文件所在目录

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 3. 导入知识库数据

```bash
cd backend
DOCX_DIR=/path/to/docx/files python seed.py
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat/sessions` | GET/POST | 对话会话管理 |
| `/api/chat/ask` | POST | 知识问答 |
| `/api/chat/ask/stream` | POST | 流式问答 |
| `/api/sql-practice/questions` | GET | 获取SQL练习题 |
| `/api/sql-practice/submit` | POST | 提交SQL答案 |
| `/api/knowledge-tree/tree` | GET | 获取知识树 |
| `/api/knowledge-tree/search` | POST | 搜索知识点 |
| `/api/admin/ingest` | POST | 导入文档到知识库 |