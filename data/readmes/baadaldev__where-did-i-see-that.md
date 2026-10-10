# WhereDidISeeThat (wdist) 🧠

<p align="center">
  <b>Local-first, privacy-focused semantic memory for everything you copy, read, and bookmark.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-emerald?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Zero--Cloud-100%25%20Offline-success?style=flat-square" alt="Offline">
  <img src="https://img.shields.io/badge/Dependencies-Zero%20External-blue?style=flat-square" alt="Zero Dependencies">
</p>

---

## 💡 The Problem

We copy and read hundreds of links, commands, and snippets every single day:
- *"What was that ffmpeg command I used last Tuesday to compress a 4K video?"*
- *"Where was that GitHub repo link I copied from Discord?"*
- *"What was the exact docker compose flag for Redis?"*

Traditional clipboard managers either:
1. Flood you with thousands of unsorted lines.
2. Require exact keyword matches (which you often don't remember).
3. Send your data to cloud servers.
4. Risk saving sensitive secrets like API tokens and passwords.

**`WhereDidISeeThat` (wdist)** solves this by giving your machine an **intelligent, privacy-shielded memory** that understands *what* you're looking for, even when you don't remember the exact syntax.

---

## ✨ Features

- 🧠 **Hybrid Search Engine:** Combines SQLite FTS5 (BM25) full-text search with fuzzy semantic token matching and snippet highlighting.
- 🛡️ **Zero-Leak Privacy Guard:** Automatically detects and blocks API tokens (GitHub, OpenAI, AWS, Slack), JWTs, private keys, and credit cards before they ever touch your disk.
- 🏷️ **Smart Auto-Classification:** Automatically tags and categorizes snippets into `Command`, `Code`, `URL`, `JSON`, and `Notes`.
- ⚡ **Background Clipboard Watcher:** Silently runs in the background, logging snippets without interrupting your workflow.
- 🌐 **Modern Web Dashboard:** Embedded, responsive dark-mode dashboard (with zero npm/pip dependencies required).
- ⌨️ **Snappy CLI:** Search, copy-back, pin, and manage everything directly from your terminal.

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[Clipboard / User Input] --> B{Privacy Guard}
    B -- Contains Secret --> C[🚫 Blocked & Ignored]
    B -- Safe Content --> D[Classifier & Tagger]
    D --> E[(Local SQLite + FTS5)]
    E --> F[Hybrid Search Engine]
    F --> G[⚡ CLI: wdist search]
    F --> H[🌐 Web Dashboard]
```

---

## 🚀 Quick Start

### 1. Installation

Clone and install directly in editable mode:

```bash
git clone https://github.com/baadaldev/where-did-i-see-that.git
cd where-did-i-see-that
pip install -e .
```

*(Note: `wdist` works using Python standard libraries out of the box — zero heavy external packages required!)*

---

### 2. Basic Usage

#### 🔍 Search your memory:
```bash
wdist search "ffmpeg compress video"
```
```text
Found 2 matching memories:

  [1] COMMAND [command,ffmpeg]
      > ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4

  [2] URL [github,url]
      > https://github.com/baadaldev/where-did-i-see-that

Copy item # to clipboard (or press Enter to skip): 1
[+ Copied item #1 to system clipboard!]
```

#### ✍️ Add a snippet or note manually:
```bash
wdist add "docker run -d -p 6379:6379 --name redis-cache redis:alpine"
```

#### 🛡️ Test the Privacy Guard:
```bash
wdist add "export GITHUB_TOKEN=ghp_secrettokenvalue12345678901234567890"
# Output: [Privacy Guard] Blocked: Content contains sensitive data (GitHub Token)!
```

#### 📡 Start Background Clipboard Watcher:
```bash
wdist monitor
```

#### 🌐 Open Web Dashboard:
```bash
wdist web
# Opens http://127.0.0.1:5432 in your browser automatically!
```

#### 📊 View Statistics:
```bash
wdist stats
```

#### 💾 Export Memories:
```bash
wdist export --output my_backup.json
```

---

## 🛠️ CLI Command Reference

| Command | Description |
| :--- | :--- |
| `wdist search <query>` | Search your stored memories with smart ranking |
| `wdist search <query> --type command` | Filter results by type (`command`, `code`, `url`, `json`, `text`) |
| `wdist add <text>` | Store a new snippet or note manually |
| `wdist monitor` | Run background clipboard listener |
| `wdist web [--port 5432]` | Launch the browser-based dark dashboard |
| `wdist stats` | View total clips, types, and database location |
| `wdist export [-o file.json]` | Export clips to JSON format |
| `wdist clear` | Clear stored memories |

---

## 🔒 Privacy & Security

`WhereDidISeeThat` was built under the philosophy of **complete data sovereignty**:
- **100% Offline:** Zero telemetry, zero analytics, zero external network requests.
- **Local Storage:** All memories reside on your machine in `~/.wdist/clips.db`.
- **Pre-Storage Filter:** Secrets and tokens are rejected before writing to database.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

Developed with ❤️ by **[Md Rakibul Islam (Baadal)](https://github.com/baadaldev)**

<p align="left">
  <a href="https://github.com/baadaldev" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-baadaldev-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile" />
  </a>
  &nbsp;
  <a href="https://www.hackerrank.com/profile/badolrakib1" target="_blank">
    <img src="https://img.shields.io/badge/HackerRank-badolrakib1-2EC866?style=for-the-badge&logo=hackerrank&logoColor=white" alt="HackerRank Profile" />
  </a>
  &nbsp;
  <a href="https://leetcode.com/u/Baadal89131/" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-Baadal89131-FFA116?style=for-the-badge&logo=leetcode&logoColor=black" alt="LeetCode Profile" />
  </a>
</p>

<p align="left">
  <a href="https://www.hackerrank.com/profile/badolrakib1" target="_blank">
    <img src="https://hackerrank-stats.vercel.app/api?username=badolrakib1" alt="HackerRank Badges & Stats" />
  </a>
</p>

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

