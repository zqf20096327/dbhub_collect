🏥 EMR Patient Summary Chatbot

A simple health chatbot demo that summarizes patient records using Retrieval-Augmented Generation (RAG) and answers general medical questions using external agents.

Built as an educational prototype using Azure AI Foundry.

✨ What this does

🧾 Summarizes patient records from a database

🔍 Uses semantic search with vector embeddings

🤖 Answers generic medical questions via external agents

🎛️ Lets you control AI response behavior (temperature, top-p, top-k)

🖥️ Simple web UI for demo

🧠 How it works (very short)

Patient data is stored in MySQL

Data is converted into vector embeddings

User asks a question

System:

uses RAG for patient-specific queries

routes generic questions to an external agent

AI generates a response and shows it in the UI

🛠️ Tech Stack

Platform: Azure AI Foundry

Backend: Python

Frontend: Streamlit

Database: MySQL

Models: Configurable (Azure / open-source / free-tier)

📊 Dataset

Mock EMR data (100-patient sample)

Used only for demonstration

🚧 Project Status

Core logic implemented

Demo is not fully materialized yet

Actively integrating and validating model components

⚠️ Disclaimer

This is a prototype for learning purposes.
Not for real medical use. Not medical advice.

⭐ Notes

Designed to run on free tiers

Focused on architecture and flow, not production scale