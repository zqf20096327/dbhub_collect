<div align="center">
  
# 🛒 Ktor E-Commerce Backend
  
  **A high-performance, enterprise-grade e-commerce backend built with Kotlin & Ktor.**

  [![Ktor](https://img.shields.io/badge/ktor-3.5.1-blue.svg)](https://github.com/ktorio/ktor)
  [![Exposed](https://img.shields.io/badge/Exposed-1.3.0-blue.svg)](https://github.com/JetBrains/Exposed)
  [![Kotlin](https://img.shields.io/badge/Kotlin-2.4.0-blue.svg?style=flat&logo=kotlin)](https://kotlinlang.org)
  ![Koin](https://img.shields.io/badge/Koin-4.2.0-29BEB0?logo=koin&logoColor=white)
  [![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-42.7.8-336791?logo=postgresql)](https://www.postgresql.org/)
  [![GitHub license](https://img.shields.io/badge/license-Apache%20License%202.0-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)
  <a href="https://github.com/piashcse"><img alt="Author" src="https://img.shields.io/static/v1?label=GitHub&message=piashcse&color=C51162"/></a>

  <h4>
    <a href="https://piashcse.github.io/ktor-E-Commerce">Documentation</a>
    <span> · </span>
    <a href="https://github.com/piashcse/ktor-E-Commerce/issues">Report Bug</a>
    <span> · </span>
    <a href="https://github.com/piashcse/ktor-E-Commerce/pulls">Request Feature</a>
  </h4>

  <img src="https://github.com/piashcse/ktor-E-Commerce/blob/master/screenshots/swagger.gif" width="100%" alt="Ktor-E-Commerce Banner" style="border-radius: 10px; margin-top: 20px;" />
</div>

---

## 🚀 Overview

**Ktor-E-Commerce** is a robust, scalable, and high-performance backend solution designed for modern e-commerce applications. Leveraging the power of [Kotlin](https://kotlinlang.org) and [Ktor](https://ktor.io), it provides an efficient service for handling complex e-commerce workflows, from multi-role authentication to advanced order processing and real-time inventory management.

### Key Pillars
- **Performance**: Built with Ktor's asynchronous engine for non-blocking I/O.
- **Security**: JWT-based auth, rate limiting, and password complexity enforcement.
- **Quality**: Strict static analysis with Ktlint and Detekt integrated.

# Features

### 1. Role-Based Access Control

- **Customer Role**: Shoppers with basic access to browse and make purchases.
- **Seller Role**: Vendors can list products and manage their inventory.
- **Admin Role**: Administrators have full control over the platform.

### 2. User Accounts and Authentication

- **User Registration**: Allow customers to create accounts. Users can register with the same email for different roles (customer and seller).
- **User Authentication**: Implement JWT-based authentication for user sessions.
- **User Profiles**: Enable users to view and update their profiles.

### 3. Product Management

- **Product Listings**: Create, update, and delete product listings.
- **Categories**: Organize products into categories and brands for easy navigation.
- **Inventory Control**: Keep track of product availability and stock levels.

### 4. Shopping Cart and Checkout

- **Shopping Cart**: Add and remove products, update quantities, and calculate totals.
- **Checkout Summary**: Retrieve detailed checkout summary with subtotal, shipping, tax, and discount breakdown.
- **Checkout**: Streamline the checkout process with consolidated shipping address and method selection.
- **Stock Validation**: Automatic stock validation during checkout using effective inventory levels.
- **Price Validation**: Order totals validated against database prices to prevent tampering.
- **Cart Clearing**: Automatic cart clearing after successful order placement.

### 5. Order Management

- **Order Processing**: Handle order creation, status updates, and order history.
- **Order Status History**: Comprehensive audit trail for every status transition (Placed, Confirmed, Shipped, etc.).
- **Automatic Taxation**: Configurable tax calculation (default 5%) applied automatically during checkout.
- **Order Cancellation**: Customers can cancel PENDING/CONFIRMED orders with autom

[...截断...]

atic stock restoration.
- **Seller Orders**: Sellers can view and manage orders from their shop.
- **Admin Orders**: Admins can view all orders with advanced filters (status, date range).
- **Human-Readable Order Numbers**: Sequential order numbers in format ORD-YYYYMMDD-XXXX.
- **Idempotency Support**: Prevent duplicate orders with idempotency keys.
- **Payment Integration**: Integrate with popular payment gateways for seamless transactions.
- **Payment Validation**: Payment amounts validated against order totals.
- **Payment History**: Track all payments for each order.

### 6. Discount & Coupon System

- **Promo Codes**: Create and manage fixed or percentage-based discount coupons.
- **Usage Limits**: Enforce expiration dates, usage limits per coupon, and minimum order amounts.
- **Admin Controls**: Dedicated administrative interface for managing the coupon lifecycle.

### 7. Refund Management

- **Refund Requests**: Customers can request refunds for order items with reasons and evidence images.
- **Refund Approval**: Sellers and admins can approve, reject, or process refunds.
- **Return Shipping**: Customers can mark approved refunds as shipped with tracking numbers.
- **Refund Tracking**: Complete refund lifecycle tracking from request to resolution.

### 8. Scalability and Performance

- **Asynchronous Processing**: Leverage Ktor's async capabilities for high performance.
- **Load Balancing**: Easily scale your application to accommodate increased traffic.

### 9. Security

- **JWT Tokens**: Implement JSON Web Tokens for secure authentication.
- **Refresh Tokens**: Secure token refresh with hashed storage and automatic revocation.
- **Rate Limiting**: Auth endpoints protected against brute-force attacks (5 req/10min).
- **Account Lockout**: Automatic 30-minute lockout after 5 failed login attempts.
- **Password Strength**: Enforced password complexity requirements (min 8 chars, mixed case, digit, special char).
- **Input Validation**: Protect against common web vulnerabilities like SQL injection and cross-site scripting (XSS).
- **Atomic Stock Operations**: Thread-safe inventory updates within database transactions.

### 10. Dashboard Analytics

- **Summary Statistics**: Quick overview of revenue, orders, users, products, and shops.
- **Revenue Analytics**: Detailed revenue breakdown with daily trends and average order value.
- **Order Statistics**: Order status distribution and recent order activity.
- **User Growth**: User registration trends with breakdown by role and daily signups.
- **Top Products**: Best-selling products ranked by sales volume and revenue.
- **Activity Feed**: Recent platform activity including orders and user registrations.

### 11. Audit Logging

- **Action Tracking**: Records every admin action with actor identity, action type, and target resource.
- **Rich Context**: Captures actor email, role, IP address, user agent, and outcome for full audit trail.
- **Filterable Queries**: Search audit logs by actor, action type, resource, or outcome.
- **Immutable Records**: Append-only log records that cannot be modified or deleted.

### 12. Code Quality & Static Analysis

- **Ktlint**: Automated Kotlin linting to ensure consistent code style.
- **Detekt**: Static code analysis for finding potential bugs and code smells.
- **Pre-commit Hooks**: Enforce quality standards before code is even committed.

## Architecture

<p align="center">
  </br>
  <img width="60%" height="60%" src="https://github.com/piashcse/ktor-E-Commerce/blob/master/screenshots/onion_architecture.png" />
</p>
<p align="center">
<b>Fig. Clean / Onion Architecture </b>
</p>

The project follows **Clean Architecture** with clear separation of concerns:

- **Route Layer** (`*Routes.kt`) — HTTP routing only, uses `by inject()` for dependency injection, delegates all logic to services/repositories
- **Service Layer** (`*Service.kt`) — Business logic orchestration, works with domain models and DTOs, zero Exposed/sql imports
- **Repository Lay