from datetime import datetime
from typing import TypedDict

from app.database import Cursor


class Count(TypedDict):
    count: int


class Url(TypedDict):
    url_id: int
    user_id: int | None
    short: str
    long_url: str
    count: int
    created: datetime


class UrlRepository:
    def __init__(self, cursor: Cursor[Url]) -> None:
        self.cursor = cursor

    async def add(self, short: str, long_url: str, user_id: int | None) -> None:
        operation = """INSERT INTO url (user_id, short, long_url)
        VALUES (%(user_id)s, %(short)s, %(long_url)s)"""
        await self.cursor.execute(
            operation,
            {
                "user_id": user_id,
                "short": short,
                "long_url": long_url,
            },
        )

    async def get(self, short: str) -> Url | None:
        operation = "SELECT * FROM url WHERE short = %(short)s"
        await self.cursor.execute(operation, {"short": short})
        return await self.cursor.fetchone()

    async def update(self, short: str, count: int) -> None:
        operation = "UPDATE url SET count = %(count)s WHERE short = %(short)s"
        await self.cursor.execute(operation, {"count": count, "short": short})

    async def get_all(self, user_id: int, size: int, offset: int) -> list[Url]:
        operation = """
        SELECT * FROM url
        WHERE user_id = %(user_id)s
        LIMIT %(size)s
        OFFSET %(offset)s
        """
        await self.cursor.execute(
            operation,
            {
                "user_id": user_id,
                "size": size,
                "offset": offset,
            },
        )
        return await self.cursor.fetchall()

    async def get_user_urls_count(self, user_id: int) -> Count | None:
        operation = "SELECT count(url_id) count FROM url WHERE user_id = %(user_id)s"
        await self.cursor.execute(operation, {"user_id": user_id})
        return await self.cursor.fetchone()
