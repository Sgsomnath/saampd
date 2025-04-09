# app/admin/crud.py

from sqlalchemy.orm import Session
from app.admin import schemas
from app.core.models import Admin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ✅ Create a new admin user
def create_admin(db: Session, admin: schemas.AdminCreate) -> Admin:
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# ✅ Get admin by email
def get_admin_by_email(db: Session, email: str) -> Admin | None:
    return db.query(Admin).filter(Admin.email == email).first()


# ✅ Get all admins (with pagination support)
def get_admins(db: Session, skip: int = 0, limit: int = 100) -> list[Admin]:
    return db.query(Admin).offset(skip).limit(limit).all()
