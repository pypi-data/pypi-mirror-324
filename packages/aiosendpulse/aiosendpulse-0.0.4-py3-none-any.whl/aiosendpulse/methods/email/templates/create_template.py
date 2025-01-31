from base64 import b64encode
from functools import cached_property
from typing import Union

from httpx import URL, Request
from pydantic import computed_field
from pydantic_extra_types.language_code import LanguageAlpha2

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import CreateTemplateResult


__all__ = ["CreateTemplate"]


class CreateTemplate(SendPulseMethod[CreateTemplateResult]):
    name: Union[str, None] = None
    body: str
    lang: LanguageAlpha2

    __http_method__ = "POST"
    __api_endpoint__ = "/template"
    __returning__ = CreateTemplateResult

    @computed_field(return_type=str)
    @cached_property
    def encoded_body(self) -> str:
        return b64encode(self.body.encode()).decode()

    def build_request(self, base_url: URL) -> Request:
        data = {
            "body": self.encoded_body,
            "lang": self.lang,
        }
        if self.name:
            data["name"] = self.name

        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__),
            json=data,
        )
