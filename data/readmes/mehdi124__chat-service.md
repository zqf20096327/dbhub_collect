# 💬 Chat Service

[![Go Version](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat&logo=go)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/mehdi124/chat-service?style=social)](https://github.com/mehdi124/chat-service)

A high-performance, scalable real-time chat service built with Go. Features WebSocket support, message persistence, file uploads, and push notifications.

```
   ____ _           _     ____                  _          
  / ___| |__   __ _| |_  / ___|  ___ _ ____   _(_) ___ ___ 
 | |   | '_ \ / _` | __| \___ \ / _ \ '__\ \ / / |/ __/ _ \
 | |___| | | | (_| | |_   ___) |  __/ |   \ V /| | (_|  __/
  \____|_| |_|\__,_|\__| |____/ \___|_|    \_/ |_|\___\___|
```

## ✨ Features

- **Real-time Messaging** - WebSocket-based real-time communication
- **Room Types** - Support for Private chats, Groups, and Channels
- **Message Types** - Text messages, file attachments, replies, and forwards
- **File Uploads** - S3-compatible storage with presigned URLs
- **Push Notifications** - Firebase Cloud Messaging integration
- **High Availability** - PostgreSQL replication with PgPool load balancing
- **Message Queue** - RabbitMQ cluster for reliable message delivery
- **Caching** - Redis for connection management and caching
- **JWT Authentication** - Secure token-based authentication

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NGINX (Load Balancer)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
              ┌─────▼─────┐                       ┌─────▼─────┐
              │  HTTP API │                       │ WebSocket │
              └─────┬─────┘                       └─────┬─────┘
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
                    │         Chat Service (Go)         │
                    │   - Fiber HTTP Framework          │
                    │   - Hexagonal Architecture        │
                    │   - Wire Dependency Injection     │
                    └─────────────────┬─────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
    ┌─────▼─────┐               ┌─────▼─────┐               ┌─────▼─────┐
    │  PgPool   │               │  RabbitMQ │               │   Redis   │
    │           │               │  Cluster  │               │           │
    └─────┬─────┘               └───────────┘               └───────────┘
          │
    ┌─────▼─────────────────────────────────┐
    │              PostgreSQL               │
    │   ┌─────────┐  ┌─────────┐  ┌─────────┐
    │   │ Primary │  │Replica 1│  │Replica 2│
    │   └─────────┘  └─────────┘  └─────────┘
    └───────────────────────────────────────┘
```

## 📋 Prerequisites

### Required Software
- **Go 1.22+** - [Download Go](https://golang.org/dl/)
- **Docker & Docker Compose** - [Install Docker](https://docs.docker.com/get-docker/)
- **Make** - Build automation tool

### Required Infrastructure Services

| Service | Purpose | Required |
|---------|---------|----------|
| **PostgreSQL** | Primary data storage with streaming replication | ✅ Yes |
| **Redis** | WebSocket connection state, chunk upload tracking, distributed locks | ✅ Yes |
| **RabbitMQ** | Message queue cluster for real-time message delivery | ✅ Yes |
| **S3-Compatible Storage** | File uploads (AWS S3, MinIO, Arvan Cloud, etc.) | ✅ Yes |
| **Firebase** | Push notifications for offline users | ⚪ Optional |

### S3 Storage Setup

This service requires an S3-compatible object storage for file uploads. You can use:
- **AWS S3** - Amazon's object storage
- **MinIO** - Self-hosted S3-compatible storage
- **Arvan Cloud** - Iranian cloud provider (used in development)
- **DigitalOcean Spaces** - S3-compatible object storage

Configure in `.env`:
```bash
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_ENDPOINT=https://your-s3-endpoint.com
S3_BUCKET_NAME=your-bucket-name
S3_REGION=default
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mehdi124/chat-service.git
cd chat-service
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Update all placeholder values with secure credentials
```

#### Generate Secure Secrets

```bash
# Generate JWT secret
openssl rand -base64 32

# Generate Redis password
openssl rand -hex 24

# Generate RabbitMQ Erlang cookie
openssl rand -hex 32

# Generate API key
openssl rand -hex 16
```

### 3. Start Infrastructure Services

```bash
# Start all infrastructure services (PostgreSQL, Redis, RabbitMQ, etc.)
docker-compose up -d
```

### 4. Install Dependencies & Build

```bash
# Install Go dependencies and development tools
make install

# Generate Wire dependency injection code
make wire

# Build the application
go build -o main .
```

### 5. Run Database Migrations

```bash
# Run migrations with your config file
./main migrate up -c .env
```

### 6. Start the Application

```bash
# Run the chat service
./main app run -c .env
```

The service will be available at:
- **HTTP API**: `http://localhost:8000/api/v1`
- **WebSocket**: `ws://localhost:8000/ws/v1`

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t chat-service:latest .
```

### Run with Docker Compose

The `docker-compose.yaml` includes all necessary services:

| Service | Description | Ports |
|---------|-------------|-------|
| PgPool | PostgreSQL connection pooler | 9999 |
| PostgreSQL Primary | Main database | - |
| PostgreSQL Replica 1-2 | Read replicas | - |
| Redis | Session/cache store | 6379 |
| RabbitMQ 1-3 | Message queue cluster | - |
| HAProxy | RabbitMQ load balancer | 5672, 15672 |
| Nginx | HTTP/WebSocket proxy | 80, 443 |

## 📁 Project Structure

```
chat-service/
├── cmd/                    # CLI commands
│   ├── app.go             # Application runner
│   ├── migrate.go         # Database migration commands
│   ├── root.go            # Root command setup
│   └── token.go           # Token generation utilities
├── config/                 # Configuration loading
├── core/
│   └── app/               # Application bootstrap & DI
├── database/
│   └── migration/         # SQL migration files
├── infra/                  # Infrastructure adapters
│   ├── logger.go          # Logging setup
│   ├── pg.go              # PostgreSQL connection
│   ├── rabbitmq.go        # RabbitMQ connection
│   ├── redis.go           # Redis connection
│   ├── s3.go              # S3 storage client
│   └── server.go          # HTTP server setup
├── internal/
│   ├── chat/
│   │   ├── adapter/
│   │   │   ├── inbound/   # HTTP, WebSocket, RabbitMQ handlers
│   │   │   └── outbound/  # Repository implementations
│   │   └── core/
│   │       ├── domain/    # Domain models & value objects
│   │       ├── port/      # Inbound & Outbound port interfaces
│   │       └── service/   # Business logic services
│   └── shared/            # Shared utilities & middleware
├── volumes/               # Docker volume configurations
├── docker-compose.yaml    # Infrastructure services
├── Dockerfile             # Application container
├── Makefile              # Build automation
└── .env.example          # Environment template
```

## 🔧 CLI Commands

```bash
# Run the application
./main app run -c <config-file>

# Database migrations
./main migrate up -c <config-file>      # Apply migrations
./main migrate down -c <config-file>    # Rollback migrations
./main migrate seed -c <config-file>    # Seed database
```

### Generate Test Tokens (Development Only)

```bash
# Generate test JWT tokens for development
./main token init -c .env
```

> ⚠️ **WARNING**: The `token init` command generates tokens for **hardcoded test user IDs** and is intended for **development and testing only**. Do NOT use this in production. For production environments, implement a proper user authentication flow through your application's login endpoint.

## 📡 API Endpoints

### Authentication

All API requests require authentication via JWT Bearer token.

```bash
Authorization: Bearer <jwt_token>
```

### API Documentation

Full API documentation is available in OpenAPI 3.0 format:

📄 **[docs/openapi.yaml](docs/openapi.yaml)**

You can view it using:
- [Swagger Editor](https://editor.swagger.io/) - Paste the file content
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Host locally
- VS Code with [OpenAPI extension](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi)

### Room Types
- **PRIVATE** - One-to-one direct messages
- **GROUP** - Multi-user group chat (max 50 members by default)
- **CHANNEL** - Broadcast channel (max 100 members by default)

### Message Types
- **TEXT** - Plain text message
- **FILE** - File attachment
- **REPLIED** - Reply to another message
- **FORWARDED** - Forwarded message

## 🔌 WebSocket Connection

Connect to the WebSocket endpoint for real-time messaging. Authentication is done via JWT token in the query parameter.

```javascript
const token = 'your_jwt_token';
const ws = new WebSocket(`ws://localhost:8000/ws/v1/chat?token=${token}`);

// Handle incoming messages (MessagePack encoded)
ws.onmessage = async (event) => {
  const buffer = await event.data.arrayBuffer();
  const message = msgpack.decode(new Uint8Array(buffer));
  console.log('Received:', message);
};
```

### Message Encoding Format

WebSocket messages use **MessagePack** binary format for efficient serialization. MessagePack is a binary-based serialization format that is more compact and faster than JSON.

#### Install MessagePack Library

```bash
# JavaScript/Node.js
npm install @msgpack/msgpack

# Go (already included)
# github.com/vmihailenco/msgpack/v5
```

#### Request Structure (Client → Server)

```javascript
import { encode } from '@msgpack/msgpack';

// Send a text message
const request = {
  Type: 'message',           // 'message' | 'seen' | 'ping'
  RoomID: 'room-uuid',       // Target room UUID
  ReceiverID: 'user-uuid',   // For private messages (optional if RoomID provided)
  Content: 'Hello World',    // Message content or filename
  ContentType: 'text',       // 'text' | 'image' | 'video' | 'audio' | 'file'
  MessageType: 'direct',     // 'direct' | 'replied' | 'forwarded'
  Sign: 'unique-sign-123',   // Unique client-side message identifier
  ParentMessageID: ''        // For replies/forwards
};

ws.send(encode(request));
```

#### Response Structure (Server → Client)

```javascript
import { decode } from '@msgpack/msgpack';

// Response format
{
  Type: 'response',      // 'response' | 'new_message' | 'seen' | 'pong'
  Success: true,
  Error: '',
  Data: {
    ID: 'message-uuid',
    RoomID: 'room-uuid',
    SenderID: 'user-uuid',
    Content: 'Hello World',
    ContentType: 'text',
    Status: 'sent',
    CreatedAt: '2024-01-01T00:00:00Z',
    // ... additional fields
  }
}
```

#### Request Types

| Type | Description |
|------|-------------|
| `message` | Send a new message |
| `seen` | Mark messages as seen in a room |
| `ping` | Keep connection alive (receives `pong`) |

#### Go Example (Server-side)

```go
import "github.com/vmihailenco/msgpack/v5"

// Decode incoming message
var req ChatRequest
if err := msgpack.Unmarshal(msg, &req); err != nil {
    return err
}

// Encode response
response := ChatResponse{
    Type:    "response",
    Success: true,
    Data:    message,
}
encoded, _ := msgpack.Marshal(response)
```

## 📤 Chunked File Upload

The service supports multipart/chunked file uploads for large files using S3's multipart upload API.

### Upload Flow

```
┌──────────┐                    ┌──────────┐                    ┌───────┐                    ┌────┐
│  Client  │                    │  Server  │                    │ Redis │                    │ S3 │
└────┬─────┘                    └────┬─────┘                    └───┬───┘                    └─┬──┘
     │                               │                              │                          │
     │  1. Send chunk 1              │                              │                          │
     │  (FileID, ChunkIndex=1,       │                              │                          │
     │   TotalChunk=N)               │                              │                          │
     │──────────────────────────────>│                              │                          │
     │                               │  2. CreateMultipartUpload    │                          │
     │                               │─────────────────────────────────────────────────────────>│
     │                               │                              │       UploadID           │
     │                               │<─────────────────────────────────────────────────────────│
     │                               │  3. Store UploadID           │                          │
     │                               │─────────────────────────────>│                          │
     │                               │  4. UploadPart (chunk 1)     │                          │
     │                               │─────────────────────────────────────────────────────────>│
     │                               │                              │       ETag               │
     │                               │<─────────────────────────────────────────────────────────│
     │                               │  5. Store ETag               │                          │
     │                               │─────────────────────────────>│                          │
     │  6. Repeat for chunks 2..N-1  │                              │                          │
     │──────────────────────────────>│                              │                          │
     │                               │                              │                          │
     │  7. Send final chunk N        │                              │                          │
     │──────────────────────────────>│                              │                          │
     │                               │  8. Get all ETags            │                          │
     │                               │─────────────────────────────>│                          │
     │                               │<─────────────────────────────│                          │
     │                               │  9. CompleteMultipartUpload  │                          │
     │                               │─────────────────────────────────────────────────────────>│
     │                               │                              │                          │
     │  10. Broadcast to room        │                              │                          │
     │<──────────────────────────────│                              │                          │
```

### Upload Requirements

- **Minimum chunk size**: 5 MB (S3 requirement for multipart uploads)
- **Maximum file size**: 20 MB (configurable via `S3_MAX_UPLOAD_SIZE`)
- **Supported formats**: Images, Videos, Audio, Documents, Archives

### Upload Example (JavaScript)

```javascript
async function uploadFile(file, messageId, token) {
  const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB minimum
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
  
  for (let i = 0; i < totalChunks; i++) {
    const start = i * CHUNK_SIZE;
    const end = Math.min(start + CHUNK_SIZE, file.size);
    const chunk = file.slice(start, end);
    
    const formData = new FormData();
    formData.append('File', chunk);
    formData.append('ChunkIndex', i + 1);
    formData.append('TotalChunk', totalChunks);
    
    await fetch(`/api/v1/files/${messageId}/upload`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    });
  }
}
```

### Concurrent Upload Handling

The service uses **Redis distributed locks** to handle concurrent chunk uploads safely:
- Lock acquisition prevents duplicate `UploadID` creation
- Each chunk's ETag is tracked in Redis
- Upload completes automatically when all chunks are received

## ⚡ RabbitMQ Load Balancing & Scalability

### Consistent Hash-Based Queue Distribution

The service uses **FNV-1a consistent hashing** to distribute messages across multiple RabbitMQ queues, enabling horizontal scaling and ordered message delivery per room.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Message Publishing                               │
│                                                                          │
│   User sends message → Hash(UserID) → Queue N → Consumer → WebSocket   │
│                                                                          │
│   Example with 10 queues:                                               │
│   ┌─────────┐     ┌──────────────┐     ┌─────────────────┐              │
│   │ User A  │────>│ hash % 10 = 3│────>│ chat.queue.3    │              │
│   │ User B  │────>│ hash % 10 = 7│────>│ chat.queue.7    │              │
│   │ User C  │────>│ hash % 10 = 3│────>│ chat.queue.3    │ (same queue) │
│   └─────────┘     └──────────────┘     └─────────────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Capacity Calculation

With the default configuration of **10 queues** per service instance:

| Metric | Value |
|--------|-------|
| Queues per instance | 10 |
| Messages/sec per queue | ~1,000 |
| Throughput per instance | ~10,000 msg/sec |
| Concurrent WebSocket connections | ~10,000 per instance |

**To handle 100,000 concurrent users:**
- Deploy **10 service instances** behind a load balancer
- Each instance handles ~10,000 connections
- Total queue count: 100 (10 queues × 10 instances)
- Configure `RABBITMQ_TOTAL_QUEUE=10` per instance

### Scaling Strategy

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    │    (Nginx)      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │Instance1│         │Instance2│         │Instance3│
   │10 queues│         │10 queues│         │10 queues│
   └────┬────┘         └────┬────┘         └────┬────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ RabbitMQ Cluster│
                    │  (3 nodes HA)   │
                    └─────────────────┘
```

### Benefits of This Architecture

1. **Ordered Delivery**: Messages from the same user always go to the same queue
2. **Horizontal Scaling**: Add more instances to handle more users
3. **Fault Tolerance**: RabbitMQ cluster ensures no message loss
4. **Load Distribution**: FNV-1a hash provides even distribution

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cover

# Run tests with race detector
make test-race
```

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files. Use `.env.example` as a template.
2. **JWT Secrets**: Generate strong, random secrets for JWT signing.
3. **Database Passwords**: Use strong, unique passwords for all database users.
4. **SSL/TLS**: Enable SSL in production for all connections.
5. **API Keys**: Rotate API keys regularly.
6. **Firebase Credentials**: Keep service account keys secure and never expose them publicly.

## 📊 Monitoring

### RabbitMQ Management UI
Access at `http://localhost:15672` (default: guest/guest in development)

### PostgreSQL
Connect via PgPool at `localhost:9999`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Fiber](https://gofiber.io/) - Fast HTTP framework
- [Wire](https://github.com/google/wire) - Compile-time dependency injection
- [Bun](https://bun.uptrace.dev/) - SQL-first ORM for Go
- [Viper](https://github.com/spf13/viper) - Configuration management
- [Cobra](https://github.com/spf13/cobra) - CLI framework

---

Made with ❤️ in Go
