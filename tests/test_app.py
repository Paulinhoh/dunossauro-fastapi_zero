from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA):
    - A: Arrage
    - A: Act
    - A: Assert
    """
    # Arrage
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}
