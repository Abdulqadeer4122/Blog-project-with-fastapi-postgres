import uuid
from typing import Union, Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from api.schemas.token_schema import TokenData
from api.database import get_db
from sqlalchemy.orm import Session
from api.models.user_model import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict[str, Union[str, int, uuid.UUID]], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    to_encode.update({"exp": expire})
    for key, value in to_encode.items():
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


async def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
        return token_data
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    token_data = await verify_access_token(token)
    user = db.query(User).filter(User.id == token_data.id).first()
    return user
