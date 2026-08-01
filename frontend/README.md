# Frontend

This directory contains the React application that renders the SignalOps landing page, public authentication screens, and the authenticated dashboard experience.

It is a route-driven single-page application that focuses on three user journeys: account access, source-app and batch management, and incident investigation.

## Stack

- React 19
- Vite
- React Router
- Redux Toolkit
- TanStack Query
- Tailwind CSS
- Recharts
- Generated OpenAPI client code in `src/api`

The UI leans on generated API types and client code so the frontend stays aligned with backend changes.

## Running Locally

1. Install dependencies.
2. Start the frontend dev server.
3. Make sure the backend is already running so API requests resolve successfully.

```bash
cd frontend
npm install
npm run dev
```

The development server runs on `http://localhost:5173`.

## Build And Preview

```bash
cd frontend
npm run build
npm run preview
```

## API Client Generation

The frontend uses an OpenAPI-generated client rather than hand-written request wrappers.

```bash
cd frontend
npm run openapi-ts
```

That command reads the backend schema from `http://127.0.0.1:8000/openapi.json` and regenerates the client in `src/api`.

Run it whenever the backend API changes so the frontend keeps the request surface and types in sync.

## Runtime Configuration

- `VITE_API_URL` points the client at the backend API.
- `src/core/config.js` reads the current Vite environment and switches error logging behavior in development.

The app also persists the signed-in user profile in local storage so the dashboard can restore session state on refresh.

## Route Structure

The app is organized around public and protected route groups.

### Public Routes

- `/login`
- `/signup`
- `/forgot-password`
- `/reset-password`

### Protected Routes

- `/dashboard`
- `/dashboard/source-apps`
- `/dashboard/source-apps/:sourceAppId/batches`
- `/dashboard/source-apps/:sourceAppId/batches/:batchId`
- `/dashboard/source-apps/:sourceAppId/batches/ingest-logs`
- `/dashboard/create-source-app`
- `/profile`
- `/change-password`

## State And Data Flow

- Redux stores the authenticated user profile and access token data.
- TanStack Query manages server state, caching, and retry behavior.
- The generated API client is configured once at startup and then used throughout the route tree.

The practical flow is simple: the router decides which screen to render, Redux keeps user identity available, TanStack Query fetches and caches server data, and the generated client does the actual API calling.
