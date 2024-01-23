from enum import Enum
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")


class HtmxEvents(Enum):
    UNSUCCESSFUL_SIGN_IN = "unsuccessfulSignIn"
    UNSUCCESSFUL_SIGN_UP = "unsuccessfulSignUp"
    INVALID_URL = "invalidUrl"

    def __str__(self) -> str:
        return self.value
