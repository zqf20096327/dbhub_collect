# z1-Chat 🚀

> **Built for [Cloneathon](https://cloneathon.t3.chat/)** - A real-time multi-user chat application with resumable LLM streaming

A next-generation chat application that demonstrates how to build scalable, real-time applications with **resumable AI streaming**. Built with [Zero's sync engine](https://zero.rocicorp.dev/) for insane scalability and PostgreSQL for rock-solid persistence.

## ✨ Key Features

- 🔄 **Resumable AI Streaming** - Reload the page mid-response? No problem, the stream continues seamlessly
- 🧠 **Multiple LLM Models** - Powered by OpenRouter with support for various AI models
- 🔐 **Flexible Authentication** - Support for both authenticated and anonymous users
- 📱 **Modern UI** - Clean, responsive interface built with React and Tailwind CSS
- ⚡ **Lightning Fast** - Optimized for performance with minimal database operations

## 🏗️ Architecture

This project showcases an innovative streaming architecture that solves the challenge of **resumable LLM responses at scale**:

### The Problem

Streaming every token through PostgreSQL/Zero isn't scalable. But users expect real-time updates and resumable streams.

### The Solution

A hybrid approach using **Redis for streaming state** and **PostgreSQL for persistence**:

1. **Start Stream**: Insert message with `isStreaming: true` and empty content into PostgreSQL
2. **Real-time Sync**: Zero immediately syncs this "streaming" message to all connected clients
3. **Token Streaming**: Client opens SSE connection for that specific message (not the entire chat)
4. **Redis Buffering**: Stream tokens are stored in Redis and sent via Server-Sent Events
5. **Resumable Magic**: New/reconnecting clients get caught up instantly from Redis buffer
6. **Completion**: Final message content saved to PostgreSQL, `isStreaming: false`, Redis cleanup

### Key Benefits

- **Only 2 PostgreSQL operations per message** (insert → update)
- **Multiple concurrent streams** per chat thread
- **Resumable streams** - refresh mid-response and it continues

## 🛠️ Tech Stack

### Frontend

- **React 19** - Latest React with concurrent features
- **TanStack Router/Start** - Type-safe routing and SSR
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Zero Client** - Reactive data synchronization

### Backend

- **TanStack Start** - Full-stack React framework
- **PostgreSQL** - Primary database with logical replication
- **Redis** - Streaming state management
- **Prisma** - Type-safe database ORM
- **Better Auth** - Modern authentication

### AI & Streaming

- **OpenRouter** - Multi-model LLM access
- **AI SDK** - Streaming text generation
- **Server-Sent Events** - Real-time token streaming
- **Zero Sync** - Reactive state management

### Infrastructure

- **Docker Compose** - Local development environment
- **TypeScript** - End-to-end type safety

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Docker & Docker Compose
- pnpm (recommended)

### Quick Start

1. **Clone the repository**

    ```bash
    git clone https://github.com/akshat-OwO/z1-chat
    cd z1-chat
    ```

2. **Install dependencies**

    ```bash
    pnpm install
    ```

3. **Start the infrastructure**

    ```bash
    docker-compose up -d
    ```

4. **Set up environment variables**

    ```bash
    cp .env.example .env
    # Edit .env with your GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET and OPENROUTER_API_KEY
    ```

5. **Run database migrations**

    ```bash
    pnpm prisma:migrate
    ```

6. **Run zero-cache server**

    ```bash
    npx zero-cache-dev
    ```

7. **Start the development server**
    ```bash
    pnpm dev
    ```

Visit `http://localhost:3000` and start chatting!

## 🔧 Configuration

### Environment Variables

```bash
cp .env.example .env
```

### Available Models

The application supports multiple LLM models via OpenRouter:

- **Google Gemini 2.0 Flash** (default for chat titles)
- **OpenAI GPT models**
- **Anthropic Claude**
- **And many more...**

## 📊 Database Schema

The application uses a clean, optimized schema:

- **Users** - Authentication and user management
- **Chats** - Chat threads with metadata
- **Messages** - Individual messages with streaming state
- **Sessions/Accounts** - Authentication data

Key optimizations:

- Minimal fields for fast queries
- Proper indexing for real-time performance
- Zero sync generation for reactive updates

## 🎯 Why This Architecture?

### Traditional Approach Problems:

- ❌ Lost streams on page refresh
- ❌ Complex state management for multiple concurrent streams
- ❌ Poor user experience during network issues

### Solution Benefits:

- ✅ **2 DB operations per message** regardless of response length
- ✅ **Resumable streams** - refresh anytime, stream continues
- ✅ **Multiple concurrent streams** per chat
- ✅ **Instant catch-up** for new connections
- ✅ **Scales horizontally** with Redis clustering

## 📸 Demo

https://github.com/user-attachments/assets/573da14e-affe-49de-85ba-cf661f617c23


## 🚀 What I Want to Add

This project has several exciting features planned for future development:

### 🌐 Deployment & Hosting
- **Production Deployment** - Currently local-only, planning to deploy to cloud platforms

### 👥 Multiplayer Chat Features
- **Shareable Chats** - Generate shareable links for chat conversations
- **Collaborative Editing** - Multiple users can participate in the same chat thread

### 🎨 Enhanced Code Experience
- **Advanced Syntax Highlighting** - Better code block rendering with language detection
- **Code Execution** - Interactive code blocks with execution capabilities

### 🌳 Chat Branching & Navigation
- **Conversation Branching** - Fork conversations at any point to explore different paths
- **Visual Chat Tree** - Tree-like visualization of conversation branches
- **Quick Navigation** - Jump between different branches and conversation points
- **Branch History** - Track and manage conversation branch history


## 🤝 Contributing

This project was built for the [Cloneathon](https://cloneathon.t3.chat/) - feel free to explore, learn, and build upon it!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Zero](https://zero.rocicorp.dev/)** - For the incredible sync engine that makes real-time updates effortless
- **[Cloneathon](https://cloneathon.t3.chat/)** - For the inspiration and platform to build this
- **[Mark MacLeod](https://x.com/marbemac/status/1929922350549479564)** - For sharing the original tweet that inspired this architecture

Built with ❤️ for the developer community. Happy chatting! 💬
