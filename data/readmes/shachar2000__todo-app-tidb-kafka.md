# Todo App with TiDB, Kafka & Node.js

## Overview
This is a full-stack Todo App project including:  
- **Backend:** Node.js + Express.js  
- **Frontend:** basic HTML 
- **Database:** TiDB  
- **Message Queue:** Apache Kafka  
- **CDC:** Change Data Capture to track database changes  
- **Logging:** log4js with structured JSON logs  

The project is fully containerized with **Docker & Docker Compose** and provides real-time logging and message streaming.

---

## Docker Compose Setup

To start all services:

```bash
docker-compose up --build -d
```

---

## Exposed Ports
Frontend Website: http://localhost:8080

Backend API: http://localhost:3000

Kafka UI: http://localhost:8081 – monitor messages in the topic test-topic

TiDB SQL: 4000

TiKV Status: 20180

---

## Services Description
pd:	Placement Driver for TiDB cluster  
tikv:	Storage node for TiDB  
tidb:	SQL node for TiDB  
ticdc:	TiDB CDC server for tracking DB changes  
ticdc-setup:	Script to automatically create a changefeed for Kafka  
db-init:	Initializes TiDB with tables and a default user  
kafka:	Kafka broker for message streaming  
kafka-ui:	Web UI for monitoring Kafka topics  
frontend:	HTML frontend for the Todo App  
backend:	Node.js backend with login & JWT authentication  
consumer:	Node.js consumer application to read DB changes from Kafka  

---

## Database Initialization
Check logs for db-init:

```bash
docker logs db-init
```  
Expected output:  
```bash
Waiting for TiDB to be ready...
Running init.sql on TiDB...
DB init done. Keeping container alive...
```

TiCDC & Changefeed Setup:
Check logs for ticdc-setup:

```bash
docker logs ticdc-setup
```

Expected output:

```bash
Waiting for TiCDC and Kafka to be ready...
Creating changefeed: todo-cf
Changefeed created successfully!
Listing all changefeeds...
Setup completed. Keeping container alive...
```
This sets up a changefeed streaming DB changes to Kafka topic test-topic.

## Frontend Usage:  
Open http://localhost:8080

Sign up or log in with default credentials:

Username: testuser

Password: test123

## Backend Logging (User Activity)
Every login is logged in JSON format using log4js. Check backend logs:
```bash
docker logs sre-task-backend-1
```

Example login log:

```bash
{
  "timestamp": "2025-08-21T10:02:50.997Z",
  "userId": 1,
  "action": "login",
  "ip": "::ffff:172.18.0.1"
}
```

## Consumer Logging (CDC / Real-time Processing)
The Node.js consumer reads all database change messages from Kafka and logs them in structured JSON format:
```bash
docker logs todo-consumer
```
Example log entry:

```bash
{
  "timestamp": "2025-08-21T10:34:43.060Z",
  "action": "UPDATE",
  "table": "users",
  "data": [
    {
      "id": "1",
      "username": "testuser",
      "password": "...",
      "token": "..."
    }
  ],
  "oldData": [
    {
      "id": "1",
      "username": "testuser",
      "password": "...",
      "token": null
    }
  ],
  "topic": "test-topic",
  "partition": 0,
  "offset": "0"
}
```

You can also monitor all messages in Kafka topic test-topic via Kafka UI.

## Notes
All logs are in structured JSON, consistent for both login activity and DB changes.

Ensure all containers are running on the same Docker network (tidb-network).

Volumes are used to persist Kafka and TiDB data/logs.