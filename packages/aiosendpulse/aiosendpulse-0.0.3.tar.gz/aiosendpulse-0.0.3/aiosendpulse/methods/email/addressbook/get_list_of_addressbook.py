from typing import Union

from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Addressbook


__all__ = ["GetListOfAddressbook"]


class GetListOfAddressbook(SendPulseMethod[list[Addressbook]]):
    limit: Union[int, None] = None
    offset: Union[int, None] = None

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks"
    __returning__ = list[Addressbook]

    def build_request(self, base_url: URL) -> Request:
        params = {}
        if self.limit is not None:
            params["limit"] = self.limit

        if self.offset is not None:
            params["offset"] = self.offset

        return Request(
            method=self.__http_method__,
            url=base_url.join(self.__api_endpoint__),
            params=params,
        )
