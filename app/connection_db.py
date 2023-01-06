from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from repositories.db import DBRepositories

Base = declarative_base()
engine = DBRepositories.base_config()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
