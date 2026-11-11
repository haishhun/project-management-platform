# Project Management Platform

A backend-focused project management platform built with Python and FastAPI. The project emphasizes production-oriented backend engineering practices, clean architecture, database integrity, automated testing, and CI/CD.

The goal is to build a maintainable application that supports user authentication, project ownership, team collaboration, task management, and role-based access control.

## Architecture

The application follows a layered architecture:

```text
API Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
SQLAlchemy Models
    ↓
PostgreSQL
```

### Layer responsibilities

| Layer | Responsibility |
|---|---|
| API | HTTP endpoints, request validation, response serialization |
| Schemas | Pydantic request and response contracts |
| Services | Business logic, authorization, transaction management |
| Repositories | Database queries and persistence operations |
| Models | SQLAlchemy mappings, relationships, constraints |
| Database | Engine, sessions, and migrations |

### Architectural principles

- Synchronous SQLAlchemy 2.x sessions.
- Services own database transactions.
- Repositories use `flush()` instead of `commit()`.
- Alembic is the source of truth for database schema changes.
- Database constraints enforce data integrity.
- Business rules are enforced in the service layer.
- Tests use an isolated PostgreSQL database.
- Explicit typing and static analysis with MyPy.

---

# Development Progress

## Milestone 1 — Foundation ✅

### Application Foundation

- [x] FastAPI application setup
- [x] Project configuration management
- [x] PostgreSQL integration
- [x] SQLAlchemy 2.x configuration
- [x] Database engine and session management
- [x] Dependency injection for database sessions
- [x] Alembic configuration
- [x] Docker configuration
- [x] Docker Compose
- [x] Health check endpoints
- [x] Logging configuration
- [x] Exception handling

### Development Infrastructure

- [x] Dependency management with uv
- [x] Pytest configuration
- [x] Ruff linting
- [x] Ruff formatting
- [x] MyPy static type checking
- [x] GitHub Actions CI workflow
- [x] PostgreSQL service in CI
- [x] Automated database migrations in CI
- [x] Automated test execution in CI
- [x] Development workflow documentation
- [x] CI pipeline verified working

## Milestone 2 — Domain & Database ✅

### User Model

- [x] User SQLAlchemy model
- [x] UUID primary key
- [x] Email field with unique constraint
- [x] Password hash field
- [x] First name and last name
- [x] Account activation flag
- [x] Creation and update timestamps
- [x] ORM relationships

### User Repository

- [x] Create user
- [x] Get user by ID
- [x] Get user by email
- [x] Update user
- [x] Partial user updates
- [x] Delete user
- [x] Handle nonexistent users
- [x] Use `flush()` instead of `commit()`
- [x] Keep transaction management outside the repository

### User Service

- [x] User registration
- [x] Password hashing
- [x] Password verification
- [x] Email normalization
- [x] Duplicate email detection
- [x] Profile updates
- [x] Partial profile updates
- [x] User deletion
- [x] Handle nonexistent users
- [x] Service-level transaction commits and rollbacks

### Project Model

- [x] Project SQLAlchemy model
- [x] UUID primary key
- [x] Project name
- [x] Optional project description
- [x] Creation and update timestamps
- [x] ORM relationships
- [x] Foreign key relationships

### Project Repository

- [x] Create project
- [x] Get project by ID
- [x] Get all projects
- [x] Pagination with limit and offset
- [x] Update project
- [x] Partial project updates
- [x] Delete project
- [x] Handle nonexistent projects
- [x] Use `flush()` instead of `commit()`

### Project Membership

- [x] ProjectMember SQLAlchemy model
- [x] Composite primary key `(project_id, user_id)`
- [x] User foreign key
- [x] Project foreign key
- [x] Project role enumeration
- [x] OWNER role
- [x] MEMBER role
- [x] Joined timestamp
- [x] Unique membership enforced by composite primary key
- [x] Index on user ID
- [x] ORM relationships
- [x] Database deletion behavior

### Project Member Repository

- [x] Create membership
- [x] Get membership by project and user
- [x] Get all project memberships
- [x] Update membership role
- [x] Delete membership
- [x] Handle nonexistent memberships
- [x] Prevent duplicate memberships through database constraints
- [x] Use `flush()` instead of `commit()`

### Task Model

- [x] Task SQLAlchemy model
- [x] UUID primary key
- [x] Project foreign key
- [x] Task title
- [x] Optional task description
- [x] Task status enumeration
- [x] Task priority enumeration
- [x] Task creator relationship
- [x] Optional task assignee
- [x] Optional due date
- [x] Creation and update timestamps
- [x] ORM relationships
- [x] Explicit foreign key configuration for creator and assignee
- [x] Database constraints
- [x] Indexes on project ID and assignee ID

### Task Repository

- [x] Create task
- [x] Get task by ID
- [x] Get all tasks by project
- [x] Chronological task ordering
- [x] Update task
- [x] Partial task updates
- [x] Delete task
- [x] Handle nonexistent tasks
- [x] Support explicitly clearing nullable fields
- [x] Implement UNSET sentinel for partial updates
- [x] Use `flush()` instead of `commit()`

### ORM Relationship Tests

- [x] User → ProjectMember relationships
- [x] Project → ProjectMember relationships
- [x] ProjectMember → User relationship
- [x] ProjectMember → Project relationship
- [x] User → created tasks
- [x] User → assigned tasks
- [x] Project → tasks
- [x] Task → Project
- [x] Task → creator
- [x] Task → assignee

### Database & Migrations

- [x] Alembic configuration
- [x] Initial database migrations
- [x] Model migrations
- [x] Migration history verification
- [x] Database revision verification
- [x] Fresh database migration test
- [x] Model metadata synchronization check
- [x] Verify no unnecessary migrations for ORM-only relationship changes

### Testing & Code Quality

- [x] Repository tests
- [x] User service tests
- [x] Model relationship tests
- [x] Database integration tests
- [x] Test database isolation
- [x] Test transaction rollback
- [x] Ruff linting
- [x] Ruff formatting
- [x] MyPy static type checking
- [x] Full test suite previously verified: 81 passed

## Milestone 3 — Service Layer 🚧

### User Service

- [x] User registration
- [x] Password hashing
- [x] Email normalization
- [x] Duplicate email handling
- [x] Profile updates
- [x] Partial profile updates
- [x] User deletion
- [x] Transaction management
- [x] User service tests

### Project Service

#### Project Creation

- [x] Implement ProjectService
- [x] Initialize ProjectRepository
- [x] Initialize ProjectMemberRepository
- [x] Create project
- [x] Automatically assign creator as OWNER
- [x] Commit project and membership in one transaction
- [x] Roll back transaction when an operation fails
- [ ] Test successful project creation
- [ ] Test automatic OWNER membership assignment
- [ ] Test rollback when membership creation fails

#### Project Retrieval

- [ ] Get project by ID
- [ ] Verify project membership before access
- [ ] Prevent non-members from accessing projects
- [ ] Test project retrieval
- [ ] Test unauthorized access

#### Project Listing

- [ ] List projects belonging to the current user
- [ ] Prevent returning unrelated projects
- [ ] Test project listing
- [ ] Test empty project lists

#### Project Updates

- [ ] Update project information
- [ ] Verify OWNER permissions
- [ ] Prevent MEMBER users from updating projects
- [ ] Support partial updates
- [ ] Test project updates
- [ ] Test permission failures

#### Project Deletion

- [ ] Delete project
- [ ] Verify OWNER permissions
- [ ] Define and enforce related resource deletion behavior
- [ ] Test project deletion
- [ ] Test unauthorized deletion

#### Project Membership Management

- [ ] Add project member
- [ ] Assign MEMBER role by default
- [ ] Prevent duplicate memberships
- [ ] Remove project member
- [ ] Change member role
- [ ] Protect the last project owner
- [ ] Enforce exactly-one-owner business rule
- [ ] Test membership management
- [ ] Test ownership edge cases

### Task Service

- [ ] Implement TaskService
- [ ] Initialize TaskRepository
- [ ] Create task
- [ ] Retrieve task
- [ ] List tasks by project
- [ ] Update task
- [ ] Change task status
- [ ] Change task priority
- [ ] Assign task to project member
- [ ] Unassign task
- [ ] Delete task
- [ ] Validate project membership
- [ ] Validate task assignee membership
- [ ] Validate task creator membership
- [ ] Handle missing resources
- [ ] Preserve partial update semantics
- [ ] Implement transaction management
- [ ] Add service tests

### Service Layer Quality

- [ ] Test successful business operations
- [ ] Test missing resources
- [ ] Test transaction rollback
- [ ] Test permission failures
- [ ] Test business rule violations
- [ ] Test edge cases
- [ ] Run full test suite
- [ ] Run Ruff
- [ ] Run Ruff formatter check
- [ ] Run MyPy

## Milestone 4 — Authentication & Authorization 📋

### Authentication

- [ ] Define authentication architecture
- [ ] Implement password verification
- [ ] Implement user login
- [ ] Implement access token generation
- [ ] Implement refresh tokens
- [ ] Implement authenticated user retrieval
- [ ] Enforce active account checks
- [ ] Test authentication workflows
- [ ] Test invalid credentials
- [ ] Test expired tokens

### Authorization

- [ ] Define project permission matrix
- [ ] Implement authenticated user dependencies
- [ ] Implement project membership authorization
- [ ] Implement OWNER permissions
- [ ] Implement MEMBER permissions
- [ ] Protect project endpoints
- [ ] Protect task endpoints
- [ ] Test authorization rules

## Milestone 5 — API Layer 📋

### Schemas

- [ ] User request schemas
- [ ] User response schemas
- [ ] Authentication schemas
- [ ] Project schemas
- [ ] Project membership schemas
- [ ] Task schemas
- [ ] Validation rules
- [ ] Response serialization

### API Endpoints

- [ ] User registration
- [ ] User login
- [ ] User profile
- [ ] Create project
- [ ] Retrieve project
- [ ] List user projects
- [ ] Update project
- [ ] Delete project
- [ ] Add project member
- [ ] Remove project member
- [ ] Change member role
- [ ] Create task
- [ ] Retrieve task
- [ ] List project tasks
- [ ] Update task
- [ ] Delete task

### API Testing

- [ ] Authentication integration tests
- [ ] Project API tests
- [ ] Task API tests
- [ ] Authorization tests
- [ ] Request validation tests
- [ ] Response serialization tests
- [ ] Error response tests

## Milestone 6 — Production Readiness 📋

- [ ] Review application architecture
- [ ] Review database indexes and query performance
- [ ] Review database constraints
- [ ] Add structured logging
- [ ] Improve error monitoring
- [ ] Add request tracing
- [ ] Review security configuration
- [ ] Review password and token security
- [ ] Add pagination where appropriate
- [ ] Add API documentation
- [ ] Review Docker production configuration
- [ ] Improve CI pipeline
- [ ] Establish minimum test coverage threshold
- [ ] Add deployment configuration
- [ ] Perform end-to-end testing

---

# Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.13 |
| Backend framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL 16 |
| Database driver | Psycopg 3 |
| Migrations | Alembic |
| Dependency management | uv |
| Testing | Pytest |
| HTTP testing | HTTPX |
| Linting | Ruff |
| Formatting | Ruff Formatter |
| Type checking | MyPy |
| Containerization | Docker |
| Orchestration | Docker Compose |
| CI/CD | GitHub Actions |

---

# Development

## Prerequisites

- Python 3.13
- Docker
- Docker Compose
- uv

## Clone the repository

```bash
git clone <repository-url>
cd project-management-platform
```

## Install dependencies

```bash
uv sync
```

## Run with Docker

```bash
docker compose up --build
```

## Run in the background

```bash
docker compose up -d --build
```

## Stop containers

```bash
docker compose down
```

## Check container status

```bash
docker compose ps
```

## Database Migrations

Apply migrations locally:

```bash
uv run alembic upgrade head
```

Apply migrations inside Docker:

```bash
docker compose exec api alembic upgrade head
```

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "migration message"
```

Check for missing migrations:

```bash
uv run alembic check
```

View migration history:

```bash
uv run alembic history
```

Check the current database revision:

```bash
uv run alembic current
```

**Important:** Review every autogenerated migration before applying it. ORM relationship changes alone do not require database migrations.

## Testing

Run the complete test suite:

```bash
uv run pytest -vvv
```

Run tests with coverage:

```bash
uv run pytest --cov=app --cov-report=term-missing
```

Run a specific test directory:

```bash
uv run pytest tests/services -vv
```

Run a specific test file:

```bash
uv run pytest tests/services/test_project.py -vv
```

## Code Quality

### Ruff linting

```bash
uv run ruff check .
```

### Ruff formatting

Format the code:

```bash
uv run ruff format .
```

Verify formatting:

```bash
uv run ruff format --check .
```

### MyPy

```bash
uv run mypy app
```

## CI/CD

GitHub Actions automatically runs the CI pipeline on:

- Pushes to `main`.
- Pull requests.

The pipeline:

1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs uv.
4. Installs locked dependencies.
5. Starts PostgreSQL 16.
6. Runs Alembic migrations.
7. Executes Pytest with coverage.
8. Runs Ruff linting.
9. Verifies Ruff formatting.
10. Runs MyPy.

The goal is to ensure that every change is tested and checked before being merged into the main branch.

---

# Current Development Focus

**Current milestone:** Milestone 3 — Service Layer

**Current feature:** ProjectService

**Implemented functionality:**

- Project creation.
- Automatic assignment of the creator as project OWNER.
- Transaction management across project and membership creation.
- Rollback on database failures.

**Immediate next steps:**

1. Complete successful project creation tests.
2. Verify rollback when owner membership creation fails.
3. Run the complete test suite and code quality checks.
4. Implement project retrieval with membership-based authorization.
5. Continue with project listing and management operations.

---

# Development Philosophy

This project is developed incrementally with an emphasis on maintainability and correctness.

Key principles:

- Business logic belongs in services.
- Database queries belong in repositories.
- Repositories do not manage transactions.
- Services own transaction boundaries.
- Database constraints protect data integrity.
- Business rules must be explicitly enforced.
- Automated tests verify both normal behavior and failure scenarios.
- Architectural decisions should be justified rather than introduced unnecessarily.

The objective is to build a realistic backend application while demonstrating professional Python engineering practices.