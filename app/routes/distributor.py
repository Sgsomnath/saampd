from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/distributor", tags=["Distributor"])

# Input schemas
class DistributorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class DistributorLogin(BaseModel):
    email: EmailStr
    password: str

# Routes
@router.get("/")
def distributor_home():
    return {"message": "Distributor API Home"}

@router.post("/register")
def register_distributor(distributor: DistributorCreate):
    # Dummy logic for now
    return {"message": f"Distributor {distributor.name} registered successfully!"}

@router.post("/login")
def login_distributor(distributor: DistributorLogin):
    # Dummy logic for now
    return {"message": f"Login attempted for distributor {distributor.email}"}
