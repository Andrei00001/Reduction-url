from pydantic import BaseModel


class ResponseURL(BaseModel):
    url: str


class RequestURL(BaseModel):
    url: str
