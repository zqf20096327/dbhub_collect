 <div align="center">

# 🦁 Riget Zoo Adventures

[![PHP](https://img.shields.io/badge/PHP-8.4%2B-777BB4.svg?style=for-the-badge\&logo=php\&logoColor=white)](https://www.php.net/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1.svg?style=for-the-badge\&logo=mysql\&logoColor=white)](https://www.mysql.com/)
[![Stripe](https://img.shields.io/badge/Stripe-Payments-635BFF.svg?style=for-the-badge\&logo=stripe\&logoColor=white)](https://stripe.com/)
[![Composer](https://img.shields.io/badge/Composer-Dependencies-885630.svg?style=for-the-badge\&logo=composer\&logoColor=white)](https://getcomposer.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

https://github.com/user-attachments/assets/d6c7d951-cfd1-42a1-8d10-4c40749492b1

</div>

## 📖 Overview

Riget Zoo Adventures is a PHP-based zoo booking and accommodation management system. It uses a custom MVC architecture, Eloquent ORM, and a dependency injection container to separate request handling, business logic, and data access.

The application allows users to register, browse tickets and accommodation options, manage a shopping cart, complete bookings through Stripe, and access their order history and reward points.

The project follows a service-oriented architecture, with dedicated services for authentication, booking, checkout, payments, notifications, and other application functionality.

### 🏗️ Architecture Overview

- **MVC pattern** — Controllers handle HTTP requests, Models manage data via Eloquent ORM, and Views render PHP templates.
- **Repository pattern** — `src/Repositories/` provides interfaces (`AccommodationRepository`, `OrderRepository`, etc.) with Eloquent implementations to decouple business logic from database access.
- **Dependency injection** — `src/Bootstrap/Container.php` registers and injects services (`BookingService`, `AuthService`, `TicketInventory`, etc.) into controllers and middleware.
- **Service layer** — `src/Services/` encapsulates business logic (booking, checkout, payments, notifications) independent of routing and data access.

### 🔒 Security Practices

- **Passwords** — Hashed with `password_hash()` using `PASSWORD_DEFAULT` (bcrypt), verified with `password_verify()`.
- **CSRF** — `CSRFMiddleware` validates tokens on state-changing requests.
- **Session regeneration** — Sessions are regenerated on login and logout (`session_regenerate_id()`).
- **Protected routes** — `AuthMiddleware` checks authentication before allowing access to checkout, profile, and order endpoints.
- **Webhook replay guard** — `PaymentWebhookHandler` uses a `processed` array with `md5` fingerprints to prevent replay attacks.

## ✨ Features

* User authentication with bcrypt password hashing (`PASSWORD_DEFAULT`) and session management
* CSRF protection (`CSRFMiddleware`) and session regeneration on login
* Role-aware authentication (`AuthMiddleware`) and protected routes
* Ticket booking with standard and premium ticket categories
* Accommodation reservations with availability and date-overlap checking
* Session-based shopping cart with ticket and accommodation support
* Stripe payments using the Payment Intent API
* Stripe webhook handling for payment success and failure events
* Transaction-safe order creation using database transactions
* Order management with ticket and accommodation order items
* Reward points awarded for qualifying purchases
* Custom exception handling with dedicated 404 and 500 error pages
* Centralised application logging and error handling
* Dependency injection and service-based business logic
* Environment-based configuration using PHP dotenv

## 🗂️ Project Structure

| Folder                       | Description                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| `public`                     | Web root, front controller, public assets, and entry point                          |
| `src/Bootstrap`              | Application bootstrapping and dependency injection container                        |
| `src/Cart`                   | Shopping cart entities and session store                                            |
| `src/Controllers`            | HTTP request handlers and application endpoints                                     |
| `src/Core`                   | Framework components: routing, sessions, validation, logging, views, and response handling |
| `src/DTOs`                   | Data transfer objects for request payloads                                          |
| `src/Enums`                  | Shared enumerations (order status, ticket type, item type)                          |
| `src/Exceptions`             | Custom exception classes and application error handling                             |
| `src/Middleware`             | HTTP middleware (authentication, CSRF)                                              |
| `src/Models`                 | Eloquent ORM models and database relationships                                      |
| `src/Payments`               | Payment gateway abstractions and Stripe integration                                 |
| `src/Repositories`           | Data access layer with Eloquent and query repositories                              |
| `src/Requests`               | Form request validation classes                                                     |
| `src/Services`               | Business logic for authentication, booking, checkout, payments, and notifications   |
| `src/Support`                | Shared helpers and message utilities                                                |
| `src/Views`                  | PHP templates and error pages                                                       |
| `database/migrations`        | Database schema migrations                                                          |
| `database/seeders`           | Database seeders and development data                                               |
| `config`                     | Application and database configuration                                              |
| `storage/logs`               | Application logs                                                                    |
| `plans`                      | Development plans and project documentation                                         |
| `.github`                    | GitHub configuration and project workflows                                          |

## 🛠️ Technologies Used

* PHP 8.2+
* Eloquent ORM (`illuminate/database` ^11)
* MySQL / MariaDB
* Stripe PHP SDK (`stripe/stripe-php` ^19)
* Composer for dependency management and PSR-4 autoloading
* PHP dotenv (`vlucas/phpdotenv`) for environment configuration
* Bootstrap 5 for the user interface
* Custom MVC framework with a regex-based router
* Dependency injection container for application services
* PHP-CS-Fixer for code formatting
* PHPStan for static analysis
* PHPCS for coding standards checks

## ✅ Requirements

Before running the application, make sure you have these installed:

* PHP 8.2 or higher
* PHP `mbstring` extension
* MySQL or MariaDB
* Composer
* Stripe account for payment processing
* Stripe CLI for local webhook testing (optional)

## 📥 Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/SirRmelTheThird/RigetZooAdventures.git
cd RigetZooAdventures
```

Install dependencies:

```bash
composer install
```

This installs the application's dependencies, including Eloquent ORM, the Stripe PHP SDK, and environment configuration.

Copy the environment file:

```bash
cp .env.example .env
```

On Windows, you can also copy the file manually:

```powershell
Copy-Item .env.example .env
```

### 📋 Complete .env Variables

```env
# Application
APP_ENV=development|production
APP_DEBUG=true|false

# Database
DB_HOST=localhost
DB_NAME=riget_zoo_adventures
DB_USER=root
DB_PASSWORD=your_password
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci

# Stripe
STRIPE_SECRET_KEY=sk_test_...|sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_test_...|pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Discord Notifications
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Session / Security
SESSION_DRIVER=file
SESSION_LIFETIME=120
CSRF_TOKEN_LIFETIME=120
```

Edit `.env` with your settings:

```env
# Application Configuration
APP_ENV=development
APP_DEBUG=true

# Database Configuration
DB_HOST=localhost
DB_NAME=riget_zoo_adventures
DB_USER=root
DB_PASSWORD=your_password_here

# Stripe Configuration
# Obtain test keys from https://dashboard.stripe.com/test/apikeys
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Discord Notifications (if enabled)
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

Configure any additional environment variables required by `.env.example` and the application's configuration files.

Create the database:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE riget_zoo_adventures;
EXIT;
```

Run the database migrations:

```bash
php cli migrate
```

Seed the database with development data:

```bash
php cli db:seed
```

The migrations create the application's database tables, while the seeders populate the database with the sample data required for development and testing.

**Note:** Use `php cli migrate:fresh --seed` instead if you want to drop and recreate the database schema before seeding. This permanently deletes existing data.

## 🚀 Running the Project

Pick whichever start method is easiest:

| Option               | Command                           | Notes                               |
| -------------------- | --------------------------------- | ----------------------------------- |
| Batch File (Windows) | `start-server.bat`                | Starts `php -S localhost:8000 -t public`; press `Ctrl+C` to stop |
| PowerShell (Windows) | `./start-server.ps1`              | Same server; run from PowerShell terminal |
| Manual               | `php -S localhost:8000 -t public` | Starts PHP development server       |

Visit: **http://localhost:8000**

Keep the terminal window open while the server runs, and press `Ctrl+C` to stop it.

### Test Accounts

Use the accounts configured by the database seeders.

If your development seeders create sample accounts, check their configured credentials before logging in. Do not use development accounts or default passwords in production.

### Stripe Test Cards

Use Stripe's test card numbers when testing payments in test mode.

| Scenario                | Card Number           |
| ----------------------- | --------------------- |
| Successful payment      | `4242 4242 4242 4242` |
| Declined payment        | `4000 0000 0000 0002` |
| Requires authentication | `4000 0025 0000 3155` |

For the test cards above, use any future expiry date and any valid three-digit CVC.

These cards only work with Stripe test API keys.

## 📜 Development Commands

| Command                                                    | Description                                         |
| ---------------------------------------------------------- | --------------------------------------------------- |
| `composer install`                                         | Install project dependencies                        |
| `composer dump-autoload`                                   | Regenerate the Composer autoloader                  |
| `php cli migrate`                                          | Run database migrations                             |
| `php cli migrate:fresh`                                    | Drop and recreate the database schema               |
| `php cli migrate:fresh --seed`                             | Reset the database, run migrations, and seed data   |
| `php cli db:seed`                                          | Run database seeders                                |
| `php -S localhost:8000 -t public`                          | Start the development server                        |
| `stripe listen --forward-to localhost:8000/webhook/stripe` | Forward Stripe events to the local webhook endpoint |

### Code Quality

The project includes development tools for maintaining consistent and reliable code.

Run PHP-CS-Fixer:

```bash
vendor/bin/php-cs-fixer fix
```

Run PHPStan:

```bash
vendor/bin/phpstan analyse
```

Run PHPCS:

```bash
vendor/bin/phpcs
```

These tools help enforce coding standards, identify potential errors, and maintain code quality as the project evolves.

## 🧪 Testing

The project includes PHPUnit tests across unit, integration, and support fixtures. Tests cover authentication, cart operations, booking, checkout, payments, routing, repositories, services, and middleware.

Run the full test suite:

```bash
vendor/bin/phpunit
```

Or using the Composer script:

```bash
composer test
```

Test structure:

| Folder | Description |
| ------------------- | ----------------------------------------------------------------- |
| `tests/Unit` | Unit tests for controllers, core framework, requests, services, and cart models |
| `tests/Integration` | Integration tests for authentication, booking, orders, payments, and routing |
| `tests/Support` | Shared fixtures, fake gateways, and test helpers |

Manual end-to-end checklist (optional):

1. **Sign Up** → Register a new customer account.
2. **Authentication** → Log in, verify session regeneration, and log out.
3. **Browse** → View available tickets and accommodation options.
4. **Add to Cart** → Select ticket quantities and accommodation dates.
5. **Checkout** → Validate the cart and authenticate where required.
6. **Payment** → Create a Stripe Payment Intent and complete payment using a test card.
7. **Confirmation** → Verify the order, payment status, and reward points.
8. **Profile** → View order history and customer information.

Covers:

* **Authentication** — registration, login, logout, password verification, session management, and protected routes.
* **Security** — CSRF token validation, session regeneration, authentication middleware, and protected checkout endpoints.
* **Shopping Cart** — adding and removing ticket and accommodation items, validating quantities, and calculating totals.
* **Accommodation Availability** — preventing bookings for occupied dates and overlapping reservations.
* **Checkout** — validating cart contents and calculating authoritative prices before creating an order.
* **Payment Flow** — creating Stripe Payment Intents, processing successful and failed payments, and handling webhook events.
* **Order Management** — creating orders and order items within database transactions, ensuring failures roll back incomplete operations.
* **Reward Points** — verifying points are awarded correctly for qualifying purchases.
* **Error Handling** — invalid routes display a 404 page, unexpected errors are handled centrally, and application errors are logged.
* **Notifications** — checking notification handling for relevant order and payment events when notification integrations are configured.

## 🔄 Resetting the Database

If data gets into a bad state or before re-testing:

```bash
php cli migrate:fresh --seed
```

This resets the database schema and repopulates it with the configured development data.

**Warning:** This permanently deletes existing database records. Do not run this command against a production database.

## 🔗 Stripe Webhook Setup (optional for development)

Stripe webhooks allow the application to receive payment events from Stripe and process payment status updates.

### Local Development

1. Install the Stripe CLI from https://docs.stripe.com/stripe-cli.
2. Start the local PHP development server.
3. Authenticate the Stripe CLI with your Stripe account.
4. Forward Stripe events to the application's webhook endpoint.

Run:

```bash
stripe listen --forward-to localhost:8000/webhook/stripe
```

The Stripe CLI will display a webhook signing secret beginning with `whsec_`.

Copy this secret into your `.env` file:

```env
STRIPE_WEBHOOK_SECRET=whsec_...
```

Keep the Stripe CLI running while testing webhooks.

To start the Stripe webhook server and listen for events:

```bash
stripe listen --forward-to localhost:8000/webhook/stripe
```

This starts the webhook listener and forwards events to your local application.

### Production Webhook

1. Go to https://dashboard.stripe.com/webhooks.

2. Create a webhook endpoint.

3. Set the endpoint URL to:

   `https://yourdomain.com/webhook/stripe`

4. Subscribe to the following events:

   * `payment_intent.succeeded`
   * `payment_intent.payment_failed`

5. Copy the endpoint's signing secret into your production environment.

The webhook endpoint must be publicly accessible over HTTPS in production. Use the signing secret associated with the relevant endpoint, and never commit it to version control.

## 🖼️ About Images

The application uses image assets for the zoo, tickets, accommodation, and other sections of the website.

Place your image assets in:

```text
public/assets/images/
```

The application can use placeholder images where configured assets are unavailable.

Ensure image paths referenced by the views match the filenames and locations of the assets in the public directory.

Images should be optimised for web use to reduce loading times and improve the user experience.

## 🧯 Common Problems

### "php is not recognized"

Install PHP 8.2 or higher from:

https://www.php.net/downloads.php

After installation:

```powershell
php -v
```

If PHP is not recognised, add the PHP installation directory to your Windows `PATH` environment variable, then restart your terminal.

### "Composer not found"

Install Composer from:

https://getcomposer.org/download/

Verify the installation:

```bash
composer --version
```

### "Class 'Illuminate\Database\Capsule\Manager' not found"

Install the Composer dependencies:

```bash
composer install
```

If the autoloader is out of date, regenerate it:

```bash
composer dump-autoload
```

### "Access denied for user 'root'@'localhost'"

Check the database credentials in `.env`:

```env
DB_HOST=localhost
DB_NAME=riget_zoo_adventures
DB_USER=root
DB_PASSWORD=your_password_here
```

Make sure MySQL or MariaDB is running and that the database user has the required permissions.

### "Table doesn't exist"

Run the migrations:

```bash
php cli migrate
```

If the database needs to be completely recreated:

```bash
php cli migrate:fresh --seed
```

### "Stripe API key not configured"

Verify that the Stripe environment variables are configured correctly:

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

Make sure the Stripe secret key matches the intended Stripe environment.

Restart the development server after changing environment variables if necessary.

### Payment Fails Silently

1. Check `storage/logs/app.log` for application errors.
2. Verify the Stripe API keys and webhook signing secret.
3. Check the Stripe Dashboard for Payment Intent status.
4. Confirm the Stripe CLI is running when testing local webhooks.
5. Verify that the webhook URL matches the application's configured route.

Use Stripe's test mode when testing payments during development.

### Database Errors (general)

Make sure MySQL is running and your `.env` database credentials are correct.

Check that the database exists and migrations have been applied:

```bash
php cli migrate
```

### View Detailed Errors

For local development, set:

```env
APP_ENV=development
APP_DEBUG=true
```

Check the application logs for additional error details:

```text
storage/logs/app.log
```

