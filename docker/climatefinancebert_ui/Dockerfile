### Base Image
FROM python:3.12-slim-bookworm as base

# Python settings
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 

# Update system libraries and install wget for healthcheck
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

### Build Image
FROM base as builder

# Get uv binary
COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /uvx /bin/

# Install dependencies into virtual environment
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

### Final Image
FROM base as final

WORKDIR /home/app

# Copy virtual environment with dependencies
COPY --from=builder /.venv /home/app/.venv
ENV VIRTUAL_ENV=/home/app/.venv
ENV PATH="/home/app/.venv/bin:$PATH"

# Copy app source code
COPY /src /home/app

# Create data directory with appropriate permissions
RUN mkdir -p /home/app/data && chown -R appuser:appuser /home/app/data

# Add healthcheck with a start period 
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget --spider --quiet http://localhost:8050/health || exit 1

# Change ownership of the app directory and switch to non-root user 
RUN chown -R appuser:appuser /home/app
USER appuser

# Expose Dash
EXPOSE 8050

# default environment variables
ENV HOST="0.0.0.0"
ENV PORT="8050"
ENV DEBUG="false"

# Run app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]