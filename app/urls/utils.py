from urllib.parse import urlparse

from app.config import Config

config = Config()


def is_url_valid(url: str) -> bool:
    try:
        result = urlparse(url)
        host, *_ = result.netloc.split(".")
        return all((result.scheme, result.netloc, host))
    except ValueError:
        return False


def get_short_link(short: str) -> str:
    return f"{config.origin}/{short}"
