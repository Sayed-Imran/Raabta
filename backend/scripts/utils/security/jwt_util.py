from typing import Dict
from xmlrpc.client import Boolean
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ...schemas.tokenschema import TokenData

# from pydantic import EmailStr
from scripts.constants.secrets import Secrets
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import status


class JWT:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self) -> None:
        self.max_login_age = Secrets.LOCK_OUT_TIME_MINS
        self.unique_key = Secrets.UNIQUE_KEY
        self.algo = Secrets.ALG

    def create_token(self, data: Dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.max_login_age)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, key=self.unique_key, algorithm=self.algo)

    def verify_admin(self, token: str, credential_exception):
        try:
            payload = jwt.decode(token, Secrets.UNIQUE_KEY, algorithms=[Secrets.ALG])
            role: Boolean = payload.get("Admin")
            if not role :
                raise credential_exception
            token_data = TokenData(Admin=role)
            return token_data
        except JWTError:
            raise credential_exception

    def verify_token(self, token: str, credential_exception):
        try:

            payload = jwt.decode(token, Secrets.UNIQUE_KEY, algorithms=[Secrets.ALG])
            role: Boolean = payload.get("Admin")
            email: str = payload.get("email")
            user_id: int = payload.get("user_id")
            
            
            if role is None:
                raise credential_exception
            token_data = {"Admin":role,"email":email,"user_id":user_id}
            return token_data
        except JWTError:
            raise credential_exception

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could Not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return self.verify_token(token, credential_exception=credential_exception)

    def get_admin_user(self, token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not allowed to access this page",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return self.verify_admin(token, credential_exception=credential_exception)
