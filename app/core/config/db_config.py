# app/core/config/db_config.py

from pydantic import BaseModel
import os

class DBSettings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "your_password")
    DB_NAME: str = os.getenv("DB_NAME", "saampd")

    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

db_settings = DBSettings()
