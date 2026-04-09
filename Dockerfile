# Build stage
FROM astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /build

COPY pyproject.toml ./
RUN uv sync --frozen --no-dev

COPY . .
RUN uv build --wheel

# Runtime stage
FROM python:3.14.2-slim-bookworm

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /usr/local/bin/uvx /usr/local/bin/uvx

# Copy built wheel and install
COPY --from=builder /build/dist/*.whl /tmp/
RUN uv pip install --system /tmp/*.whl

# Copy application code
COPY jokes.json ./
COPY src ./src

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "src/app/run.py"]
