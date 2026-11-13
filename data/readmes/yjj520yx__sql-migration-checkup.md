# SQL 迁移体检台

把 Oracle / MySQL 的 SQL 与建表语句改写成达梦（DM8）可执行写法，并逐条说明「改了什么、为什么改、风险几级」。

纯前端静态站点：不连数据库、不执行 SQL、不上传任何内容。

- 线上地址：https://37jf4e4l7ixbzw2ksvt.traesite.cn/
- 当前版本：v1.1（49 条规则 = Oracle 24 + MySQL 25；其中 6 类高频写法给「建议改写」但不自动应用）

## 本地打开

- 直接双击 `index.html` 即可（无需 Node、无需构建、无需联网）。
- 也可以起一个静态服务器：`npx serve .` 或 `python -m http.server 8000`，然后访问 `http://localhost:8000`。

## 目录

| 文件 | 作用 |
|---|---|
| `index.html` | 页面结构 |
| `styles.css` | 样式与响应式布局 |
| `app.js` | 交互：样例、方向切换、diff 渲染、导出 |
| `rules.js` | **规则表**（数据驱动的核心） |
| `converter.js` | 转换引擎、行级 diff、Markdown 报告 |
| `samples.js` | 6 个脱敏样例 |

## 怎么加一条规则

打开 `rules.js`，往 `RULES` 数组里追加一个对象即可，不需要改引擎：

```js
{
  id: 'MY-DATE-ADD',                 // 唯一标识
  name: 'DATE_ADD → 日期加法',        // 界面展示名
  dirs: ['mysql'],                   // 'oracle' | 'mysql'
  kind: 'rewrite',                   // rewrite 改写 / advice 只提示
  risk: 'medium',                    // high | medium | low
  regex: /\bDATE_ADD\s*\(/gi,        // 匹配
  build: function (m, sql) {         // 改写规则必填；返回字符串或 {after, end}
    var open = sql.indexOf('(', m.index);
    var call = SqlUtil.readCall(sql, open);
    if (!call || call.args.length !== 2) return null;   // 拿不准就返回 null（不改）
    return { after: call.args[0] + ' + INTERVAL ' + call.args[1], end: call.end };
  },
  why: '达梦用日期加减语法，没有 DATE_ADD 函数。',
  note: '单位（DAY/MONTH）需要人工确认。',
  confirm: true                       // 是否标「需人工确认」
}
```

要点：

1. `kind: 'advice'` 的规则不改写，只记录问题，用 `suggest` 给建议。
2. 想让提示规则给出**可整段替换的建议写法**，加 `offer: true`，并把 `suggest` 写成函数：
   ```js
   {
     id: 'ORA-NVL-NESTED',
     kind: 'advice', offer: true,
     suggest: function (m, text) {
       var call = SqlUtil.readCall(text, text.indexOf('(', m.index));
       if (!call || call.args.length !== 2) return null;
       return { before: text.slice(m.index, call.end), after: 'IFNULL(' + call.args[0] + ', ' + call.args[1] + ')' };
     }
   }
   ```
   `offer` 只影响展示与报告：建议写法**不会**写进输出 SQL，界面上标「建议写法（未自动应用）」，需人工确认后自己替换。
3. 拿不准就 `return null`，或在规则上标 `confirm: true`，不要硬改写。
4. 同一个规则命中很多次时，加 `aggregate: true` 会合并成一条「共 N 处」。
5. 复杂函数（参数不定长）用 `SqlUtil.readCall(sql, openIndex)` 解析括号，不要写贪心正则。
6. 改写规则可以用 `alt(m, text)` 兜底：当 `build` 返回 `null` 时，`alt` 给出的内容会作为「建议写法」展示，而不是静默跳过（`ORA-DECODE` 就是这么处理含子查询的情况）。

## 已知限制

- 不连接数据库、不执行 SQL，结果不能替代目标库实测。
- 不保证语义完全等价，尤其日期精度、字符长度、NULL 处理、分页顺序。
- 存储过程、触发器、动态 SQL 只识别提示，不改写。
- 规则按高频场景挑选（v1.1 共 49 条），不是全集。

## 部署

任何静态托管均可（本作品当前部署在 TRAE 部署服务）。无需环境变量、无需后端。
