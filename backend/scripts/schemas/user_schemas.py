from typing import Any, Optional
from pydantic import BaseModel, EmailStr


class UserRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    profilePicture: Optional[str] = ""
    coverPicture: Optional[str] = ""
    followers: Optional[list] = []
    followings: Optional[list] = []
    desc: Optional[str] = ""
    location: Optional[str] = ""

class UpdateUserData(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    profilePicture: Optional[str]
    coverPicture: Optional[str]
    desc: Optional[str]
    location: Optional[str]

class DefaultResponse(BaseModel):
    status: str = "Failed"
    message: Optional[str]
    data: Optional[Any]


class ResponseModel(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class GetUserResponse(BaseModel):
    user_id:str
    username:str
    email: EmailStr
    followers: list
    followings: list
    desc: str
    location: str
    profilePicture: str
    coverPicture: str