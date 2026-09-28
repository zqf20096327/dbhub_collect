# TickChat Backend - Real-Time Chat Application Server

A robust Java-based backend server for the TickChat real-time messaging application. Built with Java Servlets, Hibernate ORM, and WebSocket technology to deliver instant messaging with minimal latency.

**Repository:** https://github.com/cusaldmsr/TickChat-Backend.git

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [WebSocket Implementation](#websocket-implementation)
- [Core Services](#core-services)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Testing](#testing)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)

## Overview

TickChat Backend provides the server-side infrastructure for a cross-platform real-time messaging application. It handles user authentication, message persistence, contact management, and real-time message delivery through WebSocket connections.

### Key Features

- Phone number-based user authentication
- Real-time bidirectional communication via WebSocket
- Message persistence and retrieval
- Friend list management
- Message deletion with two scopes (for self/for everyone)
- User status tracking (online/offline)
- Emoji and Unicode support (UTF-8 and utf8mb4)
- Connection management and session handling

## Technology Stack

### Core Technologies

- **Java** - Primary backend programming language
- **Java Servlets** - HTTP request handling and RESTful APIs
- **Hibernate ORM** - Object-Relational Mapping framework
- **WebSocket** - Real-time bidirectional communication protocol
- **MySQL** - Relational database management system
- **GlassFish Server** - Java EE application server

### Dependencies

- **Hibernate Core & EntityManager** - ORM framework
- **MySQL JDBC Driver** - Database connectivity
- **Google GSON** - JSON serialization/deserialization
- **Google libphonenumber** - Phone number validation and parsing
- **SLF4J** - Logging framework

### Development Tools

- **NetBeans IDE** - Java development environment
- **Maven** - Project build and dependency management
- **Git** - Version control

## Prerequisites

- Java Development Kit (JDK) 8 or higher
- MySQL Server 5.7 or higher
- GlassFish Server 4.1.1 or higher
- Apache Tomcat 8.5+ (alternative to GlassFish)
- Maven 3.6 or higher
- Postman or similar API testing tool

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/cusaldmsr/TickChat-Backend.git
cd TickChat-Backend
```

### Step 2: Create MySQL Database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE tickchatapp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tickchatapp;

-- Create tables (see Database section below)
```

### Step 3: Configure Hibernate

Edit `src/java/hibernate.cfg.xml` with your database credentials:

```xml
<property name="hibernate.connection.url">
  jdbc:mysql://localhost:3306/tickchatapp?useSSL=false&allowPublicKeyRetrieval=true&useUnicode=true&characterEncoding=UTF-8&serverTimezone=UTC
</property>
<property name="hibernate.connection.username">root</property>
<property name="hibernate.connection.password">your_password_here</property>
```

### Step 4: Build the Project

Using Maven:

```bash
mvn clean build
```

Or in NetBeans:

- Right-click project → Clean and Build

### Step 5: Copy Runtime Libraries

Run the PowerShell script to copy JAR files to WEB-INF/lib:

```powershell
.\scripts\copy_runtime_libs.ps1
```

### Step 6: Deploy to GlassFish

1. Start GlassFish Server
2. Deploy the WAR file through GlassFish admin console or CLI:

```bash
asadmin deploy path/to/TickChat-Backend.war
```

### Step 7: Convert Database to UTF-8MB4 (Optional but Recommended)

Run the SQL script to enable emoji support:

```bash
mysql -u root -p tickchatapp < scripts/convert_to_utf8mb4.sql
```

## Project Structure

```
TickChat-Backend/
├── src/
│   ├── java/
│   │   ├── controller/              # HTTP Servlet controllers
│   │   │   ├── SignInController.java
│   │   │   ├── UserController.java
│   │   │   └── ProfileController.java
│   │   ├── socket/                  # WebSocket and real-time services
│   │   │   ├── ChatEndPoint.java
│   │   │   ├── ChatService.java
│   │   │   ├── UserService.java
│   │   │   ├── ProfileService.java
│   │   │   ├── MessageDeleteService.java
│   │   │   └── ChatSummary.java
│   │   ├── entity/                  # JPA entities
│   │   │   ├── User.java
│   │   │   ├── Chat.java
│   │   │   ├── FriendList.java
│   │   │   ├── Status.java
│   │   │   └── BaseEntity.java
│   │   ├── dto/                     # Data Transfer Objects
│   │   │   └── UserDTO.java
│   │   ├── util/                    # Utility classes
│   │   │   └── HibernateUtil.java
│   │   ├── filter/                  # Servlet filters
│   │   │   └── ConnectionCloseFilter.java
│   │   └── hibernate.cfg.xml        # Hibernate configuration
│   └── conf/
│       └── MANIFEST.MF
├── web/
│   ├── WEB-INF/
│   │   ├── glassfish-web.xml
│   │   ├── lib/                     # Runtime dependencies
│   │   └── web.xml
│   └── profile-images/              # User profile images
├── lib/                             # Project libraries
│   └── Hibernate/                   # Hibernate ORM libraries
├── scripts/
│   ├── convert_to_utf8mb4.sql       # Database UTF-8 conversion
│   └── copy_runtime_libs.ps1        # JAR copy utility
└── build.xml                        # Ant build configuration
```

## Architecture

### Three-Tier Architecture

#### 1. Controller Layer (HTTP Servlets)

Handles HTTP requests from mobile clients:

- `SignInController` - User authentication
- `UserController` - User registration
- `ProfileController` - Profile image management

#### 2. WebSocket Layer

Manages real-time communication:

- `ChatEndPoint` - Central WebSocket endpoint
- Message routing and broadcasting
- Connection lifecycle management

#### 3. Service Layer

Business logic implementation:

- `ChatService` - Message delivery and chat management
- `UserService` - User and friend list operations
- `MessageDeleteService` - Message deletion logic
- `ProfileService` - Profile image storage and retrieval

#### 4. Data Access Layer

Hibernate-based data persistence:

- `HibernateUtil` - Session factory management
- Criteria API for type-safe queries
- Transaction management

#### 5. Database Layer

MySQL persistence store with normalized schema

### Message Flow

**Sending a Message:**

```
Client → WebSocket → ChatEndPoint → ChatService → Database → Broadcasting → Recipient Client
```

**User Authentication:**

```
Client → SignInController → User Lookup → Status Update → Response to Client
```

## Database

### Database Schema

#### User Table

```sql
CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `country_code` VARCHAR(5) NOT NULL,
  `contact_no` VARCHAR(45) NOT NULL UNIQUE,
  `status` VARCHAR(45) DEFAULT 'ONLINE',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Chat Table

```sql
CREATE TABLE `chat` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `from_user` INT NOT NULL,
  `to_user` INT NOT NULL,
  `message` LONGTEXT NOT NULL,
  `files` LONGTEXT DEFAULT 'FILE:',
  `status` VARCHAR(30) DEFAULT 'SENT',
  `deleted_by_sender` BOOLEAN DEFAULT FALSE,
  `deleted_by_receiver` BOOLEAN DEFAULT FALSE,
  `deleted_by_user_id` INT,
  `deleted_by_user_name` VARCHAR(100),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`from_user`) REFERENCES `user`(`id`),
  FOREIGN KEY (`to_user`) REFERENCES `user`(`id`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Friend List Table

```sql
CREATE TABLE `friend_list` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `friend_id` INT NOT NULL,
  `user_status` VARCHAR(30) DEFAULT 'ACTIVE',
  `display_name` VARCHAR(100),
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
  FOREIGN KEY (`friend_id`) REFERENCES `user`(`id`),
  UNIQUE KEY `unique_friendship` (`user_id`, `friend_id`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Entity Relationships

- **User** → **Chat** (1 → Many): A user can have many chats
- **User** → **FriendList** (1 → Many): A user can have multiple friends
- **Chat** → **Status**: Tracks message delivery state
- **FriendList** → **Status**: Tracks friendship state

### Status Enum

```java
ACTIVE, BLOCKED, DELIVERED, READ, SENT, DELETED,
DELETED_FOR_ME, ONLINE, OFFLINE
```

## API Endpoints

### HTTP REST Endpoints

#### POST /SignInController

User authentication via phone number

**Request:**

```json
{
  "countryCode": "+94",
  "contactNo": "712345678"
}
```

**Response:**

```json
{
  "status": true,
  "userId": 1,
  "user": {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "countryCode": "LK",
    "contactNo": "712345678",
    "status": "ONLINE"
  }
}
```

#### POST /UserController

User registration with profile image

**Request (Multipart):**

- firstName: String
- lastName: String
- countryCode: String
- contactNo: String
- profileImage: File

**Response:**

```json
{
  "status": true,
  "userId": 2,
  "user": {
    "id": 2,
    "firstName": "Jane",
    "lastName": "Smith",
    "countryCode": "US",
    "contactNo": "15551234567"
  }
}
```

#### POST /ProfileController

Update user profile image

**Request (Multipart):**

- userId: int
- profileImage: File

**Response:**

```json
{
  "status": true,
  "message": "Profile image update successfully"
}
```

## WebSocket Implementation

### WebSocket Endpoint

**URI:** `ws://localhost:8080/TickChat-Backend/chat?userId=<USER_ID>`

**Message Format (JSON):**

```json
{
  "type": "message_type",
  "payload": {}
}
```

### Supported Message Types

#### ping

Server health check

**Request:**

```json
{
  "type": "ping"
}
```

**Response:**

```json
{
  "type": "PONG"
}
```

#### send_message

Send a new message to a friend

**Request:**

```json
{
  "type": "send_message",
  "toUserId": 2,
  "message": "Hello, how are you?"
}
```

#### get_chat_list

Retrieve all friend conversations with last message

**Request:**

```json
{
  "type": "get_chat_list"
}
```

**Response:**

```json
{
  "type": "friend_list",
  "payload": [
    {
      "friendId": 2,
      "friendName": "Jane Smith",
      "lastMessage": "See you soon!",
      "lastTimeStamp": "2025-10-14T10:30:00",
      "unreadCount": 3,
      "profileImage": "url_to_image"
    }
  ]
}
```

#### get_single_chat

Retrieve message history with specific friend (with pagination support)

**Request:**

```json
{
  "type": "get_single_chat",
  "friendId": 2,
  "beforeId": null,
  "pageSize": 20
}
```

**Response:**

```json
{
  "type": "single_chat",
  "payload": [
    {
      "id": 1,
      "from": { "id": 1, "firstName": "John" },
      "to": { "id": 2, "firstName": "Jane" },
      "message": "Hi Jane!",
      "status": "READ",
      "createdAt": "2025-10-14T10:15:00"
    }
  ]
}
```

#### get_friend_data

Retrieve detailed information about a friend

**Request:**

```json
{
  "type": "get_friend_data",
  "friendId": 2
}
```

#### get_all_users

Retrieve all users in friend list with status

**Request:**

```json
{
  "type": "get_all_users"
}
```

#### delete_message

Delete a message with specified scope

**Request:**

```json
{
  "type": "delete_message",
  "messageId": 1,
  "friendId": 2,
  "scope": "everyone"
}
```

Supported scopes:

- `"everyone"` - Delete for both sender and receiver
- `"me"` - Delete only for current user

#### save_new_contact

Add a new contact to friend list

**Request:**

```json
{
  "type": "save_new_contact",
  "user": {
    "firstName": "Alice",
    "lastName": "Johnson",
    "countryCode": "US",
    "contactNo": "15559876543"
  }
}
```

#### set_user_profile

Retrieve current user profile data

**Request:**

```json
{
  "type": "set_user_profile"
}
```

## Core Services

### ChatService

Manages all chat operations and WebSocket session management.

**Key Methods:**

- `register(userId, session)` - Register user session
- `unregister(userId)` - Unregister user session
- `sendToUser(userId, payload)` - Send message to specific user
- `getFriendChatsForUser(userId)` - Get friend list with chat summaries
- `deliverChat(chat)` - Persist and broadcast new message
- `getChatHistory(userId, friendId)` - Get full message history
- `getChatHistory(userId, friendId, beforeId, pageSize)` - Get paginated history
- `saveNewChat(userId, friendId, message)` - Save new message to database

**Session Management:**

- Maintains ConcurrentHashMap of active user sessions
- Async message sending with error handling
- Automatic connection cleanup on failure

### UserService

Handles user-related operations and status management.

**Key Methods:**

- `updateLogInStatus(userId)` - Set user status to ONLINE
- `updateLogOutStatus(userId)` - Set user status to OFFLINE
- `updateFriendChatStatus(userId)` - Update message delivery status
- `getFriendData(friendId)` - Get friend information
- `getAllUsers(userId)` - Get all contacts from friend list
- `saveNewContact(myId, user)` - Add new contact to friend list
- `getMyProfileData(userId)` - Get current user profile

### MessageDeleteService

Implements sophisticated message deletion logic with two scopes.

**Key Methods:**

- `deleteMessageForEveryone(userId, messageId)` - Delete for both parties
- `deleteMessageForMe(userId, messageId)` - Delete only for current user
- `filterDeletedMessages(userId, chats)` - Filter and transform deleted messages

**Deletion Features:**

- Validates user permissions before deletion
- Tracks deletion metadata (who, when, user name)
- Transforms message content based on deletion type
- Notifies both parties of deletion

### ProfileService

Manages profile image storage and retrieval.

**Key Methods:**

- `saveProfileImage(userId, request)` - Save image to file system
- `getProfileUrl(userId)` - Generate CDN URL for image

**Image Storage:**

- Organized by user ID in `web/profile-images/` directory
- Supports PNG format
- Generates shareable URLs via ngrok tunnel

## Configuration

### Hibernate Configuration (hibernate.cfg.xml)

```xml
<property name="hibernate.connection.driver_class">
  com.mysql.cj.jdbc.Driver
</property>
<property name="hibernate.connection.url">
  jdbc:mysql://localhost:3306/tickchatapp?useSSL=false&useUnicode=true&characterEncoding=UTF-8
</property>
<property name="hibernate.dialect">
  org.hibernate.dialect.MySQLDialect
</property>
<property name="show_sql">true</property>
```

### WebSocket Configuration

Default WebSocket URL in ChatService:

```java
public static final String URL = "https://nonreflected-esta-holy.ngrok-free.dev";
```

Update this URL for your deployment environment.

### Deployment Configuration (web.xml)

Standard Servlet 3.0+ configuration with:

- WebSocket endpoint mapping
- Servlet mappings
- Filter definitions

## Development

### Building the Project

**With Maven:**

```bash
mvn clean install
```

**With NetBeans:**

1. Open project in NetBeans
2. Right-click → Clean and Build

### Running Locally

1. Start GlassFish Server
2. Deploy application
3. Access WebSocket endpoint at: `ws://localhost:8080/TickChat-Backend/chat?userId=1`

### Code Organization

**Naming Conventions:**

- Entity classes: PascalCase (User, Chat, FriendList)
- Service classes: PascalCase with "Service" suffix (ChatService, UserService)
- DTOs: PascalCase with "DTO" suffix (UserDTO)
- Constants: UPPER_SNAKE_CASE

**Best Practices:**

- Use Criteria API for all queries (prevents SQL injection)
- Always close Hibernate sessions in finally blocks
- Implement proper transaction boundaries
- Handle exceptions gracefully with user-friendly messages
- Log errors to console and server logs

### Debugging

**Enable SQL Logging:**
In hibernate.cfg.xml, set:

```xml
<property name="show_sql">true</property>
```

**Monitor WebSocket Connections:**
Check GlassFish server logs for connection events and errors.

## Deployment

### GlassFish Deployment

**Prerequisites:**

- GlassFish 4.1.1 or higher installed
- Server running on port 8080

**Steps:**

1. Build WAR file:

```bash
mvn package
```

2. Deploy via CLI:

```bash
asadmin deploy target/TickChat-Backend.war
```

3. Or via Admin Console:
   - Navigate to http://localhost:4848
   - Applications → Deploy

### Apache Tomcat Deployment

**Steps:**

1. Copy WAR file to `CATALINA_HOME/webapps/`
2. Restart Tomcat
3. Application auto-deploys

### Database Setup for Production

1. Create backup:

```bash
mysqldump -u root -p tickchatapp > backup.sql
```

2. Create production database with proper charset:

```sql
CREATE DATABASE tickchatapp_prod
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

3. Run conversion script:

```bash
mysql -u prod_user -p tickchatapp_prod < convert_to_utf8mb4.sql
```

### SSL/TLS Configuration

For production WebSocket connections, configure SSL:

**In GlassFish:**

1. Admin Console → Configurations → server-config → Network Config
2. Create secure listener on port 8181
3. Configure keystore with valid certificate

**Update ChatService URL:**

```java
public static final String URL = "https://yourdomain.com";
```

### Environment Variables

Create `.env` file or set in application server:

```
DB_URL=jdbc:mysql://db.production.com:3306/tickchatapp
DB_USER=prod_user
DB_PASSWORD=secure_password
WEBSOCKET_URL=https://api.yourdomain.com
```

## Testing

### Unit Testing

Use JUnit for service layer testing:

```java
@Test
public void testUserRegistration() {
    User user = new User("John", "Doe", "LK", "712345678");
    // Assert user creation logic
}
```

### Integration Testing

Test API endpoints with Postman:

1. Create POST request to `/SignInController`
2. Send JSON payload
3. Verify response structure

### WebSocket Testing

Use WebSocket client to test real-time features:

```javascript
const ws = new WebSocket("ws://localhost:8080/TickChat-Backend/chat?userId=1");
ws.onopen = () => {
  ws.send(JSON.stringify({ type: "ping" }));
};
ws.onmessage = (event) => {
  console.log("Response:", event.data);
};
```

### Load Testing

Test concurrent WebSocket connections and message throughput:

- Simulate multiple users
- Send bulk messages
- Monitor server performance
- Check memory usage and database load

## Security

### Authentication

- **Phone Number Validation** - Uses libphonenumber for format validation
- **User Verification** - Lookup in database before allowing operations
- **Session Validation** - Verify userId in WebSocket query string

### Data Protection

- **SQL Injection Prevention** - Hibernate Criteria API prevents injection
- **Input Validation** - Server-side validation of all inputs
- **Unicode Support** - UTF-8MB4 encoding for emoji without attacks

### Message Security

- **Status Tracking** - Prevents message loss with SENT → DELIVERED → READ flow
- **Deletion Tracking** - Audit trail of who deleted what and when
- **Permission Validation** - Only senders can delete "for everyone"

### Production Recommendations

- **Enable HTTPS** - Use SSL/TLS for all communications
- **Implement Rate Limiting** - Prevent abuse and DoS attacks
- **Add Authentication Tokens** - JWT or OAuth for enhanced security
- **Encrypt Sensitive Data** - Hash phone numbers and implement end-to-end encryption
- **Implement Two-Factor Auth** - Additional security layer
- **Monitor Logs** - Set up centralized logging and alerting

### Connection Security

- **WebSocket over WSS** - Use secure WebSocket connections in production
- **CORS Configuration** - Restrict API access to authorized domains
- **Connection Timeout** - Auto-disconnect idle connections

## Troubleshooting

### Common Issues

**Issue: Hibernate SessionFactory not initializing**

```
Initial SessionFactory creation failed
```

**Solution:**

1. Check hibernate.cfg.xml syntax
2. Verify database credentials
3. Ensure MySQL is running
4. Check JDBC driver is in classpath

**Issue: WebSocket connection fails**

```
Failed to connect to WebSocket endpoint
```

**Solution:**

1. Verify server is running
2. Check firewall settings
3. Verify userId query parameter is valid
4. Check browser console for detailed error

**Issue: Emoji not displaying correctly**

**Solution:**

1. Run `convert_to_utf8mb4.sql` script
2. Verify database charset: `utf8mb4`
3. Verify connection string includes `&characterEncoding=UTF-8`
4. Restart application server

**Issue: Profile images not loading**

**Solution:**

1. Verify `web/profile-images/` directory exists
2. Check file permissions
3. Verify ngrok tunnel is running
4. Update ChatService.URL if using new tunnel

**Issue: Messages not being delivered**

**Solution:**

1. Check WebSocket connection is open
2. Verify both users are in database
3. Monitor server logs for errors
4. Check message status field in database

### Performance Optimization

- **Database Indexing** - Create indexes on frequently queried columns
- **Connection Pooling** - Configure Hibernate connection pool settings
- **Message Pagination** - Implement pagination for large chat histories
- **Lazy Loading** - Configure Hibernate lazy loading strategies

## Contributors

**Project Lead:** P. Kusal Damsara  
**Institution:** Java Institute for Advanced Technology  
**Supervisor:** Mr. Anjana Dilhara Samarakoon

## License

This project is part of the Handheld Device Programming I module at the Java Institute for Advanced Technology.

## Support

For issues, questions, or contributions:

1. Check existing issues on GitHub
2. Create a detailed bug report with:

   - Error message or log output
   - Steps to reproduce
   - Expected vs actual behavior
   - Server environment details

3. For security vulnerabilities, please report privately to the project maintainer

---

**Repository:** https://github.com/cusaldmsr/TickChat-Backend.git

**Project Documentation:** See included project documentation PDF for comprehensive system design details.

Last Updated: 2025
