<div align="center">

# 🌾 智慧农业一体化管理平台

**Smart Agriculture Platform · YOLO11 病虫害识别 + 全链路农业业务管理 + 大模型农技问答**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](./LICENSE)
[![Vue 3](https://img.shields.io/badge/Vue-3.2-42b883.svg?style=flat-square&logo=vue.js)](./frontend)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9-3178c6.svg?style=flat-square&logo=typescript)](./frontend)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.3.7-6DB33F.svg?style=flat-square&logo=springboot)](./backend)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat-square&logo=python)](./ai-service)
[![YOLO11](https://img.shields.io/badge/Ultralytics-YOLO11-042AFF.svg?style=flat-square)](./ai-service)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](./CONTRIBUTING.md)

</div>

---

## 一句话定位

> 上传一张叶片照片，3 秒内告诉你这是什么病、怎么治 —— 并把识别结果、温室环境、农资库存和农技问答串成一套能跑通的完整农业管理系统。

---

## 为什么要做这个项目

| 传统农业生产的痛点 | 本项目如何解决 |
| :--- | :--- |
| 病虫害靠肉眼看、凭经验判断，误判成本高 | YOLO11 目标检测模型自动定位病斑并给出置信度，覆盖 9 类作物 |
| 识别完就结束，结果没有沉淀 | 图片 / 视频 / 摄像头三类识别结果自动落库，形成可追溯的历史记录 |
| 知道病名，但不知道怎么防治 | 内置 100 条病害知识库，症状、病因、防治方法一应俱全 |
| 环境数据、农资、温室各管各的，信息割裂 | 统一平台打通温室、环境、采购、库存与数据大屏 |
| 遇到疑难杂症找不到人问 | 接入智谱 GLM 大模型，支持 Markdown 渲染的农技问答 |

---

## ✨ 核心特性

### 🔬 病虫害智能识别
- **三种识别模式**：图片识别、视频识别、摄像头实时识别（Socket.IO 实时回传处理进度）
- **9 类作物模型**：玉米、水稻、小麦、马铃薯、番茄、棉花、苹果、葡萄、草莓，可热切换权重文件
- **置信度可调**：滑动条实时调整阈值，低于阈值时给出明确提示而非静默失败
- **结果可视化**：自动标注病斑位置并回传标注图，同时展示耗时与置信度

### 📚 病虫害知识库
- 内置 **100 条** 常见病虫害条目，每条包含中文名称、作物类型、症状描述、发病原因、防治方法与示意图
- 支持按名称 / 作物类型组合检索，支持后台增删改与图片上传

### 🗂️ 识别记录追溯
- 图片、视频、摄像头三类记录独立管理，含所用模型、置信度、操作人、时间与结果文件
- 支持分页查询、详情查看与删除

### 🏡 温室与环境管理
- 温室信息与作物信息管理；环境监测页展示环境指标
- 接入和风天气实时天气；环境数据可交由 GLM 做智能分析与建议

### 📊 数据大屏
- 基于 ECharts 的农业数据可视化大屏，含图表、滚动列表等组件

### 📦 农资管理
- 采购管理与库存管理两套完整的 CRUD 流程，支持分页与条件查询

### 🤖 智能农技助手
- 基于智谱 GLM 的农业问答，Markdown 渲染 + 打字机效果
- 在识别结果页直接追问"这病怎么治"，上下文衔接

### 👤 用户与权限
- 登录、注册、角色路由控制（管理员 / 普通用户）、个人中心、头像上传、用户管理

---

## 🛠️ 技术栈

<table>
<tr>
<td width="33%" valign="top">

**前端** `frontend/`
- Vue 3.2 + TypeScript 4.9
- Vite 4
- Element Plus 2.2
- Pinia 2 + Vue Router 4
- ECharts 5
- Axios + Socket.IO Client
- Tailwind CSS 3 + vue-i18n 9

</td>
<td width="33%" valign="top">

**业务后端** `backend/`
- Spring Boot 2.3.7
- MyBatis-Plus 3.4.2
- MySQL 8
- Hutool 5.7
- Fastjson 1.2.83
- RESTful API + 文件上传

</td>
<td width="33%" valign="top">

**AI 服务** `ai-service/`
- Flask 2.3 + Flask-SocketIO
- Ultralytics YOLO11
- OpenCV 4.8
- Socket.IO 实时推送
- ffmpeg（视频/摄像头链路）

</td>
</tr>
</table>

---

## 📸 效果展示

> 截图与演示 GIF 放置于 [`docs/images/`](./docs/images) 目录。

| 模块 | 预览 |
| :--- | :--- |
| 图片识别 | `docs/images/img-predict.png` |
| 视频 / 摄像头识别 | `docs/images/video-predict.png` |
| 病虫害知识库 | `docs/images/disease-library.png` |
| 数据大屏 | `docs/images/data-view.png` |
| 智能助手 | `docs/images/smart-chat.png` |

<!-- 建议补充：在仓库根目录放置一张 demo.gif，并在下方引用 -->

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本要求 |
| :--- | :--- |
| Node.js | >= 16 |
| JDK | 1.8 |
| Maven | 3.6+ |
| Python | 3.8 ~ 3.11 |
| MySQL | 8.0+ |
| ffmpeg | 任意版本（视频 / 摄像头识别需要，需加入 PATH） |

### 1️⃣ 初始化数据库

```bash
# 方式一：命令行导入
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS cropdisease DEFAULT CHARSET utf8mb4;"
mysql -u root -p cropdisease < database/cropdisease.sql

# 方式二：使用脚本（Windows PowerShell）
.\scripts\init-db.ps1 -User root -Password yourpassword
```

数据库初始化脚本内置演示数据：

- 病虫害知识库 **100** 条
- 温室信息 **63** 条
- 图片识别记录 **634** 条
- 采购 / 库存记录各 **40** 条
- 演示账号：`admin / admin`（管理员）、`user / user`（普通用户）

> ⚠️ 演示账号仅用于本地体验，**部署到公网前请务必修改默认密码**。

### 2️⃣ 启动 AI 服务（Python）

```bash
cd ai-service
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 模型权重放入 ai-service/weights/ 目录（见下方"模型权重"说明）
python main.py                     # 默认监听 0.0.0.0:5000
```

### 3️⃣ 启动业务后端（Spring Boot）

```bash
cd backend

# 通过环境变量注入数据库配置（推荐）
export DB_USERNAME=root
export DB_PASSWORD=yourpassword
export WEATHER_API_KEY=your_qweather_key   # 可选，不配置则天气功能返回 503

mvn spring-boot:run                # 默认监听 :9999
```

### 4️⃣ 启动前端（Vue 3）

```bash
cd frontend
cp .env.example .env.development   # 按需修改
npm install
npm run dev                        # 默认监听 :8100
```

打开 <http://localhost:8100> 即可访问。开发环境下 `/api` 与 `/flask` 请求由 Vite 代理转发到后端 9999 与 AI 服务 5000，无需额外配置。

### 5️⃣ 一键脚本（可选）

```bash
./scripts/dev.sh          # macOS / Linux：串行拉起三个服务
```

---

## 📖 基础用法

### 图片识别（HTTP）

```bash
# 1. 上传图片，拿到可访问 URL
curl -X POST http://localhost:9999/files/upload \
  -F "file=@samples/test-images/玉米/corn_rust.jpg"

# 响应：{"code":"0","data":"http://localhost:9999/files/xxxx_xxx.jpg"}

# 2. 调用识别接口（后端会转发到 AI 服务并把结果落库）
curl -X POST http://localhost:9999/flask/predict \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "weight": "corn_best.pt",
    "conf": "0.45",
    "kind": "corn",
    "inputImg": "http://localhost:9999/files/xxxx_xxx.jpg",
    "startTime": "2026-01-01 10:00:00"
  }'

# 响应节选：
# {"code":0,"message":"预测成功","outImg":"...","allTime":"0.312秒",
#  "confidence":"[0.87]","label":"[\"Rust(玉米锈病)\"]"}
```

### 直接调用 AI 服务

```bash
curl -X POST http://localhost:5000/predictImg \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","weight":"tomato_best.pt","conf":"0.4",
       "kind":"tomato","inputImg":"/abs/path/to/leaf.jpg","startTime":"2026-01-01 10:00:00"}'
```

### 查询可用模型

```bash
curl http://localhost:5000/file_names
# {"weight_items":[{"value":"corn_best.pt","label":"corn_best.pt"}, ...]}
```

### 前端调用示例

```ts
import { UPLOAD_URL, AI_BASE_URL } from '/@/config';

// 文件上传地址（已按环境自动切换）
console.log(UPLOAD_URL); // 开发环境 -> /api/files/upload

// 调用识别
const res = await request.post(`${AI_BASE_URL}/predict`, {
  username: 'admin',
  weight: 'corn_best.pt',
  conf: '0.45',
  kind: 'corn',
  inputImg: imageUrl,
  startTime: formatDate(new Date()),
});
```

> 所有接口地址统一从 `frontend/src/config/index.ts` 读取，部署时只需配置
> `VITE_API_DOMAIN` / `VITE_AI_DOMAIN` / `VITE_AI_WS_URL` 三个环境变量。

---

## 📁 目录说明

```text
.
├── frontend/                 # 前端（Vue 3 + TypeScript + Vite）
│   ├── src/
│   │   ├── api/              # 接口封装
│   │   ├── components/       # 通用组件（表格、图标选择器、通知栏等）
│   │   ├── config/           # ★ 全局接口地址配置（环境变量集中入口）
│   │   ├── i18n/             # 国际化语言包
│   │   ├── layout/           # 布局（导航、标签页、面包屑、锁屏等）
│   │   ├── router/           # 路由（含前端/后端路由与权限控制）
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── theme/            # 主题与全局样式
│   │   ├── utils/            # 工具方法（请求、Socket、存储等）
│   │   └── views/            # 业务页面（识别、知识库、温室、大屏、问答等）
│   ├── public/               # 静态资源
│   ├── .env.example          # 环境变量模板
│   └── vite.config.ts        # Vite 配置（含 /api、/flask 代理）
│
├── backend/                  # 业务后端（Spring Boot + MyBatis-Plus）
│   └── src/main/java/com/example/Ece/
│       ├── common/           # 统一响应体、CORS 与 MyBatis-Plus 配置
│       ├── controller/       # REST 控制器（用户、病害、温室、记录、采购、库存…）
│       ├── entity/           # 数据实体
│       ├── mapper/           # MyBatis Mapper
│       └── dto/              # 数据传输对象
│   └── src/main/resources/application.properties   # 配置（敏感项走环境变量）
│
├── ai-service/               # AI 推理服务（Flask + YOLO11 + Socket.IO）
│   ├── main.py               # 服务入口：图片 / 视频 / 摄像头识别与 WebSocket
│   ├── predict/              # 推理逻辑与作物类别映射
│   ├── weights/              # 模型权重（不入库，见"模型权重"）
│   ├── train.py              # 训练脚本示例
│   └── yolo11.yaml           # YOLO11 模型结构定义
│
├── database/                 # 数据库脚本
│   └── cropdisease.sql       # 建表 + 演示数据
│
├── docs/                     # 文档
│   ├── architecture.md       # 系统架构说明
│   ├── api.md                # 接口文档
│   ├── deployment.md         # 部署指南
│   ├── ui-design.md          # UI/UX 设计规范
│   ├── frontend-optimization.md  # 前端优化记录
│   ├── images/               # 截图与演示素材
│   └── manual/               # 原始交付文档（.docx，不入库）
│
├── scripts/                  # 运维脚本
│   ├── init-db.sh / .ps1     # 数据库初始化
│   ├── download-weights.sh   # 模型权重下载（需自备来源）
│   └── dev.sh                # 一键启动开发环境
│
├── samples/                  # 示例素材
│   └── test-images/          # 各作物测试图片（不入库）
│
├── CONTRIBUTING.md           # 贡献指南
├── CHANGELOG.md              # 变更记录
├── LICENSE                   # MIT 开源协议
└── README.md
```

---

## 🧠 模型权重

仓库**不包含**模型权重文件（`*.pt`，共约 60 MB），请自行准备：

1. 使用 `scripts/download-weights.sh` 从你自己的模型存储地址拉取；
2. 或将自训练权重直接放入 `ai-service/weights/`，命名保持 `<crop>_best.pt`。

支持的作物与权重文件对应关系：

| 权重文件 | 作物 | `kind` 参数 | 可识别类别数 |
| :--- | :--- | :--- | :--- |
| `corn_best.pt` | 玉米 | `corn` | 7 |
| `rice_best.pt` | 水稻 | `rice` | 8 |
| `wheat_best.pt` | 小麦 | `wheat` | 8 |
| `potato_best.pt` | 马铃薯 | `potato` | 3 |
| `tomato_best.pt` | 番茄 | `tomato` | 12 |
| `cotton_best.pt` | 棉花 | `cotton` | 5 |
| `apple_best.pt` | 苹果 | `apple` | 4 |
| `grape_best.pt` | 葡萄 | `grape` | 5 |
| `strawberry_best.pt` | 草莓 | `strawberry` | 7 |

自行训练可参考 `ai-service/train.py`：

```bash
cd ai-service
python train.py    # 默认读取 ./dataset/corn_dataset/data.yaml，20 epochs
```

---

## ⚙️ 环境变量

### 前端 `frontend/.env.development`

| 变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `VITE_PORT` | 开发服务器端口 | `8100` |
| `VITE_API_DOMAIN` | 后端地址（留空走 `/api` 代理） | 空 |
| `VITE_AI_DOMAIN` | AI 服务地址（留空走 `/flask` 代理） | 空 |
| `VITE_AI_WS_URL` | Socket.IO 直连地址 | `http://localhost:5000` |
| `VITE_GLM_API_KEY` | 智谱 GLM Key（智能助手 / 环境分析） | 空 |

### 后端环境变量

| 变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `DB_URL` | MySQL 连接串 | `jdbc:mysql://localhost:3306/cropdisease` |
| `DB_USERNAME` / `DB_PASSWORD` | 数据库账号密码 | `root` / `changeit` |
| `SERVER_PORT` | 服务端口 | `9999` |
| `FILE_UPLOAD_DIR` | 上传文件目录 | `files` |
| `AI_SERVICE_URL` | AI 服务地址 | `http://localhost:5000` |
| `WEATHER_API_KEY` | 和风天气 Key（[申请](https://dev.qweather.com/)） | 空 |

### AI 服务环境变量

| 变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `BACKEND_URL` | 回传结果的后端地址 | `http://localhost:9999` |
| `AI_HOST` / `AI_PORT` | 监听地址与端口 | `0.0.0.0` / `5000` |

---

## 🗺️ 路线图

- [ ] Docker Compose 一键编排三端 + MySQL
- [ ] 识别结果与知识库条目自动关联，给出防治建议直达
- [ ] 支持自定义训练与模型上传（前端管理界面）
- [ ] 引入时序数据库存储环境监测历史数据
- [ ] 移动端适配
- [ ] 单元测试与 CI 流水线

欢迎认领以上任务，详见 [贡献指南](./CONTRIBUTING.md)。

---

## 🤝 贡献指南

我们欢迎任何形式的贡献：提 Issue、改文档、修 Bug、加功能。

请先阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)，了解分支约定、提交信息规范与本地开发流程。

提交 PR 前请确保：

```bash
cd frontend && npm run lint-fix     # 前端代码规范
```

---

## 📄 开源协议

本项目基于 [MIT License](./LICENSE) 开源。

- 前端部分基于 [vue-next-admin](https://gitee.com/lyt-top/vue-next-admin) 模板二次开发，遵循其 MIT 协议。
- AI 服务使用 [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics)，其遵循 AGPL-3.0；**若用于商业用途，请注意该协议的合规要求**。
- 模型权重与训练数据集的版权归各自来源所有。

---

## 🙏 致谢

- [Ultralytics](https://github.com/ultralytics/ultralytics) —— YOLO11 推理框架
- [Vue.js](https://vuejs.org/) / [Element Plus](https://element-plus.org/) —— 前端基础设施
- [Spring Boot](https://spring.io/projects/spring-boot) / [MyBatis-Plus](https://baomidou.com/) —— 后端基础设施
- [智谱 GLM](https://open.bigmodel.cn/) —— 大模型问答能力
- [和风天气](https://dev.qweather.com/) —— 天气数据

---

<div align="center">

如果这个项目对你有帮助，欢迎点个 ⭐ Star 支持一下！

</div>
