# Docvoice - AI Voice Agent

A Python-based AI voice agent with TiDB vector search integration for intelligent documentation assistance.

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Environment Setup

Copy the environment file and configure your credentials:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your required values:

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-instance.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Deepgram Configuration
DEEPGRAM_API_KEY=your_deepgram_api_key

# TiDB Vector Search Configuration
TIDB_HOST=gateway01.region.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=your_tidb_username
TIDB_PASSWORD=your_tidb_password
TIDB_DATABASE=test
```
 

### 3. Run the Agent

#### Development Mode
```bash
uv run python run_agent.py dev
```

#### Production Mode
```bash
uv run python run_agent.py start
```

#### Console Mode (for testing)
```bash
uv run python run_agent.py console
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LIVEKIT_URL` | LiveKit server WebSocket URL | Yes |
| `LIVEKIT_API_KEY` | LiveKit API key | Yes |
| `LIVEKIT_API_SECRET` | LiveKit API secret | Yes |
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes |
| `DEEPGRAM_API_KEY` | Deepgram API key for speech-to-text | Yes |
| `TIDB_HOST` | TiDB Cloud hostname | Yes |
| `TIDB_USER` | TiDB username | Yes |
| `TIDB_PASSWORD` | TiDB password | Yes |
| `TIDB_DATABASE` | TiDB database name | Yes |

 