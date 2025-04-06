from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/client", tags=["Client"])

# Input schemas
class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ClientLogin(BaseModel):
    email: EmailStr
    password: str

# Routes
@router.get("/")
def client_home():
    return {"message": "Client API Home"}

@router.post("/register")
def register_client(client: ClientCreate):
    # Dummy logic for now
    return {"message": f"Client {client.name} registered successfully!"}

@router.post("/login")
def login_client(client: ClientLogin):
    # Dummy logic for now
    return {"message": f"Login attempted for client {client.email}"}
