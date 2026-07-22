# Build stage: install dependencies separately so the final image stays clean
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Create virtual env
RUN python -m venv .venv

ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies first (Docker can cache this layer)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Add application code
COPY . .


# Runtime stage: this is the image that actually runs
FROM python:3.12-slim-bookworm

WORKDIR /app

# Run the app as a normal user instead of root
RUN useradd --create-home appuser

# Copy app and dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /app /app

# Create writable log directory and give ownership to appuser
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

USER appuser

# Use the virtual environment we created earlier
ENV PATH="/app/.venv/bin:$PATH"

# Faster logs and no unnecessary Python cache files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
