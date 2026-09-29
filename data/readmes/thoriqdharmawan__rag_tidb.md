# RAG with TiDB

A simple RAG (Retrieval-Augmented Generation) system that embeds knowledge data into TiDB vector database.

## Features

- Reads question-answer pairs from CSV
- Generates embeddings using Sentence Transformers
- Stores embeddings in TiDB Cloud database

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your database credentials:

```env
DB_HOST=your_host
DB_PORT=4000
DB_USER=your_user
DB_PASSWORD=your_password
DB_DATABASE=RAG
DB_SSL_CA=/etc/ssl/cert.pem
```

3. Prepare your knowledge data in `data_knowledge.csv` with columns: `question` and `answer`

## Usage

Run the embedding script:

```bash
python knowledge_embed.py
```

This will process each row in the CSV and store the text embeddings in the TiDB database.

## Chat Bot

Run the chatbot

```bash
python chat_bot.py
```
