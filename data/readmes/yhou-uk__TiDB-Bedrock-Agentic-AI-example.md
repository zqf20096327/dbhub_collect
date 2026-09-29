# TiDB Bedrock Agentic example

Intelligent data access patterns with TiDB and Amazon Bedrock - comparing RAG vs Agentic approaches.

## Overview

This notebook demonstrates two complementary AI approaches for querying data:

1. **RAG (Retrieval-Augmented Generation)**: Vector similarity search with TiDB + Amazon Bedrock
2. **Agentic Application**: AI agent with MCP tools for structured database operations

## Quick Start

### Prerequisites
- Python 3.10+
- AWS credentials configured for Bedrock access
- TiDB instance running locally

### Installation
```bash
# Install TiDB locally
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup playground
```

### Usage
1. Start TiDB playground: `tiup playground`
2. Open `tidb-bedrock-agentic.ipynb`
3. Run cells sequentially

## Features

### RAG System
- **Vector Store**: TiDB with HNSW indexing
- **Embeddings**: Amazon Titan Text Embeddings V2
- **Generation**: Claude 4 Sonnet via Bedrock
- **Best for**: Conceptual questions, semantic understanding

### Agentic System  
- **AI Agent**: Strands framework with Claude 4 Sonnet
- **Tools**: MCP server for database operations
- **Best for**: Precise queries, calculations, structured data


## License

MIT License - See notebook for full implementation details.