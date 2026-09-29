# TiDB 自动化部署项目 - 简介

## 📖 项目简介

这是一个基于 **Ansible** 的 TiDB 分布式数据库集群自动化部署项目，可以一键部署完整的 TiDB 生产环境。

### 🎯 主要功能
- ✅ 自动化部署 TiDB 集群（5节点架构）
- ✅ 系统环境优化和依赖安装
- ✅ 内置监控系统（Prometheus + Grafana）
- ✅ 安全配置和密码管理
- ✅ 支持集群管理和运维操作

## 🏗️ 集群架构

```
集群组成（5节点）：
├── TiDB 服务器：node141, node142  （SQL计算层）
├── PD 服务器：node141, node142, node143  （调度管理）
├── TiKV 服务器：node143, node144, node145  （存储层）
├── 监控：Prometheus（node141）+ Grafana（node142）
```

## 📋 系统要求

- **操作系统**：CentOS 7/8, RHEL 7/8, Ubuntu 18.04+
- **最低配置**：8核CPU, 16GB内存, 100GB SSD
- **推荐配置**：16核CPU, 32GB内存, 1TB SSD
- **网络**：千兆局域网，节点间延迟 < 10ms

## ⚙️ 核心配置文件

### 1. 节点清单 (`in.ini`)
```ini
[pd_servers]
node141 ansible_host=192.168.9.141
node142 ansible_host=192.168.9.142  
node143 ansible_host=192.168.9.143

[tidb_servers]
node141 ansible_host=192.168.9.141
node142 ansible_host=192.168.9.142

[tikv_servers]
node143 ansible_host=192.168.9.143
node144 ansible_host=192.168.9.144
node145 ansible_host=192.168.9.145

[all:vars]
ansible_ssh_pass=123123           # SSH密码
tidb_version=v7.1.0               # TiDB版本
cluster_name=tidb-prod-5node      # 集群名称
tidb_root_password=Prod@TiDB2025! # 数据库密码
```

### 2. 主要端口
- **TiDB**：4000（MySQL协议）
- **PD**：2379（客户端）, 2380（节点通信）
- **TiKV**：20160（存储服务）
- **监控**：9090（Prometheus）, 3000（Grafana）

## 🚀 快速部署

### 1. 环境准备
```bash
# 确保所有节点网络互通
ping 192.168.9.141
ping 192.168.9.142
ping 192.168.9.143
ping 192.168.9.144
ping 192.168.9.145

# 确保SSH可以连接所有节点
ssh root@192.168.9.141
```

### 2. 修改配置
```bash
# 编辑节点清单，修改IP地址和密码
vim in.ini

# 重点修改：
# - ansible_host: 实际服务器IP
# - ansible_ssh_pass: 实际SSH密码  
# - tidb_root_password: 数据库管理员密码
```

### 3. 一键部署
```bash
cd tidb-deploy
chmod +x start.sh
./start.sh
```

### 4. 部署验证
```bash
# 检查集群状态（在node141执行）
source ~/.bash_profile
tiup cluster display tidb-prod-5node

# 连接数据库测试
mysql -h 192.168.9.141 -P 4000 -u root -p'Prod@TiDB2025!'

# 访问监控系统
# Prometheus: http://192.168.9.141:9090
# Grafana: http://192.168.9.142:3000
```

## 📝 部署流程

项目部署分为4个自动化阶段：

1. **环境预处理**：系统优化、依赖安装、内核参数调优
2. **TiUP安装**：安装TiDB集群管理工具
3. **集群部署**：创建和启动TiDB集群
4. **安全加固**：配置数据库密码和访问控制

整个过程约需要 **15-30分钟**，具体时间取决于网络速度。

## ⚠️ 重要注意事项

### 🔴 部署前检查
- [ ] 确保所有节点时间同步
- [ ] 确保防火墙允许相关端口通信
- [ ] 确保磁盘空间充足（每个数据节点至少100GB）
- [ ] 确保SSH密码正确

### 🟡 安全提醒
- **立即修改默认密码**：SSH密码`123123`仅用于测试
- **生产环境配置**：启用SSL/TLS加密，配置防火墙
- **定期备份**：重要数据必须定期备份

### 🟢 性能建议
- **存储**：强烈建议使用SSD硬盘
- **内存**：TiKV节点建议32GB以上内存
- **网络**：建议使用万兆网络连接

## 🔧 常用运维命令

```bash
# 查看集群状态
tiup cluster display tidb-prod-5node

# 重启集群
tiup cluster restart tidb-prod-5node

# 重启单个组件
tiup cluster restart tidb-prod-5node -R tidb

# 集群扩容
tiup cluster scale-out tidb-prod-5node scale-out.yaml

# 集群升级
tiup cluster upgrade tidb-prod-5node v7.5.0
```

## 🆘 故障排除

### 常见问题
1. **SSH连接失败**：检查网络和密码
2. **端口占用**：检查端口是否被其他服务占用
3. **磁盘空间不足**：清理日志或扩容磁盘
4. **服务启动失败**：查看日志文件排查具体原因

### 日志位置
- **TiDB日志**：`/data/tidb/deploy/tidb-{ip}/log/`
- **TiKV日志**：`/data/tidb/deploy/tikv-{ip}/log/`
- **PD日志**：`/data/tidb/deploy/pd-{ip}/log/`

## 📞 技术支持

- **项目作者**：oranges_are_ripe
- **文档地址**：https://uniqueyouzhi.feishu.cn
- **TiDB官方文档**：https://docs.pingcap.com/zh/tidb/stable

---

> 💡 **提示**：这是一个生产级部署项目，建议先在测试环境验证后再用于生产环境。如遇问题，请优先查看日志文件进行排查。
