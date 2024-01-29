from typing import TypedDict

from app.database import Cursor


class User(TypedDict):
    user_id: int
    name: str
    hash: str


class UserRepository:
    def __init__(self, cursor: Cursor[User]) -> None:
        self.cursor = cursor

    async def add(self, username: str, hash: str) -> None:
        operation = """INSERT INTO user (name, hash)
        VALUES (%(name)s, %(hash)s)"""
        await self.cursor.execute(operation, {"name": username, "hash": hash})

    async def get(self, username: str) -> User | None:
        operation = "SELECT * FROM user WHERE name = %(username)s"
        await self.cursor.execute(operation, {"username": username})
        return await self.cursor.fetchone()
