from fastapi.responses import HTMLResponse
from app.config import Config
from app.database import Cursor

from . import database as db
from .exceptions import AuthError, SignUpError
from .models import User
from .utils import (
    create_token,
    hash_password,
    verify_password,
    is_password_secure,
)


config = Config()


async def create_user(cursor: Cursor, username: str, password: str) -> None:
    hash = hash_password(password)
    await db.create_user(cursor, username, hash)


async def get_user(cursor: Cursor, username: str) -> User | None:
    db_reply = await db.get_user(cursor, username)
    if db_reply is None:
        return None
    return User(**db_reply)


async def authenticate_user_credentials(
    cursor: Cursor, username: str, password: str
) -> None:
    user = await get_user(cursor, username)

    if user is None:
        raise AuthError

    password_correct = verify_password(password, user.hash)
    if not password_correct:
        raise AuthError


def response_with_auth_cookie(username: str) -> HTMLResponse:
    token = create_token(username)
    response = HTMLResponse()
    response.set_cookie("authCookie", token)
    response.headers.append("HX-Location", "/")
    return response


async def validate_sign_up_credentials(
    cursor: Cursor, username: str, password: str, password2: str
) -> None:
    username_to_short = len(username) < config.min_username_len
    if username_to_short:
        raise SignUpError

    username_taken = await db.get_user(cursor, username) is not None
    if username_taken:
        raise SignUpError

    if not is_password_secure(password):
        raise SignUpError

    passwords_equal = password == password2
    if not passwords_equal:
        raise SignUpError


async def username_validation_context(cursor: Cursor, username: str):
    username_to_short = len(username) < config.min_username_len
    if username_to_short:
        return {
            "username": username,
            "username_to_short": username_to_short,
        }

    username_taken = await db.get_user(cursor, username) is not None
    return {
        "username": username,
        "username_taken": username_taken,
    }
