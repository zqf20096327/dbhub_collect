# Vector Search Legal Analysis System

A multi-agent legal document analysis system built with vector search capabilities using TiDB Vector, Google ADK agents, and custom embedding models.

## Features

- **Multi-Agent Architecture**: Specialized agents for document ingestion, search, and analysis
- **Vector Search**: Efficient similarity search using TiDB Vector database
- **Legal Document Processing**: Support for PDF and DOCX document formats
- **Custom Embeddings**: Reliable hash-based embedding model for consistent results
- **Court API Integration**: External API client for legal data retrieval

## Dependencies

- `sentence-transformers==2.2.0` - Text embedding generation
- `google-adk` - Agent development kit
- `tidb-vector` - Vector database client
- `pymysql` - MySQL database connector
- `requests` - HTTP client for API calls
- `python-docx` - Word document processing
- `pypdf2` - PDF document processing
- `torch` - Machine learning framework
- `dotenv` - Environment variable management

## Project Structure

```
├── legal_agents/          # Agent implementations
│   └── sub_agents/
│       ├── ingest_agent/  # Document ingestion
│       ├── search_agent/  # Vector search
│       └── analysis_agent/# Document analysis
├── external_tools/        # API clients and processors
├── config/               # Database configuration
├── utils/                # Helper utilities
└── tests/                # Test files
```

## Setup

1. Install dependencies: `uv pip install -e .`
2. Configure environment variables in `.env`
3. Run the main application: `python main.py`
