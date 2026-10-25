<p align="center">
  <img src="https://img.shields.io/badge/Angular_17-DD0031?style=for-the-badge&logo=angular&logoColor=white" alt="Angular" />
  <img src="https://img.shields.io/badge/Spring_Boot_4-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot" />
  <img src="https://img.shields.io/badge/Java_17-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java 17" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/PostgreSQL-Current_DB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/TiDB_Cloud-Planned_DB-E30C34?style=for-the-badge&logo=mysql&logoColor=white" alt="TiDB Cloud" />
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/Platform-Web%20App-004D40?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/License-All%20Rights%20Reserved-E11D48?style=for-the-badge&logo=security&logoColor=white" alt="License" />
</p>

# 🧩 DilzJackets

> **High-Performance Full-Stack Motorcycle Gear & Heavy-Duty Rainwear Showroom Platform**

DilzJackets is a **production-grade web application** designed to **streamline motorcycle riding gear discovery, rainwear sizing inspection, and real-time inventory management**.

The system focuses on **reactive state architecture, localized buyer journeys, and stateless administrative security** and aims to **bridge online catalog browsing with physical showroom test-fitting for riders across Sri Lanka**.

---

## 🌐 Live Deployments

- 🖥️ **Frontend Web Application (Vercel)**: [https://dilzjackets.vercel.app](https://dilzjackets.vercel.app) *(Mirror: [maspothajackets.vercel.app]
- ⚙️ **Backend RESTful API (Render)**: [https://dilzjackets-backend.onrender.com/](https://dilzjackets-backend.onrender.com/) 

---

# ✨ Key Features

| Feature | Description |
|---|---|
| **Bilingual Localization (EN & SI)** | Instant, zero-latency switching between English and Sinhala with persistent preference storage in `localStorage`. |
| **Dynamic Signals-Based Catalog** | Multi-attribute filtering (Category Tabs, Material Dropdown, Sizes) powered by fine-grained Angular Signals and derived state. |
| **1-Click Showroom Hold Engine** | Zero-deposit gear reservation sending pre-filled order specifications directly via WhatsApp or EmailJS. |
| **Stateless JWT Security Filter** | HMAC SHA-256 token verification, BCrypt password hashing, and synchronized 15-minute client session countdown. |
| **Live Inventory Dashboard** | Fast admin management table with one-tap stock toggle switches, real-time pricing, and size tag audits. |
| **Direct Cloudinary Media Uploads** | Unsigned client-side image streaming directly to Cloudinary CDN, bypassing server memory bottlenecks. |
| **Local Business Rich SEO Schema** | Embedded Schema.org `ClothingStore` JSON-LD with GPS geo-coordinates, opening hours, and provincial search tags. |
| **Hybrid Persistence Roadmap** | Operates on managed cloud PostgreSQL with a defined transition path to horizontally-scalable TiDB Cloud Serverless. |

---

# 🎬 Project Demonstration

The following resources demonstrate the system's behavior:

- [📹 Product Walkthrough Video](#-product-video)
- [📸 Screenshots of Key Features](#-screenshots)
- [⚙️ Architecture Overview](#️-architecture-overview)
- [🧠 Engineering Lessons](#-engineering-lessons)
- [🔧 Key Design Decisions](#-key-design-decisions)
- [🗺️ Roadmap](#️-roadmap)
- [🚀 Future Improvements](#-future-improvements)
- [📄 Documentation](#-documentations)
- [📝 License](#-license)
- [📩 Contact](#-contact)

If deeper technical access is required, it can be provided upon request.

---

# 📹 Product Video

> **[DEMONSTRATION PENDING]**

*A comprehensive video or GIF of the system's walkthrough demonstrating the Architecture, engines, and core workflows is available soon!*

---

# 📸 Screenshots

### 👤 User Role — Customer & Rider View

#### 1. Landing Hero & Showroom Header
*High-impact hero section featuring neon branding, bilingual language toggle, emergency contact callout, and one-tap catalog navigation.*
![](docs/screenshots/01_user_landing_hero_showroom.png)

#### 2. Dynamic Product Catalog & Category Filters
*Real-time filtered product cards featuring category tabs (Jackets, Raincoats), material selectors, stock indicators, and LKR pricing.*
![](docs/screenshots/02_user_product_catalog_filter.png)

#### 3. Why Choose DilzJackets Engineering Features
*Value proposition cards detailing 600D Cordura abrasion resistance, heat-welded seam waterproofing, and in-person showroom fit guarantees.*
![](docs/screenshots/03_user_why_choose_dilz_features.png)

#### 4. Zero-Advance Showroom Hold & Email Reservation Modal
*Interactive hold modal enabling riders to reserve their exact jacket size with preferred visit date prior to traveling to the workshop.*
![](docs/screenshots/04_user_showroom_hold_reservation_modal.png)

#### 5. Official Showroom Location & Operating Hours
*Physical workshop details in Rathkarawwa, Maspotha, Kurunegala, featuring interactive Google Maps, direct phone access, and WhatsApp route guidance.*
![](docs/screenshots/05_user_showroom_location_and_hours.png)

#### 6. Rider Feedback & FAQ Accordion
*Sri Lankan road-tested customer testimonials and expandable accordion addressing waterproof guarantees, size availability, and courier delivery.*
![](docs/screenshots/06_user_biker_reviews_and_faq.png)

---

### 🛡️ Admin Role — Staff & Store Manager View

#### 1. Secure Staff Authentication Portal
*High-security admin login portal featuring password masking, BCrypt hash verification, and 15-minute token issuance.*
![](docs/screenshots/01_admin_login_portal.png)

#### 2. Inventory Management Dashboard
*Staff control dashboard with live session countdown, instant stock toggle switches, real-time pricing audits, and item editing.*
![](docs/screenshots/02_admin_inventory_dashboard.png)

#### 3. Product Management & Cloudinary Upload Modal
*Product creation and modification modal with Cloudinary CDN unsigned image upload, material attributes, and multi-size checkbox selectors.*
![](docs/screenshots/03_admin_product_management_modal.png)

---

# ⚙️ Architecture Overview

DilzJackets is implemented using a **Decoupled Multi-Tier System Architecture** with clean layer segregation across frontend and backend:

```
[ Angular 17 Standalone Client ] <--- HTTPS / JSON ---> [ Spring Boot 4 REST Backend ] <--- JDBC ---> [ PostgreSQL / TiDB Cloud ]
```

### Frontend Architecture (`DilzJackets-Frontend-Angular`)
- **Framework**: Angular 17 (Standalone Components, Signals, Computed properties)
- **Styling**: TailwindCSS 3.4 + Custom SCSS Neon Design Tokens
- **State Management**: Angular Signals with persistent `localStorage` synchronization
- **Folder Structure**: Feature-based separation (`components/`, `core/guards/`, `core/interceptors/`, `core/services/`, `assets/`, `environments/`)

### Backend Architecture (`DilzJackets-Backend-SpringBoot`)
- **Core Engine**: Spring Boot 4.x / Java 17 LTS
- **Security**: Spring Security 6 with stateless `JwtFilter` and HMAC SHA-256 token validation
- **Persistence**: Spring Data JPA with Hibernate ORM
- **Folder Structure**: Layered Domain Architecture (`controller/`, `service/`, `repository/`, `model/`, `security/`, `config/`)

### Database Persistence Strategy
- **Current Operational DB (Temporary)**: Managed Cloud PostgreSQL via HikariCP session pooler (`max-lifetime=600000`, pool size 5) on AWS `ap-southeast-1`.
- **Planned Target Database**: Transitioning to **TiDB Cloud Serverless** (Distributed MySQL-compatible HTAP engine on AWS `ap-southeast-1`: port 4000) for horizontal auto-scaling and high-concurrency showroom traffic.

### Communication & Assets
- **Client-Server Communication**: RESTful JSON API with global CORS allowlisting and pre-flight caching.
- **Media Pipeline**: Client-side direct unsigned streaming to Cloudinary Media CDN.

> 📄 *For the full architectural breakdown, diagrams, and folder hierarchy, see the [Detailed System Architecture Document](docs/system-architecture.md).*

---

# 🧠 Engineering Lessons

During development of DilzJackets the focus areas included:

- **Stateless Session Synchronization**: Coupling backend JWT validation with an active client-side 15-minute timer ensures smooth token revocation without jarring unexpected disconnections.
- **Cloud Pooler Lifecycle Tuning**: Mitigating cloud serverless database socket terminations by aligning HikariCP `max-lifetime` and `keepalive-time` below cloud gateway idle thresholds.
- **Decoupled CDN Media Pipeline**: Eliminating multipart upload bottlenecking on the application server by streaming high-resolution images directly from the browser to Cloudinary.
- **Signals vs. Subscription Management**: Leveraging Angular 17 Signals to achieve fine-grained, leak-proof DOM updates for multi-criteria catalog filtering.
- **Cultural Commerce Alignment**: Replacing traditional e-commerce cart funnels with WhatsApp and Email hold mechanisms tailored to local motorcycle apparel inspection habits.

> 📄 *For detailed case studies and technical implementations, see the [Comprehensive Engineering Lessons Document](docs/engineering-lessons.md).*

---

# 🔧 Key Design Decisions

1. **Angular 17 Standalone Architecture**  
   Selected for enterprise dependency injection, strict TypeScript typing, and clean component isolation without `NgModule` bloat.

2. **Spring Boot 4.x & Java 17 Backend**  
   Chosen for industrial-strength Spring Security 6 filter chains, mature transaction boundaries, and multi-stage container portability.

3. **High-Contrast Dark Neon Biker Aesthetic**  
   Engineered with deep carbon tones and `#ff4500` safety neon highlights to match motorcycle culture and provide superior daylight readability.

4. **Bilingual Localization (English & Sinhala)**  
   Implemented zero-latency client-side dictionary toggling to serve both international tour riders and local Kurunegala commuters.

5. **Operational Cloud PostgreSQL to TiDB Cloud Strategy**  
   Employed Cloud PostgreSQL for rapid initial development and ACID reliability, with a planned upgrade to distributed TiDB Cloud Serverless for elastic multi-region scale.

> 📄 *For full trade-off evaluations and architectural alternatives, see the [Extended Design Decisions Document](docs/design-decisions.md).*

---

# 🗺️ Roadmap

Key upcoming features planned for DilzJackets:

- [Done] **Bilingual Public Showroom** — Dual-language (EN/SI) catalog with dynamic category tabs and material filtering.
- [Done] **Showroom Hold & WhatsApp Connect** — Direct pre-filled WhatsApp link generation and EmailJS reservation modal.
- [Done] **Stateless JWT Administrative Portal** — Role-protected inventory dashboard with live stock toggles and session countdown.
- [Done] **Cloudinary CDN Media Uploads** — Direct browser-to-cloud asset storage for staff catalog management.
- [In Progress] **TiDB Cloud Database Migration** — Provisioning distributed MySQL-compatible cluster on AWS `ap-southeast-1` to replace temporary PostgreSQL instance.
- [In Progress] **PWA Offline Mode & Caching** — Progressive Web App service worker caching for offline showroom browsing along highway routes.
- [Not Started] **Automated SMS Stock Alerts** — Automated SMS notifications to reserved customers when their requested jacket size arrives at the workshop.
- [Not Started] **Multi-Branch Inventory Synchronization** — Multi-tenant support across planned retail locations in Colombo and Kandy.

---

# 🚀 Future Improvements

Planned technical enhancements include:

- **Distributed Query Optimization**: Harnessing TiDB Cloud's HTAP capabilities for real-time inventory velocity analytics.
- **Automated Visual Regression Testing**: CI/CD-integrated headless browser screenshot pipelines using GitHub Actions.
- **Granular Role-Based Access Control (RBAC)**: Distinct permissions for Store Staff, Inventory Managers, and Master Administrators.
- **3D Interactive Gear Inspector**: WebGL/Three.js-powered 360-degree jacket inspection with armor placement overlays.
- **Automated Courier API Integration**: Live shipping fee calculator for nationwide Sri Lanka domestic couriers (Pronto, Domex, PromptX).

---

## 📄 Documentations

Additional documentation is available in the `docs/` folder:

| File | Description |
|---|---|
| [System & Folder Architecture](docs/system-architecture.md) | Exhaustive breakdown of client/server layers, folder trees, data pipelines, and security topologies. |
| [Engineering Lessons & Takeaways](docs/engineering-lessons.md) | Technical deep-dive into JWT session handling, HikariCP cloud tuning, and Signals reactive state. |
| [Key Design Decisions & Trade-offs](docs/design-decisions.md) | Architectural rationale behind Angular 17, Spring Boot, visual design tokens, and database strategy. |

---

# 📝 License

This repository is published for **portfolio and educational review purposes**.

The source code may not be accessed, copied, modified, distributed, or used without explicit permission from the author.

© 2026 Viraj Tharindu — All Rights Reserved.

See the full [LICENSE](LICENSE) file for terms and conditions.

---

## 🔐 Source Code Access

This repository is intentionally private as it contains experimental architecture and unpublished product ideas.

A read-only technical walkthrough can be shared with recruiters upon request.

---

# 📩 Contact

If you are reviewing this project as part of a hiring process or are interested in the technical approach behind it, feel free to reach out.

I would be happy to discuss the architecture, design decisions, or provide a private walkthrough of the project.

**Opportunities for collaboration or professional roles are always welcome.**

📧 Email: [virajtharindu1997@gmail.com](mailto:virajtharindu1997@gmail.com)  
💼 LinkedIn: [https://www.linkedin.com/in/viraj-tharindu/](https://www.linkedin.com/in/viraj-tharindu/)  
🌐 Portfolio: [https://viraj-tharindu-portfolio-web-site.vercel.app/](https://viraj-tharindu-portfolio-web-site.vercel.app/)  
🐙 GitHub: [https://github.com/VirajTharindu](https://github.com/VirajTharindu)  

---

<p align="center">
  <em>🏍️ Built for the Highway & Monsoon — Precision Engineered Full-Stack Motorcycle Apparel Platform 🌧️</em>
</p>
