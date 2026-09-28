# RAG System with pgvector

[![Built by Groovy Web](https://img.shields.io/badge/Built%20by-Groovy%20Web-0f3460?logo=github&logoColor=white)](https://www.groovyweb.co/?utm_source=github&utm_medium=readme&utm_campaign=rag-pgvector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Production-ready Retrieval-Augmented Generation system using PostgreSQL + pgvector

## 🚀 Overview

A complete, production-ready RAG (Retrieval-Augmented Generation) implementation using PostgreSQL with the pgvector extension. This system combines semantic search with LLM generation to build intelligent applications that can reason over your data.

## ✨ Features

- **Semantic Search**: Vector similarity search with pgvector
- **Hybrid Search**: Combine semantic and keyword search
- **Multiple Embeddings**: Support for OpenAI, Cohere, and local models
- **Chunking Strategies**: Smart document splitting for better retrieval
- **Reranking**: Improve relevance with result reranking
- **Caching**: Reduce costs with intelligent caching
- **Streaming**: Real-time response streaming
- **TypeScript**: Full type safety
- **Production Ready**: Error handling, logging, monitoring
- **Scalable**: Horizontal scaling with connection pooling

## 🏗️ Architecture

```
User Query
    ↓
Embedding Generation
    ↓
Semantic Search (pgvector)
    ↓
Hybrid Search (Keyword + Semantic)
    ↓
Reranking
    ↓
Context Assembly
    ↓
LLM Generation
    ↓
Response Streaming
```

## 📦 Installation

### Prerequisites

- PostgreSQL 15+ with pgvector extension
- Node.js 18+
- OpenAI API key (or other embedding provider)

### Setup

1. **Clone and install**:

```bash
git clone https://github.com/groovy-web/rag-system-pgvector.git
cd rag-system-pgvector
npm install
```

2. **Database setup**:

```bash
# Enable pgvector extension
psql -d yourdb -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Run migrations
npm run db:migrate
```

3. **Environment configuration**:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# LLM
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

4. **Run the example**:

```bash
npm run dev
```

## 🎯 Quick Start

### Basic RAG Query

```typescript
import { RAGSystem } from '@rag-pgvector/core';

const rag = new RAGSystem({
  connectionString: process.env.DATABASE_URL,
  embeddingModel: 'text-embedding-3-small',
  llmModel: 'gpt-4',
});

const response = await rag.query({
  question: 'What are the benefits of TypeScript?',
  topK: 5, // Number of documents to retrieve
  minScore: 0.7, // Minimum similarity score
});

console.log(response.answer);
console.log(response.sources); // Retrieved documents
```

### Ingest Documents

```typescript
import { DocumentStore } from '@rag-pgvector/store';

const store = new DocumentStore({
  connectionString: process.env.DATABASE_URL,
});

// Add a single document
await store.addDocument({
  content: 'TypeScript provides static typing for JavaScript...',
  metadata: {
    title: 'Introduction to TypeScript',
    author: 'John Doe',
    url: 'https://example.com/ts-intro',
  },
});

// Batch ingest
await store.addDocuments([
  { content: 'Doc 1...', metadata: {} },
  { content: 'Doc 2...', metadata: {} },
  { content: 'Doc 3...', metadata: {} },
]);
```

## 📚 Advanced Features

### Custom Chunking

```typescript
import { RecursiveCharacterSplitter } from '@rag-pgvector/chunkers';

const chunker = new RecursiveCharacterSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
  separators: ['\n\n', '\n', '. ', ' ', ''],
});

const chunks = await chunker.split(document);
await store.addChunks(chunks);
```

### Hybrid Search

```typescript
const response = await rag.query({
  question: 'TypeScript vs JavaScript',
  searchType: 'hybrid', // Combine semantic + keyword
  semanticWeight: 0.7, // 70% semantic, 30% keyword
  keywordWeight: 0.3,
  topK: 5,
});
```

### Reranking

```typescript
import { CohereReranker } from '@rag-pgvector/rerankers';

const reranker = new CohereReranker({
  apiKey: process.env.COHERE_API_KEY,
});

const response = await rag.query({
  question: 'What is machine learning?',
  topK: 20, // Retrieve more
  reranker: reranker,
  finalTopK: 5, // Rerank to top 5
});
```

### Streaming Responses

```typescript
const stream = await rag.queryStream({
  question: 'Explain quantum computing',
  topK: 5,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

### Conversation Memory

```typescript
import { ConversationMemory } from '@rag-pgvector/memory';

const memory = new ConversationMemory({
  maxMessages: 10,
  maxTokens: 2000,
});

// First message
await memory.add({
  role: 'user',
  content: 'What is RAG?',
});

const response1 = await rag.query({
  question: 'What is RAG?',
  history: memory.getMessages(),
});

await memory.add({
  role: 'assistant',
  content: response1.answer,
});

// Follow-up with context
const response2 = await rag.query({
  question: 'What are its limitations?',
  history: memory.getMessages(),
});
```

## 🔧 Configuration

### RAG System Options

```typescript
interface RAGConfig {
  // Database
  connectionString: string;
  tableName?: string; // Default: 'documents'

  // Embeddings
  embeddingModel: string;
  embeddingDimensions?: number;
  embeddingProvider?: 'openai' | 'cohere' | 'local';

  // LLM
  llmModel: string;
  llmTemperature?: number;
  llmMaxTokens?: number;

  // Search
  topK?: number; // Default: 5
  minScore?: number; // Default: 0.0

  // Reranking
  reranker?: Reranker;

  // Streaming
  stream?: boolean;

  // Caching
  cacheEnabled?: boolean;
  cacheTTL?: number; // Seconds

  // Logging
  logLevel?: 'debug' | 'info' | 'warn' | 'error';
}
```

### Database Schema

```sql
-- Documents table
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Embeddings table
CREATE TABLE embeddings (
  id SERIAL PRIMARY KEY,
  document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
  embedding vector(1536) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Full-text search index
CREATE INDEX ON documents USING gin(to_tsvector('english', content));
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# Integration tests (requires database)
npm run test:integration
```

## 📊 Monitoring & Analytics

### Query Logging

```typescript
import { QueryLogger } from '@rag-pgvector/monitoring';

const logger = new QueryLogger({
  logLevel: 'info',
  logToDatabase: true,
});

const rag = new RAGSystem({
  // ... config
  logger,
});

// Logs include:
// - Query text
// - Retrieval time
// - Generation time
// - Token usage
// - Source documents
// - Relevance scores
```

### Performance Metrics

```typescript
const metrics = await rag.getMetrics();

console.log({
  averageQueryTime: metrics.avgTime, // ms
  averageTokensUsed: metrics.avgTokens,
  cacheHitRate: metrics.cacheHitRate, // %
  topDocuments: metrics.topDocs, // Most retrieved
});
```

## 🚀 Production Deployment

### Connection Pooling

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Maximum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

const rag = new RAGSystem({
  pool, // Use pool instead of connection string
  // ... other config
});
```

### Horizontal Scaling

```typescript
// Use Redis for distributed caching
import { RedisCache } from '@rag-pgvector/cache';

const cache = new RedisCache({
  url: process.env.REDIS_URL,
  ttl: 3600,
});

const rag = new RAGSystem({
  // ... config
  cache,
});
```

### Error Handling

```typescript
import { CircuitBreaker } from '@rag-pgvector/resilience';

const breaker = new CircuitBreaker({
  timeout: 10000, // 10 seconds
  errorThreshold: 0.5, // 50% failure rate
  resetTimeout: 60000, // 1 minute
});

const rag = new RAGSystem({
  // ... config
  circuitBreaker: breaker,
});
```

## 📖 Use Cases

### 1. Customer Support Chatbot

```typescript
const response = await rag.query({
  question: 'How do I reset my password?',
  metadata: {
    category: 'account-management',
    language: 'en',
  },
});
```

### 2. Document Search

```typescript
const results = await rag.search({
  query: 'machine learning algorithms',
  filters: {
    type: 'research-paper',
    year: { $gte: 2023 },
  },
  topK: 10,
});
```

### 3. Knowledge Base Assistant

```typescript
const assistant = new KnowledgeAssistant({
  rag,
  systemPrompt: `You are a helpful assistant.
  Answer questions based on the provided context.
  If you don't know, say "I don't have that information."`,
});

const response = await assistant.chat({
  userId: 'user-123',
  message: 'What is our refund policy?',
  conversationHistory: true,
});
```

### 4. Code Documentation

```typescript
const codeRAG = new RAGSystem({
  // ... config
  chunker: new CodeChunker({
    language: 'typescript',
    chunkSize: 500,
  }),
});

const explanation = await codeRAG.query({
  question: 'How does the authentication middleware work?',
  metadata: {
    repository: 'my-app',
    language: 'typescript',
  },
});
```

## 🔧 API Reference

### RAGSystem

| Method | Description |
|--------|-------------|
| `query(options)` | Query with context retrieval and generation |
| `queryStream(options)` | Streaming query response |
| `search(options)` | Search without LLM generation |
| `addDocument(doc)` | Add a single document |
| `addDocuments(docs)` | Batch add documents |
| `deleteDocument(id)` | Delete a document |
| `updateDocument(id, doc)` | Update document content |

### DocumentStore

| Method | Description |
|--------|-------------|
| `addDocument(doc)` | Add document with embedding |
| `addDocuments(docs)` | Batch add documents |
| `search(query, options)` | Semantic search |
| `hybridSearch(query, options)` | Hybrid semantic + keyword search |
| `delete(id)` | Delete by ID |
| `update(id, doc)` | Update document |

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](./LICENSE)

## 🔗 Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostgreSQL Vector Search](https://www.postgresql.org/docs/current/textsearch.html)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [RAG Best Practices](./docs/best-practices.md)

## ⭐ Support

If you find this helpful, please give us a star!

---

Made with ❤️ by Groovy Web

---

## Related Repositories

Explore more open-source tools from [Groovy Web](https://www.groovyweb.co/?utm_source=github&utm_medium=readme&utm_campaign=cross-link):

- **[langchain-multi-agent-example](https://github.com/groovy-web/langchain-multi-agent-example)** -- Multi-agent systems tutorial with LangChain
- **[rag-system-pgvector](https://github.com/groovy-web/rag-system-pgvector)** -- Production RAG with PostgreSQL + pgvector
- **[rag-systems-production](https://github.com/groovy-web/rag-systems-production)** -- Enterprise-grade RAG systems
- **[ai-testing-mcp](https://github.com/groovy-web/ai-testing-mcp)** -- AI testing via Model Context Protocol
- **[edge-computing-starter](https://github.com/groovy-web/edge-computing-starter)** -- Cloudflare Workers + Hono template
- **[claude-code-workflows](https://github.com/groovy-web/claude-code-workflows)** -- Workflows for Claude Code
- **[groovy-web-ai-agents](https://github.com/groovy-web/groovy-web-ai-agents)** -- Production AI agent configs
- **[groovy-web-examples](https://github.com/groovy-web/groovy-web-examples)** -- Groovy/Grails examples
