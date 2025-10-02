"""
Application entry point.

Initializes the FastAPI application, sets up the dependency-injection container,
defines the application lifecycle, and exposes the health check endpoint.

:author: Carlos S. Paredes Morillo
"""
from contextlib import asynccontextmanager
import sys
from fastapi import FastAPI, Depends
from dependency_injector.wiring import inject, Provide

from .infrastructure.connection.db import async_init_db
from .application.services.user import UserService
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

@app.get("/health")
def health():
    """Health check endpoint.

    Returns:
        dict: A simple message confirming the server is running.

    :author: Carlos S. Paredes Morillo
    """
    return {"message": "Server OK possibly"}


container.wire(modules=[sys.modules[__name__]])