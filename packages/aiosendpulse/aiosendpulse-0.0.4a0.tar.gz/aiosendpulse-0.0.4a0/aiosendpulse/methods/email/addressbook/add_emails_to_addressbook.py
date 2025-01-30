from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import EmailDetail, Result


__all__ = ["AddEmailsToAddressbook"]


class AddEmailsToAddressbook(SendPulseMethod[Result]):
    addressbook_id: int
    emails: list[EmailDetail]

    __http_method__ = "POST"
    __api_endpoint__ = "/addressbooks/{addressbook_id}/emails"
    __returning__ = dict

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(addressbook_id=self.addressbook_id)),
            json=self.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )
