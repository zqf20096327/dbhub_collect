# Project Name

A professional Go backend using **Gin**, **GORM**, **Redis**, and **Swagger** designed for fintech-grade applications.  
Features a clean architecture with **Handler → Service → Repository → Model** layers, CLI commands for migrations, seeding, and running the server, plus auto-generated Swagger API docs.

## Features

- RESTful API using **Gin**  
- GORM ORM with **auto-migrations** and **seed data**  
- Redis caching layer for high performance  
- Structured logging using **Zap** with request IDs  
- Versioned API routes (`/api/v1/...`)  
- CLI commands for DB migration, seeding, and running server  
- Auto-generated **Swagger / OpenAPI documentation**  

---

## Tech Stack

- Go 1.21+  
- Gin Web Framework  
- GORM ORM (Postgres / MySQL / SQLite)  
- Redis  
- Zap Logger  
- Swaggo for Swagger Documentation  

## Installing Golang

```bash
sudo apt update
sudo apt upgrade -y

wget https://go.dev/dl/go1.21.2.linux-amd64.tar.gz # You can change version
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.2.linux-amd64.tar.gz

nano ~/.profile

# Go environment
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

---

## Project Structure

```text
cmd/
 ├─ api/                 # HTTP server entrypoint
 │   └─ main.go
 └─ cli/                 
     ├─ main.go          # CLI commands for migrate, seed, run
     └─ create_db.go     # CLI commands for create db

internal/
 ├─ config/              # Environment / config loader
 ├─ observability/       # Logger + request ID middleware
 ├─ server/              # Gin engine
 ├─ routes/              # Route registration
 ├─ handler/             # HTTP handlers (controllers)
 ├─ service/             # Business logic
 ├─ repository/          # GORM models + DB queries
 ├─ cache/               # Redis client wrapper
 ├─ model/               # Pure data structures (optional)
 ├─ services/            # Business Logic
 └─ middleware/          # Middleware
```
---
## Setup Environment Variables

```bash
APP_ENV=local
APP_PORT=8080

LOG_LEVEL=info

NODE_ENV=development

# Security
API_KEY=local-dev-key

# Database (optional)
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=app
DB_LOG_MODE=false

# Cache
REDIS_ADDR=localhost:6379

```
---
## Install dependencies

```bash
go mod tidy
```
---
## Create the Database

This step is optional if your database already exists.
You can create the database manually:

```bash
-- PostgreSQL example
CREATE DATABASE dbname;
```

Or using a CLI command if implemented

```bash
go run ./cmd/api/main.go create-db
```

---
## Run Database Migration

To create tables based on your GORM models

```bash
go run ./cmd/api/main.go migrate
```
Or, if ```AUTO_MIGRATE=true``` in .env, migrations will run automatically when starting the server.


---
## Seed Initial Data(optional)

Populate your database with initial test data

```bash
go run ./cmd/api/main.go seed
```


---
## Start the Server

```bash
go run ./cmd/api/main.go run
```

Server will start at:

```bash
http://localhost:8080
```