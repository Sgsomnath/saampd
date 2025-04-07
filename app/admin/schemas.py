# app/admin/schemas.py

from pydantic import BaseModel, EmailStr

# Input schema for admin registration
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Input schema for admin login
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# Output schema for admin details
class AdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Output schema for admin login response
class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
