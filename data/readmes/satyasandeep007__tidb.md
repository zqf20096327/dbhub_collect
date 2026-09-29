# ![Logo](./public/submission/logo.svg) 

**docvoice** is a revolutionary platform that transforms website content into intelligent voice agents. It leverages TiDB Cloud's powerful vector search capabilities to create AI-powered knowledge bases that users can interact with through natural voice conversations.

**Tagline**: "Transform Documentation into Intelligent Voice Conversations"

![AI Knowledge Base Demo](./public/submission/demo.gif)

## 🚀 Quick Start

- **GitHub Repo**: [Frontend](https://github.com/satyasandeep007/tidb)
- **GitHub Repo**: [Backend](https://github.com/shivamangina/tidb-backend)
- **Demo Video**: [Watch on YouTube](https://www.youtube.com/watch?v=Vd_kwPGeKmw)

**Note**: This project consists of two repositories - Frontend (Next.js) and Backend (Python). You need to run both for the complete functionality.

## 🌟 Problem

Traditional knowledge management systems suffer from several critical limitations:
- **Static Content**: Information becomes outdated quickly and requires manual updates 📚
- **Poor Search**: Keyword-based search fails to understand user intent and context 🔍
- **No Voice Interface**: Users can't interact naturally through voice conversations 🗣️
- **Limited Scalability**: Traditional databases struggle with large-scale content indexing 📊
- **Complex Integration**: Difficult to embed AI capabilities into existing websites 🔧

## 💡 Solution

**docvoice** provides a comprehensive solution that transforms static websites into intelligent, voice-enabled knowledge bases:

- **Vector Search**: Leverages TiDB Cloud's vector search for semantic understanding 🌐
- **Voice AI Agents**: Natural voice conversations with AI-powered responses 🎤
- **Real-time Indexing**: Automatically crawls and indexes website content ⚡
- **Easy Integration**: Simple widget that can be embedded on any website 🚀
- **Scalable Architecture**: Built on TiDB Cloud for enterprise-grade performance 📈

### 🚀 Features

**Docvoice** enables users to:

- 🕷️ **Web Crawling**: Automatically crawl websites and extract clean text content
- 🔍 **Vector Search**: Use TiDB Cloud's vector search with OpenAI embeddings
- 🤖 **AI-Powered Q&A**: Get intelligent answers to questions about indexed content
- 🎤 **Voice Interface**: Natural voice conversations with AI agents
- 📱 **Widget Integration**: Embed voice agents on any website
- 📊 **Real-time Processing**: Live feedback on indexing and query operations
- 🔗 **Source Attribution**: See exactly where answers come from with clickable links

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **Voice**: LiveKit for real-time voice communication
- **Crawling**: Cheerio for HTML parsing
- **Vector Processing**: OpenAI embeddings with semantic chunking

### Backend
- **Language**: Python 3.8+
- **Package Manager**: uv
- **Voice Processing**: Deepgram for speech-to-text
- **AI**: OpenAI GPT-4 for language processing
- **Real-time Communication**: LiveKit server integration

### Infrastructure
- **Database**: TiDB Cloud with Vector Search
- **AI Models**: OpenAI GPT-4 and text-embedding-3-large
- **Voice Services**: LiveKit + Deepgram

## 📚 Installation & Setup

### Prerequisites

Before you begin, ensure you have:

1. **Node.js 18+** and **pnpm** installed
2. **Python 3.8+** and **uv** package manager installed
3. **TiDB Cloud account** with a cluster set up and Vector Search enabled
4. **OpenAI API key** with access to embeddings and chat models
5. **LiveKit account** with API credentials (for voice functionality)
6. **Deepgram API key** for speech-to-text functionality

### 1. Clone Both Repositories

```bash
# Clone Frontend Repository
git clone https://github.com/satyasandeep007/tidb
cd tidb

# Clone Backend Repository (in a separate directory)
cd ..
git clone https://github.com/shivamangina/tidb-backend
cd tidb-backend
```

### 2. Install Frontend Dependencies

```bash
cd ../tidb
pnpm install
```

### 3. Install Backend Dependencies

```bash
cd ../tidb-backend
uv sync
```

### 4. Configure Frontend Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-openai-project-api-key

# TiDB Cloud Configuration
TIDB_HOST=your-cluster.tidbcloud.com
TIDB_USER=your-username.root
TIDB_PASSWORD=your-password
TIDB_DATABASE=your-database-name
TIDB_PORT=4000

# LiveKit Configuration (required for voice functionality)
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
```

### 5. Configure Backend Environment Variables

Create a `.env.local` file in the backend directory:

```env
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

### 6. Set Up TiDB Cloud

1. **Create a TiDB Cloud cluster** if you haven't already
2. **Enable Vector Search** in your cluster settings
3. **Get connection details** from your TiDB Cloud dashboard
4. **Create a database** for the application (or use the default)

### 7. Set Up LiveKit

1. **Create a LiveKit account** at [livekit.io](https://livekit.io)
2. **Get your API credentials** from the LiveKit dashboard
3. **Configure the environment variables** in both frontend and backend `.env.local` files

### 8. Set Up Deepgram

1. **Create a Deepgram account** at [deepgram.com](https://deepgram.com)
2. **Get your API key** from the Deepgram dashboard
3. **Add the API key** to your backend `.env.local` file

### 9. Start Both Services

**Terminal 1 - Start Frontend:**
```bash
cd tidb
pnpm dev
```

**Terminal 2 - Start Backend:**
```bash
cd tidb-backend

# Development Mode
uv run python run_agent.py dev

# OR Production Mode
uv run python run_agent.py start

# OR Console Mode (for testing)
uv run python run_agent.py console
```

The frontend will be available at `http://localhost:3000` and the backend will run on the specified port.

## 🚀 Running the App

### Quick Demo Flow

1. **Index Content**: Go to URLs page → Add URL → Start Indexing
2. **Create Agent**: Go to Agents page → Create Agent → Assign indexed URLs
3. **Test Voice**: In Agents table → ⋮ menu → Test Voice
4. **Integration**: In Agents table → ⋮ menu → Integrate → Copy HTML code

### Testing Voice Functionality

- **Main Voice Page**: `/voice` - Full voice interface
- **Agent Testing**: Through Agents page modal (recommended)
- **Widget Testing**: Use `test-widget.html` for iframe testing

 
## 🏆 Technical Highlights

- **TiDB Cloud Vector Search**: Scalable vector database with enterprise-grade performance
- **OpenAI Integration**: Latest GPT-4 and embedding models for superior AI responses
- **LiveKit**: Real-time voice communication with low latency
- **Next.js 14**: Modern React framework with App Router
- **TypeScript**: Type-safe development for better code quality
- **Python Backend**: High-performance voice processing with Deepgram integration
- **Semantic Chunking**: Intelligent content splitting for optimal vector search
- **Dual Architecture**: Frontend-Backend separation for scalability and maintainability

## 📊 How docvoice Uses TiDB Cloud

**docvoice** leverages TiDB Cloud's vector search as its core AI knowledge system:

### **Database Schema & Storage:**
- **`enhanced_chunks`**: Stores website content chunks with 1536-dimensional vector embeddings
  - `content`: Raw text chunks from web pages
  - `embedding VECTOR(1536)`: OpenAI text-embedding-3-large vectors for semantic search
  - `metadata JSON`: Page titles, URLs, and indexing information
  - `url` & `page_title`: Source attribution for answers

- **`url_sources`**: Manages websites to be indexed
  - `indexing_mode`: Simple vs enhanced crawling options
  - `max_pages` & `max_depth`: Crawling limits and depth control
  - `chunks_count` & `pages_count`: Indexing statistics

- **`agents`**: Stores AI voice agent configurations
  - `personality`, `conversation_style`, `system_prompt`
  - `llm_model`, `stt_model`, `tts_voice_id` settings
  - `search_limit`, `context_window` for response generation

- **`agent_url_assignments`**: Links agents to their knowledge bases
  - `assignment_type`: Primary vs secondary URL sources
  - `search_priority`: Order of importance for content retrieval

- **`indexing_jobs`**: Tracks website crawling progress and status

### **Vector Search Implementation:**
- **Real-time Embedding**: Content is chunked and embedded using OpenAI's latest model
- **Semantic Retrieval**: Vector similarity search finds most relevant content chunks
- **Hybrid Search**: Combines vector search with traditional text search for comprehensive results
- **Performance**: Sub-second queries with TiDB Cloud's distributed architecture

### **TiDB Cloud Account**: **satyasandeep786@gmail.com**

## 👥 Meet the Team

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/satyasandeep007">
        <img src="https://github.com/satyasandeep007.png" width="100px;" alt="Satyasandeep Kumar"/><br />
        <sub><b>Satyasandeep Kumar</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/satyasandeep" title="LinkedIn">💼</a>
      <a href="https://twitter.com/satyasandeep76" title="Twitter">🐦</a>
    </td>
     <td align="center">
      <a href="https://github.com/shivamangina">
        <img src="https://github.com/shivamangina.png" width="100px;" alt="Shiva Kumar"/><br />
        <sub><b>Shiva Kumar</b></sub>
      </a><br />
      <a href="https://www.linkedin.com/in/shivamangina/" title="LinkedIn">💼</a>
      <a href="https://twitter.com/shivakmangina" title="Twitter">🐦</a>
    </td>
  </tr>
</table>

 

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

 

**Built with ❤️ for the TiDB Cloud Hackathon**
