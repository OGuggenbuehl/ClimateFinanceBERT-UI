#################################################################################
# GLOBALS                                                                       #
#################################################################################
ENVNAME := $(shell poetry env info --path)
VENV := $(ENVNAME)/bin

PROJECT_NAME = climatefinancebert_ui
PYTHON_INTERPRETER = $(VENV)/python


#################################################################################
# COMMANDS                                                                      #
#################################################################################
.PHONY: run
run:
	$(PYTHON_INTERPRETER) climatefinancebert_ui/app.py

.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

	rm -rf .*_cache
	rm -rf logs
	rm -rf site

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