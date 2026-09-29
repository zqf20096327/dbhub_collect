# 🚀 TeamApp + Pixotic AI

<p align="center">
  <img src="./TeamAppLogo.png" alt="TeamApp Logo" width="180">
</p>

<h1 align="center">TeamApp</h1>

<p align="center">
  <b>My Own Messaging App Powered by Pixotic AI</b>
</p>

<p align="center">
  A desktop messaging application built from scratch with Python, Tkinter and my own AI assistant — Pixotic.
</p>

---

## 📱 About TeamApp

**TeamApp** is my own messaging application that I built from scratch using Python.

The goal of this project is to create a modern desktop communication platform where users can chat, manage conversations and interact with an integrated AI assistant.

Instead of simply creating a basic chat interface, I wanted to build my own complete messaging-app concept and connect it with my own AI assistant, **Pixotic AI**.

> 💡 **TeamApp = Messaging Platform**
> 🤖 **Pixotic = AI Assistant**

---

## 🤖 Pixotic AI

**Pixotic** is my own AI assistant that is designed to work as the intelligent layer of the TeamApp ecosystem.

Pixotic can be integrated into TeamApp to provide AI-powered functionality such as:

* 💬 AI conversations
* 🧠 Memory
* 📚 RAG (Retrieval-Augmented Generation)
* 📁 File understanding
* 🔎 Search
* 🌦️ Weather information
* 📋 Task management
* ⏰ Reminders
* 🖼️ Media handling
* 📄 Document/PDF understanding
* 🤖 AI-powered assistance

The long-term goal is to make Pixotic more than a chatbot and turn it into an AI assistant that can be used across my future applications and projects.

---

# 🏗️ Project Architecture

```text
                         ┌──────────────────────┐
                         │       TEAMAPP        │
                         │   Messaging Platform  │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
          ┌───────────────┐                  ┌────────────────┐
          │    Messaging  │                  │   Pixotic AI   │
          │     System    │                  │    Assistant   │
          └───────┬───────┘                  └───────┬────────┘
                  │                                   │
                  │                         ┌─────────┼─────────┐
                  │                         │         │         │
                  │                         ▼         ▼         ▼
                  │                      Memory     RAG     Search
                  │
                  ▼
          ┌────────────────┐
          │  Conversations │
          │     & UI       │
          └────────────────┘
```

---

# 📂 Project Structure

```text
TeamApp/
│
├── logo.png
│
├── README.md
│
├── teamapp.py
│
├── pixotic.py
│
├── requirements.txt
│
├── pixotic_memory.db
│
├── assets/
│   │
│   ├── screenshots/
│   │   ├── teamapp.png
│   │   └── pixotic.png
│   │
│   └── demo/
│       └── teamapp-demo.gif
│
└── .gitignore
```

---

# 📄 File Explanation

### `teamapp.py`

The main TeamApp application.

It contains the messaging application's interface and interaction system.

Main responsibilities:

* TeamApp window
* Sidebar
* Chat interface
* Conversations
* Message input
* User interaction
* Application layout
* Integration point for Pixotic AI

---

### `pixotic.py`

The main Pixotic AI assistant.

It contains the AI-related functionality and acts as the intelligent component of the project.

Pixotic can provide:

* AI responses
* Memory
* RAG
* Search
* Weather
* File processing
* Task functionality
* Media functionality

---

### `logo.png`

The official **TeamApp logo**.

The logo is displayed at the top of this README and represents the TeamApp project.

---

### `pixotic_memory.db`

SQLite database used for Pixotic's memory system.

```text
pixotic_memory.db
        │
        ▼
   ┌──────────┐
   │ memories │
   ├──────────┤
   │ id       │
   │ user_id  │
   │ memory   │
   │ created  │
   └──────────┘
```

This allows Pixotic to store and retrieve relevant memories.

---

# 🎨 TeamApp Interface

TeamApp is designed as a dark-themed desktop messaging application.

The interface contains:

```text
┌─────────────────────────────────────────────────────────┐
│                       TEAMAPP                            │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│ Conversations│              Chat Area                   │
│              │                                          │
│  👤 User 1   │  User: Hello!                            │
│  👤 User 2   │                                          │
│  👤 User 3   │  Pixotic: How can I help you?           │
│              │                                          │
│              │                                          │
│              ├──────────────────────────────────────────┤
│              │  Type a message...              [Send]   │
└──────────────┴──────────────────────────────────────────┘
```

---

# 🤖 Pixotic AI Architecture

```text
                    USER
                     │
                     ▼
              ┌──────────────┐
              │   TeamApp    │
              │  Chat Input  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Pixotic    │
              │ AI Assistant │
              └──────┬───────┘
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
    Memory          RAG          Search
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                AI Response
                     │
                     ▼
                  TeamApp
                     │
                     ▼
                    USER
```

---

# 🧠 Key Features

## 💬 Messaging

TeamApp provides a desktop messaging interface where users can interact through a chat-based UI.

## 🤖 AI Assistant

Pixotic can act as an AI assistant directly inside the TeamApp ecosystem.

## 🧠 Memory

Pixotic includes a memory system using SQLite.

This allows the assistant to save and retrieve useful information.

## 📚 RAG

Pixotic supports the concept of **Retrieval-Augmented Generation (RAG)**.

RAG allows the AI to retrieve relevant information before generating an answer.

```text
User Question
      │
      ▼
   Retrieval
      │
      ▼
Relevant Information
      │
      ▼
      AI Model
      │
      ▼
   Response
```

## 🔎 Search

Pixotic can use search functionality to retrieve information when required.

## 🌦️ Weather

Weather-related queries can be handled through Pixotic.

## 📁 File & Document Understanding

Pixotic can work with files and documents to provide AI-powered assistance.

## 📋 Tasks & Reminders

Pixotic can also be extended with task and reminder functionality.

---

# 🛠️ Technologies Used

### Programming

* 🐍 Python

### GUI

* Tkinter

### Database

* SQLite

### AI

* Google Gemini API

### Data / AI Concepts

* RAG
* AI Memory
* Retrieval
* Prompt Engineering
* LLM Integration

### Development

* VS Code
* Git
* GitHub

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/TeamApp.git
```

```bash
cd TeamApp
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project directory.

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your real API key to GitHub.

Add `.env` to `.gitignore`.

---

# ▶️ Run TeamApp

```bash
python teamapp.py
```

---

# ▶️ Run Pixotic

```bash
python pixotic.py
```

---

# 🖼️ Screenshots

## TeamApp

<p align="center">
  <img src="teamapp.png" alt="TeamApp Screenshot" width="850">
</p>

---

## Pixotic AI

<p align="center">
  <img src="pixotic.png" alt="Pixotic AI Screenshot" width="850">
</p>

---

---

# 🔗 TeamApp + Pixotic

The main idea behind this project is to combine a communication platform with an intelligent AI assistant.

```text
                    TEAMAPP ECOSYSTEM

              ┌───────────────────────┐
              │       TEAMAPP         │
              │                       │
              │   💬 Messaging        │
              │   👥 Conversations    │
              │   🖥️ Desktop UI      │
              └───────────┬───────────┘
                          │
                          │
                          ▼
              ┌───────────────────────┐
              │       PIXOTIC         │
              │       🤖 AI           │
              │                       │
              │   🧠 Memory           │
              │   📚 RAG              │
              │   🔎 Search           │
              │   📁 Files            │
              │   🌦️ Weather          │
              │   📋 Tasks            │
              └───────────────────────┘
```

---

# 🚀 Future Plans

TeamApp and Pixotic are ongoing projects.

Future improvements may include:

* 🌐 Real-time online messaging
* 👥 User accounts
* 🔐 Authentication
* 🗄️ Cloud database
* ☁️ Cloud deployment
* 📱 Mobile application
* 🌍 Web version
* 📞 Voice calling
* 🎥 Video calling
* 📎 File sharing
* 🖼️ Image sharing
* 🔔 Notifications
* 🤖 Deeper Pixotic integration
* 🧠 Advanced AI memory
* 📚 Improved RAG pipeline
* 🔐 End-to-end encryption

---

# 📈 Project Goals

The long-term vision is to evolve TeamApp from a Python desktop project into a complete communication platform with Pixotic AI at its core.

```text
Python Prototype
       │
       ▼
Desktop Messaging App
       │
       ▼
AI Integration
       │
       ▼
Cloud Backend
       │
       ▼
Web + Mobile
       │
       ▼
Complete Communication Ecosystem
```

---

# 👨‍💻 Built By

**Divanshu Singh**

This project was designed and developed by me as a personal project to learn, experiment and build my own messaging platform and AI ecosystem.

I wanted to understand how a messaging application, GUI, database, AI assistant, memory system and RAG functionality could work together inside one project.

---

# ⭐ Why I Built This

I didn't want to only follow tutorials or build another basic Python project.

I wanted to create something that represents my own idea:

> **A messaging application with my own AI assistant built into the ecosystem.**

TeamApp is the communication layer.

Pixotic is the intelligence layer.

Together, they form the foundation of my larger AI and software-development journey.

---

# 📚 What I Learned

Through this project, I worked with and learned about:

* Python application development
* Tkinter GUI development
* Desktop application architecture
* SQLite databases
* AI API integration
* LLM applications
* Prompt engineering
* RAG
* AI memory systems
* File processing
* Search integration
* Environment variables
* Git & GitHub
* Project structure
* Debugging and error handling

---

# ⭐ Support

If you like this project, consider giving the repository a ⭐.

It helps support the project and motivates me to keep improving TeamApp and Pixotic.

---

<p align="center">

### 🚀 TeamApp × Pixotic AI

**Built from scratch. Built to learn. Built to grow.**

</p>
