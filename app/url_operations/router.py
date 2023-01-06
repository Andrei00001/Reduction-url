from base64 import b64encode

from fastapi import APIRouter, Request, Body
from sqlalchemy import insert, select
from starlette.responses import HTMLResponse, RedirectResponse

from app.connection_db import async_session
from app.url_operations.models import url

router = APIRouter(
    prefix='/url',
    tags=['Operation']
)


@router.post("/")
async def set_reduction_url(request: Request, data=Body()):
    reduction_url = await create_reduction_url(str(request.url))
    async with async_session() as session:
        stmt = insert(url).values(
            url=data.get('url') if isinstance(data, dict) else data,
            reduction_url=reduction_url)
        await session.execute(stmt)
        await session.commit()
    return reduction_url
...

@router.get("/sh/{code}", response_class=HTMLResponse)
async def get_reduction_url(request: Request):
    query = select(url).where(url.c.reduction_url == str(request.url))
    async with async_session() as session:
        obj = await session.execute(query)
        obj_url = obj.first().url
    return RedirectResponse(obj_url)


async def create_reduction_url(host):
    query = select(url).order_by(-url.c.id).limit(1)
    async with async_session() as session:
        obj = await session.execute(query)
        obj = obj.first()
        last_id = '0' if not obj else str(obj.id)
    return f"{host}sh/{b64encode(last_id.encode('ascii')).decode('utf-8')}"
