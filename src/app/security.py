from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

from src.app.api.v1.schemas.exceptions import (
    invalid_token_exception,
    credentials_exception,
)
from src.app.settings import settings
from src.app.api.v1.schemas.tokens import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    return verify_token(data)


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email, user_id, expires = (
            payload.get("sub"),
            payload.get("id"),
            payload.get("exp"),
        )
        if email is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        raise invalid_token_exception


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expires_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = 60 * 24 * 30  # 1 month
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt
