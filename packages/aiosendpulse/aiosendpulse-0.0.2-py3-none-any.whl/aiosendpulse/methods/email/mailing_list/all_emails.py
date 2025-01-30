from typing import Union

from httpx import URL, Request

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import EmailDetail


__all__ = ["GetEmailsList"]


class GetEmailsList(SendPulseMethod[list[EmailDetail]]):
    id: int
    limit: Union[int, None] = None
    offset: Union[int, None] = None
    active: Union[bool, None] = None
    not_active: Union[bool, None] = None

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}/emails"
    __returning__ = list[EmailDetail]

    def build_request(self, base_url: URL) -> Request:
        return Request(
            method=self.__http_method__,
            url=base_url.join(url=self.__api_endpoint__.format(id=self.id)),
            params=self.model_dump(exclude_none=True, exclude_unset=True, exclude={"id"}),
        )
