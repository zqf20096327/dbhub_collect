# 🤖 AI Chatbot

An AI-powered chatbot built using **Python, Streamlit, FastAPI, Hugging Face, and TiDB Cloud**. The chatbot supports intelligent conversations, remembers previous chats, protects against prompt injection attacks, stores chat history in a cloud database, reads PDF documents, and generates AI voice responses.

---

## 📌 Features

- 💬 Intelligent AI Chatbot
- 🧠 Conversation Memory
- 🛡️ Prompt Guardrails
- 📄 PDF Upload & Question Answering
- 🔊 AI Voice Response
- 💾 Chat History Storage
- ☁️ TiDB Cloud Database
- ⚡ FastAPI REST API
- 🎨 Streamlit Interactive UI
- 📥 Download Chat History

---

## 🏗️ Project Architecture

```
              User
                │
                ▼
      Streamlit Frontend
                │
                ▼
         FastAPI Backend
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
 Guardrails          Conversation Memory
      │                   │
      └─────────┬─────────┘
                ▼
        Hugging Face LLM
                │
                ▼
        TiDB Cloud Database
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| Streamlit | User Interface |
| FastAPI | REST API |
| Hugging Face | Large Language Model |
| TiDB Cloud | Database |
| MySQL Connector | Database Connectivity |
| PyPDF2 | PDF Reading |
| gTTS | AI Voice Response |
| Requests | API Communication |
| Python Dotenv | Environment Variables |

---

## 📂 Project Structure

```
AI_chatbot_project/
│
├── app.py                 # Streamlit UI
├── main.py                # FastAPI API
├── chatbot.py             # LLM Integration
├── database.py            # Database Connection
├── history.py             # Save Chat History
├── memory.py              # Conversation Memory
├── guardrails.py          # Prompt Protection
├── config.py              # Configuration
├── test_chatbot.py
├── test_connection.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/Sunitha388/AI_chatbot_project1.git
```

```bash
cd AI_chatbot_project1
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file.

```
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN

DB_HOST=YOUR_DATABASE_HOST
DB_PORT=4000
DB_USER=YOUR_USERNAME
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=chatbot_db
```

---

### Start FastAPI

```bash
uvicorn main:app --reload
```

---

### Start Streamlit

```bash
streamlit run app.py
```

---

## 💻 API Endpoint

### Health Check

```
GET /
```

### Chat Endpoint

```
POST /chat
```

Request

```json
{
    "message":"Hello"
}
```

Response

```json
{
    "response":"Hello! How can I assist you today?"
}
```

---

## 📸 Screenshots

### Chat Interface

> Add a screenshot here.

Example:

```
assets/chatbot.png
```

---

## 🔮 Future Improvements

- 🎤 Speech-to-Text (Voice Input)
- 🖼️ Image Understanding
- 📚 RAG (Retrieval-Augmented Generation)
- 🗂️ Vector Database
- 👤 User Authentication
- 🌐 Multi-user Sessions
- ☁️ Cloud Deployment (Render/Vercel)

---

## 📈 Skills Demonstrated

- Python Programming
- FastAPI
- Streamlit
- REST APIs
- Hugging Face LLM Integration
- Prompt Engineering
- AI Guardrails
- Database Design
- Conversation Memory
- Cloud Database (TiDB)
- Git & GitHub

---

## 👩‍💻 Author

**Sunitha**

GitHub: https://github.com/Sunitha388

---

## ⭐ If you found this project helpful, please consider giving it a star!
