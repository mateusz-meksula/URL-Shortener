from typing import Annotated, TypeAlias

from fastapi import Depends, Query


class Pagination:
    def __init__(
        self,
        offset: Annotated[int, Query()],
        size: Annotated[int, Query()] = 5,
    ) -> None:
        self.size = size
        self.offset = offset


PaginationD: TypeAlias = Annotated[Pagination, Depends()]
