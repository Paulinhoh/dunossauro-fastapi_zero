from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_password_hash
from fastapi_zero.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as cient:
        app.dependency_overrides[get_session] = get_session_override
        yield cient

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
# o *, é somente a forçar a escrever model=<modelo> e não somente <modelo>
def _mock_db_time(*, model, time=datetime.now()):
    def fake_time_hook(mapper, conection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = 'senha_segura'
    user = User(
        username='Alice',
        email='alice@example.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # atributo somenete em tempo de execução para o teste do token jwt
    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    repsonse = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return repsonse.json()['access_token']


@pytest.fixture
def settings():
    settings = Settings()
    return settings
