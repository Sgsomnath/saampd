from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import date


# 🔹 Input schema for investor registration
class InvestorCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: Annotated[str, Field(pattern="^(male|female)$")]
    mobile: Annotated[str, Field(pattern="^\d{10}$")]
    pan_number: str
    aadhar_number: str
    email: EmailStr
    password: str

    # Address details
    village_or_town: str
    landmark: str
    house_number: str
    district: str
    state: str
    country: str


# 🔹 Input schema for investor login
class InvestorLogin(BaseModel):
    email: EmailStr
    password: str


# 🔹 Output schema after registration/login
class InvestorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[str] = None

    class Config:
        from_attributes = True


# 🔹 Output schema for login response with JWT
class InvestorLoginResponse(BaseModel):
    access_token: str
    token_type: str


# 🔹 Input schema for profile update
class InvestorProfileUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    pan_number: Optional[str]
    aadhar_number: Optional[str]
    village_or_town: Optional[str]
    landmark: Optional[str]
    house_number: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]
    kyc_status: Optional[str]
    fatca_status: Optional[str]
    nomination_status: Optional[str]


# 🔹 Output schema for full profile view
class InvestorProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    pan_number: Optional[str]
    aadhar_number: Optional[str]
    village_or_town: Optional[str]
    landmark: Optional[str]
    house_number: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]
    kyc_status: Optional[str]
    fatca_status: Optional[str]
    nomination_status: Optional[str]

    class Config:
        from_attributes = True


# 🔐 Change password schema
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# 🔄 KYC/FATCA update schema
class KYCStatusUpdate(BaseModel):
    kyc_status: Optional[str]
    fatca_status: Optional[str]


# 🧾 Nominee info update schema
class NomineeUpdate(BaseModel):
    nomination_status: str
