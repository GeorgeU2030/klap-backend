from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    profile_image: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile_image: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    profile_image: Optional[str]
    is_active: bool
    is_oauth: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
