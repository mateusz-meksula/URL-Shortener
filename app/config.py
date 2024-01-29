from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    origin: str = Field()
    #
    secret_key: str
    algorithm: str
    #
    db_host: str = Field(alias="MYSQL_HOST")
    db_user: str = Field(alias="MYSQL_USER")
    db_password: str = Field(alias="MYSQL_PASSWORD")
    db_name: str = "shortener"
    #
    short_length: int = 6
    default_url_table_size: int = 5
    min_username_len: int = 4
    min_password_len: int = 10


@cache
def Config():
    return _Config()  # type: ignore
