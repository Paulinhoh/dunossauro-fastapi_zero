from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

AsyncSession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: AsyncSession):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        # se der erro
        # Esta não é a melhor forma de se retornar este erro, pois da
        # informções demais sobre o que ja esta cadastrado
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
            )

    # se não der o erro
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        # faz a mesma coisa que as linhas de cima em uma só
        # **user.model_dump(),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: AsyncSession,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    db_users = await session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {'users': db_users}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user_by_id(
    user_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: AsyncSession,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    try:
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists.',
        )

    return current_user


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted!'}
