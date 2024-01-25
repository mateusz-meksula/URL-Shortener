# type: ignore
import pytest
from unittest.mock import patch
from app.urls.exceptions import InvalidUrl, UrlNotFound

from app.urls.service import (
    generate_unique_short,
    get_user_urls_count,
    add_url,
    get_long_url,
    get_first_user_urls_context,
)

pytest_plugins = ("pytest_asyncio",)


DB_PATH = "app.urls.database"
SERVICE_PATH = "app.urls.service"


@pytest.mark.asyncio
async def test_generate_unique_short():
    with patch(f"{DB_PATH}.get_long_url", return_value=None):
        short = await generate_unique_short(None)
        assert isinstance(short, str)
        assert len(short) == 6


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("db_ret", "expected"),
    (
        (None, 0),
        ({"count": 0}, 0),
        ({"count": 5}, 5),
    ),
)
async def test_get_user_urls_count_not_none(db_ret, expected):
    with patch(f"{DB_PATH}.get_user_urls_count", return_value=db_ret):
        count = await get_user_urls_count(None, 1)
        assert count == expected


@pytest.mark.asyncio
async def test_add_url_raises_invalid_url():
    with patch(f"{SERVICE_PATH}.is_url_valid", return_value=False):
        with pytest.raises(InvalidUrl):
            await add_url(None, None, None)


@pytest.mark.asyncio
@patch(f"{SERVICE_PATH}.is_url_valid", return_value=True)
@patch(f"{SERVICE_PATH}.generate_unique_short", return_value="qwerty")
@patch(f"{DB_PATH}.add_url", return_value=None)
async def test_add_url(*_):
    ret = await add_url(None, None, None)
    assert ret == "qwerty"


@pytest.mark.asyncio
@patch(f"{DB_PATH}.get_long_url", return_value=None)
async def test_get_long_url_raises_url_not_found(_):
    with pytest.raises(UrlNotFound):
        await get_long_url(None, None)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("db_ret", "expected"),
    (
        ({"long_url": "test"}, "test"),
        ({"long_url": "testtest"}, "testtest"),
        ({"long_url": "abcdef"}, "abcdef"),
    ),
)
async def test_get_long_url(db_ret, expected):
    with patch(f"{DB_PATH}.get_long_url", return_value=db_ret):
        ret = await get_long_url(None, None)
        assert ret == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("count", "zero_urls"),
    (
        (0, True),
        (1, False),
        (111, False),
    ),
)
async def test_get_first_user_urls_context(count, zero_urls):
    with patch(f"{SERVICE_PATH}.get_user_urls_count", return_value=count):
        ret = await get_first_user_urls_context(None, None)
        assert ret == {"logged": True, "zero_urls": zero_urls}
