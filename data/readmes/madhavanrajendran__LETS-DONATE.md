# Let'sDonate | Full-Stack Blood Management System

**Let'sDonate** is a robust blood bank management platform designed to bridge the gap between donors and those in need. This project represents a significant evolution from local development to a professional, **cloud-native distributed architecture**.

> **Note on Implementation:** While the frontend UI utilized a professional template, the primary technical focus of this development was architecting the **Backend API, Cloud Database Integration, SSL Security, and End-to-End Deployment.**

---

## 🚀 Technical Focus & Contributions
In this iteration, the project transitioned from a standalone application to a distributed system:

* **Cloud Database Migration:** Successfully migrated data from local MySQL (XAMPP) to **TiDB Cloud (Serverless)** for global accessibility and scalability.
* **Secure Infrastructure:** Implemented **SSL/TLS encryption** for all Node.js-to-Database communication to prevent insecure data transport.
* **Decoupled Deployment:** Orchestrated a multi-platform deployment pipeline using **Render** (API) and **Vercel** (Frontend).
* **Environment Security:** Managed sensitive credentials via environment variables and robust `.gitignore` configurations.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | ReactJS, Tailwind CSS (UI Template) |
| **Backend** | Node.js, Express.js |
| **Database** | TiDB Cloud (MySQL Compatible) |
| **Security** | SSL/TLS Encryption, Dotenv |
| **Hosting** | Render (API), Vercel (Web), GitHub |

---

## 🌟 Key Features

* **Secure Donor Pipeline:** Encrypted data flow from user registration to cloud storage.
* **Blood Request Management:** Real-time processing of donor and requester data.
* **Global Access:** Cloud-hosted database ensures data persists across different development environments.

---

## 📂 System Architecture
The application follows a standard three-tier architecture:
1.  **Client-Side (Vercel):** React application communicating via Axios.
2.  **Server-Side (Render):** Node.js API processing business logic and database queries.
3.  **Data Layer (TiDB Cloud):** Distributed MySQL-compatible database.

---
## 👨‍💻 Developer
    Freelance Web Developer & Computer Science Student
    Focused on Full-Stack Engineering and Secure Cloud Integrations.
## Note on Frontend

Please note: The frontend UI of this project was built using a template to prioritize the development and optimization of the backend logic, database security, and cloud deployment 
strategies.

## 🔧 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/lets-donate.git](https://github.com/your-username/lets-donate.git)

