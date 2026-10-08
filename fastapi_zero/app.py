from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

# task run --host 0.0.0.0 -> para servir o servidor em rede (ip_do_host:8000)
app = FastAPI(title='Minha API Bala')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get(
    '/exercicio-html/', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def exercicio_aula_02():
    return '<h1>Olá, mundo!</h1>'


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
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
        password=user.password,
        # faz a mesma coisa que as linhas de cima em uma só
        # **user.model_dump(),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    db_users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': db_users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    return db_user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists.',
        )

    return db_user


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}
