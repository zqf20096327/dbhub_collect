<p align="center">
  <a href="#宣传片">
    <img src="docs/media/banner-poster.jpg" alt="Velvet Hold'em" width="100%" />
  </a>
</p>

<div align="center">

<p>
  <strong>简体中文</strong> &nbsp;|&nbsp; <a href="README.en.md">English</a>
</p>

<h3>把私人德州俱乐部的克制质感，搬进浏览器</h3>

<p>
  <a href="#宣传片">宣传片</a> &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#一局流程">一局流程</a> &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#核心亮点">核心亮点</a> &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#博弈与教学思路">博弈思路</a> &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#快速体验">快速体验</a> &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#合规说明">合规说明</a>
</p>

<p>
  <img src="https://img.shields.io/badge/3D_Salon-WebGL_%2B_2D_Fallback-D4A853?style=flat-square&labelColor=0B0E10" alt="3D Salon" />
  <img src="https://img.shields.io/badge/Poker_AI-GTO_%2B_Safe_Exploit-1E6B4B?style=flat-square&labelColor=0B0E10" alt="GTO + Safe Exploit" />
  <img src="https://img.shields.io/badge/Runtime-CPU_Only_(No_GPU)-2A332E?style=flat-square&labelColor=0B0E10" alt="CPU Only" />
  <img src="https://img.shields.io/badge/Docker-One_Click_Deploy-2496ED?style=flat-square&labelColor=0B0E10" alt="Docker Ready" />
  <img src="https://img.shields.io/badge/License-PolyForm_Noncommercial_1.0.0-2A332E?style=flat-square&labelColor=0B0E10" alt="PolyForm Noncommercial 1.0.0" />
</p>

<br />

<p>
  为亲友约局与个人德扑进阶打造的 3D 实时多人无上限德州扑克。<br />
  没有花哨廉价的棋牌弹窗，也没有含糊其辞的简化规则——围绕「<strong>打开即入局，久玩不累眼，打完有长进</strong>」打磨每一处体验。
</p>

</div>

<br />

## 宣传片

<p align="center">
  <img src="docs/media/promo.webp" alt="Velvet Hold'em 完整 1 分钟实机宣传片（Three.js 3D 渲染 + 实机对局）" width="100%" />
  <br />
  <sub>
    完整 65 秒实机宣传片（真彩动态 WebP 主页直播） · 需要 1080p 含爵士 BGM 与物理筹码原声版请
    <a href="https://github.com/jianghao-jianghao-jianghao/newHoldem/raw/main/docs/media/promo.mp4"><strong>直接下载 / 播放原片（MP4）</strong></a>
  </sub>
</p>

<br />

<table>
  <tr>
    <td width="25%" valign="top">
      <strong>克制的 3D 俱乐部质感</strong><br />
      <sub>低饱和绿绒牌桌、胡桃木包边、立体筹码堆叠与双视角切换，移动端或无 3D 环境自动无缝回退 2D。</sub>
    </td>
    <td width="25%" valign="top">
      <strong>严谨规则与懂适应的陪练</strong><br />
      <sub>完整遵循 WSOP / TDA 多级边池与短全下规则；陪练会基于 GTO 基准并随牌桌样本动态调整反制策略。</sub>
    </td>
    <td width="25%" valign="top">
      <strong>局后复盘与个人打法画像</strong><br />
      <sub>13×13 策略矩阵、逐街 EV 损益评级、对手漏损剥削推演与六维性格雷达，边打边学。</sub>
    </td>
    <td width="25%" valign="top">
      <strong>零门槛开局 · 纯 CPU 部署</strong><br />
      <sub>游客免登录即可建桌约局；邮箱验证码跨端同步战绩与成就；普通电脑或轻量服务器一键启动，无需显卡。</sub>
    </td>
  </tr>
</table>

<p align="center">
  <img src="docs/media/hero-table.jpg" alt="Velvet Hold'em 3D 丝绒牌桌主界面" width="100%" />
  <br />
  <sub>桌面端 3D 绿绒实景牌桌 · 移动端或低配环境自动回退至 2D 牌桌</sub>
</p>

<p align="center"><img src="docs/media/divider.svg" alt="" width="76%" /></p>

## 一局流程

从牌室入座、视角切换、全押摊牌到闲聊复盘，六段实录动图呈现完整一局的交互节奏：

<table>
  <tr>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-join.gif" alt="进大厅入座" width="100%" /><br />
      <strong>01 · 进厅入座</strong><br />
      <sub>3D 牌室大厅浏览在线桌，免登录一键入局</sub>
    </td>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-camera.gif" alt="双视角切换" width="100%" /><br />
      <strong>02 · 双视角切换</strong><br />
      <sub>经典 45° 与 90° 全局俯瞰平滑过渡</sub>
    </td>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-allin.gif" alt="全押与赢池特效" width="100%" /><br />
      <strong>03 · 全押打击</strong><br />
      <sub>光刃冲击波、筹码溅射与成就解锁</sub>
    </td>
  </tr>
  <tr>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-showdown.gif" alt="全下摊牌" width="100%" /><br />
      <strong>04 · 全下摊牌</strong><br />
      <sub>全员全下自动发牌，多级边池结算</sub>
    </td>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-chat.gif" alt="牌桌闲聊" width="100%" /><br />
      <strong>05 · 沙龙闲聊</strong><br />
      <sub>表情短语合一，AI 陪练自然接话</sub>
    </td>
    <td width="33.3%" align="center" valign="top">
      <img src="docs/media/flow-analytics.gif" alt="账簿与复盘" width="100%" /><br />
      <strong>06 · 账簿复盘</strong><br />
      <sub>策略矩阵、漏损推演与手牌回放</sub>
    </td>
  </tr>
</table>

<p align="center"><img src="docs/media/divider.svg" alt="" width="76%" /></p>

## 核心亮点

<table>
  <tr>
    <td width="58%" align="center" valign="middle">
      <img src="docs/media/allin-burst.jpg" alt="ALL-IN 打击光刃与筹码溅射" width="100%" />
    </td>
    <td width="42%" valign="middle">
      <h4>克制牌桌质感 × 打击动效与物理声效</h4>
      <p>低饱和祖母绿绒面搭配胡桃木包边与黄铜饰钉，高对比度原创双头 <code>J / Q / K</code> 宫廷牌面与 <code>D / SB / BB</code> 指示物清晰耐看。</p>
      <p>全押与赢池时在头像上方呈现动态光刃、双层冲击波与立体筹码喷泉；每次下注按筹码面值实时合成不同质感的物理碰撞声，按 <kbd>M</kbd> 一键静音音效与轻爵士 BGM。</p>
    </td>
  </tr>
  <tr>
    <td width="42%" valign="middle">
      <h4>严谨德扑规则 × 教学级复盘工作台</h4>
      <p>完整支持 2–10 人桌、多人全下多级边池、超额未跟注退还、中途离桌死钱守恒、短全下不重开加注（Rule 47），以及局间补码与出局重买。</p>
      <p>打完即可打开复盘工作台：查看每一街的决策质量与期望损益、在 <strong>13×13 手牌策略矩阵</strong> 中对照均衡频率、用 <strong>Node-Lock</strong> 推演针对不同对手漏损的调整方向，把“凭感觉打牌”变成可验证的直觉。</p>
    </td>
    <td width="58%" align="center" valign="middle">
      <img src="docs/media/showdown.jpg" alt="摊牌亮牌与动态段位光环" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="58%" align="center" valign="middle">
      <img src="docs/media/profile-achievements.jpg" alt="30 枚荣誉与趣事勋章陈列" width="100%" />
    </td>
    <td width="42%" valign="middle">
      <h4>30 枚趣味勋章 × 玩家性格雷达 × 无门槛约局</h4>
      <p>不登录就能直接开房约局或人机练牌；需要跨设备保存战绩时，点击右上角通过<strong>邮箱验证码</strong>登录即可同步个人中心，登录前游客期解锁的成就也会自动合并。</p>
      <p>个人中心根据真实牌局生成<strong>六维打法雷达</strong>（入池活跃、翻前主动、翻后进攻、持续施压、摊牌胜率、决策纪律）与针对性改进建议；勋章馆收录 <strong>30 枚</strong>经典德扑荣誉与牌桌彩蛋，头像外圈随青铜至钻石段位实时流转光环。</p>
    </td>
  </tr>
</table>

<br />

<p align="center">
  <img src="docs/media/analytics-panels.jpg" alt="牌局账簿与复盘面板" width="100%" />
  <br />
  <sub>牌局账簿与复盘 · 局内排行 · 筹码走势 · 分街底池 · 六维雷达与对手观察 · 13×13 策略矩阵与剥削推演</sub>
</p>

<table>
  <tr>
    <td width="50%" align="center">
      <img src="docs/media/topdown.jpg" alt="俯瞰全局视角" width="100%" /><br />
      <sub>俯瞰全局视角 · 立体筹码柱与盲位指示物</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/media/card-showcase.png" alt="原创宫廷牌面图鉴" width="100%" /><br />
      <sub>原创双头宫廷人像与内置牌型速查图鉴</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/media/chat.jpg" alt="牌桌闲聊" width="100%" /><br />
      <sub>极简沙龙闲聊 · 表情与快捷短语合一</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/media/lobby.jpg" alt="3D 牌室大厅" width="100%" /><br />
      <sub>3D 牌室大厅 · 自定义盲注与房号邀约</sub>
    </td>
  </tr>
</table>

<details>
<summary>查看更多实机截图（赢池成就弹窗 · 俱乐部徽章与形象定制）</summary>

<br />

<table>
  <tr>
    <td width="50%" align="center">
      <img src="docs/media/win-achievement.jpg" alt="赢池结算与成就解锁通知" width="100%" /><br />
      <sub>赢池飘字与右上角成就解锁通知</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/media/profile-avatar.jpg" alt="形象设置与俱乐部徽章" width="100%" /><br />
      <sub>7 款俱乐部徽章与自定义头像上传</sub>
    </td>
  </tr>
</table>

</details>

<p align="center"><img src="docs/media/divider.svg" alt="" width="76%" /></p>

## 博弈与教学思路

市面上大多数开源德扑项目要么只做到随机出牌的“玩具陪练”，要么重度依赖离线求解器与显卡算力。Velvet Hold'em 的核心设计思路是把**均衡底线、动态剥削、复盘闭环与轻量化运行**放到同一张牌桌上：

- **以 GTO 均衡作为防线**：陪练具备 6 人桌 / 单挑位置意识、短码推弃纪律、牌面范围/坚果优势判断、阻断牌选择与几何下注思维，避免机械跟注或无脑全下。
- **小样本保守、大样本精准剥削**：参考不完全信息博弈中的 **Restricted Nash Response（受限纳什应对）** 与贝叶斯先验收缩思想——刚入桌时陪练贴近均衡防止被钓鱼，随着牌局样本累积，自动识别过度弃牌、跟注站、疯狂偷鸡、高频持续下注等倾向并平滑切入针对性反制。
- **从“打完就忘”到“每局有反馈”**：对局中自动沉淀手牌证据，局后直接以 13×13 策略热力图、EV 损益评级和六维性格雷达呈现短板；支持按需接入外部大模型提供中文教练点评与牌桌互动，不配置密钥也能完整离线体验。
- **纯 CPU 轻量优先**：所有核心博弈计算、复盘求解与数据持久化都在普通 CPU 上毫秒级完成，个人电脑与低配云主机均可流畅运行，不把 GPU 当作前提条件。

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/media/architecture-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="docs/media/architecture-light.svg" />
    <img src="docs/media/architecture-dark.svg" alt="Velvet Hold'em 系统架构图" width="100%" />
  </picture>
  <br />
  <sub>
    面向开发者与 AI Agent 的英文架构文档、模块说明及开发规范请移步
    <a href="docs/ARCHITECTURE.md"><strong>Architecture Guide</strong></a> 与
    <a href="docs/DEVELOPER_GUIDE.md"><strong>Developer Handbook</strong></a>
  </sub>
</p>

<p align="center"><img src="docs/media/divider.svg" alt="" width="76%" /></p>

## 快速体验

<table>
  <tr>
    <td width="50%" valign="top">
      <strong>Docker Compose（推荐 · 纯 CPU）</strong><br />
      <sub>一条命令完成构建、启动与本地数据持久化</sub>
      <pre lang="bash">git clone https://github.com/jianghao-jianghao-jianghao/newHoldem.git
cd newHoldem
cp .env.example .env
docker compose up -d --build</pre>
    </td>
    <td width="50%" valign="top">
      <strong>本地直接运行（Node.js &gt;= 22.5）</strong><br />
      <sub>零配置启动完整多人牌桌、陪练与复盘功能</sub>
      <pre lang="bash">git clone https://github.com/jianghao-jianghao-jianghao/newHoldem.git
cd newHoldem
npm install
npm run dev</pre>
    </td>
  </tr>
</table>

启动后浏览器打开 `http://localhost:3000` 即可直接入座或创建私人房间。

<br />

**快捷键与手势**（聊天输入或弹窗打开时自动暂停）：

<p>
  <kbd>F</kbd> 弃牌 &nbsp;·&nbsp;
  <kbd>C</kbd> / <kbd>Space</kbd> 让牌或跟注 &nbsp;·&nbsp;
  <kbd>R</kbd> 下注 / 加注 &nbsp;·&nbsp;
  <kbd>N</kbd> / <kbd>Enter</kbd> 下一局 &nbsp;·&nbsp;
  <kbd>T</kbd> 闲聊 &nbsp;·&nbsp;
  <kbd>M</kbd> 静音音效与配乐 &nbsp;·&nbsp;
  <kbd>Esc</kbd> 关闭面板 &nbsp;·&nbsp;
  <strong>单击头像</strong> 查看档案与勋章 &nbsp;·&nbsp;
  <strong>双击对手</strong> 轻敲提醒
</p>

<details>
<summary>可选配置说明（邮箱发信 / AI 教练 / 公网反代）</summary>

<br />

默认不填任何密钥即可完整游玩、建桌与复盘；如需启用真实邮箱登录或大模型教练，复制 `.env.example` 为 `.env` 按需填写即可：

- **真实邮箱验证码登录**：配置 `SMTP_*`（支持 QQ 邮箱等标准 SMTP）或 `RESEND_API_KEY`。
- **AI 性格画像 / 教练点评 / 陪练聊天**：配置 `DEEPSEEK_API_KEY` 或 `GEMINI_API_KEY`（二选一或同时配置均可）。
- **公网 HTTPS / WSS 部署**：参考 [deploy/nginx.conf.example](deploy/nginx.conf.example)，并在 `.env` 中设置 `TRUST_PROXY=1` 与随机长串 `AUTH_SESSION_SECRET`。
- **Windows + WSL2 Docker 提示**：可在 `C:\Users\<用户名>\.wslconfig` 的 `[wsl2]` 下增加 `vmIdleTimeout=-1`，避免 WSL2 闲置休眠导致本地端口断开。

</details>

<p align="center"><img src="docs/media/divider.svg" alt="" width="76%" /></p>

## 合规说明

本项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE)（**仅限非商业用途**），专为软件工程学习、博弈算法研究与亲友免费娱乐打造。所有筹码与积分均为无货币价值的虚拟演练数值，不含任何支付、充值、提现或抽水通道；**严禁用于任何商业营利、赌博或违法用途**，违规部署与使用后果自负。

完整条款请参阅 [合规与免责声明（DISCLAIMER.md）](DISCLAIMER.md)。

<br />

<div align="center">
  <sub>Licensed under <a href="LICENSE">PolyForm Noncommercial 1.0.0</a> · <a href="DISCLAIMER.md">合规与免责声明</a> · Velvet Hold'em</sub>
</div>
