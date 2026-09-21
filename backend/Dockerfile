# Build stage: install dependencies separately so the final image stays clean
FROM python:3.12.13-slim-bookworm AS builder

WORKDIR /build

# Create virtual env
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies first so this layer stays cached
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Runtime stage: this is the image that actually runs
FROM python:3.12.13-slim-bookworm

WORKDIR /app

# Run the app as a normal user instead of root
RUN useradd --create-home appuser

# Copy only the dependencies from the build stage
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Add application code separately so code changes don't invalidate dependencies
COPY --chown=appuser:appuser . .

# Logs are currently written to stdout/stderr and collected by Docker/CloudWatch.
# If file-based logging is needed in the future, create /app/logs and grant appuser access.
# RUN mkdir -p /app/logs && chown -R appuser:appuser /app

USER appuser

# Faster logs and no unnecessary Python cache files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
