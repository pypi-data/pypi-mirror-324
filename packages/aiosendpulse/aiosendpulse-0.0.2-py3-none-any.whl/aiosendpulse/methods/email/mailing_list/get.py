from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import MailingList


__all__ = ["GetMailingList"]


class GetMailingList(SendPulseMethod[list[MailingList]]):
    id: int

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}"
    __returning__ = list[MailingList]

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
        )
