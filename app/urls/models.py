from datetime import datetime

from pydantic import BaseModel


class UrlModel(BaseModel):
    url_id: int
    user_id: int | None
    short: str
    long_url: str
    count: int
    created: datetime
    table_lp: int | None = None
