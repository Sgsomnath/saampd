from pydantic import BaseModel, EmailStr


# 🔹 Input schema for investor registration
class InvestorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# 🔹 Input schema for investor login
class InvestorLogin(BaseModel):
    email: EmailStr
    password: str


# 🔹 Output schema for investor details (after register/login)
class InvestorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Pydantic v2 compatible
        # orm_mode = True ← Pydantic v1 use করলে এটা রাখতাম


# 🔹 Output schema for login response with JWT
class InvestorLoginResponse(BaseModel):
    access_token: str
    token_type: str
