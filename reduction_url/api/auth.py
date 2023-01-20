from fastapi import APIRouter, Depends

from ..schemas.auth import (
    UserCreate,
    Token, UserLogin
)
from ..services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register', response_model=Token)
async def register(
        user_data: UserCreate,
        service: AuthService = Depends()
):

    return await service.register_user(user_data)


@router.post('/login', response_model=Token)
async def login(
        form_data: UserLogin,
        service: AuthService = Depends()
):
    return await service.authenticate_user(
        form_data.username,
        form_data.password,
    )

