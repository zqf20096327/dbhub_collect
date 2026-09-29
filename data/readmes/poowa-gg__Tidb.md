# CodeMentor AI - Intelligent Code Learning Companion

## 🚀 Project Overview

CodeMentor AI is an innovative, multi-agent system that creates personalized coding learning experiences using TiDB Serverless vector search and AI agents. It analyzes your coding patterns, learns from real-world codebases, and generates tailored learning paths with interactive challenges.

## 🎯 Key Innovation

Unlike traditional coding tutorials, CodeMentor AI:
- **Learns YOUR coding style** using vector embeddings
- **Adapts in real-time** based on your progress and preferences  
- **Uses real codebases** from GitHub to create relevant challenges
- **Chains multiple AI agents** for comprehensive learning experience

## 🏗️ Architecture

### Multi-Agent Workflow:
1. **Code Analysis Agent** - Analyzes user submissions and coding patterns
2. **Knowledge Extraction Agent** - Processes real-world codebases and documentation
3. **Learning Path Agent** - Creates personalized curriculum using vector similarity
4. **Challenge Generator Agent** - Builds interactive coding exercises
5. **Progress Tracker Agent** - Monitors learning and suggests optimizations

### TiDB Serverless Integration:
- **Vector Search**: Code pattern matching and similarity search
- **Full-Text Search**: Documentation and comment analysis
- **Structured Data**: User progress, challenge metadata, learning analytics

## 🛠️ Tech Stack

- **Backend**: Python FastAPI
- **Database**: TiDB Serverless (Vector + SQL)
- **AI/ML**: OpenAI GPT-4, Sentence Transformers
- **Frontend**: React with Monaco Editor
- **External APIs**: GitHub API, Code execution sandbox

## 📊 Data Flow

```
User Code → Vector Embedding → TiDB Vector Search → Similar Patterns
     ↓
Real Codebases → Knowledge Extraction → Learning Content Generation
     ↓
Personalized Challenges → User Interaction → Progress Tracking → Adaptive Learning
```

## 🎮 Features

- **Smart Code Analysis**: Understands your coding style and skill level
- **Personalized Learning Paths**: Tailored curriculum based on your goals
- **Interactive Challenges**: Real-world coding problems with instant feedback
- **Progress Gamification**: XP, badges, and learning streaks
- **Mentor Chat**: AI assistant for coding questions and guidance

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codementor-ai.git
   cd codementor-ai
   ```

2. **Install dependencies**
   ```bash
   # Windows
   .\install.ps1
   
   # Or manually
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the template
   copy .env.example .env
   
   # Edit .env with your actual credentials:
   # - TiDB Serverless connection details
   # - OpenAI API key (optional)
   ```

4. **Run the application**
   ```bash
   python start_app.py
   ```

5. **Open in browser**
   - Main app: http://localhost:8002
   - API docs: http://localhost:8002/docs

## 🎥 Demo Video

[Link to demo video showing the complete workflow]

## 🏆 Why This Wins

- **Truly Innovative**: First AI mentor that learns from YOUR code
- **Multi-Agent Architecture**: Complex workflow with 5+ chained agents
- **Real-World Impact**: Helps developers learn more effectively
- **Technical Excellence**: Advanced vector search and AI integration
- **Great UX**: Gamified, interactive learning experience