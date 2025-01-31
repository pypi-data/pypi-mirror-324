from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Union


__all__ = ["BaseTokenStorage"]


class BaseTokenStorage(ABC):
    @abstractmethod
    async def set(self, token: str, ex: Union[int, timedelta]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self) -> Union[str, None]:
        raise NotImplementedError()
