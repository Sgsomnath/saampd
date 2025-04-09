# app/core/config/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "welcome to STARSAAMPD MF DISTRIBUTORS LLP"
    admin_email: str = "admin@saampd.com"
    items_per_user: int = 50

    # Database Config
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        case_sensitive = False  # .env ফাইলের uppercase variable read করতে দিবে


settings = Settings()
