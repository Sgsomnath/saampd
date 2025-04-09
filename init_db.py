# init_db.py

from app.core.database.base import Base
from app.core.database.session import engine

# ⬇️ Import all models to ensure they're registered with SQLAlchemy's metadata
from app.core.models import (
    admin,
    distributor,
    investor,
    scheme,
    transaction
)

print("🔄 Creating tables...")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully.")
