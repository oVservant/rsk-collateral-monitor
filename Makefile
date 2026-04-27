# BTC Collateral Monitor - Makefile

.PHONY: help install dev test lint clean build docker run-dashboard run-poller setup-db install-cron backup health

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install production dependencies
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Installation complete!"

dev: ## Install development dependencies
	. venv/bin/activate && pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Development setup complete!"

test: ## Run integration tests
	. venv/bin/activate && python tests/test_integration.py

test-verbose: ## Run tests with verbose output
	. venv/bin/activate && python -m pytest tests/ -v --tb=long

coverage: ## Run tests with coverage report
	. venv/bin/activate && python -m pytest tests/ --cov=. --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

lint: ## Run linters (flake8, black, isort)
	. venv/bin/activate && flake8 .
	. venv/bin/activate && black --check .
	. venv/bin/activate && isort --check-only .

format: ## Format code with black and isort
	. venv/bin/activate && black .
	. venv/bin/activate && isort .

clean: ## Clean build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/
	@echo "✅ Clean complete!"

build: ## Build Python package
	pip install build
	python -m build
	@echo "✅ Build complete! Check dist/ folder"

docker-build: ## Build Docker image
	docker build -t rsk-collateral-monitor .
	@echo "✅ Docker image built!"

docker-run: ## Run Docker container
	docker run --rm -v $(PWD)/data:/app/data --env-file .env rsk-collateral-monitor python scripts/poll_positions.py

docker-up: ## Start all services with docker-compose
	docker-compose up -d
	@echo "✅ Services started!"

docker-down: ## Stop all services
	docker-compose down
	@echo "✅ Services stopped!"

docker-logs: ## Show docker logs
	docker-compose logs -f

setup-db: ## Initialize database
	. venv/bin/activate && python scripts/setup_db.py
	@echo "✅ Database initialized!"

run-poller: ## Run polling script manually
	. venv/bin/activate && python scripts/poll_positions.py

run-dashboard: ## Start Streamlit dashboard
	. venv/bin/activate && streamlit run dashboard/app.py --server.port=8501

install-cron: ## Install cron job
	chmod +x scripts/install_cron.sh
	./scripts/install_cron.sh

validate-env: ## Validate .env configuration
	. venv/bin/activate && python scripts/validate_env.py

health: ## Run health check
	. venv/bin/activate && python scripts/health_check.py

backup: ## Backup database
	@mkdir -p backups
	@cp data/collateral_monitor.db backups/collateral_monitor.db.backup.$$(date +%Y%m%d_%H%M%S)
	@echo "✅ Database backed up to backups/"

setup: ## Complete setup (install + setup-db + validate)
	make install
	make setup-db
	make validate-env
	make health
	@echo "✅ Complete setup finished!"
