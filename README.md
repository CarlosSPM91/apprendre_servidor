# Aprendre API

Applicació per fer el seguiment escolar.

## Getting Started
### Pre-requisits
- Python 3.13
- uv (gestor de paquets) → pip install uv
- Docker
- Un editor de codi (VS Code, PyCharm)
- Postman o editor web (Swagger UI) per provar l’API

### clona el repository
```
git clone https://github.com/CarlosSPM91/apprendre_servidor.git
cd aprendre-api
```

### instala dependencies
```
pip install uv
uv sync
```

### Variables d'entorn
1.Canvia el fitxer .env.exemple a .env

2.Omple les dades de connexió per treballar en local i fer proves, per exemple:
```
APP_ENV=dev
APP_PORT=8000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=aprendre
DB_USER=aprendre
DB_PASSWORD=aprendre

DATABASE_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### Executar API en local
```
uv run uvicorn src.main:app --reload
```

### Executar API amb Docker
Constuir l'imatge
```
	docker compose build
```
Aixecar la app en docker
```
	docker compose up
```
Aturar la app
```
	docker compose down
```
