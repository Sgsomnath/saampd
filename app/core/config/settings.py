from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "SAAMPD"
    admin_email: str = "admin@saampd.com"
    items_per_user: int = 50

settings = Settings()
