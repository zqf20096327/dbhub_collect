# v2+A 修 最终定稿（2026-11-04）

## 用户裁定
- A 修：test/example/sample 弱路径 0.5 票不直通（防测试夹具误配）✅ 已落地
- B 接受宽口径：引擎新增库位（真多库工具）不视为错 ✅
- 解析器修正：票数括号（…）不参与金标解析；人工栏显式列表优先；引证含 `|` 的
  netdata/mall/pigsty 三行人工修正

## 对账（50 条，修正口径）

| 指标 | v1 | v2 | v2+A（定稿） |
|---|---|---|---|
| 完全一致 | 13 | 27* | 24 |
| 漏判 | 34 | 16* | 18 |
| 多判 | 3 | 7* | 8 |
| **按口径达成（一致+B 类接受）** | — | — | **31/50** |

*旧解析器虚账，本次一并修正（mybatis-plus-join 虚 Oracle、motor-admin 虚 SQLite 等）。

## 漏判 18 条（全部设计内/范围外，零新逻辑错误）

- 内容仓提名通道未开 6：JavaGuide、awesome-cheatsheets、interview_internal_reference、
  JavaFamily、CS-Books、share_ppt → v1.5 读时 dbs
- 未圈已有归属不全 3：prisma、tidb（MySQL 已 overrides 签发）、chainlink → 铁律/v1.5
- 引擎无信号 3：AliSQL、sqlectron（证据分片无信号）、school-of-sre
- 金标人工增量 2：coolify（CH+SQLite）、airbyte（MariaDB）
- 部分信号 3：turso 缺 PG、grafana 缺 SS（另有 +3 宽口径库）、scalikejdbc 缺 SQLite
- TDengine 1：A 修后不再误配，金标 Oracle+SQLite 属提名类

## 多判 8 条（B 类 7 已接受 + 未圈 1）

- B 类引擎更全 7：netdata（+CH/SS/MariaDB/Oracle，真 collector 监控目标）、metabase
  （+4 真多库驱动）、dolt（+PG/SS，doltgres）、sqlmap（+SQLite）、DB-GPT（+Oracle）、
  motor-admin（+SQLite）、meteroid（+PG）→ 用户拍板接受宽口径
- pigsty 1：PolarDB 为 AI 时代历史结论，铁律不碰

## A 修效果
fill 1,992→1,964（−28 条纯弱路径误配，TDengine 类）；全量 11 套 selftest 绿；
writeback 断言 +1（test 路径 0.5 不直通）。
