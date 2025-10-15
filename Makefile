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

docs:
	pdoc --no-show-source src -o docs

test-doc:
	pytest --html=proves/resultados/pytest_report.html --self-contained-html