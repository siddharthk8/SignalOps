# Frontend

The SignalOps frontend is a React single-page application built with Vite. It provides the public landing and authentication experience, an authenticated dashboard, source application management, log ingestion tools, batch details, and incident investigation views.

## Tech Stack

- **React 19** — UI components
- **Vite** — Development server and build tooling
- **React Router** — Client-side routing
- **Redux Toolkit** — Authentication and client state
- **TanStack Query** — Server state, caching, and request management
- **Tailwind CSS** — Styling
- **Recharts** — Data visualization
- **OpenAPI-generated client** — Typed API requests and schemas in `src/api`

## Running Locally

1. Install Node.js and npm.
2. Ensure the backend is running and accessible.
3. Install dependencies and start the development server:

```bash
cd frontend
npm install
npm run dev
```

The development server is available at `http://localhost:5173` by default.

## Build and Preview

Create a production build:

```bash
cd frontend
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Environment Configuration

The frontend uses Vite environment variables. The production configuration includes:

```dotenv
VITE_GOOGLE_CLIENT_ID=...
VITE_API_URL=...
ENV=production
```

- `VITE_GOOGLE_CLIENT_ID` — Google Identity Services client ID for Google sign-in.
- `VITE_API_URL` — Base URL of the backend API.
- `ENV` — Environment indicator used by the application where configured.

Vite exposes variables prefixed with `VITE_` to client-side code. Do not put secrets, private keys, or other confidential credentials in frontend environment files. Use the appropriate environment-specific configuration for local development and production.

The file `src/core/config.js` handles application configuration, including environment-dependent error logging.

## API Client Generation

The frontend uses an OpenAPI-generated client located in `src/api`.

```bash
cd frontend
npm run openapi-ts
```

The generation command reads the backend OpenAPI schema from `http://127.0.0.1:8000/openapi.json` and regenerates the client.

Run this command when backend API schemas change to keep the generated client aligned with the API. Ensure the backend is running and reachable at the configured schema URL.

## Route and Page Structure

The application separates public pages from protected pages that require authentication.

### Public Pages

Located under `src/pages/public/`:

- `Login.jsx` — Sign in
- `Signup.jsx` — Account registration
- `EmailVerification.jsx` — Email verification
- `ForgotPassword.jsx` — Password recovery request
- `ResetPassword.jsx` — Password reset
- `PrivacyPolicy.jsx` — Privacy policy

### Protected Pages

Located under `src/pages/protected/`:

- `Dashboard.jsx` — Overview and summary metrics
- `SourceApps.jsx` — Source application management
- `CreateSourceApp.jsx` — Create a source application
- `Batches.jsx` — View batches for a source application
- `BatchDetails.jsx` — Inspect batch processing results
- `IngestLogs.jsx` — Log ingestion
- `IngestionPlayground.jsx` — Explore ingestion behavior
- `IngestionAPIAccess.jsx` — View ingestion API access information
- `Profile.jsx` — Manage the user profile
- `ChangePassword.jsx` — Change the account password

### Shared Pages

- `ErrorPage.jsx` — Application error handling
- `NotFoundPage.jsx` — Unmatched routes

## State and Data Flow

- **React Router** determines which page is rendered and separates public and protected navigation.
- **Redux Toolkit** stores client-side authentication state, including user profile and access-token data.
- **TanStack Query** manages server state, caching, and request lifecycle behavior.
- **Generated OpenAPI client** provides the frontend's API request functions and generated types.
- **Local storage** is used to persist user profile information for restoring client state across page refreshes.

Together, these components handle navigation, authentication state, server communication, and rendering of application data.

## Project Structure

```text
frontend/
├── src/
│   ├── api/          # Generated API client and types
│   ├── core/         # Shared configuration and core logic
│   └── pages/
│       ├── protected/
│       ├── public/
│       ├── ErrorPage.jsx
│       └── NotFoundPage.jsx
├── .env.example
└── package.json
```

This is a simplified overview; refer to the source tree for the complete structure.
