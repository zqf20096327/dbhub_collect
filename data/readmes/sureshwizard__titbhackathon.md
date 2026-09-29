# TiDB SmartLedger

SmartLedger is a hackathon project that demonstrates a **chat-driven financial assistant** built on top of **TiDB** (HTAP database), with real-time metrics, invoice tracking, and a conversational UI.

The system combines:
- **Frontend (React + Vite)** → Modern, responsive dashboard & chat interface  
- **Backend (FastAPI)** → Business logic, chat orchestration, database queries  
- **TiDB Cloud** → Distributed transactional + analytical database  
- **Nginx reverse proxy** → TLS termination, multi-service routing, and CSP headers  
- **Optional microservices** on ports 4057–4061 for specialized tasks (chat API, uploader, reports, analytics, graphs)


## 🚀 Features

- 📊 **Invoice & Overdue Tracking** — Query overdue invoices, trends, and summaries  
- 💬 **AI Chatbot** — Natural language queries to fetch accounting insights  
- 🔊 **Voice Integration** — Automatic speech synthesis for assistant replies  
- 📈 **Dashboards** — Visualize invoices/overdues with charts  
- 🛡️ **Secure Deployment** — TLS via Let's Encrypt, Nginx CSP headers  
- ⚡ **TiDB Context Toggle** — Switch between mock/stub data and live TiDB queries  


## 🗂️ Project Structure

tidbsmartledger/
├── services/
│ ├── smartledger4056/frontend # React + Vite (port 4056, proxied at /)
│ ├── smartledger4062/backend # FastAPI backend (port 4062, proxied at /api/)
│ ├── smartledger4057/ # Chat API service
│ ├── smartledger4058/ # File uploader
│ ├── smartledger4059/ # Reports service
│ ├── smartledger4060/ # Analytics service
│ └── smartledger4061/ # Graphs service
├── nginx/
│ └── tidb-ledger.admnwizard.com.conf # Reverse proxy config
├── docs/
│ └── SDD.pdf # System Design Document
└── README.md

## ⚙️ Tech Stack

- **Frontend**: React 18, Vite, TailwindCSS, Recharts, Web Speech API  
- **Backend**: Python 3.11+, FastAPI, Uvicorn  
- **Database**: TiDB Cloud (MySQL protocol)  
- **Proxy**: Nginx with TLS (Let’s Encrypt)  
- **AI Model**: GPT (via Together.ai API)  
- **Voice**: Browser SpeechSynthesis + pyttsx3 (backend fallback)

## 🔧 Setup Instructions

### 1. Clone & Install
git clone https://github.com/<your-org>/tidbsmartledger.git
cd tidbsmartledger
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Configure Environment
Create .env or /etc/tidbsmartledger.env:


OPENAI_API_KEY=sk-xxx
TOGETHER_API_KEY=xxx
TOGETHER_API_URL=https://api.together.xyz/v1
USE_GPT_STUB=false
TIDB_HOST=gateway01.ap-northeast-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=xxx
TIDB_DATABASE=smartledger

3. Run Backend

cd services/smartledger4062/backend
uvicorn backend:app --host 0.0.0.0 --port 4062 --reload

4. Run Frontend
cd services/smartledger4056/frontend
npm install
npm run dev -- --host --port 4056

5. Configure Nginx
Deploy TLS reverse proxy:
/ → frontend (4056)
/api/ → backend (4062)
/svc4057/..svc4061/ → other services
/chat → backend chat API

Check config:
sudo nginx -t
sudo systemctl reload nginx

🌐 Access
Frontend (UI): https://tidb-ledger.admnwizard.com/
API health: https://tidb-ledger.admnwizard.com/api/health
Chat endpoint: POST https://tidb-ledger.admnwizard.com/chat

📊 Demo Flow
Open the dashboard

Type:
show me overdue invoices this month
Backend queries TiDB (if context enabled) or stub data
Assistant replies in chat + speaks reply aloud
Dashboard refreshes charts with new data

🛠️ Development Notes
During development, Vite serves on port 4056. Always use relative URLs (/chat, /metrics, /api/...) in frontend to avoid CSP errors.
If you see Error: 404 in chat → confirm backend implements /chat or /api/chat. Adjust nginx accordingly.
Nginx regex for /proxy/<port>/<rest> must be ([0-9]+) (not {4}) due to PCRE2 quirks.

📌 To Do
 Finalize TiDB schema migration scripts
 Add proper auth (JWT / OAuth2)
 Expand dashboard with revenue/expense views
 Dockerize backend + frontend for easier deploy

📄 License
MIT — free to use, modify, and distribute.
Would you like me to also include **systemd service files** (one for frontend, one for backend) in the README so you can run SmartLedger automatically on reboot?
