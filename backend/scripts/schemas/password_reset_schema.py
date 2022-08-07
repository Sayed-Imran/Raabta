from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    email: EmailStr


class PasswordScheme(BaseModel):
    new_passwd: str
    conf_passwd: str
