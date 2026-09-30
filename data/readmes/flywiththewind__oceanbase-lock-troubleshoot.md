# OceanBase 锁等待 / 锁超时 / 死锁排查

基于业务租户 `JAMES@oboracle`（集群 obv3 / OceanBase 3.2.3.3）真实复现与日志分析材料。

## 手册（推荐）

| 文件 | 说明 |
|------|------|
| `OceanBase锁等待超时与死锁排查手册-v5.docx` | **当前推荐**：锁等待 + 锁超时 + 死锁；关键日志；每步含 SQL |
| `OceanBase锁等待超时与死锁排查手册-v4.docx` | 同上结构的前一版 |
| `OceanBase锁等待超时与死锁排查手册-v3.docx` | 死锁含未压缩全量 Observer 附录（体积大，学习用） |

生成脚本：`gen_handbook_v5.py`（依赖 `python-docx`）。

## 复现脚本

运行前先导出密码（脚本内不再硬编码密钥）：

```bash
export OB_BIZ_PASSWORD='...'
export OB_SYS_PASSWORD='...'
export OCP_MON_PASSWORD='...'
export OB_SSH_PASSWORD='...'
```

- `run_lock_repro_v2.sh` → `evidence_v2/`（单行锁等待/超时）
- `run_deadlock_repro.sh` → `evidence_deadlock/`（AB-BA 死锁环）

## 证据目录

- `evidence_v2/`：锁等待/超时（约 2026-08-03 01:05）
- `evidence_deadlock/`：死锁环（约 2026-08-03 01:13）
- `evidence/`：早期复现留档

## 说明

本环境 `__all_deadlock_event_history` 与 OCP `ob_hist_sql_audit_sample` 可能为空；死锁需用两端 `lock_for_write conflict` + 双 `NEED_WAIT` + 双 `LOCK_MGR` 证明环形等待。客户端表象常为 `ORA-30006`（内部 `-6003`）。
