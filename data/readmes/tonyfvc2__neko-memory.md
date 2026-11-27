<div align="center">

<img src="assets/logo.png" width="112" alt="Neko Memory Logo" />

# 🐾 猫猫的记忆 · Neko Memory

**给 Google Antigravity 一份会自然淡忘、平时零上下文占用、带 2D/3D 可视化星图的本地长期记忆。**

**简体中文** · [English](README.en.md)

![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)
![SQLite Built-in](https://img.shields.io/badge/storage-local%20SQLite-6366f1)
![Antigravity Plugin](https://img.shields.io/badge/Antigravity-Native%20Plugin-a855f7)
![License: MIT](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## ✨ 为什么做这个插件？

在 Google Antigravity 里聊得越久，上下文窗口越挤；开新对话或 `/compact` 压缩后，之前定好的偏好、项目路径、踩过的坑往往就会被忘掉。

**Neko Memory（猫猫的记忆）** 是一个 **100% 本地运行、零第三方依赖、无需额外 API Key** 的原生 Antigravity 插件：

- **🌌 2D / 3D 可视化记忆星图**：内置原生 Sidecar 面板，支持 **2D 力导向星座图** 与 **3D 球面星空** 一键切换（拖拽旋转、滚轮缩放、点击星辰聚焦并高亮关联星座与连线理由），附带 **深空星图 / 液态玻璃 / 暖光书页** 三套主题。
- **⏳ 会自然淡忘（智能半衰期）**：每条记忆都有「鲜活度」，随时间按半衰期柔和衰减——不删除，只是权重变低；再次被召回时会自动唤醒刷新鲜活度。
- **🔍 平时零上下文占用，按证据精准召回**：不会把全部记忆塞进每轮对话，只在相关时通过中文二/三元组分词 + IDF 证据权重检索最相关的 3–5 条注入。
- **🧠 跨会话不失忆 & 自动去重**：通过本地 SQLite 永久保存在 `~/.gemini/antigravity/neko_memory/memory.db`，Antigravity 客户端升级也不会丢失；写入高相似度记忆时自动合并更新。
- **📂 支持导入旧笔记**：可直接扫描本地 `.md` / `.txt` 笔记批量导入长期记忆。

---

## ⏳ 按分类智能默认半衰期

| 分类 (`category`) | 说明 | 默认半衰期 | 备注 |
| :--- | :--- | :---: | :--- |
| `preference` | 核心偏好（称呼、语言风格、习惯） | **365 天** | 重要度默认 5，支持在面板一键切换 180 / 365 天 |
| `decision` | 重要架构 / 方案决策 | **90 天** | 避免反复推翻既有决定 |
| `pitfall` | 踩坑记录与解决方案 | **90 天** | 防止下次踩进同一个坑 |
| `project` | 项目路径、结构与约定 | **60 天** | 跨会话无缝接手项目 |
| `fact` | 一般事实与环境信息 | **30 天** | 自然淡忘 |
| `handoff` | 长对话交接摘要 | **14 天** | 适合 `/compact` 或开新对话前归档进度 |

---

## 🚀 安装方式

### 方式一：Antigravity CLI 一键安装（推荐）

```bash
agy plugin install https://github.com/<你的用户名>/neko-memory
```

### 方式二：Windows 一键安装（无需单独安装 Node.js）

1. 下载本仓库源码或最新 Release 压缩包并解压；
2. 双击运行 **`install.bat`**（会自动检测系统 Node.js 22.5+；如果没有安装 Node.js，会自动复用 Antigravity 内置的 `agy-node.cmd`！）；
3. 重启 Antigravity 或开启新对话即可生效。

卸载只需双击 **`uninstall.bat`**（不会删除你的本地记忆数据库）。

### 方式三：macOS / Linux 一键安装

```bash
git clone https://github.com/<你的用户名>/neko-memory.git
cd neko-memory
chmod +x install.sh && ./install.sh
```

---

## 🛠️ 提供的 MCP 工具

安装后，Antigravity Agent 会自动获得以下 5 个本地工具：

| 工具名 | 功能说明 |
| :--- | :--- |
| `neko_memory_recall` | 按中文/英文自然语言检索最相关的记忆（带相对时间与鲜活度） |
| `neko_memory_remember` | 写入长期记忆（自动按分类配置半衰期并合并高相似重复项） |
| `neko_memory_forget` | 软归档指定 ID 的记忆（可在星图面板中随时恢复） |
| `neko_memory_list` | 列出活跃/归档记忆与数据库统计 |
| `neko_memory_import_file` | 从本地 `.md` / `.txt` 文件批量导入记忆 |

### 打开记忆星图面板

在 Antigravity 对话中直接说 **「打开猫猫的记忆星图面板」**，或点击侧边栏的 **猫猫的记忆** 即可打开 2D/3D 交互式星图！

你也可以在本地单独预览星图面板：
```bash
npm run preview:panel
# 访问 http://127.0.0.1:8789
```

---

## 🔒 隐私与数据安全

- **100% 本地运行**：不发起任何外部网络请求，不需要任何 API Key。
- **零外部依赖**：仅使用 Node.js 22.5+ / 24 内置的 `node:sqlite` 与标准库。
- **数据完全归你所有**：所有记忆存储在 `~/.gemini/antigravity/neko_memory/memory.db`，随时可备份、导出或删除。

---


## 📄 License

[MIT](LICENSE)
