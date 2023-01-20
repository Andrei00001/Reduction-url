from base64 import b64encode
from typing import Optional

from sqlmodel import select

from reduction_url.connection_db import Session
from reduction_url.models import URL
from reduction_url.schemas.auth import User


class OptionalService:
    @staticmethod
    async def create_reduction_url(host: str, user: Optional[User]):
        query = select(URL).order_by(-URL.id).limit(1)
        async with Session() as session:
            obj = await session.execute(query)
            obj = obj.scalar()
            last_id = 0 if not obj else obj.id
        prefix = 'anonymous' if user is None else user.prefix
        return f"{host}{prefix}/{b64encode(str(last_id).encode('ascii')).decode('utf-8')}"
