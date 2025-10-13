# Aprendre API

Application for school tracking.

## Getting Started
### Pre-requisits
- Python 3.13
- uv (package manager) → pip install uv
- Docker
- Code editor (VS Code, PyCharm)
- Postman or web editor (Swagger UI) to test the API

### Clone the repository
```
git clone https://github.com/CarlosSPM91/apprendre_servidor.git
cd aprendre-api
```

### Install dependencies
```
pip install uv
uv sync
```

### Envitoment variables
1.Rename the file .env.exemple to .env

2.Fill in the connection data to work locally and make tests, for example:
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

### Run local API
```
uv run uvicorn src.main:app --reload
```

### Executar API amb Docker
Build Image
```
	docker compose build
```
Start App
```
	docker compose up
```
Stop App
```
	docker compose down
```

### Run with Make
Install make
```
	En windows 
		Instalar cocholately o MSYS2
		Chololately: choco install make
		MSY: pacman -S make
	
	En mac
		Instalar Homebre
			brew install make
```

Build Image
```
	make build
```
Start the app
```
	make up
```
Stop the app
```
	make down
```

Testing
```
	make testing
```

View coverage
```
	make coverage
```