<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050505,50:171717,100:4F46E5&height=220&section=header&text=Supervity%20ExceptionIQ&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Understand.%20Decide.%20Resolve.&descAlignY=60&descSize=18" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&duration=2800&pause=900&color=6366F1&center=true&vCenter=true&width=850&lines=AI-Powered+Real-Time+Exception+Resolution;Human-in-the-Loop+AI+Decision+Workbench;Analyze+%E2%80%A2+Explain+%E2%80%A2+Recommend+%E2%80%A2+Resolve;AI+Advisory+%2B+Deterministic+Safety+Rules" alt="Animated project description"/>

<br/>

# Supervity ExceptionIQ

### AI-Powered Real-Time Exception Resolution Workbench

**A human-in-the-loop AI workbench for analyzing, explaining, routing, and resolving transaction exceptions.**

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vite.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3-F97316?style=for-the-badge)](https://groq.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

<br/>

**Understand. Decide. Resolve.**

<br/>

> **Disclaimer:** Supervity ExceptionIQ is an assessment implementation created for the Supervity FDE Problem 9 evaluation. It is not an official Supervity product.

</div>

---

# 🎯 Problem Statement

Organizations process large volumes of:

- Invoices
- Payments
- Purchase orders
- Expense reports
- Vendor transactions
- Financial records

These transactions can generate exceptions such as:

- Amount mismatches
- Duplicate payments
- Tax discrepancies
- Policy violations
- Suspicious transactions
- Vendor inconsistencies

Traditional manual investigation creates operational bottlenecks, increases human effort, and delays resolution.

The objective of this solution is to provide a lightweight **Exception Resolution Workbench** where a human reviewer can:

1. View flagged transactions.
2. Understand why an exception occurred.
3. Ask AI for an explanation.
4. Receive a suggested resolution.
5. Evaluate the confidence score.
6. Automatically resolve safe cases.
7. Review uncertain cases manually.
8. Escalate critical cases.
9. Track every action through an audit trail.

---

# 💡 Solution

**Supervity ExceptionIQ** combines AI advisory reasoning with deterministic backend business rules.

```text
                    FLAGGED TRANSACTION
                            │
                            ▼
                   ┌─────────────────┐
                   │   AI ANALYSIS   │
                   └────────┬────────┘
                            │
                            ▼
              Explanation + Evidence +
              Recommendation + Confidence
                            │
                            ▼
                 ┌────────────────────┐
                 │  DECISION ENGINE   │
                 └─────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          ≥ 90%         60–89%          < 60%
             │             │             │
             ▼             ▼             ▼
       AUTO-RESOLVE    HUMAN REVIEW    ESCALATE
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    UPDATE DATABASE
                           │
                           ▼
                     AUDIT TRAIL
                           │
                           ▼
                    DASHBOARD / KPIs
```

## Core Principle

> **The LLM advises. The rule engine decides. The human remains in control.**

The LLM does **not** directly modify database state or execute financial actions.

---

# 🧠 Core Architecture

```text
                         USER / REVIEWER
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    React Workbench      │
                  │ React + TypeScript      │
                  │ Tailwind + Framer       │
                  └────────────┬────────────┘
                               │
                               │ REST API
                               ▼
                  ┌─────────────────────────┐
                  │        FastAPI          │
                  │       API Layer         │
                  └────────────┬────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐   ┌────────────┐
       │  Groq AI   │   │ Decision     │   │  SQLite    │
       │  Service   │   │ Rule Engine  │   │ Database   │
       └─────┬──────┘   └──────┬───────┘   └──────┬─────┘
             │                 │                  │
             ▼                 ▼                  ▼
       AI Reasoning      Safety Rules       Source of Truth
       Evidence          Thresholds         Audit Events
       Recommendation    Overrides          State
       Confidence
```

---

# 🛡️ Human-in-the-Loop Decision Model

ExceptionIQ separates AI reasoning from business decisions.

```text
                 AI ANALYSIS
                     │
                     ▼
          Explanation + Evidence
                     │
                     ▼
             Confidence Score
                     │
                     ▼
          Deterministic Rules
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
     ≥ 90%        60–89%         < 60%
       │             │             │
       ▼             ▼             ▼
     Auto         Human         Escalate
    Resolve       Review
```

## Critical Safety Override

Critical exceptions cannot be automatically resolved merely because the AI confidence is high.

```text
Critical Exception
       │
       ▼
Safety Override
       │
       ▼
Human Review / Escalation
```

This ensures that high-risk cases remain under human control.

---

# 📊 Showcase Demo Cases

## 🟢 Case 1 — High Confidence

### TXN-1042

```text
Vendor: ABC Supplies
Exception: Amount Mismatch

PO Amount:      ₹10,000
Invoice Amount: ₹12,500

AI Confidence: 96%
Status: AUTO-RESOLVE ELIGIBLE
```

---

## 🟡 Case 2 — Medium Confidence

### TXN-1088

```text
Vendor: XYZ Services
Exception: Duplicate Payment

AI Confidence: 76%
Status: HUMAN REVIEW REQUIRED
```

---

## 🔴 Case 3 — Critical Exception

### TXN-1097

```text
Vendor: Unknown Vendor
Exception: Suspicious Wire Transfer

AI Confidence: 48%
Priority: CRITICAL
Status: ESCALATED
```

**Critical safety override prevents automatic resolution.**

---

# 🤖 ExceptionIQ AI Assistant

<div align="center">

### ✨ ExceptionIQ Assistant

**Ask. Understand. Resolve.**

</div>

ExceptionIQ includes a floating AI assistant inside the application.

The chatbot is designed as an **operational copilot**, not a generic chatbot.

### Example Questions

```text
What caused this exception?

Why is this transaction high priority?

What evidence supports the AI recommendation?

Why can't this exception be auto-resolved?

What does the confidence score mean?

What should the reviewer do next?

Explain this exception in simple terms.
```

### AI Assistant Flow

```text
Floating Chatbot
       │
       ▼
React API Service
       │
       ▼
FastAPI Backend
       │
       ▼
/api/exceptions/{id}/ask
       │
       ▼
Groq Service
       │
       ▼
Llama 3.3
       │
       ▼
Contextual AI Response
```

The Groq API key is never exposed to the frontend.

---

# 🖥️ Workbench

The application provides an operational workspace for exception management.

### Main Capabilities

- Exception queue
- Search and filtering
- Transaction details
- AI analysis
- Evidence display
- Confidence score
- Resolution recommendation
- Auto-resolution
- Human review
- Escalation
- Reopen functionality
- Audit trail
- Metrics and analytics
- Configurable business rules
- Floating AI assistant

---

# ✨ Key Features

### 📥 Exception Ingestion

- CSV import
- Demo dataset generation
- Structured transaction records
- Validation before processing

### 🔎 Exception Investigation

- Search by transaction ID
- Vendor filtering
- Category filtering
- Priority indicators
- Detailed transaction view

### 🧠 AI Analysis

- Explanation generation
- Evidence extraction
- Resolution recommendation
- Confidence scoring
- Contextual reasoning

### 🛡️ Decision Engine

- Confidence thresholds
- Critical exception override
- Human review routing
- Escalation logic
- Deterministic safety rules

### 🤖 AI Assistant

- Floating chatbot
- Contextual questions
- Natural-language explanations
- Groq-powered responses
- Backend-protected API key

### ✅ Resolution

- Auto-resolution
- Human resolution
- Escalation
- Reopen functionality

### 📜 Auditability

```text
Exception Created
       ↓
AI Analysis
       ↓
Recommendation
       ↓
Decision
       ↓
Resolution
       ↓
Audit Event
```

---

# 🔄 End-to-End Workflow

```text
                         START
                           │
                           ▼
                Upload CSV / Demo Data
                           │
                           ▼
                   Exception Queue
                           │
                           ▼
                  Select an Exception
                           │
                           ▼
                    Analyze Exception
                           │
                           ▼
             AI Explanation + Evidence
                           │
                           ▼
               Resolution Recommendation
                           │
                           ▼
                  Confidence Evaluation
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Critical?      ≥ 90%       < 90%
              │            │            │
             YES           │            │
              │            ▼            ▼
              │       Auto-Resolve   Human Review
              │                         │
              ▼                         ▼
        Escalation                 Approve / Reject
              │                         │
              └────────────┬────────────┘
                           ▼
                  Update Exception Status
                           │
                           ▼
                     Audit Event
                           │
                           ▼
                   Metrics & Dashboard
                           │
                           ▼
                          END
```

---

# 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, TypeScript, Vite |
| UI | Tailwind CSS, Framer Motion, Lucide |
| Analytics | Recharts |
| Backend | Python, FastAPI, Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite |
| AI | Groq API, Llama 3.3 70B |
| API | REST |
| Version Control | Git, GitHub |
| Deployment | Render |

---

# 🔐 Security & Grounding

### API Key Protection

The Groq API key remains exclusively on the backend.

```text
React Frontend
      │
      │ User Question
      ▼
FastAPI Backend
      │
      │ GROQ_API_KEY
      ▼
Groq API
```

The frontend never receives the secret key.

### Grounded AI

The AI receives structured exception context and is constrained to reason from the supplied information.

### Fail-Safe Operation

If the Groq API is unavailable or the API key is not configured, the backend can fall back to grounded domain intelligence.

---

# 🔌 REST API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | System health |
| GET | `/api/exceptions` | Exception queue |
| GET | `/api/exceptions/{id}` | Exception details |
| POST | `/api/exceptions/import` | CSV upload |
| POST | `/api/exceptions/{id}/analyze` | AI analysis |
| POST | `/api/exceptions/{id}/resolve` | Resolve exception |
| POST | `/api/exceptions/{id}/escalate` | Escalate exception |
| POST | `/api/exceptions/{id}/reopen` | Reopen exception |
| POST | `/api/exceptions/{id}/ask` | AI assistant |
| GET | `/api/audit` | Audit trail |
| GET | `/api/metrics` | Dashboard metrics |
| GET | `/api/rules` | Business rules |
| PUT | `/api/rules` | Update business rules |
| POST | `/api/demo/generate` | Generate demo dataset |

---

# ⚖️ Design Tradeoff

## AI Flexibility vs Deterministic Safety

A fully LLM-driven system could make decisions quickly, but it introduces the risk of unpredictable or unsafe actions.

ExceptionIQ therefore separates reasoning from execution.

```text
             LLM
              │
              ▼
      Advisory Intelligence
              │
              ▼
     Deterministic Rules
              │
              ▼
       Human Control
```

This provides:

- Better safety
- Explainability
- Predictable business decisions
- Human oversight
- Auditable actions

The tradeoff is slightly more backend complexity, but it is more appropriate for exception-resolution workflows.

---

# 🏗️ Project Structure

```text
SUPERVITY-EXCEPTIONIQ/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── groq_service.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── test_app.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FloatingChatbot.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# 🚀 Run Locally

## Prerequisites

```text
Python 3.10+
Node.js 18+
npm
Git
```

## Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Add your Groq key:

```env
GROQ_API_KEY=your_groq_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + K` | Open command palette |
| `/` | Focus search |
| `J` | Next exception |
| `K` | Previous exception |
| `R` | Resolve selected exception |
| `E` | Escalate selected exception |
| `Esc` | Close modal |

---

# 🌐 Production Deployment

```text
                       INTERNET
                          │
                          ▼
                 ┌─────────────────┐
                 │     RENDER      │
                 │   Web Service   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     FastAPI     │
                 │   Application   │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        React SPA                 REST API
                                      │
                              ┌───────┴───────┐
                              ▼               ▼
                            Groq            SQLite
```

---

# 🧪 Assessment Alignment

| Requirement | Implementation |
|---|---|
| Flagged transaction queue | ✅ |
| Key transaction details | ✅ |
| AI explanation | ✅ |
| Suggested resolution | ✅ |
| Confidence threshold | ✅ |
| Auto-resolution | ✅ |
| Human review | ✅ |
| Critical safety override | ✅ |
| Resolved state reflected in queue | ✅ |
| Audit trail | ✅ |
| Contextual chatbot | ✅ |
| Human-in-command workflow | ✅ |
| Usable workbench | ✅ |

---

# 🏆 Why ExceptionIQ?

<div align="center">

## AI should accelerate decisions — not remove accountability.

<br/>

### Analyze → Explain → Recommend → Decide → Resolve → Audit

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=17&duration=3000&pause=1000&color=8B5CF6&center=true&vCenter=true&width=750&lines=AI-assisted+exception+resolution;Human-in-the-loop+by+design;Grounded+AI.+Deterministic+Safety.+Complete+Auditability." alt="Animated tagline"/>

</div>

---

# 📌 Assessment

<div align="center">

## Supervity FDE Problem 9

### Real-Time Exception Resolution Workbench

**Built with React + FastAPI + SQLite + Groq AI**

<br/>

### Understand. Decide. Resolve.

</div>3. Ask AI for an explanation.
4. Receive a suggested resolution.
5. Evaluate confidence.
6. Automatically resolve safe cases.
7. Review uncertain cases manually.
8. Escalate critical cases.
9. Track every action through an audit trail.

---

# 💡 Solution

**Supervity ExceptionIQ** combines AI advisory reasoning with deterministic backend business rules.

```text
                    FLAGGED TRANSACTION
                            │
                            ▼
                   ┌─────────────────┐
                   │   AI ANALYSIS   │
                   └────────┬────────┘
                            │
                            ▼
              Explanation + Evidence +
              Recommendation + Confidence
                            │
                            ▼
                 ┌────────────────────┐
                 │  DECISION ENGINE   │
                 └─────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          ≥ 90%         60–89%          < 60%
             │             │             │
             ▼             ▼             ▼
       AUTO-RESOLVE    HUMAN REVIEW    ESCALATE
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    UPDATE DATABASE
                           │
                           ▼
                     AUDIT TRAIL
                           │
                           ▼
                    DASHBOARD / KPIs
Core Principle

The LLM advises. The rule engine decides. The human remains in control.

The LLM does not directly modify database state or execute financial actions.

🧠 Core Architecture
                         USER / REVIEWER
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    React Workbench      │
                  │ React + TypeScript      │
                  │ Tailwind + Framer       │
                  └────────────┬────────────┘
                               │
                               │ REST API
                               ▼
                  ┌─────────────────────────┐
                  │        FastAPI          │
                  │       API Layer         │
                  └────────────┬────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐   ┌────────────┐
       │  Groq AI   │   │ Decision     │   │  SQLite    │
       │  Service   │   │ Rule Engine  │   │ Database   │
       └─────┬──────┘   └──────┬───────┘   └──────┬─────┘
             │                 │                  │
             ▼                 ▼                  ▼
       AI Reasoning      Safety Rules       Source of Truth
       Evidence          Thresholds         Audit Events
       Recommendation    Overrides           State
       Confidence
🛡️ Human-in-the-Loop Decision Model

ExceptionIQ separates AI reasoning from business decisions.

                 AI ANALYSIS
                     │
                     ▼
          Explanation + Evidence
                     │
                     ▼
             Confidence Score
                     │
                     ▼
          Deterministic Rules
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
     ≥ 90%        60–89%         < 60%
       │             │             │
       ▼             ▼             ▼
     Auto         Human         Escalate
    Resolve       Review
Critical Safety Override

Critical exceptions cannot be automatically resolved merely because the AI confidence is high.

Critical Exception
       │
       ▼
Safety Override
       │
       ▼
Human Review / Escalation

This ensures that high-risk cases remain under human control.

📊 Showcase Demo Cases
🟢 Case 1 — High Confidence
TXN-1042
Vendor: ABC Supplies
Exception: Amount Mismatch

PO Amount:      ₹10,000
Invoice Amount: ₹12,500

AI Confidence: 96%
Status: AUTO-RESOLVE ELIGIBLE
🟡 Case 2 — Medium Confidence
TXN-1088
Vendor: XYZ Services
Exception: Duplicate Payment

AI Confidence: 76%
Status: HUMAN REVIEW REQUIRED
🔴 Case 3 — Critical Exception
TXN-1097
Vendor: Unknown Vendor
Exception: Suspicious Wire Transfer

AI Confidence: 48%
Priority: CRITICAL
Status: ESCALATED

Critical safety override prevents automatic resolution.

🤖 ExceptionIQ AI Assistant

ExceptionIQ includes a floating AI assistant inside the application.

<div align="center"> <img src="./assets/exceptioniq-bot.gif" width="180" alt="ExceptionIQ AI Assistant"/>
✨ ExceptionIQ Assistant

Ask. Understand. Resolve.

</div>

The chatbot is designed as an operational copilot, not a generic chatbot.

Example Questions
What caused this exception?

Why is this transaction high priority?

What evidence supports the AI recommendation?

Why can't this exception be auto-resolved?

What does the confidence score mean?

What should the reviewer do next?

Explain this exception in simple terms.

The chatbot communicates with the backend AI service.

Floating Chatbot
       │
       ▼
React API Service
       │
       ▼
FastAPI
       │
       ▼
/api/exceptions/{id}/ask
       │
       ▼
Groq Service
       │
       ▼
Llama 3.3
       │
       ▼
Contextual AI Response

The Groq API key is never exposed to the frontend.

🖥️ Workbench

The application provides an operational workspace for exception management.

Main capabilities
Exception queue
Search and filtering
Transaction details
AI analysis
Evidence display
Confidence score
Resolution recommendation
Auto-resolution
Human review
Escalation
Reopen functionality
Audit trail
Metrics and analytics
Configurable business rules
Floating AI assistant
✨ Key Features
📥 Exception Ingestion
CSV import
Demo dataset generation
Structured transaction records
Validation before processing
🔎 Exception Investigation
Search by transaction ID
Vendor filtering
Category filtering
Priority indicators
Detailed transaction view
🧠 AI Analysis
Explanation generation
Evidence extraction
Resolution recommendation
Confidence scoring
Contextual reasoning
🛡️ Decision Engine
Confidence thresholds
Critical exception override
Human review routing
Escalation logic
Deterministic safety rules
🤖 AI Assistant
Floating chatbot
Contextual questions
Natural-language explanations
Groq-powered responses
Backend-protected API key
✅ Resolution
Auto-resolution
Human resolution
Escalation
Reopen functionality
📜 Auditability

Important system actions are recorded through the audit trail.

Exception Created
       ↓
AI Analysis
       ↓
Recommendation
       ↓
Decision
       ↓
Resolution
       ↓
Audit Event
🔄 End-to-End Workflow
                         START
                           │
                           ▼
                Upload CSV / Demo Data
                           │
                           ▼
                   Exception Queue
                           │
                           ▼
                  Select an Exception
                           │
                           ▼
                    Analyze Exception
                           │
                           ▼
             AI Explanation + Evidence
                           │
                           ▼
               Resolution Recommendation
                           │
                           ▼
                  Confidence Evaluation
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Critical?      ≥ 90%       < 90%
              │            │            │
             YES           │            │
              │            ▼            ▼
              │       Auto-Resolve   Human Review
              │                         │
              ▼                         ▼
        Escalation                 Approve / Reject
              │                         │
              └────────────┬────────────┘
                           ▼
                  Update Exception Status
                           │
                           ▼
                     Audit Event
                           │
                           ▼
                   Metrics & Dashboard
                           │
                           ▼
                          END
🧰 Technology Stack
Frontend
Technology	Purpose
React 18	Interactive web application
TypeScript	Type-safe frontend development
Vite	Frontend development and production build
Tailwind CSS	UI styling
Framer Motion	UI animations
Recharts	Dashboard analytics
Lucide React	UI icons
Backend
Technology	Purpose
Python 3.10+	Backend language
FastAPI	REST API framework
Pydantic v2	Data validation
SQLAlchemy 2.0	Database ORM
SQLite	Persistent database
Uvicorn	ASGI server
AI
Technology	Purpose
Groq API	LLM inference
Llama 3.3 70B Versatile	AI reasoning
Structured responses	Reliable AI output
Grounded prompting	Reduce unsupported claims
Fallback intelligence	Fail-safe operation
Development / Deployment
Git
GitHub
Render
npm
REST APIs
Uvicorn
🔐 Security & Grounding
API Key Protection

The Groq API key remains exclusively on the backend.

React Frontend
      │
      │ User Question
      ▼
FastAPI Backend
      │
      │ GROQ_API_KEY
      ▼
Groq API

The frontend never receives the secret key.

Grounded AI

The AI receives structured exception context and is constrained to reason from the supplied information.

Fail-Safe Operation

If the Groq API is unavailable or the API key is not configured, the backend can fall back to grounded domain intelligence.

🔌 REST API
Method	Endpoint	Purpose
GET	/api/health	System health
GET	/api/exceptions	Exception queue
GET	/api/exceptions/{id}	Exception details
POST	/api/exceptions/import	CSV upload
POST	/api/exceptions/{id}/analyze	AI analysis
POST	/api/exceptions/{id}/resolve	Resolve exception
POST	/api/exceptions/{id}/escalate	Escalate exception
POST	/api/exceptions/{id}/reopen	Reopen exception
POST	/api/exceptions/{id}/ask	AI assistant
GET	/api/audit	Audit trail
GET	/api/metrics	Dashboard metrics
GET	/api/rules	Business rules
PUT	/api/rules	Update business rules
POST	/api/demo/generate	Generate demo dataset
⚖️ Design Tradeoff
AI Flexibility vs Deterministic Safety

A fully LLM-driven system could make decisions quickly, but it introduces the risk of unpredictable or unsafe actions.

ExceptionIQ therefore separates reasoning from execution.

             LLM
              │
              ▼
      Advisory Intelligence
              │
              ▼
     Deterministic Rules
              │
              ▼
       Human Control
Why?

This approach provides:

Better safety
Explainability
Predictable business decisions
Human oversight
Auditable actions

The tradeoff is slightly more backend complexity, but it is more appropriate for exception-resolution workflows.

🏗️ Project Structure
SUPERVITY-EXCEPTIONIQ/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── groq_service.py
│   │   │
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── database/
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── test_app.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FloatingChatbot.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── types/
│   │   │
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── assets/
│   └── exceptioniq-bot.gif
│
└── README.md
🚀 Run Locally
Prerequisites
Python 3.10+
Node.js 18+
npm
Git
Backend
cd backend

pip install -r requirements.txt

cp .env.example .env

Configure your environment:

GROQ_API_KEY=your_groq_api_key

Start the backend:

uvicorn app.main:app --reload --port 8000

Backend:

http://localhost:8000

API documentation:

http://localhost:8000/docs
Frontend
cd frontend

npm install

npm run dev

Frontend:

http://localhost:5173
⌨️ Keyboard Shortcuts
Shortcut	Action
Ctrl + K	Open command palette
/	Focus search
J	Next exception
K	Previous exception
R	Resolve selected exception
E	Escalate selected exception
Esc	Close modal
🌐 Production Deployment

The application can run as a unified production application where FastAPI serves the built React SPA alongside the API.

                       INTERNET
                          │
                          ▼
                 ┌─────────────────┐
                 │     RENDER      │
                 │   Web Service   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     FastAPI     │
                 │   Application   │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        React SPA                 REST API
              │                       │
              │                       ├── Groq
              │                       │
              │                       └── SQLite
              │
              ▼
             USER
🧪 Assessment Alignment
Requirement	Implementation
Flagged transaction queue	✅
Key transaction details	✅
AI explanation	✅
Suggested resolution	✅
Confidence threshold	✅
Auto-resolution	✅
Human review	✅
Critical safety override	✅
Resolved state reflected in queue	✅
Audit trail	✅
Contextual chatbot	✅
Human-in-command workflow	✅
Usable workbench	✅
🏆 Why ExceptionIQ?

---

# 🏆 Why ExceptionIQ?

ExceptionIQ is built around one principle:

<div align="center">

## AI should accelerate decisions — not remove accountability.

<br/>

### Analyze → Explain → Recommend → Decide → Resolve → Audit

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=17&duration=3000&pause=1000&color=8B5CF6&center=true&vCenter=true&width=750&lines=AI-assisted+exception+resolution;Human-in-the-loop+by+design;Grounded+AI.+Deterministic+Safety.+Complete+Auditability." alt="Animated tagline" />

</div>

---

# 📌 Assessment

<div align="center">

## Supervity FDE Problem 9

### Real-Time Exception Resolution Workbench

**Built with React + FastAPI + SQLite + Groq AI**

<br/>

### Understand. Decide. Resolve.

</div>
</div> ```
