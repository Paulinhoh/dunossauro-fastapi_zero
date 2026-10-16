from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()

AsyncSession = Annotated[AsyncSession, Depends(get_session)]
Oauth2 = Annotated[str, Depends(oauth2_scheme)]


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    # adiciona um tempo de 30 minutos para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encode_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encode_jwt


async def get_current_user(
    session: AsyncSession,
    token: Oauth2,
):
    credetials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credetials_exception
    except DecodeError:
        raise credetials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credetials_exception

    return user
