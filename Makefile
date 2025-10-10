build:
	docker compose build

up: down build
	docker compose up --abort-on-container-exit

down:
	docker compose down

testing:
	PYTHONDONTWRITEBYTECODE=1 uv run pytest -v

remove pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

coverage: 
	coverage run -m pytest
	coverage html