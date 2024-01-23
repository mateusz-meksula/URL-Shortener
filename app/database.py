from typing import Annotated, TypeAlias, Generic, TypeVar

from fastapi import Depends
from mysql.connector.aio import connect
from mysql.connector.aio.cursor import MySQLCursorDict

from app.config import Config


config = Config()


T = TypeVar("T")


class Cursor(MySQLCursorDict, Generic[T]):
    async def fetchone(self) -> T | None:
        return await super().fetchone()  # type: ignore

    async def fetchall(self) -> list[T]:
        ret = await super().fetchall()
        match ret:
            case [None]:
                return []
            case _:
                return ret  # type: ignore


async def get_connection():
    return await connect(
        host=config.db_host,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
    )


async def get_cursor():
    connection = await get_connection()
    cursor = await connection.cursor(dictionary=True)
    yield cursor
    await connection.commit()
    await cursor.close()
    await connection.close()


CursorD: TypeAlias = Annotated[Cursor, Depends(get_cursor)]
