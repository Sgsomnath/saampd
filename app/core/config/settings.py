from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Info
    app_name: str
    admin_email: str
    items_per_user: int

    # Database Config
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # JWT Auth Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Email Config (Only required fields for FastAPI-Mail)
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_starttls: bool
    mail_ssl_tls: bool

    class Config:
        env_file = ".env"

settings = Settings()
