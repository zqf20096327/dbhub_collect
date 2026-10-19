# 🧠 rag-tidb-knowledge-assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Vector_DB-TiDB_Cloud-orange.svg)](https://tidbcloud.com/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![LLM](https://img.shields.io/badge/Inference-Ollama-black.svg)](https://ollama.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Proyek Chatbot AI berbasis **Retrieval-Augmented Generation (RAG)** menggunakan model embedding **BAAI/bge-m3**, database vektor **TiDB Cloud**, dan Large Language Model lokal **Ollama (Qwen / DeepSeek)** dengan antarmuka interaktif **Streamlit**.

---

## 🌟 Fitur Utama
1. **Semantic Vector Search:** Pencarian dokumen berbasis kemiripan kosinus (`vec_cosine_distance`) di TiDB Cloud.
2. **Anti-Duplikasi Data:** Pengelolaan data otomatis agar tidak terjadi entri ganda saat re-indexing.
3. **Multi-Interface:**
   - **Terminal CLI (`cetbot.py`):** Pengujian cepat dan interaktif langsung dari terminal.
   - **Web UI Streamlit (`app.py`):** Antarmuka web modern dengan streaming chat dan inspeksi sumber referensi.
4. **Streaming Response:** Respons jawaban dihasilkan kata-demi-kata secara real-time.
5. **Auto-Reconnect & Timeout:** Penanganan koneksi database yang aman dan stabil.

---

## 📁 Struktur Direktori
```text
rag-tidb-knowledge-assistant/
├── app.py                # Aplikasi Web UI Streamlit
├── cetbot.py             # CLI Chatbot Interaktif Terminal
├── config.py             # Konfigurasi & kredensial
├── db_connector.py       # Pengelola koneksi TiDB Cloud
├── rag_engine.py         # Inti RAG (Embedding, Retrieval & LLM Generation)
├── knowledge_embed.py    # Script embedding dataset CSV ke TiDB
├── data_knowledge.csv    # Basis pengetahuan (156 entri Q&A)
├── isrgrootx1.pem        # Sertifikat CA SSL TiDB
├── requirements.txt      # Dependensi Python
├── .env.example          # Template konfigurasi environment
└── .streamlit/
    └── config.toml       # Konfigurasi tema Streamlit
```

---

## 🚀 Panduan Menjalankan

### 1. Setup Environment
Salin file template `.env.example` menjadi `.env.local` dan isi kredensial TiDB Anda:
```bash
cp .env.example .env.local
```

Install dependensi:
```bash
pip install -r requirements.txt
```

### 2. Embed Data ke Database (Sekali Saja)
```bash
python knowledge_embed.py
```

### 3. Menjalankan Chatbot di Terminal (CLI)
```bash
python cetbot.py
```

### 4. Menjalankan Chatbot di Web Browser (Streamlit)
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

---

## ☁️ Panduan Deploy ke Streamlit Community Cloud
Proyek ini **100% siap di-deploy ke Streamlit Cloud (gratis)**:
1. Push project ini ke repository GitHub Anda.
2. Buka [share.streamlit.io](https://share.streamlit.io/) dan login dengan GitHub.
3. Pilih repository `rag-tidb-knowledge-assistant` dan set Main file path ke `app.py`.
4. Di bagian **Advanced Settings -> Secrets**, tambahkan konfigurasi TiDB:
   ```toml
   TIDB_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
   TIDB_PORT = 4000
   TIDB_USER = "your_tidb_username"
   TIDB_PASSWORD = "your_tidb_password"
   TIDB_DATABASE = "RAG"
   ```
5. Klik **Deploy**!
