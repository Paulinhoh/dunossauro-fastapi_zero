from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Arrage
    # client = TestClient(app)

    # Act
    response = client.get('/')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_exercicio_ola_mundo_em_html(client):
    response = client.get('/exercicio-html/')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá, mundo!</h1>' in response.text


# post
def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'senha_segura',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_create_user_should_return_409_username_exists__exercicio(
        client, user
):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'senha_segura',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_should_return_409_email_exists__exercicio(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice B.',
            'email': user.email,
            'password': 'senha_segura',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists.'}


# get
def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# update
def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'senha_segura',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'senha_segura',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user_integrity_error(client, user):
    # inserindo um usuario
    client.post(
        '/users/',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'senha_segura',
        },
    )

    # alterando o user das fixture para o Bob
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'nova_senha_segura',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists.'
    }


# get by id
def test_read_user_by_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_user_by_id_not_found(client):
    response = client.get('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


# delete
def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted!',
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
