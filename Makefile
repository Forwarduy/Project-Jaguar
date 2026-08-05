.PHONY: help install test test-cov lint format clean docker-build docker-run

help: ## Show available commands
	@echo "Project-Jaguar - Available Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install development dependencies
	pip install -r requirements.txt

test: ## Run pytest suite
	pytest

test-cov: ## Run pytest with coverage report (>85% requirement)
	pytest --cov=agents --cov=config --cov=main --cov-report=term-missing --cov-fail-under=85

lint: ## Run code linter
	ruff check .

format: ## Format code automatically
	ruff format .

clean: ## Remove temporary cache and test files
	rm -rf .pytest_cache .coverage htmlcov __pycache__ agents/__pycache__ tests/__pycache__

docker-build: ## Build Docker container
	docker build -t project-jaguar:latest .

docker-run: ## Run Docker container CLI help
	docker run --rm project-jaguar:latest --help
