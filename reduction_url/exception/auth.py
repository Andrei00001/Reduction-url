from fastapi import HTTPException
from fastapi import status


def validate_token_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={
            'WWW-Authenticate': 'Bearer'
        },
    )


def authenticate_user_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={
            'WWW-Authenticate': 'Bearer'
        },
    )
