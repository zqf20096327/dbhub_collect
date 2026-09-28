# AI Resume Analyzer 🚀

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-green.svg)](https://spacy.io/)
[![Database](https://img.shields.io/badge/Database-TiDB%20Cloud-orange.svg)](https://www.pingcap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, full-stack resume screening and analytical profile evaluation platform. Leveraging **Natural Language Processing (NLP)** and relational cloud architectures, this application automates layout text extraction, isolates critical candidate structural blocks, scores resume profiles dynamically, and maps operational logging to a remote cloud-native cluster.

🔗 **Live Deployment URL:** [https://ai-resume-analyzer-fxy7psn2cxwdgr9an4dknr.streamlit.app/](https://ai-resume-analyzer-fxy7psn2cxwdgr9an4dknr.streamlit.app/)

---

## 📌 Project Overview

Manually parsing thousands of resumes presents an immense operational bottleneck in modern recruitment. This project establishes a seamless end-to-end processing pipeline that translates unformatted text profiles within multi-page PDF files into structured, querying-ready talent intelligence metrics.

### 🎯 Key Engineering Objectives
* **Automated Screening:** Instantly strip structural layouts from documents without client-side plugin dependencies.
* **Granular Extraction:** Mine dense skills, objectives, and domain-specific tokens out of unstructured string sets.
* **Proactive Feedback Loops:** Compute dynamic score evaluation blocks, highlighting explicit resume areas requiring content enhancements.
* **Persistent Analytics:** Store structural data parameters within an active serverless cluster, preparing historical logs for programmatic query metrics.

---

## ✨ System Features & Capabilities

### 📄 Document Intelligence Pipeline
* Direct ingestion of multi-page `.pdf` resumes via an isolated multi-threaded handler.
* Fast, native rendering optimizations via **PyMuPDF (`fitz`)** and structured text mapping using **PDFMiner.six**.
* Integrated security filters preventing inline layout viewing blocks on Chromium engine sandboxes.

### 🧠 Deep NLP Mining Matrix
Using matching vectors in **spaCy** and **NLTK**, the application isolates core contextual modules:
* **Identity Indicators:** Name, Email Address, and Contact Channels.
* **Technical Footprints:** Core Skill Vectors, Projects, and Professional Experience arrays.
* **Validation Sub-blocks:** Career Objectives, Clear Declarations, Achievements, and Certifications.

### 📊 Metric Evaluation & Analytics Dashboard
* **Dynamic Scorer:** Allocates weight metrics based on the completeness of structural blocks.
* **Recruiter Dashboard:** Compiles interactive data arrays displaying skill density distributions, domain classifications, and candidate experience thresholds via responsive **Plotly Engine** layouts.

---

## 🏗️ Technical Architecture Flow

```text
       ┌───────────────────────────┐
       │   Uploaded PDF Resume     │
       └─────────────┬─────────────┘
                     │ (Binary Stream)
                     ▼
       ┌───────────────────────────┐
       │   PyMuPDF (fitz) Parser   │
       └─────────────┬─────────────┘
                     │ (Extracted Layout Text)
                     ▼
       ┌───────────────────────────┐
       │  spaCy & NLTK NLP Engines │
       └─────────────┬─────────────┘
                     ├──────────────────────────┐
                     │                          │
                     ▼                          ▼
           [ Skill Mapping ]           [ Pattern Matchers ]
                     │                          │
                     └─────────────────┬────────┘
                                       │
                                       ▼
       ┌───────────────────────────┐
       │   Resume Scoring Engine   │
       └─────────────┬─────────────┘
                     │ (Calculated Analytics)
                     ▼
       ┌───────────────────────────┐
       │  Streamlit Interactive UI │
       └─────────────┬─────────────┘
                     │ (Secure PyMySQL Connection)
                     ▼
       ┌───────────────────────────┐
       │   TiDB Serverless Cloud   │
       └───────────────────────────┘

```

## ⚙️ Managed Technology Stack

| Layer                           | Technologies                                 |
| ------------------------------- | -------------------------------------------- |
| **Frontend UI Engine**          | Streamlit Framework                          |
| **Natural Language Processing** | spaCy Core (`en_core_web_sm`), NLTK          |
| **Document Parsing Core**       | PyMuPDF (`fitz`), PDFMiner.six               |
| **Database Architecture**       | TiDB Cloud Serverless (MySQL Protocol Layer) |
| **Database Connector**          | PyMySQL Runtime Client                       |
| **Data Orchestration**          | Pandas, NumPy                                |
| **Visualization Components**    | Plotly Graphics, Matplotlib                  |

---

# 🚀 Local Deployment Setup

## 1️⃣ Clone the Target Repository

```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer
```

---

## 2️⃣ Instantiate the Isolated Environment

```bash
python -m venv venv
```

### Activate on Windows

```bash
venv\Scripts\activate
```

### Activate on Linux / MacOS

```bash
source venv/bin/activate
```

---

## 3️⃣ Synchronize Core Packages

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Inject Secret Environment Variables

Create the Streamlit secrets directory:

```bash
mkdir .streamlit
```

Create the secrets file:

```bash
touch .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and add your deployment credentials:

```toml
admin_user = "your_admin_username"
admin_password = "your_admin_password"

db_host = "gateway01.your-region.prod.aws.tidbcloud.com"
db_user = "your_unique_cluster_string.root"
db_password = "your_tidb_generated_password"
db_database = "cv"
db_port = 4000
```

---

## 5️⃣ Execute the Main Thread

```bash
streamlit run app.py
```

---

## 🌐 Application Access

After successful deployment, Streamlit will automatically launch the application in your browser.

Default URL:

```text
http://localhost:8501
```

You can now:

* Upload PDF resumes
* Analyze candidate profiles
* Generate resume scores
* Receive AI-powered recommendations
* View recruiter analytics dashboards
* Store candidate insights in TiDB Cloud

## 🛠️ Tech Stack & Architecture Highlights
* **Frontend & UI:** Streamlit
* **Core Language:** Python 3.10+
* **NLP & Processing:** PyPDF2 / pdfminer, NLTK / spaCy for text extraction & keyword analysis
* **Key Features:** Automated resume parsing, skill matching score, and course/skill recommendations
