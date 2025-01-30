from __future__ import annotations

from typing import TYPE_CHECKING, Union

from httpx import AsyncClient


if TYPE_CHECKING:
    from aiosendpulse import AioSendPulseClient
    from aiosendpulse.auth import BearerTokenAuth


__all__ = ["BaseService"]


class BaseService:
    def __init__(self, client: AioSendPulseClient) -> None:
        self.client = client

    @property
    def http_client(self) -> AsyncClient:
        return self.client.http_client

    @property
    def auth(self) -> Union[BearerTokenAuth, None]:
        return self.client.auth
