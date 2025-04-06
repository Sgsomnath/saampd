# app/core/config/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SAAMPD"
    admin_email: str = "admin@saampd.com"
    items_per_user: int = 50

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
