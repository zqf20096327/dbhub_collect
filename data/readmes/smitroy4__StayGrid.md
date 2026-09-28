# StayGrid — Hotel Booking System

<p align="center">
  <img src="https://img.shields.io/badge/Java-21-orange?style=for-the-badge&logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Spring_Boot-4.x-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Stripe-Payment-635BFF?style=for-the-badge&logo=stripe&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-Deployed-0B0D0E?style=for-the-badge&logo=Render&logoColor=white" />
</p>

<p align="center">
  <b>A production-grade hotel booking backend built with Spring Boot, featuring dynamic pricing, real-time inventory management, and Stripe-powered payments.</b>
</p>

---

## Live Links

| Resource | URL |
|---|---|
| Frontend Application | [https://stay-grid.vercel.app](https://stay-grid.vercel.app) |
| Backend API (Render) | [https://staygrid-b02y.onrender.com/api/v1](https://staygrid-b02y.onrender.com/api/v1) |

---

## Overview

**StayGrid** is a full-featured hotel booking REST API designed to mirror the core functionality of platforms like MakeMyTrip or Booking.com. It handles the complete lifecycle of a hotel reservation — from hotel onboarding and room inventory management, to guest booking, Stripe Checkout-based payments, and automated refunds on cancellation.

The system is built around two primary user roles:

- **Hotel Manager (`HOTEL_MANAGER`)** — registers hotels, manages rooms, controls inventory availability, sets surge pricing, and views booking analytics.
- **Guest (`GUEST`)** — searches hotels, browses room availability with real-time pricing, initiates bookings, adds guests, and completes payment via Stripe.

Prices are not static. A **scheduled pricing engine** runs hourly and recalculates room prices across all active hotels using a **Decorator pattern chain** of four strategies — surge factor, occupancy rate, booking urgency, and holiday multiplier.

---

## Key Features

- **JWT Authentication** with access token (10-minute expiry) + refresh token (6-month expiry via HttpOnly cookie)
- **Role-based access control** — `GUEST` and `HOTEL_MANAGER` roles enforced at the security filter level
- **Dynamic pricing engine** — Decorator pattern chain applying surge, occupancy, urgency, and holiday multipliers on top of a base price
- **Pessimistic locking** on inventory rows during booking to prevent race conditions and double-bookings under concurrent load
- **Stripe Checkout integration** — generates hosted payment sessions; confirms bookings via signed webhook events
- **Automated refunds** — on booking cancellation, a Stripe refund is triggered programmatically against the original payment intent
- **Scheduled inventory price updates** — a Spring `@Scheduled` job runs every hour, recalculating prices for all hotels in paginated batches
- **`HotelMinPrice` table** — a denormalized price summary table updated by the scheduler to enable fast hotel search queries without scanning the full inventory
- **Paginated hotel search** — city + date range + room count search returns paginated results with average price per stay
- **Booking expiry** — bookings not completed within 10 minutes are treated as expired and cannot proceed to payment
- **Hotel analytics** — hotel managers can generate booking reports filtered by date range (total bookings, total revenue, average revenue)
- **Global response wrapper** — all API responses are uniformly wrapped in `ApiResponse<T>` with timestamp, data, and error fields
- **Global exception handler** — centralized `@RestControllerAdvice` mapping all exception types to appropriate HTTP status codes
- **Multi-stage Dockerfile** — Maven build stage + slim JRE runtime stage for optimized image size
- **Swagger/OpenAPI documentation** — all endpoints documented and explorable via Swagger UI

## AI Features

- AI-powered hotel recommendations via Gemini API

### AI Recommendation Workflow

The `POST /api/v1/ai/recommend` endpoint is **public** (permitAll) and generates hotel recommendations via the Gemini API.

1. **Request** — client sends `{"preferences": "budget hotel, near airport, good wifi"}`.
2. **Controller** (`AIController`) — forwards the preferences to `GeminiAIService`.
3. **Service** (`GeminiAIService`) — builds a `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}` via `RestTemplate`:
   - API key from env `GEMINI_API_KEY`; model from env `GEMINI_MODEL` (default `gemini-3.6-flash`) — so model retirements never require a code change.
4. **Prompt** — `"Given these user preferences: [...] recommend 3 best hotels with brief reasons."`
5. **Parse** — extracts `candidates[0].content.parts[0].text` from the Gemini response.
6. **Respond** — wrapped in `ApiResponse<String>` (`200`).
7. **Failure** — Gemini errors (bad key, deprecated model, outage) return `ApiResponse` with **502** instead of an unhandled crash.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Java 21 |
| Framework | Spring Boot 4.x |
| Security | Spring Security + JJWT |
| ORM | Spring Data JPA + Hibernate |
| Database | PostgreSQL (Neon — serverless) |
| Payments | Stripe Java SDK |
| Object Mapping | ModelMapper |
| API Docs | SpringDoc OpenAPI (Swagger UI) |
| Build Tool | Maven |
| Containerization | Docker (multi-stage build) |
| Deployment | Render |
| Frontend | React + Vite (deployed on Vercel) |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
│          React Frontend (Vercel)  /  Swagger UI / Postman       │
└─────────────────────┬───────────────────────────────────────────┘
                      │  HTTPS
┌─────────────────────▼───────────────────────────────────────────┐
│                    Spring Boot Application                       │
│                   (Render — Docker Container)                   │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │  Controllers │──▶│   Services   │──▶│    Repositories      │ │
│  │  (REST API)  │   │ (Biz Logic)  │   │  (Spring Data JPA)   │ │
│  └──────────────┘   └──────┬───────┘   └──────────┬───────────┘ │
│                            │                      │             │
│  ┌─────────────────────────▼──────────────────────▼───────────┐ │
│  │              Spring Security Filter Chain                   │ │
│  │          JWTAuthFilter → WebSecurityConfig                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────┐   ┌─────────────────────────────┐   │
│  │  PricingUpdateService │   │  GlobalExceptionHandler      │   │
│  │  (@Scheduled — 1hr)   │   │  GlobalResponseHandler       │   │
│  └───────────────────────┘   └─────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐  ┌──────▼──────┐  ┌───▼──────────┐
    │  PostgreSQL │  │   Stripe    │  │  Stripe      │
    │   (Neon)   │  │  Checkout   │  │  Webhooks    │
    └────────────┘  └─────────────┘  └──────────────┘
```

---

## Dynamic Pricing Engine

The pricing engine is one of the core technical highlights of StayGrid. It applies the **Decorator design pattern** to compose multiple pricing strategies on top of a base price.

### Strategy Chain

```
BasePricingStrategy
      ↓
SurgePricingStrategy       →  basePrice × surgeFactor (admin-configurable per room per date range)
      ↓
OccupancyPricingStrategy   →  +20% if occupancy rate > 80%
      ↓
UrgencyPricingStrategy     →  +15% if check-in date is within the next 7 days
      ↓
HolidayPricingStrategy     →  +25% if the date is a holiday
```

Each strategy wraps the previous one and delegates to it before applying its own multiplier. This makes it trivially easy to add, remove, or reorder pricing factors without modifying existing strategy classes — a textbook open/closed principle application.

### Scheduled Price Refresh

`PricingUpdateService` runs every hour via `@Scheduled(cron = "0 0 * * * *")`:

1. Fetches all hotels in batches of 100 using pagination.
2. For each hotel, recalculates prices for all inventory records from today to one year out.
3. Computes the minimum price per day across all room types.
4. Upserts those daily minimums into the `HotelMinPrice` table.

The `HotelMinPrice` table acts as a **materialized price summary**, allowing the hotel search query to run against a lightweight table rather than joining and aggregating the full inventory.

---

## Booking Lifecycle

A booking in StayGrid transitions through the following states:

```
RESERVED → GUESTS_ADDED → PAYMENT_PENDING → CONFIRMED
                                                ↓
                                           CANCELLED
```

| State | Description |
|---|---|
| `RESERVED` | Booking created; inventory rows pessimistically locked and `reservedCount` incremented. |
| `GUESTS_ADDED` | Guest IDs attached to the booking. |
| `PAYMENT_PENDING` | Stripe Checkout session created; booking associated with `paymentSessionId`. |
| `CONFIRMED` | Stripe webhook `checkout.session.completed` received; `reservedCount` decremented, `bookedCount` incremented. |
| `CANCELLED` | Booking cancelled by user; `bookedCount` decremented; Stripe refund triggered. |
| `EXPIRED` | Booking not completed within 10 minutes (enforced at service layer on every operation). |

### Concurrency Safety

When a booking is initiated, `InventoryRepository.findAndLockAvailableInventory()` applies `@Lock(LockModeType.PESSIMISTIC_WRITE)` on the relevant inventory rows. This ensures that concurrent booking requests for the same room and date range serialize correctly at the database level, preventing double-booking.

---

## Project Structure

```
src/main/java/com/smit/projects/stayGrid/
│
├── advice/                      # Global cross-cutting concerns
│   ├── ApiError.java            # Error response model
│   ├── ApiResponse.java         # Unified response wrapper
│   ├── GlobalExceptionHandler.java  # @RestControllerAdvice
│   └── GlobalResponseHandler.java   # ResponseBodyAdvice wrapper
│
├── config/                      # Spring configuration beans
│   ├── CorsConfig.java          # CORS mappings
│   ├── MapperConfig.java        # ModelMapper bean
│   └── StripeConfig.java        # Stripe SDK initialization
│
├── controller/                  # REST controllers
│   ├── AIController.java        # /ai — AI hotel recommendations
│   ├── AuthController.java      # /auth — signup, login, refresh
│   ├── HotelBrowseController.java   # /hotels — public search & info
│   ├── HotelController.java     # /admin/hotels — hotel CRUD + reports
│   ├── HotelBookingController.java  # /bookings — booking flow
│   ├── InventoryController.java # /admin/inventory — inventory management
│   ├── RoomAdminController.java # /admin/hotels/{id}/rooms — room CRUD
│   ├── UserController.java      # /users — profile & guest management
│   └── WebhookController.java   # /webhook/payment — Stripe events
│
├── dto/                         # Data Transfer Objects (23 DTOs)
│   ├── AIRecommendationRequest.java # /ai/recommend — user preferences
│
├── entity/                      # JPA entities
│   ├── enums/                   # BookingStatus, Gender, PaymentStatus, Role
│   ├── Booking.java
│   ├── Guest.java
│   ├── Hotel.java
│   ├── HotelContactInfo.java    # @Embeddable
│   ├── HotelMinPrice.java       # Denormalized price summary
│   ├── Inventory.java           # Per-room per-day availability + pricing
│   ├── Payment.java             # (stubbed — payment tracking via Stripe)
│   ├── Room.java
│   └── User.java                # Implements UserDetails
│
├── exception/                   # Custom exceptions
│   ├── ResourceNotFoundException.java
│   └── UnAuthorizedException.java
│
├── repository/                  # Spring Data JPA repositories (7)
│   └── InventoryRepository.java # Contains all critical JPQL queries
│
├── security/                    # Auth & JWT infrastructure
│   ├── AuthService.java
│   ├── JWTAuthFilter.java       # OncePerRequestFilter
│   ├── JWTService.java          # Token generation & parsing
│   └── WebSecurityConfig.java   # SecurityFilterChain
│
├── service/                     # Service interfaces + implementations
│   ├── impl/
│   │   ├── BookingServiceImpl.java
│   │   ├── CheckoutServiceImpl.java   # Stripe session creation
│   │   ├── GuestServiceImpl.java
│   │   ├── HotelServiceImpl.java
│   │   ├── InventoryServiceImpl.java
│   │   ├── RoomServiceImpl.java
│   │   └── UserServiceImpl.java
│   ├── GeminiAIService.java          # AI hotel recommendations via Gemini API
│   └── PricingUpdateService.java      # @Scheduled pricing job
│
├── strategy/                    # Decorator-based pricing engine
│   ├── PricingStrategy.java         # Interface
│   ├── BasePricingStrategy.java
│   ├── SurgePricingStrategy.java
│   ├── OccupancyPricingStrategy.java
│   ├── UrgencyPricingStrategy.java
│   ├── HolidayPricingStrategy.java
│   └── PricingService.java          # Composes the decorator chain
│
└── util/
    └── AppUtils.java            # getCurrentUser() from SecurityContext
```

---

## API Reference

All endpoints are prefixed with `/api/v1`. Full interactive documentation is available at the [Swagger UI](https://staygrid-b02y.onrender.com/api/v1/swagger-ui/index.html).

### Authentication — `/auth`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/auth/signup` | No | Register a new user account |
| `POST` | `/auth/login` | No | Login; returns `accessToken` in body + `refreshToken` in HttpOnly cookie |
| `POST` | `/auth/refresh` | Cookie | Issue a new access token using the refresh token cookie |

**Signup Request Body**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Login Response**
```json
{
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiJ9..."
  },
  "timeStamp": "2025-06-01T10:30:00"
}
```

---

### Hotel Browse (Public) — `/hotels`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/hotels/search` | No | Search hotels by city, date range, and room count |
| `POST` | `/hotels/{hotelId}/info` | No | Get hotel details and available rooms with pricing |

**Hotel Search Request Body**
```json
{
  "city": "Mumbai",
  "startDate": "2025-07-01",
  "endDate": "2025-07-05",
  "roomsCount": 2,
  "page": 0,
  "size": 10
}
```

---

### Booking Flow — `/bookings` *(Authenticated)*

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/bookings/init` | Initiate booking — reserves inventory and returns a `BookingDto` |
| `POST` | `/bookings/{bookingId}/addGuests` | Attach a list of guest IDs to the booking |
| `POST` | `/bookings/{bookingId}/payments` | Create a Stripe Checkout session; returns `sessionUrl` |
| `GET` | `/bookings/{bookingId}/status` | Poll current booking status |
| `POST` | `/bookings/{bookingId}/cancel` | Cancel a confirmed booking and trigger a Stripe refund |

**Booking Init Request Body**
```json
{
  "hotelId": 1,
  "roomId": 3,
  "checkInDate": "2025-07-01",
  "checkOutDate": "2025-07-05",
  "roomsCount": 2
}
```

---

### User Profile — `/users` *(Authenticated)*

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/profile` | Fetch the authenticated user's profile |
| `PATCH` | `/users/profile` | Update name, date of birth, gender |
| `GET` | `/users/myBookings` | List all bookings made by the authenticated user |
| `GET` | `/users/guests` | List all saved guests |
| `POST` | `/users/guests` | Add a new guest to the user's guest list |
| `PUT` | `/users/guests/{guestId}` | Update a guest |
| `DELETE` | `/users/guests/{guestId}` | Remove a guest |

---

### Admin — Hotel Management — `/admin/hotels` *(HOTEL_MANAGER role)*

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/hotels` | Create a new hotel (starts as inactive) |
| `GET` | `/admin/hotels` | Get all hotels owned by the authenticated manager |
| `GET` | `/admin/hotels/{hotelId}` | Get a specific hotel by ID |
| `PUT` | `/admin/hotels/{hotelId}` | Update hotel details |
| `DELETE` | `/admin/hotels/{hotelId}` | Delete hotel (cascades to rooms and inventory) |
| `PATCH` | `/admin/hotels/{hotelId}/activate` | Activate hotel; initializes 1-year inventory for all rooms |
| `GET` | `/admin/hotels/{hotelId}/bookings` | List all bookings for a hotel |
| `GET` | `/admin/hotels/{hotelId}/reports` | Revenue report with optional `startDate` / `endDate` query params |

---

### Admin — Room Management — `/admin/hotels/{hotelId}/rooms` *(HOTEL_MANAGER role)*

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/hotels/{hotelId}/rooms` | Add a room to a hotel |
| `GET` | `/admin/hotels/{hotelId}/rooms` | List all rooms in a hotel |
| `GET` | `/admin/hotels/{hotelId}/rooms/{roomId}` | Get a specific room |
| `PUT` | `/admin/hotels/{hotelId}/rooms/{roomId}` | Update room details |
| `DELETE` | `/admin/hotels/{hotelId}/rooms/{roomId}` | Delete room and its inventory |

---

### Admin — Inventory Management — `/admin/inventory` *(HOTEL_MANAGER role)*

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/inventory/rooms/{roomId}` | View full inventory calendar for a room |
| `PATCH` | `/admin/inventory/rooms/{roomId}` | Update surge factor or close availability for a date range |

**Update Inventory Request Body**
```json
{
  "startDate": "2025-12-20",
  "endDate": "2025-12-31",
  "surgeFactor": 1.50,
  "closed": false
}
```

---

### Webhook — `/webhook`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/webhook/payment` | Stripe webhook endpoint; validates `Stripe-Signature` header and processes `checkout.session.completed` events |

> This endpoint must be registered in your Stripe Dashboard as a webhook endpoint. It verifies the request signature before processing.

---

### Unified API Response Format

All responses (success and error) are wrapped in `ApiResponse<T>`:

**Success**
```json
{
  "timeStamp": "2025-06-01T10:30:00",
  "data": { ... },
  "error": null
}
```

**Error**
```json
{
  "timeStamp": "2025-06-01T10:30:00",
  "data": null,
  "error": {
    "status": "NOT_FOUND",
    "message": "Hotel not found with ID: 99",
    "subErrors": null
  }
}
```

---

## Database Design

### Core Entities and Relationships

```
app_user (User)
    │
    ├──< hotel (Hotel) — owner FK
    │       │
    │       ├──< room (Room)
    │       │       │
    │       │       └──< inventory (Inventory) — unique(hotel_id, room_id, date)
    │       │
    │       └──< hotel_min_price (HotelMinPrice) — one row per hotel per date
    │
    ├──< booking (Booking) — user FK
    │       │
    │       ├── hotel FK
    │       ├── room FK
    │       └──>< booking_guest (join table) ──< guest (Guest)
    │
    └──< guest (Guest) — user FK
```

### Key Design Decisions

**`Inventory` table** holds one row per room per date with `bookedCount`, `reservedCount`, `totalCount`, `surgeFactor`, and the computed `price`. The unique constraint on `(hotel_id, room_id, date)` prevents duplicate entries.

**`HotelMinPrice` table** is a denormalized cache updated hourly. It stores the cheapest room price for each hotel on each date, enabling the hotel search query to aggregate over this lightweight table instead of the full inventory, which can have thousands of rows per hotel.

**`Booking.paymentSessionId`** ties each booking directly to a Stripe Checkout Session ID, enabling the webhook handler to correlate incoming payment events with the correct booking record without any shared state.

---

## Security Model

### JWT Token Strategy

| Token | Validity | Storage | Purpose |
|---|---|---|---|
| Access Token | 10 minutes | Response body | Authenticate API requests via `Authorization: Bearer <token>` |
| Refresh Token | 6 months | HttpOnly Cookie | Silently obtain a new access token via `/auth/refresh` |

Tokens are signed with HMAC-SHA using a secret key from environment variables. The `JWTAuthFilter` extends `OncePerRequestFilter` — on each request it extracts the user ID from the token, loads the `User` entity, and populates the `SecurityContextHolder`.

### Endpoint Authorization Matrix

| Pattern | Access |
|---|---|
| `/admin/**` | `ROLE_HOTEL_MANAGER` only |
| `/bookings/**` | Any authenticated user |
| `/users/**` | Any authenticated user |
| All others | Public (no auth required) |

### Exception Routing

JWT exceptions thrown inside the filter chain (which sits outside `@ControllerAdvice` scope) are delegated to Spring's `HandlerExceptionResolver` via constructor injection. This ensures JWT errors still pass through `GlobalExceptionHandler` and return the standard `ApiResponse` error format rather than Spring's default error page.

---

## Getting Started

### Prerequisites

- Java 21+
- Maven 3.9+
- PostgreSQL database (or a [Neon](https://neon.tech) serverless PostgreSQL connection string)
- Stripe account with a secret key and webhook signing secret

### Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/smitroy4/StayGrid.git
cd StayGrid
```

**2. Configure environment variables**

Create `src/main/resources/application.properties` or set environment variables (see [Environment Variables](#-environment-variables) section).

```properties
spring.datasource.url=jdbc:postgresql://<host>/<dbname>
spring.datasource.username=<username>
spring.datasource.password=<password>
spring.jpa.hibernate.ddl-auto=update

jwt.jwtSecretKey=<your-256-bit-secret-key>

stripe.secret.key=sk_test_...
stripe.webhook.secret=whsec_...

frontend.url=https://stay-grid.vercel.app
```

**3. Build and run**

```bash
mvn clean install -DskipTests
mvn spring-boot:run
```

The application starts on `http://localhost:8080`. Swagger UI is available at `http://localhost:8080/api/v1/swagger-ui/index.html`.

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SPRING_DATASOURCE_URL` | PostgreSQL JDBC connection URL | `jdbc:postgresql://...neon.tech/stayGrid` |
| `SPRING_DATASOURCE_USERNAME` | Database username | `stayGrid_owner` |
| `SPRING_DATASOURCE_PASSWORD` | Database password | `*****` |
| `JWT_SECRET_KEY` | HMAC-SHA signing secret (min 256-bit) | `myVeryLongSecretKeyForJWTSigning...` |
| `STRIPE_SECRET_KEY` | Stripe secret key | `sk_live_...` or `sk_test_...` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook endpoint signing secret | `whsec_...` |
| `FRONTEND_URL` | Frontend base URL for Stripe redirect | `https://stay-grid.vercel.app` |
| `GEMINI_API_KEY` | Your Gemini API key from AI Studio | `AIza...` |
| `GEMINI_MODEL` | Gemini model for recommendations (defaults to `gemini-3.6-flash`) | `gemini-3.6-flash` |

---

## Docker Setup

The project includes a multi-stage `Dockerfile`:

- **Stage 1 (Builder):** Uses `maven:3.9.9-eclipse-temurin-21` to compile and package the JAR. Maven dependencies are cached in a separate layer (`mvn dependency:go-offline`) to avoid re-downloading on every source change.
- **Stage 2 (Runtime):** Uses `eclipse-temurin:21-jre` (slim JRE only) to run the packaged JAR.

**Build the image**

```bash
docker build -t staygrid:latest .
```

**Run the container**

```bash
docker run -p 8080:8080 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://... \
  -e SPRING_DATASOURCE_USERNAME=... \
  -e SPRING_DATASOURCE_PASSWORD=... \
  -e JWT_SECRET_KEY=... \
  -e STRIPE_SECRET_KEY=... \
  -e STRIPE_WEBHOOK_SECRET=... \
  -e FRONTEND_URL=https://stay-grid.vercel.app \
  staygrid:latest
```

---

## Deployment

The backend is deployed on **Render** using the included Dockerfile. The PostgreSQL database is hosted on **Neon** (serverless PostgreSQL with connection pooling).

**Stripe Webhook Setup**

For Stripe to reach the webhook endpoint in production, register the following URL in your Stripe Dashboard under **Developers → Webhooks**:

```
https://staygrid-b02y.onrender.com/api/v1/webhook/payment
```

Select the `checkout.session.completed` event. Copy the signing secret and set it as `STRIPE_WEBHOOK_SECRET` in your Render environment variables.

> For local testing with Stripe webhooks, use the [Stripe CLI](https://stripe.com/docs/stripe-cli):
> ```bash
> stripe listen --forward-to localhost:8080/api/v1/webhook/payment
> ```

---

## Author

**Smit Roy**
MCA Student · Associate Web Developer → Aspiring Java Backend Developer

- GitHub: [@smitroy4](https://github.com/smitroy4)
- Portfolio: [smitroy.com](https://smitroy.com)
- LinkedIn: [linkedin.com/in/smitroy](https://linkedin.com/in/smitroy)

---

## License

This project is open source and available under the [MIT License](LICENSE).
