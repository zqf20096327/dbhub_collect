# 11-03 全量测试记录 + 金标 50 条深度归因

## 一、已完成后脚本全量测试（11 套）

| 脚本 | 覆盖 | 结果 |
|---|---|---|
| attribution/selftest_api.py | T2a schema 空包 4 变体+反例 17+rich 聚合+确定性 | ✅ |
| attribution/selftest_dep_match.py | T1b 误伤契约 28/28+双档互斥+@types 排除 | ✅ |
| attribution/selftest_matcher.py | T2b topic 三规则+镜像/路径+43 案例+v0.3.0 文件名/org | ✅ |
| attribution/selftest_quorum.py | T2c 活案例四断言+票制边界+E-CI | ✅ |
| attribution/selftest_scan.py | T2d 三清单口径+验收门 | ✅ |
| attribution/selftest_vocab.py | T1c 词表派生 diff | ✅ |
| attribution/selftest_adjudicate.py | T4a 裁决 cite 校验+台账 | ✅ |
| attribution/selftest_writeback.py | T4b 四类映射+铁律+幂等+回滚 | ✅（首跑 2 断言失败，修后绿，见下） |
| collect/selftest_exit_gate.py | T0 出池闸门 | ✅ |
| collect/selftest_readme_relay.py | README 月度接力 | ✅ |
| evidence/selftest_evidence.py | 证据采集 71 断言 | ✅ |

**本轮抓到并修复的问题（唯一失败）**：selftest_writeback 两断言——①报告"四段齐全"仍查已删的"金标核对"段（11-03 金标清理的连带）；②"回滚逐字节还原"没跟上 CRLF 修复（写盘强制 LF 后与测试宇宙初始 CRLF 字节必然不同），改内容级比对。两处都是测试自身过期，非产品逻辑缺陷。

## 二、50 条金标 vs 引擎(T3b 验证面) vs 回写结果 分层归因

口径：金标=pilot_review_50.md 人工栏；引擎=T3b 复核表引擎建议列（用户 79/79 全认的那个面）；
我的=回写台账 fill dbs（未圈仓取 interp 最新 dbs，铁律不碰）。3 行引证含 `|` 字符被列解析污染
（netdata/mall/pigsty）不计入。

**分层计数（去解析污染后）**：

| 归因层 | 条数 | 性质 |
|---|---|---|
| 一致 | 15 | — |
| 信号层·oos 短路 | 7 | 我的薄壳层错误（T3b 未验证） |
| 信号层·AI 旧 verdicts 短路 | 3 | 同上 |
| 质量门·单信号拒绝 | 4 | 同上 |
| 裁决频道·砍库 | 7 | T4a 子集裁决压过引擎完整结论 |
| 多判 | 2 | 引擎新信号超金标（sqlmap+SQLite、DB-GPT+Oracle） |
| 金标人工增量 | 3+4 | 引擎上限（库位召回 71.8% 已知），非退步 |
| 未圈（已有归属不碰） | 5 | 铁律设计内；tidb 双标 overrides 已补 |

## 三、根因结论

**引擎没退步**：11 套测试全绿；T3b 验证面（引擎建议）与金标一致的行今天仍然成立。
**今天"不行"的是回写薄壳**：我在引擎外面焊了三层从未经过金标验证的关口——
①信号层 oos/edu/db_verdicts 短路（继承自 unattr_judge 侦查台账，侦查层只影响"进不进侦查"，
我把它升级成"直接决定 dbs"）；②质量门（topic 单通道/cat/quorum 再砍一刀）；③裁决频道
（622 条子集裁决覆盖引擎完整结论）。50 金标第一次照射这三层，14 条误杀现形。

修法（待用户拍板）：①oos 让位只压"17 库信号全无"仓；②删 AI 旧 verdicts 短路（v1.5 落地）；
③引擎立案结论直通，质量门只挡 cat 应用类；④裁决只作补集不作覆盖；⑤未圈仓的补全归
v1.5 读时 dbs。
