#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_ROOT := $(shell pwd)
ENVNAME := $(shell pwd)/.venv
VENV := $(ENVNAME)/bin
PYTHON_INTERPRETER = $(VENV)/python


#################################################################################
# COMMANDS                                                                      #
#################################################################################

.PHONY: run
run:
	PYTHONPATH=$(PROJECT_ROOT) $(PYTHON_INTERPRETER) src/app.py

.PHONY: test
test:
	$(PYTHON_INTERPRETER) -m pytest ./tests
	$(VENV)/coverage report

.PHONY: lint
lint:
	git add --intent-to-add .
	. $(VENV)/activate; $(VENV)/
	
.PHONY: format
format:
	ruff format .


#################################################################################
# SETUP
#################################################################################

.PHONY: install
install: _install_uv _create_venv _install_dependencies

.PHONY: _install_uv
_install_uv:
	@echo "Installing uv"
	# Install uv only if not already installed
	if ! command -v uv > /dev/null 2>&1; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv is already installed"; \
	fi

.PHONY: _create_venv
_create_venv:
	@echo "Creating virtual environment"
	uv venv  # This will create the virtual environment in .venv

.PHONY: _install_dependencies
_install_dependencies:
	@echo "Installing dependencies"
	uv sync --all-extras  # This will install the dependencies based on uv configuration


#################################################################################
# DOCKER
#################################################################################

.PHONY: docker-build
docker-build:
	docker compose -f "docker/docker-compose.yml" build --pull

.PHONY: docker-push
docker-push:
	docker compose -f "docker/docker-compose.yml" push

.PHONY: docker-up
docker-up:
	docker compose -f "docker/docker-compose.yml" up --pull always --build --detach --wait

.PHONY: docker-down
docker-down:
	docker compose -f "docker/docker-compose.yml" down

.PHONY: docker-restart
docker-restart:
	docker compose -f "docker/docker-compose.yml" restart

.PHONY: docker-logs
docker-logs:
	docker compose -f "docker/docker-compose.yml" logs --follow

.PHONY: docker-overview
docker-overview:
	docker compose -f "docker/docker-compose.yml" ps