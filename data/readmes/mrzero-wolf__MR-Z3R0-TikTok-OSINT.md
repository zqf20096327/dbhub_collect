# 🔎 MR Z3R0 TikTok OSINT

### Cross-Platform TikTok OSINT & Public Profile Research Framework

**MR Z3R0 TikTok OSINT** is a Python-based Open Source Intelligence (OSINT) tool for researching **publicly available TikTok profile information** and organizing results into structured reports.

Built for:

**📱 Termux** · **🐧 Linux** · **🪟 Windows**

---

## ⚡ Overview

MR Z3R0 TikTok OSINT provides a command-line interface for authorized OSINT research.

The framework can:

- 🔍 Analyze public TikTok profiles
- 👤 Collect public profile information
- 📊 Retrieve public account statistics
- 🎬 Collect public video metadata
- 📝 Extract links and contact information voluntarily published in profile text
- 📍 Report publicly available location metadata when present
- 💾 Store results in SQLite
- 📄 Generate JSON reports
- 📃 Generate TXT reports
- 📂 Process multiple usernames from a file
- 🌐 Support proxy configuration
- 🎨 Provide colored terminal output
- 🖥️ Work across multiple operating systems

> ⚠️ **Important:** This project is intended for lawful OSINT, research, education, and authorized investigations. Do not use it to obtain private information, bypass access controls, or target individuals without a legitimate and lawful reason.

---

## ✨ Features

| Feature | Status |
|---|---|
| 👤 Public Profile Information | ✅ |
| 📊 Followers / Following | ✅ |
| ❤️ Likes / Video Count | ✅ |
| ✔️ Verification Status | ✅ |
| 🔒 Public/Private Account Status | ✅ |
| 📝 Biography | ✅ |
| 🔗 Public Bio Links | ✅ |
| 📧 Publicly Listed Email Detection | ✅ |
| 📞 Publicly Listed Phone Detection | ✅ |
| 📍 Public Location Metadata | ✅ |
| 🎬 Video Metadata | ✅ |
| #️⃣ Hashtag Extraction | ✅ |
| @️⃣ Mention Extraction | ✅ |
| 🖼️ Avatar URLs | ✅ |
| 💾 SQLite Database | ✅ |
| 📄 JSON Reports | ✅ |
| 📃 TXT Reports | ✅ |
| 📂 Multiple Targets | ✅ |
| 🌐 Proxy Support | ✅ |
| 🎨 Colored CLI | ✅ |
| 📱 Termux | ✅ |
| 🐧 Linux | ✅ |
| 🪟 Windows | ✅ |

---

# 🛠️ Requirements

You need:

```bash
Python 3.x
pip
Internet connection
```

The following Python packages are used:

```bash
requests
colorama
python-dotenv
```

The program also includes automatic dependency installation.

---

# 📦 Installation

## 📱 Termux

```bash
pkg update
pkg install python
```

Then run the script:

```bash
python mr_z3ro.py --user example
```

The script will automatically check and install missing dependencies.

---

## 🐧 Linux

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

Run:

```bash
python3 mr_z3ro.py --user example
```

---

## 🪟 Windows

Install Python 3.x and make sure Python is available from the command line.

Then run:

```bash
python mr_z3ro.py --user example
```

---

# 🚀 Usage

## 👤 Scan a Single Username

```bash
python mr_z3ro.py --user username
```

Example:

```bash
python mr_z3ro.py --user example
```

The `@` symbol is automatically removed if supplied.

```bash
python mr_z3ro.py --user @example
```

---

# 🎬 Fetch Public Videos

Specify the maximum number of public videos to process:

```bash
python mr_z3ro.py --user example --videos 20
```

Example with a larger limit:

```bash
python mr_z3ro.py --user example --videos 50
```

Use reasonable limits and respect platform rate limits.

---

# 📂 Scan Multiple Users

Create a text file:

```bash
nano users.txt
```

Add one username per line:

```text
user_one
user_two
user_three
user_four
```

Then run:

```bash
python mr_z3ro.py --users-file users.txt
```

The scanner will process each username sequentially.

---

# 🖼️ Show Avatar URL

To display the public avatar URL in the terminal:

```bash
python mr_z3ro.py --user example --show-avatar
```

---

# 💾 Custom Database

By default, results are stored in:

```bash
mr_z3ro_tiktok.db
```

Use a custom SQLite database:

```bash
python mr_z3ro.py --user example --db research.db
```

---

# 🌐 Proxy Configuration

A proxy list can be supplied as a comma-separated argument:

```bash
python mr_z3ro.py --user example --proxies http://127.0.0.1:8080
```

Multiple proxies:

```bash
python mr_z3ro.py --user example --proxies http://127.0.0.1:8080,http://127.0.0.1:8081
```

> Use proxies only where you have permission and ensure their use complies with applicable laws and the platform's terms.

---

# 🧹 Clear Terminal

Clear the terminal before starting:

```bash
python mr_z3ro.py --user example --clear
```

---

# 💖 Support the Project

To display the project support information:

```bash
python mr_z3ro.py --donate
```

---

# ⚙️ Command-Line Options

```bash
--user              Single TikTok username
--users-file        TXT file containing usernames
--videos            Maximum public videos to process
--db                SQLite database path
--proxies           Comma-separated proxy list
--show-avatar       Display public avatar URL
--donate            Display project support information
--clear              Clear terminal before execution
-h, --help           Display help information
```

---

# 🔍 Information Collected

## 👤 Profile Information

The scanner can process publicly available profile information such as:

```bash
Username
Nickname
User ID
Profile URL
Bio
Bio Links
Avatar URL
Followers
Following
Likes
Video Count
Verification Status
Private/Public Status
Region
Language
Website
```

---

## 📧 Public Contact Information

The scanner can detect contact information that a user has **voluntarily published in accessible profile text**.

Supported patterns include:

```bash
Email addresses
Phone-number-like strings
```

> The tool does not provide access to private account information. Detection is based on information available in the content being processed.

---

# 📍 Location Information

The scanner can report location information when it is publicly available through supported video metadata.

Possible fields include:

```bash
City
Country
Latitude
Longitude
```

> Location information can be sensitive. Use this functionality only for legitimate and authorized OSINT purposes.

---

# 🎬 Video Intelligence

For publicly accessible video metadata, the scanner can process:

```bash
Video ID
Author
Description
Creation Time
Duration
Views
Likes
Shares
Comments
Music
Video URLs
Cover URLs
Hashtags
Mentions
```

Additional metadata fields are stored when available.

---

# #️⃣ Hashtag & Mention Extraction

From public video descriptions, the scanner extracts:

```bash
#hashtags
@mentions
```

Example:

```text
#technology #gaming #python
@creator
```

---

# 💾 SQLite Database

The project automatically creates a local SQLite database.

Default:

```bash
mr_z3ro_tiktok.db
```

The database contains separate structures for:

```bash
users
videos
```

This allows previously collected research data to be retained locally for analysis.

---

# 📊 Reporting System

Every scan creates a dedicated `reports` directory.

```bash
reports/
├── report_user_20260828_194200_xxxxxx.json
└── report_user_20260828_194200_xxxxxx.txt
```

Filenames contain:

```bash
Report Type
Timestamp
Random Identifier
```

---

# 📄 JSON Report

JSON reports contain structured information including:

```bash
Summary
Target
Status
Profile Information
Video Information
Metadata
Timestamp
```

Example structure:

```json
{
    "summary": {
        "total": 1,
        "hits": 1,
        "misses": 0,
        "errors": 0
    },
    "results": [],
    "metadata": {
        "platform": "Linux",
        "timestamp": "2026-08-28T00:00:00+00:00",
        "version": "MR Z3R0 v2.1"
    }
}
```

---

# 📃 TXT Report

A human-readable TXT report is also generated:

```text
MR Z3R0 OSINT Report
============================================================

Platform: Linux
Generated: ...

Total   : 1
Hits    : 1
Misses  : 0
Errors  : 0

🎯 Target : @example
📌 Status : HIT
   Name        : Example
   Followers   : 10,000
   Following   : 500
   Likes       : 100,000
   Videos      : 50
   Verified    : False
   Private     : False
```

---

# 🗂️ Project Structure

```bash
MR-Z3R0-TikTok-OSINT/
│
├── mr_z3ro.py
├── README.md
├── requirements.txt
├── mr_z3ro_tiktok.db
│
└── reports/
    ├── report_user_*.json
    └── report_user_*.txt
```

---

# 📋 requirements.txt

You can create a `requirements.txt` file containing:

```bash
requests
colorama
python-dotenv
```

Install manually with:

```bash
pip install -r requirements.txt
```

---

# 🧪 Example Workflow

```bash
# 1. Install Python
pkg install python

# 2. Run a single-user scan
python mr_z3ro.py --user example

# 3. Fetch public videos
python mr_z3ro.py --user example --videos 20

# 4. Save to a custom database
python mr_z3ro.py --user example --db research.db

# 5. Process multiple usernames
python mr_z3ro.py --users-file users.txt
```

---

# 🖥️ Cross-Platform Support

### 📱 Termux

```bash
Android + Termux
```

### 🐧 Linux

```bash
Linux + Python 3
```

### 🪟 Windows

```bash
Windows + Python 3
```

---

# 🔐 Privacy & Responsible OSINT

This project should be used for:

```bash
✓ Authorized Investigations
✓ Security Research
✓ OSINT Education
✓ Public Information Research
✓ Academic Research
✓ Journalism With Appropriate Legal Basis
✓ Your Own Accounts / Data
```

Do not use it to:

```bash
✗ Access private accounts
✗ Bypass authentication
✗ Circumvent platform security
✗ Harass or stalk individuals
✗ Collect sensitive personal information without a legitimate basis
✗ Evade platform restrictions
✗ Perform unauthorized automated activity
```

Always respect:

```bash
Privacy Laws
Platform Terms of Service
Local Regulations
Rate Limits
User Privacy
```

---

# ⚠️ Disclaimer

**MR Z3R0 TikTok OSINT is provided for educational and authorized research purposes.**

The developer does not encourage or support:

- Unauthorized surveillance
- Privacy violations
- Harassment
- Stalking
- Credential theft
- Account compromise
- Circumvention of access controls

You are solely responsible for how you use this software.

---

# 🧑‍💻 Author

```text
MR Z3R0
TikTok OSINT Framework
```

---

# ⭐ Star the Repository

If this project helped you with legitimate OSINT research or security education, consider giving the repository a ⭐.

```text
⭐ Star → Fork → Learn → Research
```

---

# 📜 License

This project is released under the license included in this repository.

Use the software responsibly and only for lawful purposes.

---

## 🔎 MR Z3R0 TikTok OSINT

```text
Public Data
     ↓
TikTok Profile
     ↓
OSINT Collection
     ↓
Local SQLite Database
     ↓
JSON / TXT Reports
     ↓
Research & Analysis
```

### **MR Z3R0 · TikTok OSINT Framework**
### **Research • Reconnaissance • Public Data • Authorized OSINT**
