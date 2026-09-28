<p align="center">
    <img src="art/header.png" alt="Laravel Lock Banner" width="100%">
</p>

# Laravel Lock

[![Latest Version on Packagist](https://img.shields.io/packagist/v/zaber-dev/laravel-lock.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-lock)
[![Run Tests](https://img.shields.io/github/actions/workflow/status/zaber-dev/laravel-lock/run-tests.yml?branch=main&label=tests&style=flat-square)](https://github.com/zaber-dev/laravel-lock/actions/workflows/run-tests.yml)
[![Total Downloads](https://img.shields.io/packagist/dt/zaber-dev/laravel-lock.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-lock)
[![PHP Version Require](https://img.shields.io/packagist/dependency-v/zaber-dev/laravel-lock/php.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-lock)
[![License](https://img.shields.io/packagist/l/zaber-dev/laravel-lock.svg?style=flat-square)](https://packagist.org/packages/zaber-dev/laravel-lock)

**Supports:** Laravel 11, 12 & 13+ • PHP 8.2+ • Redis • Memcached • Database

**Application-level distributed locking for Laravel.** Prevent race conditions and concurrent execution across actions, workflows, and endpoints with automatic owner detection and cleanup.

Manage locks using cache or persistent database storage, attach them to Eloquent models, protect routes with middleware, and automatically track ownership — all through a clean, expressive API.

> Unlike Laravel's low-level `Cache::lock()`, Laravel Lock elevates distributed locking into a first-class, entity-scoped application abstraction (`Lock::for(...)`) with owner detection and lifecycle events.

---

## Quick Example

```php
// Option 1: High-level atomic block execution (acquires lock + executes + auto-releases in finally)
Lock::for('billing_charge', $user)
    ->block(function () {
        // Critical section...
    });

// Option 2: Step-by-step acquisition and release with automatic owner detection
if (Lock::for('billing_charge', $user)
        ->ttl(60)
        ->acquire()) {
    try {
        // Do work...
    } finally {
        Lock::for('billing_charge', $user)->release();
    }
}
```
---

## Common Use Cases

Laravel Lock is ideal for:

- Preventing duplicate payment processing
- Serializing inventory allocation and order checkout pipelines
- Protecting high-concurrency webhook processing endpoints
- Ensuring single-instance background cron job execution
- Preventing race conditions during financial account balance transfers
- Coordinating distributed microservice operations
- Preventing simultaneous document edits

---

## Why not Cache::lock()?

Laravel's `Cache::lock()` is an excellent low-level primitive for atomic locking.

**Laravel Lock doesn't replace `Cache::lock()`**. Instead, it builds on the same concept while providing higher-level application primitives for common Laravel workflows. Laravel Lock focuses on application-level locking with:

- **Automatic owner resolution** (`user_id`, queue job ID, or request hash)
- **Eloquent model integration** (`$user->lock('billing_charge')->acquire()`)
- **Route middleware** (`lock:billing_charge,30`)
- **Interchangeable storage backends** (Cache & persistent Database)
- **Rich lifecycle events** (`LockAcquired`, `LockReleased`, `LockFailed`)
- **Immutable DTOs** (`LockInfo` with strict date math)
- **Polymorphic target resolution** (Models, strings, integers)
- **Automatic database pruning** (`model:prune`)
- **High-level fluent API** (`Lock::for('action', $target)->ttl(60)->acquire()`)

---

## Why Laravel Lock?

While `Cache::lock()` handles basic mutex acquisition, **Laravel Lock** is engineered for entity-scoped, application-level mutual exclusion across your entire Laravel ecosystem.

| Feature | Cache::lock() | Laravel Lock |
| :--- | :---: | :---: |
| **Primary Purpose** | Low-level atomic mutex | **Application-level distributed locking** |
| **High-Level Fluent API** (`Lock::for()->ttl()`) | ❌ Manual | ✅ **Expressive & Clean (`Lock::for()`)** |
| **Automatic Owner Resolution** | ❌ Manual Token | ✅ **Built-in (`user_id`, job, hash)** |
| **First-Class Eloquent Integration** (`$user->lock()`) | ❌ | ✅ **Native (`HasLocks`)** |
| **Persistent Database Storage** | ❌ Cache Only | ✅ **Both Cache & Database Supported** |
| **Success-Only / Auto-Release Route Middleware** | ❌ | ✅ **Built-in (`RequireLock`)** |
| **Polymorphic Target Scoping** | ❌ Manual Keys | ✅ **Automatic Key Mapping** |
| **Immutable DTOs (`LockInfo`)** | ❌ | ✅ **Strict (`CarbonImmutable`)** |
| **Automatic Database Pruning** (`model:prune`) | N/A | ✅ **Built-in (`Prunable`)** |
| **Custom Storage Extensibility** (`Lock::extend()`) | ❌ | ✅ **Closure / Container** |
| **Event Dispatching** (`LockAcquired` / `Released`) | ❌ | ✅ **Configurable Events** |

---

## Features

- **Automatic Owner Detection**: Generates and tracks unique ownership tokens automatically (`user_id`, job ID, or request hash) to ensure threads only release locks they actually own.
- **Expressive Fluent API**: Chain expressive calls like `Lock::for('process_payout', $user)->ttl(120)->acquire()`.
- **Native Eloquent Integration**: Attach the `HasLocks` trait to any model for scoped lock management (`$user->lock('billing_charge')->acquire()`).
- **Route Middleware**: Protect endpoints automatically using `lock:action_name,duration_in_seconds` with automatic HTTP `429` enforcement and `finally` auto-release cleanup.
- **Multiple Storage Backends** (Cache & Database): Choose lightweight fast cache stores (Redis, Memcached, Array) or persistent database-backed locks with automatic cleanup.
- **Immutable DTOs**: Work safely with strict `LockInfo` Data Transfer Objects returning precise metadata (`key`, `owner`, `expiresAt`, `isExpired()`).
- **Custom Storage Extensibility**: Register custom storage drivers on the fly with closure-based creators via `Lock::extend()`.
- **Prunable Database Storage**: Built-in `Prunable` trait integration ensures expired database lock records never clutter your database.

---

## Documentation

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [LEARN.md](LEARN.md)

---

## Installation

Ready to get started? Install the package with Composer:

```bash
composer require zaber-dev/laravel-lock
```

Publish the configuration and database migrations:

```bash
php artisan vendor:publish --provider="ZaberDev\Lock\LockServiceProvider"
```

Run migrations if you intend to use the `database` driver:

```bash
php artisan migrate
```

---

## Configuration

The configuration file `config/locks.php` allows you to define your default storage engine, driver parameters, and event dispatching behaviors:

```php
return [
    /*
    |--------------------------------------------------------------------------
    | Default Lock Driver
    |--------------------------------------------------------------------------
    |
    | Supported drivers: "cache", "database"
    |
    */
    'default' => env('LOCK_DRIVER', 'cache'),

    'drivers' => [
        'cache' => [
            'driver' => 'cache',
            'store' => env('LOCK_CACHE_STORE', null),
            'prefix' => 'locks:',
        ],
        'database' => [
            'driver' => 'database',
            'table' => 'locks',
        ],
    ],

    'events' => [
        'dispatch' => true,
    ],
];
```

---

## Usage Guide

### 1. The Fluent Lock API

The `Lock` facade provides an expressive builder interface for acquiring, checking, blocking, and releasing locks.

#### Acquiring & Checking a Lock
```php
use ZaberDev\Lock\Facades\Lock;

$builder = Lock::for('billing_charge', $user)
    ->ttl(60)
    ->owner('worker_abc'); // Optional: explicit override (defaults to automatic owner detection)

if ($builder->acquire()) {
    try {
        // Lock acquired, execute sensitive logic...
    } finally {
        $builder->release();
    }
} else {
    // Lock is currently held by someone else
}

// Check lock status
$isLocked = Lock::for('billing_charge', $user)->isLocked();
$info = Lock::for('billing_charge', $user)->info(); // LockInfo DTO
```

#### Atomic Block Execution (`block`)
For operations vulnerable to concurrent execution bursts, use the `block()` helper. `block()` automatically acquires the lock, executes your callback, and safely releases the lock inside a `try...finally` block:

```php
Lock::for('billing_charge', $user)->block(function () use ($stripeService, $user) {
    $stripeService->charge($user);
});
```

#### Force Releasing Locks
If an administrative or recovery script needs to clear a locked resource regardless of owner:

```php
Lock::for('billing_charge', $user)->forceRelease();
```

---

### 2. Eloquent Model Integration (`HasLocks`)

Add the `HasLocks` trait to any Eloquent model to scope locks directly to that entity:

```php
namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use ZaberDev\Lock\HasLocks;

class User extends Authenticatable
{
    use HasLocks;
}
```

You can now interact directly with your model instance:

```php
$user = User::find(1);

// Acquire a 60-second lock on "billing_charge" for this user
if ($user->lock('billing_charge')->ttl(60)->acquire()) {
    try {
        // Charge user...
    } finally {
        $user->lock('billing_charge')->release();
    }
}

// Check status
if ($user->lock('billing_charge')->isLocked()) {
    return response()->json(['message' => 'Action locked.'], 429);
}
```

#### Polymorphic Database Querying
When using the `database` driver, `HasLocks` also exposes a `locks()` polymorphic relationship, allowing direct querying and bulk management:

```php
// Get all database lock records assigned to this user
$activeLocks = $user->locks()->where('expires_at', '>', now())->get();

// Delete all lock records for this user
$user->locks()->delete();
```

---

### 3. Route Middleware

Protect routes declaratively without writing boilerplate checks in your controllers using the `RequireLock` middleware:

```php
use Illuminate\Support\Facades\Route;

// Enforce a 30-second lock on billing endpoints per User / IP address
Route::post('/billing/charge', [BillingController::class, 'charge'])
    ->middleware('lock:billing_charge,30');

// Use a specific storage engine
Route::post('/api/payout', [PayoutController::class, 'store'])
    ->middleware('lock:payout,60,database');
```

**How the Middleware Works:**
- Before executing your controller, `RequireLock` attempts to acquire a lock for the specified duration (`HTTP 429` if already locked).
- When your controller finishes executing (whether `2xx success`, `4xx validation error`, or `5xx exception`), the middleware automatically releases the lock in its `finally` block so subsequent requests can proceed without waiting for TTL expiration.

---

### 4. Working with Storage Backends (`using` & `driver`)

By default, the package uses the storage engine defined in `config/locks.php`. You can switch storage drivers on the fly per request or action:

```php
// Store transient mutex checks in fast cache/Redis
Lock::for('api_sync', $ip)->using('cache')->ttl(15)->acquire();

// Store critical transaction locks inside persistent database tables
Lock::for('account_transfer', $user)->using('database')->ttl(120)->acquire();
```

#### Registering Custom Storage Drivers
You can extend the `LockManager` with your own storage drivers (e.g., DynamoDB, Redis Cluster) in your `AppServiceProvider`:

```php
use ZaberDev\Lock\Contracts\LockDriverContract;
use ZaberDev\Lock\Facades\Lock;

public function boot(): void
{
    Lock::extend('redis-cluster', function ($app) {
        return new MyRedisClusterLockDriver($app['redis']);
    });
}
```

---

### 5. Database Pruning (`Prunable`)

When using the `database` driver, expired records are automatically marked for pruning via Laravel's `Prunable` trait on the `ZaberDev\Lock\Models\LockModel` model.

To clean up old records automatically, schedule Laravel's `model:prune` command in your `console.php` or `Kernel.php`:

```php
use Illuminate\Support\Facades\Schedule;
use ZaberDev\Lock\Models\LockModel;

Schedule::command('model:prune', ['--model' => LockModel::class])->daily();
```

---

### 6. Events

Whenever a lock is acquired, released, failed, or force-released, the package dispatches strongly typed events if enabled (`locks.events.dispatch = true`):

- **`ZaberDev\Lock\Events\LockAcquired`**: Dispatched when `acquire()` succeeds (`$key`, `$owner`, `$expiresAt`, `$info`).
- **`ZaberDev\Lock\Events\LockReleased`**: Dispatched when `release()` succeeds (`$key`, `$owner`).
- **`ZaberDev\Lock\Events\LockFailed`**: Dispatched when `acquire()` fails due to concurrent ownership (`$key`, `$owner`).
- **`ZaberDev\Lock\Events\LockForceReleased`**: Dispatched when `forceRelease()` clears a lock (`$key`).

You can listen to these in your `EventServiceProvider` for logging, monitoring, or alerting.

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
