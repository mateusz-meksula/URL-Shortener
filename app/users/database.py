from typing import TypedDict

from app.database import Cursor


class User(TypedDict):
    user_id: int
    name: str
    hash: str


async def create_user(
    cursor: Cursor,
    username: str,
    hash: str,
) -> None:
    operation = """INSERT INTO user (name, hash)
    VALUES (%(name)s, %(hash)s)"""
    await cursor.execute(operation, {"name": username, "hash": hash})


async def get_user(cursor: Cursor[User], username: str) -> User | None:
    operation = "SELECT * FROM user WHERE name = %(username)s"
    await cursor.execute(operation, {"username": username})
    return await cursor.fetchone()
