# TiDB 大表渐进式比对工具 (Shell 版本)

高性能比对两个 TiDB 数据库的数据一致性，使用渐进式分片策略自动适应数据分布。基于 Shell 脚本实现，轻量高效。

## 核心特性

- **自动字段检测**：自动从表结构获取所有字段进行比对
- **智能字段处理**：对 text/blob 类型自动使用前 256 个字符比对，提升性能
- **快速采样分析**：采样分析主键列特性，选择最佳分片列
- **数值范围分片**：基于最佳列的数值范围生成初始分片
- **动态调整**：自动检测过大分片，动态拆分
- **渐进式优化**：迭代优化，直到所有分片大小合理
- **Checkpoint 支持**：中断后可继续执行
- **高性能并发**：使用 GNU Parallel 实现多线程比对

## 依赖

- `mysql-client` - MySQL 命令行客户端
- `jq` - JSON 处理工具
- `parallel` - GNU Parallel 并发执行工具

### 安装依赖

**macOS:**
```bash
brew install mysql-client jq parallel
```

**Ubuntu/Debian:**
```bash
sudo apt-get install mysql-client jq parallel
```

**CentOS/RHEL:**
```bash
sudo yum install mysql jq parallel
```

## 使用方法

```bash
# 1. 修改配置
vi config.yaml

# 2. 加载配置并运行
source scripts/config.sh && load_config config.yaml
source scripts/utils.sh

# 3. 执行比对 (主脚本)
bash scripts/main.sh config.yaml
```

## 性能估算

对于 60亿行数据：
- 采样分析：约 1-5 分钟
- 初始分片：约 1-3 分钟
- 并行比对：约 2-6 小时（取决于数据分布）
- 总耗时：约 2-7 小时
