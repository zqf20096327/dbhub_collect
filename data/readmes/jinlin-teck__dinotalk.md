# DinoTalk · 小恐龙英语冒险岛 🦕✨

> 专为 **7 岁、小学二年级、英语零基础** 小朋友打造的 **AI 情景式英语启蒙 PWA 应用**。  
> 全中文亲切引导 · 绘本点读 · 自然拼读 · 趣味闯关 · AI 小恐龙陪练 · 家庭自托管。

---

## 🌟 为什么适合零基础孩子？

- **看得懂、敢开口**：没有满屏让人畏难的英文菜单！界面采用简体中文引导、大图标绘本卡片与圆润触控按键；AI 对话每轮都会提供 **2~3 个图文提示气泡**，孩子点一下小喇叭就能先慢速听示范，再勇敢张嘴模仿。
- **听 → 拼 → 玩 → 说，四步科学闭环**：每个主题单元依次经过「绘本点读屋 → 自然拼读小站 → 趣味闯关游戏 → AI 情景剧场」，让孩子从输入磨耳朵自然过渡到开口角色扮演。
- **开箱即用，也可自由接入大模型**：即使**不配置任何 API Key**，应用内置的「本地智能情景剧本」也能完整陪孩子玩通全部 10 个关卡；家长在后台填入任意 OpenAI 兼容大模型 Key 后，即刻升级为真正的 AI 外教伙伴！
- **多设备进度共享与隐私安全**：数据保存在本地 SQLite 数据库中，API Key 仅留在服务端不暴露给浏览器；爸爸妈妈用 iPad、手机、电脑打开同一个家庭地址即可同步进度。

---

## 📚 课程内容体系（循序渐进 L0 → L2）

系统内置 L0–L2 三级成长路线，当前版本完整交付 **L0 启蒙岛全部 10 个高频生活单元**（104 个核心生活词、30 句实用短句、全部 26 个字母大小写自然拼读，并从 U2 起逐步加入渐进式 CVC 拼读）：

| 关卡 | 主题名称 | 核心词汇精选 | 目标核心句型 | 自然拼读 | AI 情景剧场任务 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | 你好，新朋友！ | `hello, hi, bye, morning, name, friend, yes, no` | `Hello! I am ...` / `Nice to meet you!` | **S, A, T** | 在阳光码头认识 Dino 并自我介绍 |
| **U2** | 魔法彩虹画板 | `red, blue, yellow, green, orange, pink, purple, black, white, brown` | `It is red.` / `I like blue.` | **P, I, N + CVC** | 帮迷糊小画家找回丢失的彩虹颜色 |
| **U3** | 生日派对数一数 | `one ~ ten, cake, candle` | `I am seven.` / `Seven candles!` | **C, K, E + CVC** | 为小恐龙准备 7 岁生日派对点蜡烛 |
| **U4** | 温暖的恐龙之家 | `mom, dad, sister, brother, grandma, grandpa, baby, big, small` | `This is my mom.` / `I love my dad!` | **H, R, M + CVC** | 翻看恐龙家庭相册认识每位家人 |
| **U5** | 阳光水果店 | `apple, banana, orange, grape, pear, milk, bread, water, eat, drink, hungry, please` | `An apple, please!` / `Thank you!` | **D, G, O + CVC** | 当小顾客在森林水果店挑选零食水果 |
| **U6** | 奇妙动物园 | `cat, dog, bird, fish, rabbit, panda, tiger, elephant, run, swim, fly` | `It's a panda!` / `Look at the dog.` | **U, L, F + CVC** | 在动物园里帮饲养员寻找躲起来的小动物 |
| **U7** | 动一动身体 | `head, eye, nose, mouth, ear, hand, foot, jump, clap, open, close` | `Touch your nose!` / `Clap your hands!` | **B, J, Z + CVC** | 玩“Dino Says”趣味动作指令游戏 |
| **U8** | 整理我的小书包 | `book, pen, pencil, bag, ruler, eraser, desk, teacher, in, on, under` | `I have a pencil.` / `My bag is ready!` | **W, V, Y + CVC** | 上学前清点文具自己整理小书包 |
| **U9** | 小小天气预报员 | `sunny, rainy, cloudy, windy, snowy, sun, cloud, rainbow, hot, cold` | `It's sunny today!` / `Let's play!` | **X, Q + CVC** | 观察窗外天气决定今天出门去哪玩 |
| **U10** | 神奇玩具箱 | `ball, car, doll, robot, kite, bear, happy, fun, sad, sorry` | `This is my robot.` / `Let's share!` | **CVC 拼读大合体** | 在玩具屋邀请好朋友一起分享玩具 |

> 💡 后续规划中的 **L1 探索岛**（日常作息、餐厅点餐、公园游玩等）和 **L2 冒险岛**（故事复述、趣味科普）已在冒险地图中预留进阶路线。

### 其他好玩功能
- **🎁 每日 3 分钟复习宝箱（`/review`）**：根据儿童版间隔重复记忆曲线（SRS）自动抽取快遗忘的单词、字母音和核心句型；题型会随熟练度自动升级（听音选图 → 盲听辨音 → 开口说卡片，拼读在高熟练度下转为盲听辨音），答对即开宝箱领星星。
- **🦕 小恐龙宠物小屋（`/pet`）**：学习赚取的星星可以给小恐龙 Dino 买苹果、草莓、牛奶、蛋糕喂食——大声读出美食英文名还能 **半价投喂**！还能解锁 4 种恐龙肤色和 16 件装扮（小皇冠、魔法帽、红围巾、太阳镜、星光披风、魔法棒等），每关满 4 星还会免费赠送 1 件专属荣誉装扮。
- **💬 和 Dino 自由聊聊（`/chat`）**：内置「问单词怎么说（如“苹果用英语怎么说？”）」「动物猜猜乐」「超短英文故事」等趣味话题。
- **👀 贴心护眼提醒**：支持家长自定义学习护眼间隔（默认 15 分钟），到点温柔弹出休息提示。
- **⏱️ 今日冒险能量条**：首页实时显示今天的学习分钟数与家长设定的每日目标完成度，达标后 Dino 会开心地为你欢呼。

---

## 🚀 快速开始

### 环境要求
- **Node.js `v24` 或更高版本**（使用了 Node 24 内置的 `node:sqlite`，无需额外编译 C++ 原生依赖）
- **pnpm** 包管理器

### 1. 本地开发 / 体验运行

```bash
cd dinotalk
pnpm install
pnpm dev
```

启动成功后，在浏览器访问：`http://localhost:3000`。

### 2. 本地生产模式运行（推荐日常家庭使用）

```bash
cd dinotalk
pnpm build
pnpm start
```

### 3. Docker 一键自托管（推荐 NAS / 家庭服务器）

```bash
cd dinotalk
mkdir -p ./data
docker compose up -d --build
```

- 默认监听 `3000` 端口。
- 孩子的学习进度数据库（`kids.db`）和 TTS 音频缓存（`audio-cache/`）会持久化保存在 `./data` 目录，升级镜像不会丢失记录。
- 容器默认用 UID/GID `1000:1000` 启动。如果数据目录由其他普通用户拥有，在项目的 `.env` 中设置对应的 `DINOTALK_UID` 和 `DINOTALK_GID`。

#### 从以 root 运行的旧镜像升级

旧容器可能以 root 创建了 SQLite 文件。首次升级时，先停止旧容器并备份整个数据目录，再将目录移交给新容器的运行用户。以下命令适用于普通 Linux Docker 部署，请在宿主机终端手动执行。

```bash
docker compose build dinotalk &&
  docker compose stop dinotalk &&
  (umask 077 &&
    docker compose run --rm -T --no-deps --user 0:0 --entrypoint tar dinotalk \
      -C /app/data -czf - . > "$HOME/dinotalk-data-$(date +%Y%m%d-%H%M%S).tar.gz") &&
  docker compose run --rm -T --no-deps --user 0:0 --entrypoint sh dinotalk \
    -c 'chown -hR "$DINOTALK_DATA_OWNER" /app/data' &&
  docker compose up -d --no-build dinotalk
```

启动后，用家长控制台确认旧学习记录仍可读取，再完成一次练习确认可以写入。

---

## 📱 在 iPad / 手机上像原生 App 一样全屏使用（PWA）

1. 让电脑或服务器与 iPad / 手机处于同一家庭 Wi-Fi 下。
2. 在 iPad **Safari**（或安卓 Chrome）地址栏输入 `http://<服务器局域网IP>:3000`。
3. 点击 Safari 顶部/底部的 **「分享」按钮** → 选择 **「添加到主屏幕」**。
4. 之后从桌面图标打开，即可享受**无浏览器地址栏的全屏绘本级体验**！

---

## 👨‍👩‍👧 家长控制台使用指南（`/parent`）

首次点击右上角黑色的 **「🔒 家长」** 按钮时，会引导设置家长密码（至少 4 位字符，服务端加盐哈希存储）；之后进入控制台需输入密码，修改密码时需先验证当前密码，修改成功后旧会话会立即失效。也可在启动前通过 `PARENT_PIN` 环境变量预置初始密码。

进入后台后，可在 **「用户档案与密码」** 页签：
- 新建、编辑或删除多个孩子档案，每位孩子的学习进度、星星、恐龙装扮与对话历史完全独立；
- 查看指定孩子的学习成长报告；
- 修改家长密码。

孩子端首次访问会弹出建档引导（支持直接说出名字），之后可通过顶栏随时切换当前学习的孩子档案。

### 1. 接入外部 AI 大模型（可选）
在 **「AI 大模型设置」** 页签中，点击一键预设即可快速填入接口格式：
- **DeepSeek（深度求索）**：`deepseek-chat`
- **通义千问（阿里云百炼）**：`qwen-plus` / `qwen-turbo`
- **OpenAI / 兼容中转**：`gpt-4o-mini`
- **Google Gemini（OpenAI 兼容端）**：`gemini-2.5-flash`
- **火山引擎豆包（Ark）** / **本地 Ollama（离线免费）** / **自定义接口**

填好 **API Key** 后建议先点 **「测试连接」** 确认畅通，再点 **「保存模型配置」**。  
也可通过复制 `.env.example` 为 `.env.local` 在启动前预设默认环境变量（可在后台随时覆盖）：

```bash
cp .env.example .env.local
```

### 2. 语音设置（TTS 播音与 STT 语音识别）
- **TTS 播音引擎**：
  - **Edge-TTS（默认推荐）**：免费自然的神经童声（默认英文 `en-US-AnaNeural`，中文 `zh-CN-XiaoxiaoNeural`），并在本地自动缓存音频，常用词第二次播放零延迟；若网络暂时不可用，孩子端会自动无感切换为浏览器原生朗读。
  - **OpenAI 兼容语音** / **浏览器原生离线语音**：可按需一键切换。
  - **语速调节**：建议 7 岁零基础先从 **`0.85x`** 开始，熟悉后调回 `0.95x ~ 1.0x`。
  - **中文引导自动朗读**：默认开启。Dino 会先读完英文回复，再温柔朗读中文提示，帮助识字量还在积累的孩子纯靠听觉顺畅互动（可在本页签关闭）。
- **STT 听孩子说话**：
  - **MiniMax 语音识别（国内推荐）**：国内直连、识别准确率高且延迟低，默认接口 `https://api.minimax.cn/v1/speech_to_text`、模型 `asr-1.0`（海外账号可改用 `https://api.minimax.io/v1/speech_to_text`）。前端录音会自动重采样并封装为 16kHz 单声道 WAV 上传，全面兼容电脑浏览器与 iPad Safari PWA，填好 Key 后可点 **「测试语音识别 STT」** 一键测通。
  - **云端 Whisper 接口**：兼容 OpenAI `/v1/audio/transcriptions` 格式（仅官方 `api.openai.com` 强制要求 Key，第三方中转可留空），自带当前单元词库识别偏置。
  - **浏览器原生语音识别**：零配置免费使用，适合桌面端 Chrome / Edge 快速体验。
  - 自由聊天会按话题自动切换识别语言（「问单词」用中文，猜谜/英文对话用英文）。

### 3. 查看学习成长报告
切换到 **「学习成长报告」**，可以直观看到：
- 近 7 天每天学习时长与完成任务数柱状图；
- L0 全部 10 个单元的 4 项环节完成度；
- 词汇、拼读与句型掌握墙，自动区分「⚠️ 重点巩固」与「✅ 稳步掌握」；
- 今晚 1 分钟亲子英语陪读卡（按最近进度自动生成，含 1 句可共读例句）；
- 孩子最近与 AI 小恐龙的真实英文对话文字回顾。

---

## 🛠️ 常用开发与检查命令

```bash
cd dinotalk

pnpm typecheck   # TypeScript 类型检查
pnpm lint        # ESLint 代码检查
pnpm test        # 运行 Vitest 单元测试（SRS、发音评分、STT/WAV、文本清洗、游戏出题、Agent 解析、课程校验、路由安全）
pnpm build       # 构建生产版本
pnpm test:e2e    # 端到端测试（自动构建并在 3100 端口用临时 DATA_DIR 启动服务）
```

> 端到端测试默认使用 `os.tmpdir()/dinotalk-e2e-data` 作为数据目录，不会污染 `./data/kids.db`。若已有服务在运行，可设置 `TEST_BASE_URL` 复用，例如 `TEST_BASE_URL=http://127.0.0.1:3100 pnpm test:e2e`。

### 可选的安全相关环境变量

| 变量 | 作用 |
| :--- | :--- |
| `ALLOWED_ENDPOINT_HOSTS` | 出站白名单，限制 LLM / TTS / STT 可访问的域名，支持 `.home.arpa` 后缀匹配 |
| `BLOCK_PRIVATE_ENDPOINTS=1` | 禁止访问内网与回环地址（默认允许，便于连接本机 Ollama / 局域网中转） |
| `ALLOWED_HOSTS` | 入站 Host 白名单（含端口），缓解 DNS rebinding；设置后请包含你实际访问的地址 |
| `TRUST_PROXY_HEADERS=1` | 使用受信反向代理写入的 `X-Real-IP` 做按 IP 限流。仅在代理覆盖该请求头且客户端不能直连应用时开启。默认使用共享限流额度 |
| `SESSION_SECRET` | 家长会话签名密钥；不填会自动生成并保存在 `data/.session-secret` |
| `PARENT_PIN` | 首次初始化数据库时预置家长密码（至少 4 位字符）；不填则在首次进入 `/parent` 时引导设置 |

---

## ❓ 常见问题（FAQ）

**Q：启动时提示 `Cannot find module 'node:sqlite'` 怎么办？**  
A：请确认当前 Node.js 版本为 **`v24.0.0` 及以上**（`node -v` 查看）。本项目利用 Node 24 原生内置的 `node:sqlite`，彻底摆脱了原生 C++ 插件编译问题。

**Q：没有申请任何大模型 API Key 能用吗？**  
A：完全可以！应用内置了覆盖全部 10 个主题情景的本地智能剧本，点读、拼读、闯关游戏、复习宝箱、宠物小屋和情景剧场都能正常跑通。等以后准备好了 Key，随时到家长后台填入即可解锁自由对话。

**Q：孩子害羞不敢对着麦克风说话，或浏览器麦克风不可用怎么办？**  
A：在绘本点读和 AI 情景剧场中，孩子既可以对着麦克风开口说，也可以直接点击底部的「提示气泡」先慢速听一遍再点击发送完成互动，不会卡关。

**Q：如何备份孩子的学习进度？**  
A：直接备份 `dinotalk/data/kids.db` 文件即可（音频缓存目录 `dinotalk/data/audio-cache/` 可按需重新生成，无需刻意备份）。
