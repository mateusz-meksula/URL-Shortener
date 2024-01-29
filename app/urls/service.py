from random import choice
from string import ascii_letters

from app.config import Config
from app.database import Cursor

from .database import UrlRepository
from .exceptions import InvalidUrl, UrlNotFound
from .models import UrlModel
from .utils import get_short_link, is_url_valid

config = Config()


class UrlService:
    def __init__(self, cursor: Cursor) -> None:
        self.url_repo = UrlRepository(cursor)

    async def generate_unique_short(self) -> str:
        while True:
            short = "".join(choice(ascii_letters) for _ in range(config.short_length))
            short_exist = await self.url_repo.get(short) is not None
            if not short_exist:
                break
        return short

    async def get_user_urls_count(self, user_id: int) -> int:
        db_reply = await self.url_repo.get_user_urls_count(user_id)
        return db_reply["count"] if db_reply else 0

    async def add_url(self, long_url: str, user_id: int | None) -> str:
        if not is_url_valid(long_url):
            raise InvalidUrl
        short = await self.generate_unique_short()
        await self.url_repo.add(short, long_url, user_id)
        return get_short_link(short)

    async def get_long_url(self, short: str) -> str:
        db_reply = await self.url_repo.get(short)
        if db_reply is None:
            raise UrlNotFound
        return db_reply["long_url"]

    async def get_user_url_table_context(
        self,
        user_id: int,
        size: int,
        offset: int,
    ):
        db_url_rows = await self.url_repo.get_all(
            user_id=user_id,
            size=size,
            offset=offset,
        )

        urls = [UrlModel(**row) for row in db_url_rows]
        for i, url in enumerate(urls, start=offset + 1):
            url.table_lp = i
            url.short = get_short_link(url.short)

        urls_count = await self.get_user_urls_count(user_id)
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

    async def increment_url_count(self, short: str) -> None:
        db_url_count = await self.url_repo.get(short)
        count: int = db_url_count["count"]  # type: ignore
        count += 1
        await self.url_repo.update(short, count)
