# Contributing to SignalOps

Thank you for contributing to SignalOps. The project consists of a FastAPI backend, a React frontend, and supporting documentation and deployment workflows.

## Before You Start

- Read the root [README](README.md) and [Architecture Documentation](docs/architecture.md).
- Use Python 3.12 for backend development and Node.js 24 for frontend development.
- Review `backend/core/config.py` to understand how backend environment configuration is loaded and where to place your local development `.env` file.
- Never commit secrets, credentials, or local environment files.

## Development Workflow

1. Create a focused branch for your change.
2. Implement the smallest change that solves the problem.
3. Update relevant documentation when API behavior, application workflows, or deployment processes change.
4. Run the relevant tests, linters, and build checks.
5. Open a pull request describing the change and its impact.

## Backend Checks

Run backend tests and lint checks:

```bash
cd backend
pytest
ruff check .
```

Ensure the required database and environment configuration are available when running tests.

## Frontend Checks

Run frontend linting and build checks:

```bash
cd frontend
npm run lint
npm run build
```

If the backend API schema changes, regenerate the OpenAPI client from the `frontend` directory:

```bash
npm run openapi-ts
```

Ensure the backend is running and accessible at the schema URL configured for client generation.

## Code Style and Architecture

- Keep API endpoints focused on HTTP handling.
- Place business workflows in domain services.
- Keep database queries and persistence logic in repositories.
- Keep log parsing, rule evaluation, correlation, and AI analysis within the engine layer.
- Enforce authentication and authorization on the backend; frontend route protection is not a substitute for server-side checks.
- Prefer clear, consistent names and focused changes.
- Avoid unrelated refactoring.

## Testing Expectations

- Add or update tests when behavior changes.
- Use focused unit tests for parsing, rules, and other isolated logic.
- Use integration tests for important API and database workflows where appropriate.
- For ingestion pipeline changes, verify persisted batches, events, signals, incidents, and analysis results as applicable.
- For authentication or authorization changes, verify relevant access-control and session behavior.

## Pull Requests

A good pull request should:

- Explain what changed and why.
- Summarize relevant tests and checks performed.
- Identify database migrations, environment changes, or deployment impacts.
- Link to a related issue when available.
- Mention any manual verification that was necessary.
