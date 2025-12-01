"""
Application configuration settings.
Manages database connection strings, environment variables, and app-wide settings.
Separates configuration from code for different environments (dev, test, prod).
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Try to load from project root first, then from env folder
env_path = Path(__file__).resolve().parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent / "env" / ".env"
load_dotenv(env_path)

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "3005-final")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    
    # Construct DATABASE_URL if not provided directly
    def _build_database_url(self) -> str:
        """Build database URL from components."""
        from urllib.parse import quote_plus
        user = quote_plus(self.DATABASE_USER) if self.DATABASE_USER else ""
        password = quote_plus(self.DATABASE_PASSWORD) if self.DATABASE_PASSWORD else ""
        host = self.DATABASE_HOST
        port = self.DATABASE_PORT
        name = self.DATABASE_NAME
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL") or ""
    
    # Application Settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
 
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env file

# Create a global settings instance
settings = Settings()

# Build DATABASE_URL if not provided directly
if not settings.DATABASE_URL:
    settings.DATABASE_URL = settings._build_database_url()
