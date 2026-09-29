# ✦ NexusForensics

**NexusForensics** is a professional-grade Digital Forensic Case Management System (DFCMS) designed to maintain evidence integrity and streamline forensic workflows. It provides a secure, tamper-evident environment for managing cases, tracking evidence through the Chain of Custody, and performing automated file-carving operations on disk images or binary blobs.

---

## 🚀 Features

### ⚖️ Case Management
- **Centralized Registry:** Track multiple forensic investigations with unique IDs and assigned lead investigators.
- **Detailed Descriptions:** Maintain context for every case within a secure database.

### 🔒 Evidence Locker & Integrity
- **Secure Ingestion:** Upload evidence files directly to the secure locker.
- **SHA-256 Hashing:** Automated cryptographic hashing upon upload to ensure data integrity.
- **Integrity Validation:** System-wide monitoring for evidence tampering or modification.

### 🔍 Automated File Carving
- **High-Performance Scanning:** Uses memory-mapped files (`mmap`) for efficient binary data processing.
- **Multi-Format Recovery:** Automatically carves and recovers JPEG images and PDF documents from raw data.
- **Live Visualization:** Real-time hex-dump animation during carving operations for a high-tech forensic experience.

### 📜 Chain of Custody
- **Tamper-Evident Logs:** Immutable records of every action—from upload to carving and reporting.
- **Audit Trails:** Detailed timestamps and investigator actions to ensure legal admissibility.

### 📊 Professional PDF Reporting
- **Automated Report Generation:** Create high-quality, forensic-standard reports with a single click.
- **Custom Themes:** Sophisticated, dark-themed PDF layouts including:
  - **Dashboard Overview:** System-wide stats and recent activity.
  - **Case Registry:** Full investigator logs and case summaries.
  - **Evidence Manifest:** Detailed item tracking with SHA-256 hashes.
  - **Audit Logs:** Certified Chain of Custody records with signature blocks.

---

## 🛠️ Technology Stack

- **Backend:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) with SQLite
- **Reporting:** [ReportLab](https://www.reportlab.com/) for professional PDF generation
- **Forensics:** `mmap` for binary carving and `hashlib` for SHA-256 integrity
- **Frontend:** TailwindCSS, Vanilla JavaScript, and Custom CSS for a premium "Cyber" aesthetic

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start
1. **Clone the repository** (or extract the project files).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   - On Windows: Double-click `run.bat`
   - Or manually: `python app.py`
4. **Access the interface:**
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 📂 Project Structure

```text
NexusForensics/
├── app.py                # Main Flask application & API routes
├── models.py             # Database schema (Case, Evidence, Custody, etc.)
├── report_generator.py   # Advanced PDF generation logic (ReportLab)
├── requirements.txt      # Python dependencies
├── run.bat               # Windows startup script
├── static/               # Frontend assets (JS, CSS, Images)
│   ├── app.js            # Main UI logic & AJAX handlers
│   └── style.css         # Custom animations & theme tokens
├── templates/            # HTML templates
│   └── index.html        # Main Dashboard interface
├── uploads/              # Secure evidence storage
└── carved_files/         # Directory for recovered forensic artifacts
```

---

## ⚖️ Legal Disclaimer
NexusForensics is designed for educational and professional forensic use. Users are responsible for ensuring that all forensic procedures comply with local laws and regulations regarding evidence handling and privacy.

---
*Created by the NexusForensics Team*
