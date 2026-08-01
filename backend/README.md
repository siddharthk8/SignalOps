# Backend

This directory contains the FastAPI application that powers SignalOps. The backend is responsible for authentication, source application management, log ingestion, incident correlation, AI-assisted analysis, and the batch and dashboard APIs consumed by the frontend.

It is the authoritative implementation of the product workflow: everything from login and ownership checks to log parsing, incident creation, and dashboard summaries happens here.

## Architecture Summary

- Entry point: [main.py](main.py)
- API router: `app/api/v1/router.py`
- Core layers:
	- `app/api` for HTTP endpoints
	- `app/domains` for business workflows and request/response models
	- `app/engine` for parsing, rule execution, correlation, and AI analysis
	- `app/db` for SQLAlchemy models, repositories, and session management
	- `app/core` for configuration, logging, exceptions, and rate limiting

The codebase follows a hybrid DDD-style modular monolith: the HTTP layer is thin, business logic lives in domain services, and the pipeline is split into small, testable engine stages.

## Configuration

SignalOps keeps backend configuration outside the repository.

Set `ENV_DIR` to your home directory so tools that need an explicit base path can resolve the config folder consistently across machines. The backend itself reads the final files from the user's home config directory:

- development: `~/.config/signalops/backend/.env.local`
- production: `~/.config/signalops/backend/.env.production`

Those are the actual runtime filenames. The repository also includes [backend/.env.example](.env.example) as a reference for the available variables and their intended values.

The example file is intentionally descriptive. It shows the expected variables for backend code and container orchestration, but it is not the runtime file that the application loads.

## Running Locally

1. Set `ENV_DIR` to your home directory.
2. Create `~/.config/signalops/backend`.
3. Copy [backend/.env.example](.env.example) into that folder and rename it to `.env.local`.
4. Optionally create `.env.production` in the same folder with production-ready values.

Then install dependencies and start the service:

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

The API is served at `http://127.0.0.1:8000` by default.

## Database And Migrations

- SQLAlchemy uses an async engine and async session factory.
- Alembic handles schema migrations.
- The default test and local configuration assumes PostgreSQL.

Typical migration commands:

```bash
cd backend
alembic upgrade head
```

## API Surface

All routes are mounted under `/api/v1`.

- `GET /health` checks the database connection.
- `POST /auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/logout-all`, `/auth/forgot-password`, `/auth/reset-password` manage sessions.
- `POST /users` creates an account.
- `GET/PATCH/DELETE /users/me` manages the current user.
- `POST/DELETE /users/me/profile-image` uploads or deletes the profile image.
- `POST /source-apps` creates a source application.
- `GET /source-apps` lists the current user’s source applications.
- `GET /source-apps/{id}/batches` lists batches for a source app.
- `POST /logs` ingests a batch of logs and runs the pipeline.
- `GET /batches/{id}` returns the full batch payload.
- `GET /dashboard` returns the user’s summary metrics.
- `POST /incidents/{id}/resolve` marks an incident as resolved.

## Ingestion Pipeline

`POST /logs` is the entry point for the operational pipeline.

1. Raw logs are persisted with a batch record.
2. Logs are parsed through the source-app registry.
3. Any unresolved logs are sent to the Bedrock-backed fallback parser.
4. Domain rules and generic rules create signals.
5. Signals are correlated into incidents.
6. Incidents are analyzed by the AI incident analyzer.
7. All persisted changes are committed at the end of the pipeline.

The endpoint returns the incident analysis payload that the UI renders in batch details and related views.

## How The Pieces Fit Together

- Routers expose HTTP endpoints only and keep request handling lightweight.
- Domain services enforce ownership and orchestrate business workflows.
- Repositories isolate database queries and writes.
- The engine layer handles the log pipeline, from parsing to incident analysis.
- SQLAlchemy models represent the persisted batch, event, signal, incident, and user data.

## Authentication Model

- Access tokens are JWTs.
- Refresh tokens are stored in hashed form.
- The `token_version` claim is checked on every request, which allows password changes and logout-all operations to invalidate older sessions.
- Protected endpoints use the `CurrentUser` dependency and ownership checks before reading or mutating user-owned data.

## Testing

Backend tests live in `backend/tests` and use `pytest` with async HTTP client fixtures.

```bash
cd backend
pytest
```

The test suite covers:

- authentication and password resets
- user CRUD and profile image uploads
- source app CRUD and pagination
- log ingestion and batch retrieval
- incident resolution
- dashboard metrics
