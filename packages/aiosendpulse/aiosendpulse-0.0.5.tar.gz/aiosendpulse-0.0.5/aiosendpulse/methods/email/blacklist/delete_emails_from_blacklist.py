from base64 import b64encode
from functools import cached_property

from httpx import URL, Request
from pydantic import EmailStr, computed_field

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Result


class DeleteEmailsFromBlacklist(SendPulseMethod[Result]):
    emails: list[EmailStr]

    __http_method__ = "DELETE"
    __api_endpoint__ = "/blacklist"
    __returning__ = Result

    @computed_field(return_type=str)
    @cached_property
    def encoded_emails(self) -> str:
        return b64encode(",".join(self.emails).encode()).decode()

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__),
            json={
                "emails": self.encoded_emails,
            },
        )
