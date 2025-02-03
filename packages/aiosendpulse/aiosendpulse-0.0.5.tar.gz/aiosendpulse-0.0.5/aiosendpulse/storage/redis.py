from datetime import timedelta
from typing import Union

from redis import ConnectionError as RedisConnectionError
from redis.asyncio import Redis

from .base import BaseTokenStorage
from .exceptions import CacheUnavailableError


__all__ = ["RedisTokenStorage"]


class RedisTokenStorage(BaseTokenStorage):
    def __init__(self, redis: Redis, key: str = "SENDPULSE_TOKEN") -> None:
        self.redis = redis
        self.key = key

    async def set(self, token: str, ex: Union[int, timedelta] = 3600) -> None:
        try:
            await self.redis.set(name=self.key, value=token, ex=ex)
        except RedisConnectionError as e:
            raise CacheUnavailableError from e

    async def get(self) -> Union[str, None]:
        try:
            token = await self.redis.get(name=self.key)
            if token:
                return token.decode()
        except RedisConnectionError as e:
            raise CacheUnavailableError from e
