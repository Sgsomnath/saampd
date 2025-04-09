# init_db.py

from app.core.database.base import Base
from app.core.database.session import engine

# ✅ Explicit imports to register models with SQLAlchemy metadata
from app.core.models.admin import Admin
from app.core.models.distributor import Distributor
from app.core.models.investor import Investor
from app.core.models.scheme import Scheme
from app.core.models.transaction import Transaction

def init_db():
    print("📦 Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    init_db()
