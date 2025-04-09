from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update with your actual PostgreSQL credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/saampd_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the create_database function
def create_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("CREATE DATABASE saampd_db"))
    except Exception as e:
        print(f"Database creation failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Comment this out after the database is created
# create_database()

# List all tables in the database
def list_tables():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            for row in result:
                print(row)
    except Exception as e:
        print(f"Failed to list tables: {e}")

# Create all tables
Base.metadata.create_all(bind=engine)

list_tables()

from sqlalchemy import Column, Integer, String
from app.database import Base
from app.admin.models import Admin

class Admin(Base):
    __tablename__ = "admins"
    __table_args__ = {"extend_existing": True}  # Prevent redefinition error

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.admin.models import Admin
from app.admin.schemas import AdminCreate, AdminResponse
from app.utils import get_password_hash
import logging

router = APIRouter(prefix="/admin", tags=["Admin"])

logger = logging.getLogger(__name__)

@router.post("/register", response_model=AdminResponse)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registering admin: {admin.email}")
        existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="Admin with this email already exists.")

        hashed_password = get_password_hash(admin.password)
        new_admin = Admin(name=admin.name, email=admin.email, password=hashed_password)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception as e:
        logger.error(f"Error registering admin: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Predefined admin data
predefined_admin = {
    "id": 1,
    "name": "Somnath Admin",
    "email": "admin@saampd.com"
}
