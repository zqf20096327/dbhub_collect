# Production-Grade Django Starter Kit

A batteries-included, modular boilerplate and development environment for **Django 4.2+** and **Django REST Framework (DRF)**. Pre-configured with **Docker Compose**, **PostgreSQL**, **Elasticsearch**, **Celery** (asynchronous workers + scheduler), and **Swagger / OpenAPI** interactive documentation.

[![Release](https://img.shields.io/github/v/release/codewithmuh/django-starter-kit?style=flat-square&color=blue)](https://github.com/codewithmuh/django-starter-kit/releases)
[![Stars](https://img.shields.io/github/stars/codewithmuh/django-starter-kit?style=flat-square&color=gold)](https://github.com/codewithmuh/django-starter-kit/stargazers)
[![Forks](https://img.shields.io/github/forks/codewithmuh/django-starter-kit?style=flat-square&color=blueviolet)](https://github.com/codewithmuh/django-starter-kit/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Celery](https://img.shields.io/badge/Celery-Async%20Tasks-37814A.svg?style=flat-square&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-005571.svg?style=flat-square&logo=elasticsearch&logoColor=white)](https://elastic.co)
[![YouTube](https://img.shields.io/badge/YouTube-codewithmuh-red?style=flat-square&logo=youtube)](https://youtube.com/@codewithmuh)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad%20Rashid-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/muhammadrashid-daha/)

![aws cost (7)](https://github.com/codewithmuh/django-starter-kit/assets/51082957/71b37d29-ec83-4063-bbcd-7afe11bebc0a)

---

## 📑 Table of Contents
- [Architecture Overview](#architecture-overview)
- [Key Features](#features)
- [Project Directory Layout](#project-directory-layout)
- [One-Command Quickstart](#one-command-quickstart)
- [Environment Configuration](#environment-configuration)
- [Services & Ports Reference](#services--ports-reference)
- [Common Development Commands](#common-development-commands)
- [Author & Community](#author)
- [License](#license)

---

## 🏛️ Architecture Overview

```mermaid
flowchart TD
    Client([Client / Frontend / Browser]) -->|HTTP :8000| Django[Django REST API Core]
    Django -->|Docs / API Schema| Swagger[Swagger / OpenAPI UI]
    Django -->|Relational Data| Postgres[(PostgreSQL Database)]
    Django -->|Full-Text Search| ES[(Elasticsearch Engine)]
    Django -->|Dispatch Async Job| Broker[(Redis / RabbitMQ Broker)]
    Broker --> Worker[Celery Worker]
    Beat[Celery Beat Scheduler] --> Broker
    Worker --> Postgres
```

---

## 🌟 Features

- 🐳 **One-Command Docker Setup:** No need to install and configure Python, PostgreSQL, Redis, or Elasticsearch manually.
- ⚡ **Asynchronous Task Processing:** Pre-wired **Celery** workers and **Celery Beat** periodic task scheduler.
- 🔍 **Full-Text Search Engine:** Integrated **Elasticsearch** service ready for search indexing and fast queries.
- 📖 **Self-Documenting REST APIs:** Interactive **Swagger / OpenAPI** documentation at `/api/docs/`.
- 🗄️ **Production PostgreSQL:** Resilient relational database layer pre-configured with volume persistence.
- 🛡️ **Secure Secret Management:** Clean environment segregation using `.env` templates.

---

## 📂 Project Directory Layout

```
django-starter-kit/
├── backend/                       # Django project source code
│   ├── apps/                      # Modular Django apps
│   ├── config/                    # Core settings (base, dev, prod), WSGI, ASGI
│   └── manage.py                  # Management script
├── build-process/                 # Docker orchestration assets
│   ├── docker-compose-django-backend.yml
│   ├── Dockerfile
│   └── local.backend.env          # Development environment variables
├── requirements/                  # Split Python dependencies
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
└── README.md
```

---

## 🚀 One-Command Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/codewithmuh/django-starter-kit.git
cd django-starter-kit
```

### 2. Configure environment variables
Verify or modify the environment values in `build-process/local.backend.env`.

### 3. Spin up all services
```bash
docker compose -f "./build-process/docker-compose-django-backend.yml" up -d --build
```

### 4. Create an admin user
```bash
docker compose -f "./build-process/docker-compose-django-backend.yml" exec web python manage.py createsuperuser
```

---

## 🔌 Services & Ports Reference

Once running, access the local services via these ports:

| Service | Port | Description |
| :--- | :--- | :--- |
| **Django Backend API** | `http://localhost:8000/` | Main application server |
| **Swagger / OpenAPI Docs** | `http://localhost:8000/api/docs/` | Interactive API sandbox & schema |
| **Django Admin** | `http://localhost:8000/admin/` | Management and database administration |
| **PostgreSQL** | `localhost:5432` | Relational database connection |
| **Elasticsearch** | `localhost:9200` | Search engine HTTP REST interface |

---

## 🛠️ Common Development Commands

```bash
# View real-time container logs
docker compose -f "./build-process/docker-compose-django-backend.yml" logs -f web

# Run database migrations inside container
docker compose -f "./build-process/docker-compose-django-backend.yml" exec web python manage.py migrate

# Stop all background services
docker compose -f "./build-process/docker-compose-django-backend.yml" down
```

---

## 👨‍💻 Author

**Muhammad Rashid** — Backend & Cloud DevOps Engineer, AWS Community Builder.  
- 🎥 **YouTube:** [@codewithmuh](https://youtube.com/@codewithmuh)  
- 💼 **LinkedIn:** [Muhammad Rashid](https://www.linkedin.com/in/muhammadrashid-daha/)  
- 🌐 **Website:** [codewithmuh.com](https://codewithmuh.com) · [devopsbymuh.com](https://devopsbymuh.com)

⭐ **If you find this Starter Kit helpful, please star the repository!**

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
