from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str


# alembic init migrations  -> para iniciar os migrations

# alembic revision --autogenerate -m "create users table"  ->  criar uma
# nova versão da migration em um arquivo .py

# alembic upgrade head  -> aplica a ultima versão da migration
# alembic downgrade -1 -> volta uma versão da migrations
# alembic downgrade <version> -> volta para a versão escolhida da migrations
