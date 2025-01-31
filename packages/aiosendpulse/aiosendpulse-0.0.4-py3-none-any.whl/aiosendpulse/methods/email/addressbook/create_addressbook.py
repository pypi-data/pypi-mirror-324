from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import AddressbookId


__all__ = ["CreateAddressbook"]


class CreateAddressbook(SendPulseMethod[AddressbookId]):
    book_name: str

    __http_method__ = "POST"
    __api_endpoint__ = "/addressbooks"
    __returning__ = AddressbookId

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__, url=base_url.join(url=self.__api_endpoint__), json={"bookName": self.book_name}
        )
