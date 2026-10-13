# Region 搬家大作战

TiDB 科普小游戏：扮演 PD（Placement Driver），把 4 个 Region（R1–R4）的三份投票副本，在 3 个机房（A/B/C）、6 台 TiKV 之间搬家。

单文件 HTML/CSS/JS，无后端、无数据库、无构建工具。

## 运行方法

用浏览器直接打开 `index.html`（双击即可，Chrome / Edge / Safari 均可），无需安装任何东西。

- 桌面：点彩色副本选中，再点目标 TiKV 搬迁；也可以直接拖拽；键盘用 Tab 聚焦、Enter 确认、Esc 取消。
- 手机：点选副本 → 点目标机器；页面自适应，无横向滚动。

## 两关目标

- 关卡 1 · 扩容救场：6 次搬迁以内，让 6 台 TiKV 每台正好 2 份副本。
- 关卡 2 · 机房断电：8 次搬迁以内，让每个 Region 的三份副本分别位于 A、B、C，再点“断电挑战”。

评分：两关总搬迁 ≤8 次三星、≤10 次两星、其余通关一星；两关通关显示“野生 PD 上岗证”。

## 规则要点

- 同一 Region 不能在同一台 TiKV 放两份副本；每台 TiKV 最多 4 个槽位（游戏规则）。
- 合法搬迁消耗 1 次额度；原地、重复副本、槽位已满不消耗；支持重开本关。
- 断电挑战不消耗搬迁额度；断电机房会让最多 Region 失去多数派（并列按 A→B→C）。
- 顶部“参考答案”在独立演示棋盘上逐步展示解法，不影响当前对局。

科普设定：等大 Region、三个投票副本、仅模拟 TiKV 层。“失去多数派”表示副本暂时无法投票、Region 暂不可用，并非数据立即丢失。

延伸阅读：[TiDB 调度原理](https://pingkai.cn/docs/tidb/stable/tidb-scheduling) · [Raft 存储与副本](https://pingkai.cn/docs/tidb/stable/tidb-storage)

## 开发方式

使用平凯 Loop 中配置的 DeepSeek V4.1 Flash 智能体生成和迭代。

## 开源许可

本项目采用 [BSD Zero Clause（0BSD）](LICENSE) 许可证，允许自由使用、修改和分发，包括商业用途。
