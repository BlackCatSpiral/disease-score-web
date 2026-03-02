from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "test"
    DB_CHARSET: str = "utf8mb4"
    
    # 应用配置
    APP_NAME: str = "病种分值管理系统"
    DEBUG: bool = True
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
