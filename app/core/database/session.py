# app/core/database/session.py
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from app.core.config.db_config import db_settings

SQLALCHEMY_DATABASE_URL = db_settings.database_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Added this new function (only addition)
def initialize_models():
    """Import all models here to register them with Base"""
    from app.admin.models import Admin  # noqa: F401
    # Add other models as needed
    # from app.distributor.models import Distributor  # noqa: F401