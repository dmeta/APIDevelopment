from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostInput(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class UserCreateOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True



class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True



class UpdatePost(PostInput):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateOutput
    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
