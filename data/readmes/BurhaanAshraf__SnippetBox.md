# SnippetBox

A production-style web application built with Go's standard library that enables users to securely create, manage, and view personal code snippets.

The project demonstrates backend engineering concepts including authentication, authorization, session management, CSRF protection, testing, cloud database integration with TiDB Cloud, and server-side rendering using Go templates.

## 🌐 Live Demo

**Application:** https://snippetbox-0mlk.onrender.com/

---

## ✨ Highlights

- Production-style Go web application
- Cloud-hosted TiDB database
- Session-based authentication and authorization
- CSRF protection and secure password hashing
- Layered architecture with dependency injection
- Comprehensive unit and handler tests
- Embedded HTML templates and static assets
- Deployed on Render

---

## 🚀 Features

### Authentication

- User registration
- Secure login and logout
- Password hashing using bcrypt
- Change password functionality
- Persistent server-side session management using SCS

### Snippet Management

- Create new snippets
- View personal snippets
- Automatic snippet expiration
- Personalized **My Latest Snippets** dashboard

### Authorization

- Guests can browse the latest snippet titles
- Only authenticated users can view snippet contents
- Users can only access snippets they own

### Security

- CSRF protection
- Secure session cookies
- bcrypt password hashing
- Input validation
- Environment variable configuration
- TLS-secured connection to TiDB Cloud

### Database

- TiDB Cloud integration
- Foreign key relationships
- Persistent database-backed sessions

### Testing

- Unit tests
- Handler tests
- Model tests
- Mock implementations

---

## 🛠️ Tech Stack

| Category         | Technology          |
| ---------------- | ------------------- |
| Language         | Go                  |
| HTTP             | net/http            |
| Templates        | html/template       |
| Database         | TiDB Cloud          |
| Driver           | go-sql-driver/mysql |
| Sessions         | SCS                 |
| Forms            | go-playground/form  |
| Password Hashing | bcrypt              |
| Testing          | Go Testing Package  |

---

## 🏗️ Architecture

```text
Browser
    │
    ▼
Render
    │
    ▼
HTTP Router
    │
    ▼
Middleware
    │
    ▼
Handlers
    │
    ▼
Models
    │
    ▼
TiDB Cloud
```

The application follows a layered architecture that cleanly separates routing, middleware, handlers, business logic, and database access.

---

## 📁 Project Structure

```text
.
├── cmd/
│   └── web/
│       ├── handlers.go
│       ├── middleware.go
│       ├── routes.go
│       ├── templates.go
│       └── main.go
│
├── internal/
│   ├── models/
│   ├── validator/
│   ├── mocks/
│   └── assert/
│
├── ui/
│   ├── html/
│   ├── static/
│   └── efs.go
│
├── tls/
│   └── isrgrootx1.pem
│
├── go.mod
└── README.md
```

---

## ⚙️ Running Locally

Clone the repository.

```bash
git clone https://github.com/BurhaanAshraf/SnippetBox.git
cd SnippetBox
```

Install dependencies.

```bash
go mod tidy
```

Create a `.env` file.

```env
DB_HOST=
DB_PORT=4000
DB_USER=
DB_PASSWORD=
DB_NAME=snippetbox
```

Run the application.

```bash
go run ./cmd/web
```

Visit:

```
https://localhost:4000
```

---

## 🧪 Quality Assurance

Run all tests.

```bash
go test ./...
```

Run static analysis.

```bash
go vet ./...
```

Format the project.

```bash
gofmt -w .
```

---

## 🎯 Key Concepts Demonstrated

- HTTP routing using Go's `net/http`
- Middleware composition
- Authentication and authorization
- Session management with SCS
- CSRF protection
- Secure password hashing with bcrypt
- Layered application architecture
- Dependency injection
- SQL database integration
- Cloud database deployment with TiDB Cloud
- Server-side rendering using Go templates
- Unit testing with mocks
- Environment-based configuration
- Production deployment on Render

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
