# 🔐 Spring Security JWT Template — Spring Boot 3.3.5

## 📋 Prerequisites

- ☕ Java 23
- 🐘 PostgreSQL
- 💻 IDE: IntelliJ IDEA, Eclipse, etc.

## ⚙️ Configuration

Copy and update the `application-local.properties.example` in resources folder, it should be named `application-local.properties`

Copy and update the `.env.example` file in the .devcontainer folder of the application, it should be named `.env`

📚 Documentation
----------------

- 📖 Swagger UI available at:`/api/v1/swagger-ui/index.html`
- 🔍 OpenAPI docs at:`/api/v1/v3/api-docs`

🛡️ Security Features
---------------------

**Authentication & Authorization**

- ✅ JWT-based authentication
- ✅ Role-based access control (RBAC)
- ✅ Permission-based access control
- ✅ Secure password handling
- ✅ Token invalidation on user updates
- ✅ Locale-based responses (en/es)
- ✅ Cache-based permission management
- ✅ Dynamic path pattern matching

**Developer Protection**

- ✅ Cannot delete last remaining developer
- ✅ Automatic token invalidation before deletion
- ✅ Username uniqueness validation
- ✅ Safe update operations
- ✅ Path-based permission control
- ✅ Status change validation

**Admin Protection**

- ✅ Cannot delete last remaining admin
- ✅ Automatic token invalidation before deletion
- ✅ Username uniqueness validation
- ✅ Safe update operations
- ✅ Enhanced path security

**Customer Management**

- ✅ Full CRUD operations
- ✅ Role-based access control
- ✅ Username uniqueness validation
- ✅ Safe update operations
- ✅ Status management

**Business Rules**

*User Management:*

- System maintains at least one active user per role
- Validates unique usernames across all user types
- Auto-logout (token invalidation) on profile updates
- Internationalization support (i18n)
- Permission caching with Guava
- Dynamic path pattern matching for endpoints

*Token Security:*

- Automatic invalidation on sensitive data changes
- Proper cleanup during user deletion
- Expiration handling
- Refresh token support
- JWT validation and cleanup
- Role-only JWT payload
- Cached permissions management

*Path Security:*

- Dynamic path pattern matching
- Support for numeric IDs in paths
- Boolean status handling
- Nested resource protection
- Base path standardization
- API version prefix handling

*API Documentation:*

- Swagger UI integration
- OpenAPI 3.0 specification
- Interactive API testing
- Endpoint authorization information
- Permission requirements documentation

*Performance Improvements:*

- Guava cache implementation
- Optimized path matching
- Efficient permission checking
- Pattern-based URL matching

*Useful links:*

- To convert any text into Markdown format: [Markdown Converter](https://euangoddard.github.io/clipboard2markdown/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

This project is licensed under the Apache License 2.0—see the [LICENSE](LICENSE) file for details.