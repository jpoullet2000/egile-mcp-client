# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set work directory
WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Copy project code
COPY egile_mcp_client/ ./egile_mcp_client/
COPY config.example.yaml ./
COPY README.md ./

# Install the project
RUN poetry install --only=main

# Create data directory for conversation history
RUN mkdir -p /app/data

# Create config directory
RUN mkdir -p /app/config

# Expose port for web interface
EXPOSE 8080

# Set default command
ENTRYPOINT ["poetry", "run", "egile-mcp-client"]
CMD ["--help"]
