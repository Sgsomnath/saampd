# scripts/db/init_db.py

from app.core.database.base import Base
from app.core.database.session import engine

# 🔄 সকল মডেল import করতে হবে যাতে তারা Base এর সঙ্গে register হয়
from app.core.models import user
from app.core.models import distributor
from app.core.models import investor
from app.core.models import transaction
from app.core.models import scheme
# প্রয়োজন অনুযায়ী আরও model import করো...

def init_db():
    print("🔧 Initializing the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")

if __name__ == "__main__":
    init_db()
