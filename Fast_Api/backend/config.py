# backend/config.py
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    APP_ENV: Literal["development", "production"] = "development"
    DEBUG: bool = True
    DB_HOST: str = "localhost"
    DB_PORT: int = 13306
    DB_USER: str = "root"
    DB_PASSWORD: str = "abc123"
    DB_NAME: str = "douban_movies"

    class Config:
        env_file = "../.env"


settings = Settings()


    

