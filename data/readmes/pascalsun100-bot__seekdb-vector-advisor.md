# seekdb-vector-advisor 1.1.0

向量检索调优技能包，入口为 SKILL.md；按任务读取 references 中的选型、SQL、诊断与演示说明。

```bash
python scripts/review_sql.py examples/case1_slow.sql
python scripts/review_sql.py examples/case2_good.sql
python scripts/recall_eval.py --gt examples/recall_gt.csv --pred examples/recall_pred.csv --target-recall 0.6 --max-p95-ms 30 --json
```

第一条预期退出 1（坏例），后两条退出 0。默认召回阈值为 0.9，示例 recall@10 为 0.6333，因此默认评估退出 1。延迟每请求一个样本，样例共 5 个，P95 约 28.86 ms。

只需 Python 3.8+ 标准库，不连接数据库。静态检查不能证明 SQL 实际可执行、索引实际命中或性能达标。输入格式、指标定义和边界见 SKILL.md；真实库验证步骤见 references/demo.md。

许可：Apache-2.0，完整条款见 LICENSE。版本写在 front-matter 中以延续项目发布格式；其他工具若限制 front-matter 字段，导入时按其规范转换。
