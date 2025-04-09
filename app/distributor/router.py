from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database.dependency import get_db
from app.core.models.distributor import Distributor
from jwt_auth.password_handler import hash_password, verify_password
from jwt_auth.token_handler import create_access_token

router = APIRouter(prefix="/distributor", tags=["Distributor"])

# Schemas
class DistributorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class DistributorLogin(BaseModel):
    email: EmailStr
    password: str

class DistributorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

# Routes
@router.get("/")
def distributor_home():
    return {"message": "Distributor API Home"}

@router.post("/register", response_model=DistributorResponse)
def register_distributor(distributor: DistributorCreate, db: Session = Depends(get_db)):
    existing_distributor = db.query(Distributor).filter(Distributor.email == distributor.email).first()
    if existing_distributor:
        raise HTTPException(status_code=400, detail="Distributor with this email already exists.")

    hashed_password = hash_password(distributor.password)
    new_distributor = Distributor(
        name=distributor.name,
        email=distributor.email,
        password=hashed_password
    )
    db.add(new_distributor)
    db.commit()
    db.refresh(new_distributor)
    return new_distributor

@router.post("/login")
def login_distributor(distributor: DistributorLogin, db: Session = Depends(get_db)):
    db_distributor = db.query(Distributor).filter(Distributor.email == distributor.email).first()
    if not db_distributor:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(distributor.password, db_distributor.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": db_distributor.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
