from pydantic import BaseModel, EmailStr
from typing import Optional


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
    mobile: Optional[str] = None
    dob: Optional[str] = None
    pan: Optional[str] = None
    kyc_status: Optional[str] = None
    fatca_status: Optional[str] = None
    nomination_status: Optional[str] = None

    class Config:
        from_attributes = True  # ORM to Pydantic conversion


# 🔹 Output schema for login response with JWT
class InvestorLoginResponse(BaseModel):
    access_token: str
    token_type: str


# 🔹 Input schema for profile update
class InvestorProfileUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[str]
    dob: Optional[str]
    pan: Optional[str]
    kyc_status: Optional[str]
    fatca_status: Optional[str]
    nomination_status: Optional[str]


# 🔹 Output schema for full profile view
class InvestorProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[str] = None
    dob: Optional[str] = None
    pan: Optional[str] = None
    kyc_status: Optional[str] = None
    fatca_status: Optional[str] = None
    nomination_status: Optional[str] = None

    class Config:
        from_attributes = True
