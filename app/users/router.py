from typing import Annotated

from fastapi import Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from fastapi_restful.cbv import cbv

from app import templates
from app.database import Cursor, get_cursor
from app.users.models import User

from .dependencies import SignInFormD, SignUpFormD, get_user_or_none
from .service import UserService

router = APIRouter()


@cbv(router)
class UserResource:
    cursor: Cursor = Depends(get_cursor)
    user: User | None = Depends(get_user_or_none)

    def __init__(self) -> None:
        self.service = UserService(self.cursor)

    @router.get("/sign-in", response_class=HTMLResponse)
    def log_in(self, request: Request):
        return templates.TemplateResponse(
            request=request,
            name="pages/sign_in.html",
        )

    @router.post("/sign-in")
    async def login_for_token(self, form: SignInFormD):
        await self.service.authenticate_user_credentials(
            username=form.username,
            password=form.password,
        )

        response = self.service.response_with_auth_cookie(form.username)
        return response

    @router.get("/sign-up", response_class=HTMLResponse)
    def sign_in(self, request: Request):
        return templates.TemplateResponse(
            request=request,
            name="pages/sign_up.html",
        )

    @router.post("/sign-up")
    async def create_user(self, form: SignUpFormD):
        await self.service.validate_sign_up_credentials(
            username=form.username,
            password=form.password,
            password2=form.password2,
        )

        await self.service.create_user(form.username, form.password)
        return Response(headers={"HX-Location": "/?userCreated=true"})

    @router.get("/log-out")
    def log_out(self):
        response = RedirectResponse("/")
        if self.user:
            response.delete_cookie("authCookie")
        return response

    @router.post("/sign-up/validate/username")
    async def validate_username(
        self,
        request: Request,
        username: Annotated[str, Form()],
    ):
        context = await self.service.username_validation_context(username)
        return templates.TemplateResponse(
            request=request,
            name="partial/username_validation.html",
            context=context,
        )

    @router.get("/sign-in/error")
    def show_sign_in_error(self, request: Request):
        return templates.TemplateResponse(
            request=request,
            name="partial/sign_in_unsuccessful.html",
        )

    @router.get("/sign-up/error")
    def show_sign_up_error(self, request: Request):
        return templates.TemplateResponse(
            request=request,
            name="partial/sign_up_unsuccessful.html",
        )
