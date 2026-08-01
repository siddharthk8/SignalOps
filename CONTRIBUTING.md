# Contributing

Thank you for improving SignalOps. This repository is organized as a backend FastAPI application, a frontend React application, and a set of deployment files and docs that describe the full workflow.

## Before You Start

- Read the root [README](README.md) and the [architecture notes](docs/architecture.md).
- Use Python 3.12 for the backend and Node 24 for the frontend.
- Keep local environment files outside the repository in `~/.config/signalops/backend`.

## Development Workflow

1. Create a focused branch for the change.
2. Make the smallest implementation change that solves the problem.
3. Update docs if the API, workflow, or deployment behavior changes.
4. Run the relevant tests and linters.
5. Open a pull request with a clear description of the behavior change.

## Backend Checks

```bash
cd backend
pytest
ruff check .
```

## Frontend Checks

```bash
cd frontend
npm run lint
npm run build
```

If you change the API schema, regenerate the client with `npm run openapi-ts`.

## Code Style

- Preserve the existing layer boundaries: routers should stay thin, services should own workflow logic, and repositories should own queries.
- Keep authorization checks in the domain services or dependency layer, not in the frontend.
- Favor clear names over clever code.
- Avoid introducing unrelated refactors in the same change.

## Testing Expectations

- Add or update tests when behavior changes.
- Prefer integration-style tests for request/response flows and focused unit tests for parsing and rule logic.
- When a change affects the pipeline, verify the batch and incident views still produce the expected persisted data.

## Pull Requests

- Summarize what changed and why.
- Call out any migration, environment, or deployment impact.
- Link to the relevant issue if one exists.
- Mention any manual verification performed.
