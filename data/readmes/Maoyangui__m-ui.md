<p align="center"><img src="brand/logo.svg" width="130" alt="m-ui"></p>
<h1 align="center">m-ui</h1>
<p align="center">内嵌 <a href="https://github.com/SagerNet/sing-box">sing-box</a> 的控制面,面向自托管与多服务器部署 · 一个 Go 二进制 · 线路代替 inbound/outbound/route · 每次应用先干跑、失败即回滚 · 一台主机管所有副机</p>
<p align="center"><sub>m-ui · <a href="https://github.com/Maoyangui">Maoyangui</a> 的 sing-box 面板 · Go · Linux · GPL-3.0 —— 与其它同名 “m-ui” 项目无关</sub></p>
<p align="center"><b>中文</b> · <a href="README.en.md">English</a> · <a href="https://maoyangui.github.io/m-ui/zh/">文档站</a> · <a href="https://maoyangui.github.io/m-ui/demo/">在线演示</a> · <a href="#架构">架构</a> · <a href="https://github.com/Maoyangui/m-ui/releases">下载</a></p>
<p align="center">
  <a href="https://github.com/Maoyangui/m-ui/actions/workflows/ci.yml"><img src="https://github.com/Maoyangui/m-ui/actions/workflows/ci.yml/badge.svg" alt="tests"></a>
  <a href="https://github.com/Maoyangui/m-ui/actions/workflows/install-test.yml"><img src="https://github.com/Maoyangui/m-ui/actions/workflows/install-test.yml/badge.svg" alt="install smoke test"></a>
  <a href="https://github.com/Maoyangui/m-ui/releases/latest"><img src="https://img.shields.io/github/v/release/Maoyangui/m-ui?label=release" alt="latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Maoyangui/m-ui" alt="GPL-3.0"></a>
</p>

---

**一行安装**(Debian / Ubuntu,root 运行):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Maoyangui/m-ui/main/deploy/install.sh)
```

装完打开 `http://<服务器IP>:2053/app/`,默认账号 `admin / admin`(登录后到「管理员」页改掉)。**没有域名也能用**:一键自签证书 → 建线路 → 建用户 → 把订阅发出去,五分钟内完成。详见 [安装](#安装) 与 [快速上手](#快速上手)。

**先看看再装?** [在线演示](https://maoyangui.github.io/m-ui/demo/) 就是真实的面板界面跑在示例数据上:不用登录、没有后端,随便点,刷新即恢复。安装命令后面加 `--dry-run` 可以先看它会写哪些文件。

**不想自己搭建?** 直接[选购节点](https://godusevpn.org/subscription/),装上客户端就能用。

**赞助商** <sub>广告</sub> · TikTok 广告户:Telegram [@a88321](https://t.me/a88321)

<p align="center"><img src="docs/screenshots/dashboard.png" alt="m-ui 概览:流量走势、数据面状态、在线用户与流量排行" width="960"></p>

## 这是什么

m-ui 是一个自托管的代理面板:**一个二进制 + 一个数据库文件**,sing-box 直接内嵌其中。线路、用户、订阅、证书、备份、多台服务器,全在网页里管。

和常见面板的四点不同:

- **一条线路就是一件事** —— 入口协议 + 端口 → 从哪出去。不用再分别维护入站、出站、路由三张表。
- **保存不怕改错** —— 整份配置先交给 sing-box 干跑,过不了就进不了库;改用户、改上游是热更新,只有改线路才重启数据面,新配置万一起不来(比如端口被同机别的程序抢走)会自动回滚到上一份。
- **一主多副,主机挂了有备用顶上** —— 主机把线路、用户推给任意多台副机,收回流量、统一判定配额;订阅里每条线路按服务器各出一个节点,客户端自己挑延迟低的入口。开了主机容灾,主机宕机时备用带着加密的数据副本接任,订阅地址可以不变。
- **运维不用回终端** —— 证书签发续期、Cloudflare WARP、内核调优、备份还原、换机搬迁、Telegram 通知、两步验证、外部 API,都在面板里。

从一台服务器自用,到几十台服务器、几千用户、带代理分销的对外运营,用的都是同一套面板:主机统一管线路、用户、套餐和代理(代理有自己的面板、额度和用户),副机只跑数据面;配额、到期、设备数跨全部服务器统一判定;外部 API 直接对接商城和 Telegram 机器人。

## 功能总览

| 模块 | 内容 |
|---|---|
| 线路 | Hysteria2、AnyTLS、TUIC、Trojan、VLESS(Reality / Vision)、VMess、Shadowsocks(含 2022)、SOCKS、HTTP、Mixed;传输层 WS / gRPC / HTTPUpgrade / HTTP;Hysteria2 端口跳跃与伪装站点;Reality 握手目标一键检测;按服务器选择部署位置;按规则分流(域名 / IP 段 / 端口分给不同出口);**中转入口**(经集群里别的服务器或外部中转连进来,加密数据原样转发、UDP 也能转,订阅自动加节点) |
| 节点设置 | 订阅里的每个节点(一条线路在一台服务器上的直连、每个中转入口)可以单独设倍率、节点限速、每用户限速、在线人数上限,或者不输出到订阅;页面按线路分组(节点多时默认收起),线路行带汇总,点开看各节点;用户 / 套餐的线路选择里中转入口也能逐个勾 |
| 上游 | VLESS / VMess / Trojan / TUIC / Hysteria2 / Shadowsocks / SOCKS 落地,粘贴分享链接导入;一键测延迟、定时巡检、故障 / 恢复告警;WARP 一键接入;**线路也能加为上游**(链式代理),参数跟着线路自动走;**上游组**:几条上游自动用最快能通的,挂了自动换 |
| 用户 | 配额(可到 0.1 GB)、到期(可设首次连接后才开始计时)、周期重置、同时在线设备数(按源 IP:IPv4 地址与 IPv6 /64 各自计数,跨服务器并集;经中转入口进来的连接不占名额)、上下行限速;超量 / 到期自动禁用并踢线;批量生成、批量操作、CSV 导出。代理的用户归代理管,不混进主面板用户页 |
| 套餐 | 配额 / 时长 / 设备 / 限速 / 线路的模板,建号、续费(一次 N 期)、延期一键套用;换套餐可立即替换、叠加或按参考价折算,先预览再确认;可绑定限速规则,现有和以后的套餐用户都生效 |
| 代理 | 给代理分配线路、流量 / 设备 / 带宽额度与到期日,他在自己的面板(默认 2054,路径 /dl)里建号、建套餐;用量汇总到代理,超额 / 到期 / 停用即刻断其全部用户 |
| 订阅 | 通用链接、Clash、sing-box 三种格式,同一个地址按客户端自动给对的格式;Clash / sing-box 可自定义模板;外部节点可隐藏、改名、按关键词排除、测大陆连通;浏览器打开是落地页(用量、到期、一键导入、客户端下载、二维码、临时共享);订阅失效时给一页说明而不是空白 404;外部节点 / 外部订阅聚合;自签证书自动带 insecure |
| 多服务器 | 主机推送配置、回收流量、集中判定;每台服务器可设流量倍率,以及流量额度与到期(按量计费、月租的机器用完或到期自己停下,续上后自动恢复);双栈服务器可按线路选 IPv4 / IPv6;副机失联 / 恢复告警;大陆连通检测(移动 / 电信 / 联通家宽测点,手动 + 定时,被墙告警);**设为主机**(一键把主机换到另一台,订阅地址不变)与**主机容灾**(主机挂了由备用接任,确认后或自动

[...截断...]

)|
| 证书 | 一台服务器可放多张证书:Let's Encrypt HTTP-01 / Cloudflare DNS-01 / 手动 DNS 签发(支持泛域名),到期前自动续期,热更新不重启;无域名时一键自签;线路默认、面板、订阅各选各的,每条线路也能单独选 |
| 备份 | 一个 zip 含数据库一致快照与证书;上传即整机还原;定时备份、轮转、推送 Telegram;换机向导 |
| 运维 | WARP 安装 / 启用 / 停用 / 卸载并验证出口;swap(按磁盘余量封顶)、内核参数 + BBR、文件句柄、NTP;限制系统日志(journald)占用;磁盘快满提醒与一键清理(主机能远程清理副机) |
| 防火墙 | 各服务器的系统防火墙(ufw / firewalld / iptables)有没有挡端口,一键放开 / 撤销(先备份),或自动放行 m-ui 用到的端口;规则:放行端口、拉黑来源、端口只给指定来源,下发到选中的服务器、可设有效期;面板 / 订阅 / 外部 API 的访问黑白名单,可选自动拉黑扫描者(默认关) |
| 通知 | Telegram 与 Webhook:登录、用户到期 / 超量 / 禁用、上游故障、数据面停止、服务器大陆连通异常 / 恢复、每日报告(发送时点与日期都按面板时区);**Telegram 机器人**:手机上查用户、续期、重置流量、启停、要备份 |
| 观测 | 流量走势(按时段柱状,1h / 6h / 24h / 7d / 30d)、流量排行、在线用户与 IP、线路详情(总流量与各服务器分开的流量、此刻连着的用户与 IP)、最近入站连接诊断、审计日志、订阅访问日志(后两者可各自设定自动清理天数);概览「需要处理」的各类提醒可在设置里逐类关掉 |
| 安全 | bcrypt 密码、CSRF 防护、登录冷却(同一来源连续失败即暂停尝试)、两步验证(TOTP)、外部 API 令牌;代理面板与主面板会话严格隔离 |
| 页面伪装 | 有人直接打开订阅 / 面板端口的根目录,或用浏览器连 AnyTLS、Trojan、Hysteria2 线路时,看到一个普通网站(下载镜像、软件下载、视频站、个人博客,每台服务器各自随机生成,不会都长一样),或跳转到你自己的网站;可选也放在空着的 80 / 443。默认关,真客户端和正确的订阅地址不受影响 |
| 更新 | 面板自己发现新版本,侧栏版本号旁提示;一键更新 = 验发布者的签名、校验 SHA256 → 替换程序 → 重启,数据库、证书与所有设置不动(签名验不过就不装) |
| 集成 | 外部 API(建号、批量建号、续费 N 期、换套餐、启停、订阅地址、按订阅地址找用户、按快到期 / 用完筛用户、面板概况 / 服务器 / 线路 / 在线、代理自己的剩余额度;建号可以不给名字,建号和套餐操作带幂等键重试不重复建、不重复加时,套餐操作可预览;可建多把密钥,每把单独勾权限、单独限来源 IP),见 [docs/API.md](docs/API.md) |
| 流量奖励 | 线路上每跑满 1 TB 真实流量得 1 积分,2027-09-03 按积分比例发放奖池(USDT);奖池 = godusevpn 节点订阅订单的 40% + 捐赠,逐笔入账公开可查;自愿参加,不登记领取地址就什么都不上报,设置里可关。见[流量奖励计划](#流量奖励计划) |

<table>
<tr>
<td width="50%"><img src="docs/screenshots/user-detail.png" alt="用户详情:订阅地址、二维码、用量与流量走势"></td>
<td width="50%"><img src="docs/screenshots/nodes.png" alt="服务器:一主两副,配置推送、同步状态与在线数"></td>
</tr>
<tr>
<td align="center"><sub>用户详情:订阅地址、二维码、用量、在线设备</sub></td>
<td align="center"><sub>服务器:一主多副,推送同步、在线状态一眼看完</sub></td>
</tr>
</table>

更多截图(线路、落地页、英文界面)在 [docs/screenshots](docs/screenshots)。演示数据全部是 example.com 与文档保留 IP。

## 架构

一个二进制里跑着四件事:**面板**(管理界面与 API)、**订阅服务**(客户端来拉配置)、**数据面**(内嵌 sing-box,真正过流量)、**后台**(统计、配额与限速规则判定、上游巡检、公网 IP 探测、大陆连通检测、日志清理、主副同步)。它们共用同一个 SQLite 文件,所以面板里点一下保存,订阅和数据面立刻看到同一份数据。

<sub>下面几张图由 [docs/diagrams](docs/diagrams) 里的 Mermaid 源文件渲染而成(网页和手机 App 看到的是同样的图);改了源文件运行 `node docs/diagrams/render.mjs` 重新出图。</sub>

### 一台服务器里有什么

<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/architecture-dark.png">
  <img src="docs/diagrams/architecture-light.png" width="918" alt="m-ui 一台服务器里有什么:管理员(:2053 /app/)和代理(:2054 /dl/)连面板,用户客户端连线路端口(数据面,真流量)和订阅服务(:2056 /sub/);面板热更新或重启数据面,数据面把流量与在线 IP 交给后台任务;面板、后台任务、订阅服务共用 m-ui.db;流量经出口(直连 · WARP · 落地中转,按线路上游与分流规则)出去">
</picture></p>

> 端口和路径都能改;上面写的是默认值。面板与代理面板是同一套前端,靠会话里的作用域区分能看到什么。
>
> 每条线路有一个默认上游(直连、WARP 或某个落地中转),勾上按规则分流后,指定的域名 / IP 段 / 端口可以走别的出口或直接拦掉;纯 IPv6 机器的直连线路还会把 1.1.1.1、8.8.8.8 这类公共 DNS 改连它们的 IPv6 地址。外部服务都是可选的:GitHub(检查更新、下载更新包;功德箱名单、流量奖励的公开账本、伪装站用的照片也从它取,取不到走 jsDelivr)、v2fly 域名库(查应用域名)、Cloudflare / ipify(探测本机公网 IPv4 与 IPv6)、Globalping(大陆连通检测、主机容灾的境外见证)、DNS 服务商的接口(Cloudflare 签证书;主机容灾改解析可用 Cloudflare / 阿里云 / 腾讯云 DNSPod,都要自己填凭据)、Telegram(通知)、ntfy.sh 与 TronGrid(功德箱:发留名、查到账)、流量奖励的登记服务(reward.godusevpn.org,登记了领取地址才上报);连不上只影响对应那一项。

### 保存一次改动,发生了什么

面板从不直接去改运行中的 sing-box —— 先让 sing-box 自己把整份新配置解析一遍,通过了才落库、才动数据面。

<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/apply-dark.png">
  <img src="docs/diagrams/apply-light.png" width="882" alt="保存一次改动:面板校验后开事务写库,让 sing-box 干跑整份配置;干跑不过就回滚、运行中的不动;通过才提交,并按变化分级重载(换用户表 / 热换出站 / 重启且能回滚)">
</picture></p>

### 一次订阅请求怎么走

<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/subscription-dark.png">
  <img src="docs/diagrams/subscription-light.png" width="848" alt="一次订阅请求:按地址认人 —— 用户名或随机令牌命中用户,临时共享令牌是同一个用户的另一套凭据,对不上给 404(浏览器看到「订阅地址无效」页);命中用户时看 User-Agent:浏览器看到落地页(停用、到期、用尽时顶部标明原因,共享令牌是精简版),代理客户端在停用、到期、用尽时拿到 404,否则 Clash 系客户端或 ?format=clash 拿到 Clash YAML,sing-box 系客户端或 ?format=json 拿到 sing-box 配置,其它拿到通用链接">
</picture></p>

> 三种格式里的节点都是同一套来源:**用户已分配的线路 × 该线路已部署的服务器**,再拼上外部节点与外部订阅。所以加一台服务器,所有人的订阅里自动多出对应节点。分配也可以