from sqlalchemy.orm import declarative_base

Base = declarative_base()

from ..models.auth import User
from ..models.operations import URL