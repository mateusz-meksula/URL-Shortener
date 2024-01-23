from datetime import datetime
from typing import TypedDict

from app.database import Cursor


class LongUrl(TypedDict):
    long_url: str


class Count(TypedDict):
    count: int


class Url(TypedDict):
    url_id: int
    user_id: int | None
    short: str
    long_url: str
    count: int
    created: datetime


async def add_url(
    cursor: Cursor, short: str, long_url: str, user_id: int | None
) -> None:
    operation = """INSERT INTO url (user_id, short, long_url)
    VALUES (%(user_id)s, %(short)s, %(long_url)s)"""
    await cursor.execute(
        operation,
        {
            "user_id": user_id,
            "short": short,
            "long_url": long_url,
        },
    )


async def get_long_url(cursor: Cursor[LongUrl], short: str) -> LongUrl | None:
    operation = "SELECT long_url FROM url WHERE short = %(short)s"
    await cursor.execute(operation, {"short": short})
    return await cursor.fetchone()


async def get_user_urls_count(cursor: Cursor[Count], user_id: int) -> Count | None:
    operation = "SELECT count(url_id) count FROM url WHERE user_id = %(user_id)s"
    await cursor.execute(operation, {"user_id": user_id})
    return await cursor.fetchone()


async def get_user_urls(
    cursor: Cursor[Url],
    user_id: int,
    size: int,
    offset: int,
) -> list[Url]:
    operation = """
    SELECT * FROM url
    WHERE user_id = %(user_id)s
    LIMIT %(size)s
    OFFSET %(offset)s
    """
    await cursor.execute(
        operation,
        {
            "user_id": user_id,
            "size": size,
            "offset": offset,
        },
    )
    return await cursor.fetchall()


async def get_url_count(cursor: Cursor[Count], short: str) -> Count | None:
    operation = "SELECT count FROM url WHERE short = %(short)s"
    await cursor.execute(operation, {"short": short})
    return await cursor.fetchone()


async def increment_url_count(cursor: Cursor, short: str, count: int) -> None:
    operation = "UPDATE url SET count = %(count)s WHERE short = %(short)s"
    await cursor.execute(operation, {"count": count, "short": short})
