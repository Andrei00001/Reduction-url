from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from repositories.db import DBRepositories

engine = DBRepositories.base_config()[0]
Session = sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)
