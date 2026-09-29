# TiDB X - AI Agent Value Landing Page

A high-performance, dark-themed landing page designed to showcase the value of TiDB X for AI Agent architectures. This project highlights how TiDB X solves critical system foundation challenges for scaling AI agents, such as schema agility, isolation, and unified scaling.

## 🚀 Overview

AI Agents represent a new class of application workload that differs significantly from traditional web apps. They are long-running, stateful, and require rapid schema evolution. This landing page articulates why traditional databases fail these workloads and how TiDB X provides the necessary system foundations.

### Key Value Propositions
- **Unified Scale:** Eliminate manual sharding for unpredictable agent workflows.
- **Schema Agility:** Online DDL allows schema changes without downtime as agent capabilities evolve.
- **Native Isolation:** Isolate state explosion safely while maintaining ACID compliance.
- **SQL + Vector:** Unified context management for intelligent retrieval.

## 🛠 Tech Stack

- **Framework:** [React 19](https://react.dev/)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Icons:** [Lucide React](https://lucide.dev/)
- **Animation:** CSS Animations & Custom Scroll Reveal components

## 📂 Project Structure

```
├── components/          # React components
│   ├── Architecture.tsx     # (Internal reference/unused)
│   ├── Challenges.tsx       # "The Problem" section
│   ├── Comparison.tsx       # (Internal reference/unused)
│   ├── Footer.tsx           # Application footer
│   ├── FoundationAnimation.tsx # Hero visual element
│   ├── Hero.tsx             # Main landing section
│   ├── Icons.tsx            # SVG Icon assets
│   ├── Navbar.tsx           # Top navigation
│   ├── NeuralBackground.tsx # Dynamic background effect
│   ├── Scenarios.tsx        # Problem/Solution deep dives
│   ├── ScenarioVisuals.tsx  # SVG diagrams for scenarios
│   ├── ScrollReveal.tsx     # Animation wrapper
│   ├── Trusted.tsx          # Social proof / Logos
│   └── WhenNotToUse.tsx     # "Honest Assessment" section
├── App.tsx              # Main application entry
├── index.html           # HTML entry point
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── types.ts             # Shared type definitions
└── vite.config.ts       # Vite configuration
```

## ⚡️ Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TiDB-X-Value-For-AI-Agent
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) (or the port shown in your terminal) to view the app.

### Building for Production

To create a production build:

```bash
npm run build
```

This will generate a `dist` folder with the optimized assets ready for deployment.

## 🎨 Features & Components

- **Neural Background:** A canvas-based interactive background simulating neural connections (`NeuralBackground.tsx`).
- **Scroll Reveal:** A reusable wrapper component that triggers animations as elements enter the viewport.
- **Interactive Visuals:** SVG-based problem/solution diagrams that illustrate concepts like sharding failures and lock-free DDL (`ScenarioVisuals.tsx`).
- **Dark Mode Aesthetic:** Built with a custom dark theme using Tailwind, featuring "brand-red" accents `#FF0033`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
