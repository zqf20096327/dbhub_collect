# Golang CRUD Service

This is a sample CRUD service built with **Golang**, demonstrating a layered architecture that separates concerns into handler, service, repository, and model layers. The project uses **TiDB** as the relational database, **Redis** for `caching` and `async tasks` in-memory operations, and **JWT** for authentication.

## Project Purpose

Build a sample CRUD service API with Golang to showcase code structure and common best practices in web API development.

## Tech Stack

- **[Golang](https://golang.org)** — Core programming language
- **[Fiber](https://gofiber.io)** — Fast HTTP router
- **[GORM](https://gorm.io)** — ORM for database operations
- **[TiDB](https://www.pingcap.com)** — Distributed SQL database
- **[Validator](https://github.com/go-playground/validator)** — Input validation
- **[Copier](https://github.com/jinzhu/copier)** — Object copying for DTOs
- **[Redis](https://redis.io)** — Distributed In-memory data caching
- **[Redis Stream](https://redis.io/docs/latest/develop/data-types/streams)** — Background task queue using consumer group
- **[JWT](https://github.com/golang-jwt/jwt)** — JSON Web Token implementation for authentication

## Project Structure

```
├── cmd/
│   └── app/
│       └── main.go                # Application entry point
├── pkg/                           # Shared package configure
│   ├── crypto/
│   │   ├── aes.go                 # Advanced Encryption Standard
│   │   └── bcrypt.go              # Bcrypt hashing
│   ├── redis/
│   │   └── redis.go               # Redis configuration
│   └── db/
│       └── db.go                  # DB configuration
├── api/
│   ├── auth/
│   │   ├── routes.go              # User authenticate-related endpoints
│   │   └── handler.go             # Logic for handling auth API requests
│   └── student/
│       ├── routes.go              # Student-related endpoints
│       └── handler.go             # Logic for handling student API requests
├── internal/
│   ├── middleware/                # HTTP middleware (e.g., auth, rate limit, logging)
│   ├── repository/                # Data access layer (calls GORM & queries DB)
│   ├── service/                   # Business logic, called from handler
│   ├── model/                     # Database models/entities
│   └── dto/                       # DTOs for transforming request/response data
```

## Key Concepts

- **Layered Architecture**: Divides the project into clear layers for maintainability and scalability.
- **Goroutines**: Background task workers use `goroutines` to run concurrent `redis stream` jobs efficiently.
- **Rate Limit**: Failed attempts and request limited using `redis` to prevent abuse `429 Too Many Requests`.
- **DTO Pattern**: Uses `copier` to map between internal models and request/response structures.
- **Validation**: Ensures request payloads are validated with `go-playground/validator`.
- **ORM**: Leverages `GORM` to interact with `TiDB` in a concise and type-safe way.
- **SMTP**: Standard `net/smtp` package for email sending to SMTP server.

> 💡 Tip: If you're using Gmail SMTP: allow **"Less secure apps"** (not recommended)

## Running the Project

1. **Configure Environment**
   Create a `.env` file. find in a `.env.example` file for environment:
   - Redis connection
   - TiDB connection
   - Email configure
   - JWT Secret key

2. **Run the App**
   ```bash
   go run cmd/app/main.go
   ```

3. **Build the App**
   ```bash
   GOOS=linux GOARCH=amd64 go build -o bin/app ./cmd/app
   ```

4. **Containerize the App**
   ```bash
   docker compose up -d
   ```


## Future Enhancements

- Add unit tests and integration tests
- Add Swagger/OpenAPI documentation

## License

This project is open-source and available under the [MIT License]().
