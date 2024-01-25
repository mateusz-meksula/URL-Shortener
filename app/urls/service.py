from random import choice
from string import ascii_letters

from app.config import Config
from app.database import Cursor

from . import database as db
from .models import UrlModel
from .utils import is_url_valid
from .exceptions import InvalidUrl, UrlNotFound


config = Config()


async def generate_unique_short(cursor: Cursor) -> str:
    while True:
        short = "".join(choice(ascii_letters) for _ in range(config.short_length))
        short_exist = await db.get_long_url(cursor, short) is not None
        if not short_exist:
            break
    return short


async def get_user_urls_count(cursor: Cursor, user_id: int) -> int:
    db_reply = await db.get_user_urls_count(cursor, user_id)
    return db_reply["count"] if db_reply else 0


async def add_url(cursor: Cursor, long_url: str, user_id: int | None) -> str:
    if not is_url_valid(long_url):
        raise InvalidUrl
    short = await generate_unique_short(cursor)
    await db.add_url(cursor, short, long_url, user_id)
    return short


async def get_long_url(cursor: Cursor, short: str) -> str:
    db_reply = await db.get_long_url(cursor, short)
    if db_reply is None:
        raise UrlNotFound
    return db_reply["long_url"]


async def get_first_user_urls_context(cursor: Cursor, user_id: int):
    urls_count = await get_user_urls_count(cursor, user_id)
    return {
        "logged": True,
        "zero_urls": urls_count == 0,
    }


async def get_user_url_table_context(
    cursor: Cursor,
    user_id: int,
    size: int,
    offset: int,
):
    db_url_rows = await db.get_user_urls(
        cursor=cursor,
        user_id=user_id,
        size=size,
        offset=offset,
    )
    urls = [UrlModel(**row) for row in db_url_rows]
    for i, url in enumerate(urls, start=offset + 1):
        url.table_lp = i
        url.short = get_short_link(url.short)

    urls_count = await get_user_urls_count(cursor, user_id)
    is_next_available = urls_count > offset + size
    is_previous_available = offset != 0

    context = {
        "urls": urls,
        "logged": True,
        "size": size,
        "is_next_available": is_next_available,
        "is_previous_available": is_previous_available,
    }

    if is_previous_available:
        context |= {"offset_p": offset - size}

    if is_next_available:
        context |= {"offset_n": offset + size}

    return context


async def increment_url_count(cursor: Cursor, short: str) -> None:
    db_url_count = await db.get_url_count(cursor, short)
    count: int = db_url_count["count"]  # type: ignore
    count += 1
    await db.increment_url_count(cursor, short, count)


def get_short_link(short: str) -> str:
    return f"{config.origin}/{short}"
