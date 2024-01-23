from typing import Annotated

from fastapi import Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter

from app import HtmxEvents, templates
from app.database import CursorD

from . import service
from .dependencies import SignInFormD, SignUpFormD, UserOrNoneD


router = APIRouter()


@router.get("/sign-in", response_class=HTMLResponse)
def log_in(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/sign_in.html",
    )


@router.post("/sign-in")
async def login_for_token(cursor: CursorD, form: SignInFormD):
    await service.authenticate_user_credentials(
        cursor=cursor,
        username=form.username,
        password=form.password,
    )

    response = service.response_with_auth_cookie(form.username)
    return response


@router.get("/sign-up", response_class=HTMLResponse)
def sign_in(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/sign_up.html",
    )


@router.post("/sign-up")
async def create_user(cursor: CursorD, form: SignUpFormD):
    await service.validate_sign_up_credentials(
        cursor=cursor,
        username=form.username,
        password=form.password,
        password2=form.password2,
    )

    await service.create_user(cursor, form.username, form.password)
    return Response(headers={"HX-Location": "/?userCreated=true"})


@router.get("/log-out")
def log_out(user: UserOrNoneD):
    response = RedirectResponse("/")
    if user:
        response.delete_cookie("authCookie")
    return response


@router.post("/sign-up/validate/username")
async def validate_username(
    request: Request,
    cursor: CursorD,
    username: Annotated[str, Form()],
):
    context = await service.username_validation_context(cursor, username)
    return templates.TemplateResponse(
        request=request,
        name="partial/username_validation.html",
        context=context,
    )


@router.get("/sign-in/error")
def show_sign_in_error(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/sign_in_unsuccessful.html",
    )


@router.get("/sign-up/error")
def show_sign_up_error(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/sign_up_unsuccessful.html",
    )
