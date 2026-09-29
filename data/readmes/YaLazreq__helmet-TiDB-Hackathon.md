# 🚧 Helmet - Intelligent Construction Task Management

> An agentic system that transforms construction sites into self-organizing, adaptive systems using real-time worker feedback and AI orchestration.

## 🎯 Quick Start

> If you want to use our host application, please visit [Worker App](http://34.236.170.225:3000/), [Construction Site Supervisor App](http://dashboard-lb-491753214.us-east-1.elb.amazonaws.com/) for the hosted version.


### Prerequisites
- TiDB Cloud database Credentials
- LangSmith API key (optional for monitoring)
- Anthropic API key (For agent)
- OpenAI API key (For whisper-1)
- Docker

### 1. Configure Environment
Create `.env` file using `.env.EXAMPLE` as a template:


### 2. Initialize Database (One Time)
```bash
# Create database schema
python HELMET_MCP/mcp/mcp_db/schema/execute_schema.py

# Load sample dataset
cd HELMET_MCP/mcp/mcp_db/data && python dataset_001.py
```

### 3. Run with Docker
```bash
# Build and start services
docker compose up --build -d

# Monitor logs
docker compose logs -f

# Stop services
docker compose down

# Backend health check
curl http://localhost:8000/health

# MCP server check
curl http://localhost:8080

```

## 🤖 Multi-Agent Architecture

- **Supervisor**: Central orchestration and delegation
- **Planning**: Task scheduling and optimization
- **Conflict**: Resource conflict detection/resolution
- **Notifier**: Real-time alerts and notifications (on the dashboard)
- **Executor**: Action execution (Database updates)

## 🧪 Testing Crisis Scenarios

See `CRISIS_TEST_SCENARIOS.md` for testing various construction crisis situations:
- Container blockage at site entrance
- Key worker injury scenarios
- Weather emergencies
- Supplier cascade failures

## 🔧 Tech Stack

- **TiDB**: Vector database for semantic search
- **LangGraph**: Multi-agent orchestration
- **MCP**: Secure database integration
- **FastAPI**: RESTful API backend
- **LangSmith**: Agent monitoring & tracing

## 📊 API Endpoints

- **Backend**: `http://backend-helmet-lb-1240358724.us-east-1.elb.amazonaws.com`
  - `/health` - Health check

- **MCP Server**: `http://localhost:8080`

## 🏗️ Project Structure

```
├── HELMET_BACKEND/          # FastAPI backend
├── HELMET_MCP/             # MCP database server
├── src/agents/             # Multi-agent system
├── CRISIS_TEST_SCENARIOS.md # Testing scenarios
└── Dockerfile              # Container setup
```

---

**TiDB Hackathon 2025** 🚀