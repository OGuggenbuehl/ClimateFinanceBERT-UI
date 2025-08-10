#################################################################################
# GLOBALS                                                                       #
#################################################################################

# Common settings
PROJECT_ROOT := $(CURDIR)

ifeq ($(OS),Windows_NT)
	# Windows
	PATHSEP := \\
	SCRIPTS_DIR := Scripts
	SET_PYTHONPATH := set "PYTHONPATH=$(PROJECT_ROOT)" &&
else
	# Unix
	PATHSEP := /
	SCRIPTS_DIR := bin
	SET_PYTHONPATH := PYTHONPATH=$(PROJECT_ROOT)
endif

ENVNAME := $(PROJECT_ROOT)$(PATHSEP).venv
VENV := $(ENVNAME)$(PATHSEP)$(SCRIPTS_DIR)
PYTHON_INTERPRETER := $(VENV)$(PATHSEP)python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

# Default target
.PHONY: help
help:
	@echo "ClimateFinanceBERT-UI Makefile"
	@echo "==============================="
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  run              Run the application locally"
	@echo "  test             Run tests and generate coverage report"
	@echo "  lint             Run code linting"
	@echo "  format           Format code"
	@echo "  clean            Clean temporary files"
	@echo "  install          Install dependencies"
	@echo "  docker-run       Run application in Docker container"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-up        Start Docker services"
	@echo "  docker-down      Stop Docker services"
	@echo "  docker-logs      View Docker logs"
	@echo "  dev              Start development environment"
	@echo "  duckdb-pipeline  Run DuckDB pipeline"

.PHONY: run
run:
	$(SET_PYTHONPATH) $(PYTHON_INTERPRETER) src$(PATHSEP)app.py

.PHONY: test
test:
	uv pip install -e ".[test]"
	$(PYTHON_INTERPRETER) -m pytest

.PHONY: lint
lint:
	$(PYTHON_INTERPRETER) -m ruff check .

.PHONY: format
format:
	$(PYTHON_INTERPRETER) -m ruff format .

.PHONY: clean
clean:
ifeq ($(OS),Windows_NT)
	@echo "Cleaning temporary files"
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .ruff_cache rmdir /s /q .ruff_cache
	@if exist .coverage del /f /q .coverage
	@for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@for /r %%f in (*.pyc) do @del /f /q "%%f"
else
	@echo "Cleaning temporary files"
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
endif

.PHONY: dev
dev: format lint
	$(SET_PYTHONPATH) $(PYTHON_INTERPRETER) src$(PATHSEP)app.py --debug

#################################################################################
# SETUP                                                                        #
#################################################################################

.PHONY: install
install:
ifeq ($(OS),Windows_NT)
	@echo "Installing on Windows"
	@echo "Please run setup manually:"
	@echo "1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
	@echo "2. Create virtual environment: uv venv"
	@echo "3. Install dependencies: uv sync --all-extras"
else
	@echo "Installing on Unix"
	@$(MAKE) _install_uv
	@$(MAKE) _create_venv
	@$(MAKE) _install_dependencies
	@$(MAKE) _install_direnv
	@echo "Installation complete"
	@echo "Execute make run to start the application"
endif

.PHONY: _install_uv _create_venv _install_dependencies _install_direnv
_install_uv:
	@echo "Installing uv"
	@if ! command -v uv > /dev/null 2>&1; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv is already installed"; \
	fi

_create_venv:
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment"; \
		uv venv; \
	else \
		echo "Virtual environment already exists"; \
	fi

_install_dependencies:
	@echo "Installing dependencies"
	uv sync --all-extras

_install_direnv:
	@echo "Installing direnv"
	@if ! command -v direnv > /dev/null 2>&1; then \
		curl -sfL https://direnv.net/install.sh | bash; \
	else \
		echo "direnv is already installed"; \
	fi

#################################################################################
# DOCKER                                                                       #
#################################################################################

# Docker variables - more robust environment variable handling
DOCKER_PORT ?= $(if $(PORT),$(PORT),8050)
DOCKER_DEBUG ?= $(if $(DEBUG),$(DEBUG),false)
DOCKER_COMPOSE_FILE := docker/docker-compose.yml

# Handle Windows paths in Docker commands
ifeq ($(OS),Windows_NT)
    DOCKER_DATA_MOUNT := $(subst /,\,$(PWD)/data):/home/app/data
else
    DOCKER_DATA_MOUNT := $(PWD)/data:/home/app/data
endif

.PHONY: docker-run docker-build docker-push docker-up docker-down docker-restart docker-logs docker-overview

# Run the application in a Docker container - use the same env vars as docker-compose
docker-run:
	docker run -v "$(DOCKER_DATA_MOUNT)" \
		-p $(DOCKER_PORT):$(DOCKER_PORT) \
		-e PORT=$(DOCKER_PORT) \
		-e DEBUG=$(DOCKER_DEBUG) \
		-e HOST=0.0.0.0 \
		climatefinancebert_ui:latest

# Build Docker images defined in the docker-compose file
docker-build:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" build --pull

# Push Docker images to registry
docker-push:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" push

# Start services in detached mode, pulling latest images and waiting for healthchecks
docker-up:
ifeq ($(OS),Windows_NT)
	set "PORT=$(DOCKER_PORT)" && set "DEBUG=$(DOCKER_DEBUG)" && docker compose -f "$(DOCKER_COMPOSE_FILE)" up --pull always --build --detach --wait
else
	PORT=$(DOCKER_PORT) DEBUG=$(DOCKER_DEBUG) docker compose -f "$(DOCKER_COMPOSE_FILE)" up --pull always --build --detach --wait
endif

# Stop and remove containers, networks
docker-down:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" down

# Restart all containers
docker-restart:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" restart

# Follow log output from containers
docker-logs:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" logs --follow

# Show status of containers
docker-overview:
	docker compose -f "$(DOCKER_COMPOSE_FILE)" ps

# Quick target for development with Docker
.PHONY: docker-dev
docker-dev: docker-build
ifeq ($(OS),Windows_NT)
	set "PORT=$(DOCKER_PORT)" && set "DEBUG=true" && docker compose -f "$(DOCKER_COMPOSE_FILE)" up
else
	PORT=$(DOCKER_PORT) DEBUG=true docker compose -f "$(DOCKER_COMPOSE_FILE)" up
endif

#################################################################################
# DUCKDB                                                                       #
#################################################################################

.PHONY: duckdb-pipeline
duckdb-pipeline: 
	$(PYTHON_INTERPRETER) src$(PATHSEP)utils$(PATHSEP)duckdb_pipeline.py