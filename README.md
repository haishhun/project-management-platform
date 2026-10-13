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


## Milestone 2 — Domain & Database 🚧

### User Model
- [x] User SQLAlchemy model
- [x] UUID primary key
- [x] Email and password hash fields
- [x] First name and last name fields
- [x] Account activation flag
- [x] Creation and update timestamps
- [x] Email uniqueness constraint

### User Repository
- [x] Create user
- [x] Get user by ID
- [x] Get user by email
- [x] Update user
- [x] Partial user updates
- [x] Delete user
- [x] Handle nonexistent users
- [x] Use flush() instead of commit()
- [x] Keep transaction management outside the repository

### User Service
- [x] User registration
- [x] Password hashing
- [x] Email normalization
- [x] Duplicate email detection
- [x] Profile updates
- [x] Partial profile updates
- [x] User deletion
- [x] Handle nonexistent users
- [x] Service-level transaction commits and rollbacks

### User Tests
- [x] Repository creation and lookup tests
- [x] Duplicate email creation test
- [x] Repository update tests
- [x] Repository deletion tests
- [x] Missing user tests
- [x] Service registration tests
- [x] Email normalization tests
- [x] Password hashing and verification tests
- [x] Duplicate email registration test
- [x] Duplicate email update test
- [x] Partial update tests
- [x] Transaction recovery test
- [ ] Add remaining repository edge-case tests
- [ ] Run and verify all tests

### Database & Migrations
- [x] Alembic configuration
- [ ] Verify User migration
- [ ] Verify migration history and database revision
- [ ] Test migrations against a fresh database
- [ ] Verify model metadata matches the database schema

### Project Model
- [ ] Define Project fields and business rules
- [ ] Implement Project SQLAlchemy model
- [ ] Add Project relationships
- [ ] Generate and review Project migration
- [ ] Add Project repository
- [ ] Add Project service where needed
- [ ] Add Project tests

### Project Membership
- [ ] Define ProjectMember model
- [ ] Define membership roles
- [ ] Implement User–Project relationship
- [ ] Add foreign keys and uniqueness constraints
- [ ] Define project ownership rules
- [ ] Define deletion behavior
- [ ] Generate and review migration
- [ ] Add membership tests

### Task Model
- [ ] Define Task fields and business rules
- [ ] Implement Task SQLAlchemy model
- [ ] Add Project relationship
- [ ] Define task statuses and priorities
- [ ] Define optional task assignee
- [ ] Add foreign keys and constraints
- [ ] Generate and review migration
- [ ] Add Task repository
- [ ] Add Task tests

### Quality & Documentation
- [ ] Run Pytest successfully
- [ ] Run Ruff linting
- [ ] Verify Ruff formatting
- [ ] Run MyPy successfully
- [ ] Verify GitHub Actions CI
- [ ] Update README with implemented functionality
- [ ] Complete and verify Milestone 2
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