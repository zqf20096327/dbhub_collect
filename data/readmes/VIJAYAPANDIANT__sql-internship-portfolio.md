# 📊 Interactive SQL Internship Portfolio

Welcome to the source code of my **SQL & Database Engineering Internship Portfolio**! This is a premium, interactive, and fully responsive Single Page Application (SPA) dashboard designed to showcase all my database architectures, SQL tasks, index optimizations, and query designs.

---

## 🎨 Portfolio Features

- **Dynamic Data Aggregator (`generate_data.py`):** Automatically scans and parses my commit directories, reads SQL files, processes markdown README docs, and compiles them into a unified dataset (`data.js`) while sanitizing metadata.
- **Glassmorphic Dark Mode UI:** Built using Vanilla CSS grid/flex layouts, CSS custom variables, floating neon glow elements, and modern typography (Outfit & Inter fonts).
- **Relational Query Explorer:** An editor-like interface displaying syntax-highlighted SQL scripts (powered by **Prism.js**) with a "Copy to Clipboard" feature.
- **Simulated SQL Console Terminal:** Click **"Run Query Simulator"** on any script to watch a simulated database execute it, complete with execution latency statistics and realistic HTML tabular results.
- **Markdown Documentation Viewer:** Renders specific project documentation files on-the-fly (powered by **Marked.js**), including custom styling overrides for tables and GitHub-style alerts.

---

## 🛠️ Technology Stack

- **Core Structure:** HTML5
- **Styling & Theme:** Vanilla CSS3 (Glassmorphism design language)
- **Application Logic:** JavaScript (ES6+)
- **Parser Compiler:** Python 3.x
- **Libraries (via CDN):**
  - **Prism.js:** High-fidelity SQL syntax highlighting
  - **Marked.js:** Lightweight markdown parser
  - **Font Awesome 6.4.0:** Vector design icons
  - **Google Fonts:** Outfit (headings), Inter (body), JetBrains Mono (code editor)

---

## 🚀 How to Run Locally

### 1. Launch the Server
Since the website dynamically fetches files and scripts, it is best run on a local HTTP server. Open your terminal in this directory and execute:
```powershell
python -m http.server 8000
```
Then, open your browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

### 2. Regenerate Project Data
If you add new `.sql` scripts or update the README files inside any of your internship folders, run the compiler script to update the portfolio database:
```powershell
python generate_data.py
```

---

## 📁 Folder Structure
```text
SQL-Internship-Portfolio/
├── index.html          # Web application structure
├── style.css           # Custom Glassmorphic styles
├── script.js           # UI logic, filters, and SQL simulator
├── data.js             # Automatically compiled SQL and markdown database
├── generate_data.py    # Python crawler script to compile data.js
├── clean_git.py        # Helper to clean nested submodules
└── README.md           # This documentation file
```

---
<div align="center">
  Developed with ❤️ by <b>Vijayapandian T</b>
</div>
