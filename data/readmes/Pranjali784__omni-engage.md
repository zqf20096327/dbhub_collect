
---

# 🌐 **Omni-Engage — Unified Customer Engagement Platform**

A modern **microservices-based omni-channel engagement system** built with:

<p align="center">
  <img src="https://img.shields.io/badge/Java-17-5382A1.svg?logo=java&logoColor=white">
<img src="https://img.shields.io/badge/Spring_Boot-3.3.x-6DB33F.svg?logo=spring&logoColor=white">
<img src="https://img.shields.io/badge/React-18-087EA4.svg?logo=react&logoColor=white">
<img src="https://img.shields.io/badge/TiDB_Cloud-Distributed_SQL-BF0A30.svg?logo=tidb&logoColor=white">
<img src="https://img.shields.io/badge/Docker-Containerized-2496ED.svg?logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/Maven-Build_Tool-C71A36.svg?logo=apachemaven&logoColor=white">
<img src="https://img.shields.io/badge/Render-Backend_Hosting-46E3B7.svg?logo=render&logoColor=black">
<img src="https://img.shields.io/badge/Vercel-Frontend_Hosting-FF69B4.svg?logo=vercel&logoColor=white">
<img src="https://img.shields.io/badge/Postman-API_Testing-FF6C37.svg?logo=postman&logoColor=white">
<img src="https://img.shields.io/badge/JMeter-Load_Testing-D22128.svg?logo=apachejmeter&logoColor=white">
<img src="https://img.shields.io/badge/UptimeRobot-Monitoring-5CCD18.svg?logo=uptimerobot&logoColor=white">
</p>

**Omni-Engage** provides a unified dashboard where support agents can manage conversations from **Facebook, WhatsApp, Instagram, Email, Chat, and more** — all in one place.

---

**Omni-Engage** is a next-generation **cloud-native omni-channel engagement platform** engineered for organizations that require **high availability**, **scalable microservices**, and **real-time customer interaction management**.

Powered by a modern **microservices architecture**—built on **Spring Boot**, **React**, and **TiDB Distributed SQL**—Omni-Engage consolidates customer conversations across **Facebook, WhatsApp, Instagram, Email, Chat, and Telephony** into one **unified, intelligent dashboard**.

Designed for **mission-critical customer support operations**, Omni-Engage provides:

* ⚡ **Low-latency APIs** optimized for enterprise scale
* 🔄 **High-throughput ingestion pipelines** for multi-channel workloads
* 🧠 **Intelligent routing & agent workload balancing**
* 🔍 **Advanced filtering, auditability, and analytics-ready event streaming**
* ☁️ **Production cloud deployments on Render & Vercel with CI/CD**
* 🌐 **Horizontally scalable distributed SQL backend powered by TiDB Cloud**

Inspired by platforms like **Zendesk**, **Freshdesk**, **Intercom**, and **Salesforce Service Cloud**, Omni-Engage demonstrates how leading enterprises architect **modern omni-channel systems** in 2025 and beyond.

> **Omni-Engage is not just a project — it is a complete enterprise product blueprint built using real-world architectural patterns.**

---

## 📚 **Table of Contents**

* [🧩 Architecture Overview](#-architecture-overview)
* [🚀 Getting Started](#-getting-started)
* [⚙️ Tech Stack](#️-tech-stack)
* [🧠 Core Features](#-core-features)
* [🧪 API Testing](#-api-testing)
* [🚦 Load Testing](#-load-testing)
* [🌐 Monitoring & Uptime](#-monitoring--uptime)
* [📦 Deployment Guide](#-deployment-guide)
* [📈 Future Enhancements](#-future-enhancements)
* [👩‍💼 Author](#-author)

---

# 🧩 **Architecture Overview**

Omni-Engage follows a **scalable microservices architecture** with clear separation of concerns.

### 🏗 **System Components**

| Component              | Responsibility                                              | Technology     | Deployment      |
| ---------------------- | ----------------------------------------------------------- | -------------- | --------------- |
| **Agent Service**      | Agents, conversations, messages, assignment logic           | Spring Boot 3  | Render / Docker |
| **Ingestion Service**  | Receives messages from external channels (FB, IG, WhatsApp) | Spring Boot 3  | Render / Docker |
| **Agent Dashboard**    | Web UI for agents                                           | React 18       | Vercel          |
| **Distributed SQL DB** | Stores conversations, agents, messages                      | **TiDB Cloud** | Serverless      |

### 🖼 Architecture Diagram (Conceptual)

```
   Facebook / IG / WhatsApp / Email
                │
       ┌────────▼─────────┐
       │ Ingestion Service │
       └────────┬─────────┘
                │ REST
       ┌────────▼──────────┐
       │   Agent Service    │─── TiDB Cloud (MySQL-Compatible)
       └────────┬──────────┘
                │ REST APIs
       ┌────────▼─────────┐
       │  React Dashboard  │ (Vercel)
       └───────────────────┘
```

---

# 🚀 **Getting Started**

### ✅ **Prerequisites**

* Java 17
* Spring Boot 3.x
* MySQL 8+ / TiDB Cloud
* Maven 3.9+
* Docker Desktop (recommended)

---

## 🐳 **Run Entire System with Docker (Recommended)**

```bash
git clone https://github.com/Pranjali784/omni-engage.git
cd omni-engage

cp .env.example .env

docker compose up -d --build
```

### Access Services

| Service                    | URL                                                                            |
| -------------------------- | ------------------------------------------------------------------------------ |
| **Dashboard (Frontend)**   | [http://localhost:3000](http://localhost:3000)                                 |
| **Agent API**              | [http://localhost:8081](http://localhost:8081)                                 |
| **Ingestion API**          | [http://localhost:8080](http://localhost:8080)                                 |
| **Agent Health Check**     | [http://localhost:8081/actuator/health](http://localhost:8081/actuator/health) |
| **Ingestion Health Check** | [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health) |

---

# ⚙️ **Tech Stack**

### **Backend**

* Java 17
* Spring Boot 3.3
* JPA/Hibernate
* REST APIs
* MySQL / TiDB Cloud
* Docker

### **Frontend**

* React 18
* Axios
* Bootstrap / Custom CSS

### **DevOps**

* Docker Compose
* Render
* Vercel
* UptimeRobot (Monitoring)

---

# 🧠 **Core Features**

### 🎧 Agent Management

* Availability tracking
* Auto-assignment with locking
* Prevents race conditions

### 💬 Conversation Management

* Create / Close / Reopen
* Timestamped messages
* Channel-specific sorting

### 🌐 Omni-channel Support

* WhatsApp
* Facebook
* Instagram
* Email
* In-App Chat

### 🔍 Filtering

* Channel
* Agent
* Status

### ♻ Real-Time Updates

* Polling
* Auto-refresh

### 📊 Production-Ready

* Actuator health checks
* Configurable environments
* Containerized microservices

---

# 🧪 **API Testing**

All REST endpoints were validated using **Postman**.

**Tested areas include:**

* Agent lifecycle & availability
* Conversation creation, assignment & closure
* Message ingestion across channels
* Error handling & actuator endpoints

This ensures correctness, stability, and predictable API behavior.

---

# 🚦 **Load Testing**

**Apache JMeter** was used to stress-test both microservices under concurrent load.

**Key scenarios tested:**

* Rapid message ingestion
* Parallel conversation creation
* High agent concurrency
* TiDB Cloud under heavy read/write volume

The platform maintained **low latency** and **stable throughput** during load testing.

---

# 🌐 **Monitoring & Uptime**

To prevent Render’s free-tier servers from sleeping, **UptimeRobot** continuously pings:

```
/actuator/health
```

For both:

* Agent Service
* Ingestion Service

**Ping interval:** every 1 minute

This ensures:

* No cold starts
* Consistent response times
* Reliable user experience

---

# 📦 **Deployment Guide**

### ✔ Frontend → Deploy on Vercel

Set environment variables:

```
REACT_APP_AGENT_API=https://your-agent-service.onrender.com
REACT_APP_INGESTION_API=https://your-ingestion-service.onrender.com
```

### ✔ Backend → Deploy on Render

Set:

```
SPRING_DATASOURCE_URL=
SPRING_DATASOURCE_USERNAME=
SPRING_DATASOURCE_PASSWORD=
```

### ✔ Database → TiDB Cloud

* MySQL-compatible
* Scalable
* Serverless

---

# 📈 **Future Enhancements (2025 Roadmap)**

* WebSockets / SSE
* Deployment on AWS ECS/EKS / Kubernetes
* Redis caching
* AI Agent Assistant
* ClickHouse analytics
* SLA workflows
* LLM conversation summarization

---

# 👩‍💼 **Author**

**Pranjali Srivastava**
*Java Developer | Backend Engineer | Microservices | SQL & Cloud*
📍 Chennai, India

<p align="center">
  <a href="https://www.linkedin.com/in/pranjali784/">
    <img src="https://img.shields.io/badge/LinkedIn-Pranjali%20Srivastava-0077B5?style=for-the-badge&logo=linkedin">
  </a>
</p>

---

> 🚀 *Omni-Engage represents a fully modern, scalable, production-grade microservices system built using today’s best practices.*

---



