from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None
    Admin: Boolean = False