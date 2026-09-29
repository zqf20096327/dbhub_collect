# TiDB单机生产环境模拟部署

这是一个基于官方文档在N305单台服务器上部署TiDB生产环境模拟集群的完整方案。

## 🏗️ 项目概述

本项目基于 [TiDB官方快速上手指南](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-tidb/) 在单台N305服务器（Ubuntu，8核心，16GB RAM）上使用TiUP部署一个模拟生产环境的TiDB集群。

## 🎯 部署目标

- ✅ 单机多实例TiDB集群
- ✅ 完整的监控体系
- ✅ 生产环境配置模拟
- ✅ 高可用架构演示

## 🖥️ 硬件配置

- **CPU**: 8核心
- **内存**: 16GB RAM
- **操作系统**: Ubuntu
- **网络**: 内网环境

## 🏛️ 架构设计

### 集群组件分布
```
┌─────────────────────────────────────────────────────────┐
│                     N305 服务器                          │
├─────────────────────────────────────────────────────────┤
│  PD节点 (2379,2380)  │  TiDB节点 (4000)                  │
├─────────────────────────────────────────────────────────┤
│  TiKV节点 (20160)    │  TiKV节点 (20161)                │
├─────────────────────────────────────────────────────────┤
│  TiFlash节点 (9000)  │  监控组件 (3000,9090)            │
└─────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
TiDB_RM01/
├── configs/          # 配置文件
├── scripts/          # 部署脚本
├── docs/            # 文档资料
├── logs/            # 日志文件
├── monitoring/      # 监控配置
└── README.md        # 项目说明
```

## 🚀 快速开始

### 1. 系统要求检查
```bash
# 检查系统信息
./scripts/check_system.sh
```

### 2. 安装TiUP
```bash
# 安装TiUP集群管理工具
./scripts/install_tiup.sh
```

### 3. 部署集群
```bash
# 部署TiDB集群
./scripts/deploy_cluster.sh
```

### 4. 验证集群
```bash
# 检查集群状态
./scripts/check_cluster.sh
```

## 📊 监控访问

- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **TiDB Dashboard**: http://localhost:2379/dashboard

## 📚 详细文档

- [部署指南](docs/deployment-guide.md)
- [配置说明](docs/configuration.md)
- [监控指南](docs/monitoring.md)
- [故障排除](docs/troubleshooting.md)

## ⚠️ 注意事项

1. 确保系统满足最低硬件要求
2. 关闭防火墙或开放必要端口
3. 确保有足够的磁盘空间（至少50GB）
4. 建议在测试环境先验证部署流程

## 🔧 常用命令

```bash
# 查看集群状态
tiup cluster display tidb-test

# 启动集群
tiup cluster start tidb-test

# 停止集群
tiup cluster stop tidb-test

# 重启集群
tiup cluster restart tidb-test

# 扩容节点
tiup cluster scale-out tidb-test scale-out.yaml

# 缩容节点
tiup cluster scale-in tidb-test --node 192.168.1.100:20160
```

## 📞 技术支持

如有问题，请参考：
- [TiDB官方文档](https://docs.pingcap.com/zh/tidb/stable)
- [TiUP使用指南](https://docs.pingcap.com/zh/tidb/stable/tiup-overview)
- [社区论坛](https://asktug.com/)

---

**项目状态**: ✅ 已完成  
**最后更新**: 2025年10月17日  
**GitHub仓库**: https://github.com/mengni-w/TiDB-production-environment-simulation-cluster