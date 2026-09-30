# Waterworks Ops Toolkit 水务智能运维工具集

面向水务行业（物联网平台 / 二次供水 / 大数据中心）的**生产级运维实战项目集**，
覆盖数据库运维、可观测平台、容器网络风险防控、老旧系统接手标准化、极端场景应急五大方向。

## 模块导航

| 模块 | 内容 | 亮点 |
|---|---|---|
| [01-db-ops-toolkit](01-db-ops-toolkit/) | MySQL/PostgreSQL/达梦 巡检+备份+故障手册+调优 | 三库统一巡检脚本(退出码对接告警)、达梦国产化部署 |
| [02-observability-stack](02-observability-stack/) | Prometheus+Grafana+Alertmanager+ELK 一键部署 | P1/P2/P3分级告警、降噪三板斧、水务业务拨测 |
| [03-container-network](03-container-network/) | 容器网络规划 + IP冲突检测工具(Python零依赖) | docker网段重叠/资产表冲突/ARP多MAC 检测 |
| [04-legacy-system-takeover](04-legacy-system-takeover/) | 老旧系统接手方法论 | 30天四阶段Checklist + 变更/巡检/值班SOP |
| [05-emergency-response](05-emergency-response/) | 极端场景应急 | 台风三级应对Playbook + 5Why故障复盘模板 |
| [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) | 岗位技能地图与面试准备 | 按JD逐条拆解+STAR故事框架+考前速记 |

## 快速开始

```bash
git clone https://github.com/<你的用户名>/waterworks-ops-toolkit.git
cd waterworks-ops-toolkit/02-observability-stack
docker compose up -d        # 监控栈一键起: Grafana :3000 / Prometheus :9090

cd 03-container-network
python3 ip_conflict_checker.py --asset assets.csv   # IP冲突检测(零依赖)
```

## 技术栈

`MySQL 5.7/8.0` `PostgreSQL 12+` `达梦DM8` `Docker/Compose` `Prometheus` `Alertmanager`
`Grafana` `ELK 8.x` `Blackbox-Exporter` `Shell` `Python3`

## 设计原则

1. **开箱可用**：脚本/配置零第三方依赖或 docker compose 一键启动
2. **生产思维**：巡检对接告警、备份必演练、变更必回滚、预案必演练
3. **业务贴合**：告警规则/日志管道/应急预案均针对水务场景（抄表高峰、台风、泵站设备）
