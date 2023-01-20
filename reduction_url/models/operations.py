from sqlalchemy import Column, Integer, String, Date

from reduction_url.models import Base


class URL(Base):
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    reduction_url = Column(String, unique=True)
    expired_at = Column(Date, nullable=True)

    def __repr__(self):
        return "".format(self.code)
