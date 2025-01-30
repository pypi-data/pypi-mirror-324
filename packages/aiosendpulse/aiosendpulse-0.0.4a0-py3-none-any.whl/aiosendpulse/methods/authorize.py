from typing import Literal

from httpx import URL, Request

from aiosendpulse.types import Token

from .base import SendPulseMethod


__all__ = ["Authorize"]


class Authorize(SendPulseMethod[Token]):
    grant_type: Literal["client_credentials"]
    client_id: str
    client_secret: str

    __http_method__ = "POST"
    __api_endpoint__ = "/oauth/access_token"
    __returning__ = Token

    def build_request(self, base_url: URL):
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__),
            json={
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
