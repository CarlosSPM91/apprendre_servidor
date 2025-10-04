"""
Application Settings.

Defines the configuration for the application using Pydantic's
BaseSettings. Loads environment variables from `.env`.

:author: Carlos S. Paredes Morillo
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

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

print(f"DATABASE_URL: {settings.database_url}")
print(f"SECRET_KEY: {settings.secret_key}")
print(f"ALGORITHM: {settings.algorithm}")