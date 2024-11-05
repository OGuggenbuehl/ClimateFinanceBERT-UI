### Base Image
FROM python:3.11.5-slim-bullseye as base

# Python settings
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Update system libraries
RUN apt-get update -y && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

### Build Image
FROM base as builder

# Install python development dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Python settings
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.7.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Create virtual environment
RUN python -m venv /venv

# Install dependencies into virtual environment
COPY pyproject.toml poetry.lock ./
RUN poetry export --no-ansi --no-interaction --without-hashes --format requirements.txt --output requirements.txt
RUN /venv/bin/pip install --pre -r requirements.txt

# Install app
COPY . .
RUN poetry build --no-ansi --no-interaction --format wheel && /venv/bin/pip install dist/*.whl

### Final Image
FROM base as final

# Copy virtual environment with app and dependencies
COPY --from=builder /venv /venv

# Activate virtual environment
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# copy app
COPY /climatefinancebert_ui /app

# set workdir
WORKDIR /app

# Expose Dash
EXPOSE 9000

# run app
ENTRYPOINT ["python"]
CMD ["./app.py"]