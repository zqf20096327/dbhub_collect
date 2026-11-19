# 彩票分析与推荐平台

基于 **Vue3 + Express + SQLite** 的彩票分析平台,支持**双色球**与**大乐透**两个彩种:历史数据同步、冷热/遗漏走势分析、多策略号码推荐、统计报告。

> ⚠️ 所有分析与推荐仅基于历史数据统计,不构成任何投注建议,请理性购彩。

## 功能一览

| 模块 | 说明 |
|---|---|
| 首页 | 两彩种最新一期开奖展示、快速入口 |
| 历史数据 | 官方开奖数据同步、分页浏览、手动录入、删除 |
| 走势分析 | 红/蓝球走势热力图(出现显示号码,未出显示遗漏期数)、遗漏 TOP10 |
| 智能推荐 | 三种策略(均衡分布 / 热号加权 / 冷号回补)+ 和值/奇偶/连号过滤 |
| 统计报告 | 和值分布、奇偶比、大小比、区间分布、连号比例 |

## 快速开始

要求 Node.js ≥ 18、Python ≥ 3.10。

```bash
# 1. 安装依赖(根目录、server、web)
npm install
npm install --prefix server
npm install --prefix web

# 2. 安装 AI 服务依赖(PyTorch CPU + FastAPI,约 500MB,仅需一次)
python -m venv ml/.venv
ml/.venv/Scripts/python.exe -m pip install --index-url https://download.pytorch.org/whl/cpu torch
ml/.venv/Scripts/python.exe -m pip install fastapi uvicorn numpy

# 3. 开发模式(同时启动 server 3001 + web 5173 + ml 5001)
npm run dev
# 打开 http://localhost:5173,进入「🤖 AI 预测」页训练模型

# 4. 生产模式(前端构建产物由后端单端口托管;AI 服务需另行启动:npm run ml)
npm run build
npm start
# 打开 http://localhost:3001
```

首次启动时,若数据库为空会自动尝试从官方接口(福彩官网 / 体彩网)抓取最近 1000 期开奖数据;接口不可达时自动写入内置示例数据并标记「示例数据」,之后可在「历史数据」页点击「同步最新数据」重试。

## 项目结构

```
├── package.json            # 根:concurrently 一键启动脚本
├── ml/                     # Python AI 服务 (FastAPI, 端口 5001)
│   ├── app.py              # 训练/预测/回测/状态 API
│   ├── lottery_lstm.py     # LSTM 模型、数据集构建、walk-forward 回测、概率选号过滤
│   └── models/             # 训练产物(*.pt + meta.json)
├── server/                 # Express 后端 (端口 3001)
│   └── src/
│       ├── index.js        # 入口
│       ├── config.js       # 彩种元信息与官方接口地址
│       ├── db.js           # better-sqlite3 数据访问层
│       ├── data/seed.js    # 离线示例数据
│       ├── services/       # syncService / analysisService / recommendService / dlService
│       └── routes/api.js   # REST API
└── web/                    # Vue3 前端 (Vite)
    └── src/
        ├── api/index.js    # API 封装
        ├── components/     # Ball / BallGroup / Chart / LotteryTabs
        └── views/          # 首页 / 历史 / 走势 / 推荐 / 报告
```

## API 一览(前缀 `/api`)

- `GET /meta`、`GET /latest`
- `GET /draws?lottery=ssq&page=1&size=30`、`POST /draws/sync`、`POST /draws`、`DELETE /draws/:id`
- `GET /analysis/overview?lottery=ssq&periods=30`
- `GET /analysis/trend?lottery=ssq&periods=30`
- `GET /report?lottery=ssq&periods=100`
- `GET /recommend?lottery=ssq&strategy=balanced|hot|cold&count=5&periods=30`
- `GET /dl/status?lottery=ssq`、`POST /dl/train {lottery}`、`GET /dl/predict?lottery=ssq&count=5`、`POST /dl/backtest {lottery, points, epochs}`(经 Node 代理到 Python 服务)
- `GET /draws/export?lottery=ssq` — 导出 CSV(带 BOM,Excel 兼容)

## 推荐策略说明

- **均衡分布**:温号权重最高,和值不过于极端,奇偶/大小比例均衡,最多一组连号
- **热号加权**:近 N 期高频号码加权随机
- **冷号回补**:低频次(高遗漏)号码加权随机

## 自动机制

- **定时同步**:server 每 30 分钟检查一次,开奖日(双色球 周二/四/日、大乐透 周一/三/六)21:40 后自动抓取新数据
- **自动核对**:同步到新一期开奖后,自动核对所有待开奖的预测与投注,计算命中与奖级
- **自动重训**:同步到有新数据时,自动重新训练 LSTM 模型(AI 服务运行时)

## 深度学习模型说明

- **输入**:近 10 期开奖号码的 multi-hot 向量序列(红球 + 蓝球拼接)
- **网络**:2 层 LSTM(hidden=64)+ 全连接 + Sigmoid,多标签 BCE 损失,Adam 优化,验证集早停
- **输出**:下一期每个号码的出现概率;推荐号码按概率加权采样,再经和值/奇偶/大小/连号过滤
- **训练**:每次训练前自动同步最近 1000 期官方数据(双色球已支持近 1000 期);模型与指标持久化在 `ml/models/`,CPU 上约 2 秒
- **回测**:walk-forward 方式对最近 20 期逐期重训并预测,对比 TOP-K 命中率与随机基准,诚实评估模型有效性
- **注意**:摇奖是独立随机事件,实测回测命中与随机基准相当,模型学习的是历史分布特征,无法真正预测未来,请理性看待
