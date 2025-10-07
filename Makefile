build:
	docker compose build --target dev

up:
	docker compose up

down:
	docker compose down

pushA:
	git push origin main:main
