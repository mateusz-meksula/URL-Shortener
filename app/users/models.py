from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    hash: str
