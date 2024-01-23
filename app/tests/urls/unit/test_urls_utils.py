import pytest

from app.urls.utils import is_url_valid


@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("", False),
        ("garbage", False),
        ("@#$#^#23", False),
        (".com", False),
        ("www.", False),
        ("www.com", False),
        ("https://.com", False),
        ("http://.com", False),
        ("https://.org", False),
        ("http://.org", False),
        ("http://test.com", True),
        ("https://test.com", True),
        ("https://test.com/test", True),
        ("https://test.com/test/test", True),
        ("https://test.com/test/test?test=test", True),
        ("https://fastapi.tiangolo.com/advanced/security/http-basic-auth/", True),
    ),
)
def test_is_url_valid(input, expected):
    assert is_url_valid(input) == expected
