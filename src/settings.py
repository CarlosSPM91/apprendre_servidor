"""
Application Settings.

Defines the configuration for the application using Pydantic's
BaseSettings. Loads environment variables from `.env`.

:author: Carlos S. Paredes Morillo
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings model.

    Attributes:
        database_url (str): Database connection URL.

    Configuration:
        - env_file: `.env`
        - env_prefix: none
        - extra: ignore unknown variables
        - case_sensitive: False

    :author: Carlos S. Paredes Morillo
    """
    database_url: str
    secret_key:str
    algorithm:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

settings = Settings()