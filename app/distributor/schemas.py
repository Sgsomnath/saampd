from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ GET Profile Response Schema
class DistributorProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str]
    company: Optional[str]
    avatar: Optional[str]

    class Config:
        from_attributes = True  # ORM compatible


# ✅ PUT Profile Update Schema
class DistributorProfileUpdate(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    company: Optional[str]


# ✅ PUT Change Password Schema
class DistributorChangePassword(BaseModel):
    old_password: str
    new_password: str
