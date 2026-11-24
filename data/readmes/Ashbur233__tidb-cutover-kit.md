# TiDB Cutover Kit

面向已有 TiCDC 链路的 TiDB 迁移工具，支持数据一致性校验、切换前检查、正反向 CDC 编排和回退演练。

**当前切换流程供隔离环境演练。** TGW 调权与权重查询为模拟，业务成功率需单独验证。`cutover --execute` 会实际终止会话、修改账号权限和操作 TiCDC。R2 会移除本批次的反向任务并删除原源端的 `tidb_cdc` 库。

## 快速开始

在 Linux 中控机上使用 Python 3.6 或更新版本和 `mysql` 客户端。从仓库根目录运行命令，配置中的相对路径以当前工作目录为基准。数据一致性校验还需要 `sync_diff_inspector`。

已有正向 CDC 时，先复制预检查与切换的配置模板：

```bash
cp configs/config.precheck-cutover.example.ini config.cutover.ini
chmod 600 config.cutover.ini
```

填写两端的 TiDB 连接和 `[cdc] api_url`。运行 `cutover-check` 前，还需填写反向 TiCDC API 地址和控制账号、CDC 写入账号的保护名单。

```bash
python3 -m tidb_cutover precheck --config config.cutover.ini
python3 -m tidb_cutover cutover-check --config config.cutover.ini
```

这两条命令查询 TiDB 和 TiCDC 并生成本地报告。模式二和模式三可以独立运行，数据一致性历史由模式一单独记录。

## 操作指南

| 功能 | 常用命令 | 文档 |
| --- | --- | --- |
| 数据一致性校验 | `init`、`check-once`、`monitor` | [数据校验](docs/validation.md) |
| 检查 CDC、对象及账号 | `precheck`、`precheck-report` | [切换前预检查](docs/precheck.md) |
| 只读检查、切换、续跑及回退 | `cutover-check`、`cutover`、`cutover-resume`、`cutover-rollback` | [切换与回退](docs/cutover.md) |
| 构造数据、模拟业务流量 | `python3 -m tidb_cutover.lab_mode`、`python3 -m tidb_cutover.traffic_workload` | [隔离演练](docs/lab.md) |

## 本地测试

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

测试使用模拟后端覆盖校验、预检查、切换和回退。真实 TiDB、TiCDC 版本的兼容性需要在测试集群联调确认。
