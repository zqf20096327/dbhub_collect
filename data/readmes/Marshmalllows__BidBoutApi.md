# BidBout API — Backend Server

REST API backend for the [BidBout](https://bid-bout.vercel.app/) online auction platform. Built with ASP.NET Core 9 and MySQL, deployed via Docker on **Render**. Database is hosted on **TiDB Cloud** (serverless MySQL-compatible).

**Frontend repository:** https://github.com/Marshmalllows/BidBout

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Bidding System](#bidding-system)
- [Data Models](#data-models)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Docker](#docker)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | ASP.NET Core 9.0 |
| Language | C# (.NET 9) |
| ORM | Entity Framework Core 9 (Pomelo MySQL) |
| Database | MySQL 8.0 |
| Authentication | JWT Bearer + HTTP-only refresh token cookies |
| Password hashing | BCrypt.Net-Next |
| API docs | Swagger / Swashbuckle |
| Containerization | Docker (Linux, port 8080) |
| Hosting | Render (Docker deploy) |
| Database hosting | TiDB Cloud (serverless, MySQL-compatible) |

---

## Project Structure

```
BidBoutApi/
├── Controllers/
│   ├── AuthController.cs       # Login, register, token refresh
│   ├── BidsController.cs       # Place bids, set auto-bid
│   ├── CategoriesController.cs # List auction categories
│   ├── LotsController.cs       # CRUD for auction lots + image upload
│   ├── ReviewsController.cs    # Seller reviews (CRUD)
│   └── UserController.cs       # Get/update own profile
├── Data/
│   └── MyDbContext.cs          # EF Core DbContext
├── DTOs/
│   ├── BidRequest.cs / BidResponse.cs
│   ├── CategoryResponse.cs
│   ├── CreateProductRequest.cs
│   ├── CreateReviewRequest.cs / UpdateReviewRequest.cs
│   ├── ImageResponse.cs
│   ├── LoginRequest.cs / RegisterRequest.cs
│   ├── ProductResponse.cs
│   ├── ReviewResponse.cs
│   ├── SellerProfileResponse.cs
│   └── UpdateUserRequest.cs
├── Models/
│   ├── UserModel.cs            # Users table
│   ├── RefreshTokenModel.cs    # Refresh tokens (per device/browser/OS)
│   ├── CategoryModel.cs
│   ├── ProductModel.cs         # Auction lots
│   ├── ImageModel.cs           # Lot images (stored as binary)
│   ├── BidModel.cs             # Bid history
│   ├── AutoBidModel.cs         # Auto-bid limits per user per lot
│   └── ReviewModel.cs          # Seller reviews
├── Program.cs                  # Service registration, middleware pipeline
├── appsettings.json
└── BidBoutApi.csproj
```

---

## API Reference

All routes are prefixed with `/api`.

### Auth — `/api/auth`

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/auth/login` | No | Log in; returns JWT + sets refresh cookie |
| POST | `/auth/register` | No | Register; returns JWT + sets refresh cookie |
| POST | `/auth/refresh` | Cookie | Rotate refresh token; returns new JWT |

**Login / Register request body:**
```json
{
  "email": "user@example.com",
  "password": "secret",
  "deviceType": "desktop",
  "browser": "Chrome",
  "os": "Windows"
}
```

**Response:**
```json
{
  "token": "<jwt>",
  "user": { "id": 1, "email": "user@example.com" }
}
```

The refresh token is set as an HTTP-only `Secure; SameSite=None` cookie named `refreshToken`. One refresh token is stored per unique `(userId, deviceType, browser, os)` combination and rotated on every `/auth/refresh` call.

---

### Lots — `/api/lots`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/lots` | No | All non-deleted lots (thumbnail only) |
| GET | `/lots/{id}` | Optional | Full lot detail, bids, seller info |
| GET | `/lots/my` | JWT | Caller's own lots |
| POST | `/lots` | Cookie | Create lot with images (`multipart/form-data`) |
| PUT | `/lots/{id}` | JWT | Edit lot (only before auction starts) |
| DELETE | `/lots/{id}` | JWT | Soft-delete lot (only before auction ends) |

**Create / update fields (`multipart/form-data`):**

| Field | Type | Constraints |
|---|---|---|
| `title` | string | 1–100 chars |
| `categoryId` | int | must exist |
| `pickupPlace` | string | max 100 chars |
| `description` | string | optional |
| `startDate` | datetime | not in past, max 1 year ahead |
| `duration` | int | 1–30 days |
| `reservePrice` | int | ≥ 0 |
| `images` | files | 1–50 files, max 10 MB each |

`GET /lots/{id}` exposes `sellerEmail` and `sellerPhone` only to the auction winner or the lot owner after the auction ends.

---

### Bids — `/api/bids`

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/bids` | JWT | Place a manual bid |
| POST | `/bids/auto` | JWT | Set / update auto-bid limit |

**Request body:**
```json
{ "lotId": 42, "amount": 150 }
```

**Response:**
```json
{ "newPrice": 150 }
```

---

### Categories — `/api/categories`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/categories` | No | List all categories `[{ "id": 1, "name": "Electronics" }, ...]` |

---

### Reviews — `/api/reviews`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/reviews/user/{userId}` | No | Seller profile + all reviews |
| POST | `/reviews` | JWT | Leave a review (one per seller) |
| PUT | `/reviews/{id}` | JWT | Edit own review |
| DELETE | `/reviews/{id}` | JWT | Delete own review |

**Create review body:**
```json
{ "targetUserId": 5, "rating": 4, "comment": "Great seller!" }
```

---

### User — `/api/user`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/user/me` | JWT | Get own profile |
| PUT | `/user/me` | JWT | Update name, phone, region, city |

---

## Authentication Flow

```
Client                          Server
  |                                |
  |--- POST /auth/login ---------->|
  |<-- { token, user }  ---------  |  (+ Set-Cookie: refreshToken)
  |                                |
  |--- GET /lots/my                |
  |    Authorization: Bearer <jwt> |
  |<-- lots ---------------------- |
  |                                |
  |  (JWT expires)                 |
  |--- POST /auth/refresh -------> |  (cookie sent automatically)
  |<-- { token, user } ----------  |  (+ rotated cookie)
```

- **Access token:** short-lived JWT (configured via `JwtSettings:ExpiryMinutes`), signed with HMAC-SHA256.
- **Refresh token:** long-lived opaque GUID (configured via `JwtSettings:ExpiryDays`), stored in DB and sent as an HTTP-only cookie. Rotated on every refresh call.
- Refresh tokens are scoped per device/browser/OS — logging in from a new device creates a separate entry rather than invalidating existing sessions.

---

## Bidding System

The auto-bidding engine lives in `BidsController.ProcessBidding`. The minimum bid increment is **$10**.

**Manual bid** (`POST /bids`):
1. Validates the lot is active (started, not ended).
2. Rejects the bid if it does not exceed the current highest bid.
3. Records the bid, then runs the auto-bid resolution loop.

**Auto-bid setup** (`POST /bids/auto`):
1. Saves / updates the caller's max limit for the lot.
2. If the caller is not currently winning, immediately places an opening bid (current price + $10, or reserve price if no bids exist yet), capped at their max.
3. Runs the same auto-bid resolution loop.

**Auto-bid resolution loop** (runs after every bid):
- Finds the top competing auto-bid that can still outbid the current winner.
- Places a counter-bid at `currentPrice + $10`, capped at that defender's max limit.
- Repeats until no eligible defender exists.

---

## Data Models

| Model | Key Fields |
|---|---|
| `User` | Id, Email, PasswordHash, FirstName, LastName, Phone, Region, City |
| `RefreshToken` | Id, UserId, Token, ExpiresAt, DeviceType, Browser, Os |
| `Category` | Id, Name |
| `Product` | Id, Title, Description, PickupPlace, CategoryId, CreatorId, StartDate, EndDate, ReservePrice, Status (0=active, 1=deleted) |
| `Image` | Id, LotId, ImageData (binary) |
| `Bid` | Id, LotId, BidderId, Amount, CreatedAt |
| `AutoBid` | Id, LotId, UserId, MaxAmount |
| `Review` | Id, ReviewerId, TargetUserId, Rating, Comment, CreatedAt |

---

## Getting Started

### Prerequisites

- .NET 9 SDK
- MySQL 8.0 (local or remote)

### Configuration

Create `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=bidbout;User=root;Password=yourpassword;"
  },
  "JwtSettings": {
    "Key": "your-secret-key-min-32-chars",
    "Issuer": "BidBoutApi",
    "Audience": "BidBoutClient",
    "ExpiryMinutes": 15,
    "ExpiryDays": 30
  }
}
```

### Run locally

```bash
cd BidBoutApi
dotnet restore
dotnet run
```

The API starts at `https://localhost:7xxx` / `http://localhost:5xxx`. Swagger UI is available at `/swagger` in Development mode.

---

## Environment Variables

For production, supply these as environment variables or via a secrets manager:

| Variable | Description |
|---|---|
| `ConnectionStrings__DefaultConnection` | MySQL connection string |
| `JwtSettings__Key` | JWT signing secret (min 32 chars) |
| `JwtSettings__Issuer` | JWT issuer claim |
| `JwtSettings__Audience` | JWT audience claim |
| `JwtSettings__ExpiryMinutes` | Access token lifetime in minutes |
| `JwtSettings__ExpiryDays` | Refresh token lifetime in days |

---

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t bidbout-api .

# Run (inject config via env vars)
docker run -p 8080:8080 \
  -e ConnectionStrings__DefaultConnection="Server=host;Database=bidbout;User=root;Password=pw;" \
  -e JwtSettings__Key="your-secret-key-min-32-chars" \
  -e JwtSettings__Issuer="BidBoutApi" \
  -e JwtSettings__Audience="BidBoutClient" \
  -e JwtSettings__ExpiryMinutes="15" \
  -e JwtSettings__ExpiryDays="30" \
  bidbout-api
```

The container listens on port **8080** (`ASPNETCORE_HTTP_PORTS=8080`).

CORS is pre-configured to allow `http://localhost:5173`, `http://localhost:5174`, and `https://bid-bout.vercel.app`.

The production image is deployed to **Render** as a Docker web service. The database runs on **TiDB Cloud** (serverless), which is MySQL 8.0-compatible — no driver changes required beyond using a TiDB Cloud connection string in `DefaultConnection`.
