"""
Application entry point.

Initializes the FastAPI application, sets up the dependency-injection container,
defines the application lifecycle, and exposes the health check endpoint.

:author: Carlos S. Paredes Morillo
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import sentry_sdk

from src.endpoints.user import router as user_router
from src.endpoints.auth import router as auth_router
from src.endpoints.role import router as role_router
from src.endpoints.student import router as student_router
from src.endpoints.allergy_info import router as allergy_router
from src.endpoints.medical_info import router as medical_router
from src.endpoints.food_intolerance import router as intolerance_router
from src.endpoints.parent import router as parent_router
from src.settings import settings
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


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    send_default_pii=True,
)
container = Container()
app = FastAPI(lifespan=lifespan)
app.container = container


@app.get("/health")
def health():
    """Health check endpoint.

    Returns:
        dict: A simple message confirming the server is running.

    :author: Carlos S. Paredes Morillo
    """
    return {"message": "Server OK possibly"}


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(student_router)
app.include_router(allergy_router)
app.include_router(medical_router)
app.include_router(intolerance_router)
app.include_router(parent_router)

container.wire(
    modules=[
        "src.endpoints.user",
        "src.endpoints.auth",
        "src.endpoints.role",
        "src.endpoints.student",
        "src.endpoints.allergy_info",
        "src.endpoints.medical_info",
        "src.endpoints.food_intolerance",
        "src.endpoints.parent",
        "src.middleware.token.authenticateToken",
    ]
)
