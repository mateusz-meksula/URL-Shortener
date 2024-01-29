from typing import Annotated

from fastapi import Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from fastapi_restful.cbv import cbv

from app import templates
from app.database import Cursor, get_cursor
from app.users.dependencies import UserD, get_user_or_none
from app.users.models import User

from .dependencies import PaginationD
from .service import UrlService

router = APIRouter(tags=["url"])


@cbv(router)
class UrlResource:
    cursor: Cursor = Depends(get_cursor)
    user: User | None = Depends(get_user_or_none)

    def __init__(self) -> None:
        self.service = UrlService(self.cursor)

    @router.post("/url/")
    async def add_url(
        self,
        request: Request,
        url: Annotated[str, Form()],
    ):
        short = await self.service.add_url(url, self.user and self.user.user_id)
        return templates.TemplateResponse(
            request=request,
            name="partial/url_short.html",
            context={"short": short},
        )

    @router.get("/url/my-urls")
    async def get_user_urls(
        self,
        request: Request,
        user: UserD,
    ):
        zero_urls = await self.service.get_user_urls_count(user.user_id) == 0
        return templates.TemplateResponse(
            request=request,
            name="pages/user_urls.html",
            context={
                "logged": True,
                "zero_urls": zero_urls,
            },
        )

    @router.get("/url/my-urls/pag/")
    async def get_user_urls_pagination(
        self,
        request: Request,
        user: UserD,
        pagination: PaginationD,
    ):
        context = await self.service.get_user_url_table_context(
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
    def invalid_url(self, request: Request):
        return templates.TemplateResponse(
            request=request,
            name="partial/url_validation.html",
        )

    @router.get("/{short}")
    async def redirect(
        self,
        short: str,
    ):
        long_url = await self.service.get_long_url(short)
        await self.service.increment_url_count(short)
        return RedirectResponse(long_url)
