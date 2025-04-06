# app/admin/schemas.py

from pydantic import BaseModel, EmailStr

# ✅ Input schema for registration
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# ✅ Input schema for login
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ Output schema for admin details
class AdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
