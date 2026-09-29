# h3c-idf-manager · 弱电井设备管理工具

面向楼宇弱电间（IDF, Intermediate Distribution Frame）的 H3C 交换机管理工具。
按 **楼栋 → 楼层 → 弱电井** 三级结构组织设备，自动扫描网段发现在线交换机，
通过 Telnet / SSH 读取 H3C Comware 配置并留存历史版本，图形化展示每个端口的
VLAN 归属、上联拓扑、端口对端 IP / 设备，并提供健康评分、VLAN 反查、
配置变更对比与定时巡检。

> 单机本地运行，无需外部数据库，适合园区 / 医院 / 学校等多楼宇内网运维场景。
> 已适配 H3C Comware V5（如 S5120S-EI 系列），协议算法兼容老设备（ssh-rsa / group1-sha1）。

---

## 功能特性

- **三级目录管理**：楼栋 → 楼层 → 弱电井，支持批量生成楼层结构、复制整栋、同层多弱电井
- **网段扫描**：输入网段（如 192.168.1.0/24）Ping + 端口探测发现在线设备，按命名规则正则自动归档到对应楼层，匹配不到可手动调整（已分类设备不会被重复归档）
- **配置读取与备份**：Telnet / SSH 自动登录（多凭据轮询），读取整机配置、端口状态、MAC 表、ARP 表、LLDP 邻居；每次读取自动保存带时间戳的历史版本，自动标注「配置变更 / 无变更」，支持任意两版行级 diff
- **端口图形化面板**：按实物板卡布局展示每个端口，格子内直接显示 VLAN 号，颜色区分端口状态，悬停查看对端 IP / MAC / LLDP 邻居
- **楼栋总览**：点击楼栋显示全楼设备清单、健康指标卡与分级处理意见（离线、低健康分、配置变更、VLAN 1 安全风险等）
- **上联关系图**：基于 LLDP 邻居自动绘制力导向拓扑，节点可拖动，离线设备标红
- **VLAN 反查**：按 VLAN 号聚合，一键查看某 VLAN 分布在哪些设备的哪些端口
- **健康评分**：采集 CPU / 内存 / 风扇 / 电源状态，0–100 评分，支持定时自动巡检
- **全局搜索**：IP / 设备名 / 型号 / 备注 / 弱电间 / VLAN 号统一搜索
- **凭据管理**：全局凭据 + 单设备凭据，密码加密存储于本地 SQLite；登录失败可弹窗手动输入并自动保存

## 界面截图（演示数据，均为虚构）

| 楼栋总览 | 设备详情 · 端口面板 |
|---|---|
| ![楼栋总览](docs/screenshots/02-building-overview.png) | ![设备详情](docs/screenshots/03-device-detail.png) |

| 上联关系图 | VLAN 反查 |
|---|---|
| ![上联关系图](docs/screenshots/04-topology.png) | ![VLAN 反查](docs/screenshots/05-vlan.png) |

## 快速开始

环境要求：Windows，Python 3.10+

```bash
# 1. 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 2. 启动（默认 http://127.0.0.1:7100）
.venv\Scripts\python app.py --port 7100
```

也可以直接双击 `start.bat`（自动打开浏览器）。

### 没有交换机也想先体验？

```bash
python scripts/seed_demo.py   # 生成一套虚构的演示数据（请勿在已有真实数据时运行）
```

### 典型使用流程

1. **设置**页配置命名规则正则（含命名组 `building` / `floor`，可选 `label`），用于扫描后按设备名自动归档
2. 左侧「+ 添加」批量生成楼栋楼层结构
3. **网段扫描**页输入网段开始扫描，在线设备自动入库归档
4. **凭据管理**页添加全局账号密码（支持多组轮询）
5. 设备列表点「读取配置」，带进度条逐台读取；登录失败可现场输入凭据并保存
6. 双击设备行查看端口面板 / 健康评分 / 备份历史与 diff

## 安全说明

- 所有采集仅使用 `display` 类**只读命令**（version / interface / current-configuration /
  mac-address / arp / lldp / cpu-usage / memory / fan / power），不会修改交换机任何配置；
  唯一的 `screen-length disable` 仅作用于当前登录会话，不写入设备
- 设备密码加密后存储在本地 `data/idf.db`，不会上传或外发
- `data/` 目录（含配置备份与凭据）已在 `.gitignore` 中排除，请勿手动提交

## 技术架构

```
Flask (REST API + 静态页面)
├── h3c.py        Telnet/SSH 采集与 Comware 配置解析（paramiko 2.12 兼容老算法）
├── scanner.py    网段 Ping / 端口扫描任务
├── db.py         SQLite 数据层（rooms / devices / credentials / configs / settings）
├── crypto_util.py 凭据加密
└── static/       原生前端（无构建步骤）：目录树 / 端口面板 / 拓扑图 / VLAN 反查 / 搜索
```

数据与配置备份均保存在本地 `data/` 目录，迁移时整体复制即可。

## License

[MIT](LICENSE)
