# UV Image to fetch binary from
ARG UV_VERSION=latest

### Base Image
FROM python:3.12-slim-bookworm as base

# Python settings
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 

# Update system libraries
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

### Build Image
FROM base as builder

# Set the working directory to /app during the build stage
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /uvx /bin/

# Install python development dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies into virtual environment
COPY pyproject.toml uv.lock ./
RUN uv venv
RUN uv sync --frozen

### Final Image
FROM base as final

# Set the working directory to /home/app
WORKDIR /home/app

# Copy virtual environment with app and dependencies
COPY --from=builder /app/.venv /home/app/.venv
ENV VIRTUAL_ENV=/home/app/.venv
ENV PATH="/home/app/.venv/bin:$PATH"

# Copy app code to /home/app
COPY /src /home/app

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /home/app

# Switch to non-root user
USER appuser

# Expose Dash
EXPOSE 9000

# Run app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]