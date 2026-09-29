# Ollama AI Agents with TiDB Vector Search - FastAPI Backend

A FastAPI backend for CrewAI agents with Ollama integration and TiDB Serverless Vector Search capabilities, providing a RESTful API for AI-powered research, financial analysis, and content creation workflows.

## 🚀 Features

- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **CrewAI Integration**: Multi-agent workflows for research and content creation
- **Ollama Support**: Local LLM integration with various models
- **TiDB Vector Search**: Powerful vector database for semantic search and retrieval
- **Financial Analysis**: Specialized agents for financial research and investment analysis
- **RESTful API**: Clean API endpoints for easy integration
- **Health Monitoring**: Built-in health checks and status monitoring
- **Async Support**: Non-blocking operations for better performance
- **Document Ingestion**: Tools for ingesting and processing financial documents
- **Multi-step Workflows**: Complex agent interactions for sophisticated analysis

## 📁 Project Structure

```
ollama-ai-agents/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── models.py           # Basic Pydantic models
│   │   │   └── financial_models.py # Financial API models
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health_routes.py    # Health check routes
│   │       ├── research_routes.py  # Research workflow routes
│   │       ├── models_routes.py    # Models info routes
│   │       └── financial_routes.py # Financial analysis routes
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research_agents.py      # Research agent definitions
│   │   └── financial_agents.py     # Financial agent definitions
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── research_tasks.py       # Research task definitions
│   │   └── financial_tasks.py      # Financial task definitions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crew_service.py         # Basic crew service
│   │   ├── financial_service.py    # Financial research service
│   │   ├── ingestion_service.py    # Document ingestion service
│   │   └── search_service.py       # Vector search service
│   └── models/
│       ├── __init__.py
│       ├── ollama_llm.py           # LLM configuration
│       └── tidb_vector.py          # TiDB Vector Store integration
├── run_server.py               # Server runner
├── .env.example                # Example environment variables
├── requirements.txt            # Dependencies
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites

1. **Python 3.13+** installed
2. **Ollama** installed and running locally
3. **DeepSeek model** pulled in Ollama
4. **TiDB Serverless** account and database
5. **OpenAI API key** for embeddings generation

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ollama-ai-agents
   ```

2. **Install dependencies**:
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (recommended)
   uv sync
   ```

3. **Setup Ollama**:
   ```bash
   # Install Ollama (if not already installed)
   # Visit: https://ollama.ai/
   
   # Pull the DeepSeek model
   ollama pull deepseek-r1:1.5b
   
   # Start Ollama (if not running)
   ollama serve
   ```

4. **Setup Environment Variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your TiDB and OpenAI credentials
   # TIDB_CONNECTION_STRING=mysql://username:password@gateway01.region.prod.aws.tidbcloud.com:4000/database
   # OPENAI_API_KEY=your-api-key
   ```

## 🚀 Running the Server

### Development Mode

```bash
# Run the FastAPI server
python run_server.py

# Or directly with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
# Run without reload for production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/api/v1/health

## 🔌 API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health status and Ollama availability |
| `/research` | POST | Execute research workflow |
| `/models` | GET | Available models information |
| `/financial/health` | GET | Financial service health status |
| `/financial/company` | POST | Company financial research |
| `/financial/portfolio` | POST | Portfolio analysis |
| `/financial/market-trend` | POST | Market trend analysis |
| `/financial/ingest` | POST | Ingest financial document |
| `/financial/search` | POST | Search financial data |

### Example Usage

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

#### Research Workflow
```bash
curl -X POST "http://localhost:8000/api/v1/research" \
     -H "Content-Type: application/json" \
     -d '{"topic": "artificial intelligence trends 2024"}'
```

#### Financial Research
```bash
curl -X POST "http://localhost:8000/api/v1/financial/company" \
     -H "Content-Type: application/json" \
     -d '{"ticker": "AAPL"}'
```

#### Financial Data Search
```bash
curl -X POST "http://localhost:8000/api/v1/financial/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "recent earnings report", "ticker": "AAPL"}'
```

#### Python Example
```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Research workflow
data = {"topic": "artificial intelligence trends 2024"}
response = requests.post("http://localhost:8000/api/v1/research", json=data)
result = response.json()
print(result["result"])

# Financial company research
data = {"ticker": "AAPL"}
response = requests.post("http://localhost:8000/api/v1/financial/company", json=data)
result = response.json()
print(result["result"])

# Ingest financial document
data = {
    "ticker": "AAPL",
    "document_type": "earnings_report",
    "content": "Apple Inc. reported record revenue of $123.9 billion...",
    "source": "Q1 2024 Earnings Call"
}
response = requests.post("http://localhost:8000/api/v1/financial/ingest", json=data)
print(response.json())
```

## 🤖 Agents and Workflows

### Research Workflow Agents

The research system uses three specialized agents:

1. **Research Analyst**: Conducts thorough research on topics
2. **Content Writer**: Creates engaging content from research
3. **Content Editor**: Reviews and improves content quality

### Financial Workflow Agents

The financial system uses five specialized agents:

1. **Financial Analyst**: Analyzes financial data and company performance
2. **Investment Advisor**: Provides investment recommendations
3. **Data Researcher**: Gathers and organizes financial information
4. **Market Analyst**: Analyzes market trends and sector performance
5. **Risk Assessor**: Evaluates investment risks and mitigation strategies

### Research Workflow Process

1. **Research Phase**: Agent analyzes the topic and gathers information
2. **Writing Phase**: Agent creates structured content based on research
3. **Editing Phase**: Agent polishes and improves the final content

### Financial Workflow Process

1. **Data Gathering**: Agent collects financial data from various sources
2. **Financial Analysis**: Agent analyzes company financial performance
3. **Market Analysis**: Agent evaluates market position and trends
4. **Risk Assessment**: Agent identifies and evaluates investment risks
5. **Investment Recommendation**: Agent provides investment advice based on analysis

## ⚙️ Configuration

### Ollama Model Configuration

Edit `app/models/ollama_llm.py` to change the default model:

```python
# Change the default model
ollama_llm = OllamaLLM(model_name="llama3.2:7b")
```

### TiDB Vector Store Configuration

Edit `.env` file to configure TiDB connection:

```
# TiDB Serverless Configuration
TIDB_CONNECTION_STRING=mysql://username:password@gateway01.region.prod.aws.tidbcloud.com:4000/database

# OpenAI API Key (for embeddings)
OPENAI_API_KEY=your-api-key
```

### Supported Models

- `deepseek-r1:1.5b` (default)
- `qwen3:0.6b`
- `llama3.2:1b`
- `llama3.2:3b`
- `llama3.2:7b`
- `llama3.2:70b`

## 🔧 Development

### Adding New Agents

1. Create agent functions in `app/agents/`
2. Add corresponding tasks in `app/tasks/`
3. Update the service in `app/services/`
4. Add API endpoints in `app/api/routes.py`

### Adding New Workflows

1. Define workflow tasks in `app/tasks/`
2. Create workflow service methods in `app/services/crew_service.py`
3. Add API endpoints for the new workflow

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Error**:
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is pulled: `ollama list`
   - Verify the model name in configuration

2. **TiDB Connection Error**:
   - Verify your TiDB connection string in `.env`
   - Ensure your TiDB Serverless cluster is running
   - Check network connectivity to TiDB Serverless

3. **OpenAI API Key Error**:
   - Verify your OpenAI API key in `.env`
   - Check if your OpenAI account has sufficient credits

4. **Port Already in Use**:
   - Change the port in `run_server.py` or use a different port
   - Kill existing processes using the port

5. **Dependency Issues**:
   - Update dependencies: `pip install -r requirements.txt --upgrade`
   - Check Python version compatibility

### Debug Mode

Run with debug logging:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Open an issue on GitHub
