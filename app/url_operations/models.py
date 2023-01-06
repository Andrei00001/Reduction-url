from app.connection_db import Base
from sqlalchemy import Column, Integer, String, MetaData, Table

metadata = MetaData()

url = Table(
    'url',
    metadata,
    Column('id', Integer, primary_key=True),
    Column("url", String),
    Column("reduction_url", String),
)


class URL(Base):
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True)
    url = Column('url', String)
    reduction_url = Column('reduction_url', String, unique=True)

    def __repr__(self):
        return "".format(self.code)
