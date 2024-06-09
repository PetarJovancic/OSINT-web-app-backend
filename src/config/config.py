import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")
    ALLOW_CREDENTIALS: bool =  bool(os.getenv('ALLOW_CREDENTIALS', True))
    ALLOW_METHODS: str = os.getenv('ALLOW_METHODS', "*")
    ALLOW_HEADERS: str =  os.getenv('ALLOW_HEADERS', "*")
    HOST: str = os.getenv('HOST', "0.0.0.0")
    PORT: int = int(os.getenv('PORT', 8000))
    RELOAD: bool = bool(os.getenv('RELOAD', True))


settings = Settings()