import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class DBRepositories:

    @staticmethod
    def base_config(
            dialect: str = "postgresql",
            driver: str = "asyncpg",
            username: str = os.getenv('USERNAME'),
            password: str = os.getenv('PASSWORD'),
            host: str = "localhost",
            port: str = "5432",
            database_name: str = os.getenv('DATABASENAME'),
            echo: bool = True,
            pool_size: int = 10,
            max_overflow: int = 100,
            encoding: str = "utf8",
    ):
        connect_args: dict = {"server_settings": {"jit": "off"}}
        return create_async_engine(
            f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database_name}",
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            encoding=encoding,
            connect_args=connect_args
        ), f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database_name}"
