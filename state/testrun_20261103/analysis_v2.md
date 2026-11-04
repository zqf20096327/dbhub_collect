# v2 五刀修法后的 50 金标对账与原因分析（2026-11-03）

## 对账结果（50 条，3 条引证含 `|` 的行人工修正）

| 指标 | v1 口径 | v2 五刀后 | 变化 |
|---|---|---|---|
| 完全一致 | 13 | **27** | +14 |
| 漏判 | 34 | **16** | −18 |
| 多判 | 3 | **7** | +4 |

## 漏判 16 条原因分层（全部设计内/范围外，无新逻辑错误）

| 类 | 条数 | 仓 | 原因 |
|---|---|---|---|
| 内容仓·提名通道未开 | 6 | JavaGuide、awesome-cheatsheets、interview_internal_reference、JavaFamily、CS-Books、share_ppt | 信号只在 README 行号提名里（引擎无指纹）；五刀未含提名通道，已声明归 v1.5 读时 dbs |
| 未圈·已有归属不全 | 3 | prisma（PG/5）、tidb（TiDB，MySQL 已 overrides 签发）、chainlink（PG/2） | 铁律不碰 AI 时代非空结论；补全属 v1.5 范畴 |
| 引擎无对应信号 | 2 | AliSQL（无裁决无指纹）、sqlectron（旧 draft 有 sqlite3 依赖，当前证据分片无此信号——证据侧采集变化，非回写逻辑） | 提名/旧信号未落到证据层 |
| 人工增量 | 2 | coolify 缺 CH+SQLite、airbyte 缺 MariaDB | 金标比引擎多，用户人工加库（引擎上限） |
| 信号错位 | 1 | TDengine：金标 Oracle+SQLite，引擎只有 test 路径 0.5 票 MySQL/PG | 弱路径信号 ≠ 真实支持，见多判 A 类 |

## 多判 7 条原因分层（v2 直通的代价，全部定位）

| 类 | 条数 | 仓 | 原因 |
|---|---|---|---|
| **A 弱路径 0.5 直通** | 1 | TDengine | test/requirements.txt 的 pymysql/psycopg 0.5 票直接 fill——测试夹具信号，quorum 设计本要挡的。**应修**：0.5 弱路径（test/example/sample）不进直通 |
| B 引擎比金标更全（真多库工具） | 5 | netdata（+CH/SS/MariaDB/Oracle：collector 插件目录树票 82.5 等，6 库都是真监控目标）、metabase（+MariaDB/Oracle/SS/SQLite：真多库驱动）、dolt（+PG/SS：doltgres 存在）、sqlmap（+SQLite）、DB-GPT（+Oracle） | 引擎树票/依赖票放大后超金标——金标当时只勾了 caps/quorum 遮挡下的子集，对新增库位无否定表态 |
| 未圈历史结论 | 1 | pigsty（现判 PolarDB+PG） | 铁律不碰，非 v2 产物 |

## 结论

1. **五刀全部按方案生效**：oos 短路误杀清零（JavaGuide 等从"范围外"改为带提名的"证据不足"）、旧 verdicts 不短路（dolt/quivr/school-of-sre 恢复引擎判定）、topic 单通道直通（codebase-memory-mcp ✓）、裁决补集（metasfresh）、旧 fill 重判扩库（sqlc 5 库 ✓、metabase +CH ✓）。一致率 26%→54%。
2. **漏判 16 条零新逻辑错误**：全是已声明的范围外类（提名通道/未圈补全/证据层信号缺位）。
3. **多判 A 类是真精度风险**：test 路径 0.5 票直通与"测试夹具误伤"防线冲突——修法一行（直通门槛排除 is_weak_path 0.5），建议下刀。
4. **多判 B 类属口径决策**：引擎新增库位多为真支持（netdata 六库监控目标、metabase 多库驱动），金标未表态。要么接受宽口径，要么抽 20-30 条引擎增量库位人工过目定案。
