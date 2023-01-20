from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: str
    prefix: str


class UserName(BaseModel):
    username: str


class UserPassword(BaseModel):
    password: str


class UserCreate(BaseUser, UserName, UserPassword):
    pass


class UserLogin(UserName, UserPassword):
    pass


class User(BaseUser, UserName):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_superuser: bool
    is_staff: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type = 'bearer'
