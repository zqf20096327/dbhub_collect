# tidb-dr-lab

TiDB 災難復原（DR）runbook 的實驗與驗證環境。

目標：MASTER/SLAVE 雙 TiDB cluster（v8.5.0）以 TiCDC 單向同步，演練
**failover → MASTER 重建回灌 → 計畫性切回** 的完整流程，實測 RPO/RTO，
產出可直接照做的 [完整說明版 runbook](runbook/runbook.md)，以及事故當下使用的
[直接指令版 runbook](runbook/disaster-runbook.md)。

## 架構

```
 k8s cluster A (Azure)                k8s cluster B (Azure)
┌─────────────────────────┐  ~10ms  ┌─────────────────────────┐
│  MASTER TiDB v8.5.0     │◄───────►│  SLAVE TiDB v8.5.0      │
│  (PD/TiKV/TiDB/TiCDC)   │         │  (PD/TiKV/TiDB)         │
│                         │         │  (TiCDC 僅 failback 時) │
│  app: dr-probe (Go)     │         │                         │
│  每秒讀寫一次            │         │                         │
└───────────┬─────────────┘         └───────────┬─────────────┘
            │        changefeed: MASTER→SLAVE   │
            │        (redo log + syncpoint)     │
            └────────────┬──────────────────────┘
                         ▼
                 MinIO (S3 相容)
        全量備份 / TiCDC redo log 共用
```

## 目錄結構

| 路徑 | 內容 |
|------|------|
| `app/` | dr-probe：量測用 Go app（每秒寫遞增序號＋讀回，事後算 RPO/RTO） |
| `deploy/` | k8s manifests：TiDB Operator、master/slave TidbCluster、MinIO、dr-probe |
| `deploy/changefeed/` | TiCDC changefeed 設定（redo log、syncpoint） |
| `scripts/` | 各 Phase 的操作腳本（runbook 的可執行版本） |
| `runbook/runbook.md` | 完整說明版：背景、原理、每步預期與 rollback |
| `runbook/disaster-runbook.md` | 真實事故直接指令版：不呼叫 `scripts/*.sh` |
| `docs/` | 決策記錄、測試計畫、實測結果 |

## 關鍵決策

完整記錄見 [docs/decisions.md](docs/decisions.md)。摘要：

1. **災難範圍**：只有 TiDB cluster 掛掉；k8s 與 app 存活，app 跨 cluster 連 SLAVE。
2. **一致性**：TiCDC 開 redo log（`consistent.level=eventual`），failover 時 `cdc redo apply`。
3. **App 切換**：改 env + `kubectl rollout restart`。
4. **備份**：**BACKUP/RESTORE SQL statement 優先，BR CLI 為 fallback**（兩者皆驗證；2026-07-20 改定案，見 decisions.md D4。REPORT §5.1 記錄的是 1.0 時期的 BR 定案）。
5. **觸發**：告警自動、切換手動（人確認後執行腳本）。
6. **驗證**：syncpoint + sync-diff-inspector 事前驗；切換窗口只做筆數快核。
7. **儲存**：MinIO（S3 相容），貼近正式環境。
8. **GC**：備份回灌期間用 `SET GLOBAL tidb_gc_enable=FALSE`（官方流程），不是調 `tidb_gc_life_time`。

## 流程總覽

- **Phase 0 平時態勢**：MASTER→SLAVE changefeed（redo log + syncpoint），監控 checkpoint lag。
- **Phase 1 Failover**：人工確認 → `cdc redo apply` 推平 SLAVE → 記錄 TSO → app 切 SLAVE。
- **Phase 2 重建回灌**（不停機）：重建空 MASTER → SLAVE 關 GC → 全量備份/還原 →
  SLAVE→MASTER changefeed（`--start-ts=backupTS`）→ 開回 GC → sync-diff 驗證。
- **Phase 3 計畫性切回**：停 app → 等追平 → 快核筆數 → 換向 changefeed → app 切回 MASTER。

## 快速開始（lab）

```bash
# 前置：兩座 AKS 的 kubeconfig，環境參數
cp scripts/env.example scripts/env.sh && vim scripts/env.sh

scripts/00-install-operator.sh     # 兩座 cluster 裝 TiDB Operator
scripts/01-deploy-clusters.sh      # 部署 master/slave TiDB + MinIO
scripts/02-create-changefeed.sh    # 建 MASTER→SLAVE changefeed（redo+syncpoint）
scripts/03-deploy-app.sh           # 部署 dr-probe
scripts/10-failover.sh             # Phase 1
scripts/20-rebuild-resync.sh       # Phase 2
scripts/30-switchback.sh           # Phase 3
```
