from pydantic import BaseModel, EmailStr, Field


# ✅ Input schema for admin registration
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str  # user will submit this as 'mobile'


# ✅ Input schema for admin login
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# ✅ Output schema for admin profile/details
class AdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str = Field(..., alias="mobile")  # map DB's phone_number to mobile

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # allows `mobile` as field name in output


# ✅ Output schema for JWT token after login
class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
