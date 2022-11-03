from uuid import uuid4

from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from starlette.responses import RedirectResponse

from connection_db import async_session
from database.models import URL

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.post("/")
async def set_reduction_url(request: Request, data=Body()):
    reduction_url = await create_reduction_url(str(request.url))
    async with async_session() as session:
        session.add(URL(
            url=data.get('url') if isinstance(data, dict) else data,
            reduction_url=reduction_url
        ))
        await session.commit()
        await session.close()


@app.get("/sh/{id}", response_class=HTMLResponse)
async def get_reduction_url(request: Request, id:str):
    async with async_session() as session:
        query = select(
            URL
        ).where(
            URL.reduction_url == str(request.url)
        )
        obj = await session.execute(query)
        obj_url = obj.scalars().first().url
        return RedirectResponse(obj_url)


async def create_reduction_url(host):
    return f"{host}sh/{str(uuid4())[0:6]}"
