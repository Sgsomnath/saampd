# app/core/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.db_config import db_settings

SQLALCHEMY_DATABASE_URL = db_settings.database_url()  # No parentheses

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
