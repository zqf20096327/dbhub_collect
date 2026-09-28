<p align="center">
    <img src="art/header.png" alt="Laravel Reservation Banner" width="100%">
</p>

# Laravel Reservation

[![Latest Version on Packagist](https://img.shields.io/packagist/v/zaber-dev/laravel-reservation.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-reservation)
[![Run Tests](https://img.shields.io/github/actions/workflow/status/zaber-dev/laravel-reservation/run-tests.yml?branch=main&label=tests&style=flat-square)](https://github.com/zaber-dev/laravel-reservation/actions/workflows/run-tests.yml)
[![Total Downloads](https://img.shields.io/packagist/dt/zaber-dev/laravel-reservation.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-reservation)
[![PHP Version Require](https://img.shields.io/packagist/dependency-v/zaber-dev/laravel-reservation/php.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-reservation)
[![License](https://img.shields.io/packagist/l/zaber-dev/laravel-reservation.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-reservation)

**Supports:** Laravel 11, 12 & 13+ • PHP 8.2+ • Redis • Memcached • Database

**Application-level resource reservation for Laravel.**
Temporarily hold resources, manage reservation lifecycles, and prevent double-bookings with cache or database storage.

Manage reservations with a clean, expressive API using cache or persistent database storage, attach them directly to Eloquent models, protect routes with declarative middleware, and extend the package with custom storage backends.

> Unlike `Cache::lock()`, which provides short-lived mutual exclusion, Laravel Reservation manages complete reservation lifecycles—from temporary holds to confirmation, cancellation, and expiration.

```text
Available
    │
    ▼
 Held (15 min)
    │
 ┌──┴─────────────┐
 ▼                ▼
Confirmed     Cancelled
    │
    ▼
Completed

or after timeout

Held ─────► Expired
```

---

## Quick Example

```php
Reservation::for('seat_A12')
    ->heldBy($user)
    ->forMinutes(15)
    ->hold();

// Process payment...

Reservation::for('seat_A12')->confirm();
```
---

## Documentation

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Agentic Development with Laravel Boost](#agentic-development-with-laravel-boost)
- [LEARN.md](LEARN.md)

---

## Common Use Cases

Laravel Reservation is ideal for:

- Ticket & seat reservations
- E-commerce inventory reservation while payment processes
- Hotel room and appointment slot bookings
- Limited edition product release drops
- Cloud resource or sandbox instance provisioning
- Equipment rentals
- Time-bounded coupon or discount reservation

---

## Why not `Cache::lock()`?

Laravel's `Cache::lock()` is excellent for preventing concurrent execution within a request.

Laravel Reservation solves a different problem. It models **resource availability**, not just concurrency.

It manages **stateful resource reservations** that survive beyond a single request and follow a complete booking lifecycle.

Typical examples include:

* Seat reservations
* Hotel bookings
* Inventory holds
* Appointment scheduling
* Checkout reservations

where a resource may remain temporarily held for several minutes before eventually being confirmed or released.

| Feature | Cache::lock() | Laravel Reservation |
| :--- | :---: | :---: |
| **Primary Purpose** | Low-level atomic mutex | **Stateful resource holds & booking lifecycles** |
| **Fluent Builder API** (`Reservation::for()->hold()`) | ❌ Manual | ✅ **Expressive & Clean** |
| **First-Class Eloquent Integration** (`$seat->reserve()`) | ❌ | ✅ **Native (`HasReservations`)** |
| **Driver-Based Architecture** (`cache` & `database`) | ❌ Cache Only | ✅ **Both Supported** |
| **Multi-Step Lifecycle Tracking** (`held`/`confirmed`) | ❌ | ✅ **Built-in (`held`, `confirmed`, `cancelled`)** |
| **Success-Only / Auto-Cancel Route Middleware** | ❌ | ✅ **Built-in (`ReserveResource`)** |
| **Immutable DTOs (`ReservationInfo`)** | ❌ | ✅ **Strict (`CarbonImmutable`)** |
| **Automatic Database Pruning** (`model:prune`) | N/A | ✅ **Built-in (`Prunable`)** |
| **Polymorphic Target Scoping** | ❌ Manual Keys | ✅ **Automatic Key Mapping** |
| **Custom Driver Extensibility** (`Reservation::extend()`) | ❌ | ✅ **Closure / Container** |
| **Event Dispatching** (`ReservationHeld` / `Confirmed`) | ❌ | ✅ **Configurable Events** |

---

## Features

- **Stateful reservation lifecycle**: Strictly enforce valid reservation lifecycles (`held` ➔ `confirmed` or `cancelled`), preventing confirmed bookings from expiring or expiring reservations from confirming.
- **Atomic concurrency protection**: Prevent double-booking race conditions during high-traffic ticket or inventory drops.
- **Expressive API**: Chain expressive calls like `Reservation::for('room_101')->using('database')->heldBy($user)->forMinutes(30)->hold()`.
- **Automatic expiration**: Schedule holds to expire at precise times or minute durations.
- **Eloquent integration**: Attach the `HasReservations` trait to any resource or user model for scoped hold management.
- **Middleware**: Protect booking and checkout endpoints automatically using `reserve:resource_key,minutes` with automatic HTTP `429` enforcement.
- **Storage backends**: Switch seamlessly between high-performance `cache` stores (Redis, Memcached, Array) and persistent `database` storage with automatic state tracking.
- **DTOs**: Work safely with strict `ReservationInfo` Data Transfer Objects returning precision status metadata (`status`, `holder`, `expiresAt`, `isExpired()`).
- **Extensibility**: Register custom storage drivers on the fly with closure-based creators via `Reservation::extend()`.
- **Prunable storage**: Built-in `Prunable` trait integration ensures historical `cancelled` and `expired` reservation records never clutter your database.

---

## Installation

Ready to get started? Install the package with Composer:

```bash
composer require zaber-dev/laravel-reservation
```

Publish the configuration and database migrations:

```bash
php artisan vendor:publish --provider="ZaberDev\Reservation\ReservationServiceProvider"
```

Run migrations if you intend to use the `database` driver:

```bash
php artisan migrate
```

---

## Configuration

The configuration file `config/reservations.php` allows you to define your default storage driver, driver parameters, and event dispatching behaviors:

```php
return [
    /*
    |--------------------------------------------------------------------------
    | Default Storage Backend
    |--------------------------------------------------------------------------
    |
    | Supported drivers: "cache", "database"
    |
    */
    'default' => env('RESERVATION_DRIVER', 'cache'),

    'drivers' => [
        'cache' => [
            'driver' => 'cache',
            'store' => env('RESERVATION_CACHE_STORE', null),
            'prefix' => 'reservations:',
        ],
        'database' => [
            'driver' => 'database',
            'table' => 'reservations',
        ],
    ],

    'events' => [
        'dispatch' => true,
    ],
];
```

---

## Usage Guide

### 1. The Fluent Reservation API

The `Reservation` facade provides an expressive builder interface for holding, confirming, cancelling, and inspecting reservations.

#### Holding & Confirming a Resource
```php
use ZaberDev\Reservation\Facades\Reservation;

// 1. Place a temporary hold
$builder = Reservation::for('seat_A12')
    ->heldBy($user)
    ->forMinutes(15);

if ($builder->hold()) {
    // Hold placed successfully, present payment form...
} else {
    // Resource is currently held or already confirmed by another customer
}

// 2. Confirm the reservation once payment completes
if (Reservation::for('seat_A12')->confirm()) {
    // Reservation is now permanently confirmed!
}
```

#### Cancelling a Hold
If the customer aborts checkout or payment fails:

```php
Reservation::for('seat_A12')->cancel();
```

#### Inspecting Status
```php
$info = Reservation::for('seat_A12')->info(); // ReservationInfo DTO

if ($info->isHeld()) {
    echo "Resource is reserved by " . $info->holder . " until " . $info->expiresAt->toDateTimeString();
} elseif ($info->isConfirmed()) {
    echo "Resource is permanently booked.";
} elseif ($info->isExpired() || $info->isCancelled()) {
    echo "Resource is available.";
}
```

---

### 2. Eloquent Model Integration (`HasReservations`)

Add the `HasReservations` trait to any resource Eloquent model (such as `Seat`, `Room`, or `InventoryItem`) to manage reservations directly off the entity:

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use ZaberDev\Reservation\HasReservations;

class Seat extends Model
{
    use HasReservations;
}
```

You can now interact directly with your model instance:

```php
$seat = Seat::find(1);

// Reserve this seat for the user for 20 minutes
if ($seat->reserve()->heldBy($user)->forMinutes(20)->hold()) {
    return response()->json(['message' => 'Seat held!']);
}

// Confirm booking
$seat->reserve()->confirm();

// Cancel hold
$seat->reserve()->cancel();
```

#### Polymorphic Database Querying
When using the `database` driver, `HasReservations` also exposes a `reservations()` polymorphic relationship, allowing direct querying and bulk management:

```php
// Get all database reservation records for this seat
$history = $seat->reservations()->orderBy('created_at', 'desc')->get();
```

---

### 3. Route Middleware

Protect booking endpoints declaratively without writing boilerplate checks in your controllers using the `ReserveResource` middleware:

```php
use Illuminate\Support\Facades\Route;

// Enforce that "seat_A12" (or dynamic route parameter) is held during checkout submission
Route::post('/checkout/submit', [CheckoutController::class, 'submit'])
    ->middleware('reserve:seat_id,15');
```

**How the Middleware Works:**
- Before executing your controller, `ReserveResource` checks if the resource is currently held by someone else (`HTTP 429` if unavailable).
- If available, it places a temporary hold (`held`) for the duration.
- When your controller completes successfully (`2xx` or `3xx`), the reservation remains active until it is confirmed, cancelled, or expires. If the controller fails (`4xx` validation error or `5xx` server error), the temporary hold is automatically cancelled (`cancel()`) so the resource returns immediately to the available pool.

---

### 4. Working with Storage Backends (`using` & `driver`)

By default, the package uses the storage backend configured in `config/reservations.php`. You can switch storage backends on the fly per request or action:

```php
// Store transient shopping cart holds in fast cache/Redis
Reservation::for('cart_item_99')->using('cache')->heldBy($user)->forMinutes(30)->hold();

// Store high-value hotel booking holds inside SQL database with row locks
Reservation::for('penthouse_suite')->using('database')->heldBy($user)->forMinutes(60)->hold();
```

#### Registering Custom Storage Backends
You can extend the `ReservationManager` with your own storage backends (e.g., DynamoDB, MongoDB) in your `AppServiceProvider`:

```php
use ZaberDev\Reservation\Contracts\ReservationDriverContract;
use ZaberDev\Reservation\Facades\Reservation;

public function boot(): void
{
    Reservation::extend('dynamodb', function ($app) {
        return new MyDynamoDbReservationDriver($app['config']['reservations.drivers.dynamodb']);
    });
}
```

---

### 5. Database Pruning (`Prunable`)

When using the `database` driver, expired or cancelled records (`status in ('cancelled', 'expired')`) are automatically marked for pruning via Laravel's `Prunable` trait on the `ZaberDev\Reservation\Models\ReservationModel` model.

To clean up old records automatically, schedule Laravel's `model:prune` command in your `console.php` or `Kernel.php`:

```php
use Illuminate\Support\Facades\Schedule;
use ZaberDev\Reservation\Models\ReservationModel;

Schedule::command('model:prune', ['--model' => ReservationModel::class])->daily();
```

---

### 6. Events

Whenever a reservation changes state, the package dispatches strongly typed events if enabled (`reservations.events.dispatch = true`):

- **`ZaberDev\Reservation\Events\ReservationHeld`**: Dispatched when `hold()` succeeds (`$key`, `$holder`, `$expiresAt`, `$info`).
- **`ZaberDev\Reservation\Events\ReservationConfirmed`**: Dispatched when `confirm()` transitions a hold to confirmed (`$key`, `$info`).
- **`ZaberDev\Reservation\Events\ReservationCancelled`**: Dispatched when `cancel()` releases a hold (`$key`, `$info`).
- **`ZaberDev\Reservation\Events\ReservationExpired`**: Dispatched when an expired hold is detected or reaped (`$key`).

You can listen to these in your `EventServiceProvider` for inventory metrics, webhook notifications, or customer emails.

---

## Agentic Development with Laravel Boost

**Laravel Reservation** includes built-in AI support and architectural skills engineered for [Laravel Boost](https://github.com/laravel/boost).

When using AI coding assistants (such as Cursor, Claude Code, or GitHub Copilot connected via the Boost MCP server), your AI agent can automatically load specialized design patterns and exact API rules for implementing stateful resource reservations, hold/confirm lifecycles, and inventory holds with our package.

### Automatic Skill Installation
When Laravel Boost (`laravel/boost`) is installed in your application, our package AI skill is **automatically discovered and published** during package installation and updates (`php artisan boost:install` or `php artisan boost:update`).

If you install `laravel-reservation` into an existing Boost-enabled project, our service provider also automatically synchronizes the skill directly into your `.ai/skills/laravel-reservation` directory on boot with zero configuration needed.

### Manual Skill Installation
If you prefer to install or update the AI skill manually, you can use any of the following commands:

```bash
# Using Laravel Boost
php artisan boost:add-skill zaber-dev/laravel-reservation

# Using Vendor Publish
php artisan vendor:publish --tag=reservations-skill
```

### What the AI Skill Teaches Your Assistant
By enabling our skill, your AI assistant will strictly follow package conventions, including:
- Modeling full booking lifecycles (`hold()` -> `confirm()` / `cancel()`) rather than treating reservations as short-lived mutexes.
- Applying `use ZaberDev\Reservation\HasReservations;` directly to Eloquent models (`$seat->reserve()->heldBy($user)->forMinutes(15)->hold()`).
- Selecting the proper storage driver (`cache` for fast volatile holds vs `database` for auditability, persistence, and reporting).
- Enforcing route middleware (`middleware('reservation:seat_{id},15')`) to guard booking actions against double-holds.
- Handling `ReservationConflictException` (`HTTP 409`) idiomatically when a requested resource is already held or confirmed.

---

## Related Packages

This package is part of the **[ZaberDev Laravel Ecosystem](https://github.com/zaber-dev/laravel-ecosystem)** (Laravel Productivity Toolkit) — a cohesive suite of high-level application primitives engineered for concurrency, state management, and resource allocation.

Explore the complete directory of packages, detailed use cases, and documentation in our **[Ecosystem Index Hub](https://github.com/zaber-dev/laravel-ecosystem/blob/main/PACKAGES.md)**.

---

## Testing & Quality

Run the comprehensive PHPUnit test suite locally:

```bash
composer test
```

---

## Contributing

Thank you for considering contributing! Please ensure any pull requests include thorough PHPUnit tests covering unit, feature, and driver integration scenarios.

---

## License

The MIT License (MIT). Please see [LICENSE.md](LICENSE.md) for more information.

---

<p align="center">
    <b>Built with ❤️ as part of the ZaberDev Laravel Ecosystem.</b>
</p>
