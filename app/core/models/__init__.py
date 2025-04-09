# init_db.py

from app.core.database.base import Base
from app.core.database.session import engine
from app.core.models import *  # সব মডেল একসাথে import হচ্ছে

def init_db():
    print("📦 Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    init_db()
