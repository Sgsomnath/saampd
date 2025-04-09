from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database.dependency import get_db
from app.core.models.investor import Investor

# ✅ Schemas
from app.investor.schemas import (
    InvestorCreate,
    InvestorLogin,
    InvestorResponse,
    InvestorLoginResponse
)

# ✅ Auth tools
from jwt_auth.password_handler import get_password_hash, verify_password
from jwt_auth.token_handler import create_access_token

router = APIRouter(prefix="/investor", tags=["Investor"])


# 🔹 Investor Home
@router.get("/")
def investor_home():
    return {"message": "Welcome to the Investor API"}


# 🔐 Register Investor
@router.post("/register", response_model=InvestorResponse)
def register_investor(investor: InvestorCreate, db: Session = Depends(get_db)):
    try:
        existing_investor = db.query(Investor).filter(Investor.email == investor.email).first()
        if existing_investor:
            raise HTTPException(status_code=400, detail="Investor with this email already exists.")

        hashed_password = get_password_hash(investor.password)

        new_investor = Investor(
            name=investor.name,
            email=investor.email,
            hashed_password=hashed_password
        )
        db.add(new_investor)
        db.commit()
        db.refresh(new_investor)
        return new_investor

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔐 Login Investor
@router.post("/login", response_model=InvestorLoginResponse)
def login_investor(investor: InvestorLogin, db: Session = Depends(get_db)):
    db_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if not db_investor:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(investor.password, db_investor.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": str(db_investor.id), "role": "investor"})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
