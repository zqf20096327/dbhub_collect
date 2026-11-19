# 猫球约 · 校园 AI 约球平台（monorepo）

Vue3 + Element Plus 前端 ｜ FastAPI + TiDB 后端（Vercel Serverless 部署）

```
.
├── campus_ball/     # 后端：FastAPI + SQLAlchemy 2.0(async) + MySQL/TiDB
└── frontend/        # 前端：Vue3 + Vite + Element Plus（响应式）
```

## 一分钟了解

| 能力 | 说明 |
| --- | --- |
| 认证 | bcrypt 密码 + JWT 双令牌 + 认证中间件（路由前置统一鉴权） |
| 球局 | 发起（场地/时间冲突校验）、列表（筛选分页 + 匹配分）、详情、报名、退出、候补补位 |
| 签到核销 | 发起人给到场用户核销，**触发惰性结算**（+2 / 迟到 -3） |
| 小黑屋 | 缺席 -10 分；缺席即封禁 3 天；封禁期拦发局/报名，查询与签到放行；**到期惰性自动解封**；连续缺席顺延不叠加 |
| AI 信誉画像 | 签到/缺席/退出触发重算；DeepSeek 优先，无 Key **自动降级本地加权规则版**；个人主页展示信誉分与标签；画像分驱动球局匹配参考分 |

## 快速开始（本地）

```bash
# 后端
cd campus_ball
python -m venv .venv && .venv\Scripts\activate      # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                              # 填 MySQL/TiDB 连接串与 JWT 密钥
mysql -uroot -p < sql/001_schema.sql                # TiDB 用户请用 sql/tidb/001_schema.sql
uvicorn app.main:app --reload                       # → http://127.0.0.1:8000/docs

# 前端
cd ../frontend
npm install
npm run dev                                         # → http://localhost:5173（默认 mock 模式，可离线预览）
```

## 部署（Vercel 双项目 + TiDB Cloud Serverless）

- 后端：Root Directory = `campus_ball`，入口 `api/index.py`（Mangum），见 `campus_ball/vercel.json`
- 前端：Root Directory = `frontend`，构建产物 `dist/`
- 完整步骤、环境变量清单、常见问题：**[campus_ball/docs/DEPLOY_VERCEL_TIDB.md](campus_ball/docs/DEPLOY_VERCEL_TIDB.md)**

## 文档索引

| 文档 | 内容 |
| --- | --- |
| [campus_ball/docs/DEPLOY_VERCEL_TIDB.md](campus_ball/docs/DEPLOY_VERCEL_TIDB.md) | Vercel + TiDB 部署、环境变量清单、Cron 与惰性策略说明 |
| [campus_ball/docs/E2E_TEST_CASES.md](campus_ball/docs/E2E_TEST_CASES.md) | 33 个端到端用例与执行状态 |
| [campus_ball/docs/API_AUTH.md](campus_ball/docs/API_AUTH.md) | 认证模块接口文档 |
| [campus_ball/docs/API_GAME.md](campus_ball/docs/API_GAME.md) | 球局核心业务接口文档 |
| [campus_ball/docs/API_BLACKLIST.md](campus_ball/docs/API_BLACKLIST.md) | 小黑屋规则与接口文档 |
| [campus_ball/docs/API_AI_PROFILE.md](campus_ball/docs/API_AI_PROFILE.md) | AI 信誉画像算法说明与接口文档 |
| [frontend/README.md](frontend/README.md) | 前端结构、设计稿还原说明、截图清单、Vercel 配置 |

## 演示账号（来自 `sql/tidb/002_init_data.sql`）

| 学号 | 昵称 | 密码 | 状态 |
| --- | --- | --- | --- |
| `20230001` | 球场小王子 | `123456` | 正常（信誉分 100） |
| `20230002` | 羽毛球爱好者 | `123456` | 正常（信誉分 92，有 1 次迟到） |
| `20230003` | 鸽王本王 | `123456` | **封禁中**（信誉分 55，可验证 403 拦截与解禁倒计时） |

## 测试

```bash
cd campus_ball && python -m pytest -q          # 110 个用例（无需数据库）
python scripts/e2e_check.py --base http://127.0.0.1:8000/api/v1   # 真实 HTTP 端到端
```
