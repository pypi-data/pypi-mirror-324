from base64 import b64encode
from functools import cached_property
from typing import Union

from httpx import URL, Request
from pydantic import computed_field

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Result


__all__ = ["EditTemplate"]


class EditTemplate(SendPulseMethod[Result]):
    id: Union[str, int]
    body: str

    __http_method__ = "POST"
    __api_endpoint__ = "/template/edit/{id}"
    __returning__ = Result

    @computed_field(return_type=str)
    @cached_property
    def encoded_body(self) -> str:
        return b64encode(self.body.encode()).decode()

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
            json={
                "body": self.encoded_body,
            },
        )
