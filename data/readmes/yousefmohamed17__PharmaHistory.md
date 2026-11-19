# 💊 PharmaHistory — صيدليتك
### AI-Powered Pharmacy Management, POS & Drug Interaction Checker

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_App-0ea5e9?style=for-the-badge&logo=vercel)](https://pharma-frontend-omega.vercel.app)
[![Backend API](https://img.shields.io/badge/Laravel_API-Live-10b981?style=for-the-badge&logo=laravel)](https://pharma-history.vercel.app/api/drug-classes)
[![AI Microservice](https://img.shields.io/badge/Python_AI_Service-Running-6366f1?style=for-the-badge&logo=python)](https://yousef17.pythonanywhere.com)

**PharmaHistory** is a full-stack intelligent pharmacy management system designed to eliminate medication dispensing errors. By linking each patient's **14-digit National ID** to their longitudinal medication history and known allergies, the system leverages a **Python NLP & Machine Learning microservice** to detect drug-drug interactions, active ingredient duplications, and allergy conflicts in real time—automatically recommending safe therapeutic alternatives from a catalog of **25,000+ Egyptian medications**.

---

## ✨ Key Features

- **🧠 Real-Time AI Prescription Check:**
  - Active ingredient normalization (strips pharmaceutical salts like *HCl, Sodium, Potassium, Trihydrate* and maps synonyms like *Acetaminophen → Paracetamol*).
  - Detects **Allergy Conflicts**, **Drug-Drug Interactions**, **Active Ingredient Duplication** (across past history and current cart items), and **Previous Side-Effect Risks**.
  - **Content-Based Recommendation Engine:** Uses **TF-IDF Vectorization** & **Cosine Similarity** (`scikit-learn`) to suggest safe, conflict-free alternatives within the same therapeutic class.
- **🪪 National ID Patient EHR:** Instant lookup and registration via 14-digit National ID, tracking chronic medications, documented allergies, and reported side effects.
- **🛒 Smart Point of Sale (POS) & Electronic Invoicing:** Real-time stock validation, automated inventory deduction, discount calculation, and printable electronic receipts.
- **📦 Full Inventory & Catalog Management:** Search, filter by therapeutic class, monitor low-stock alerts, and manage pricing across 25,070+ drugs.

---

## 🏗️ System Architecture & Tech Stack

| Layer | Technologies | Deployment |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS, Lucide Icons | Vercel |
| **Backend API** | PHP 8, Laravel, RESTful API | Vercel Serverless |
| **AI Microservice** | Python, Flask/FastAPI, Scikit-learn (TF-IDF & Cosine Similarity), Pandas | PythonAnywhere |
| **Database** | MySQL-compatible Distributed Cloud Database | TiDB Cloud |

---

## 🧪 Quick Demo Credentials & Test Scenarios

- **Live URL:** [https://pharma-frontend-omega.vercel.app](https://pharma-frontend-omega.vercel.app)
- **Username:** `yousef`
- **Password:** `12345678`

**Ready-to-Test National IDs (available in the app sidebar):**
- `29901011234567` — Patient with documented allergy & previous side-effect history.
- `29505057654321` — Patient currently on Aspirin (tests NSAID/anticoagulant interaction).
- `29208151122334` — Patient allergic to *Diclofenac*.
- `30103209876543` — Healthy patient profile for clean checkout & invoicing.

---

## 👨‍💻 Author
**Youssef Mohamed** — Full-Stack Web Developer  
- Live App: [pharma-frontend-omega.vercel.app](https://pharma-frontend-omega.vercel.app)
