# HyCo-openGauss：源码、数据与复现材料

本仓库保存 2026-11-05 从实验服务器整理的修改版 openGauss、HyCo runtime、修改版 BenchBase、实验脚本及数据。原工程和未提交修改保持原样，仓库不导入服务器账号、密码文件、SSH 密钥或数据库认证目录。

先阅读 [复现步骤](REPRODUCE.md)、[数据清单](datasets/README.md)、[安全与完整性审查](provenance/AUDIT.md) 和 [许可审查](provenance/LICENSE-AUDIT.md)。原始实验报告位于 [迁移报告](opengauss-exp/docs/HyCo-openGauss迁移报告-20260730.md)。

| 目录 | 内容 |
| --- | --- |
| `opengauss-exp/src/openGauss-server/` | openGauss 6.0.1 工作源码，包含 HyCo/CXLQueue/RDMA 修改及新增文件 |
| `hyco/hyco-runtime-release-v0.1.0/` | HyCo 实现、头文件、API 文档、示例和测试 |
| `benchbase/` | 实验实际使用的 BenchBase 源码及本地 Java 修改 |
| `opengauss-exp/{scripts,config,env,sql,tests,tools}/` | 构建、部署、数据加载、实验与汇总脚本，配置模板和传输工具源码 |
| `datasets/` | 可移植合成数据、经清理的实验原始测量及校验索引；大文件使用 Git LFS |
| `provenance/` | 原始提交、修改补丁、依赖哈希、审查结果与受限外部存储说明 |
| `repro/` | 数据生成、校验、工作目录迁移和固定依赖准备工具 |

```bash
git clone https://github.com/Geertis/Hyco-openGauss.git
cd Hyco-openGauss
git lfs install
git lfs pull
python3 repro/verify.py --unpack-measurements /absolute/new/path/hyco-measurements
```

已验证独立 HyCo 编译和 4 项运行时测试、测量归档完整性、Customer 数据完整性及历史结果汇总。完整的跨平台性能重跑仍需要 CXL devdax、两台 RDMA 主机和对应 Linux 环境，不能仅凭源码上传宣称已经复现。历史报告中的加速比属于原实验结果。

上游软件保留各自许可证。原始 HyCo 材料没有找到独立许可文件，仓库没有擅自指定新的开源许可证。
