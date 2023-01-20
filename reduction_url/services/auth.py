from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from requests import Request
from sqlalchemy import select

from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION
from reduction_url.connection_db import Session
from reduction_url.exception.auth import validate_token_exception, authenticate_user_exception
from reduction_url.schemas.auth import User as SchemasUser, Token, UserCreate
from reduction_url.models import User


class AuthService:

    @classmethod
    async def register_user(cls, user_data: UserCreate) -> Token:
        async with Session() as session:
            user = User(
                username=user_data.username,
                email=user_data.email,
                password=cls._hash_password(user_data.password),
                prefix=user_data.prefix,
            )
            session.add(user)
            await session.commit()
        return await cls._create_token(user)

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Token:
        query = select(User).filter(User.username == username)
        async with Session() as session:
            user = await session.execute(query)
            user = user.scalar()

        if not user:
            raise authenticate_user_exception()

        if not cls._verify_password(password, user.password):
            raise authenticate_user_exception()

        return await cls._create_token(user)

    @classmethod
    async def get_current_user(cls, request: Request) -> Optional[User]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return None
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() != "bearer":
            return None
        return cls._validate_token(param)

    @staticmethod
    def _verify_password(plain_password: str, hash_password: str) -> bool:
        return bcrypt.verify(plain_password, hash_password)

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def _validate_token(token: str) -> SchemasUser:
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                JWT_ALGORITHM,
            )
        except JWTError:
            raise validate_token_exception()

        user_data = payload.get('user')

        try:
            user = SchemasUser.parse_obj(user_data)
        except ValidationError:
            raise validate_token_exception()

        return user

    @staticmethod
    async def _create_token(user: User) -> Token:
        user_data = SchemasUser.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=JWT_EXPIRATION),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }

        token = jwt.encode(
            payload,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

        return Token.parse_obj({"access_token": token})
