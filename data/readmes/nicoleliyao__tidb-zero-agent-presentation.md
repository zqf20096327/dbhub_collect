# TiDB Zero Replay Demos

> **TiDB Zero - AI Agents Essential**
> This repository contains standalone, purely frontend browser demonstrations for the TiDB Zero Agent MVP. It replays real historic execution logs without requiring any backend services, active database connections, or LLM API keys.

This repo is ideal for quick sales pitches, presentations, and product demonstrations.

## 🌟 Available Demos

There are two primary ways to experience the power of the TiDB Zero Agent, tailored to your audience:

### 1. The Business Insights Demo 

**File**: `index_business.html`
**Target Audience**: C-Level, Business Lines, Investors.

**What it shows**:
Focuses on the *business value* and *Actionable Insights* instead of parsing raw code. The complex SQL execution logs are visually translated into a sleek, 6-step business workflow:
1. 🧠 Provision memory
2. 🌐 Gather live data
3. 🧩 Structure schemas
4. 💾 Ingest actual records
5. 💡 Execute logic
6. 🎯 Deliver insight

*Features an animated visual workflow map, real-time stage duration trackers, dynamic control (Pause/Play), and a cinematic Outro.*

### 2. The Technical Showcase Demo
**File**: `index_tech.html`
**Target Audience**: Developers, Architects, Data Engineers.

**What it shows**:
The raw, unfiltered "under the hood" power of the Agent. Simulates a terminal environment running 4 autonomous agents simultaneously. You will literally watch the agent write DDL, perform DML operations, and execute SQL analytical queries.

## 🔗 Original Source Code
This repository is an **interactive presentation layer only**. 

If you are looking for the actual Python backend, the AI Agent logic, and the CLI tool that generated these results by reasoning with live data and TiDB Zero, please visit the main repository:

👉 **[lilyjazz/agent-tidb-mvp-demo](https://github.com/lilyjazz/agent-tidb-mvp-demo)**

---

## 🚀 How to Run

Absolutely zero setup is required. 

1. Clone or download this folder.
2. Ensure you have the data asset: `unified_scenarios_data.js` located in the same directory.
3. Simply **double-click** either `index_business.html` or `index_tech.html` to open it in any modern web browser (Chrome, Edge, Safari, Firefox).
4. Use the controls at the top right to **Pause ⏸**, adjust **Speed**, or restart the simulation.

## 📊 Demonstrated Scenarios

Both demonstrations run the following scenarios concurrently to prove multitasking capabilities:

- **Market Intelligence**: TechCrunch AI Trends
- **Risk Analysis**: Global USGS Earthquake Activity
- **Supply Chain / Weather**: Tokyo 48H High-Resolution Temperature Map
- **Engineering Sentiment**: Lobste.rs Core Dev-Topic Extraction

---

## ⬆️ How to Upload to a New GitHub Repository

Since this is a standalone presentation project, you can push this specific folder to a new GitHub repository:

1. Create a new empty repository on GitHub (e.g., `tidb-zero-agent-presentation`).
2. Open your terminal, navigate to this folder (`TiDB-Zero-Replay`), and run:

```bash
git init
git add .
git commit -m "Initial commit: TiDB Zero Agent Business & Tech Demos"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git
git push -u origin main
```
