# qq-bak-chat-history-export

**QQ聊天记录， bak文件解码导出工具 — 将 QQ / NTQQ 聊天记录转换为 Agent 可读的 TXT、JSON、CSV**

Python 3 · SQLite · SQLCipher 工作流 · NTQQ `nt_msg.db` · Codex Skill · 本地处理

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-supported-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![GitHub Stars](https://img.shields.io/github/stars/zywstudy123/qq-bak-chat-history-export?style=flat-square&logo=github)](https://github.com/zywstudy123/qq-bak-chat-history-export/stargazers)

[快速开始](#快速开始) · [主要功能](#主要功能) · [真实 bak 文件流程](#真实-bak-文件流程) · [输出格式](#输出格式) · [安装为 Codex Skill](#安装为-codex-skill) · [English](README_EN.md)

---

## 项目定位

`qq-bak-chat-history-export` 用于把 QQ 旧版 `.bak` 聊天记录备份、已导入 QQ 的历史聊天记录、或已解密的 NTQQ 本地数据库导出为文本和结构化文件。

适用场景：

| 场景 | 说明 |
|---|---|
| QQ bak 文件无法直接阅读 | 通过 QQ 官方导入后，从本地 NTQQ 数据库导出 |
| 聊天记录只能在 QQ 内查看 | 将目标群聊或私聊导出为 `txt/json/csv` |
| 需要 AI agent 读取聊天记录 | 输出 agent 友好的文本、结构化 JSON 和表格 CSV |
| 需要筛选重点消息 | 支持关键词、日期、导入前后差异文件 |

## 主要功能

| 功能 | 状态 |
|---|---|
| QQ bak 文件导入后的聊天记录导出 | 支持 |
| NTQQ `nt_msg.db` 消息读取 | 支持 |
| 群聊导出 | 支持 |
| 私聊导出 | 支持 |
| `TXT` 可读文本 | 支持 |
| `JSON` 结构化消息 | 支持 |
| `CSV` 表格文件 | 支持 |
| 日期过滤 | 支持 |
| 关键词命中导出 | 支持 |
| 导入前后新增消息对比 | 支持 |
| 合成测试数据 | 支持 |

## 快速开始

先用合成数据验证脚本，不需要真实 QQ 账号、真实 bak 文件或真实聊天数据库。

```bash
git clone https://github.com/zywstudy123/qq-bak-chat-history-export.git
cd qq-bak-chat-history-export

python3 skills/qq-bak-chat-history-export/scripts/create_synthetic_ntqq_fixture.py \
  --out-dir /tmp/ntqq-fixture

python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /tmp/ntqq-fixture \
  --list-groups

python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /tmp/ntqq-fixture \
  --chat-type group \
  --peer 123456 \
  --self-uin 100000 \
  --out-dir /tmp/ntqq-export \
  --prefix synthetic \
  --keywords onboarding \
  --date 2023-11-14
```

预期输出：

```text
synthetic_full.txt
synthetic_full.json
synthetic_full.csv
synthetic_summary.txt
synthetic_daily_counts.csv
synthetic_keyword_hits.txt
synthetic_keyword_hits.json
synthetic_keyword_hits.csv
synthetic_2023-11-14.txt
synthetic_2023-11-14.json
synthetic_2023-11-14.csv
```

## 真实 bak 文件流程

```text
QQ .bak 文件
    ↓
QQ 官方导入历史聊天记录
    ↓
本机 NTQQ nt_db 数据库
    ↓
本地解密为 SQLite
    ↓
导出 TXT / JSON / CSV
    ↓
交给 agent 搜索、总结、整理
```

操作步骤：

1. 登录能导入该备份的 QQ 账号。
2. 在 QQ 的聊天记录管理界面导入 `.bak` 文件。
3. 打开目标群聊或私聊一次，让 QQ 加载消息。
4. 找到本机 NTQQ 的 `nt_db` 目录。
5. 使用本地解密工具把数据库解密成普通 SQLite 文件。
6. 对解密后的目录运行本项目导出脚本。

解密后的目录通常包含：

```text
nt_msg.db
group_info.db
profile_info.db
```

## 导出命令

列出群聊：

```bash
python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /path/to/decrypted_nt_db \
  --list-groups \
  --query "关键词"
```

导出一个群聊：

```bash
python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /path/to/decrypted_nt_db \
  --chat-type group \
  --peer GROUP_UIN \
  --self-uin YOUR_UIN \
  --out-dir /path/to/output \
  --prefix group_export \
  --keywords "入职,体检,宿舍" \
  --date YYYY-MM-DD
```

导出一个私聊：

```bash
python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /path/to/decrypted_nt_db \
  --chat-type c2c \
  --peer TARGET_NT_UID_OR_UIN \
  --self-uin YOUR_UIN \
  --out-dir /path/to/output \
  --prefix c2c_export
```

导出导入后新增消息：

```bash
python3 skills/qq-bak-chat-history-export/scripts/export_ntqq_chat.py \
  --db-dir /path/to/post_import_decrypted_nt_db \
  --pre-msg-db /path/to/pre_import/nt_msg.db \
  --chat-type group \
  --peer GROUP_UIN \
  --out-dir /path/to/output \
  --prefix group_after_import
```

## 输出格式

| 文件 | 用途 |
|---|---|
| `<prefix>_full.txt` | 按时间排序的完整聊天文本 |
| `<prefix>_full.json` | 适合 agent 和脚本读取的结构化消息 |
| `<prefix>_full.csv` | 适合 Excel、Numbers、数据库导入的表格 |
| `<prefix>_summary.txt` | 消息数量、时间范围、参与者数量 |
| `<prefix>_daily_counts.csv` | 每日消息数量统计 |
| `<prefix>_keyword_hits.*` | 关键词命中结果 |
| `<prefix>_<date>.*` | 指定日期的消息 |
| `<prefix>_new_after_import.*` | 导入后新增消息 |

## 安装为 Codex Skill

本仓库同时提供可安装的 Codex Skill。安装后可以让本地 agent 自动执行 QQ bak 聊天记录导出流程。

```bash
mkdir -p ~/.codex/skills
cp -R skills/qq-bak-chat-history-export ~/.codex/skills/
```

使用示例：

```text
使用 $qq-bak-chat-history-export，把这个已解密 NTQQ 数据库里的群聊导出为 txt/json/csv。
```

## 目录结构

```text
qq-bak-chat-history-export/
├── README.md
├── README_EN.md
├── LICENSE
└── skills/
    └── qq-bak-chat-history-export/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/schema.md
        └── scripts/
            ├── create_synthetic_ntqq_fixture.py
            └── export_ntqq_chat.py
```

## 常见问题

| 问题 | 回答 |
|---|---|
| 能直接把 `.bak` 转成 txt 吗 | 推荐先用 QQ 官方导入 `.bak`，再从本机 NTQQ 数据库导出 |
| 支持群聊吗 | 支持，使用 `--chat-type group` |
| 支持私聊吗 | 支持，使用 `--chat-type c2c` |
| 输出能给 AI agent 读取吗 | 可以，推荐使用 `txt` 和 `json` |
| 会上传聊天记录吗 | 不会，脚本默认只读写本地文件 |
| 是否需要数据库解密 | 如果 NTQQ 数据库仍是加密状态，需要先本地解密 |

## 开发者与贡献者

维护者：[@zywstudy123](https://github.com/zywstudy123)

欢迎提交 Issue 和 Pull Request，尤其是以下方向：

| 方向 | 说明 |
|---|---|
| 新 QQ / NTQQ 版本适配 | 更新字段映射和消息体解析 |
| 更多消息类型解析 | 图片、文件、引用、语音转写、卡片消息 |
| 跨平台路径说明 | macOS、Windows、Linux 的 NTQQ 数据目录 |
| 导出格式增强 | Markdown、HTML、Parquet、SQLite |

## 致谢

| 项目 / 工具 | 用途 |
|---|---|
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Codex Skills 仓库结构参考 |
| [zhaoxinyi02/ClawPanel](https://github.com/zhaoxinyi02/ClawPanel) | 开源项目 README 组织方式参考 |
| [SQLite](https://sqlite.org/) | 本地数据库读取 |
| [SQLCipher](https://www.zetetic.net/sqlcipher/) | NTQQ 加密数据库解密工作流 |

## 免责声明

本项目仅用于导出和整理使用者有权访问的本机聊天记录备份。请遵守当地法律法规、平台服务条款和数据授权边界。项目不提供 QQ 官方服务，不隶属于腾讯，不对任何账号、数据或法律后果承担责任。

## License

[MIT](LICENSE) © 2026
