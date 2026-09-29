# News & Jokes: Making Headlines Funny  

## Project Summary  
This project combines **real-time news search** (via DuckDuckGo) with **contextual joke retrieval** (stored in TiDB vector database using HuggingFace embeddings).  

The workflow uses **LangGraph** to orchestrate multiple tools and **ChatGroq (Llama-3.1)** as the reasoning LLM.  

### Data Flow  
1. **User Query** → Input topic (e.g., "Computer").  
2. **Web Search Tool** → Fetches recent news snippets.  
3. **RAG Search Tool** → Retrieves top related jokes from TiDB using vector search.  
4. **LangGraph Workflow** → LLM composes a **news summary + humor blend**.  
5. **Final Output** → Engaging, informative, and funny news article.  

---

## Features & Functionality  
**Hybrid AI Workflow** – Combines **web search** and **RAG-based joke retrieval**  
**Humorous News Generation** – Summarizes real news with a sense of humour  
**Vector DB Integration (TiDB)** – Stores and retrieves jokes using semantic similarity search  
**LangGraph Orchestration** – Manages multi-tool execution & decision-making  
**Groq-Powered LLM** – Fast inference with **Llama-3.1**  

---

## Run Instructions  

### 1. Clone repo & install dependencies  
```bash
pip install langchain langgraph langchain-community langchain-groq \
            langchain-huggingface peewee tidb-vector datasets duckduckgo-search \
            python-dotenv
```

### 2. Set environment variables  
Create a `.env` file in the project root:
```env
TIDB_HOST=your_tidb_host
TIDB_USERNAME=your_tidb_username
TIDB_PASSWORD=your_tidb_password
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_api_key
```

### 3. Run the app  
```bash
python app.py
```

### 4. Test with a query  
The script already runs with `"Computer"` as an example.  
Modify the last line in `app.py` to test with your own topic.  

---

## Demo Example  

**Input:** `"Computer"`  
**Output (sample):**  
> *"In recent news, tech giants are racing to improve AI chips for computers. And speaking of chips, here’s a joke: Why don’t computers ever get hungry? Because they eat bytes!"*  

![demo output](demo_output.png)

---

## 📂 Tech Stack  
- **LLM**: [Groq Llama-3.1](https://groq.com/)  
- **Workflow**: [LangGraph](https://www.langchain.com/langgraph)  
- **Vector DB**: [TiDB](https://www.pingcap.com/tidb/) + Peewee ORM  
- **Embeddings**: HuggingFace `all-mpnet-base-v2`  
- **Search**: DuckDuckGo API Wrapper  
