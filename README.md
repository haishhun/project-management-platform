# Project Management Platform

A backend project-management platform built with Python and FastAPI, designed with production-oriented architecture, testing, database migrations, Docker, and CI/CD.

## Milestone 1 — Foundation ✅

### Completed

- [x] FastAPI application
- [x] Configuration management
- [x] PostgreSQL
- [x] SQLAlchemy 2.x
- [x] Database sessions and dependencies
- [x] Alembic migrations
- [x] Docker
- [x] Health checks
- [x] Logging
- [x] Exception handling
- [x] Automated tests
- [x] Ruff
- [x] MyPy
- [x] GitHub Actions CI
- [x] PostgreSQL integration in CI
- [x] Development workflow documentation
- [x] CI verified working

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Psycopg 3
- Alembic
- Pytest
- HTTPX
- Ruff
- MyPy
- Docker
- GitHub Actions
- uv

## Development

### Run with Docker

```bash
docker compose up --build
```

### Install dependencies

```bash
uv sync
```

### Run in background

```
docker compose up -d --build
```

### Stop Docker containers

```
docker compose down
```

### Check container status

```
docker compose ps
```

### Apply migrations

```
docker compose exec api alembic upgrade head
```

### Create a migration

```
docker compose exec api alembic revision --autogenerate -m "migration message"
```

### Run tests

```
uv run pytest -vvv
```

### Code quality

#### Ruff

```
uv run ruff check .
```

#### MyPy

```
uv run mypy app
```