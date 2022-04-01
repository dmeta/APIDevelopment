from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

from pydantic.types import conint

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

#class PostOut(PostInput): 
#    Post: UpdatePost
#    votes: int
#    class Config:
#        orm_mode = True

class PostOut(BaseModel): 
    Post: UpdatePost
    votes: int
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

class Vote(BaseModel):
    post_id: int
    dir: conint (le=1)
