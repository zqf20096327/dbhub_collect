# GaussDB 跨云容灾自动化运维工具 (DrCtl)

本项目提供了一套完整的自动化脚本工具集 (`drctl`)，用于简化 GaussDB 的跨云容灾日常运维、演练、倒换及灾备验证工作。

## 📖 快速上手

请查看 **[用户操作手册 (Operation Guide)](docs/op_guide.md)** 获取详细（保姆级）使用指南。

手册包含：
- 环境安装与前置条件（Python, sshpass）
- 配置文件说明
- **场景一：灾备切换演练** (A->B, B->A 全流程)
- **场景二：灾备解除与验证** (解耦 -> 验证 -> 重建)

## 🚀 核心功能

- **一键倒换演练**：全自动执行预检、切换及后置清理。
- **仿真演练支持**：支持开启/结束容灾仿真演练，验证业务读写。
- **灾备关系管理**：支持一键解除和建立容灾关系。
- **智能轮询**：内置针对长耗时任务（如建立/删除容灾）的智能等待机制。
- **多版本适配**：脚本自动兼容 Python 2/3 及各类 Linux 发行版。

## 📂 项目结构

```text
.
├── drctl                            # 统一入口命令
├── configs/                         # 配置文件目录
├── docs/                            # 文档目录
│   └── operation_guide.md           # 用户操作手册
│   └── official_product_manual.md   # 官方使用说明书
├── lib/                             # 核心脚本库
│   ├── 00-show_status.sh            # 状态显示
│   ├── 01-daily_precheck.sh         # 日常巡检
│   ├── 02-precheck_switchover.sh    # 倒换预检
│   ├── 03-disaster_switchover.sh    # 倒换执行
│   ├── 04-post_switchover.sh        # 后置清理
│   ├── 05-delete_dr.sh              # 解除容灾
│   ├── 06-establish_dr.sh           # 建立容灾
│   ├── 07-simulation_start.sh       # 开启演练
│   └── 08-simulation_stop.sh        # 结束演练
└── log/                             # 运行日志
```

## 🛠 使用示例

**执行全流程切换演练（Site A -> Site B）：**
```bash
./drctl --profile bj-sh --action all --direction A2B
```

**执行容灾仿真演练（开启/结束）：**
```bash
./drctl --profile bj-sh --action simulation-start --direction A2B
./drctl --profile bj-sh --action simulation-stop --direction A2B
```

**执行日常健康检查：**
```bash
./drctl --profile bj-sh --action daily --direction A2B
```
