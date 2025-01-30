from typing import Union

from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import Template


__all__ = ["GetTemplate"]


class GetTemplate(SendPulseMethod[Template]):
    template_id: Union[int, str]

    __http_method__ = "GET"
    __api_endpoint__ = "/template/{template_id}"
    __returning__ = Template

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(template_id=self.template_id)),
        )
