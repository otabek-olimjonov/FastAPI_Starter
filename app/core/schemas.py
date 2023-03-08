from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime, timedelta

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Login(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserReturn(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True