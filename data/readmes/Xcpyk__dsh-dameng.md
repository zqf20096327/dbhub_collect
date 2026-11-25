# dsh-dameng

**在 DeepSeek Harness 对话里完成 140 题人生调研，并把回答蒸馏成数字人档案。**

Host-only DSH plugin. It adds five tools and stores answers locally; there is no separate web page.

## Tools

| Tool | Purpose |
| --- | --- |
| `dameng_status` | progress, chapter coverage, next question ids |
| `dameng_guide` | interview protocol: one question at a time, follow-ups, safety |
| `dameng_questions` | fetch next questions by chapter / core / deep / all |
| `dameng_answer` | record an answer verbatim, or skip |
| `dameng_export` | write life archive, distillation brief, coverage report, backup, next steps |

Try saying: **“开始大梦访谈”**. The agent reads the guide, asks one question, records the answer, and continues.

## Languages

Chinese, English, 日本語, 한국어. Questions, prompts, exports and file names follow the language passed to the tools (default Chinese).

## Data and privacy

- Answers: `$DSH_HOME/dameng/answers.json` (normally `~/.dsh/dameng/answers.json`)
- Exports: `$DSH_HOME/dameng/exports/`
- No network, no credentials, no web routes. The plugin never reads the workspace or Git history.
- `DAMENG_DATA_DIR` can move the data directory.
- Do not commit the answer file. It is outside this repository by default.

## Install

Once listed in the Open Plugin Market, install from **Plugins → Discover**. For local development:

1. Open **Plugins → Add plugin**.
2. Choose this repository directory (the directory containing `package.json`).
3. Restart DSH if the plugin row does not appear immediately.

The package declares `dsh.bundle.patch`; the patch inserts the `dameng` row.

## Limits

This is a self-reflection tool, not a psychological assessment or diagnosis. The digital twin is a mirror, not a stand-in: do not use it to impersonate the person in promises, signatures, payments or manipulation. For self-harm, suicide or violence, stop and contact a trusted person or local emergency services (mainland China: 12356).

## License

MIT. See [LICENSE](LICENSE).
