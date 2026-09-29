# Intelligent Industrial Equipment Management System

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Industrial equipment management platform connecting monitoring, openGauss, knowledge graphs, and AI maintenance assistance">
</p>
An openGauss-based web platform for industrial equipment lifecycle management, real-time condition monitoring, threshold-based alerts, maintenance tracking, knowledge-graph exploration, and LLM-assisted maintenance support.

This repository is the implementation accompanying the research project **Intelligent Industrial Equipment Management System Based on openGauss**. It explores how openGauss, graph data, retrieval, and large language models can support more efficient industrial operations and maintenance.
## Built for the maintenance loop

From the first equipment record to an operator's question, the platform keeps operational context connected: assets and status history are managed in openGauss; alert rules turn metrics into actionable events; Neo4j and FAISS connect faults, documents, and solutions; the Flask service presents that context to an LLM-powered maintenance assistant.

**Start here:** follow the [Quick Start](#quick-start) guide, then initialize the demonstration graph with `POST /graph/init`.

## Highlights

- **Equipment lifecycle management** — maintain equipment records, status history, categories, and operational metadata.
- **Condition monitoring and alerts** — collect metrics, configure threshold rules, and manage alert events.
- **Maintenance management** — record maintenance activities and connect them with equipment and alerts.
- **Role-based access control** — JWT authentication with users, roles, and permissions.
- **Knowledge graph** — model equipment, faults, parts, parameters, and solutions in Neo4j.
- **AI maintenance assistant** — use document retrieval, graph knowledge, and an LLM to answer maintenance questions in natural language.
- **Data visualization** — Vue and ECharts dashboards for equipment and monitoring data.

## Architecture

<p align="center">
  <img src="./assets/readme/workflow.svg" width="100%" alt="Four-step flow from equipment signals to openGauss records, Neo4j and FAISS retrieval, and AI maintenance answers">
</p>
```text
Vue 3 + Element Plus + ECharts
             |
             | REST API / JWT
             v
Spring Boot application  <---->  openGauss
             |
             | AI service API
             v
Flask AI service  <----------->  Neo4j + FAISS + LLM API
```

## Technology Stack

| Layer | Technologies |
| --- | --- |
| Frontend | Vue 3, Vite, Element Plus, Axios, ECharts |
| Backend | Java 17+, Spring Boot, Spring Security, Spring Data JPA, JWT |
| AI Service | Python 3.10+, Flask, FAISS, Sentence-Transformers, jieba |
| Data | openGauss, Neo4j |
| AI | Retrieval-augmented generation (RAG) and an OpenAI-compatible LLM API |

## Project Structure

```text
.
├── src/                         # Spring Boot backend
├── frontend/                    # Vue 3 frontend
├── ai_service/                  # Flask AI service
│   ├── app.py                   # Service entry point
│   ├── knowledge_graph.py       # Neo4j integration
│   ├── retriever.py             # Hybrid retrieval
│   ├── llm_chain.py             # LLM integration
│   ├── pdf_processor.py         # PDF knowledge ingestion
│   └── .env.example             # Safe AI configuration template
├── backend.env.example          # Safe backend configuration template
├── database.sql                 # openGauss schema and seed data
└── pom.xml                      # Maven configuration
```

## Prerequisites

- JDK 17 or later
- Maven 3.8 or later
- Node.js 18 or later
- Python 3.10 or later
- openGauss
- Neo4j 5.x for the knowledge graph

## Quick Start

### 1. Initialize openGauss

Create a database and run the initialization script with your own database account:

```bash
gsql -h <host> -p <port> -U <username> -d <database> -f database.sql
```

Configure the backend with environment variables. `backend.env.example` lists the required values:

```text
DB_URL=jdbc:postgresql://localhost:5432/equipment_management
DB_USERNAME=your-database-username
DB_PASSWORD=your-database-password
```

For PowerShell:

```powershell
$env:DB_URL = "jdbc:postgresql://localhost:5432/equipment_management"
$env:DB_USERNAME = "your-database-username"
$env:DB_PASSWORD = "your-database-password"
```

> Never commit real database credentials, API keys, or local `.env` files.

### 2. Start the backend

```bash
mvn spring-boot:run
```

The backend starts at `http://localhost:8081/api`. Swagger UI is available at `http://localhost:8081/api/swagger-ui/index.html`.

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The Vite development server proxies `/api` requests to the Spring Boot backend.

### 4. Start the AI service

```bash
cd ai_service
cp .env.example .env
pip install -r requirements.txt
python app.py
```

Edit only the local `ai_service/.env` file:

```text
DEEPSEEK_API_KEY=your-api-key
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password
```

The AI service starts at `http://localhost:5000`.

To create demonstration knowledge-graph data:

```bash
curl -X POST http://localhost:5000/graph/init
```

## Core APIs

### Backend API

Base URL: `http://localhost:8081/api`

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/login` | Sign in and receive a JWT |
| POST | `/auth/register` | Register an account |
| GET | `/dashboard/stats` | Read dashboard statistics |
| GET / POST | `/equipments` | List or create equipment |
| PUT / DELETE | `/equipments/{id}` | Update or delete equipment |
| GET | `/monitoring-data/latest/{id}` | Get the latest monitoring data |
| GET | `/alarm-rules` | List alert rules |
