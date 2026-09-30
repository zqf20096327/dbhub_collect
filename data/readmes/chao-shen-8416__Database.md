# 手势传感器数据 OpenGauss 管理系统

这是一个围绕 `data_raw.csv` 构建的数据库课程项目，包含前端、后端、OpenGauss 数据库、CSV 导入、增删改查、查询统计、录制样本管理和 DeepSeek 大模型加分模块。

## 技术栈

- 数据库：OpenGauss，Docker 容器部署
- 后端：Python FastAPI
- 前端：原生 HTML/CSS/JavaScript
- 大模型：DeepSeek 自然语言查询助手，可通过环境变量配置

## 数据建模

CSV 一共有 104610 行、77 列。系统将 `worker`、`v`、`label`、`active_hand`、`sample_id`、`timestamp/ms`、`frame_id`、`hand_type` 作为可查询元数据列，其余传感器字段保存到 `sensor_data` JSONB 字段中，便于完整保留原始数据。

## 启动步骤

1. 启动 OpenGauss：

```powershell
docker compose -p gesturedb up -d
```

本项目使用 `enmotech/opengauss:3.1.1` 镜像。

2. 安装后端依赖：

```powershell
python -m pip install -r requirements.txt
```

3. 初始化数据库并导入 CSV：

```powershell
python backend/import_csv.py --csv data_raw.csv --reset
```

4. 启动后端和前端：

```powershell
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

浏览器打开：

```text
http://127.0.0.1:8000
```

## DeepSeek 配置

复制 `.env.example` 为 `.env`，填写 `DEEPSEEK_API_KEY`。前端“大模型查询”会把中文问题转换成安全的筛选条件，只允许查询本系统开放的字段，不会让模型直接执行任意 SQL。

## 主要功能

- 数据列表分页
- 按人员、标签、手型、速度、样本编号、关键字查询
- 新增、编辑、删除记录
- 数据集统计：总记录数、标签分布、人员分布、手型分布
- DeepSeek：中文自然语言查询转结构化筛选条件

