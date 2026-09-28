# Spring Boot REST API with PostgreSQL

![Build](https://github.com/OKaluzny/spring-boot-rest-api-postgresql/actions/workflows/ci.yml/badge.svg)

Educational project: REST API for managing books built with Spring Boot 4 and PostgreSQL.

## What You Will Learn

- Building REST API with Spring Boot
- Working with databases using Spring Data JPA
- Data validation
- Error handling (RFC 7807 Problem Details)
- Basic Authentication
- Swagger/OpenAPI documentation
- Docker for database
- Writing tests

## Requirements

Before starting, make sure you have installed:

- **Java 17+** — check: `java -version`
- **Maven 3.8+** — check: `mvn -version`
- **Docker** — check: `docker --version`

## Quick Start (5 minutes)

### Step 1: Clone the repository

```bash
git clone https://github.com/OKaluzny/spring-boot-rest-api-postgresql.git
cd spring-boot-rest-api-postgresql
```

### Step 2: Start PostgreSQL

```bash
docker-compose up -d postgres
```

Verify the container is running:
```bash
docker ps
```
You should see container `book-db` with status `Up`.

### Step 3: Run the application

```bash
mvn spring-boot:run
```

Wait for the message:
```
Started Application in X seconds
```

### Step 4: Open Swagger UI

Open in browser: **http://localhost:8080/swagger-ui.html**

Here you can interactively test the API.

### Step 5: Authorization

API requires authentication:
- **Username:** `user`
- **Password:** `user`

In Swagger UI click the **"Authorize"** button and enter these credentials.

## Your First Request with curl

Create a book:

```bash
curl -X POST http://localhost:8080/api/books \
  -H "Content-Type: application/json" \
  -u user:user \
  -d '{"name": "Java Programming", "description": "Learn Java", "tags": ["java"]}'
```

Response:
```json
{
  "id": 1,
  "name": "Java Programming",
  "description": "Learn Java",
  "tags": ["java"]
}
```

Get all books:
```bash
curl http://localhost:8080/api/books -u user:user
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/books` | Create a book |
| `GET` | `/api/books` | Get all books (paginated) |
| `GET` | `/api/books/{id}` | Get book by ID |
| `GET` | `/api/books?name=Java` | Search by name |
| `PUT` | `/api/books/{id}` | Update a book |
| `DELETE` | `/api/books/{id}` | Delete a book |

### Pagination

```
GET /api/books?page=0&size=10&sort=name,asc
```

- `page` — page number (starting from 0)
- `size` — number of items per page
- `sort` — sorting (field,direction)

## Project Structure

```
src/main/java/com/kaluzny/
│
├── Application.java          # Entry point
│
├── config/                   # Configuration
│   ├── SecurityConfig.java   # Security settings
│   └── OpenApiConfig.java    # Swagger settings
│
├── domain/                   # Data layer
│   ├── Book.java             # JPA entity
│   └── BookRepository.java   # Repository
│
├── dto/                      # Data Transfer Objects
│   ├── BookCreateRequest.java
│   ├── BookUpdateRequest.java
│   ├── BookResponse.java
│   └── BookMapper.java
│
├── service/                  # Business logic
│   └── BookService.java
│
├── exception/                # Error handling
│   ├── BookNotFoundException.java
│   └── GlobalExceptionHandler.java
│
└── web/                      # REST controllers
    └── BookRestController.java
```

## Architecture

```
HTTP Request
     ↓
┌─────────────────┐
│   Controller    │  ← Receives DTO, validation
└────────┬────────┘
         ↓
┌─────────────────┐
│    Service      │  ← Business logic
└────────┬────────┘
         ↓
┌─────────────────┐
│   Repository    │  ← Database operations
└────────┬────────┘
         ↓
┌─────────────────┐
│   PostgreSQL    │
└─────────────────┘
```

## Stopping the Application

1. Stop Spring Boot: `Ctrl+C` in terminal
2. Stop PostgreSQL:
```bash
docker-compose down
```

## Running Tests

```bash
mvn test
```

Tests use H2 in-memory database, PostgreSQL is not required.

## Useful Links

| URL | Description |
|-----|-------------|
| http://localhost:8080/swagger-ui.html | Swagger UI |
| http://localhost:8080/v3/api-docs | OpenAPI JSON |
| http://localhost:8080/actuator/health | Health check |

## Troubleshooting

### Error: "Port 8080 already in use"

Find and stop the process:
```bash
lsof -i :8080
kill -9 <PID>
```

### Error: "Connection refused" to PostgreSQL

Check that container is running:
```bash
docker ps
docker-compose up -d postgres
```

### Error: "docker: command not found"

Install Docker Desktop: https://www.docker.com/products/docker-desktop

## Technologies

| Technology | Version | Description |
|------------|---------|-------------|
| Java | 17 | Programming language |
| Spring Boot | 4.0.2 | Framework |
| Spring Data JPA | - | ORM for database |
| Spring Security | - | Security |
| PostgreSQL | 16 | Database |
| Swagger/OpenAPI | 3.1 | API documentation |
| Lombok | 1.18 | Reduce boilerplate |
| JUnit 5 | - | Testing |

## License

MIT
