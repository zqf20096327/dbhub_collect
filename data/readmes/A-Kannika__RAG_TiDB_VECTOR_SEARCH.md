# Retrieval Augmented Generation (RAG) with TiDB Vector Search

A Retrieval-Augmented Generation (RAG) system using TiDB's vector search capabilities for cybersecurity knowledge management.

## Overview

This project demonstrates how to build a RAG system that stores cybersecurity documents as vector embeddings in TiDB and retrieves relevant information to answer user queries using a local LLM (Llama 3.2 via Ollama).

## Features

- **Vector Embeddings**: Uses `BAAI/bge-m3` model to generate 1024-dimensional embeddings
- **TiDB Vector Search**: Leverages TiDB's native vector search with cosine distance
- **Local LLM Integration**: Integrates with Ollama (Llama 3.2) for response generation
- **Cybersecurity Knowledge Base**: Pre-loaded with 20 cybersecurity concept documents

## Prerequisites

- Python 3.10+
- TiDB Cloud account (or local TiDB instance with vector search support)
- Ollama installed locally with Llama 3.2 model

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

3. Create a `credentials.yml` file in the project root:
```yaml
TiDB:
  host: your-tidb-host
  port: 4000
  user: your-username
  password: your-password
  database: your-database
  ssl_ca: path-to-ca-cert
```

4. Ensure Ollama is running with Llama 3.2:
```bash
ollama pull llama3.2
ollama serve
```

## Database Setup

Create the required table in TiDB:
```sql
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document TEXT,
    embedding VECTOR(1024)
);
```

## Usage

The Jupyter notebook `RAG_TiDB_VECTOR_SEARCH.ipynb` contains the complete workflow:

1. **Connect to TiDB**: Establishes secure connection to TiDB Cloud
2. **Generate Embeddings**: Converts text documents to vector embeddings
3. **Store Documents**: Inserts documents with embeddings into TiDB
4. **Query System**: Retrieves relevant documents using vector similarity search
5. **Generate Responses**: Uses RAG to answer questions based on retrieved context

### Example Queries

```python
# Query the system
query_text = "What is the meaning of Security Awareness?"
response = generate_response(connection, query_text)
print(response)
```

The system will:
1. Convert the query to a vector embedding
2. Find the top 5 most similar documents using cosine distance
3. Pass the retrieved documents as context to the LLM
4. Generate a contextually relevant response

## Project Structure

```
.
├── RAG_TiDB_VECTOR_SEARCH.ipynb  # Main notebook with implementation
├── requirement.txt                # Python dependencies
├── credentials.yml                # Database credentials (not in repo)
└── README.md                      # This file
```

## Key Components

- **Embedder**: `SentenceTransformer("BAAI/bge-m3")` for generating embeddings
- **Vector Search**: TiDB's `vec_cosine_distance()` function for similarity matching
- **LLM**: Ollama with Llama 3.2 for response generation

## How It Works

1. Documents are embedded using the BGE-M3 model (1024 dimensions)
2. Embeddings are stored as JSON in TiDB alongside the original text
3. User queries are converted to embeddings using the same model
4. TiDB performs vector similarity search using cosine distance
5. Top-k relevant documents are retrieved and used as context
6. Llama 3.2 generates a response based on the retrieved context

## Example Output

**Query1**: "What is the meaning of Security Awareness?"

**Response**: "According to the context provided, Security Awareness refers to educating employees about common cyber threats, organizational security policies, and best practices for protecting sensitive information, significantly reducing the risk of human error in security breaches."

**Query2**: "What is the meaning of Pentest?"

**Response**: "The term "Pentest" is an abbreviation for Penetration Testing, which I mentioned earlier in our context. In this case, "Pentest" refers to a simulated cyber attack against a computer system conducted by security engineers to identify vulnerabilities and weaknesses, thereby strengthening the overall security posture of the organization."

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
