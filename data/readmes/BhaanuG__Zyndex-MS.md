<div align="center">

<a href="https://github.com/BhaanuG/Zyndex-MS">
  <img src="https://raw.githubusercontent.com/BhaanuG/Zyndex-MS/main/public/logo.svg" alt="Zyndex Logo" width="100" height="100" />
</a>

# ZYNDEX

### Enterprise Distributed Academic Learning & Digital Resource Management Platform

<p align="center">
  <b>Architected, Engineered & Authored Solely by <a href="mailto:Bhaanugali@gmail.com">Bhaanu G (Bhaanu Gali)</a></b><br/>
  <code>Platform Maintainer & Principal Systems Architect</code><br/>
  <a href="mailto:Bhaanugali@gmail.com">Bhaanugali@gmail.com</a> &bull; <a href="mailto:2400030952@kluniversity.in">2400030952@kluniversity.in</a> &bull; <a href="https://github.com/BhaanuG/Zyndex-MS">GitHub Repository</a>
</p>

---

<p align="center">
  <a href="#core-architectural-highlights"><img src="https://img.shields.io/badge/Architecture-Poly--Service%20Microservices-blueviolet?style=for-the-badge" alt="Architecture" /></a>
  <a href="#backend-runtime-specifications"><img src="https://img.shields.io/badge/Java-21%20LTS-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java 21 LTS" /></a>
  <a href="#backend-runtime-specifications"><img src="https://img.shields.io/badge/Spring%20Boot-3.4.2-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot 3.4.2" /></a>
  <a href="#backend-runtime-specifications"><img src="https://img.shields.io/badge/Spring%20Cloud-2024.0.0-6DB33F?style=for-the-badge&logo=spring&logoColor=white" alt="Spring Cloud" /></a>
  <a href="#frontend-runtime-specifications"><img src="https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React 18" /></a>
  <a href="#frontend-runtime-specifications"><img src="https://img.shields.io/badge/Vite-6.0.5-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite 6" /></a>
  <a href="#database-runtime-specifications"><img src="https://img.shields.io/badge/MySQL-8.4%20LTS-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL 8.4" /></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT%20(Exclusive%20Attribution)-yellow?style=flat-square" alt="License" /></a>
  <a href=".github/SECURITY.md"><img src="https://img.shields.io/badge/Security-Cryptographic%20OTP%20%26%20JWT-2ea44f?style=flat-square" alt="Security" /></a>
  <a href=".github/ACCESSIBILITY.md"><img src="https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA%20%26%20Section%20508-blue?style=flat-square" alt="Accessibility" /></a>
  <img src="https://img.shields.io/badge/Build%20Status-Passing%20(0%20Errors)-brightgreen?style=flat-square" alt="Build Status" />
  <img src="https://img.shields.io/badge/Deployment-Oracle%20Cloud%20Infrastructure%20(OCI)-F80000?style=flat-square&logo=oracle&logoColor=white" alt="Deployment" />
</p>

<p align="center">
  <a href="#system-architecture--microservices-topology"><b>System Topology</b></a> &bull;
  <a href="#core-architectural-highlights"><b>Architectural Highlights</b></a> &bull;
  <a href="#microservice-registry-and-port-allocation"><b>Service Ports</b></a> &bull;
  <a href="#10-comprehensive-rest-api-reference"><b>REST API Documentation</b></a> &bull;
  <a href="#pin-to-pin-local-cluster-execution"><b>Cluster Quickstart</b></a> &bull;
  <a href="#17-quantitative-codebase-statistics--metrics"><b>Quantitative Metrics</b></a>
</p>

</div>

---

### Executive Architectural Abstract

**Zyndex** is a production-grade, distributed academic learning and digital resource management platform designed for universities, campus libraries, research labs, and academic consortia. The platform eliminates content redistribution risks and resolves fragmented student entitlements through:

- **Strict Cryptographic Perimeter**: Dynamic 4-digit TLS-relayed OTP authentication, multi-device session management with real-time active session monitoring, 24-hour trusted device recognition with daily midnight IST reset, single-session token ve

[...截断...]

rsion enforcement (`session_token_version`), and stateless HMAC-SHA256 JWT access tokens.

- **Zero-Leakage In-Memory PDF Slicing**: Proprietary academic documents are sliced on-the-fly in heap memory via Apache PDFBox for unverified and evaluation tiers, preventing client-side retrieval of complete files.

- **Real-Time Telemetry Engine**: Continuous 15-second client heartbeat aggregation that accurately measures active reading duration, total unique readers, and concurrent live sessions.

- **Dedicated UPI Checkout & Instant Reconciliation**: Dedicated multi-segment checkout route (`/Zyndex/User/:name/:email/Profile/Billing/:amount/Payment/:orderId/UTR/*`) featuring real-time analog clock hands with digital countdown (5-minute QR window, 10-minute UTR window), live UPI payment intent generation, bank UTR hold verification, browser-authenticated invoice viewer (`/Zyndex/Invoice/:id`), and administrative reconciliation portal.

---

### Engineering & Systems Matrix

| Architecture Dimension | Technical Implementation | Operational SLA / Characteristic |
| :--- | :--- | :--- |
| **System Model** | Poly-Service Distributed Microservices | Zero shared memory; independent process isolation |
| **Edge Gateway** | Spring Cloud Gateway on Netty (Reactive Non-Blocking I/O) | Sub-50ms reverse-proxy routing; global CORS & rate limiting |
| **Service Registry** | Netflix Eureka Service Discovery | Real-time 30s heartbeat leasing & client-side load balancing |
| **Perimeter Security** | `X-Gateway-Secret` Internal Header Validation | Downstream services block direct external access |
| **Identity & Hashing** | Spring Security 6 + BCrypt (Adaptive Salt Factor 10) | Brute-force resistant credential storage |
| **Persistence Layer** | MySQL 8.4 LTS with InnoDB Engine | ACID transaction boundaries with relational referential integrity |
| **Frontend Framework** | React 18.3.1 SPA via Vite 6 + Tailwind CSS 3.4 | Dynamic code-split bundle; client-side routing fallback |
| **Sole Authority** | **Bhaanu G (Bhaanu Gali)** | All system designs, IP, and platform rights reserved |

---

## System Architecture & Microservices Topology

[![Architecture diagram of bhaanug/zyndex-ms](https://gitdiagram.com/bhaanug/zyndex-ms/diagram.png)](https://gitdiagram.com/bhaanug/zyndex-ms?utm_source=readme&utm_medium=picture)

<br/>

```mermaid
flowchart TD
    subgraph ClientLayer["🖥️ Presentation & Edge Tier"]
        UI["Zyndex Web SPA\n(React 18 + Vite 6 + Tailwind CSS)"]
    end

    subgraph GatewayTier["🛡️ Reverse Proxy & Edge Perimeter"]
        GW["API Gateway (Port 8080)\nSpring Cloud Gateway + Stateless JWT Validation"]
    end

    subgraph DiscoveryTier["🧭 Discovery & Service Mesh"]
        EUREKA["Eureka Service Registry (Port 8761)\nHeartbeat Monitoring & Distributed Registry"]
    end

    subgraph ServiceMesh["⚙️ Autonomous Domain Microservices (Java 21 LTS + Spring Boot 3.4.2)"]
        AUTH["auth-service (8081)\nIdentity, 4-Digit OTP, 24h Trust, BCrypt"]
        CONTENT["content-service (8082)\nCatalog, PDFBox Slicing, Metadata"]
        ACCESS["access-service (8083)\nTier Entitlements, Quotas, Token Issuance"]
        USAGE["usage-service (8084)\nTelemetry Heartbeats, Aggregation Engine"]
        SUB["subscription-service (8085)\nUPI QR Intent, 12-Digit UTR Hold Pipeline"]
    end

    subgraph StorageTier["💾 Persistence & State Store"]
        DB[("MySQL 8.4 Enterprise RDBMS\nACID Distributed Schemas")]
    end

    UI -->|"HTTPS / REST"| GW
    GW -.->|"Service Discovery"| EUREKA
    AUTH -.->|"Self-Registration"| EUREKA
    CONTENT -.->|"Self-Registration"| EUREKA
    ACCESS -.->|"Self-Registration"| EUREKA
    USAGE -.->|"Self-Registration"| EUREKA
    SUB -.->|"Self-Registration"| EUREKA

    GW -->|"X-Gateway-Secret"| AUTH
    GW -->|"X-Gateway-Secret"| CONTENT
    GW -->|"X-Gateway-Secret"| ACCESS
    GW -->|"X-Gateway-Secret"| USAGE
    GW -->|"X-Gateway-Secret"| SUB

    AUTH --> DB
    CONTENT --> DB
    ACCESS --> DB
    USAGE --> DB
