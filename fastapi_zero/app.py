import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.routers import auth, todo, users
from fastapi_zero.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Minha API Bala')
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá, mundo!'}


@app.get(
    '/exercicio-html/', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
async def exercicio_aula_02():
    return '<h1>Olá, mundo!</h1>'

# task run --host 0.0.0.0 -> para servir o servidor em rede (ip_do_host:8000)
