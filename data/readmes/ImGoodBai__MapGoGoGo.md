# 点亮挑战 (MapGoGoGo)

把现实城市变成一场可以分享的地图挑战。

MapGoGoGo 是一个 H5 地图点亮应用：发起人勾选一个真实地图区域，生成挑战链接；参与者用手机打开后在范围内走动，经过的地图格子会被点亮，大家一起把学校、公园、街区、商圈或城市地标点亮出来。

适合用来做校园打卡、公园跑步、城市漫游、商圈活动、线下社群挑战，也可以作为「现实地图 + 轻游戏 + 分享传播」产品方向的原型。

线上体验：[https://map.suishouai.cn/](https://map.suishouai.cn/)

## 功能亮点

- 创建地图挑战：搜索学校、公园、街区、商场，也可以用当前位置或直接在地图上选点。
- 自定义挑战范围：设置半径、挑战时长和格子大小。
- 手机 GPS 点亮：参与者走到挑战区域内，经过的格子会被真实记录。
- 地图遮罩效果：未点亮区域覆盖一层遮罩，走过后露出地图，进度直观。
- 挑战榜：查看参与人数、点亮进度和每个参与者贡献。
- 分享传播：挑战列表和挑战页都可以复制分享文案。
- 桌面测试器：电脑上可以模拟移动，方便快速预览玩法效果。
- 基础管理页：查看挑战数量、参与人数、点亮来源和挑战列表。

## 怎么玩

1. 打开首页，选择一个已有挑战，或者点击「发起挑战」创建新的地图区域。
2. 创建挑战时，搜索真实地点，调整半径和挑战时长，发布后得到挑战链接。
3. 把链接发给朋友、同学或社群成员。
4. 参与者用手机系统浏览器打开链接，允许定位后开始点亮。
5. 在挑战范围内走动，地图会按经过的位置逐步点亮。
6. 打开挑战信息面板，可以查看进度、数据和挑战榜。

注意：真实 GPS 点亮需要手机系统浏览器和 HTTPS。微信内置浏览器更适合传播和预览，正式点亮建议从微信右上角选择用系统浏览器打开。

## 截图

### 首页和挑战列表

![首页和挑战列表](docs/images/home.png)

### 发起挑战

![发起挑战](docs/images/create-challenge.png)

### 桌面测试器

![桌面测试器](docs/images/desktop-simulator.png)

### 管理页

![管理页](docs/images/admin.png)

## 本地运行

准备 Python 和 Node.js 环境后，在项目根目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
npm run build
cd ..

cp .env.example .env
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

打开：

- 应用：http://127.0.0.1:8000
- API 健康检查：http://127.0.0.1:8000/api/health

开发前端时可以单独运行：

```bash
cd frontend
npm run dev
```

Vite 会把 `/api` 代理到 `http://127.0.0.1:8000`。

## 高德地图配置

真实地图需要高德开放平台的 Web 端 JS API Key：

1. 打开 [高德开放平台控制台](https://console.amap.com/dev/key/app)。
2. 创建应用。
3. 添加 Key，服务平台选择 `Web端(JS API)`。
4. 复制 Key 和安全密钥。
5. 写入 `.env`。

```bash
AMAP_KEY=你的Key
AMAP_SECURITY_CODE=你的安全密钥
```

没有配置高德 Key 时，项目仍可以运行，会进入模拟地图模式；创建挑战、排行榜、管理页等流程都可以测试。

## 手机定位说明

桌面端适合创建、查看和本地模拟。真实 GPS 点亮请用手机系统浏览器打开 HTTPS 地址。

iPhone Safari 如果点击开始后显示 `User denied Geolocation`，通常是系统或站点定位权限已经被关闭。可以按下面顺序检查：

1. iPhone「设置」->「隐私与安全性」->「定位服务」确认总开关已开启。
2. iPhone「设置」->「Safari」->「位置」确认不是拒绝。
3. Safari 打开站点后，在地址栏左侧 `aA` / 网站设置里检查位置权限。
4. 刷新页面后重新点击开始。
5. 如果从微信打开，先用右上角菜单在 Safari 中打开。

## 技术栈

- 前端：React、Vite、TypeScript、高德地图 JS API、H3 六边形网格。
- 后端：Python、FastAPI、SQLite。
- 定位：浏览器 Geolocation API，服务端做坐标转换、范围判断、去重和进度统计。
- 部署：Nginx + systemd，HTTPS 域名承载手机 GPS 体验。

SQLite 适合当前原型和小规模内测。后续如果出现高并发点亮、多人同时写入卡顿或后台查询变慢，可以迁移到 PostgreSQL。

## 测试

```bash
.venv/bin/python -m pytest
cd frontend
npm run typecheck
npm run build
```

## 当前边界

- 当前模式是多人一起完成同一个地图挑战。
- 桌面测试器只做本地预览，不保存到服务器，也不进入挑战榜。
- H5 不承诺锁屏或切到后台后继续记录，挑战时请保持页面在前台。
- 默认只允许真实 GPS 点亮；手动测试点亮接口需要显式打开服务端配置。
