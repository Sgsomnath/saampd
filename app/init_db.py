from app.database import Base, engine
from app.admin.models import Admin  # Import all models here

print("🔄 Creating tables...")

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully.")
