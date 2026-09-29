# 🚀 TiDB AgentX Hackathon 2025: Autonomous Crypto Trading Agent

**An innovative, multi-step, agentic solution that leverages Google's Gemini LLM for trading decisions, powered by TiDB Cloud's serverless vector database for historical market context.**

---

# 🚀 Хакатон TiDB AgentX 2025: Автономный Криптовалютный Торговый Агент

**Инновационное, многошаговое агентное решение, использующее LLM Google Gemini для принятия торговых решений и бессерверную векторную базу данных TiDB Cloud для получения исторического рыночного контекста.**

- **[English Version](#english-version)**
- **[Русская версия](#русская-версия)**

---

## English Version

### 🎥 Demo Video

*<[Link to your 3-minute demo video will be here](https://youtube.com/your-video-link)>*

### 💡 The Idea

Traditional algorithmic trading relies on rigid, pre-programmed rules. Such systems are fragile and often fail to adapt to unpredictable market volatility.

Our project introduces a next-generation **autonomous trading agent**. Instead of hard-coded logic, it uses the advanced reasoning capabilities of a Large Language Model (Google Gemini) to make trading decisions. The key innovation is how we provide context to the LLM: by using **TiDB Cloud's Vector Search** to find historically similar market patterns. This allows the agent to make informed decisions based on what happened in the past under similar conditions.

### 🏛️ Architecture and Data Flow

Our system follows a clear, agentic loop, with TiDB Cloud at its core for memory and context.

![Architecture Diagram](https://i.imgur.com/your-diagram-image.png) <!-- It is highly recommended to create and upload a simple diagram -->

1.  **Data Ingestion**: A local MCP (Model-Context-Protocol) server periodically fetches the latest market data (candlesticks/klines) for a given symbol (e.g., `BTC/USDT`) from the **Binance API**.
2.  **Vectorization & Storage**: The fresh market data is converted into a high-dimensional vector using a sentence-transformer model. Both the raw data and its vector embedding are stored in a `market_data` table in our **TiDB Serverless** instance.
3.  **Context Retrieval (The Magic ✨)**: Before making a decision, the agent queries TiDB. It takes the vector of the *current* market situation and uses **TiDB Vector Search** (`VEC_COSINE_DISTANCE`) to find the top K most similar historical market situations from the database.
4.  **LLM-Powered Decision Making**: A detailed prompt is constructed for the **Google Gemini API**. This prompt includes:
    *   The current market data.
    *   The most similar historical data retrieved from TiDB.
    *   A clear instruction to return a decision in a `ACTION|REASON` format (e.g., `BUY|The pattern resembles a breakout after a consolidation period.`).
5.  **Action Execution**: The agent parses Gemini's response. If the decision is `BUY` or `SELL`, it executes the trade through the **Binance API**.
6.  **Logging**: The entire context (prompt) and the LLM's decision are logged in a `trade_history` table in TiDB for future analysis and auditing.

### 🚀 How It Uses TiDB Cloud

TiDB Cloud is the backbone of our agent's "memory" and "intelligence".

*   **TiDB Serverless**: We chose Serverless for its scalability and cost-effectiveness, which is perfect for a hackathon. It handles unpredictable loads without manual intervention.
*   **TiDB Vector Search**: This is the core feature enabling our agent's contextual awareness. By storing market data as vectors, we can instantly find similar historical patterns. This is far more powerful than simple rule-based comparisons and provides rich, relevant context for the LLM. It transforms TiDB from a simple database into a long-term memory for our AI agent.

### 💻 Tech Stack

-   **Backend**: Python, FastAPI
-   **Database**: TiDB Cloud (Serverless with Vector Search)
-   **LLM**: Google Gemini API
-   **Exchange API**: Binance (via `ccxt` library)
-   **Vectorization**: `sentence-transformers`
-   **DB Driver**: `sqlalchemy`, `tidb-vector`

### 🔧 Run Instructions (How to Get Started)

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/mcp_trading_agent.git
    cd mcp_trading_agent
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables**:
    -   Copy the `.env.example` file to a new file named `.env`.
    -   `cp .env.example .env`
    -   Fill in your credentials in the `.env` file:
        -   `TIDB_CONNECTION_STRING`: Get this from your TiDB Cloud cluster's "Connect" dialog (SQLAlchemy format).
        -   `BINANCE_API_KEY` & `BINANCE_SECRET_KEY`: Generate these in your Binance account.
        -   `GEMINI_API_KEY`: Get this from Google AI Studio.

4.  **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```
    The server will start on `http://localhost:8000`.

5.  **Interact with the Agent**:
    -   Open your browser and go to `http://localhost:8000/docs` to see the OpenAPI documentation.
    -   To trigger a trading decision cycle for `BTC/USDT`, send a POST request to the `/trade/analyze/BTC/USDT` endpoint.
