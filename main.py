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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('geniral.html', {'request': request})


@app.post("/", response_class=HTMLResponse)
async def root2(request: Request, data=Body()):
    reduction_url = await get_reduction_url()
    async with async_session() as session:
        session.add(URL(
            url=data.get('url'),
            reduction_url=reduction_url
        ))
        await session.commit()
        await session.close()
    return templates.TemplateResponse('geniral.html', {'request': request, 'url': reduction_url})


@app.get("/sh/{id}", response_class=HTMLResponse)
async def root3(request: Request, id: str):
    base_url = await get_local_url()
    async with async_session() as session:
        query = select(
            URL
        ).where(
            URL.reduction_url == base_url + f'sh/{id}'
        )
        obj = await session.execute(query)
        obj_url = obj.scalars().first().url
        return RedirectResponse(obj_url)


async def get_reduction_url():
    local = await get_local_url()
    return f"{local}sh/{str(uuid4())[0:6]}"


async def get_local_url():
    return f"http://127.0.0.1:8000/"
