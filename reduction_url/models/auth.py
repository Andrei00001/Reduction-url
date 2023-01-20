from sqlalchemy import Column, Integer, String, Boolean, DateTime

from reduction_url.models import Base


class User(Base):
    __tablename__ = "auth_user"

    id: int = Column(Integer, primary_key=True)
    password: str = Column(String(length=128), nullable=False)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    username: str = Column(String(length=64), nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_staff: bool = Column(Boolean, default=False, nullable=False)

    last_login = Column(DateTime, nullable=True)
    date_joined = Column(DateTime, nullable=True)

    prefix: str = Column(String(length=12), unique=True, index=True, nullable=False)