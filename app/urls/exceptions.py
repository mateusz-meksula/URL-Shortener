from fastapi import HTTPException, Request, Response, status

from app import HtmxEvents


class UrlNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404)


class InvalidUrl(Exception):
    hx_trigger = HtmxEvents.INVALID_URL


def invalid_url_exception_handler(request: Request, exc: InvalidUrl) -> Response:
    return Response(
        content=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"HX-Trigger": str(exc.hx_trigger)},
    )
