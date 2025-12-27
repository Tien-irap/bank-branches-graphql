"""
Core configuration for the Bank Branches API
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings"""
    
    # Application Settings
    APP_NAME: str = "Bank Branches GraphQL API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    GRAPHQL_ENDPOINT: str = "/graphql"
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    RELOAD: bool = Field(default=True, env="RELOAD")
    
    # API Key Settings (for authentication)
    API_KEY_ENABLED: bool = Field(default=False, env="API_KEY_ENABLED")
    API_KEY: Optional[str] = Field(default=None, env="API_KEY")
    API_KEY_HEADER: str = "X-API-Key"
    
    # Database Settings
    DATABASE_PATH: Path = Field(
        default=BASE_DIR / "data" / "indian_banks.db",
        env="DATABASE_PATH"
    )
    DATABASE_URL: str = Field(default="", env="DATABASE_URL")
    
    # CORS Settings
    CORS_ORIGINS: list[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Build DATABASE_URL from DATABASE_PATH if not explicitly set
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"sqlite:///{self.DATABASE_PATH}"
    
    @property
    def db_path_str(self) -> str:
        """Get database path as string"""
        return str(self.DATABASE_PATH)
    
    def validate_database(self) -> bool:
        """Check if database file exists"""
        return self.DATABASE_PATH.exists()


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
