# 病历 Ghost Writer

从检查结果自动生成符合医学逻辑的病程演化路径，把'病历记录'变成'AI剧本'

## 项目简介

病历 Ghost Writer 是一个智能病历生成工具，通过分析检查结果数据，自动生成符合医学逻辑的病程演化路径。它能够：

- **智能分析检查结果**：自动提取关键医学指标和异常值
- **病程演化推断**：基于医学知识库推断症状演化路径
- **规则校验**：内置时间线合理性、药物相互作用、诊断与症状匹配等校验规则
- **多格式输出**：支持 CLI 命令行和 Web 服务两种使用方式
- **多科室模板**：提供内科、外科、急诊科等不同科室的病历模板
- **数据库存储**：支持 SQLite 持久化存储和历史记录管理

## 项目结构

```
medical-record-ghostwriter/
├── cli/              # CLI 命令行工具
│   ├── index.ts      # CLI 入口
│   ├── generate.ts   # 病历生成功能
│   ├── validate.ts   # 规则校验功能
│   ├── template.ts   # 模板管理功能
│   └── database.ts   # 数据库管理功能
├── server/           # Python FastAPI Web 服务
├── data/             # 数据文件和示例
│   └── sample/       # 示例数据集
├── templates/        # 病历模板
├── knowledge/        # 医学知识库
├── db/               # 数据库文件
├── src/              # Node.js 源码
├── tests/            # 测试文件
├── README.md         # 项目说明
└── package.json      # Node.js 项目配置
```

## 快速开始

### 安装依赖

```bash
cd medical-record-ghostwriter
npm install
```

### CLI 使用

```bash
# 查看帮助
npx med-ghost --help

# 生成单个病历
npx med-ghost generate input.json

# 批量生成
npx med-ghost generate batch.json --dry-run -v

# 校验病历记录
npx med-ghost validate output.json

# 查看模板列表
npx med-ghost template list

# 管理数据库
npx med-ghost db list
```

### Web 服务

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload
```

访问 `http://localhost:8000` 使用 Web 界面。

---

## CLI 详细使用文档

### 1. 环境配置（可选）

如果需要使用 LLM 生成能力，可以配置以下环境变量：

```bash
# OpenAI API (默认使用 mock 模式，无需配置)
export OPENAI_API_KEY=your-api-key-here
export OPENAI_BASE_URL=https://api.openai.com/v1

# 国产模型 (兼容 OpenAI 格式)
export LLM_BASE_URL=https://your-model-api.com/v1
export LLM_API_KEY=your-api-key-here
export LLM_MODEL_NAME=qwen-max
```

如果未配置 API Key，系统将自动使用**模拟模式**进行本地规则生成。

---

### 2. 核心命令

#### 2.1 generate - 病历生成命令

从检查结果数据生成完整的病历记录。

```bash
npx med-ghost generate <input> [options]
```

**参数说明：**

| 参数 | 说明 | 类型 |
|------|------|------|
| input | 输入文件路径（JSON 或 CSV） | 必需 |

**选项说明：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-o, --output <dir>` | 输出目录 | `./output` |
| `-t, --template <name>` | 使用的模板名称 | `default` |
| `--dry-run` | 模拟运行，不调用 LLM | `false` |
| `-v, --verbose` | 输出详细日志 | `false` |
| `-d, --debug` | 启用调试模式 | `false` |
| `-q, --quiet` | 静默模式，仅输出错误 | `false` |

**输入文件格式：**

**JSON 格式（单个患者）：**
```json
{
  "patientId": "P001",
  "patientName": "张三",
  "age": 45,
  "gender": "男",
  "chiefComplaint": "胸痛3小时",
  "historyOfPresentIllness": "患者3小时前突发胸痛...",
  "checkResults": {
    "血压": "160/95 mmHg",
    "心率": "98 次/分",
    "心电图": "ST段抬高"
  }
}
```

**JSON 格式（批量）：**
```json
[
  {
    "patientId": "P001",
    "patientName": "张三",
    "age": 45,
    "gender": "男",
    "chiefComplaint": "胸痛3小时",
    "historyOfPresentIllness": "..."
  },
  {
    "patientId": "P002",
    "patientName": "李四",
    "age": 32,
    "gender": "女",
    "chiefComplaint": "发热1天",
    "historyOfPresentIllness": "..."
  }
]
```

**CSV 格式：**
```csv
patientId,patientName,age,gender,chiefComplaint,historyOfPresentIllness,checkResults
P001,张三,45,男,胸痛3小时,患者3小时前突发胸痛...,{"血压":"160/95 mmHg"}
P002,李四,32,女,发热1天,患者1小时前开始发热...,{"体温":"38.5℃"}
```

**使用示例：**

```bash
# 生成单个病历（从文件）
npx med-ghost generate ./data/patients.json

# 批量生成（模拟模式，用于测试）
npx med-ghost generate ./data/batch.json --dry-run -v

# 指定输出目录
npx med-ghost generate ./data/input.json -o ./results

# 使用verbose模式查看详细过程
npx med-ghost generate ./data/patients.json -v
```

**输出说明：**

- 生成的病历保存为 JSON 文件：`record_{patientId}_{timestamp}.json`
- 同时保存患者信息到 SQLite 数据库（`db/medical_records.db`）
- 输出目录自动创建

---

#### 2.2 validate - 规则校验命令

校验病历记录的合规性和逻辑性。

```bash
npx med-ghost validate <input> [options]
```

**参数说明：**

| 参数 | 说明 | 类型 |
|------|------|------|
| input | 输入文件路径 | 必需 |

**选项说明：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-r, --rules <dir>` | 自定义规则目录 | `./rules` |
| `-f, --format <type>` | 输出格式: json\|text | `text` |

**校验规则：**

| 规则代码 | 说明 |
|----------|------|
| TL001-TL004 | 时间线合理性检查（日期、症状演变） |
| MED001-MED003 | 药物相互作用和禁忌症检查 |
| DIA001-DIA004 | 诊断与症状匹配检查 |
| LOG001-LOG006 | 逻辑一致性检查（年龄/性别/生命体征） |

**使用示例：**

```bash
# 文本格式输出（默认）
npx med-ghost validate ./output/record_P001_*.json

# JSON格式输出（用于自动化处理）
npx med-ghost validate ./output/record_P001_*.json -f json

# 使用自定义规则目录
npx med-ghost validate ./input.json -r ./custom-rules
```

**输出示例：**
```
校验文件: ./output/record.json

校验结果:
  有效性: 通过
  得分: 95/100
  问题数: 1

发现的问题:
  1. [警告] 年龄>=65岁，建议调整药物剂量
     位置: 病历记录 - 用药建议

校验完成: 通过
```

---

#### 2.3 template - 模板管理命令

管理病历模板，查看可用的内置模板。

```bash
npx med-ghost template <command>
```

**子命令：**

| 命令 | 说明 |
|------|------|
| `list` | 列出所有可用的病历模板 |
| `show <template-id>` | 显示指定模板的详细信息 |

**list 选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-d, --department <dept>` | 筛选指定科室 | 全部 |
| `-j, --json` | 以JSON格式输出 | `false` |

**show 选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-j, --json` | 以JSON格式输出完整模板 | `false` |

**使用示例：**

```bash
# 列出所有模板（文本格式）
npx med-ghost template list

# 列出内科模板（JSON格式）
npx med-ghost template list -d 内科 -j

# 显示模板详情
npx med-ghost template show INTERNAL_MEDICINE_PNEUMONIA

# 查看完整模板数据（JSON格式）
npx med-ghost template show INTERNAL_MEDICINE_PNEUMONIA -j
```

**支持的科室：**

- 内科（内科、心内科、呼吸科、消化科等）
- 外科（普外科、骨科、神外等）
- 急诊科
- 儿科
- 妇产科
- 耳鼻喉科
- 眼科
- 皮肤科

---

#### 2.4 db - 数据库管理命令

管理 SQLite 数据库，查看和导出病历记录。

```bash
npx med-ghost db <command>
```

**子命令：**

| 命令 | 说明 |
|------|------|
| `list` | 列出病历记录 |
| `search <keyword>` | 搜索病历记录 |
| `export [output]` | 导出数据库为JSON |
| `import <input>` | 从JSON导入数据 |
| `stats` | 显示数据库统计信息 |

**list 选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-p, --patient <id>` | 按患者ID筛选 | 全部 |
| `-l, --limit <num>` | 限制输出数量 | `20` |
| `-o, --offset <num>` | 偏移量 | `0` |
| `-j, --json` | JSON格式输出 | `false` |

**search 选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-p, --patient` | 按患者信息搜索 | `false` |
| `-r, --record` | 按记录内容搜索 | `false` |
| `-j, --json` | JSON格式输出 | `false` |

**使用示例：**

```bash
# 列出所有记录
npx med-ghost db list

# 按患者筛选
npx med-ghost db list -p P001

# 分页查询
npx med-ghost db list -l 10 -o 20

# 搜索关键词
npx med-ghost db search 张三

# 导出数据库
npx med-ghost db export ./backup/medical_records.json

# 查看统计信息
npx med-ghost db stats
```

---

### 3. 常见使用场景

#### 3.1 快速生成测试

```bash
# 使用示例数据快速测试
npx med-ghost generate ./data/sample/internal_medicine_cases.json --dry-run -v
```

#### 3.2 批量处理 HIS 数据

```bash
# 导出 HIS 系统数据为 CSV
npx med-ghost generate ./data/his_export.csv -v

# 校验生成 results
npx med-ghost validate ./output/record_*.json
```

#### 3.3 工作流整合

```bash
# 清理旧输出
rm -rf ./output/*

# 批量生成
npx med-ghost generate ./input/patients.json -o ./output -v

# 校验所有生成的记录
for f in ./output/*.json; do
  npx med-ghost validate "$f" -f json
done
```

#### 3.4 数据备份

```bash
# 导出数据库
npx med-ghost db export ./backup/$(date +%Y%m%d)_records.json
```

---

### 4. 输入文件示例

#### 4.1 单个患者 JSON

```json
{
  "patientId": "IM001",
  "patientName": "王明",
  "age": 58,
  "gender": "男",
  "chiefComplaint": "突发呼吸困难2小时",
  "historyOfPresentIllness": "患者2小时前无明显诱因突发呼吸困难，伴胸痛、大汗...",
  "pastHistory": "高血压病史10年，冠心病史5年",
  "physicalExam": {
    "一般情况": "急性病容，端坐呼吸",
    "生命体征": "T 36.8℃, P 110次/分, R 28次/分, BP 170/100mmHg"
  },
  "checkResults": {
    "血常规": "WBC 12.5×10^9/L, N 85%",
    "心电图": "窦性心动过速，ST段压低",
    "心脏超声": "LVEF 45%，左室扩大",
    "BNP": "850 pg/mL"
  }
}
```

#### 4.2 批量患者 CSV

```csv
patientId,patientName,age,gender,chiefComplaint,historyOfPresentIllness,pastHistory
P001,张三,45,男,胸痛3小时,突发胸痛伴出汗,高血压10年
P002,李四,32,女,发热1天,咳嗽、发热、咽痛,无
P003,王五,67,男,肢体无力2小时,右侧肢体无力,房颤史5年
```

---

### 5. Troubleshooting（故障排除）

#### 5.1 常见错误

**错误：文件不存在**

```
错误: 文件不存在: ./data/input.json
```

**解决方法：**检查文件路径是否正确，使用绝对路径或确保文件在当前目录。

---

**错误：JSON 解析失败**

```
[错误] JSON parsing failed: Unexpected token ... in JSON at position 123
```

**解决方法：**检查输入文件是否为合法 JSON 格式，可以使用在线 JSON 校验工具验证。

---

**错误：数据库已锁定**

```
[错误] database is locked
```

**解决方法：**

1. 等待其他进程完成操作
2. 重启应用
3. 必要时删除 `db/medical_records.db` 重新开始（会丢失历史数据）

---

**错误：模板未找到**

```
错误: 未找到模板 DEFAULT_TEMPLATE
```

**解决方法：**使用 `npx med-ghost template list` 查看可用模板，确认模板ID正确。

---

#### 5.2 调试技巧

**启用调试模式：**
```bash
npx med-ghost generate input.json -d
# 或
npx med-ghost --debug generate input.json
```

**静默模式（仅错误）：**
```bash
npx med-ghost generate input.json -q
```

**使用模拟模式（无API）：**
```bash
npx med-ghost generate input.json --dry-run -v
```

---

#### 5.3 性能优化

| 场景 | 建议 |
|------|------|
| 大批量生成 | 使用 `--dry-run` 进行测试，确认无误后再运行真实生成 |
| CSV 文件 | 确保文件编码为 UTF-8，避免特殊字符 |
| 数据库性能 | 定期导出备份，必要时重建数据库 |

---

### 6. 完整命令参考

```bash
# 基础命令
npx med-ghost help                    # 显示帮助
npx med-ghost --version              # 显示版本号

# 全局选项
npx med-ghost -d [command]           # 启用调试模式
npx med-ghost -q [command]           # 静默模式

# 生成相关
npx med-ghost generate <input>       # 生成病历
npx med-ghost generate --dry-run     # 模拟生成

# 校验相关
npx med-ghost validate <input>       # 校验病历
npx med-ghost validate -f json       # JSON格式输出

# 模板相关
npx med-ghost template list          # 列出模板
npx med-ghost template show <id>     # 显示模板详情

# 数据库相关
npx med-ghost db list                # 列出记录
npx med-ghost db stats               # 统计信息
npx med-ghost db export [file]       # 导出数据
npx med-ghost db search <keyword>    # 搜索记录
```

## Web 服务使用文档

### 1. 服务架构

项目采用双引擎架构：

```
┌─────────────────────────────────────────────────────────┐
│                    Web 服务层                            │
│  ┌─────────────────┐  ┌────────────────────────────────┐ │
│  │  FastAPI 服务   │  │  React 前端界面                │ │
│  │  (Python)       │  │  (Vite + React + Tailwind)   │ │
│  └─────────────────┘  └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                    ↓                              ↓
┌─────────────────────────────────────────────────────────┐
│                    业务逻辑层                            │
│  ┌─────────────────┐  ┌────────────────────────────────┐ │
│  │  CLI 命令行工具  │  │  病历生成核心引擎               │ │
│  │  (Node.js)      │  │  LLM 集成/模拟生成             │ │
│  └─────────────────┘  └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                    ↓                              ↓
┌─────────────────────────────────────────────────────────┐
│                      数据层                              │
│  ┌─────────────────┐  ┌────────────────────────────────┐ │
│  │  SQLite 数据库   │  │  医学知识库 (JSON)             │ │
│  └─────────────────┘  └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2. 启动服务

#### 2.1 环境准备

```bash
cd server

# 安装依赖
pip install -r requirements.txt

# (可选) 配置环境变量
cp .env.example .env
# 编辑 .env 填写 API Key
```

#### 2.2 启动命令

```bash
# 开发模式（热重载）
uvicorn main:app --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000

# 使用 gunicorn (生产环境推荐)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

默认服务运行在 `http://localhost:8000`

### 3. API 文档

启动服务后，访问以下地址查看 API 文档：

| 文档类型 | 地址 | 说明 |
|----------|------|------|
| Swagger UI | `http://localhost:8000/docs` | 交互式 API 文档 |
| ReDoc | `http://localhost:8000/redoc` | 简洁文档视图 |
| JSON Schema | `http://localhost:8000/openapi.json` | OpenAPI 规范 |

#### 3.1 核心端点

**POST /api/generate** - 单个病历生成

请求体：
```json
{
  "patient_id": "P001",
  "patient_name": "张三",
  "age": 45,
  "gender": "男",
  "chief_complaint": "胸痛3小时",
  "present_illness": "患者3小时前突发胸痛...",
  "past_history": "高血压病史10年",
  "record_type": "progress_note",
  "department": "内科",
  "diagnosis": "冠心病"
}
```

响应：
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "pending",
  "created_at": "2026-03-24T10:00:00Z"
}
```

**GET /api/generate/{task_id}** - 查询生成结果

响应：
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "generated_content": "# 病历记录\n...",
  "validation_results": [],
  "has_issues": false,
  "model_used": "simulated",
  "tokens_used": 1250
}
```

**GET /api/generate/{task_id}/content** - 获取生成内容（纯文本）

**GET /api/tasks** - 任务列表（支持分页和状态过滤）

**GET /api/stats** - 统计信息

响应：
```json
{
  "total_tasks": 42,
  "pending": 3,
  "processing": 1,
  "completed": 38,
  "failed": 0,
  "timestamp": "2026-03-24T10:05:00Z"
}
```

**POST /api/generate/batch** - 批量生成

**DELETE /api/generate/{task_id}** - 删除任务

### 4. 数据格式要求

#### 4.1 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patient_id | string | 否 | 患者ID |
| patient_name | string | 否 | 患者姓名 |
| age | integer | 否 | 年龄 |
| gender | string | 否 | 性别 |
| chief_complaint | string | 是 | 主诉 |
| present_illness | string | 是 | 现病史 |
| past_history | string | 否 | 既往史 |
| physical_exam | string | 否 | 体格检查 |
| auxiliary_exams | string | 否 | 辅助检查 |
| record_type | string | 否 | 病历类型：admission/progress_note/discharge_record/emergency_record |
| department | string | 否 | 科室 |
| diagnosis | string | 否 | 诊断 |
| model_name | string | 否 | 使用的AI模型 |
| temperature | float | 否 | 生成温度 (0-1) |
| max_tokens | integer | 否 | 最大token数 |

#### 4.2 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务唯一标识 |
| status | string | 任务状态 (pending/processing/completed/failed) |
| created_at | datetime | 任务创建时间 |
| completed_at | datetime | 任务完成时间 |
| generated_content | string | 生成的病历内容（Markdown格式） |
| validation_results | array | 校验结果列表 |
| has_issues | boolean | 是否有问题 |
| model_used | string | 使用的模型名称 |
| tokens_used | integer | 使用的token数量 |

### 5. 部署说明

#### 5.1 本地部署

```bash
# 克隆或复制项目
cd medical-record-ghostwriter/server

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

#### 5.2 Docker 部署

创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：
```bash
docker build -t medical-record-ghostwriter .
docker run -p 8000:8000 medical-record-ghostwriter
```

#### 5.3 生产环境配置

**环境变量：**

| 变量 | 说明 |
|------|------|
| `LLM_BASE_URL` | LLM API 地址 |
| `LLM_API_KEY` | LLM API 密钥 |
| `LLM_MODEL_NAME` | 使用的模型名称 |

**生产环境启动命令：**
```bash
# 使用 gunicorn（多进程）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 或使用 uvicorn with workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**CORS 配置（生产环境）：**

在 `main.py` 中修改 CORS 允许来源：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # 限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5.4云平台部署

**Render:**
1. 创建 Web Service
2. 选择 Python 项目
3. 设置启动命令：`uvicorn main:app --host 0.0.0.0 --port $PORT`

**Railway:**
1. 新建项目
2. 连接代码仓库
3. 自动检测 Python 项目
4. 配置端口：`8000`

### 6. API 使用示例

#### 6.1 cURL 示例

```bash
# 生成病历
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "张三",
    "age": 45,
    "gender": "男",
    "chief_complaint": "胸痛3小时",
    "present_illness": "患者3小时前突发胸痛...",
    "record_type": "progress_note"
  }'

# 查询结果
curl http://localhost:8000/api/generate/TASK_ID

# 获取生成内容
curl http://localhost:8000/api/generate/TASK_ID/content
```

#### 6.2 Python 示例

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 生成病历
response = requests.post(f"{BASE_URL}/api/generate", json={
    "patient_name": "张三",
    "age": 45,
    "gender": "男",
    "chief_complaint": "胸痛3小时",
    "present_illness": "患者3小时前突发胸痛...",
    "record_type": "progress_note"
})

task = response.json()
task_id = task["task_id"]
print(f"任务ID: {task_id}")

# 轮询结果
while True:
    result = requests.get(f"{BASE_URL}/api/generate/{task_id}").json()
    if result["status"] == "completed":
        print("生成完成！")
        print(result["generated_content"])
        break
    elif result["status"] == "failed":
        print(f"生成失败: {result.get('message')}")
        break
    print(f"当前状态: {result['status']}")
    time.sleep(1)
```

#### 6.3 JavaScript 示例

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function generateMedicalRecord() {
  // 生成病历
  const response = await axios.post(`${BASE_URL}/api/generate`, {
    patient_name: '张三',
    age: 45,
    gender: '男',
    chief_complaint: '胸痛3小时',
    present_illness: '患者3小时前突发胸痛...',
    record_type: 'progress_note'
  });

  const taskId = response.data.task_id;
  console.log('任务ID:', taskId);

  // 轮询结果
  while (true) {
    const result = await axios.get(`${BASE_URL}/api/generate/${taskId}`);
    const status = result.data.status;

    if (status === 'completed') {
      console.log('生成完成！');
      console.log(result.data.generated_content);
      break;
    } else if (status === 'failed') {
      console.log('生成失败:', result.data.message);
      break;
    }

    console.log('当前状态:', status);
    await new Promise(r => setTimeout(r, 1000));
  }
}

generateMedicalRecord();
```

### 7. Web 前端界面

项目提供了配套的 React 前端界面：

```bash
# 启动前端开发服务器
cd ..
npm run web:dev

# 构建前端
npm run web:build
```

前端功能：
- 文件上传（JSON 格式）
- 患者信息展示
- 生成设置（模板选择、科室选择）
- 病历生成模拟
- 结果编辑和预览
- 校验结果展示
- 下载功能

### 8. 故障排除

#### 8.1 常见错误

**错误：端口已被占用**
```
OSError: [Errno 98] Address already in use
```

**解决方法：**
```bash
# 使用不同的端口
uvicorn main:app --port 8001

# 或停止占用端口的进程
lsof -ti:8000 | xargs kill
```

**错误：依赖安装失败**
```
ERROR: Could not find a version that satisfies the requirement ...
```

**解决方法：**
```bash
# 确保 Python 版本 >= 3.9
python --version

# 升级 pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

**错误：CORS 错误**
```
Access to CORS policy: No 'Access-Control-Allow-Origin' ...
```

**解决方法：**检查 `main.py` 中的 CORS 配置，确保允许跨域请求。

#### 8.2 日志调试

```bash
# 启用详细日志
uvicorn main:app --reload --log-level debug

# 查看访问日志
uvicorn main:app --access-log
```

## 技术栈

- **CLI 工具**：Node.js + TypeScript + Commander
- **Web 服务**：Python + FastAPI + SQLite
- **AI 集成**：OpenAI API + ChatGLM/Qwen 等国产模型

## 医学知识库

项目内置了完整的医学知识库：

- **诊断规则**：常见疾病的症状-诊断映射关系
- **药物指南**：药物相互作用、禁忌症知识库
- **病程模式**：典型疾病的病程演化时间线

## 支持作者

如果您觉得这个项目对您有帮助，欢迎打赏支持！
Wechat:gdgdmp
![Buy Me a Coffee](buymeacoffee.png)

**Buy me a coffee (crypto)**

| 币种 | 地址 |
|------|------|
| BTC | `bc1qc0f5tv577z7yt59tw8sqaq3tey98xehy32frzd` |
| ETH / USDT | `0x3b7b6c47491e4778157f0756102f134d05070704` |
| SOL | `6Xuk373zc6x6XWcAAuqvbWW92zabJdCmN3CSwpsVM6sd` |
