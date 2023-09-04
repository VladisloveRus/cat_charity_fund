from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'

    class Config:
        env_file = '.env'


settings = Settings()
