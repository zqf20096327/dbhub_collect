<div align="center">

  <h1>🎓 Tidbit AI</h1>
  <p><strong>Transform static PDFs into interactive, AI-powered courses with adaptive tutoring, dynamic feeds, and gamified learning.</strong></p>

  [![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
  [![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)](https://www.mongodb.com/)
  [![Anthropic](https://img.shields.io/badge/AI-Claude%203.5-purple?style=for-the-badge&logo=anthropic)](https://www.anthropic.com/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

  <br />

  [Explore Features](#-key-features) • [Tech Stack](#-tech-stack) • [System Architecture](#-system-architecture) • [Getting Started](#-getting-started) • [Project Structure](#-project-structure) • [Team](#-author--team)

</div>

---

## 📌 Overview

**Tidbit AI** is an intelligent learning ecosystem designed to revolutionize educational content delivery. Teachers upload course PDFs or repository materials, and Tidbit's AI engine automatically parses them into structured chapters, interactive quizzes, dynamic learning targets, and real-time Claude-powered AI tutoring.

For students, Tidbit delivers an adaptive micro-learning feed featuring **stamina-based card lengths**, **prerequisite curriculum graph depth**, **zero-friction active recall speed-breakers**, and **background pre-fetching** to ensure a seamless, zero-latency learning experience.

---

## ✨ Key Features

### 👩‍🏫 For Teachers
* **⚡ Instant PDF-to-Course**: Converts raw PDFs into structured modules, chapters, and dynamic lesson plans.
* **🎯 AI Content Generation**: Auto-generates learning objectives, interactive assessments, and reflection questions.
* **📊 Analytics Dashboard**: Monitor student progress, engagement patterns, and quiz performance metrics.
* **✏️ Modular Course Management**: Easily edit, organize, and publish course content with customizable tools.

### 👨‍🎓 For Students
* **📱 Adaptive Length Feed**: Content dynamically scales from quick 2-line quotes to deep articles based on reading stamina.
* **🗺️ Curriculum Depth Graph**: Prerequisite-driven depth progression across multiple niches with interleaved topic feeds.
* **⚡ Active Recall Speed-Breakers**: Scroll-locking MCQ pop-ups with immediate green/red feedback and auto-injected refresher cards.
* **💬 Claude AI Tutor**: Integrated 24/7 AI assistant offering step-by-step explanations and instant Q&A.
* **🎮 Gamified Progression**: Earn XP, build streak multipliers, unlock achievements, and level up on a Duolingo-style visual roadmap.
* **🔄 Spaced Repetition (SRS)**: Smart review schedules optimized for long-term memory retention.

---

## 🛠 Tech Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | **Next.js 14** (App Router) | React framework with Server Actions & SSR |
| **Language** | **TypeScript** | Type-safe enterprise code structure |
| **Database** | **MongoDB & Mongoose** | Document storage for courses, users, analytics & feeds |
| **Authentication** | **NextAuth.js** | Secure session-based authentication |
| **AI Engine** | **Anthropic Claude API** | `claude-3-5-sonnet` model integration |
| **Styling & UI** | **Tailwind CSS + Lucide Icons** | Responsive, modern dark/light interface design |

---

## ⚙️ System Architecture

```text
 ┌────────────────┐      ┌─────────────────────────┐      ┌────────────────────────┐
 │ Teacher PDFs   │ ───► │  Claude AI Parsing Engine│ ───► │ Structured Course Data │
 └────────────────┘      └─────────────────────────┘      └────────────────────────┘
                                                                       │
 ┌────────────────┐      ┌─────────────────────────┐                   │
 │ Student Feed   │ ◄─── │ Adaptive Engine Loop    │ ◄───────────────────┘
 └────────────────┘      └─────────────────────────┘
        │                             │
        ├─► Stamina Length Scaling    ├─► Active Recall Speed-Breakers
        ├─► Interleaved Topic Queue   ├─► Background Pre-fetch Buffer
        └─► Duolingo Visual Roadmap   └─► AI Tutor Guidance & SRS
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** >= 18.0.0
- **MongoDB** instance (Local or MongoDB Atlas)
- **Anthropic API Key** (for Claude AI capabilities)

---

### Quick Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChiragSharma/Tidbit.git
   cd Tidbit
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure Environment Variables**  
   Create a `.env.local` file in the root directory:
   ```env
   # Database Connection
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/Tidbit?retryWrites=true&w=majority

   # Authentication
   NEXTAUTH_URL=http://localhost:3000
   NEXTAUTH_SECRET=your_nextauth_secret_key

   # Anthropic AI Integration
   ANTHROPIC_API_KEY=sk-ant-your-api-key
   ```

4. **Launch Development Server**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📁 Project Structure

```text
src/
├── app/                    # Next.js App Router routes & pages
│   ├── (auth)/             # Login & Registration flows
│   ├── (dashboard)/        # Role-protected dashboard routes
│   │   ├── student/        # Student feed, learning path & analytics
│   │   └── teacher/        # Course creation & student analytics
│   └── api/                # REST API endpoints & Anthropic handlers
├── components/             # Reusable UI modules & interactive components
│   ├── feed/               # Adaptive cards, speedbreakers & milestone UI
│   ├── interactive/        # Quiz & assessment widgets (MCQ, Code, Reflection)
│   ├── layouts/            # Navigation bar, sidebars & footers
│   ├── roadmap/            # Duolingo-style visual learning path
│   └── ui/                 # Core design system primitives (Buttons, Modals, Badges)
├── hooks/                  # Custom React hooks (Stamina timer, Buffer manager, Trigger)
├── lib/                    # Core utilities, AI services & database models
│   ├── ai/                 # Anthropic SDK batch & feed generators
│   ├── auth/               # NextAuth authentication setup
│   ├── curriculum/         # Graph engine & multi-niche interleaving logic
│   └── db/                 # Mongoose schemas & MongoDB connection
└── types/                  # TypeScript interface definitions
```

---

## 📊 Environment Variables Reference

| Variable | Required | Description |
| :--- | :---: | :--- |
| `MONGODB_URI` | **Yes** | MongoDB Atlas or local connection URI string |
| `NEXTAUTH_URL` | **Yes** | Application root URL (`http://localhost:3000` in dev) |
| `NEXTAUTH_SECRET` | **Yes** | Secret key for encrypting NextAuth session JWT tokens |
| `ANTHROPIC_API_KEY` | **Yes** | Anthropic Claude API key for automated course generation |

---

## 👤 Author & Team

* **Chirag Sharma** — CEO & Lead Developer ([@ChiragSharma](https://github.com/ChiragSharma-DEV))
* **Aafreen Khan** — Founder & Product Lead
* **Arohi Kate** — Co-Founder & AI Research
* **Parth Jakar** — CTO & Full-Stack Lead

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.