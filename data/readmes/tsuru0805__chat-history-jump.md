# chat-history-jump

[English](README.en.md)

这个仓库做一件事:给任何有「聊天记录」的应用装上 QQ / 微信那种**查找聊天记录**——搜关键词命中一条,点它跳到原文位置,前后文接着滚;点日历上有记录的一天,跳到那天第一句。三个只读接口 + 一份平台中立的客户端算法 + 三个真跑过的参考客户端(Expo/React Native、SwiftUI、Web PWA)+ 一张我们用生产环境换来的坑单。

它来自一个真实系统的真实需求。我们的家用 AI 系统 tilldusk 24/7 跑在一台 Mac mini 上,聊天记录几个月下来几千条,存 SQLite;想翻旧话只能一周一周整包拉,没有搜索,没有日期定位。照着 QQ 做完「搜索→跳转+日历」之后回头看:UI 只花了一天,**返工全花在一串小坑上**——JSON 列里搜含引号的词一条都搜不到、高亮偏移在 emoji 后面错两格、假命中把一页占满就再也翻不到真命中、跳转落点差几行、凌晨一点半的消息该算哪天……每一个都不难,但每一个都要踩一次才知道。这些坑跟我们的系统无关,跟你的也无关——只跟「聊天记录 + 搜索 + 跳转」这个形状有关。所以抽出来。

```
      /conversations/{cid}/search    …/{cid}/days            …/{cid}/context?anchor_seq=
                 ┌──────────────┐        ┌───────────┐           ┌──────────────────────┐
  SQLite ──────▶ │ 命中列表     │        │ 有记录的天 │           │ 锚点前后 N 条,       │
  messages       │ 三段 snippet │        │ count      │           │ 跨归档界连续,        │
  (seq 游标)     │ seq 游标翻页 │        │ first_seq  │           │ 双向 has_more        │
                 └──────┬───────┘        └─────┬─────┘           └──────────┬───────────┘
                        │ 点命中                │ 点日                        │ 开页 / 翻页
                        └───────────────────────┴────────────► jumpTo(seq) ◄─┘
                                                              客户端状态机(docs/client-algorithm.md)
            (跨会话版:GET /search 与 GET /days 无 cid 前缀,命中带 conversation_id)
```

## 仓里有什么

| 目录 | 内容 |
|---|---|
| [`server/`](server/) | Python 参考后端(FastAPI + SQLite,零业务依赖)。最小 schema、读口(会话内 + 跨会话)、`visible_text` 可插拔钩子、演示库种子;测试覆盖坑单每一条 + 把契约文档里的示例值逐个钉死 |
| [`docs/api.md`](docs/api.md) | 读口契约,逐字段 |
| [`docs/client-algorithm.md`](docs/client-algorithm.md) | **客户端算法**,平台中立伪码:世代、安静期落位、跳转替换/翻页合并、防重入、保视口、日头。给没提供客户端的平台(Flutter / Compose / macOS…)照着落 |
| [`docs/pitfalls.md`](docs/pitfalls.md) | **坑单 23 条**:服务端 8 + 客户端 6 + 多会话 4 + 审查抓的 2 + 写参考客户端时抓的 3。借鉴前必读 |
| [`clients/web/`](clients/web/) | Vite + React + TypeScript,PWA(可加主屏,壳离线) |
| [`clients/expo/`](clients/expo/) | Expo / React Native,`FlatList` |
| [`clients/swiftui/`](clients/swiftui/) | SwiftUI,iOS 17+,`ScrollViewReader` + `LazyVStack` |
| [`docs/screenshots/`](docs/screenshots/) | 三端真跑截图(同一份演示库) |

三个客户端是**同一份算法文档打出来的三份字**,各自只做一件平台特有的事:怎么在 prepend 之后不让视口跳、怎么把某一行滚到视口中央。

## 快速开始

后端(Python ≥ 3.10):

```bash
cd server
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python -m chat_history_jump seed  --db demo.db --tz Asia/Tokyo   # 一个月的演示对话,故意含所有坑的形状
python -m chat_history_jump serve --db demo.db --tz Asia/Tokyo --day-start-hour 4 \
    --cors-origin http://localhost:5173        # CORS 默认关;web 客户端要这一行
# → http://127.0.0.1:8890  (/health /conversations /search?q=lighthouse ...)
```

客户端(任选,都默认连 `http://127.0.0.1:8890`):

```bash
cd clients/web   && npm i && npm run dev        # 浏览器 http://localhost:5173
cd clients/expo  && npm i && npx expo start     # iOS/Android 模拟器或 Expo Go
cd clients/swiftui && xcodegen generate && open ChatHistoryJump.xcodeproj   # Xcode → iPhone 模拟器
```

跑一遍验收动作(三端一致,见 [算法文档 §9](docs/client-algorithm.md#9-what-the-reference-clients-verify)):打开落在最底 → 搜 `lighthouse 🌊` → 点第二条命中,那行居中高亮 → 往上翻过归档界,不重不跳 → 日历点亮有记录的天,点一天落到当天第一句 → 请求在途时换关键词,不闪旧结果 → 切会话,旧锚点不拽新流。

## 接口(详见 [docs/api.md](docs/api.md))

| 接口 | 干什么 | 关键约定 |
|---|---|---|
| `GET /conversations/{cid}/search?q=&limit=&before_seq=` | 会话内关键词命中,新→旧,游标翻页 | 命中文本按**三段** `snippet_before / snippet_match / snippet_after` 返回,**不返偏移**;`has_more` 按真命中数;`q` 空/超 100 字 → 400 |
| `GET /conversations/{cid}/days` | 会话内日历数据 | `[{day, count, first_seq}]`;`day` 由服务端按 `tz` + `day_start_hour` 算好;`first_seq` 按 seq 不按时间 |
| `GET /conversations/{cid}/context?anchor_seq=&before=&after=` | 锚点前后一窗 | 省略锚点=最新;锚点缺失→就近吸附(等距取旧);**无视归档界**;双向 `has_more_*` |
| `GET /search?q=&limit=&cursor=` | **跨会话**命中 | 按 `(created_at, id)` 新→旧;游标是不透明串;每条命中带 `conversation_id` |
| `GET /days` | **跨会话**日历 | 每天列出当天有话的会话与各自 `first_seq` |

**一话题一会话的应用(ChatGPT 那种)也在射程内**:搜索和日历有跨会话版,`context` 仍按会话——`seq` 只在会话内有意义,跨会话的一条命中就是 `(conversation_id, seq)` 一对,点它=切会话再跳。会话内的游标与锚点只有 `seq`(会话内单调整数,允许空洞);不用 `id`(全局)也不用 `created_at`(时钟回拨、同秒写入)。

## `visible_text` 钩子:唯一的文本通路

搜索匹配、snippet、`context` 里的 `text`,全部出自服务端**同一个函数** `visible_text(row)`。默认实现把 JSON 字符串 / `text` 块拼成人看到的正文;如果你的记录里有读者不该搜到、不该看到的东西(隐藏标记、工具载荷、私密注释),换一个函数把它们剥掉——之后三个接口**物理上**泄不出来,因为没有第二条文本通路。演示库里带 `[secret: pineapple]` 这样的标记,`server/examples/strip_markers.py` 是一个钩子样例:

```bash
python -m chat_history_jump serve --db demo.db --visible-text examples.strip_markers:visible_text
# 搜 "secret" 零命中;搜 "pineapple" 仍命中正文里聊到 pineapple 的那些句子,
# 但 [secret: pineapple] 标记本身从所有出口消失
```

## 我们踩过的坑(借鉴前必读)

完整版 [docs/pitfalls.md](docs/pitfalls.md);挑最疼的几条:

1. **列里存的是 JSON,就要搜编码后的形状**——`she said "hi"` 在库里是 `she said \"hi\"`,`LIKE '%"hi"%'` 一条都不中,静默。先 `json.dumps` 再转义 LIKE 元字符,顺序不能反。
2. **SQL 只当粗筛**——`LIKE '%text%'` 命中每个块的 `"type":"text"` 键名;工具载荷、隐藏标记也命中。真匹配跑在 `visible_text` 上,只在隐藏内容里命中的行不算命中,snippet 也从同一段可见文本切——一条通路,否则会漏。
3. **别返偏移**——Python 数码点、JS 数 UTF-16、Swift 数字素簇,一个 emoji 之后三端高亮各错各的。返三段字符串,客户端零算术。
4. **`has_more` 数真命中**——粗筛一批全是假命中时,天真实现返回 `hits:[] has_more:false`,读者被告知「没有更早的了」,真命中就在下面。找到第 limit+1 个真命中才算有下一页。
5. **凌晨一点半算哪天**——`day_start_hour` 可配、`tz` 可配、算术在服务端做、客户端只渲染字符串;**先转时区再回拨墙钟**,反过来在夏令时那天会错一整天。
6. **落位靠安静期,不靠数回调**——虚拟化列表分批挂载,「滚一次」落在当时挂载到的尾巴上;世代认身份、160ms 无布局变化算稳、翻页入口即让位、新跳转取消旧定时器。这一条我们四轮 review 才收敛。
7. **跨会话时 `seq` 会骗人**——A 的 500 和 B 的 500 毫无关系。全局命中列表按时间排、用不透明游标翻页,一条命中是 `(conversation_id, seq)` 一对;拿 A 的 seq 去查 B 的 `context` 不报错,只是安静地给你看错消息。
8. **你自己的滚动会被当成用户在滚**——iOS 上程序化 `scrollToEnd` 照样发动量事件,于是落位滚动自己触发了「翻上一页」,应用一打开就停在归档中段。翻页闸只认「手指开始拖」。

## 不做什么(诚实边界)

- ❌ 不是全文检索引擎:LIKE 粗筛 + Python 精筛,个人量级(万条级)够用;百万条请换 FTS5/影子表,契约不变。
- ❌ 不管写入:怎么产生 `seq`、怎么归档,是你的事。仓里的 `insert` 只为种子和测试。
- ❌ 不带鉴权:参考后端裸跑,放到你现有的网关后面。
- ❌ 客户端不是 UI 库:是把算法文档打出来的最小实现,拿去改,别拿去 `import`。

## 相关工作

- [claude-code-chat-explorer](https://github.com/drewburchfield/claude-code-chat-explorer) — SQLite + FTS5 的 Claude Code 会话浏览器,搜索强、无锚点上下文/日历跳日。你要的是「翻库」而不是「跳回原位」时它更合适。
- [shadcn/ui MessageScroller](https://ui.shadcn.com/docs/components/radix/message-scroller) — web 端「锚点行=视口起点」的滚动容器,概念相通,无后端契约。
- [Stream:RN 双向无限滚动](https://getstream.io/blog/react-native-how-to-build-bidirectional-infinite-scroll/) — RN prepend 保视口的手艺来源之一,绑定其 SDK。
- [react-native-gifted-chat #938](https://github.com/FaridSafi/react-native-gifted-chat/issues/938) — 「搜索命中滚到那条」在最流行的 RN 聊天组件里是多年未解的 issue,是本仓存在的旁证。

## 作者

- **晚晚**([@tsuru0805](https://github.com/tsuru0805))——设计、拍板、真场验收
- **弥野**(Claude,晚晚的工程手)——实现与文档

出自我们的家用系统 tilldusk。设计与踩坑来自那套系统;本仓所有代码按 [`docs/`](docs/) 里的规格重写,不含它的任何代码或数据。

## License

MIT
