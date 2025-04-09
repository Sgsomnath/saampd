from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.jwt_auth import password_handler
from app.auth import create_access_token
from app.core.database.session import get_db
from app.core.models.investor import Investor
from app.model.schemas import InvestorCreate, InvestorLogin, InvestorResponse

investor_router = APIRouter(prefix="/investor", tags=["Investor"])

# Routes
@investor_router.get("/")
def investor_home():
    return {"message": "Welcome to the Investor API"}

@investor_router.post("/register", response_model=InvestorResponse)
def register_investor(investor: InvestorCreate, db: Session = Depends(get_db)):
    # Check if the investor already exists
    existing_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if existing_investor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Investor with this email already exists."
        )

    # Hash the password and create a new investor
    hashed_password = password_handler.get_password_hash(investor.password)
    new_investor = Investor(
        name=investor.name,
        email=investor.email,
        mobile=investor.mobile,
        password=hashed_password
    )
    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)
    return new_investor

@investor_router.post("/login")
def login_investor(investor: InvestorLogin, db: Session = Depends(get_db)):
    # Check if the investor exists
    db_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if not db_investor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")

    # Verify the password
    if not password_handler.verify_password(investor.password, db_investor.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # Generate a token
    token = create_access_token(data={"sub": db_investor.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
