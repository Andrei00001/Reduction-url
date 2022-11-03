from connection_db import Base
from sqlalchemy import Column, Integer, String


class URL(Base):
    __tablename__ = 'app_url'

    id = Column(Integer, primary_key=True)
    url = Column('url', String)
    reduction_url = Column('reduction_url', String, unique=True)

    def __repr__(self):
        return "".format(self.code)
