from base64 import b64encode
from functools import cached_property
from typing import Union

from httpx import URL, Request
from pydantic import EmailStr, computed_field

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Result


class AddEmailsToBlacklist(SendPulseMethod[Result]):
    emails: list[EmailStr]
    comment: Union[str, None] = None

    __http_method__ = "POST"
    __api_endpoint__ = "/blacklist"
    __returning__ = Result

    @computed_field(return_type=str)
    @cached_property
    def encoded_emails(self) -> str:
        return b64encode(",".join(self.emails).encode()).decode()

    def build_request(self, base_url: URL) -> Request:
        data = {
            "emails": self.encoded_emails,
        }

        if self.comment:
            data["comment"] = self.comment

        return Request(method=self.__http_method__, url=base_url.join(url=self.__api_endpoint__), json=data)
