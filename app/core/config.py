from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    app_title: str
    app_description: str

    class Config:
        env_file = '.env'


settings = Settings()
