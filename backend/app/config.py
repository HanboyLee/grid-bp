"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = Field(default="sqlite:///./trading_bot.db", alias="DATABASE_URL")
    
    # Backpack API
    backpack_api_key: str = Field(default="", alias="BACKPACK_API_KEY")
    backpack_secret_key: str = Field(default="", alias="BACKPACK_SECRET_KEY")
    backpack_api_url: str = Field(default="https://api.backpack.exchange", alias="BACKPACK_API_URL")
    backpack_ws_url: str = Field(default="wss://ws.backpack.exchange", alias="BACKPACK_WS_URL")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
