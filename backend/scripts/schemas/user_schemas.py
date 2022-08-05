from typing import Any, Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr


class UserRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    profilePicture: Optional[str] = ""
    coverPicture: Optional[str] = ""
    followers: Optional[list] = []
    following: Optional[list] = []
    desc: Optional[str] = ""
    location: Optional[str] = ""

class UpdateUserData(BaseModel):
    username: str
    email: EmailStr
    profilePicture: Optional[str] = ""
    coverPicture: Optional[str] = ""
    desc: Optional[str] = ""
    location: Optional[str] = ""

class DefaultResponse(BaseModel):
    status: str = "Failed"
    message: Optional[str]
    data: Optional[Any]


class ResponseModel(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
