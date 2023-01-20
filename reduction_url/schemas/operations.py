from datetime import date
from typing import Union

from pydantic import BaseModel


class ResponseURL(BaseModel):
    url: str


class RequestURL(BaseModel):
    url: str
    expired_at: Union[date, str] = "for life"
