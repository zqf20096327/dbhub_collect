# NEYDA — Backend

Sistema de Gestión Clínica | API REST

**Stack:** Node.js · Express · mysql2 · TiDB Cloud (MySQL)
**Deploy:** Render
**Base URL:** `/neyda/*`

## Estructura

```
src/
  config/      → DB connection (TiDB Cloud SSL) + env validation
  routes/      → auth, pacientes, citas, consultas, dashboard
  controllers/ → lógica de negocio por módulo
  middlewares/ → auth JWT, roleGuard, rateLimiter
  models/      → queries SQL con mysql2 (sin ORM)
database/
  schema.sql   → DDL completo
  seed.sql     → datos iniciales (1 admin + 2 médicos)
```

## Setup local

```bash
npm install
cp .env.example .env
# Editar .env con credenciales de TiDB Cloud
node server.js
```

## Variables de entorno

Ver `.env.example`

## Ramas

- `main` → producción
- `dev`  → desarrollo activo
