from fastapi import FastAPI

from app.auth.auth_config import auth_backend, fastapi_users
from app.auth.schemas import UserRead, UserCreate
from app.url_operations.router import router as router_url
app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    router_url
)
