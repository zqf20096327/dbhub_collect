# 基于 openGauss DB4AI 的智慧零售用户行为分析与商品推荐系统

本项目基于 H&M Personalized Fashion Recommendations 结构化数据集，使用 FastAPI + Vue3 + openGauss 构建本地可运行的智慧零售分析、DB4AI 建模与推荐系统。

系统不使用商品图片，只使用 `articles.csv`、`customers.csv`、`transactions_train.csv` 或 `transactions_small.csv`。

## 项目结构

```text
hm-retail-db4ai/
├── backend/     # FastAPI、openGauss、SQL、导入与建模脚本
├── frontend/    # Vue3 + Vite + Element Plus + ECharts
└── README.md
```

当前 `.env.example` 默认读取仓库同级的 `dataset/` 目录：

```text
project/
├── dataset/
│   ├── articles.csv
│   ├── customers.csv
│   └── transactions_train.csv
└── hm-retail-db4ai/
```

## 后端运行

```bash
cd hm-retail-db4ai/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

编辑 `.env`，填写 openGauss 密码。后端远程业务用户使用 `smartcare_app`，不要使用 `omm`。

```env
OPENGAUSS_HOST=your_opengauss_host
OPENGAUSS_PORT=5432
OPENGAUSS_DB=customer_service_db
OPENGAUSS_USER=your_app_user
OPENGAUSS_PASSWORD=填写你的密码
OPENGAUSS_SSLMODE=disable
```

初始化表结构：

```bash
python scripts/init_db.py
```

如果没有 `transactions_small.csv`，建议先生成小样本：

```bash
python scripts/create_small_transactions.py ^
  --input ../../dataset/transactions_train.csv ^
  --output ../../dataset/transactions_small.csv ^
  --recent-days 60 ^
  --top-customers 50000
```

导入 CSV：

```bash
python scripts/import_csv.py
```

构建特征表：

```bash
python scripts/build_features.py
```

启动 API：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档：

```text
http://localhost:8000/docs
```

## 前端运行

```bash
cd hm-retail-db4ai/frontend
npm install
npm run dev
```

访问：

```text
http://localhost:5173
```

## 主要功能

- 数据导入：初始化 openGauss 表、导入 articles/customers/transactions。
- Dashboard：交易数、客户数、商品数、销售趋势、渠道占比、热销商品。
- 用户行为分析：年龄、会员状态、消费金额、购买次数和高价值用户。
- 商品分析：商品大类、颜色、部门、销量排行和热度结果。
- DB4AI 任务：
  - 用户价值分群
  - 用户复购预测
  - 商品大类偏好预测
  - 用户未来消费金额预测
  - 商品热度预测
- 推荐系统：结合复购概率、偏好大类、商品热度和近期热销生成 Top 12 推荐。
- 系统检查：openGauss 连接、表行数、CSV 状态、DB4AI/fallback 状态和模型记录。

## DB4AI 与 fallback

`backend/app/sql/04_db4ai_templates.sql` 中集中放置 DB4AI SQL 模板。后端执行建模任务时会优先尝试 openGauss DB4AI SQL。

由于不同 openGauss 版本的 DB4AI 语法和可用算法可能存在差异，如果 DB4AI SQL 执行失败，系统会自动切换到 sklearn fallback，并将预测结果写回 openGauss 结果表。每次训练都会写入 `db4ai_model_record`，其中 `is_fallback` 标识模型来源。

## 数据库连接注意事项

- 后端远程连接用户使用 `smartcare_app`。
- 不要使用 `omm` 做远程业务连接。
- `article_id` 和 `customer_id` 均按字符串导入，避免前导 0 丢失。
- 如果 TCP 通但连接失败，优先检查 openGauss 日志、`pg_hba.conf`、安全组和业务用户权限。
- 推荐只对本地公网 IP `/32` 开放 5432。

## 常用接口

```text
GET  /api/system/check
POST /api/import/init-schema
POST /api/import/articles
POST /api/import/customers
POST /api/import/transactions
POST /api/features/build-customer-features
POST /api/features/build-article-features
POST /api/db4ai/customer-clustering
POST /api/db4ai/repurchase-prediction
POST /api/db4ai/preference-prediction
POST /api/db4ai/spend-prediction
POST /api/db4ai/article-hotness-prediction
POST /api/recommendation/generate
GET  /api/recommendation/customer/{customer_id}
```

## 项目说明

本系统以 H&M 真实匿名零售交易数据为基础，将客户、商品和交易数据导入 openGauss 数据库。系统通过 SQL 构造用户画像特征和商品热度特征，并围绕用户价值分群、复购预测、商品偏好预测、未来消费金额预测和商品热度预测五个任务使用 DB4AI 进行建模。预测结果直接回写 openGauss，由前端管理端进行可视化展示。系统不依赖商品图片，而是突出结构化零售数据在数据库内部完成分析、训练、预测和业务决策的能力。


