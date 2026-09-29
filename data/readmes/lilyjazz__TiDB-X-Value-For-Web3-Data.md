# TiDB X - Web3 Data Consolidation

A modern, high-performance landing page showcasing the power of **TiDB** for Web3 data consolidation. This project visualizes how TiDB's HTAP (Hybrid Transactional and Analytical Processing) architecture solves critical challenges in blockchain data management, such as event floods, schema evolution, and massive storage costs.

## 🚀 Overview

The decentralized web generates terabytes of data across fragmented chains. **TiDB X for Web3** consolidates this on-chain and off-chain data into a single, scalable SQL layer. This application acts as a compelling visual narrative (or "explainable interactive") for developers and architects.

### Key Value Propositions
*   **Unified Data**: Query Ethereum, Solana, Polygon, and off-chain user data in one SQL query.
*   **Massive Scale**: Handle millions of events per hour with linear scalability.
*   **Cost Efficiency**: Tiered storage architecture (Hot/Cold) to manage tens of terabytes without cost explosion.

## ✨ Features

*   **Interactive SQL Terminal**: A simulated "TiDB Cloud SQL Editor" allowing users to run sample queries against blockchain datasets (e.g., \`ethereum.transactions\`).
*   **Dynamic Visualizations**:
    *   **"What Breaks First"**: Breakdown of traditional database failures under Web3 loads.
    *   **Scenario Cards**: A/B comparison of legacy architectures vs. TiDB X.
*   **Modern UX/UI**:
    *   Fully responsive design using **Tailwind CSS**.
    *   Glassmorphism effects and gradient typographies.
    *   Scroll-triggered animations (\`ScrollReveal\`) for engaging storytelling.
    *   Animated background elements (floating crypto logos, glowing blobs).

## 🛠 Tech Stack

*   **Framework**: [React](https://react.dev/) (v19)
*   **Build Tool**: [Vite](https://vitejs.dev/)
*   **Language**: [TypeScript](https://www.typescriptlang.org/)
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/) (Currently configured via CDN for rapid prototyping)
*   **Icons**: [Lucide React](https://lucide.dev/)

## 🏃‍♂️ Getting Started

Follow these steps to run the project locally.

### Prerequisites
*   Node.js (v18 or higher recommended)
*   npm or yarn

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/lilyjazz/TiDB-X-Value-For-Web3-Data.git
    cd TiDB-X-Value-For-Web3-Data
    ```

2.  **Install dependencies**
    ```bash
    npm install
    ```

3.  **Run the development server**
    ```bash
    npm run dev
    ```
    Open [http://localhost:3000](http://localhost:3000) (or the port shown in your terminal) to view the app.

4.  **Build for Production**
    ```bash
    npm run build
    ```

## 📂 Project Structure

```text
├── components/          # UI Components
│   ├── Hero.tsx         # Main landing area with animations
│   ├── TerminalDemo.tsx # Interactive SQL editor simulation
│   ├── ChallengesSection.tsx # "Event Flood" problem statement
│   ├── ScenariosSection.tsx  # Detailed architectural comparisons
│   └── ...
├── App.tsx              # Main application entry
├── index.html           # HTML entry point (contains Tailwind config)
└── vite.config.ts       # Vite configuration
```

## 📄 License

This project is licensed under the MIT License.
