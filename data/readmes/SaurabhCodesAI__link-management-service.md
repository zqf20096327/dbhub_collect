# Link Management Service

A production-inspired backend service for creating, managing, resolving, and analyzing shareable links.

This project is built as a first serious backend engineering project.

The goal is not only to build a working service, but to learn how backend systems are designed, implemented, tested, debugged, documented, and explained.

## Current Status

Early backend foundation stage.

The project is intentionally starting simple before introducing databases, caching, background workers, Docker, and CI/CD.

## Learning Goals

- Understand backend request flow from client to response.
- Learn clean API, schema, service, and storage separation.
- Build features incrementally.
- Practice debugging one layer at a time.
- Grow the project from in-memory storage to a production-inspired backend service.

## Planned Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- Redis
- Celery
- Docker
- Pytest
- GitHub Actions

Technologies should be introduced only when they solve the next real project problem.

## Project Structure

```text
app/
  api/        HTTP routes
  core/       settings, logging, security, shared configuration
  db/         storage and database integration
  models/     database models when persistence is introduced
  schemas/    request and response validation
  services/   business logic
  utils/      small reusable helpers
  main.py     application entry point
```

## Local Development

Run the app from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

This command will work after the FastAPI application entry point is implemented.

## Documentation

- `AGENTS.md`: how AI agents should mentor and work in this repository
- `PROJECT_CONTEXT.md`: what the project is and why it exists
- `ENGINEERING_GUIDE.md`: architecture and engineering standards
- `ROADMAP.md`: learning milestones
- `KNOWN_CONCEPTS.md`: concept progression tracker
- `DECISIONS.md`: architecture decision log
- `LEARNING_JOURNAL.md`: short personal learning log
