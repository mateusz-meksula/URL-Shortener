from typing import Annotated, TypeAlias

from fastapi import Cookie, Depends, Form

from app.database import CursorD

from .utils import get_username_from_token
from .models import User
from .service import get_user
from .exceptions import UserNotLoggedIn


class UserSignUpForm:
    def __init__(
        self,
        *,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        password2: Annotated[str, Form()],
    ) -> None:
        self.username = username
        self.password = password
        self.password2 = password2


class UserSignInForm:
    def __init__(
        self,
        *,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ):
        self.username = username
        self.password = password


async def get_user_or_none(
    cursor: CursorD,
    authCookie: Annotated[str | None, Cookie()] = None,
) -> User | None:
    if not authCookie:
        return None

    username = get_username_from_token(authCookie)
    user = await get_user(cursor, username)
    return user


async def get_current_user(
    user_or_none: Annotated[User | None, Depends(get_user_or_none)]
) -> User:
    if user_or_none is None:
        raise UserNotLoggedIn
    return user_or_none


UserOrNoneD: TypeAlias = Annotated[User | None, Depends(get_user_or_none)]
UserD: TypeAlias = Annotated[User, Depends(get_current_user)]
SignUpFormD: TypeAlias = Annotated[UserSignUpForm, Depends()]
SignInFormD: TypeAlias = Annotated[UserSignInForm, Depends()]
