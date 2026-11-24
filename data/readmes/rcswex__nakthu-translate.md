# nakthu-translate

**A Claude skill that translates text into Nakthu (梦天语), a constructed language — faithfully, fluently, elegantly.**
**把原文（主要是中文）按「信、达、雅」译进梦天语的 Claude skill。**

[English](#english) · [中文](#中文)

> Nakthu · 梦天语 — project site / 项目主页: <https://rcswex.github.io/nakthu/>

---

## English

### What is this?

[Nakthu](https://rcswex.github.io/nakthu/) (`Nāk-θụʔ`, "human language") is an experimental constructed language built with a *sandbox method*: instead of coining words one by one, a fifty-person lakeside settlement is simulated for a hundred years, and every grammatical feature is added only when that society *has to* say something it could not say before. Its signatures:

- **A syllable is a grid point with four slots** — onset, nucleus, coda, tone. Words are read, not memorised: the slots encode texture, reachability, duration and operation.
- **Vowels run on two axes** (reachable / not, specified / not); length adds only "non-termination".
- **Evidentiality is obligatory.** An assertion must say how you know it (`-i:` seen, `-e:` heard, `-u:` felt, `-ei` hearsay …).
- **Words never translate word-for-word, but always translate.** Paths differ; landing points are shared.

This skill is a translator's workbench for that language. It makes Claude work the way the project's own translators do: read the archive, find the *landing point* of each word, choose a register, assemble short paths, check every form against the lexicon, and report honestly what was lost.

### Features

| Mode | Command | Output |
|---|---|---|
| default | `/nakthu-translate <text>` | per stanza: **Nakthu · word-by-word gloss · landing reading** |
| `-only` | `/nakthu-translate -only <text>` | **Nakthu text only** |
| `-doc` | `/nakthu-translate -doc <text>` | a **Markdown document**: original, translation, interlinear gloss, landing reading, commentary, additions & omissions, ✧ provisional-word table, proofreading notes — in the layout of the project's *遇到* and *至圣先师歌* translations |

Other options: `-style=<register>` (one of 22 registers), `-out=<path>` (for `-doc`), `-root=<path>` (archive root).

Also included:

- **Translation craft** distilled from the project's *Literature & Translation Compendium*: two laws of translation, the four-step method, the five prohibitions, "keep the image", reduplication rules, the "never say *unsayable*" discipline, a loss ledger.
- **`scripts/nakthu_lex.py`** (stdlib-only Python):
  - `lookup` — find a form or a Chinese gloss in the lexicons;
  - `check` — verify that every form is attested, one syllable per hyphen-unit, and that provisional words stay under 5 %;
  - `coin` — register newly coined **✧ words** into `_temp/新铸词列表.md` (rejects collisions and same-form/different-sense clashes; `--kind` is validated);
  - `gap` — log Chinese senses the lexicon really lacks into `_temp/缺词候选.md`, as a to-do list for the lexicon's editors.

### Requirements

1. **[Claude Code](https://docs.claude.com/en/docs/claude-code)** (CLI, desktop app or IDE extension).
2. **Python 3.8+** on `PATH` (as `python`).
That is all. **The skill is self-contained: the Nakthu archive it translates from is bundled inside** (see below). Nothing else needs to be downloaded.

### What is bundled

`skills/nakthu-translate/archive/language/` is a snapshot (2026-11-22, ≈ 2.7 MB) of the project's core knowledge, so Claude can look every word and rule up instead of guessing:

| File | Role |
|---|---|
| `_grammar_book/grammar-handbook.md` (词法手册) | **Grammar handbook** — mature Nakthu, by word class, with examples and counter-examples (authoritative) |
| `graded-dictionary.md` (分级词典) · `dictionary.md` (词典) · `provisional-ledger.md` (临时词账) | Graded lexicon (10 levels), lexicon, provisional-word ledger |
| `main-book.md` (主书) | Main book (design rationale) |
| `compendium.md` (文学与翻译汇编) | *Literature & Translation Compendium* (registers, translation craft) |
| `overview.md` · `register-samples.md` · `greetings.md` | Overview, register samples, greetings |
| `ten-lessons.md` (十课通稿) · `intro-lesson.md` (绪论课) | Ten-lesson course and introduction |
| `_zhihu/` | Model translations (*遇到*, *至圣先师歌*) used as `-doc` layout models |

File names are ASCII on purpose (Claude Chat rejects zip paths containing non-ASCII characters); the Chinese book titles are in parentheses. Authority order when sources disagree: handbook > lexicons > main book > compendium > model translations. The snapshot can be overridden: set `NAKTHU_ROOT` (or pass `-root=`) to use a live copy of the archive instead; `tools/sync_archive.ps1` refreshes the snapshot from a live archive.

### Installation

**Option A — as a Claude Code plugin (recommended for sharing)**

```text
/plugin marketplace add rcswex/nakthu-translate
/plugin install nakthu-translate@nakthu-translate
```

**Option B — as a personal skill (local, no marketplace)**

```powershell
git clone https://github.com/rcswex/nakthu-translate.git
cd nakthu-translate
powershell -ExecutionPolicy Bypass -File .\install.ps1      # Windows
# sh install.sh                                             # macOS / Linux
```

This copies `skills/nakthu-translate/` to `~/.claude/skills/nakthu-translate/`. Or copy that folder by hand.

**Option C — project-level**

Copy `skills/nakthu-translate/` into `<your-project>/.claude/skills/`.

**Option D — Claude Chat (claude.ai / the Chat tab of the desktop app)**

Chat does **not** read `~/.claude/skills`; skills are uploaded as a zip in Settings. The bundled archive makes this work even though Chat cannot see your local folders.

```bash
git clone https://github.com/rcswex/nakthu-translate.git
cd nakthu-translate
python tools/build_zip.py            # → dist/nakthu-translate.zip (about 1 MB)
```

1. In Chat open **Settings → Capabilities** and make sure **code execution and file creation** is on (the lookup/check scripts and the bundled archive are read from the sandbox).
2. Under **Skills**, **delete any older `nakthu-translate`** first, then **upload `dist/nakthu-translate.zip`**.
3. Start a new chat and try: `/nakthu-translate -only 山不走，人走。`

If Chat answers that it needs "four archive files" or asks you to attach folders, an old version is still installed — remove it and upload again. Size limits for uploaded skills are set by Anthropic and may change; if the upload is rejected, check the current limit in the Skills page.

No further setup is needed — the archive travels with the skill. *(Optional)* to use a live archive instead of the bundled snapshot:

```powershell
setx NAKTHU_ROOT "D:\path\to\Nakthu"      # Windows (new shells); the directory that contains language/
# export NAKTHU_ROOT=/path/to/Nakthu       # macOS / Linux
```

Verify:

```powershell
python "$HOME\.claude\skills\nakthu-translate\scripts\nakthu_lex.py" where
```

### Usage

```text
/nakthu-translate 你身上专属的陌生味道，是我确认你存在的目标。
/nakthu-translate -only 山不走，人走。
/nakthu-translate -doc -style=风雅体 枯藤老树昏鸦，小桥流水人家。
/nakthu-translate -doc F:\poems\遇到.txt -out=F:\out\遇到_梦天语译.md
```

Or just ask in natural language: "translate this into Nakthu", "译成梦天语".

New coinages are logged to `_temp/新铸词列表.md`: in the nearest parent of the current directory that contains a `language/` folder, else in `./_temp/`. Override with `NAKTHU_TEMP` or `--temp`; `nakthu_lex.py where` prints the resolved path.

### Repository layout

```text
.claude-plugin/
  plugin.json                  plugin manifest
  marketplace.json             single-plugin marketplace
skills/nakthu-translate/
  SKILL.md                     the skill (arguments, workflow, hard rules)
  references/
    translation-craft.md       laws, 4-step method, prohibitions, register chooser
    grammar-card.md            quick grammar card (the handbook is authoritative)
    output-formats.md          templates for the three modes + coinage list
  scripts/nakthu_lex.py        lookup / check / coin / gap
  data/backfill-glosses.md         glosses for the 37 back-filled words the lexicon body lacks
  archive/                     bundled Nakthu archive snapshot (handbook, lexicons, main book, compendium …)
tools/sync_archive.ps1         maintainer: refresh the snapshot from a live archive
tools/build_zip.py             build dist/nakthu-translate.zip for Claude Chat upload
install.ps1 · install.sh       local installers
```

### Honest limits

- `check` verifies **forms and syllable structure only**. It cannot prove a sentence grammatical; Claude is instructed to check syntax against the handbook, and to list every "extrapolated" construction in the proofreading notes.
- The skill treats the lexicon and handbook as authoritative; the example translations are *layout* models, not lexical authorities (e.g. the old 2nd person `tə́k` is superseded by `nī`).
- Quality tracks the archive: if the archive is out of date, so is the output.

### License

[MIT](LICENSE) © 2026 rcswex. The licence covers the whole repository, including the bundled Nakthu archive snapshot in `skills/nakthu-translate/archive/`.

---

## 中文

### 这是什么

[梦天语](https://rcswex.github.io/nakthu/)（Nakthu，本语自名 `Nāk-θụʔ`，「人语」）是一门基于语言决定论与**沙盒法**设计的造语：不为概念配词，而是设一个约五十人的湖畔聚落，让它走一百年，看这个社会什么时候**非说不可**，语法才长出一项。它的几个签名：

- **一格一音节，四个槽**：起首、韵核、韵尾、声调。词是读出来的，不是背出来的；
- **元音走两根轴**（够得着／够不着，指定／不指定），长音只加「不终止」；
- **断言必须作证**：说一句话，要说出你怎么知道的（`-i:` 亲眼、`-e:` 亲耳、`-u:` 亲身、`-ei` 传闻……）；
- **词永远不能逐词对译，永远可以被译出**：路径无一相同，落点是共享的。

本 skill 是这门语言的**译者工作台**：让 Claude 像项目自己的译者那样工作——先读档案，认每个词的**落点**，定文体，配短弯，逐词查词典，最后诚实交代丢了什么。

### 功能

| 模式 | 调用 | 输出 |
|---|---|---|
| 默认 | `/nakthu-translate <原文>` | 每节：**梦天语 · 逐字译 · 落点读** |
| `-only` | `/nakthu-translate -only <原文>` | **仅梦天语** |
| `-doc` | `/nakthu-translate -doc <原文>` | **MD 文档**：原文、译文、逐词直译、落点读、译解、增减与补注、✧ 临时词表、校记，体例参照《遇到_梦天语译》《至圣先师歌_梦天语译》 |

另有 `-style=<文体>`（22 体之一）、`-out=<路径>`（配合 `-doc`）、`-root=<路径>`（档案根目录）。

附带：

- **翻译手艺**，提炼自《文学与翻译汇编》：两定律、四步法、五禁例、意象照翻、叠字二分、「不写说不出」的纪律、损失清单；
- **`scripts/nakthu_lex.py`**（纯标准库 Python）：
  - `lookup` 按词形或汉义查词；
  - `check` 校验词形是否在册、连字符单元是否一格一音节、临时词占比是否 ≤ 5%；
  - `coin` 把新铸的 **✧ 词**登记到 `_temp/新铸词列表.md`（自动拦截撞形与同形两义，`--kind` 受校验）；
  - `gap` 把词典里真查不到的汉义登记到 `_temp/缺词候选.md`，作为给词典编委的待办清单。

### 前置条件

1. **[Claude Code](https://docs.claude.com/en/docs/claude-code)**（命令行、桌面应用或 IDE 扩展均可）。
2. **Python 3.8+**，命令名 `python` 在 `PATH` 中。
就这些。**skill 是自足的：翻译所依据的梦天语档案已经打包在里面**（见下），无需另行下载任何东西。

### 内置了什么

`skills/nakthu-translate/archive/language/` 是项目核心知识的快照（2026-11-22，约 2.7 MB），Claude 译写时逐词逐规则查档案，而不是凭印象：

| 文件 | 作用 |
|---|---|
| `_grammar_book/grammar-handbook.md`（词法手册） | **词法手册**：成熟梦天语，按词类查，有例有误例（权威） |
| `graded-dictionary.md`（分级词典）· `dictionary.md`（词典）· `provisional-ledger.md`（临时词账） | 分级词典（十级）、词典、✧ 临时词账 |
| `main-book.md`（主书） | 主书（设计理由） |
| `compendium.md`（文学与翻译汇编） | 《文学与翻译汇编》（文体志、翻译手艺） |
| `overview.md` · `register-samples.md` · `greetings.md` | 概况、文体样例、寒暄 |
| `ten-lessons.md`（十课通稿）· `intro-lesson.md`（绪论课） | 十课教材与绪论 |
| `_zhihu/` | 范文《遇到》《至圣先师歌》等，`-doc` 的体例范本 |

文件名特意用 ASCII（Claude Chat 上传会拒绝含中文的 zip 路径），括号里是中文书名。各来源冲突时的权威次序：词法手册 > 词典 > 主书 > 汇编 > 范文。快照可以被覆盖：设环境变量 `NAKTHU_ROOT`（或 `-root=`）即改用活档案；`tools/sync_archive.ps1` 可从活档案刷新快照。

### 安装

**方式 A：作为 Claude Code 插件（便于分享）**

```text
/plugin marketplace add rcswex/nakthu-translate
/plugin install nakthu-translate@nakthu-translate
```

**方式 B：个人 skill（本地使用，无需 marketplace）**

```powershell
git clone https://github.com/rcswex/nakthu-translate.git
cd nakthu-translate
powershell -ExecutionPolicy Bypass -File .\install.ps1      # Windows
# sh install.sh                                             # macOS / Linux
```

它会把 `skills/nakthu-translate/` 复制到 `~/.claude/skills/nakthu-translate/`；手动复制该目录也一样。

**方式 C：项目级**

把 `skills/nakthu-translate/` 复制到 `<你的项目>/.claude/skills/`。

**方式 D：Claude Chat（claude.ai，或桌面应用的 Chat 标签）**

Chat **不会**读 `~/.claude/skills`，skill 要在设置里以 zip 上传。内置档案正是为此：Chat 看不到你电脑上的文件夹，档案必须随 skill 走。

```bash
git clone https://github.com/rcswex/nakthu-translate.git
cd nakthu-translate
python tools/build_zip.py            # → dist/nakthu-translate.zip（约 1 MB）
```

1. 在 Chat 打开 **设置 → 功能（Capabilities）**，确认已开启**代码执行与文件创建**（查词、校验脚本和内置档案都要在沙盒里读取）。
2. 在 **Skills** 页面，**先删除任何旧的 `nakthu-translate`**，再**上传 `dist/nakthu-translate.zip`**。
3. 新开一个对话试：`/nakthu-translate -only 山不走，人走。`

如果 Chat 回答说需要“四份档案”或要你接入文件夹，说明装的还是旧版——删掉重传。上传 skill 的大小等限制由 Anthropic 设定，可能变化；若上传被拒，请看 Skills 页面当前的限制说明。

无需其他配置——档案随 skill 一起走。*（可选）* 想用活档案而不是内置快照时：

```powershell
setx NAKTHU_ROOT "D:\path\to\Nakthu"      # Windows（新开终端生效）；指向含 language/ 的目录
# export NAKTHU_ROOT=/path/to/Nakthu       # macOS / Linux
```

验证：

```powershell
python "$HOME\.claude\skills\nakthu-translate\scripts\nakthu_lex.py" where
```

### 使用

```text
/nakthu-translate 你身上专属的陌生味道，是我确认你存在的目标。
/nakthu-translate -only 山不走，人走。
/nakthu-translate -doc -style=风雅体 枯藤老树昏鸦，小桥流水人家。
/nakthu-translate -doc F:\poems\遇到.txt -out=F:\out\遇到_梦天语译.md
```

也可以直接说「把这段译成梦天语」。译写中新铸的词登记在 `_temp/新铸词列表.md`：取当前目录向上第一个含 `language/` 的目录下的 `_temp`，没有则取 `./_temp/`；可用 `NAKTHU_TEMP` 或 `--temp` 改；`nakthu_lex.py where` 会打印实际路径。

### 目录结构

```text
.claude-plugin/
  plugin.json                  插件清单
  marketplace.json             单插件 marketplace
skills/nakthu-translate/
  SKILL.md                     skill 本体（参数、工作流、硬规则）
  references/
    translation-craft.md       定律、四步法、禁例、文体选择表
    grammar-card.md            语法速查卡（以词法手册为准）
    output-formats.md          三种模式与新铸词列表的模板
  scripts/nakthu_lex.py        查词 / 校验 / 登记新铸词 / 登记缺词
  data/backfill-glosses.md         37 枚回补词（词典正文未收）的释义索引
  archive/                     内置梦天语档案快照（词法手册、词典、主书、汇编……）
tools/sync_archive.ps1         维护者用：从活档案刷新快照
tools/build_zip.py             打出 dist/nakthu-translate.zip，供 Claude Chat 上传
install.ps1 · install.sh       本地安装脚本
```

### 诚实的边界

- `check` 只核**词形与一格一音节**，不能证明句子合乎语法。skill 要求 Claude 对照词法手册自查语法，并把「译者往前推」的句式逐条写进校记。
- 词典与词法手册是权威；范文只是**体例**范本，不是词形权威（例如旧第二人称 `tə́k` 已由 `nī` 取代）。
- 产出质量随档案：档案旧，译文就旧。

### 许可

[MIT](LICENSE) © 2026 rcswex。许可证覆盖整个仓库，包括 `skills/nakthu-translate/archive/` 中内置的梦天语档案快照。

### 链接

- 梦天语项目主页：<https://rcswex.github.io/nakthu/>
