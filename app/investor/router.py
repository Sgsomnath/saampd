from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database.dependency import get_db
from app.core.models.investor import Investor
from jwt_auth.password_handler import hash_password, verify_password
from jwt_auth.token_handler import create_access_token

router = APIRouter(prefix="/investor", tags=["Investor"])

# Schemas
class InvestorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class InvestorLogin(BaseModel):
    email: EmailStr
    password: str

class InvestorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

# Routes
@router.get("/")
def investor_home():
    return {"message": "Welcome to the Investor API"}

@router.post("/register", response_model=InvestorResponse)
def register_investor(investor: InvestorCreate, db: Session = Depends(get_db)):
    existing_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if existing_investor:
        raise HTTPException(status_code=400, detail="Investor with this email already exists.")

    hashed_password = hash_password(investor.password)
    new_investor = Investor(
        name=investor.name,
        email=investor.email,
        password=hashed_password
    )
    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)
    return new_investor

@router.post("/login")
def login_investor(investor: InvestorLogin, db: Session = Depends(get_db)):
    db_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if not db_investor:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(investor.password, db_investor.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": db_investor.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
