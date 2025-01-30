from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import MailingListVariable


__all__ = ["GetListMailingListVariables"]


class GetListMailingListVariables(SendPulseMethod[list[MailingListVariable]]):
    id: int

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}/variables"
    __returning__ = list[MailingListVariable]

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
        )
