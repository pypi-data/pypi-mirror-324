from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Result


__all__ = ["EditMailingList"]


class EditMailingList(SendPulseMethod[Result]):
    id: int
    name: str

    __http_method__ = "PUT"
    __api_endpoint__ = "/addressbooks/{id}"
    __returning__ = Result

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
            json={
                "name": self.name,
            },
        )
