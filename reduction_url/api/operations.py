from datetime import date, timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Request, Query, Cookie, Form, File, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from sqlalchemy import select
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from reduction_url.connection_db import Session
from reduction_url.models import URL
from reduction_url.schemas.auth import User
from reduction_url.schemas.operations import ResponseURL, RequestURL
from reduction_url.services.auth import AuthService
from reduction_url.services.operations import OperationService

router = APIRouter(
    prefix='/url',
    tags=['Operation']
)

anonymous_prefix = 'anonymous'


@router.post("/", response_model=RequestURL)
async def set_reduction_url(request: Request, data_url: ResponseURL):
    user: Optional[User] = await AuthService.get_current_user(request)
    prefix = OperationService.get_prefix(anonymous_prefix, user)
    reduction_url = await OperationService.create_reduction_url(str(request.url), prefix)

    url = URL(
        url=data_url.url,
        reduction_url=reduction_url
    )
    request = RequestURL(url=reduction_url)
    if prefix is anonymous_prefix:
        url.expired_at = date.today() + timedelta(days=30)
        request.expired_at = url.expired_at

    async with Session() as session:
        session.add(url)
        await session.commit()
    return request


@router.get("/{prefix}/{code}", response_class=HTMLResponse)
async def get_reduction_url(request: Request):
    query = select(URL).where(URL.reduction_url == str(request.url))
    async with Session() as session:
        obj = await session.execute(query)
        obj_url = obj.scalar().url
    return RedirectResponse(obj_url)


# class FixedContentQueryChecker:
#     def __init__(self, fixed_content: str):
#         self.fixed_content = fixed_content
#
#     def __call__(self, q: str = ""):
#         if q:
#             return self.fixed_content in q
#         return False
#
#
# checker = FixedContentQueryChecker("bar")
#
#
# @router.get("/query-checker/")
# async def read_query_check(fixed_content_included: bool = Depends(checker)):
#     return {"fixed_content_in_query": fixed_content_included}