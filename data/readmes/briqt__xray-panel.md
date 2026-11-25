# xray-panel

[![Release](https://img.shields.io/github/v/release/briqt/xray-panel)](https://github.com/briqt/xray-panel/releases)
[![Go](https://img.shields.io/badge/Go-1.25+-00ADD8?logo=go&logoColor=white)](https://go.dev)
[![Xray](https://img.shields.io/badge/Xray--core-26.11-5c6bc0)](https://github.com/XTLS/Xray-core)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

个人多节点 Xray 集中管理面板：只需在一台机器上部署一个单文件二进制（内嵌 Web 界面与 SQLite，无外部依赖），即可经 SSH 集中管理多台节点——安装 Xray 与 Caddy、自动签发续期证书、配置互补协议与节点间中转、管理多用户与线路授权、下发订阅、统计流量。

设计依据与工程取舍见 [docs/design.md](docs/design.md)，版本变更见 [CHANGELOG.md](CHANGELOG.md)。

![架构拓扑](docs/images/architecture.png)

## 特点

- **单文件控制面，节点无 Agent**：被管节点只运行官方原版 Xray 与 Caddy，不部署面板进程或轮询守护端；面板机预下载官方发布包校验后经 SSH 推送，节点无需访问 GitHub（纯 IPv6 节点同样可用）。
- **三条互补线路，服务端独立隔离**：每台节点同时提供 UDP、TCP 直连与 CDN 兜底三条物理隔离线路，按线路授权与启停实时生效：
  - **Hysteria2（UDP）**：自带端口跳跃与 BBR，应对单端口 UDP 限速；
  - **VLESS + XHTTP + REALITY（TCP 直连）**：不借用易被识别阻断的公共大站域名，直接使用节点本机真实 HTTPS 站点做伪装，按域名生成内容与特征各异的多页静态站；
  - **VLESS Encryption + XHTTP + TLS（CDN）**：经 Cloudflare 中转并启用 0-RTT 加密，作为节点 IP 被封时的保底线路。
- **节点间中转落地**：任意入口节点可挂载其他节点作为落地，复用入口现有端口（无需新开公网端口，流量不重复计费）；落地节点走 Shadowsocks 2022，由防火墙自动维护活跃入口 IP 白名单，默认拒绝外部连接。
- **确定性纳管与真客户端自检**：纳管过程依次完成环境探测、DNS 校验、自动签证、配置回读，并由面板机运行真实 Xray 客户端逐条线路（含中转出口）实测通断与延迟；中途失败自动回滚，重复纳管不破坏已下发订阅。
- **与已有服务共存，DNS 自主可控**：节点 `443` 空闲时独占，已有 Caddy 占用 `443` 时自动切换回退端口共存、不影响原有站点；面板不索取云厂商 API 密钥、不修改 DNS 记录，仅做校验与提示。
- **开箱即用订阅与用户自助**：自适应下发 v2rayN 与 Mihomo / Clash 订阅（内置分流规则，支持按用户自定义 Clash 配置并做保存前校验）；普通用户可独立登录一键导入订阅、查看用量与内置客户端图文教程。
- **双口径流量统计**：同时统计按用户代理流量与节点整机流量（按网卡、服务、端口与对端拆解，便于核对账单、排查漏维护导致的异常跑流）。
- **HTTP API 与 Agent 友好**：节点纳管、结构化回读、线路自检、授权与流量查询均通过 REST JSON 接口提供，无需解析终端文本，方便直接交给 AI Agent 或脚本调用维护。

## 界面预览

![节点管理](docs/images/nodes.png)

| 代理流量统计 | 节点整机流量去向 |
| :---: | :---: |
| ![代理流量统计](docs/images/stats.png) | ![整机流量统计](docs/images/host-traffic.png) |

| 普通用户订阅自助 | 内置客户端图文指引 |
| :---: | :---: |
| ![我的订阅](docs/images/me.png) | ![使用指引](docs/images/guide.png) |

## 部署面板

面板机需能通过 SSH 连接各节点，并能访问 GitHub。

**下载预编译二进制（`linux-amd64` / `linux-arm64`）**：

```bash
mkdir -p /opt/xray-panel/data
curl -fL https://github.com/briqt/xray-panel/releases/latest/download/xray-panel-linux-amd64 \
  -o /opt/xray-panel/xray-panel
chmod +x /opt/xray-panel/xray-panel
curl -fsSL https://raw.githubusercontent.com/briqt/xray-panel/main/deploy/xray-panel.service \
  -o /etc/systemd/system/xray-panel.service
```

或从源码构建：

```bash
make build                                   # 产出 bin/xray-panel（linux/amd64，静态链接）
scp bin/xray-panel host:/opt/xray-panel/xray-panel
scp deploy/xray-panel.service host:/etc/systemd/system/
```

配置 `/opt/xray-panel/.env` 并启动：

```ini
ADMIN_USER=admin
ADMIN_PASS=<强密码>
JWT_SECRET=<固定随机串>
# 可选
PORT=2082                         # 默认只监听 127.0.0.1:PORT；或设 LISTEN=地址:端口
DATA_DIR=/opt/xray-panel/data
SSH_KEY_PATH=/root/.ssh/id_ed25519
TIMEZONE=Asia/Shanghai
```

```bash
systemctl daemon-reload && systemctl enable --now xray-panel
```

面板默认只监听本地回环，通过反向代理（如 Caddy：`<面板域名> { reverse_proxy 127.0.0.1:2082 }`）对外提供 HTTPS。

## 添加节点

1. **解析域名**：将节点域名指向节点 IP（不开 CDN 代理）；如需 CDN 兜底线路，另将 CDN 域名指向节点 IP 并开启 Cloudflare 代理（确保未对 ACME 验证路径强制跳转 HTTPS）。
2. **接入与纳管**：在面板新建节点、注入一次 SSH 公钥后点击“纳管”，面板自动完成环境检查、签证部署与逐条线路连通自检。
3. **分配线路**：在用户管理中勾选可用线路，保存即同步至对应节点。

## 边界说明

面板只负责常规环境的前置检查与确定性配置维护。若目标机器所需端口已被非 Caddy 的其他程序占用，或存在历史遗留配置冲突，纳管会报出原因并停止，不会擅自停用或清理外部服务。

## 开发

```bash
make web    # 构建前端
make test   # 后端测试 + 前端 lint + 脚本测试
make build  # 交叉编译 linux/amd64 静态二进制到 bin/
```

## 文档

- [设计与决策依据](docs/design.md)
- [参与贡献](CONTRIBUTING.md) · [安全](SECURITY.md) · [变更记录](CHANGELOG.md)

## 社区

[学 AI，上 Linux DO](https://linux.do/)

## 许可证

[MIT](LICENSE)
