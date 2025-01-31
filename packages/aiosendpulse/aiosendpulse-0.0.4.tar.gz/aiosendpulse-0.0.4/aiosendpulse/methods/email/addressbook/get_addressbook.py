from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Addressbook


__all__ = ["GetAddressbook"]


class GetAddressbook(SendPulseMethod[list[Addressbook]]):
    id: int

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}"
    __returning__ = list[Addressbook]

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
        )
