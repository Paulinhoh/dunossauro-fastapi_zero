from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        # criando um novo usuario
        new_user = User(
            username='alice', email='alice@test.com', password='senha_segura'
        )

        # adicionando o usuario no banco e salvando
        session.add(new_user)
        session.commit()

        # recuperando os dados salvos no banco
        user = session.scalar(select(User).where(User.username == 'alice'))

    # fazendo os asserts para saber se os dados foram salvos corretamente
    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@test.com',
        'password': 'senha_segura',
        'created_at': time,
        'updated_at': time,
    }
