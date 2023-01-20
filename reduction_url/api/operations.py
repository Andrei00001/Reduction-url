from typing import Optional

from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from starlette.responses import HTMLResponse, RedirectResponse

from reduction_url.connection_db import Session
from reduction_url.models import URL
from reduction_url.schemas.auth import User
from reduction_url.schemas.operations import ResponseURL, RequestURL
from reduction_url.services.auth import AuthService
from reduction_url.services.operations import OptionalService

router = APIRouter(
    prefix='/url',
    tags=['Operation']
)


@router.post("/", response_model=RequestURL)
async def set_reduction_url(request: Request, url: ResponseURL):
    user: Optional[User] = AuthService.get_current_user(request)
    reduction_url = await OptionalService.create_reduction_url(str(request.url), user)
    async with Session() as session:
        session.add(URL(
            url=url.url,
            reduction_url=reduction_url
        ))
        await session.commit()
    return RequestURL(url=reduction_url)


@router.get("/{prefix}/{code}", response_class=HTMLResponse)
async def get_reduction_url(request: Request):
    query = select(URL).where(URL.reduction_url == str(request.url))
    async with Session() as session:
        obj = await session.execute(query)
        obj_url = obj.scalar().url
    return RedirectResponse(obj_url)
