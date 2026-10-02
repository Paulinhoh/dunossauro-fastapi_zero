from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message

# task run --host 0.0.0.0 -> para servir o servidor em rede (ip_do_host:8000)
app = FastAPI(title='Minha API Bala')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get(
    '/exercicio-html', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def exercicio_aula_02():
    return '<h1>Olá, mundo!</h1>'
