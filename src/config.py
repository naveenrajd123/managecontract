"""
Configuration Management
This file manages all settings for the application, loading from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Pydantic automatically loads these from .env file.
    """
    
    # Google Gemini API Configuration
    GEMINI_API_KEY: str
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./contracts.db"
    
    # Application Settings
    APP_NAME: str = "Contract Management System"
    DEBUG: bool = True
    
    # Vector Database Settings
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_data"
    
    # File Upload Settings
    UPLOAD_DIRECTORY: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".txt", ".docx"}
    STORE_FILES: bool = True  # Set to False for free tier (stores text in DB instead)
    
    # Early Warning Settings (days before expiration)
    WARNING_DAYS_CRITICAL: int = 30  # Red alert
    WARNING_DAYS_WARNING: int = 90   # Yellow alert
    WARNING_DAYS_INFO: int = 180     # Blue alert
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
