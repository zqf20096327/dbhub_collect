# InsightWeaver

https://vimeo.com/1118614972?share=copy

https://poe.com/InsightWeawer

InsightWeaver Agent is a multi-step autonomous assistant that demonstrates the power of TiDB Serverless with vector search.

Features:
📂 Upload and ingest multi-format data (PDFs, chat logs, transcripts).
🔍 Perform semantic + full-text hybrid search on stored content.
🧠 Summarize and recommend next steps with LLM reasoning.
🔗 Trigger external integrations (Slack, Trello) for actionable outcomes.
🔄 End-to-end flow: Raw Data → Indexed → Search → LLM → Action.
Functionality Demo Use Case:
A customer support team uploads logs of refund requests. InsightWeaver indexes and searches complaints, clusters issues using LLM, and automatically posts top findings into Slack for the product team.

Data Flow:
Ingestion – User uploads PDFs or chat logs. Documents are embedded using OpenAI embeddings and stored in TiDB Serverless with vector indexes + metadata.
Retrieval – Queries trigger hybrid search (vector similarity + full-text). Results are ranked and merged.
Analysis – Retrieved results are passed into an LLM for summarization and recommendation.
External Action – Based on findings, the agent automatically posts into Slack or creates a Trello task.
Output – Summarized insights + confirmation are shown in the UI.
Integrations:
TiDB Serverless (vector + full-text search)
LLM API (OpenAI, Gemini, or Claude)
Slack API (webhook)
Trello API (optional fallback action)

📌 InsightWeaver Agent
InsightWeaver Agent is a multi-step autonomous assistant built on TiDB Serverless (with vector search). It ingests unstructured data, retrieves relevant context with hybrid search, analyzes it with an LLM, and triggers external actions like Slack notifications or Trello tasks — all in a single automated workflow.
🚀 Features
📂 Ingest & Index Data
Upload PDFs, chat logs, or transcripts. Extracted text is embedded and stored in TiDB Serverless with vector indexes.
🔍 Hybrid Search (Vector + Fulltext)
Combine semantic similarity search with keyword-based full-text queries for high-precision retrieval.
🧠 LLM-Powered Insights
Summarize, cluster, or analyze retrieved data with an LLM (OpenAI, Claude, Gemini).
🔗 External Integrations
Automatically trigger downstream actions:
Post urgent findings to Slack
Create issue cards in Trello
🔄 End-to-End Flow
Raw Data → TiDB Storage → Search → LLM Analysis → External Action.
🗂 Data Flow & Integrations
Ingest Data → User uploads files → embeddings generated → stored in TiDB Serverless.
Search → Hybrid vector + keyword queries against indexed data.
Analysis → Results sent to an LLM for summarization/recommendations.
Action → Insights posted to Slack (if urgent) or Trello (otherwise).
Output → Final results displayed in the app.
Integrations Used:
TiDB Cloud (Serverless) – vector search + full-text search
OpenAI API – embeddings + analysis
Slack Webhook – team notifications
Trello API – issue/task tracking
🛠 Run Instructions
See RUN_INSTRUCTIONS.md for full setup.
Quickstart:
# Clone repo
git clone https://github.com/<your-username>/insightweaver-agent
cd insightweaver-agent

# Install deps
pip install -r requirements.txt

# Set environment variables
export TIDB_URL="<your_tidb_url>"
export TIDB_API_KEY="<your_tidb_key>"
export OPENAI_API_KEY="<your_openai_key>"
export SLACK_WEBHOOK="<your_slack_webhook_url>"
export TRELLO_API_KEY="<your_trello_key>"

# Run the agent
python src/agent.py
Then upload demo data (demo_data/sample_chats.json) and query:
What are the top refund issues?

🏃 Run Instructions – InsightWeaver Agent
📦 Prerequisites
TiDB Cloud account (Serverless cluster with vector search enabled)
Python 3.10+ (or Node.js 18+ if you adapt to JS)
API keys / tokens:
TiDB Cloud connection string + API key
LLM provider (e.g., OpenAI API key)
Slack Webhook URL (optional, for notifications)
Trello API key + token (optional, for task creation)
⚙️ Setup
Clone the repository
git clone https://github.com/<your-username>/insightweaver-agent
cd insightweaver-agent
Install dependencies
pip install -r requirements.txt
Configure environment variables
Create a .env file in the project root or export variables directly:
export TIDB_URL="<your_tidb_url>"
export TIDB_API_KEY="<your_tidb_api_key>"
export OPENAI_API_KEY="<your_openai_key>"
export SLACK_WEBHOOK="<your_slack_webhook_url>"
export TRELLO_API_KEY="<your_trello_api_key>"
export TRELLO_TOKEN="<your_trello_token>"
▶️ Running the Application
Start the agent
python src/agent.py
Upload demo data
Example dataset is provided in demo_data/sample_chats.json.
Upload it through the CLI prompt or UI (if configured).
Run a query
What are the top refund issues?
Observe results
The app displays summarized findings in the console/UI.
If urgent issues are detected → a message is posted to Slack.
Otherwise → a Trello card is created automatically.
✅ Verification
TiDB Cloud → Check that documents and embeddings were inserted.
Slack/Trello → Confirm that insights are posted automatically.
Console/UI → See summary of results and confirmation of external action.
🧪 Example Workflow
Upload 20 customer support chat logs.
Ask: “What recurring refund problems are customers facing?”
Agent finds: “Delayed refunds, missing confirmation emails, and duplicate charges.”
Posts urgent findings into Slack → “Top 3 refund issues detected in support logs.”
