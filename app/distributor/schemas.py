from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# 🔹 Distributor Registration Schema
class DistributorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    arn_code: str  # AMFI ARN code

    phone_number: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    pan_number: Optional[str]
    aadhar_number: Optional[str]

    # Address fields
    village_or_town: Optional[str]
    landmark: Optional[str]
    house_number: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]

# 🔹 Login Schema
class DistributorLogin(BaseModel):
    email: EmailStr
    password: str

# 🔹 JWT Login Response
class DistributorLoginResponse(BaseModel):
    access_token: str
    token_type: str

# 🔹 Full Profile View
class DistributorProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str]
    arn_code: str

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

    avatar_url: Optional[str]
    payout_details: Optional[str]

    class Config:
        from_attributes = True  # ✅ ORM compatible

# 🔹 Profile Update Schema
class DistributorProfileUpdate(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
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

# 🔐 Change Password Schema
class DistributorChangePassword(BaseModel):
    old_password: str
    new_password: str
