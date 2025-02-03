from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import TotalEmails


__all__ = ["GetTotalEmails"]


class GetTotalEmails(SendPulseMethod[TotalEmails]):
    id: int

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}/emails/total"

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__),
        )
