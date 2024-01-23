from typing import Annotated
from fastapi import Form, Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from app import templates
from app.database import CursorD
from app.users.dependencies import UserD, UserOrNoneD


from . import service
from .dependencies import PaginationD


router = APIRouter(tags=["url"])


@router.post("/url/")
async def add_url(
    request: Request,
    cursor: CursorD,
    user: UserOrNoneD,
    url: Annotated[str, Form()],
):
    short = await service.add_url(cursor, url, user and user.user_id)
    short_link = service.get_short_link(short)
    return templates.TemplateResponse(
        request=request,
        name="partial/url_short.html",
        context={"short": short_link},
    )


@router.get("/url/my-urls")
async def get_user_urls(
    request: Request,
    cursor: CursorD,
    user: UserD,
):
    context = await service.get_first_user_urls_context(cursor, user.user_id)
    return templates.TemplateResponse(
        request=request,
        name="pages/user_urls.html",
        context=context,
    )


@router.get("/url/my-urls/pag/")
async def get_user_urls_pagination(
    request: Request,
    cursor: CursorD,
    user: UserD,
    pagination: PaginationD,
):
    context = await service.get_user_url_table_context(
        cursor=cursor,
        user_id=user.user_id,
        size=pagination.size,
        offset=pagination.offset,
    )
    return templates.TemplateResponse(
        request=request,
        name="partial/url_table_pag.html",
        context=context,
    )


@router.get("/url/invalid-url")
def invalid_url(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/url_validation.html",
    )


@router.get("/{short}")
async def redirect(
    cursor: CursorD,
    short: str,
):
    long_url = await service.get_long_url(cursor, short)
    await service.increment_url_count(cursor, short)
    return RedirectResponse(long_url)
