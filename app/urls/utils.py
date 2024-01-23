from urllib.parse import urlparse


def is_url_valid(url: str) -> bool:
    try:
        result = urlparse(url)
        host, *_ = result.netloc.split(".")
        return all((result.scheme, result.netloc, host))
    except ValueError:
        return False
