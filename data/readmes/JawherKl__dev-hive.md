# DevHive: NestJS API with PostgreSQL & Prisma

<!--
![Repository Size](https://img.shields.io/github/repo-size/JawherKl/dev-hive)
![Last Commit](https://img.shields.io/github/last-commit/JawherKl/dev-hive)
![Issues](https://img.shields.io/github/issues-raw/JawherKl/dev-hive)
![Forks](https://img.shields.io/github/forks/JawherKl/dev-hive)
![Stars](https://img.shields.io/github/stars/JawherKl/dev-hive)
-->

<img src="images/nestjs.png" alt="nestapi" width="420"/>

A robust developer platform for managing internal resources, secrets, and API keys with enterprise-grade authentication.

> Built with modern technologies:  
> NestJS + Fastify • PostgreSQL + Prisma • Keycloak • OpenAPI/Swagger

![NestJS.js](https://img.shields.io/badge/nestjs-E0234E?style=for-the-badge&logo=nestjs&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Fastify](https://img.shields.io/badge/Fastify-000000?style=for-the-badge&logo=fastify&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-3982CE?style=for-the-badge&logo=Prisma&logoColor=white)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)

## ✨ Features

### 🔒 Authentication & Authorization
- [x] Keycloak integration for secure authentication
- [x] JWT-based authorization with role management
- [x] User registration with first/last name validation
- [x] Protected routes with role-based access control
- [x] Token refresh and logout functionality

### 📊 Project Management
- [x] CRUD operations for projects
- [x] Project ownership validation
- [x] Soft delete with restore capability
- [x] Pagination & filtering support
- [x] Search functionality

### 🔑 Resource Management
- [x] Secure storage of API keys and secrets
- [x] Resource types validation (API_KEY, SECRET, URL)
- [x] Project-based resource organization
- [x] Pagination & search capabilities
- [x] Archive/restore functionality

### 📚 API Documentation
- [x] OpenAPI/Swagger integration
- [x] Detailed endpoint documentation
- [x] Request/response schemas
- [x] Authentication flows documented
- [x] API versioning support

### 🧪 Testing & Quality
- [x] Unit tests with Jest
- [x] E2E tests with Supertest
- [x] Test environment configuration
- [x] CI/CD ready test suites
- [x] Code coverage reporting

### 📂 File Management
- [x] Secure file uploads with MinIO
- [x] User-specific folder organization
- [x] Access control based on ownership
- [x] Pre-signed URLs for secure downloads
- [x] Asynchronous file processing
- [x] File metadata management

### 🚀 Queue System
- [x] Redis-based queue management
- [x] Background job processing
- [x] File processing queue
- [x] Job status monitoring
- [x] Error handling and retries


## 🛠️ Tech Stack

| Category        | Technology                |
|----------------|---------------------------|
| Framework      | NestJS + Fastify         |
| Database       | PostgreSQL + Prisma       |
| Authentication | Keycloak                  |
| Documentation  | OpenAPI/Swagger          |
| Testing        | Jest + Supertest         |

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/JawherKl/dev-hive.git
cd dev-hive
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Update the .env file with your configurations
```

4. Start the services:
```bash
docker-compose up -d   # Start Keycloak and PostgreSQL
npm run start:dev     # Start the NestJS application
```

## 🧪 Running Tests

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Test coverage
npm run test:cov
```

## 📝 API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:3000/api/docs
- API Base URL: http://localhost:3000/api

## 🗺️ Roadmap

### 🔹 Phase 2 – Enhanced Features
- [ ] Rate limiting and throttling
- [x] Advanced audit logging
- [ ] Automated backup system
- [x] Multi-tenant support
- [x] API key rotation

### 🔹 Phase 3 – Integration & Storage
- [x] MinIO integration for file storage
- [x] Redis caching layer
- [x] Background job processing
- [ ] Email notifications
- [ ] Analytics and reporting

### 🔹 Phase 4 – Frontend & Monitoring
- [ ] Angular admin dashboard
- [ ] Real-time updates
- [x] Monitoring and alerting
- [x] Performance optimization
- [ ] Mobile responsiveness

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jawher Kallel**
- Github: [@JawherKl](https://github.com/JawherKl)

## 🙏 Acknowledgments
- Special thanks to all contributors and the open-source community.
- Gratitude to the maintainers of the libraries used in this project.

---
Made with ❤️ by [Jawher Kallel](https://github.com/JawherKl)
