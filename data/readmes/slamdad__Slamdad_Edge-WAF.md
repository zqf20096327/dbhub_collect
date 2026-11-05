]# 🛡️ Slamdad Edge: Web Application Firewall (WAF)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Microframework-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Security](https://img.shields.io/badge/Security-Threat%20Interception-red.svg)]()

**Slamdad Edge** is a custom-engineered Web Application Firewall (WAF) and reverse proxy. Designed to sit directly in front of vulnerable web applications, it actively intercepts, inspects, and filters incoming HTTP traffic at the network edge to neutralize malicious payloads before they reach the origin server.

---

## ✨ Key Features

* **🚦 Global Threat Interception:** Operates as a true reverse proxy, inspecting all incoming traffic against an SQLite threat intelligence database.
* **🛑 Automatic IP Banning:** Employs a strike-based threshold system. Repeated malicious requests automatically trigger an IP ban and blocklist routing.
* **🕵️ Payload Inspection:** Detects SQL Injection (SQLi), Cross-Site Scripting (XSS), Command Injection, and Path Traversal attempts via exact-string signature matching.
* **📊 Secure Command Center:** A password-protected admin dashboard for real-time traffic logging, threat analysis, and ban management.
* **🔒 Intelligent Data Redaction:** Automatically sanitizes intercepted payloads (parsing `request.form` and `request.get_json()`) to mask passwords and sensitive secrets as `[REDACTED]` before writing to the database.

---

## 🏗️ Architecture & Request Flow

1. **Client Request:** Traffic hits the Slamdad Edge WAF on `port 5002`.
2. **Access Control:** The firewall checks the `bans` table. If the IP is blacklisted, the connection is instantly dropped with a 403 Block Page.
3. **Deep Inspection:** The request path, query string, and body are scanned against known threat signatures.
4. **Verdict & Logging:** 
   * *Malicious:* The request is blocked, a strike is recorded, and the payload is logged.
   * *Clean:* The request is transparently forwarded to the target origin server (`port 5001`).

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.8+
* macOS/Linux/Windows

### 1. Clone & Setup
```bash
git clone [https://github.com/slamdad/Slamdad-Edge-Web-Application-Firewall-WAF-.git](https://github.com/slamdad/Slamdad-Edge-Web-Application-Firewall-WAF-.git)
cd Slamdad-Edge-Web-Application-Firewall-WAF-
pip3 install -r requirements.txt
