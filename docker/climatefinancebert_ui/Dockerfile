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

# Get uv binary
COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /uvx /bin/

# Install python development dependencies
RUN apt-get update && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

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

# Change ownership of the app directory and switch to non-root user 
RUN chown -R appuser:appuser /home/app
USER appuser

# Expose Dash
EXPOSE 9000

# Run app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]