from jose import jwt
from passlib.context import CryptContext

from app.config import Config

config = Config()
SECRET_KEY = config.secret_key
ALGORITHM = config.algorithm


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(username: str):
    token = jwt.encode({"username": username}, SECRET_KEY, ALGORITHM)
    return token


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def get_username_from_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    return payload["username"]


def is_password_secure(password: str) -> bool:
    has_min_len = len(password) >= config.min_password_len
    if not has_min_len:
        return False

    has_uppercase_and_lowercase = (password.lower() != password) and (
        password.upper() != password
    )
    if not has_uppercase_and_lowercase:
        return False

    has_different_chars = len(set(password)) >= len(password) / 2
    if not has_different_chars:
        return False

    has_special_chars = bool(set("!@#$%^&*") & set(password))
    if not has_special_chars:
        return False

    has_numbers = bool(set(range(10)) & set(int(ch) for ch in password if ch.isdigit()))
    if not has_numbers:
        return False

    return True
