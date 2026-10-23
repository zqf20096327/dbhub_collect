# MySQL Analyst AI Agent - E-commerce Database Assistant

A full-stack, production-grade AI-powered MySQL analyst agent for e-commerce data analysis. Ask natural language questions about your database, and get intelligent, data-driven answers with real-time streaming responses.

## 🎯 Project Overview

This project implements an intelligent database assistant that uses:
- **Google Generative AI (Gemini)** for natural language understanding and response generation
- **LangChain + LanGraph** for agent orchestration and conversation memory management
- **Model Context Protocol (MCP)** for secure database tool integration
- **FastAPI** for high-performance async streaming API
- **Streamlit** for an intuitive web-based user interface
- **TiDB (MySQL-compatible)** for distributed database storage

Users can ask complex questions about e-commerce data (orders, customers, products, etc.) in natural language, and the AI agent automatically formulates and executes appropriate SQL queries, returning formatted responses.

### Key Features

✅ **Natural Language to SQL**: Ask questions in English, get data-driven answers  
✅ **Real-time Streaming**: See AI responses appear in real-time with tool execution visibility  
✅ **Conversation Memory**: Thread-based session management for maintaining context  
✅ **Safe Database Access**: Read-only MCP tools prevent accidental data modification  
✅ **PDF Export**: Download AI responses as formatted PDFs  
✅ **Production-Ready**: Async/await architecture, CORS enabled, error handling  
✅ **MCP Tool Integration**: Easily extend with additional data sources via MCP  

---

## 🏗️ Architecture Overview

The system follows a **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Streamlit)                   │
│                     streamlit_client.py                         │
│  - Interactive chat interface                                   │
│  - Session state & message history                              │
│  - PDF export functionality                                     │
│  - Thread ID management for memory                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/WebSocket
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    Backend Layer (FastAPI)                      │
│                      stream_server.py                           │
│  - RESTful API endpoints                                        │
│  - Streaming response support                                   │
│  - LangChain Agent orchestration                                │
│  - CORS & async request handling                                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │                     │
            ┌───────▼─────┐      ┌───────▼─────┐
            │   LangChain │      │  MCP Client │
            │    Agent    │      │             │
            └──────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────────┐
│              Data & Tool Integration Layer                      │
│  - utils.py: MCP configuration loader                           │
│  - MCP MySQL Tool: SQL execution against TiDB                   │
│  - Database: E-commerce dataset (orders, customers, products)   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Details

| Component | File | Purpose |
|-----------|------|---------|
| **Streamlit Client** | `streamlit_client.py` | Web UI for user interaction |
| **FastAPI Server** | `stream_server.py` | REST API with streaming support |
| **Utilities** | `utils.py` | MCP config loading |
| **Database Migration** | `app.py` | SQLite → MySQL migration script |

See [Architecture.png](Architecture.png) for a detailed architecture diagram.

---

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Node.js & npm**: Required for MCP MySQL server
- **Database**: TiDB (MySQL-compatible) account or local MySQL server
- **API Keys** (see Configuration section):
  - Google Generative AI API key
  - Database credentials (host, user, password)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mysql-analyst-agent.git
cd mysql-analyst-agent
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **langchain**: Agent and chain orchestration
- **langchain-google-genai**: Google Generative AI integration
- **langchain-mcp-adapters**: MCP client for database tools
- **fastapi**: Web framework
- **streamlit**: Frontend framework
- **httpx**: Async HTTP client
- **pymysql**: MySQL database driver
- **markdown2** & **xhtml2pdf**: PDF export
- **ollama**: Local LLM support (optional)

### 4. Install MCP MySQL Server (Node.js)

The MCP MySQL tool requires Node.js:

```bash
npm install -g @benborla29/mcp-server-mysql
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Google Generative AI
API_KEY=your-google-api-key-here
LLM_MODEL=gemini-pro

# TiDB / MySQL Database
MYSQL_HOST=gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com
MYSQL_PORT=4000
MYSQL_USER=your-tidb-username
MYSQL_PASSWORD=your-tidb-password
MYSQL_DB=ecommerce

# Optional
DEBUG=false
```

### MCP Configuration

The MCP configuration is stored in `mcp_config.json`. The default config connects to a TiDB instance with read-only permissions:

```json
{
    "tidb_ecommerce": {
      "command": "npx",
      "args": ["-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "...",
        "MYSQL_PORT": "4000",
        "MYSQL_USER": "...",
        "MYSQL_PASS": "...",
        "MYSQL_DB": "ecommerce",
        "ALLOW_INSERT_OPERATION": "false",
        "ALLOW_UPDATE_OPERATION": "false",
        "ALLOW_DELETE_OPERATION": "false",
        "MYSQL_SSL": "true"
      },
      "transport": "stdio"
    }
}
```

**Security Note**: Read/Write operations are disabled by default. Modify only if needed.

---

## 📂 Project Structure

```
.
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
│
├── app.py                       # SQLite → MySQL migration script
├── stream_server.py             # FastAPI streaming server (main backend)
├── streamlit_client.py          # Streamlit web UI (main frontend)
├── utils.py                     # Utility functions (MCP config loader)
│
├── mcp_config.json              # MCP server configuration
├── mcp_configuration.json       # Alternative MCP config format
├── interview.md                 # Q&A documentation
├── Architecture.png             # Architecture diagram
│
├── db/                          # Database files
│   └── olist.sqlite             # Local SQLite database (for migration)
│
└── venv/                        # Virtual environment (created after setup)
```

---

## 🏃 How to Run

### Option 1: Run Everything Locally

#### Terminal 1 - Start FastAPI Server

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the server on port 8002
python stream_server.py

# Or with auto-reload (development):
fastapi dev stream_server.py
```

Expected output:
```
Tools are loaded. ready to create agent!
INFO:     Application startup complete
```

#### Terminal 2 - Start Streamlit Client

```bash
# In a new terminal (with venv activated)
streamlit run streamlit_client.py
```

The Streamlit app will automatically open in your browser at `http://localhost:8501`

#### Use the Application

1. Enter a **Thread ID** in the sidebar (for conversation memory)
2. Type your database query in natural language
3. Watch the AI agent execute the query and stream results
4. View tool execution details in real-time
5. Export responses as PDF using the "Download PDF" button
6. Click "Clear Messages" to reset conversation

### Option 2: Using UV Package Manager

If you prefer using `uv` (faster Python package installer):

```bash
# Terminal 1 - Start server
uv run stream_server.py

# Terminal 2 - Start Streamlit
uv run streamlit run streamlit_client.py
```

### Option 3: Database Migration (If Using SQLite → MySQL)

If you need to migrate data from SQLite to MySQL:

```bash
python app.py
```

This script:
1. Reads all tables from `db/olist.sqlite`
2. Creates matching schema in MySQL
3. Copies all data to remote database

---

## 📡 API Endpoints

### FastAPI Server: `http://localhost:8002`

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "Hello": "Dheeraj. Your FastAPI Server is up!"
}
```

#### 2. Streaming Chat
```http
POST /chat_stream
Content-Type: application/json

{
  "query": "What are the top 5 most ordered products?",
  "model": "gemini-pro",
  "thread_id": "default"
}
```

**Response Format** (Newline-Delimited JSON):
```json
{"type": "AIMessageChunk", "content": "The top 5 most ordered products are:\n\n1. ..."}
{"type": "AIMessageChunk", "content": " Product Beta with 450 orders\n2. ..."}
{"type": "AIMessageChunk", "tool_calls": [{"name": "query_database", "args": {...}}]}
```

---

## 💡 Usage Examples

### Example 1: Simple Query
```
User: "How many customers do we have?"

Agent Response: "There are 999 registered customers in the database."
Tool Used: query_database (executing SQL SELECT COUNT(*) FROM customers)
```

### Example 2: Complex Analysis
```
User: "Show me revenue by month for the last year"

Agent Response: "Monthly Revenue Report:
- January: $45,230
- February: $52,100
- March: $48,900
..."
Tool Used: query_database (complex JOIN queries on orders and products)
```

### Example 3: Multi-turn Conversation
```
User: "What's our average order value?"
Agent: "The average order value is $156.42"

User: "Which product category has the highest average order value?"
Agent: "Electronics category with $312.88 average order value"
(Thread ID maintains context between messages)
```

---

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload for code changes
fastapi dev stream_server.py

# And in another terminal:
streamlit run streamlit_client.py --logger.level=debug
```

### Adding New Database Tools

1. Update `mcp_config.json` with new MCP server config
2. Restart `stream_server.py` to reload tools
3. Tools are automatically available to the agent

### Testing the API

```bash
# Using curl
curl -X POST http://localhost:8002/chat_stream \
  -H "Content-Type: application/json" \
  -d '{"query":"How many orders exist?","thread_id":"test"}'

# Using Python
import httpx
with httpx.Client() as client:
    response = client.get("http://localhost:8002/")
    print(response.json())
```

---

## 🐛 Troubleshooting

### 1. **Connection Error to Database**
```
Error: Unable to connect to MySQL server
```
**Solution**:
- Verify `MYSQL_HOST`, `MYSQL_PORT`, and credentials in `.env`
- Check network connectivity to TiDB/MySQL server
- Ensure `MYSQL_SSL` is set correctly

### 2. **MCP Tools Not Loading**
```
Error: Loaded 0 Tools
```
**Solution**:
- Verify Node.js is installed: `node --version`
- Install MCP MySQL server: `npm install -g @benborla29/mcp-server-mysql`
- Check `mcp_config.json` for valid configuration
- Restart server and check logs

### 3. **Streamlit Connection Refused**
```
Error: Failed to connect to http://localhost:8002/chat_stream
```
**Solution**:
- Ensure FastAPI server is running
- Check server is listening on `http://localhost:8002`
- Verify firewall allows local connections
- No CORS issue since it's localhost

### 4. **PDF Export Not Working**
```
Error: xhtml2pdf error
```
**Solution**:
- Verify `xhtml2pdf` is installed: `pip install xhtml2pdf`
- Check Downloads directory exists
- Ensure assistant has generated a response

### 5. **API Key Error**
```
Error: Google API key not found or invalid
```
**Solution**:
- Create `.env` file with valid `API_KEY`
- Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Restart server after updating `.env`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | Latest | Agent orchestration and chains |
| langchain-google-genai | Latest | Google Generative AI integration |
| langchain-mcp-adapters | Latest | MCP client for database tools |
| fastapi | Latest | REST API framework |
| streamlit | Latest | Frontend web framework |
| pymysql | Latest | MySQL database connector |
| httpx | Latest | Async HTTP client |
| markdown2 | Latest | Markdown to HTML conversion |
| xhtml2pdf | Latest | HTML to PDF conversion |
| python-dotenv | Implicit | Environment variable loading |

---

## 🔐 Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **MCP Read-Only Permissions** - INSERT/UPDATE/DELETE are disabled by default
3. **API Key Protection** - Keep Google API keys confidential
4. **CORS Configuration** - Currently allows all origins; restrict in production to specific domains
5. **Streamlit Authentication** - Add password protection for production deployment

---

## 🚀 Deployment

### Deploying to Production

#### Option 1: Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN npm install -g @benborla29/mcp-server-mysql

COPY . .

# Expose ports
EXPOSE 8002 8501

# Run both services
CMD ["sh", "-c", "python stream_server.py & streamlit run streamlit_client.py"]
```

#### Option 2: Using Systemd (Linux)

Create `/etc/systemd/system/mysql-agent.service`:
```ini
[Unit]
Description=MySQL Analyst AI Agent
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/mysql-agent
Environment="PATH=/opt/mysql-agent/venv/bin"
ExecStart=/opt/mysql-agent/venv/bin/python stream_server.py

[Install]
WantedBy=multi-user.target
```

#### Option 3: Cloud Platforms

- **Heroku**: `git push heroku main` (with Procfile)
- **AWS EC2**: Launch instance, install dependencies, run with systemd
- **Google Cloud Run**: Container-based deployment with serverless scaling
- **Render**: Direct GitHub integration with auto-deploy

---

## 📚 Documentation

- [LangChain Docs](https://python.langchain.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [TiDB Docs](https://docs.pingcap.com/tidb/stable)

---

## 📝 File Descriptions

### `stream_server.py`
FastAPI-based backend server that orchestrates LangChain agents with database tool integration via MCP. Handles streaming responses to user queries and maintains conversation memory using thread IDs.

### `streamlit_client.py`
Interactive web UI built with Streamlit for user interaction. Manages chat sessions, displays AI responses in real-time, visualizes tool execution, and exports conversations as formatted PDFs.

### `utils.py`
Utility module providing MCP configuration loading and helper functions for tool initialization.

### `app.py`
Database migration script that moves data from local SQLite to remote MySQL/TiDB servers.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Dheeraj**  
Building AI-powered database analysis tools

---

## 🙋 Support

For issues, questions, or suggestions:
- Open a GitHub Issue
- Check existing documentation in `interview.md`
- Review the troubleshooting section above

---

## 🎉 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Google Generative AI](https://deepmind.google/technologies/gemini/)
- UI by [Streamlit](https://streamlit.io/)
- Database via [TiDB](https://www.pingcap.com/)
- Tool integration via [MCP](https://modelcontextprotocol.io/)

---

**Last Updated**: September 2026  
**Status**: Production Ready ✅
