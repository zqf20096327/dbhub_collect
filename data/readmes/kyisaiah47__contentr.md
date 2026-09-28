<div align="center">

<img src="assets/banner.png" alt="banner" width="100%" />

# ✍️ Contentr

**AI content strategy engine — from idea to published, fully automated with vector-powered insights**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![TiDB](https://img.shields.io/badge/TiDB_Serverless-CC0200?style=for-the-badge&logo=pingcap&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

</div>

<br/>

Contentr is an end-to-end autonomous content marketing engine that ingests social signals, runs cosine-similarity vector search against TiDB Serverless to surface content gaps, and generates AI-driven content calendars — all without manual intervention. From trend discovery to publishing via Buffer/Hootsuite and Slack notifications, every step in the workflow is automated and continuously refined using GPT-4 insights.

## ✨ Features

- **Vector-Powered Gap Analysis** — TiDB Serverless cosine similarity (`VEC_COSINE_DISTANCE`) surfaces under-served topics across your niche in real time
- **Autonomous 6-Step Agent** — Ingestion → vector search → AI analysis → strategy generation → performance tracking → external publishing, fully orchestrated
- **AI Content Calendar** — GPT-4 generates optimized weekly publishing schedules tailored to engagement data
- **Social API Integration** — Pulls live signals from social platforms; publishes directly through Buffer and Hootsuite APIs
- **Instant ROI** — 90% reduction in content planning time (10+ hours → ~1 hour/week) with 40% engagement uplift from data-driven recommendations
- **Production-Ready API** — Full FastAPI backend with interactive Swagger docs, auto-scaling via Railway, and a Next.js 14 frontend on Vercel

## 🎥 Demo

[![Watch Demo](https://img.shields.io/badge/YouTube-Watch%20Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=oD5264ALLCo)

## 🛠️ Tech Stack

TiDB Serverless · Python · FastAPI · OpenAI GPT-4 · Redis · TypeScript · Next.js 14 · Tailwind CSS · Docker · Railway · Vercel

## 🚀 Getting Started

```bash
# Clone and configure
git clone https://github.com/kyisaiah47/contentr.git
cd contentr
cp .env.example .env   # Add TiDB, OpenAI, and social API keys

# Start all services
docker-compose up -d

# Frontend → http://localhost:3000
# API Docs → http://localhost:8000/docs
```

**Live links**
- Frontend: https://contentr-one.vercel.app/
- API Docs: https://contentr-production.up.railway.app/docs

## 📄 License

MIT
