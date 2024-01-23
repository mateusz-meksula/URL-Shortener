import pytest

from app.users.utils import is_password_secure, create_token, get_username_from_token


@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("", False),
        ("short", False),
        ("loooooooooong", False),
        ("upperLooooong", False),
        ("UpperHasChars$%", False),
        ("7128768176318263", False),
        ("!@#!@@$@#$@#$@#", False),
        ("AAAAAAAAAAAAA$AAA4", False),
        ("aAAAAAAAAAAAA$AAA4", False),
        ("aAAAAAAbcAAAAA$AAA4", False),
        ("UpperHasChars$and4", True),
    ),
)
def test_is_password_secure(input, expected):
    assert is_password_secure(input) == expected
