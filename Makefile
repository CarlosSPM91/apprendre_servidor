build:
	docker compose build

up: down build
	docker compose up --abort-on-container-exit

down:
	docker compose down