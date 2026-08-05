.PHONY: install test coverage lint docker-build clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest --cov=agents --cov=config --cov=main --cov-report=term-missing --cov-fail-under=85

coverage:
	pytest --cov=agents --cov=config --cov=main --cov-report=html

lint:
	flake8 agents tests main.py config.py

docker-build:
	docker build -t project-jaguar:latest .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .cov_html .coverage
