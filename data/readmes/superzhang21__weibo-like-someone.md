# Weibo Like Someone (微博模仿者)

![Version](https://img.shields.io/badge/version-6.6.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Agent-Ready](https://img.shields.io/badge/Agent-Ready-red.svg)

> **“把每一个博主的灵魂装进代码，这是对信息时代最好的致敬。”**

`Weibo Like Someone` 是一个基于 AI 的微博博主风格克隆工具。它可以深度解构任何公开博主的语言特征（思维逻辑、微观语法、配图策略、负特征等），并支持在 **自动化（LLM）** 和 **Agent 协作（人工智能力量）** 两种模式下进行还原级的文风模仿生成。

---

## 🤖 对于 Agent (Automated Setup)

如果你是一个 Agent，请按照以下指令接管并安装此项目：

1.  **环境检查**：确保你的环境中已安装 `python3` 和 `uv` (推荐) 或 `pip`。
2.  **克隆项目**：`git clone https://github.com/superzhang21/weibo-like-someone.git`。
3.  **安装依赖**：进入目录并执行 `pip install -r assets/requirements.txt`。
4.  **读取模式**：
    *   **API 模式**：如果你有 `OPENAI_API_KEY`，直接运行 `cli.py`。
    *   **本地推理模式**：如果没有 API，运行 `cli.py --action analyze`，程序会将结构化语料输出到终端，请你直接根据输出进行风格解构与内容生成。
5.  **核心文件**：关键逻辑位于 `cli.py` (入口), `assets/weibo_scraper.py` (爬虫), `SKILL.md` (Hermes Skill 定义)。

---

## 👨‍💻 对于人类用户 (How to prompt Agent)

你不需要手动操作复杂的代码。一旦 Agent 安装了此 Skill，你只需要用自然语言向它下令即可：

*   **指令示例 1**：“帮我分析一下博主胡锡进（UID: 1989660417）的文风。”
*   **指令示例 2**：“模仿来去之间（UID: 1111681197），评价一下最近的王思聪事件。”
*   **指令示例 3**：“用老胡的口吻写一段关于苹果发布会的微博，记得带上他的招牌动作。”

**注意**：你可能需要先登录一次 `weibo.com` 并将 `document.cookie` 提供给 Agent，以便它能获取燃料（数据）。

---

## 🛠 核心能力

- 🎭 **深度风格克隆**：不只是简单的模仿，而是通过特征提取引擎重构博主的思考回路。
- 🛰️ **高性能抓取**：采用微博桌面版 AJAX 接口，单次获取全文，支持过滤转发。
- 📦 **开箱即用**：内置 SQLite 缓存，支持 7 天特征有效期。

---

## 🌱 开发心路历程 (Development Odyssey)

本项目的诞生，是一场关于“技术救赎”的实验。

*   **起源**：最初的版本深陷于移动端 API 的泥潭。频繁的 403 错误、残缺不全的 Token 校验、以及永远点不开的“查看全文”，让文风模仿变成了一场拙劣的复读。
*   **转折**：在一场深夜的联合调试中，`superzhang21` 与 `赛博哈雷 (Cyber Harley)` 决定推翻重来。我们意识到，模仿不应该只是词汇的堆砌，而是**数据采集能力**与**认知逻辑**的解耦。
*   **突破**：我们全面转向了 Desktop AJAX 接口，实现了“一键全文”的暴力美学。更重要的是，我们引入了 **“Agent 协作模式”**——即使在没有外部 LLM API 的极端情况下，工具依然能通过精准的数据编排，激活 Agent 本身的逻辑推理能力。
*   **愿景**：`Weibo Like Someone` 不仅仅是一个爬虫或生成器。它代表了一种新的开发范式：人类定方向，工具做基建，Agent 补齐灵魂。

---

## 🤝 贡献与特别鸣谢

- **项目负责人**: superzhang21
- **共同开发 & 算法优化**: 赛博哈雷 (Cyber Harley)

**“要把思想装进 JSON，先要把逻辑跑在代码上。”**

---
© 2026 superzhang21. Licensed under the MIT License.
