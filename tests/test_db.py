from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        # criando um usuario
        new_user = User(
            username='alice', email='alice@test.com', password='senha_segura'
        )

        # adicionando o usuario no banco e salvando
        session.add(new_user)
        await session.commit()

        # recuperando os dados salvos no banco
        user = await session.scalar(
            select(User).where(User.username == 'alice')
        )

    # fazendo os asserts para saber se os dados foram salvos corretamente
    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@test.com',
        'password': 'senha_segura',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


"""
@pytest.mark.asyncio
async def test_create_todo_error(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='test',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()

    with pytest.raises(LookupError):
        await session.scalar(select(Todo))
"""
