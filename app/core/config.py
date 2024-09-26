import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env.docker')


settings = Settings()
