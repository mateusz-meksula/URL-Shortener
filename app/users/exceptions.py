from fastapi import HTTPException, Request, Response, status

from app import HtmxEvents


class UserNotLoggedIn(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthError(Exception):
    hx_trigger = HtmxEvents.UNSUCCESSFUL_SIGN_IN


class SignUpError(Exception):
    hx_trigger = HtmxEvents.UNSUCCESSFUL_SIGN_UP


def auth_exception_handler(request: Request, exc: AuthError) -> Response:
    return Response(
        content=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"HX-Trigger": str(exc.hx_trigger)},
    )


def sign_up_exception_handler(request: Request, exc: SignUpError) -> Response:
    return Response(
        content=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"HX-Trigger": str(exc.hx_trigger)},
    )
