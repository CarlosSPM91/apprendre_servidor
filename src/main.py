"""
Application entry point.

Initializes the FastAPI application, sets up the dependency-injection container,
defines the application lifecycle, and exposes the health check endpoint.

:author: Carlos S. Paredes Morillo
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.endpoints.user import router as user_router
from src.endpoints.auth import router as auth_router
from src.endpoints.role import router as role_router

from .infrastructure.connection.db import async_init_db
from .container import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context.

    Initializes the database at startup and keeps the app running
    until shutdown.

    Args:
        app (FastAPI): FastAPI application instance.

    Yields:
        None

    :author: Carlos S. Paredes Morillo
    """
    engine = container.database_engine()
    await async_init_db(engine)
    yield


container = Container()
app = FastAPI(lifespan=lifespan)
app.container = container

# @app.middleware("http")
# async def my_middleware(request: Request, call_next):
#     print(f"Request path: {request.url.path}")
#     token = request.headers.get("Authorization")
#     token_service = TokenService()
#     resp = token_service.validate(token)
#     print(resp.user_id)
#     response = await call_next(request)
#     response.headers["X-Custom-Header"] = "MiMiddleware"
#     return response


@app.get("/health")
def health():
    """Health check endpoint.

    Returns:
        dict: A simple message confirming the server is running.

    :author: Carlos S. Paredes Morillo
    """
    return {"message": "Server OK possibly"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(role_router)

container.wire(
    modules=["src.endpoints.user", "src.endpoints.auth", "src.endpoints.role"]
)
