.PHONY: help build up down logs migrate superuser shell test test-verbose clean health

help:
	@echo "Ken ABM Platform Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup & Infrastructure:"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services (detached)"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - Follow logs from all services"
	@echo ""
	@echo "Database & Users:"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make superuser      - Create superuser account"
	@echo ""
	@echo "Development:"
	@echo "  make shell          - Django shell in container"
	@echo "  make test           - Run tests"
	@echo "  make test-verbose   - Run tests with verbose output"
	@echo "  make health         - Check system health"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""

build:
	docker compose build

up:
	docker compose up -d
	@echo "✓ Services started"
	@echo "API: http://localhost:8000"
	@echo "Admin: http://localhost:8000/admin/"

down:
	docker compose down

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f django-api

logs-worker:
	docker compose logs -f celery-worker

migrate:
	docker compose exec django-api python manage.py migrate
	@echo "✓ Migrations applied"

migrate-makemigrations:
	docker compose exec django-api python manage.py makemigrations

superuser:
	docker compose exec django-api python manage.py createsuperuser

shell:
	docker compose exec django-api python manage.py shell

shell-plus:
	docker compose exec django-api python manage.py shell_plus

test:
	docker compose exec django-api python manage.py test apps --parallel auto

test-verbose:
	docker compose exec django-api python manage.py test apps --parallel auto -v 2

test-coverage:
	docker compose exec django-api coverage run --source='.' manage.py test apps
	docker compose exec django-api coverage report

test-campaigns:
	docker compose exec django-api python manage.py test apps.campaigns

test-audit:
	docker compose exec django-api python manage.py test apps.audit

health:
	@echo "Checking API health..."
	@curl -s http://localhost:8000/health/ | jq . || echo "API not responding"

health-db:
	@echo "Checking database connection..."
	docker compose exec -T postgres pg_isready

health-redis:
	@echo "Checking Redis connection..."
	docker compose exec -T redis redis-cli ping

clean:
	docker compose down -v
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type f -name ".coverage" -delete
	@echo "✓ Cleaned up"

format:
	docker compose exec django-api black apps/
	docker compose exec django-api isort apps/

lint:
	docker compose exec django-api flake8 apps/

static:
	docker compose exec django-api python manage.py collectstatic --noinput

install-deps:
	docker compose exec django-api pip install -r requirements.txt

install-dev-deps:
	docker compose exec django-api pip install black flake8 isort coverage

django-createsuperuser:
	docker compose exec django-api python manage.py createsuperuser

django-changepassword:
	docker compose exec django-api python manage.py changepassword

restart-api:
	docker compose restart django-api

restart-worker:
	docker compose restart celery-worker

restart-beat:
	docker compose restart celery-beat

ps:
	docker compose ps

# Development workflow shortcuts

init: build up migrate superuser
	@echo "✓ Development environment initialized"
	@echo "Next steps:"
	@echo "  1. Create admin user (already done above)"
	@echo "  2. Visit http://localhost:8000/admin/"
	@echo "  3. Check API docs at http://localhost:8000/api/v1/"

ready: up migrate health
	@echo "✓ System ready"

dev: build up migrate
	@echo "✓ Dev environment ready"

freeze:
	docker compose exec django-api pip freeze > backend/requirements.txt
