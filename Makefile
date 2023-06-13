
start_db:
	docker-compose up -d postgres

test:
	poetry run pyupgrade
	poetry run pytest src/ --junitxml=.pytest_cache/report.xml

start_api:
	poetry run uvicorn candlestick.interface.api.main:app

coding_standard:
	poetry run isort --gitignore src/
	poetry run black src/

start_infrastructure:
	docker-compose up -d

stop_infrastructure:
	docker-compose down

db_upgrade:
	@echo 'Applying migrations...'
	cd src/candlestick/infrastructure/repositories/alembic/ && \
	python -m alembic upgrade head

db_make_migration:
	cd src/candlestick/infrastructure/repositories/alembic/ && \
	python -m alembic revision --autogenerate -m "$(message)"

build-local-base:
	@docker build -t candlestick_base_image --platform linux/amd64 -f build/Dockerfile.base ./
