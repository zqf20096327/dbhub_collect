# Campuslands MySQL

Repositorio publico de ejercicios de MySQL para estudiantes de Campuslands.

El objetivo es aprender bases de datos relacionales con MySQL de forma practica, progresiva y profesional: desde consultas y tablas basicas hasta funcionalidades propias como indices, transacciones, procedimientos, triggers, JSON y optimizacion.

## Estructura

```text
campuslands-mysql/
├── basico/              # 60 ejercicios
├── intermedio/          # 60 ejercicios
├── avanzado/            # 60 ejercicios
├── funcionalidades/     # 20 ejercicios sobre capacidades de MySQL
├── docs/
├── docker-compose.yml
├── .github/
├── CONTRIBUTING.md
└── FLUJO-DE-ENTREGA.md
```

Cada ejercicio tiene `README.md`, plantilla SQL y carpeta `resoluciones/`.

## Ramas principales

- `main`: estable/produccion. No recibe entregas directas de estudiantes.
- `dev`: integracion de ejercicios. Todo PR estudiantil debe apuntar a esta rama.

## Como entregar

1. Haz fork del repositorio.
2. Cambiate a `dev`.
3. Crea una rama personal.
4. Guarda tu solucion dentro del ejercicio correspondiente en `resoluciones/nombre-apellido/`.
5. Haz commit con mensaje claro.
6. Abre Pull Request hacia `dev`.

## Levantar MySQL con Docker

```bash
cp .env.example .env
docker compose up -d
```

Servicios locales:

- MySQL: `localhost:3307`
- Usuario: `campus`
- Password: `campus123`
- Base: `campuslands_mysql`
- phpMyAdmin: `http://localhost:8085`

## Reglas clave

- No abrir PR hacia `main`.
- No subir archivos fuera de la estructura.
- No modificar enunciados base.
- No borrar archivos base.
- No editar respuestas de otros estudiantes.
- No subir `.env`, dumps grandes, bases locales ni archivos temporales.
