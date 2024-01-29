from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import templates
from app.urls.exceptions import InvalidUrl, invalid_url_exception_handler
from app.urls.router import router as urls_router
from app.users.dependencies import UserOrNoneD
from app.users.exceptions import (
    AuthError,
    SignUpError,
    auth_exception_handler,
    sign_up_exception_handler,
)
from app.users.router import router as users_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static_files"), name="static")
app.include_router(users_router)
app.include_router(urls_router)
app.add_exception_handler(InvalidUrl, invalid_url_exception_handler)  # type: ignore
app.add_exception_handler(AuthError, auth_exception_handler)  # type: ignore
app.add_exception_handler(SignUpError, sign_up_exception_handler)  # type: ignore


@app.get("/")
async def homepage(
    request: Request,
    user: UserOrNoneD,
    userCreated: bool = False,
):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "logged": bool(user),
            "user_created": userCreated,
        },
    )


@app.get("/favicon.ico")
async def get_favicon():
    return RedirectResponse("https://fastapi.tiangolo.com/img/favicon.png")


@app.exception_handler(status.HTTP_404_NOT_FOUND)
@app.exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED)
def not_found_page(request: Request, _):
    return templates.TemplateResponse(
        request=request,
        name="pages/404.html",
        headers={"HX-Retarget": "body"},
    )


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
def unauthorized_page(request: Request, _):
    return templates.TemplateResponse(
        request=request,
        name="pages/401.html",
        headers={"HX-Retarget": "body"},
    )


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error_page(request: Request, _):
    return templates.TemplateResponse(
        request=request,
        name="pages/500.html",
        headers={"HX-Retarget": "body"},
    )
