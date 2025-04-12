from pydantic import BaseModel, EmailStr


# ✅ Input schema for admin registration
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str  # ✅ Required mobile field


# ✅ Input schema for admin login
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# ✅ Output schema for admin profile/details
class AdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: str

    class Config:
        from_attributes = True  # ORM compatibility


# ✅ Output schema for JWT token after login
class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
