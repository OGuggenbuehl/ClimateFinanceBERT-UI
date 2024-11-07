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

WORKDIR /app

### Build Image
FROM base as builder
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

# Copy virtual environment with app and dependencies
COPY --from=builder /app/.venv /app/.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# copy app
COPY /src /app

# Expose Dash
EXPOSE 9000

# run app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]